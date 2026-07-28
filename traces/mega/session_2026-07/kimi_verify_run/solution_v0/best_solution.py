"""Initial solution: correct stock PyTorch (baseline clone), NOT a megakernel."""
from __future__ import annotations

import os
os.environ.setdefault("CUDA_HOME", "/tmp/cudatk")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

from dataclasses import dataclass, field
from math import exp, log

import torch
import torch.nn as nn
import torch.nn.functional as F

torch.set_float32_matmul_precision("high")
torch.backends.cuda.matmul.allow_tf32 = True
try:
    torch.backends.cudnn.allow_tf32 = True
except Exception:
    pass

torch.set_num_threads(2)

EPS = 1.0e-6
GROUP_SIZE = 128


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


def build_config(shape: dict) -> Config:
    return Config(n_experts=int(shape.get("n_experts", 64)))


# --------------------------------------------------------------------------- #
# W4A16 helpers
# --------------------------------------------------------------------------- #
def _pack_int4(w_q: torch.Tensor) -> torch.Tensor:
    lo = w_q[0::2] & 0xF
    hi = w_q[1::2] & 0xF
    return (lo | (hi << 4)).contiguous()


def _unpack_int4(w_packed: torch.Tensor, K: int) -> torch.Tensor:
    out = torch.empty((K, w_packed.shape[1]), dtype=torch.uint8, device=w_packed.device)
    out[0::2] = w_packed & 0xF
    out[1::2] = (w_packed >> 4) & 0xF
    return out


def quantize(w_io: torch.Tensor, group: int = GROUP_SIZE):
    K, N = w_io.shape
    ng = K // group
    wg = w_io.view(ng, group, N).float()
    wmin = wg.min(dim=1, keepdim=True).values
    wmax = wg.max(dim=1, keepdim=True).values
    scales = (wmax - wmin).clamp_min(1e-8) / 15.0
    zeros = (-wmin / scales).round().clamp(0, 15)
    w_q = ((wg / scales) + zeros).round().clamp(0, 15).to(torch.uint8).view(K, N)
    return _pack_int4(w_q), scales.squeeze(1).to(torch.bfloat16), zeros.squeeze(1).to(torch.bfloat16)


def dequant(w_q: torch.Tensor, scales: torch.Tensor, zeros: torch.Tensor, K: int, group: int) -> torch.Tensor:
    wu = _unpack_int4(w_q, K).to(torch.bfloat16)
    s = scales.repeat_interleave(group, dim=0)
    z = zeros.repeat_interleave(group, dim=0)
    return (wu - z) * s


class QuantLinear(nn.Module):
    def __init__(self, in_f: int, out_f: int, group: int = GROUP_SIZE):
        super().__init__()
        assert in_f % group == 0 and in_f % 2 == 0
        self.in_f, self.out_f, self.group = in_f, out_f, group
        ng = in_f // group
        self.register_buffer("w_q", torch.zeros(in_f // 2, out_f, dtype=torch.uint8))
        self.register_buffer("scales", torch.zeros(ng, out_f, dtype=torch.bfloat16))
        self.register_buffer("zeros", torch.zeros(ng, out_f, dtype=torch.bfloat16))

    def init_random(self, gen: torch.Generator, std: float = 0.02) -> None:
        w = torch.randn(self.in_f, self.out_f, generator=gen) * std
        wq, s, z = quantize(w, self.group)
        self.w_q.copy_(wq)
        self.scales.copy_(s)
        self.zeros.copy_(z)

    def weight_bf(self) -> torch.Tensor:
        if getattr(self, "_cache", None) is None:
            self._cache = dequant(self.w_q, self.scales, self.zeros, self.in_f, self.group)
        return self._cache


class QuantExperts(nn.Module):
    def __init__(self, n: int, in_f: int, out_f: int, group: int = GROUP_SIZE):
        super().__init__()
        self.n, self.in_f, self.out_f, self.group = n, in_f, out_f, group
        ng = in_f // group
        self.register_buffer("w_q", torch.zeros(n, in_f // 2, out_f, dtype=torch.uint8))
        self.register_buffer("scales", torch.zeros(n, ng, out_f, dtype=torch.bfloat16))
        self.register_buffer("zeros", torch.zeros(n, ng, out_f, dtype=torch.bfloat16))

    def init_random(self, gen: torch.Generator, std: float = 0.02) -> None:
        for e in range(self.n):
            w = torch.randn(self.in_f, self.out_f, generator=gen) * std
            wq, s, z = quantize(w, self.group)
            self.w_q[e].copy_(wq)
            self.scales[e].copy_(s)
            self.zeros[e].copy_(z)

    def weight_bf(self, e: int) -> torch.Tensor:
        if getattr(self, "_cache", None) is None:
            self._build_cache()
        return self._cache[e]

    def _build_cache(self) -> None:
        self._cache = torch.stack([
            dequant(self.w_q[i], self.scales[i], self.zeros[i], self.in_f, self.group)
            for i in range(self.n)
        ])


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _rmsnorm(x: torch.Tensor, w: torch.Tensor) -> torch.Tensor:
    xf = x.float()
    scale = torch.rsqrt(xf.pow(2).mean(-1, keepdim=True) + EPS) * w.float()
    return (xf * scale).to(x.dtype)


def _apply_rope_plain(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
    out = torch.empty_like(x)
    even, odd = x[..., 0::2], x[..., 1::2]
    out[..., 0::2] = even * cos - odd * sin
    out[..., 1::2] = odd * cos + even * sin
    return out


_apply_rope = torch.jit.script(_apply_rope_plain)


@torch.jit.script
def _jit_short_conv(val: torch.Tensor, p0: torch.Tensor, p1: torch.Tensor,
                    p2: torch.Tensor, w0: torch.Tensor, w1: torch.Tensor,
                    w2: torch.Tensor, w3: torch.Tensor) -> torch.Tensor:
    return F.silu(p0 * w0 + p1 * w1 + p2 * w2 + val * w3)


@torch.jit.script
def _jit_moe(x: torch.Tensor, gate_w: torch.Tensor, up_w: torch.Tensor,
             down_w: torch.Tensor, w: torch.Tensor,
             s_gu_w: torch.Tensor, s_down_w: torch.Tensor,
             m: int) -> torch.Tensor:
    k = gate_w.shape[0]
    xv = x[None, None, :].expand(k, 1, -1)
    g = torch.matmul(xv, gate_w).squeeze(1)
    u = torch.matmul(xv, up_w).squeeze(1)
    h = F.silu(g) * u
    routed = torch.matmul(h.unsqueeze(1), down_w).squeeze(1)
    out = torch.matmul(w.unsqueeze(0), routed).squeeze(0)
    sgu = F.linear(x, s_gu_w)
    sg = sgu[:m]
    su = sgu[m:]
    sh = F.silu(sg) * su
    return out + F.linear(sh, s_down_w)


@torch.jit.script
def _jit_block(h: torch.Tensor, attn_out: torch.Tensor, moe_out: torch.Tensor) -> torch.Tensor:
    return h + attn_out + moe_out


@torch.jit.script
def _jit_beta(x: torch.Tensor, w: torch.Tensor) -> torch.Tensor:
    return torch.sigmoid(F.linear(x, w))


@torch.jit.script
def _jit_router(x: torch.Tensor, w: torch.Tensor) -> torch.Tensor:
    return torch.softmax(F.linear(x, w), dim=-1)


def _rmsnorm_plain(x: torch.Tensor, w: torch.Tensor, eps: float = 1.0e-6) -> torch.Tensor:
    xf = x.float()
    scale = torch.rsqrt(xf.pow(2).mean(-1, keepdim=True) + eps) * w.float()
    return (xf * scale).to(x.dtype)


_rmsnorm = torch.jit.script(_rmsnorm_plain)


def _rope_cossin(pos: int, dim: int, theta: float, device):
    inv = 1.0 / (theta ** (torch.arange(0, dim, 2, device=device, dtype=torch.float32) / dim))
    ang = pos * inv
    return torch.cos(ang), torch.sin(ang)


def _apply_rope(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
    xf = x.float()
    even, odd = xf[..., 0::2], xf[..., 1::2]
    xf[..., 0::2] = even * cos - odd * sin
    xf[..., 1::2] = odd * cos + even * sin
    return xf.to(x.dtype)


def _wbf(ql) -> torch.Tensor:
    return ql.weight_bf()


class KDA(nn.Module):
    def __init__(self, cfg: Config):
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
        self._qkv_cache = None
        self._qkv_cache_t = None
        self._o_t = None
        self._conv_w_t = None

    def _ensure_proj_cache(self):
        if self._qkv_cache_t is None:
            C = self.cfg.kda_heads * self.cfg.kda_head_dim
            q = self.q_proj.weight_bf()
            k = self.k_proj.weight_bf()
            v = self.v_proj.weight_bf()
            g = self.g_proj.weight_bf()
            self._qkv_cache = torch.cat([q, k, v, g], dim=1)
            self._qkv_cache_t = self._qkv_cache.t().contiguous()
            self._qkv_cache = None
            self.q_proj._cache = None
            self.k_proj._cache = None
            self.v_proj._cache = None
            self.g_proj._cache = None

    def _short_conv(self, val, prev, idx):
        if self._conv_w_t is None:
            self._conv_w_t = self.conv_w.to(torch.bfloat16).transpose(1, 2)
        w = self._conv_w_t[idx]
        p0, p1, p2 = prev[0], prev[1], prev[2]
        out = _jit_short_conv(val, p0, p1, p2, w[0], w[1], w[2], w[3])
        prev[0] = p1
        prev[1] = p2
        prev[2] = val
        return out, prev

    def step(self, x, st):
        H, Dk = self.cfg.kda_heads, self.cfg.kda_head_dim
        C = H * Dk
        self._ensure_proj_cache()
        cq, ck, cv = st["cq"], st["ck"], st["cv"]
        qkvg = (self._qkv_cache_t @ x.unsqueeze(1)).squeeze(1)
        q = qkvg[0 * C : 1 * C]
        k = qkvg[1 * C : 2 * C]
        v = qkvg[2 * C : 3 * C]
        g = qkvg[3 * C : 4 * C]
        q, _ = self._short_conv(q, cq, 0)
        k, _ = self._short_conv(k, ck, 1)
        v, _ = self._short_conv(v, cv, 2)
        q = q.view(H, Dk)
        q.mul_(self.scale)
        k = k.view(H, Dk)
        v = v.view(H, Dk)
        g = -F.softplus(g.view(H, Dk))
        beta = _jit_beta(x, self.beta_proj.weight)
        S = st["S"].to(torch.bfloat16)
        S = S * g.exp()[:, :, None]
        pred = (S * k[:, :, None]).sum(1)
        S = S + beta[:, None, None] * k[:, :, None] * (v - pred)[:, None, :]
        o = (S * q[:, :, None]).sum(1)
        st["S"] = S
        if self._o_t is None:
            self._o_t = self.o_proj.weight_bf().t().contiguous()
        return F.linear(o.view(H * Dk), self._o_t)


class MLA(nn.Module):
    _EXTRA = 1024

    def __init__(self, cfg: Config):
        super().__init__()
        self.cfg = cfg
        H, d = cfg.mla_heads, cfg.hidden
        self.q_proj = QuantLinear(d, H * (cfg.qk_nope + cfg.qk_rope), cfg.group)
        self.kv_a = QuantLinear(d, cfg.kv_lora + cfg.qk_rope, cfg.group)
        self.kv_b = QuantLinear(cfg.kv_lora, H * (cfg.qk_nope + cfg.v_head), cfg.group)
        self.o_proj = QuantLinear(H * cfg.v_head, d, cfg.group)
        self.scale = (cfg.qk_nope + cfg.qk_rope) ** -0.5
        self._q_w = None
        self._kv_a_w = None
        self._o_t = None
        self._kv_b_view = None
        self._wk = None
        self._wv = None
        self._rope_cos = None
        self._rope_sin = None
        self._cache_c = None
        self._cache_r = None

    def _build_rope(self, device):
        cfg = self.cfg
        max_len, dim = 32768, cfg.qk_rope
        inv = 1.0 / (cfg.rope_theta ** (torch.arange(0, dim, 2, device=device, dtype=torch.float32) / dim))
        ang = torch.arange(max_len, device=device, dtype=torch.float32)[:, None] * inv[None, :]
        self._rope_cos = torch.cos(ang).to(cfg.dtype)
        self._rope_sin = torch.sin(ang).to(cfg.dtype)

    def _ensure_cache(self, src_c, src_r, device):
        L = src_c.shape[0]
        rebuild = (self._cache_c is None or self._cache_c.shape[0] < L + self._EXTRA
                   or src_c.data_ptr() != self._cache_c.data_ptr())
        if rebuild:
            self._cache_c = torch.empty((L + self._EXTRA, src_c.shape[1]), dtype=src_c.dtype, device=device)
            self._cache_r = torch.empty((L + self._EXTRA, src_r.shape[1]), dtype=src_r.dtype, device=device)
            if L:
                self._cache_c[:L].copy_(src_c)
                self._cache_r[:L].copy_(src_r)
        return L

    def step(self, x, st):
        cfg = self.cfg
        H = cfg.mla_heads
        src_c, src_r = st["c_kv"], st["k_rope"]
        pos = src_c.shape[0]
        L = self._ensure_cache(src_c, src_r, x.device)
        if self._rope_cos is None or self._rope_cos.device != x.device:
            self._build_rope(x.device)
        if self._q_w is None:
            self._q_w = self.q_proj.weight_bf().t().contiguous()
        if self._kv_a_w is None:
            self._kv_a_w = self.kv_a.weight_bf().t().contiguous()
        q = (self._q_w @ x.unsqueeze(1)).squeeze(1).view(H, cfg.qk_nope + cfg.qk_rope)
        q_nope = q[:, : cfg.qk_nope]
        q_rope = q[:, cfg.qk_nope :]
        kv = (self._kv_a_w @ x.unsqueeze(1)).squeeze(1)
        c_kv = kv[: cfg.kv_lora]
        k_rope = kv[cfg.kv_lora :]
        cos, sin = self._rope_cos[pos], self._rope_sin[pos]
        q_rope = _apply_rope(q_rope, cos, sin)
        k_rope = _apply_rope(k_rope, cos, sin)
        self._cache_c[L] = c_kv
        self._cache_r[L] = k_rope
        self._cache_source = (self._cache_c.data_ptr(), L + 1, self._cache_c.stride(0),
                              self._cache_r.data_ptr(), L + 1, self._cache_r.stride(0))
        st["c_kv"] = self._cache_c[:L + 1]
        st["k_rope"] = self._cache_r[:L + 1]
        # Absorb kv_b into q instead of expanding every cached latent to key/value.
        if self._kv_b_view is None:
            self._kv_b_view = _wbf(self.kv_b).view(cfg.kv_lora, H, cfg.qk_nope + cfg.v_head)
            self._wk = self._kv_b_view[..., : cfg.qk_nope].permute(1, 2, 0)
            self._wv = self._kv_b_view[..., cfg.qk_nope :].permute(1, 0, 2)
        q_abs = torch.matmul(q_nope.unsqueeze(1), self._wk).squeeze(1)
        scores = torch.matmul(q_abs, st["c_kv"].t()) + torch.matmul(q_rope, st["k_rope"].t())
        scores.mul_(self.scale)
        p = torch.softmax(scores, dim=-1)
        latent = torch.matmul(p, st["c_kv"])
        o = torch.matmul(latent.unsqueeze(1), self._wv).squeeze(1)
        if self._o_t is None:
            self._o_t = self.o_proj.weight_bf().t().contiguous()
        return F.linear(o.view(H * cfg.v_head), self._o_t)


def _batch_wbf(qe: QuantExperts, idx: torch.Tensor) -> torch.Tensor:
    if getattr(qe, "_cache", None) is not None:
        return qe._cache[idx]
    K = qe.in_f
    wu = torch.empty((idx.numel(), K, qe.out_f), dtype=torch.uint8, device=qe.w_q.device)
    wp = qe.w_q[idx]
    wu[:, 0::2] = wp & 0xF
    wu[:, 1::2] = (wp >> 4) & 0xF
    s = qe.scales[idx].repeat_interleave(qe.group, dim=1)
    z = qe.zeros[idx].repeat_interleave(qe.group, dim=1)
    return (wu.to(torch.bfloat16) - z) * s


class MoE(nn.Module):
    def __init__(self, cfg: Config):
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
        self._s_gu_t = None
        self._s_down_t = None

    def step(self, x):
        cfg = self.cfg
        probs = _jit_router(x, self.router.weight)
        w, idx = torch.topk(probs, cfg.n_active, sorted=False)
        w = w / (w.sum() + 1e-9) * cfg.routed_scaling
        # Ensure expert caches exist (built lazily on first step).
        for exp in (self.gate, self.up, self.down, self.s_gate, self.s_up, self.s_down):
            if getattr(exp, "_cache", None) is None:
                exp._build_cache()
        # Batched gate/up/down over the selected experts using cached bf16 weights.
        if self._s_gu_t is None:
            gu = torch.cat([self.s_gate._cache[0], self.s_up._cache[0]], dim=1)
            self._s_gu_t = gu.t().contiguous()
            self._s_down_t = self.s_down._cache[0].t().contiguous()
        return _jit_moe(x, self.gate._cache[idx], self.up._cache[idx],
                        self.down._cache[idx], w,
                        self._s_gu_t, self._s_down_t, cfg.moe_inter)


class Block(nn.Module):
    def __init__(self, cfg: Config, kind: str):
        super().__init__()
        self.kind = kind
        self.attn_norm = nn.Parameter(torch.ones(cfg.hidden, dtype=cfg.dtype))
        self.moe_norm = nn.Parameter(torch.ones(cfg.hidden, dtype=cfg.dtype))
        self._attn_norm_fp = None
        self._moe_norm_fp = None
        self.attn = KDA(cfg) if kind == "K" else MLA(cfg)
        self.moe = MoE(cfg)

    def step(self, x, st):
        if self._attn_norm_fp is None:
            self._attn_norm_fp = self.attn_norm.float()
            self._moe_norm_fp = self.moe_norm.float()
        attn_out = self.attn.step(_rmsnorm(x, self._attn_norm_fp), st)
        h = x + attn_out
        moe_out = self.moe.step(_rmsnorm(h, self._moe_norm_fp))
        return _jit_block(x, attn_out, moe_out)


class Model(nn.Module):
    def __init__(self, cfg: Config):
        super().__init__()
        self.cfg = cfg
        self.blocks = nn.ModuleList(Block(cfg, k) for k in cfg.pattern)

    def step(self, hidden, state):
        with torch.inference_mode():
            for i, blk in enumerate(self.blocks):
                hidden = blk.step(hidden, state[i])
            return hidden, state


def init_state(cfg: Config, context_len: int, seed: int) -> list:
    dev = torch.device("cuda:0")
    g = torch.Generator(device=dev).manual_seed(seed)
    H, Dk = cfg.kda_heads, cfg.kda_head_dim
    C = H * Dk
    state = []
    for kind in cfg.pattern:
        if kind == "K":
            state.append({
                "S": torch.randn(H, Dk, Dk, device=dev, generator=g) * 0.05,
                "cq": torch.randn(cfg.short_conv - 1, C, device=dev, generator=g, dtype=cfg.dtype) * 0.1,
                "ck": torch.randn(cfg.short_conv - 1, C, device=dev, generator=g, dtype=cfg.dtype) * 0.1,
                "cv": torch.randn(cfg.short_conv - 1, C, device=dev, generator=g, dtype=cfg.dtype) * 0.1,
            })
        else:
            state.append({
                "c_kv": torch.randn(context_len, cfg.kv_lora, device=dev, generator=g, dtype=cfg.dtype) * 0.1,
                "k_rope": torch.randn(context_len, cfg.qk_rope, device=dev, generator=g, dtype=cfg.dtype) * 0.1,
            })
    return state


def init_token(cfg: Config, seed: int) -> torch.Tensor:
    dev = torch.device("cuda:0")
    g = torch.Generator(device=dev).manual_seed(seed + 1)
    return torch.randn(cfg.hidden, device=dev, generator=g, dtype=cfg.dtype) * 0.25
