"""W4A16 Kimi-Linear decode -- single fused Triton megakernel (solution).

The entire per-token forward (4 blocks, MoE FFNs, KDA recurrence, MLA latent
attention, RMSNorms, residuals, all int4 dequant-GEMVs) runs in ONE Triton
kernel launch (mkern.megakernel). Buffer/parameter names match reference.py so
load_state_dict(strict=True) loads the reference weights.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import torch
import torch.nn as nn

import mkern

EPS = 1.0e-6
GROUP = 128


def _pack_int4(w_q):
    lo = w_q[0::2] & 0xF
    hi = w_q[1::2] & 0xF
    return (lo | (hi << 4)).contiguous()


def quantize(w_io, group=GROUP):
    K, N = w_io.shape
    ng = K // group
    wg = w_io.view(ng, group, N).float()
    wmin = wg.min(dim=1, keepdim=True).values
    wmax = wg.max(dim=1, keepdim=True).values
    scales = (wmax - wmin).clamp_min(1e-8) / 15.0
    zeros = (-wmin / scales).round().clamp(0, 15)
    w_q = ((wg / scales) + zeros).round().clamp(0, 15).to(torch.uint8).view(K, N)
    return _pack_int4(w_q), scales.squeeze(1).to(torch.bfloat16), zeros.squeeze(1).to(torch.bfloat16)


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
    n_experts: int = 64
    n_active: int = 8
    n_shared: int = 1
    moe_inter: int = 1024
    routed_scaling: float = 2.446
    group: int = 128
    pattern: tuple = ("K", "K", "K", "M")
    dtype: torch.dtype = field(default=torch.bfloat16)


def build_config(shape):
    return Config(n_experts=int(shape.get("n_experts", 64)))


# ----- quant classes (buffer names identical to reference) -----------------
class QuantLinear(nn.Module):
    def __init__(self, in_f, out_f, group=GROUP):
        super().__init__()
        self.in_f, self.out_f, self.group = in_f, out_f, group
        ng = in_f // group
        self.register_buffer("w_q", torch.zeros(in_f // 2, out_f, dtype=torch.uint8))
        self.register_buffer("scales", torch.zeros(ng, out_f, dtype=torch.bfloat16))
        self.register_buffer("zeros", torch.zeros(ng, out_f, dtype=torch.bfloat16))


class QuantExperts(nn.Module):
    def __init__(self, n, in_f, out_f, group=GROUP):
        super().__init__()
        self.n, self.in_f, self.out_f, self.group = n, in_f, out_f, group
        ng = in_f // group
        self.register_buffer("w_q", torch.zeros(n, in_f // 2, out_f, dtype=torch.uint8))
        self.register_buffer("scales", torch.zeros(n, ng, out_f, dtype=torch.bfloat16))
        self.register_buffer("zeros", torch.zeros(n, ng, out_f, dtype=torch.bfloat16))


class KDA(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        d = cfg.hidden
        H, Dk = cfg.kda_heads, cfg.kda_head_dim
        self.q_proj = QuantLinear(d, H * Dk, cfg.group)
        self.k_proj = QuantLinear(d, H * Dk, cfg.group)
        self.v_proj = QuantLinear(d, H * Dk, cfg.group)
        self.g_proj = QuantLinear(d, H * Dk, cfg.group)
        self.beta_proj = nn.Linear(d, H, bias=False, dtype=cfg.dtype)
        self.conv_w = nn.Parameter(torch.empty(3, H * Dk, cfg.short_conv, dtype=cfg.dtype))
        self.o_proj = QuantLinear(H * Dk, d, cfg.group)


class MLA(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        H, d = cfg.mla_heads, cfg.hidden
        self.q_proj = QuantLinear(d, H * (cfg.qk_nope + cfg.qk_rope), cfg.group)
        self.kv_a = QuantLinear(d, cfg.kv_lora + cfg.qk_rope, cfg.group)
        self.kv_b = QuantLinear(cfg.kv_lora, H * (cfg.qk_nope + cfg.v_head), cfg.group)
        self.o_proj = QuantLinear(H * cfg.v_head, d, cfg.group)


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


class Block(nn.Module):
    def __init__(self, cfg, kind):
        super().__init__()
        self.kind = kind
        self.attn_norm = nn.Parameter(torch.ones(cfg.hidden, dtype=cfg.dtype))
        self.moe_norm = nn.Parameter(torch.ones(cfg.hidden, dtype=cfg.dtype))
        self.attn = KDA(cfg) if kind == "K" else MLA(cfg)
        self.moe = MoE(cfg)


def init_state(cfg, context_len, seed):
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


def init_token(cfg, seed):
    dev = torch.device("cuda:0")
    g = torch.Generator(device=dev).manual_seed(seed + 1)
    return torch.randn(cfg.hidden, device=dev, generator=g, dtype=cfg.dtype) * 0.25


# ============================ Model =======================================
class Model(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.blocks = nn.ModuleList(Block(cfg, k) for k in cfg.pattern)
        self.reset_parameters()
        self._build_workspace()
        self._table_built = False
        self._last_sig = None
        self._gen = 0
        self._mla_len = 0

    def reset_parameters(self):
        g = torch.Generator(device="cpu").manual_seed(1234)
        for mod in self.modules():
            if isinstance(mod, (QuantLinear, QuantExperts)):
                w = torch.randn(mod.in_f, mod.out_f, generator=g) * 0.02
                wq, s, z = quantize(w, mod.group)
                mod.w_q.copy_(wq); mod.scales.copy_(s); mod.zeros.copy_(z)
            elif isinstance(mod, nn.Linear):
                nn.init.normal_(mod.weight, 0.0, 0.02, generator=g)

    def _build_workspace(self):
        dev = torch.device("cuda:0")
        M = mkern
        self.ws = {
            "w_norma": torch.zeros(M.HIDDEN, device=dev, dtype=torch.bfloat16),
            "w_qkvg": torch.zeros(4 * M.KDA_C, device=dev, dtype=torch.bfloat16),
            "w_beta": torch.zeros(M.KDA_H, device=dev, dtype=torch.float32),
            "w_oat": torch.zeros(M.KDA_C, device=dev, dtype=torch.bfloat16),
            "w_h1": torch.zeros(M.HIDDEN, device=dev, dtype=torch.bfloat16),
            "w_normm": torch.zeros(M.HIDDEN, device=dev, dtype=torch.bfloat16),
            "w_logits": torch.zeros(M.N_EXP, device=dev, dtype=torch.float32),
            "w_idx": torch.zeros(M.N_ACT, device=dev, dtype=torch.int32),
            "w_wsel": torch.zeros(M.N_ACT, device=dev, dtype=torch.float32),
            "w_hh": torch.zeros(M.EXPERTS, M.MOE_M, device=dev, dtype=torch.bfloat16),
            "w_up": torch.zeros(M.EXPERTS, M.MOE_M, device=dev, dtype=torch.bfloat16),
            "w_down": torch.zeros(M.EXPERTS, M.HIDDEN, device=dev, dtype=torch.bfloat16),
            "w_moeout": torch.zeros(M.HIDDEN, device=dev, dtype=torch.bfloat16),
            "w_h2": torch.zeros(M.HIDDEN, device=dev, dtype=torch.bfloat16),
            "w_mlaq": torch.zeros(M.MLA_H * (M.QK_NOPE + M.QK_ROPE), device=dev, dtype=torch.bfloat16),
            "w_kva": torch.zeros(M.KV_LORA + M.QK_ROPE, device=dev, dtype=torch.bfloat16),
            "w_qabs": torch.zeros(M.MLA_H, M.KV_LORA, device=dev, dtype=torch.float32),
            "w_cvw": torch.zeros(M.MLA_H, M.KV_LORA, device=dev, dtype=torch.float32),
            "w_omla": torch.zeros(M.MLA_H * M.V_HEAD, device=dev, dtype=torch.bfloat16),
            "w_ckv": torch.zeros(M.CAP, M.KV_LORA, device=dev, dtype=torch.bfloat16),
            "w_krp": torch.zeros(M.CAP, M.QK_ROPE, device=dev, dtype=torch.bfloat16),
            "w_pos": torch.zeros(1, device=dev, dtype=torch.int32),
            "w_cvp": torch.zeros(M.NTMAX, M.MLA_H, M.KV_LORA, device=dev, dtype=torch.bfloat16),
            "w_msp": torch.zeros(M.NTMAX, M.MLA_H, 2, device=dev, dtype=torch.float32),
            "w_ropeinv": (1.0/(10000.0 ** (torch.arange(0, int(M.QK_ROPE)//2, dtype=torch.float32)/float(M.QK_ROPE)))).cuda(),
            "w_bar": torch.zeros(M.NPHASE, device=dev, dtype=torch.int32),
        }

    def _blk_ptrs(self, blk):
        """Pointers for one block's weights, in mkern.ENTRY order."""
        a = blk.attn; m = blk.moe
        P = []
        if blk.kind == "K":
            for p in (a.q_proj, a.k_proj, a.v_proj, a.g_proj, a.o_proj):
                P += [p.w_q, p.scales, p.zeros]
            P += [a.beta_proj.weight, a.conv_w]
        else:
            for p in (a.q_proj, a.kv_a, a.kv_b, a.o_proj):
                P += [p.w_q, p.scales, p.zeros]
        P += [blk.attn_norm, blk.moe_norm]
        for e in (m.gate, m.up, m.down, m.s_gate, m.s_up, m.s_down):
            P += [e.w_q, e.scales, e.zeros]
        P += [m.router.weight]
        return P

    def _build_table(self):
        ptrs = []
        for blk in self.blocks:
            ptrs += self._blk_ptrs(blk)
        # workspace in mkern.ENTRY workspace order
        ws_names = [n for n in mkern.ENTRY if n.startswith("w_")]
        for n in ws_names:
            ptrs.append(self.ws[n])
        T = torch.tensor([p.data_ptr() for p in ptrs], device="cuda", dtype=torch.int64)
        assert T.numel() == mkern.NTAB, (T.numel(), mkern.NTAB)
        self.T = T

    def step(self, hidden, state):
        if not self._table_built:
            self._build_table()
            self._table_built = True
        sig = (state[0]["S"].data_ptr(), id(state))
        if sig != self._last_sig:
            migrate = 1
            self._last_sig = sig
            ref_ckv = state[3]["c_kv"]
            ref_krp = state[3]["k_rope"]
            ctx = ref_ckv.shape[0]
            self._mla_len = ctx
        else:
            migrate = 0
            ref_ckv = state[3]["c_kv"]
            ref_krp = state[3]["k_rope"]
            ctx = 0
        out = torch.empty_like(hidden)
        kda_state = [(state[i]["S"], state[i]["cq"], state[i]["ck"], state[i]["cv"]) for i in range(3)]
        mkern.launch(self.T, hidden, out, kda_state, ref_ckv, ref_krp, ctx, migrate, self._gen)
        self._gen += 1
        self._mla_len += 1
        state[3]["c_kv"] = self.ws["w_ckv"][:self._mla_len]
        state[3]["k_rope"] = self.ws["w_krp"][:self._mla_len]
        return out, state
