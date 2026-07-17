"""Fused W4A16 Kimi-Linear hybrid decode.

Custom fused int4 dequant-GEMV (Triton) -- the int4 unpack + group dequant is
fused directly into the matrix-vector product, so the bf16 weight is never
materialized. MLA uses the absorb formulation (weight-absorbed KV) so the
per-step cost is independent of the O(L*8192) cache-projection the baseline
pays. MoE routed/shared experts run through the same fused batched GEMV.
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F
import triton
import triton.language as tl

EPS = 1.0e-6
GROUP_SIZE = 128


# --------------------------------------------------------------------------- #
# Fused int4 dequant-GEMV : y[e,n] = sum_k x[e,k] * dequant(W[e])[k,n]
# W packed (K//2, N) uint8: even-k low nibble, odd-k high nibble.
# scales/zeros per (K//group, N).  BLOCK_P = group/2 -> one group per iter.
# --------------------------------------------------------------------------- #
@triton.jit
def _bgemv_kernel(X, WQ, S, Z, Y,
                  K, N, G,
                  sxe, sxk,
                  swe, swk, swn,
                  sse, ssg, ssn,
                  sye, syn,
                  BLOCK_N: tl.constexpr, BLOCK_P: tl.constexpr):
    e = tl.program_id(0)
    nb = tl.program_id(1)
    offs_n = nb * BLOCK_N + tl.arange(0, BLOCK_N)
    mask_n = offs_n < N
    parange = tl.arange(0, BLOCK_P)
    acc = tl.zeros([BLOCK_N], tl.float32)
    for g in range(0, G):
        p = g * BLOCK_P + parange
        ke = 2 * p
        ko = ke + 1
        xe = tl.load(X + e * sxe + ke * sxk).to(tl.float32)
        xo = tl.load(X + e * sxe + ko * sxk).to(tl.float32)
        wq = tl.load(WQ + e * swe + p[:, None] * swk + offs_n[None, :] * swn,
                     mask=mask_n[None, :], other=0)
        lo = (wq & 0xF).to(tl.float32)
        hi = ((wq >> 4) & 0xF).to(tl.float32)
        s = tl.load(S + e * sse + g * ssg + offs_n * ssn, mask=mask_n, other=0.0).to(tl.float32)
        z = tl.load(Z + e * sse + g * ssg + offs_n * ssn, mask=mask_n, other=0.0).to(tl.float32)
        sum_lohi = tl.sum(xe[:, None] * lo + xo[:, None] * hi, axis=0)
        sum_x = tl.sum(xe + xo, axis=0)
        acc += s * (sum_lohi - z * sum_x)
    tl.store(Y + e * sye + offs_n * syn, acc, mask=mask_n)


def _bgemv(X, WQ, S, Z, N, BLOCK_N=32, num_warps=1):
    """X[E,K] f32, WQ[E,K//2,N] u8, S/Z[E,G,N] bf16 -> Y[E,N] f32."""
    E = WQ.shape[0]
    KP = WQ.shape[1]
    G = KP // (GROUP_SIZE // 2)
    K = KP * 2
    Y = torch.empty((E, N), dtype=torch.float32, device=WQ.device)
    grid = (E, triton.cdiv(N, BLOCK_N))
    _bgemv_kernel[grid](
        X, WQ, S, Z, Y,
        K, N, G,
        X.stride(0), X.stride(1),
        WQ.stride(0), WQ.stride(1), WQ.stride(2),
        S.stride(0), S.stride(1), S.stride(2),
        Y.stride(0), Y.stride(1),
        BLOCK_N=BLOCK_N, BLOCK_P=GROUP_SIZE // 2, num_warps=num_warps,
    )
    return Y


def _gemv(x, ql):
    """single W4A16 matrix-vector; x[in] f32 -> [out] f32."""
    x = x.reshape(1, -1).float().contiguous()
    y = _bgemv(x, ql.w_q.unsqueeze(0), ql.scales.unsqueeze(0), ql.zeros.unsqueeze(0), ql.out_f)
    return y[0]


def _dequant_torch(w_q, scales, zeros, K, group=GROUP_SIZE):
    wu = torch.empty((K, w_q.shape[1]), dtype=torch.uint8, device=w_q.device)
    wu[0::2] = w_q & 0xF
    wu[1::2] = (w_q >> 4) & 0xF
    s = scales.repeat_interleave(group, dim=0)
    z = zeros.repeat_interleave(group, dim=0)
    return (wu.to(torch.bfloat16) - z) * s


# --------------------------------------------------------------------------- #
# quant containers (buffer layout identical to reference for state_dict load)
# --------------------------------------------------------------------------- #
class QuantLinear(nn.Module):
    def __init__(self, in_f, out_f, group=GROUP_SIZE):
        super().__init__()
        self.in_f, self.out_f, self.group = in_f, out_f, group
        ng = in_f // group
        self.register_buffer("w_q", torch.zeros(in_f // 2, out_f, dtype=torch.uint8))
        self.register_buffer("scales", torch.zeros(ng, out_f, dtype=torch.bfloat16))
        self.register_buffer("zeros", torch.zeros(ng, out_f, dtype=torch.bfloat16))


class QuantExperts(nn.Module):
    def __init__(self, n, in_f, out_f, group=GROUP_SIZE):
        super().__init__()
        self.n, self.in_f, self.out_f, self.group = n, in_f, out_f, group
        ng = in_f // group
        self.register_buffer("w_q", torch.zeros(n, in_f // 2, out_f, dtype=torch.uint8))
        self.register_buffer("scales", torch.zeros(n, ng, out_f, dtype=torch.bfloat16))
        self.register_buffer("zeros", torch.zeros(n, ng, out_f, dtype=torch.bfloat16))


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _rmsnorm(x, w):
    xf = x.float()
    xf = xf * torch.rsqrt(xf.pow(2).mean(-1, keepdim=True) + EPS)
    return (xf * w.float()).to(x.dtype)


def _rope_cossin(pos, dim, theta, device):
    inv = 1.0 / (theta ** (torch.arange(0, dim, 2, device=device, dtype=torch.float32) / dim))
    ang = pos * inv
    return torch.cos(ang), torch.sin(ang)


def _apply_rope(x, cos, sin):
    xf = x.float()
    even, odd = xf[..., 0::2], xf[..., 1::2]
    out = torch.empty_like(xf)
    out[..., 0::2] = even * cos - odd * sin
    out[..., 1::2] = odd * cos + even * sin
    return out.to(x.dtype)


# --------------------------------------------------------------------------- #
# layers
# --------------------------------------------------------------------------- #
class KDA(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        H, Dk, d = cfg.kda_heads, cfg.kda_head_dim, cfg.hidden
        self.q_proj = QuantLinear(d, H * Dk, cfg.group)
        self.k_proj = QuantLinear(d, H * Dk, cfg.group)
        self.v_proj = QuantLinear(d, H * Dk, cfg.group)
        self.g_proj = QuantLinear(d, H * Dk, cfg.group)
        self.beta_proj = nn.Linear(d, H, bias=False, dtype=cfg.dtype)
        self.conv_w = nn.Parameter(torch.empty(3, H * Dk, cfg.short_conv, dtype=cfg.dtype))
        self.o_proj = QuantLinear(H * Dk, d, cfg.group)
        self.scale = Dk ** -0.5
        self._qkvg = None

    def _qkvg_stack(self):
        if self._qkvg is None:
            wq = torch.stack([self.q_proj.w_q, self.k_proj.w_q,
                              self.v_proj.w_q, self.g_proj.w_q], 0)
            sc = torch.stack([self.q_proj.scales, self.k_proj.scales,
                              self.v_proj.scales, self.g_proj.scales], 0)
            zc = torch.stack([self.q_proj.zeros, self.k_proj.zeros,
                              self.v_proj.zeros, self.g_proj.zeros], 0)
            self._qkvg = (wq, sc, zc)
        return self._qkvg

    def _short_conv(self, val, prev, idx):
        win = torch.cat([prev, val[None]], dim=0)
        w = self.conv_w[idx].float().transpose(0, 1)
        out = (win.float() * w).sum(0)
        return F.silu(out).to(val.dtype), win[1:]

    def step(self, x, st):
        H, Dk = self.cfg.kda_heads, self.cfg.kda_head_dim
        wq, sc, zc = self._qkvg_stack()
        xin = x.reshape(1, -1).float().expand(4, -1).contiguous()
        y = _bgemv(xin, wq, sc, zc, H * Dk)   # [4, H*Dk]
        q = y[0].to(torch.bfloat16)
        k = y[1].to(torch.bfloat16)
        v = y[2].to(torch.bfloat16)
        q, st["cq"] = self._short_conv(q, st["cq"], 0)
        k, st["ck"] = self._short_conv(k, st["ck"], 1)
        v, st["cv"] = self._short_conv(v, st["cv"], 2)
        q = q.view(H, Dk).float() * self.scale
        k = k.view(H, Dk).float()
        v = v.view(H, Dk).float()
        g = (-F.softplus(y[3])).view(H, Dk)
        beta = torch.sigmoid(self.beta_proj(x).float())
        S = st["S"] * g.exp()[:, :, None]
        pred = (S * k[:, :, None]).sum(1)
        S = S + beta[:, None, None] * k[:, :, None] * (v - pred)[:, None, :]
        o = (S * q[:, :, None]).sum(1)
        st["S"] = S
        return _gemv(o.reshape(H * Dk).to(torch.bfloat16), self.o_proj).to(torch.bfloat16)


class MLA(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        H, d = cfg.mla_heads, cfg.hidden
        self.q_proj = QuantLinear(d, H * (cfg.qk_nope + cfg.qk_rope), cfg.group)
        self.kv_a = QuantLinear(d, cfg.kv_lora + cfg.qk_rope, cfg.group)
        self.kv_b = QuantLinear(cfg.kv_lora, H * (cfg.qk_nope + cfg.v_head), cfg.group)
        self.o_proj = QuantLinear(H * cfg.v_head, d, cfg.group)
        self.scale = (cfg.qk_nope + cfg.qk_rope) ** -0.5
        self._wb = None

    def _kvb_bf(self):
        if self._wb is None:
            self._wb = _dequant_torch(self.kv_b.w_q, self.kv_b.scales, self.kv_b.zeros,
                                      self.cfg.kv_lora, self.cfg.group)
        return self._wb

    def step(self, x, st):
        cfg = self.cfg
        H = cfg.mla_heads
        nope, rope, vh, lora = cfg.qk_nope, cfg.qk_rope, cfg.v_head, cfg.kv_lora
        pos = st["c_kv"].shape[0]
        q = _gemv(x, self.q_proj).view(H, nope + rope)
        q_nope = q[:, :nope].float()
        q_rope = q[:, nope:]
        kv = _gemv(x, self.kv_a).to(torch.bfloat16)
        c_kv = kv[:lora]
        k_rope = kv[lora:]
        cos, sin = _rope_cossin(pos, rope, cfg.rope_theta, x.device)
        q_rope = _apply_rope(q_rope, cos, sin).float()
        k_rope = _apply_rope(k_rope, cos, sin)
        st["c_kv"] = torch.cat([st["c_kv"], c_kv[None]], 0)
        st["k_rope"] = torch.cat([st["k_rope"], k_rope[None]], 0)

        wb = self._kvb_bf().view(lora, H, nope + vh).float()
        Wk = wb[:, :, :nope]          # [lora, H, nope]
        Wv = wb[:, :, nope:]          # [lora, H, vh]
        ckv = st["c_kv"].float()      # [L, lora]
        # absorb: qc[h,c] = q_nope[h,:] @ Wk[:,h,:]^T
        qc = torch.einsum("hd,chd->hc", q_nope, Wk)
        # keep scores as [H, L] so softmax reduces over the contiguous last dim
        scores = (torch.einsum("hc,lc->hl", qc, ckv)
                  + torch.einsum("hr,lr->hl", q_rope, st["k_rope"].float())) * self.scale
        p = torch.softmax(scores, dim=1)               # [H, L]
        pc = torch.einsum("hl,lc->hc", p, ckv)         # [H, lora]
        o = torch.einsum("hc,chd->hd", pc, Wv)         # [H, vh]
        return _gemv(o.reshape(H * vh).to(torch.bfloat16), self.o_proj).to(torch.bfloat16)


class MoE(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        d, m, E = cfg.hidden, cfg.moe_inter, cfg.n_experts
        self.router = nn.Linear(d, E, bias=False, dtype=cfg.dtype)
        self.gate = QuantExperts(E, d, m, cfg.group)
        self.up = QuantExperts(E, d, m, cfg.group)
        self.down = QuantExperts(E, m, d, cfg.group)
        self.s_gate = QuantExperts(cfg.n_shared, d, m, cfg.group)
        self.s_up = QuantExperts(cfg.n_shared, d, m, cfg.group)
        self.s_down = QuantExperts(cfg.n_shared, m, d, cfg.group)

    def _experts(self, x, ge, ue, de, idx):
        d = self.cfg.hidden
        m = self.cfg.moe_inter
        k = idx.numel()
        xe = x.reshape(1, d).expand(k, d)
        g = _bgemv(xe, ge.w_q[idx], ge.scales[idx], ge.zeros[idx], m)
        u = _bgemv(xe, ue.w_q[idx], ue.scales[idx], ue.zeros[idx], m)
        hh = (F.silu(g) * u).contiguous()
        out = _bgemv(hh, de.w_q[idx], de.scales[idx], de.zeros[idx], d)   # [k, d]
        return out

    def step(self, x):
        cfg = self.cfg
        probs = torch.softmax(self.router(x).float(), dim=-1)
        w, idx = torch.topk(probs, cfg.n_active)
        w = (w / (w.sum() + 1e-9) * cfg.routed_scaling).float()
        routed = self._experts(x, self.gate, self.up, self.down, idx)  # [k, d]
        out = (w[:, None] * routed).sum(0)
        sidx = torch.arange(cfg.n_shared, device=x.device)
        sh = self._experts(x, self.s_gate, self.s_up, self.s_down, sidx)
        out = out + sh.sum(0)
        return out.to(torch.bfloat16)


class Block(nn.Module):
    def __init__(self, cfg, kind):
        super().__init__()
        self.kind = kind
        self.attn_norm = nn.Parameter(torch.ones(cfg.hidden, dtype=cfg.dtype))
        self.moe_norm = nn.Parameter(torch.ones(cfg.hidden, dtype=cfg.dtype))
        self.attn = KDA(cfg) if kind == "K" else MLA(cfg)
        self.moe = MoE(cfg)

    def step(self, x, st):
        h = x + self.attn.step(_rmsnorm(x, self.attn_norm), st)
        return h + self.moe.step(_rmsnorm(h, self.moe_norm))


class Model(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.blocks = nn.ModuleList(Block(cfg, k) for k in cfg.pattern)

    def step(self, hidden, state):
        for i, blk in enumerate(self.blocks):
            hidden = blk.step(hidden, state[i])
        return hidden, state
