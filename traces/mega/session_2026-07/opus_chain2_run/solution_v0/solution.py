"""Kimi-Linear W4A16 hybrid decode -- single fused cooperative CUDA megakernel.

This file exposes the same Model / step(hidden, state) -> (hidden, state)
interface and identical buffer/parameter names as reference.py, so it loads the
reference weights via load_state_dict.

The timed decode path is ONE cooperative CUDA kernel launch (grid.sync barriers
between stages); the int4 unpack + per-group dequant is fused directly into
every GEMV so the int4 weights are streamed exactly once and never materialized
as bf16.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

import torch
import torch.nn as nn
import torch.nn.functional as F

import megakernel_src as _mk

EPS = 1.0e-6
GROUP_SIZE = 128

os.environ.setdefault("CUDA_HOME", "/tmp/cudatk")

_MOD = None


def _get_module():
    global _MOD
    if _MOD is None:
        from torch.utils.cpp_extension import load_inline
        _MOD = load_inline(
            name="kimi_megakernel",
            cpp_sources=_mk.CPP,
            cuda_sources=_mk.CUDA,
            functions=["mega_launch"],
            extra_cuda_cflags=["-O3", "-arch=sm_120", "--use_fast_math",
                               "-DLB=" + os.environ.get("KIMI_LB", "2"),
                               "-maxrregcount=" + os.environ.get("KIMI_RREG", "128")],
            verbose=False,
        )
    return _MOD


# --------------------------------------------------------------------------- #
# Config (structurally identical to reference.Config)
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Config:
    hidden: int = 2304
    kda_heads: int = 32
    kda_head_dim: int = 128
    short_conv: int = 4
    mla_heads: int = 32
    kv_lora: int = 512
    qk_nope: int = 128
    qk_rope: int = 64
    v_head: int = 128
    rope_theta: float = 10000.0
    n_experts: int = 64
    n_active: int = 8
    n_shared: int = 1
    moe_inter: int = 1024
    routed_scaling: float = 2.446
    group: int = 128
    pattern: tuple = ("K", "K", "K", "M")
    dtype: torch.dtype = field(default=torch.bfloat16)


# --------------------------------------------------------------------------- #
# W4A16 storage modules (buffer names match reference)
# --------------------------------------------------------------------------- #
def _unpack_int4(w_packed: torch.Tensor, K: int) -> torch.Tensor:
    out = torch.empty((K, w_packed.shape[1]), dtype=torch.uint8, device=w_packed.device)
    out[0::2] = w_packed & 0xF
    out[1::2] = (w_packed >> 4) & 0xF
    return out


def _dequant(w_q, scales, zeros, K, group):
    wu = _unpack_int4(w_q, K).to(torch.bfloat16)
    s = scales.repeat_interleave(group, dim=0)
    z = zeros.repeat_interleave(group, dim=0)
    return (wu - z) * s


class QuantLinear(nn.Module):
    def __init__(self, in_f, out_f, group=GROUP_SIZE):
        super().__init__()
        self.in_f, self.out_f, self.group = in_f, out_f, group
        ng = in_f // group
        self.register_buffer("w_q", torch.zeros(in_f // 2, out_f, dtype=torch.uint8))
        self.register_buffer("scales", torch.zeros(ng, out_f, dtype=torch.bfloat16))
        self.register_buffer("zeros", torch.zeros(ng, out_f, dtype=torch.bfloat16))

    def weight_bf(self):
        return _dequant(self.w_q, self.scales, self.zeros, self.in_f, self.group)


class QuantExperts(nn.Module):
    def __init__(self, n, in_f, out_f, group=GROUP_SIZE):
        super().__init__()
        self.n, self.in_f, self.out_f, self.group = n, in_f, out_f, group
        ng = in_f // group
        self.register_buffer("w_q", torch.zeros(n, in_f // 2, out_f, dtype=torch.uint8))
        self.register_buffer("scales", torch.zeros(n, ng, out_f, dtype=torch.bfloat16))
        self.register_buffer("zeros", torch.zeros(n, ng, out_f, dtype=torch.bfloat16))

    def weight_bf(self, e):
        return _dequant(self.w_q[e], self.scales[e], self.zeros[e], self.in_f, self.group)


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
# layers -- torch reference-mirror (validation path). The timed path replaces
# Model.step with the fused megakernel.
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

    def _short_conv(self, val, prev, idx):
        win = torch.cat([prev, val[None]], dim=0)
        w = self.conv_w[idx].float().transpose(0, 1)
        out = (win.float() * w).sum(0)
        return F.silu(out).to(val.dtype), win[1:]

    def step(self, x, st):
        H, Dk = self.cfg.kda_heads, self.cfg.kda_head_dim
        q = x @ self.q_proj.weight_bf()
        k = x @ self.k_proj.weight_bf()
        v = x @ self.v_proj.weight_bf()
        q, st["cq"] = self._short_conv(q, st["cq"], 0)
        k, st["ck"] = self._short_conv(k, st["ck"], 1)
        v, st["cv"] = self._short_conv(v, st["cv"], 2)
        q = q.view(H, Dk).float() * self.scale
        k = k.view(H, Dk).float()
        v = v.view(H, Dk).float()
        g = (-F.softplus((x @ self.g_proj.weight_bf()).float())).view(H, Dk)
        beta = torch.sigmoid(self.beta_proj(x).float())
        S = st["S"] * g.exp()[:, :, None]
        pred = (S * k[:, :, None]).sum(1)
        S = S + beta[:, None, None] * k[:, :, None] * (v - pred)[:, None, :]
        o = (S * q[:, :, None]).sum(1)
        st["S"] = S
        return (o.reshape(H * Dk).to(torch.bfloat16)) @ self.o_proj.weight_bf()


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

    def step(self, x, st):
        cfg = self.cfg
        H = cfg.mla_heads
        qn, qr, vh, L0 = cfg.qk_nope, cfg.qk_rope, cfg.v_head, cfg.kv_lora
        pos = st["c_kv"].shape[0]
        q = (x @ self.q_proj.weight_bf()).view(H, qn + qr)
        q_nope = q[:, :qn].float()
        q_rope = q[:, qn:]
        kv = x @ self.kv_a.weight_bf()
        c_kv = kv[:L0]
        k_rope = kv[L0:]
        cos, sin = _rope_cossin(pos, qr, cfg.rope_theta, x.device)
        q_rope = _apply_rope(q_rope, cos, sin).float()
        k_rope = _apply_rope(k_rope, cos, sin)
        st["c_kv"] = torch.cat([st["c_kv"], c_kv[None]], 0)
        st["k_rope"] = torch.cat([st["k_rope"], k_rope[None]], 0)
        ckv = st["c_kv"].float()
        krope = st["k_rope"].float()
        Wb = self.kv_b.weight_bf().float().view(L0, H, qn + vh)
        Wk = Wb[:, :, :qn].permute(1, 0, 2).contiguous()   # [H,512,128]
        Wv = Wb[:, :, qn:].permute(1, 0, 2).contiguous()   # [H,512,128]
        qa = torch.einsum("hd,hkd->hk", q_nope, Wk)          # [H,512]
        s_nope = torch.einsum("hk,lk->lh", qa, ckv)
        s_rope = torch.einsum("hd,ld->lh", q_rope, krope)
        scores = (s_nope + s_rope) * self.scale
        p = torch.softmax(scores, dim=0)
        cvec = torch.einsum("lh,lk->hk", p, ckv)             # [H,512]
        o = torch.einsum("hk,hkd->hd", cvec, Wv)             # [H,128]
        return (o.reshape(H * vh).to(torch.bfloat16)) @ self.o_proj.weight_bf()


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

    def _ffn(self, x, eg, eu, ed, e):
        h = F.silu(x @ eg.weight_bf(e)) * (x @ eu.weight_bf(e))
        return h @ ed.weight_bf(e)

    def step(self, x):
        cfg = self.cfg
        probs = torch.softmax(self.router(x).float(), dim=-1)
        w, idx = torch.topk(probs, cfg.n_active)
        w = (w / (w.sum() + 1e-9) * cfg.routed_scaling).to(x.dtype)
        out = x.new_zeros(cfg.hidden)
        for j in range(cfg.n_active):
            out = out + w[j] * self._ffn(x, self.gate, self.up, self.down, int(idx[j]))
        for s in range(cfg.n_shared):
            out = out + self._ffn(x, self.s_gate, self.s_up, self.s_down, s)
        return out


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


def _qp(ql):
    return [ql.w_q.data_ptr(), ql.scales.data_ptr(), ql.zeros.data_ptr()]


class Model(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.blocks = nn.ModuleList(Block(cfg, k) for k in cfg.pattern)
        self._mod = None
        self._Wt = None
        self._Woff = None
        self._scr = None
        self._St = None
        self._Soff = None
        self._state_id = None
        self._cap_ckv = None
        self._cap_krope = None
        self._cap_len = 0
        self._cap_base_id = None
        self._meta_cpu = None
        self._meta_gpu = None
        self._hid = None
        self._out = None
        self._mla_idx = self.cfg.pattern.index("M")

    # ------- build the persistent weight pointer table (once) -------
    def _build_weights(self):
        W = []
        Woff = []
        for blk in self.blocks:
            attn_base = len(W)
            W += [blk.attn_norm.data_ptr(), blk.moe_norm.data_ptr()]
            a = blk.attn
            if blk.kind == "K":
                W += _qp(a.q_proj) + _qp(a.k_proj) + _qp(a.v_proj) + _qp(a.g_proj) + _qp(a.o_proj)
                W += [a.beta_proj.weight.data_ptr(), a.conv_w.data_ptr()]
            else:
                W += _qp(a.q_proj) + _qp(a.kv_a) + _qp(a.kv_b) + _qp(a.o_proj)
            moe_base = len(W)
            mo = blk.moe
            W += [blk.moe_norm.data_ptr(), mo.router.weight.data_ptr()]
            W += _qp(mo.gate) + _qp(mo.up) + _qp(mo.down)
            W += _qp(mo.s_gate) + _qp(mo.s_up) + _qp(mo.s_down)
            Woff += [attn_base, moe_base]
        self._Wt = torch.tensor(W, dtype=torch.int64, device="cuda")
        self._Woff = torch.tensor(Woff, dtype=torch.int32, device="cuda")
        # L2-persist the largest reused (per-token-invariant) projection weight
        # (MLA q_proj, ~7MB) so the per-token MoE weight stream can't evict it.
        # Hardware access-policy window (SM120). A precise single-buffer window
        # beats a wide span (a span over scattered buffers pins unrelated MoE
        # weights and thrashes -- verified in separate-process benchmarks).
        mla = self.blocks[self._mla_idx].attn
        self._pin_ptr = mla.q_proj.w_q.data_ptr()
        self._pin_size = mla.q_proj.w_q.numel()  # uint8 bytes
        # scratch: big enough for MLA at largest ctx. sized dynamically in step.
        self._mod = _get_module()

    def _ensure_scratch(self, Lt):
        cfg = self.cfg
        nexp = cfg.n_active + cfg.n_shared
        need = cfg.hidden + max(
            cfg.hidden + 4 * cfg.kda_heads * cfg.kda_head_dim + cfg.kda_heads + cfg.hidden,
            cfg.mla_heads * (cfg.qk_nope + cfg.qk_rope) + 576 + cfg.mla_heads * cfg.kv_lora
            + Lt * cfg.mla_heads + cfg.mla_heads * cfg.kv_lora + cfg.mla_heads * cfg.v_head + cfg.hidden
            + cfg.kv_lora * cfg.mla_heads,
            cfg.n_experts + 2 * nexp * cfg.moe_inter + nexp * cfg.hidden + cfg.hidden + 64,
        ) + 4096 + (1 << 21)  # + PART_FLOATS for deterministic split-K + cvec partials
        if self._scr is None or self._scr.numel() < need:
            self._scr = torch.empty(need, dtype=torch.float32, device="cuda")

    def step(self, hidden, state):
        if self._Wt is None:
            self._build_weights()
        cfg = self.cfg
        if self._hid is None:
            self._hid = torch.empty(cfg.hidden, dtype=torch.float32, device="cuda")
        hid = self._hid
        hid.copy_(hidden)
        nblk = getattr(self, "_dbg_nblk", len(self.blocks))
        do_last_moe = getattr(self, "_dbg_last_moe", 1)
        # Detect whether the state object identity changed (new state list) --
        # only then rebuild the (mostly fixed) pointer table on the host.
        rebuild = (self._state_id != id(state))
        mla_i = self._mla_idx
        st_mla = state[mla_i]
        cur_ckv = st_mla["c_kv"]
        L = cur_ckv.shape[0]
        # ---- grow MLA caches in place (capacity-backed) to avoid copy+realloc ----
        # Continuation only if the incoming cache IS our capacity view (same
        # storage) with matching length; otherwise treat as a fresh cache and
        # reseed. (data_ptr identity is robust to Python id() reuse.)
        cap_ckv = self._cap_ckv
        is_continuation = (cap_ckv is not None
                           and cur_ckv.data_ptr() == cap_ckv.data_ptr()
                           and L == self._cap_len
                           and L + 1 <= cap_ckv.shape[0])
        if not is_continuation:
            cap = L + 512
            new_ckv = torch.empty(cap, cfg.kv_lora, dtype=torch.bfloat16, device="cuda")
            new_krope = torch.empty(cap, cfg.qk_rope, dtype=torch.bfloat16, device="cuda")
            new_ckv[:L] = cur_ckv
            new_krope[:L] = st_mla["k_rope"]
            self._cap_ckv = cap_ckv = new_ckv
            self._cap_krope = new_krope
            self._cap_len = L
            rebuild = True
        # old cache = capacity[:L], new cache written at row L; kernel copies
        # only the appended row (old==new base here, so pass same ptr for both).
        old_ckv_ptr = self._cap_ckv.data_ptr()
        old_krope_ptr = self._cap_krope.data_ptr()
        new_ckv_ptr = old_ckv_ptr
        new_krope_ptr = old_krope_ptr
        if rebuild:
            Sptrs = []
            Soff = []
            for i, blk in enumerate(self.blocks):
                Soff.append(len(Sptrs))
                stt = state[i]
                if blk.kind == "K":
                    Sptrs += [stt["S"].data_ptr(), stt["cq"].data_ptr(), stt["ck"].data_ptr(), stt["cv"].data_ptr()]
                else:
                    Sptrs += [old_ckv_ptr, old_krope_ptr, new_ckv_ptr, new_krope_ptr]
            self._St = torch.tensor(Sptrs, dtype=torch.int64, device="cuda")
            self._Soff = Soff
            self._state_id = id(state)
        # Scalars (Soff, L, nblk, do_last_moe) are passed by value as kernel
        # launch args -- captured at launch time, so no host-buffer race between
        # back-to-back async steps.
        s0, s1, s2, s3 = self._Soff
        self._ensure_scratch(L + 1)
        self._mod.mega_launch(
            self._Wt.data_ptr(), self._Woff.data_ptr(), self._St.data_ptr(),
            hid.data_ptr(), self._scr.data_ptr(),
            int(s0), int(s1), int(s2), int(s3),
            int(L), int(nblk), int(do_last_moe),
            int(self._pin_ptr), int(self._pin_size),
        )
        # publish grown cache as views [0:L+1]
        self._cap_len = L + 1
        state[mla_i]["c_kv"] = self._cap_ckv[:L + 1]
        state[mla_i]["k_rope"] = self._cap_krope[:L + 1]
        # single fused convert (bf16 out) instead of a separate _out buffer copy
        return hid.to(torch.bfloat16), state
