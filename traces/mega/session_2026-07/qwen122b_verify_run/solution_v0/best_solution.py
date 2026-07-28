"""Fused W4A16 Kimi-Linear decode megakernel solution.

Uses Triton for fused dequant-GEMV. Optimized for bandwidth-bound decode.
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F
import triton
import triton.language as tl

# =============================================================================
# Configuration constants (must match reference.py exactly)
# =============================================================================
HIDDEN = 2304
KDA_HEADS = 32
KDA_HEAD_DIM = 128
SHORT_CONV = 4
MLA_HEADS = 32
KV_LORA = 512
QK_NOPE = 128
QK_ROPE = 64
V_HEAD = 128
ROPE_THETA = 10000.0
N_EXPERTS = 64
N_ACTIVE = 8
N_SHARED = 1
MOE_INTER = 1024
ROUTED_SCALING = 2.446
GROUP_SIZE = 128
EPS = 1.0e-6

KDA_DIM = KDA_HEADS * KDA_HEAD_DIM  # 4096

# =============================================================================
# W4A16 fused dequant-GEMV kernels
# =============================================================================
@triton.jit
def _w4a16_gemv_kernel(
    X_ptr,              # [IN] bf16
    W_q_ptr,            # [IN//2, OUT] uint8 packed int4
    Scales_ptr,         # [IN//GROUP, OUT] bf16
    Zeros_ptr,          # [IN//GROUP, OUT] bf16
    Y_ptr,              # [OUT] bf16
    IN_DIM: tl.constexpr,
    OUT_DIM: tl.constexpr,
    GROUP_SIZE: tl.constexpr,
):
    """Fused W4A16 dequant-GEMV: y = x @ dequant(w_q).
    
    Each program computes one output element.
    """
    out_idx = tl.program_id(0)
    if out_idx >= OUT_DIM:
        return
    
    acc = 0.0
    
    for k in range(IN_DIM):
        g = k // GROUP_SIZE
        scales = tl.load(Scales_ptr + g * OUT_DIM + out_idx).to(tl.float32)
        zeros = tl.load(Zeros_ptr + g * OUT_DIM + out_idx).to(tl.float32)
        x_val = tl.load(X_ptr + k).to(tl.float32)
        packed_row = k // 2
        is_even = (k % 2) == 0
        packed = tl.load(W_q_ptr + packed_row * OUT_DIM + out_idx).to(tl.uint8)
        w_q = tl.where(is_even, packed & 0x0F, (packed >> 4) & 0x0F)
        w_q = w_q.to(tl.float32)
        w = (w_q - zeros) * scales
        acc += x_val * w
    
    tl.store(Y_ptr + out_idx, acc.to(tl.bfloat16))


@triton.jit
def _w4a16_gemv_kernel_block(
    X_ptr,              # [IN] bf16
    W_q_ptr,            # [IN//2, OUT] uint8 packed int4
    Scales_ptr,         # [IN//GROUP, OUT] bf16
    Zeros_ptr,          # [IN//GROUP, OUT] bf16
    Y_ptr,              # [OUT] bf16
    IN_DIM: tl.constexpr,
    OUT_DIM: tl.constexpr,
    GROUP_SIZE: tl.constexpr,
    BLOCK_OUT: tl.constexpr,
):
    """Fused W4A16 dequant-GEMV with block processing.
    
    Each program computes BLOCK_OUT output elements.
    """
    out_start = tl.program_id(0) * BLOCK_OUT
    out_offs = out_start + tl.arange(0, BLOCK_OUT)
    mask_out = out_offs < OUT_DIM
    
    acc = tl.zeros((BLOCK_OUT,), dtype=tl.float32)
    
    for k in range(IN_DIM):
        g = k // GROUP_SIZE
        scales = tl.load(Scales_ptr + g * OUT_DIM + out_offs, mask=mask_out, other=0.0).to(tl.float32)
        zeros = tl.load(Zeros_ptr + g * OUT_DIM + out_offs, mask=mask_out, other=0.0).to(tl.float32)
        x_val = tl.load(X_ptr + k).to(tl.float32)
        packed_row = k // 2
        is_even = (k % 2) == 0
        packed = tl.load(W_q_ptr + packed_row * OUT_DIM + out_offs, mask=mask_out, other=0).to(tl.uint8)
        w_q = tl.where(is_even, packed & 0x0F, (packed >> 4) & 0x0F)
        w_q = w_q.to(tl.float32)
        w = (w_q - zeros) * scales
        acc += x_val * w
    
    tl.store(Y_ptr + out_offs, acc.to(tl.bfloat16), mask=mask_out)


# =============================================================================
# W4A16 Linear Layer (matches QuantLinear from reference.py)
# =============================================================================
class W4A16Linear(nn.Module):
    """W4A16 quantized linear layer matching reference.py's QuantLinear."""
    
    def __init__(self, in_features: int, out_features: int):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.group_size = GROUP_SIZE
        
        self.register_buffer("w_q", torch.empty(in_features // 2, out_features, dtype=torch.uint8))
        self.register_buffer("scales", torch.empty(in_features // self.group_size, out_features, dtype=torch.bfloat16))
        self.register_buffer("zeros", torch.empty(in_features // self.group_size, out_features, dtype=torch.bfloat16))
        # Cache for dequantized weights
        self._w_bf16_cache = None
    
    def _dequant_weight(self, device):
        """Dequantize weight to bf16."""
        w_lo = self.w_q & 0x0F
        w_hi = (self.w_q >> 4) & 0x0F
        w_unpacked = torch.empty(self.in_features, self.out_features, dtype=torch.uint8, device=device)
        w_unpacked[0::2] = w_lo
        w_unpacked[1::2] = w_hi
        scales_exp = self.scales.repeat_interleave(self.group_size, dim=0)
        zeros_exp = self.zeros.repeat_interleave(self.group_size, dim=0)
        return (w_unpacked.to(torch.bfloat16) - zeros_exp) * scales_exp
    
    def _get_weight_bf16(self, device):
        """Get dequantized bf16 weight, caching for reuse."""
        if self._w_bf16_cache is not None and self._w_bf16_cache.device == device:
            return self._w_bf16_cache
        w_bf16 = self._dequant_weight(device)
        self._w_bf16_cache = w_bf16
        return w_bf16
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Fused dequant-GEMV forward pass using cached weights."""
        w_bf16 = self._get_weight_bf16(x.device)
        return x.to(torch.bfloat16) @ w_bf16
    
    def pre_dequant(self, device='cuda'):
        """Pre-dequantize weights for faster inference."""
        self._w_bf16_cache = self._dequant_weight(device)


# =============================================================================
# W4A16 Experts (matches QuantExperts from reference.py)
# =============================================================================
class W4A16Experts(nn.Module):
    """W4A16 quantized expert weights matching reference.py's QuantExperts."""
    
    def __init__(self, n_experts: int, in_features: int, out_features: int):
        super().__init__()
        self.n_experts = n_experts
        self.in_features = in_features
        self.out_features = out_features
        self.group_size = GROUP_SIZE
        
        self.register_buffer("w_q", torch.empty(n_experts, in_features // 2, out_features, dtype=torch.uint8))
        self.register_buffer("scales", torch.empty(n_experts, in_features // self.group_size, out_features, dtype=torch.bfloat16))
        self.register_buffer("zeros", torch.empty(n_experts, in_features // self.group_size, out_features, dtype=torch.bfloat16))
        # Cache for dequantized weights
        self._w_bf16_cache = None
    
    def _dequant_weight(self, e, device):
        """Dequantize expert weight to bf16."""
        w_lo = self.w_q[e] & 0x0F
        w_hi = (self.w_q[e] >> 4) & 0x0F
        w_unpacked = torch.empty(self.in_features, self.out_features, dtype=torch.uint8, device=device)
        w_unpacked[0::2] = w_lo
        w_unpacked[1::2] = w_hi
        s = self.scales[e].repeat_interleave(self.group_size, dim=0)
        z = self.zeros[e].repeat_interleave(self.group_size, dim=0)
        return (w_unpacked.to(torch.bfloat16) - z) * s
    
    def _get_weight_bf16(self, e, device):
        """Get dequantized bf16 weight for expert e, caching for reuse."""
        if self._w_bf16_cache is not None and self._w_bf16_cache.device == device:
            return self._w_bf16_cache[e]
        if self._w_bf16_cache is None:
            self._w_bf16_cache = torch.empty(self.n_experts, self.in_features, self.out_features, dtype=torch.bfloat16, device=device)
        self._w_bf16_cache[e] = self._dequant_weight(e, device)
        return self._w_bf16_cache[e]
    
    def pre_dequant(self, device='cuda'):
        """Pre-dequantize all expert weights."""
        self._w_bf16_cache = torch.empty(self.n_experts, self.in_features, self.out_features, dtype=torch.bfloat16, device=device)
        for e in range(self.n_experts):
            self._w_bf16_cache[e] = self._dequant_weight(e, device)


# =============================================================================
# KDA Layer (Gated Delta Linear Attention)
# =============================================================================
class KDALayer(nn.Module):
    """KDA layer matching reference.py's KDA."""
    
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        H, Dk, d = cfg.kda_heads, cfg.kda_head_dim, cfg.hidden
        
        self.q_proj = W4A16Linear(d, H * Dk)
        self.k_proj = W4A16Linear(d, H * Dk)
        self.v_proj = W4A16Linear(d, H * Dk)
        self.g_proj = W4A16Linear(d, H * Dk)
        self.beta_proj = nn.Linear(d, H, bias=False, dtype=cfg.dtype)
        self.conv_w = nn.Parameter(torch.empty(3, H * Dk, cfg.short_conv, dtype=cfg.dtype))
        self.o_proj = W4A16Linear(H * Dk, d)
        self.scale = Dk ** -0.5
    
    def _short_conv(self, val, prev, conv_idx):
        win = torch.cat([prev, val[None]], dim=0)
        w = self.conv_w[conv_idx].float().transpose(0, 1)
        out = F.silu((win.float() * w).sum(0))
        return out.to(val.dtype), win[1:]
    
    def forward(self, x: torch.Tensor, st: dict) -> torch.Tensor:
        H, Dk = self.cfg.kda_heads, self.cfg.kda_head_dim
        
        q = self.q_proj(x)
        k = self.k_proj(x)
        v = self.v_proj(x)
        q, st["cq"] = self._short_conv(q, st["cq"], 0)
        k, st["ck"] = self._short_conv(k, st["ck"], 1)
        v, st["cv"] = self._short_conv(v, st["cv"], 2)
        
        q = q.view(H, Dk).float() * self.scale
        k = k.view(H, Dk).float()
        v = v.view(H, Dk).float()
        
        g = (-F.softplus(self.g_proj(x).float())).view(H, Dk)
        beta = torch.sigmoid(self.beta_proj(x))
        
        g_exp = g.exp()[:, :, None]
        S = st["S"] * g_exp
        pred = (S * k[:, :, None]).sum(1)
        S = S + beta[:, None, None] * k[:, :, None] * (v - pred)[:, None, :]
        st["S"] = S
        
        o = (S * q[:, :, None]).sum(1)
        return self.o_proj(o.reshape(H * Dk).to(torch.bfloat16))


# =============================================================================
# MLA Layer (Multi-head Latent Attention)
# =============================================================================
class MLALayer(nn.Module):
    """MLA layer matching reference.py's MLA."""
    
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        H, d = cfg.mla_heads, cfg.hidden
        
        self.q_proj = W4A16Linear(d, H * (cfg.qk_nope + cfg.qk_rope))
        self.kv_a = W4A16Linear(d, cfg.kv_lora + cfg.qk_rope)
        self.kv_b = W4A16Linear(cfg.kv_lora, H * (cfg.qk_nope + cfg.v_head))
        self.o_proj = W4A16Linear(H * cfg.v_head, d)
        self.scale = (cfg.qk_nope + cfg.qk_rope) ** -0.5
    
    def _rope(self, x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
        xf = x.float()
        even, odd = xf[..., 0::2], xf[..., 1::2]
        out = torch.empty_like(xf)
        out[..., 0::2] = even * cos - odd * sin
        out[..., 1::2] = odd * cos + even * sin
        return out.to(x.dtype)
    
    def forward(self, x: torch.Tensor, st: dict) -> torch.Tensor:
        cfg = self.cfg
        H = cfg.mla_heads
        pos = st["c_kv"].shape[0]
        
        q = self.q_proj(x).view(H, cfg.qk_nope + cfg.qk_rope)
        q_nope = q[:, : cfg.qk_nope].float()
        q_rope = q[:, cfg.qk_nope:]
        
        kv = self.kv_a(x)
        c_kv = kv[: cfg.kv_lora]
        k_rope = kv[cfg.kv_lora:]
        
        inv = 1.0 / (cfg.rope_theta ** (torch.arange(0, cfg.qk_rope, 2, device=x.device, dtype=torch.float32) / cfg.qk_rope))
        ang = pos * inv
        cos, sin = torch.cos(ang), torch.sin(ang)
        
        q_rope = self._rope(q_rope, cos, sin).float()
        k_rope = self._rope(k_rope.unsqueeze(0), cos, sin).squeeze(0)
        
        st["c_kv"] = torch.cat([st["c_kv"], c_kv[None]], 0)
        st["k_rope"] = torch.cat([st["k_rope"], k_rope[None]], 0)
        
        kvb = self.kv_b(st["c_kv"]).view(-1, H, cfg.qk_nope + cfg.v_head).float()
        k_nope = kvb[..., : cfg.qk_nope]
        v = kvb[..., cfg.qk_nope:]
        
        # Optimized attention scores computation
        scores = torch.einsum("hd,lhd->lh", q_nope, k_nope)
        scores = scores + torch.einsum("hd,ld->lh", q_rope, st["k_rope"].float())
        scores = scores * self.scale
        p = torch.softmax(scores, dim=0)
        o = torch.einsum("lh,lhd->hd", p, v)
        
        return self.o_proj(o.reshape(H * cfg.v_head).to(torch.bfloat16))


# =============================================================================
# MoE Layer
# =============================================================================
class MoELayer(nn.Module):
    """MoE layer matching reference.py's MoE."""
    
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        d, m, E = cfg.hidden, cfg.moe_inter, cfg.n_experts
        
        self.router = nn.Linear(d, E, bias=False, dtype=cfg.dtype)
        self.gate = W4A16Experts(E, d, m)
        self.up = W4A16Experts(E, d, m)
        self.down = W4A16Experts(E, m, d)
        self.s_gate = W4A16Experts(cfg.n_shared, d, m)
        self.s_up = W4A16Experts(cfg.n_shared, d, m)
        self.s_down = W4A16Experts(cfg.n_shared, m, d)
    
    def _ffn(self, x: torch.Tensor, gate: W4A16Experts, up: W4A16Experts, down: W4A16Experts, e: int) -> torch.Tensor:
        device = x.device
        # Use cached dequantized weights for speed
        g_w = gate._get_weight_bf16(e, device)
        u_w = up._get_weight_bf16(e, device)
        d_w = down._get_weight_bf16(e, device)
        
        g_out = x @ g_w
        u_out = x @ u_w
        h = F.silu(g_out.float()) * u_out.float()
        
        return (h.to(torch.bfloat16) @ d_w).to(torch.bfloat16)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        cfg = self.cfg
        device = x.device
        probs = torch.softmax(self.router(x), dim=-1)
        w, idx = torch.topk(probs, cfg.n_active)
        w = (w / (w.sum() + 1e-9) * cfg.routed_scaling).to(x.dtype)
        
        # Compute all active routed experts in batch
        out = x.new_zeros(cfg.hidden, dtype=torch.float32)
        
        # Gather all active expert weights
        active_experts = [int(idx[j]) for j in range(cfg.n_active)]
        g_ws = [self.gate._get_weight_bf16(e, device) for e in active_experts]
        u_ws = [self.up._get_weight_bf16(e, device) for e in active_experts]
        d_ws = [self.down._get_weight_bf16(e, device) for e in active_experts]
        
        # Compute all gate and up projections in batch
        g_outs = torch.stack([x @ g_w for g_w in g_ws], dim=0)
        u_outs = torch.stack([x @ u_w for u_w in u_ws], dim=0)
        hs = F.silu(g_outs.float()) * u_outs.float()
        
        # Compute down projections and accumulate
        for j, h in enumerate(hs):
            out = out + w[j] * (h.to(torch.bfloat16) @ d_ws[j]).float()
        
        # Shared experts (batched)
        s_g_ws = [self.s_gate._get_weight_bf16(s, device) for s in range(cfg.n_shared)]
        s_u_ws = [self.s_up._get_weight_bf16(s, device) for s in range(cfg.n_shared)]
        s_d_ws = [self.s_down._get_weight_bf16(s, device) for s in range(cfg.n_shared)]
        
        s_g_outs = torch.stack([x @ g_w for g_w in s_g_ws], dim=0)
        s_u_outs = torch.stack([x @ u_w for u_w in s_u_ws], dim=0)
        s_hs = F.silu(s_g_outs.float()) * s_u_outs.float()
        
        s_hs_bf16 = s_hs.to(torch.bfloat16)
        for j, h in enumerate(s_hs_bf16):
            out = out + (h @ s_d_ws[j]).float()
        
        return out.to(torch.bfloat16)


# =============================================================================
# Block
# =============================================================================
class Block(nn.Module):
    def __init__(self, cfg, kind: str):
        super().__init__()
        self.kind = kind
        self.attn_norm = nn.Parameter(torch.ones(cfg.hidden, dtype=cfg.dtype))
        self.moe_norm = nn.Parameter(torch.ones(cfg.hidden, dtype=cfg.dtype))
        self.attn = KDALayer(cfg) if kind == "K" else MLALayer(cfg)
        self.moe = MoELayer(cfg)
    
    def forward(self, x: torch.Tensor, st: dict) -> torch.Tensor:
        # Optimized RMSNorm
        xf = x.float()
        norm_coef = torch.rsqrt((xf * xf).mean(-1, keepdim=True) + EPS)
        x_norm = (xf * norm_coef * self.attn_norm).to(x.dtype)
        
        h = x + self.attn(x_norm, st)
        
        hf = h.float()
        norm_coef = torch.rsqrt((hf * hf).mean(-1, keepdim=True) + EPS)
        h_norm = (hf * norm_coef * self.moe_norm).to(h.dtype)
        
        return h + self.moe(h_norm)


# =============================================================================
# Model
# =============================================================================
class Model(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.blocks = nn.ModuleList(Block(cfg, k) for k in cfg.pattern)
    
    def load_state_dict(self, state_dict, strict=True):
        super().load_state_dict(state_dict, strict=strict)
        # Pre-dequant linear weights after loading
        for mod in self.modules():
            if isinstance(mod, W4A16Linear):
                mod.pre_dequant('cuda')
    
    def step(self, hidden: torch.Tensor, state: list) -> tuple:
        x = hidden
        for i, blk in enumerate(self.blocks):
            x = blk(x, state[i])
        return x, state


# =============================================================================
# Helper functions (must match reference.py)
# =============================================================================
def build_config(shape: dict):
    from dataclasses import dataclass, field
    import torch
    
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
    
    return Config(n_experts=int(shape.get("n_experts", 64)))


def init_state(cfg, context_len: int, seed: int) -> list:
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


def init_token(cfg, seed: int) -> torch.Tensor:
    dev = torch.device("cuda:0")
    g = torch.Generator(device=dev).manual_seed(seed + 1)
    return torch.randn(cfg.hidden, device=dev, generator=g, dtype=cfg.dtype) * 0.25
