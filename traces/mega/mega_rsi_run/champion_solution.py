"""Fused single-launch Triton megakernel for Kimi-Linear W4A16 hybrid decode.

The entire per-token forward (3 KDA blocks + 1 MLA block, each + 64-expert MoE,
RMSNorms, residuals, short conv, gated-delta recurrence, MLA latent attention,
fused int4 dequant-GEMV) is fused into ONE @triton.jit grid launch, invoked
exactly once per step(). Cross-block sequencing uses a grid-wide monotonic
barrier over a persistent counter buffer; there is no CUDA graph, no
torch.compile, no per-op kernel loop. The int4 unpack + per-group dequant is
fused directly into every GEMV so the 4-bit weights are streamed once.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import torch
import torch.nn as nn
import triton
import triton.language as tl

EPS = 1.0e-6
EPS_C = tl.constexpr(1.0e-6)
GROUP_SIZE = 128
NPROG = 152  # persistent programs; must all co-reside (<= resident CTA capacity)

KSCALE = tl.constexpr(0.08838834764831843)   # 1/sqrt(128)
MLASCALE = tl.constexpr(0.07216878364870323)  # 1/sqrt(192)
LN10000 = tl.constexpr(9.210340371976182)


# --------------------------------------------------------------------------- #
# Module shells (match reference buffer/parameter names for state_dict load)
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


# --------------------------------------------------------------------------- #
# Device helpers
# --------------------------------------------------------------------------- #
@triton.jit
def _bar(bar_ptr, site, step, NP: tl.constexpr):
    tl.atomic_add(bar_ptr + site, 1, sem="acq_rel")
    tgt = (step + 1) * NP
    while tl.atomic_add(bar_ptr + site, 0, sem="acquire") < tgt:
        pass


@triton.jit
def gemv_col(x_ptr, wq_ptr, woff, sc_ptr, soff, zr_ptr, zoff, N, n0,
             BN: tl.constexpr, NG: tl.constexpr):
    n = n0 + tl.arange(0, BN)
    nm = n < N
    acc = tl.zeros([BN], tl.float32)
    j = tl.arange(0, 64)
    for g in range(NG):
        base = g * 128
        xe = tl.load(x_ptr + base + 2 * j)
        xo = tl.load(x_ptr + base + 2 * j + 1)
        wp = tl.load(wq_ptr + woff + (g * 64 + j)[:, None] * N + n[None, :],
                     mask=nm[None, :], other=0).to(tl.int32)
        lo = (wp & 0xF).to(tl.float32)
        hi = ((wp >> 4) & 0xF).to(tl.float32)
        dot = tl.sum(xe[:, None] * lo + xo[:, None] * hi, axis=0)
        sx = tl.sum(xe + xo)
        s = tl.load(sc_ptr + soff + g * N + n, mask=nm, other=0.0).to(tl.float32)
        z = tl.load(zr_ptr + zoff + g * N + n, mask=nm, other=0.0).to(tl.float32)
        acc += s * (dot - z * sx)
    return acc


@triton.jit
def rmsnorm_write(src_ptr, w_ptr, woff, dst_ptr, D: tl.constexpr, pid, NP: tl.constexpr):
    ss = 0.0
    for o in range(0, D, 256):
        idx = o + tl.arange(0, 256)
        m = idx < D
        v = tl.load(src_ptr + idx, mask=m, other=0.0)
        ss += tl.sum(v * v)
    rstd = 1.0 / tl.sqrt(ss / D + EPS_C)
    CB: tl.constexpr = 256
    for c0 in range(pid * CB, D, NP * CB):
        idx = c0 + tl.arange(0, CB)
        m = idx < D
        v = tl.load(src_ptr + idx, mask=m, other=0.0)
        w = tl.load(w_ptr + woff + idx, mask=m, other=0.0).to(tl.float32)
        tl.store(dst_ptr + idx, v * rstd * w, mask=m)


# --------------------------------------------------------------------------- #
# The megakernel
# --------------------------------------------------------------------------- #
@triton.jit
def mega(
    hidden_in, out, s_hidden, s_norm, s_proj, s_kva, s_conv, s_o, s_beta,
    s_qrope, s_qabs, s_ctx, s_wkb, s_h, s_router, s_topw, s_topidx, bar,
    # KDA stacked weights [3, ...]
    kq_wq, kq_sc, kq_zr, kk_wq, kk_sc, kk_zr, kv_wq, kv_sc, kv_zr,
    kg_wq, kg_sc, kg_zr, ko_wq, ko_sc, ko_zr, kbeta, kconv,
    # KDA states (per block)
    S0, S1, S2, cq0, ck0, cv0, cq1, ck1, cv1, cq2, ck2, cv2,
    # MLA weights
    mq_wq, mq_sc, mq_zr, ma_wq, ma_sc, ma_zr, mb_wq, mb_sc, mb_zr, mo_wq, mo_sc, mo_zr,
    ckv_old, krope_old, ckv_new, krope_new, pos,
    # norms
    anorm, mnorm,
    # MoE stacked weights [4, ...]
    g_wq, g_sc, g_zr, u_wq, u_sc, u_zr, d_wq, d_sc, d_zr,
    sg_wq, sg_sc, sg_zr, su_wq, su_sc, su_zr, sd_wq, sd_sc, sd_zr, router,
    step,
    NP: tl.constexpr,
):
    pid = tl.program_id(0)
    D: tl.constexpr = 2304
    HD: tl.constexpr = 4096

    # ---- P0: hidden_in (bf16) -> s_hidden (f32) ----
    for c0 in range(pid * 256, D, NP * 256):
        idx = c0 + tl.arange(0, 256)
        m = idx < D
        v = tl.load(hidden_in + idx, mask=m, other=0.0).to(tl.float32)
        tl.store(s_hidden + idx, v, mask=m)
    _bar(bar, 60, step, NP)

    # ============================ KDA blocks 0,1,2 ============================
    for blk in range(3):
        base = blk * 8
        if blk == 0:
            Sp = S0; cqp = cq0; ckp = ck0; cvp = cv0
        elif blk == 1:
            Sp = S1; cqp = cq1; ckp = ck1; cvp = cv1
        else:
            Sp = S2; cqp = cq2; ckp = ck2; cvp = cv2

        # P1 rmsnorm(attn)
        rmsnorm_write(s_hidden, anorm, blk * D, s_norm, D, pid, NP)
        _bar(bar, base + 0, step, NP)

        # P2 GEMV q,k,v,g -> s_proj[4*4096]; beta -> s_beta
        woff = blk * 1152 * HD
        soff = blk * 18 * HD
        NT: tl.constexpr = HD // 128
        for t in range(pid, NT, NP):
            n0 = t * 128
            a = gemv_col(s_norm, kq_wq, woff, kq_sc, soff, kq_zr, soff, HD, n0, 128, 18)
            tl.store(s_proj + 0 * HD + n0 + tl.arange(0, 128), a)
        for t in range(pid, NT, NP):
            n0 = t * 128
            a = gemv_col(s_norm, kk_wq, woff, kk_sc, soff, kk_zr, soff, HD, n0, 128, 18)
            tl.store(s_proj + 1 * HD + n0 + tl.arange(0, 128), a)
        for t in range(pid, NT, NP):
            n0 = t * 128
            a = gemv_col(s_norm, kv_wq, woff, kv_sc, soff, kv_zr, soff, HD, n0, 128, 18)
            tl.store(s_proj + 2 * HD + n0 + tl.arange(0, 128), a)
        for t in range(pid, NT, NP):
            n0 = t * 128
            a = gemv_col(s_norm, kg_wq, woff, kg_sc, soff, kg_zr, soff, HD, n0, 128, 18)
            tl.store(s_proj + 3 * HD + n0 + tl.arange(0, 128), a)
        # beta
        DPAD: tl.constexpr = 4096
        dm = tl.arange(0, DPAD) < D
        xd = tl.load(s_norm + tl.arange(0, DPAD), mask=dm, other=0.0)
        for hh in range(pid, 32, NP):
            wrow = tl.load(kbeta + (blk * 32 + hh) * D + tl.arange(0, DPAD), mask=dm, other=0.0).to(tl.float32)
            bv = tl.sum(xd * wrow)
            tl.store(s_beta + hh, 1.0 / (1.0 + tl.exp(-bv)))
        _bar(bar, base + 1, step, NP)

        # P3 conv+silu for q,k,v ; update conv window
        CB: tl.constexpr = 64
        for c0 in range(pid * CB, HD, NP * CB):
            c = c0 + tl.arange(0, CB)
            for seg in range(3):
                if seg == 0:
                    stp = cqp
                elif seg == 1:
                    stp = ckp
                else:
                    stp = cvp
                raw = tl.load(s_proj + seg * HD + c)
                p0 = tl.load(stp + 0 * HD + c).to(tl.float32)
                p1 = tl.load(stp + 1 * HD + c).to(tl.float32)
                p2 = tl.load(stp + 2 * HD + c).to(tl.float32)
                wb = (blk * 3 + seg) * HD * 4
                w0 = tl.load(kconv + wb + c * 4 + 0).to(tl.float32)
                w1 = tl.load(kconv + wb + c * 4 + 1).to(tl.float32)
                w2 = tl.load(kconv + wb + c * 4 + 2).to(tl.float32)
                w3 = tl.load(kconv + wb + c * 4 + 3).to(tl.float32)
                o = p0 * w0 + p1 * w1 + p2 * w2 + raw * w3
                o = o / (1.0 + tl.exp(-o))  # silu
                tl.store(s_conv + seg * HD + c, o)
                tl.store(stp + 0 * HD + c, p1.to(tl.bfloat16))
                tl.store(stp + 1 * HD + c, p2.to(tl.bfloat16))
                tl.store(stp + 2 * HD + c, raw.to(tl.bfloat16))
        _bar(bar, base + 2, step, NP)

        # P4 recurrence over (h,j)
        ii = tl.arange(0, 128)
        for item in range(pid, HD, NP):
            h = item // 128
            j = item % 128
            q_h = tl.load(s_conv + 0 * HD + h * 128 + ii) * KSCALE
            k_h = tl.load(s_conv + 1 * HD + h * 128 + ii)
            graw = tl.load(s_proj + 3 * HD + h * 128 + ii)
            sp = tl.where(graw > 20.0, graw, tl.log(1.0 + tl.exp(graw)))
            eg = tl.exp(-sp)
            v_hj = tl.load(s_conv + 2 * HD + h * 128 + j)
            beta = tl.load(s_beta + h)
            Scol = tl.load(Sp + h * 128 * 128 + ii * 128 + j)
            Sdec = Scol * eg
            pred = tl.sum(Sdec * k_h)
            coef = beta * (v_hj - pred)
            Snew = Sdec + coef * k_h
            o_hj = tl.sum(Snew * q_h)
            tl.store(Sp + h * 128 * 128 + ii * 128 + j, Snew)
            tl.store(s_o + h * 128 + j, o_hj)
        _bar(bar, base + 3, step, NP)

        # P5 o_proj (4096 -> 2304), add residual
        oo = blk * 2048 * D
        os = blk * 32 * D
        NTD: tl.constexpr = (D + 127) // 128
        for t in range(pid, NTD, NP):
            n0 = t * 128
            a = gemv_col(s_o, ko_wq, oo, ko_sc, os, ko_zr, os, D, n0, 128, 32)
            idx = n0 + tl.arange(0, 128)
            m = idx < D
            cur = tl.load(s_hidden + idx, mask=m, other=0.0)
            tl.store(s_hidden + idx, cur + a, mask=m)
        _bar(bar, base + 4, step, NP)

        # ---- MoE for this block ----
        _moe(pid, NP, blk, step, bar, 32 + blk * 5, s_hidden, s_norm, s_h,
             s_router, s_topw, s_topidx, mnorm, router,
             g_wq, g_sc, g_zr, u_wq, u_sc, u_zr, d_wq, d_sc, d_zr,
             sg_wq, sg_sc, sg_zr, su_wq, su_sc, su_zr, sd_wq, sd_sc, sd_zr)

    # ============================ MLA block 3 ============================
    HD2: tl.constexpr = 4096
    QHD: tl.constexpr = 6144
    # P1 rmsnorm
    rmsnorm_write(s_hidden, anorm, 3 * D, s_norm, D, pid, NP)
    _bar(bar, 24, step, NP)

    # P2 q_proj (6144), kv_a (576), dequant kv_b -> s_wkb[512,8192]
    NTQ: tl.constexpr = QHD // 128
    for t in range(pid, NTQ, NP):
        n0 = t * 128
        a = gemv_col(s_norm, mq_wq, 0, mq_sc, 0, mq_zr, 0, QHD, n0, 128, 18)
        tl.store(s_proj + n0 + tl.arange(0, 128), a)
    NTA: tl.constexpr = (576 + 127) // 128
    for t in range(pid, NTA, NP):
        n0 = t * 128
        a = gemv_col(s_norm, ma_wq, 0, ma_sc, 0, ma_zr, 0, 576, n0, 128, 18)
        idx = n0 + tl.arange(0, 128)
        tl.store(s_kva + idx, a, mask=idx < 576)
    # dequant kv_b: rows c in 0..511, cols 0..8191
    for c in range(pid, 512, NP):
        jrow = c // 2
        even = (c % 2) == 0
        gg = c // 128
        for ct in range(0, 8192, 256):
            cols = ct + tl.arange(0, 256)
            pk = tl.load(mb_wq + jrow * 8192 + cols).to(tl.int32)
            nib = tl.where(even, pk & 0xF, (pk >> 4) & 0xF).to(tl.float32)
            sc = tl.load(mb_sc + gg * 8192 + cols).to(tl.float32)
            zr = tl.load(mb_zr + gg * 8192 + cols).to(tl.float32)
            tl.store(s_wkb + c * 8192 + cols, (nib - zr) * sc)
    _bar(bar, 25, step, NP)

    # P3 rope + cache copy/append
    if pid == 0:
        ir = tl.arange(0, 32)
        ang = pos.to(tl.float32) * tl.exp(-(ir.to(tl.float32) / 32.0) * LN10000)
        cs = tl.cos(ang)
        sn = tl.sin(ang)
        for h in range(32):
            e = tl.load(s_proj + h * 192 + 128 + 2 * ir).to(tl.float32)
            o = tl.load(s_proj + h * 192 + 128 + 2 * ir + 1).to(tl.float32)
            tl.store(s_qrope + h * 64 + 2 * ir, e * cs - o * sn)
            tl.store(s_qrope + h * 64 + 2 * ir + 1, o * cs + e * sn)
        ek = tl.load(s_kva + 512 + 2 * ir).to(tl.float32)
        ok = tl.load(s_kva + 512 + 2 * ir + 1).to(tl.float32)
        tl.store(krope_new + pos * 64 + 2 * ir, (ek * cs - ok * sn).to(tl.bfloat16))
        tl.store(krope_new + pos * 64 + 2 * ir + 1, (ok * cs + ek * sn).to(tl.bfloat16))
        cvec = tl.arange(0, 512)
        cc = tl.load(s_kva + cvec)
        tl.store(ckv_new + pos * 512 + cvec, cc.to(tl.bfloat16))
    # copy old cache
    tot = pos * 512
    for e0 in range(pid * 256, tot, NP * 256):
        idx = e0 + tl.arange(0, 256)
        m = idx < tot
        tl.store(ckv_new + idx, tl.load(ckv_old + idx, mask=m, other=0), mask=m)
    tot2 = pos * 64
    for e0 in range(pid * 256, tot2, NP * 256):
        idx = e0 + tl.arange(0, 256)
        m = idx < tot2
        tl.store(krope_new + idx, tl.load(krope_old + idx, mask=m, other=0), mask=m)
    _bar(bar, 26, step, NP)

    # P4 qabs (h, c-tile)
    NQ: tl.constexpr = 32 * (512 // 128)
    for tile in range(pid, NQ, NP):
        h = tile // 4
        c0 = (tile % 4) * 128
        qn = tl.load(s_proj + h * 192 + tl.arange(0, 128))
        rows = c0 + tl.arange(0, 128)
        cols = h * 256 + tl.arange(0, 128)
        w = tl.load(s_wkb + rows[:, None] * 8192 + cols[None, :])
        qa = tl.sum(w * qn[None, :], axis=1)
        tl.store(s_qabs + h * 512 + c0 + tl.arange(0, 128), qa)
    _bar(bar, 27, step, NP)

    # P5 attention per head (online softmax)
    L = pos + 1
    cvec = tl.arange(0, 512)
    rvec = tl.arange(0, 64)
    for h in range(pid, 32, NP):
        qabs = tl.load(s_qabs + h * 512 + cvec)
        qrope = tl.load(s_qrope + h * 64 + rvec)
        m = -1e30
        den = 0.0
        ctx = tl.zeros([512], tl.float32)
        for l in range(L):
            ckvl = tl.load(ckv_new + l * 512 + cvec).to(tl.float32)
            krl = tl.load(krope_new + l * 64 + rvec).to(tl.float32)
            sc = (tl.sum(qabs * ckvl) + tl.sum(qrope * krl)) * MLASCALE
            nm = tl.maximum(m, sc)
            corr = tl.exp(m - nm)
            p = tl.exp(sc - nm)
            den = den * corr + p
            ctx = ctx * corr + p * ckvl
            m = nm
        ctx = ctx / den
        tl.store(s_ctx + h * 512 + cvec, ctx)
    _bar(bar, 28, step, NP)

    # P6 o-projection (h, e-tile) -> s_o
    for tile in range(pid, 32, NP):
        h = tile
        ctx_h = tl.load(s_ctx + h * 512 + cvec)
        cols = h * 256 + 128 + tl.arange(0, 128)
        w = tl.load(s_wkb + cvec[:, None] * 8192 + cols[None, :])
        o = tl.sum(w * ctx_h[:, None], axis=0)
        tl.store(s_o + h * 128 + tl.arange(0, 128), o)
    _bar(bar, 29, step, NP)

    # P7 o_proj (4096 -> 2304) add residual
    NTD2: tl.constexpr = (D + 127) // 128
    for t in range(pid, NTD2, NP):
        n0 = t * 128
        a = gemv_col(s_o, mo_wq, 0, mo_sc, 0, mo_zr, 0, D, n0, 128, 32)
        idx = n0 + tl.arange(0, 128)
        m = idx < D
        cur = tl.load(s_hidden + idx, mask=m, other=0.0)
        tl.store(s_hidden + idx, cur + a, mask=m)
    _bar(bar, 30, step, NP)

    # MoE block 3
    _moe(pid, NP, 3, step, bar, 47, s_hidden, s_norm, s_h,
         s_router, s_topw, s_topidx, mnorm, router,
         g_wq, g_sc, g_zr, u_wq, u_sc, u_zr, d_wq, d_sc, d_zr,
         sg_wq, sg_sc, sg_zr, su_wq, su_sc, su_zr, sd_wq, sd_sc, sd_zr)

    # ---- final: s_hidden (f32) -> out (bf16) ----
    for c0 in range(pid * 256, D, NP * 256):
        idx = c0 + tl.arange(0, 256)
        m = idx < D
        tl.store(out + idx, tl.load(s_hidden + idx, mask=m, other=0.0).to(tl.bfloat16), mask=m)


@triton.jit
def _moe(pid, NP: tl.constexpr, blk, step, bar, sbase, s_hidden, s_norm, s_h,
         s_router, s_topw, s_topidx, mnorm, router,
         g_wq, g_sc, g_zr, u_wq, u_sc, u_zr, d_wq, d_sc, d_zr,
         sg_wq, sg_sc, sg_zr, su_wq, su_sc, su_zr, sd_wq, sd_sc, sd_zr):
    D: tl.constexpr = 2304
    M: tl.constexpr = 1024
    E: tl.constexpr = 64
    SCALING = 2.446

    # MP1 rmsnorm(moe)
    rmsnorm_write(s_hidden, mnorm, blk * D, s_norm, D, pid, NP)
    _bar(bar, sbase + 0, step, NP)

    # MP2 router + topk8 (program 0)
    if pid == 0:
        DPAD: tl.constexpr = 4096
        dm = tl.arange(0, DPAD) < D
        xd = tl.load(s_norm + tl.arange(0, DPAD), mask=dm, other=0.0)
        for o in range(E):
            wrow = tl.load(router + (blk * E + o) * D + tl.arange(0, DPAD), mask=dm, other=0.0).to(tl.float32)
            tl.store(s_router + o, tl.sum(xd * wrow))
        lg = tl.load(s_router + tl.arange(0, E))
        mx = tl.max(lg, 0)
        ex = tl.exp(lg - mx)
        probs = ex / tl.sum(ex, 0)
        ar = tl.arange(0, E)
        for jsel in range(8):
            idx = tl.argmax(probs, 0)
            val = tl.max(probs, 0)
            tl.store(s_topidx + jsel, idx)
            tl.store(s_topw + jsel, val)
            probs = tl.where(ar == idx, -1.0, probs)
        wv = tl.load(s_topw + tl.arange(0, 8))
        ws = tl.sum(wv, 0)
        tl.store(s_topw + tl.arange(0, 8), wv / (ws + 1e-9) * SCALING)
    _bar(bar, sbase + 1, step, NP)

    # MP3 gate/up -> s_h[9,1024]
    NTM: tl.constexpr = 9 * (M // 128)
    for tile in range(pid, NTM, NP):
        slot = tile // (M // 128)
        m0 = (tile % (M // 128)) * 128
        if slot < 8:
            e = tl.load(s_topidx + slot)
            wo = (blk * E + e) * 1152 * M
            so = (blk * E + e) * 18 * M
            ag = gemv_col(s_norm, g_wq, wo, g_sc, so, g_zr, so, M, m0, 128, 18)
            au = gemv_col(s_norm, u_wq, wo, u_sc, so, u_zr, so, M, m0, 128, 18)
        else:
            wo = blk * 1152 * M
            so = blk * 18 * M
            ag = gemv_col(s_norm, sg_wq, wo, sg_sc, so, sg_zr, so, M, m0, 128, 18)
            au = gemv_col(s_norm, su_wq, wo, su_sc, so, su_zr, so, M, m0, 128, 18)
        hh = (ag / (1.0 + tl.exp(-ag))) * au
        tl.store(s_h + slot * M + m0 + tl.arange(0, 128), hh)
    _bar(bar, sbase + 2, step, NP)

    # MP4 down -> accumulate into s_hidden (atomic)
    NTD: tl.constexpr = 9 * ((D + 127) // 128)
    ntd: tl.constexpr = (D + 127) // 128
    for tile in range(pid, NTD, NP):
        slot = tile // ntd
        d0 = (tile % ntd) * 128
        if slot < 8:
            e = tl.load(s_topidx + slot)
            wo = (blk * E + e) * 512 * D
            so = (blk * E + e) * 8 * D
            wslot = tl.load(s_topw + slot)
            a = gemv_col(s_h + slot * M, d_wq, wo, d_sc, so, d_zr, so, D, d0, 128, 8)
        else:
            wo = blk * 512 * D
            so = blk * 8 * D
            wslot = 1.0
            a = gemv_col(s_h + slot * M, sd_wq, wo, sd_sc, so, sd_zr, so, D, d0, 128, 8)
        idx = d0 + tl.arange(0, 128)
        m = idx < D
        tl.atomic_add(s_hidden + idx, a * wslot, mask=m)
    _bar(bar, sbase + 3, step, NP)


# --------------------------------------------------------------------------- #
# Model
# --------------------------------------------------------------------------- #
class Model(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.blocks = nn.ModuleList(Block(cfg, k) for k in cfg.pattern)
        self._prepared = False
        self._step = 0

    def _prepare(self):
        dev = self.blocks[0].attn.q_proj.w_q.device
        K = [self.blocks[i].attn for i in range(3)]
        M = self.blocks[3].attn

        def st(getter):
            return torch.stack([getter(k) for k in K]).contiguous()

        self.kq_wq = st(lambda a: a.q_proj.w_q); self.kq_sc = st(lambda a: a.q_proj.scales); self.kq_zr = st(lambda a: a.q_proj.zeros)
        self.kk_wq = st(lambda a: a.k_proj.w_q); self.kk_sc = st(lambda a: a.k_proj.scales); self.kk_zr = st(lambda a: a.k_proj.zeros)
        self.kv_wq = st(lambda a: a.v_proj.w_q); self.kv_sc = st(lambda a: a.v_proj.scales); self.kv_zr = st(lambda a: a.v_proj.zeros)
        self.kg_wq = st(lambda a: a.g_proj.w_q); self.kg_sc = st(lambda a: a.g_proj.scales); self.kg_zr = st(lambda a: a.g_proj.zeros)
        self.ko_wq = st(lambda a: a.o_proj.w_q); self.ko_sc = st(lambda a: a.o_proj.scales); self.ko_zr = st(lambda a: a.o_proj.zeros)
        self.kbeta = st(lambda a: a.beta_proj.weight).contiguous()
        self.kconv = st(lambda a: a.conv_w).contiguous()

        self.mq_wq = M.q_proj.w_q.contiguous(); self.mq_sc = M.q_proj.scales.contiguous(); self.mq_zr = M.q_proj.zeros.contiguous()
        self.ma_wq = M.kv_a.w_q.contiguous(); self.ma_sc = M.kv_a.scales.contiguous(); self.ma_zr = M.kv_a.zeros.contiguous()
        self.mb_wq = M.kv_b.w_q.contiguous(); self.mb_sc = M.kv_b.scales.contiguous(); self.mb_zr = M.kv_b.zeros.contiguous()
        self.mo_wq = M.o_proj.w_q.contiguous(); self.mo_sc = M.o_proj.scales.contiguous(); self.mo_zr = M.o_proj.zeros.contiguous()

        self.anorm = torch.stack([b.attn_norm for b in self.blocks]).contiguous()
        self.mnorm = torch.stack([b.moe_norm for b in self.blocks]).contiguous()

        def stm(getter):
            return torch.stack([getter(b.moe) for b in self.blocks]).contiguous()

        self.g_wq = stm(lambda m: m.gate.w_q); self.g_sc = stm(lambda m: m.gate.scales); self.g_zr = stm(lambda m: m.gate.zeros)
        self.u_wq = stm(lambda m: m.up.w_q); self.u_sc = stm(lambda m: m.up.scales); self.u_zr = stm(lambda m: m.up.zeros)
        self.d_wq = stm(lambda m: m.down.w_q); self.d_sc = stm(lambda m: m.down.scales); self.d_zr = stm(lambda m: m.down.zeros)
        self.sg_wq = stm(lambda m: m.s_gate.w_q); self.sg_sc = stm(lambda m: m.s_gate.scales); self.sg_zr = stm(lambda m: m.s_gate.zeros)
        self.su_wq = stm(lambda m: m.s_up.w_q); self.su_sc = stm(lambda m: m.s_up.scales); self.su_zr = stm(lambda m: m.s_up.zeros)
        self.sd_wq = stm(lambda m: m.s_down.w_q); self.sd_sc = stm(lambda m: m.s_down.scales); self.sd_zr = stm(lambda m: m.s_down.zeros)
        self.router = stm(lambda m: m.router.weight).contiguous()

        # scratch
        f = lambda n: torch.empty(n, dtype=torch.float32, device=dev)
        self.s_hidden = f(2304); self.s_norm = f(2304); self.s_proj = f(16384)
        self.s_kva = f(576); self.s_conv = f(12288); self.s_o = f(4096)
        self.s_beta = f(32); self.s_qrope = f(2048); self.s_qabs = f(16384)
        self.s_ctx = f(16384); self.s_wkb = f(512 * 8192); self.s_h = f(9 * 1024)
        self.s_router = f(64); self.s_topw = f(8)
        self.s_topidx = torch.empty(8, dtype=torch.int32, device=dev)
        self.bar = torch.zeros(64, dtype=torch.int32, device=dev)
        self._prepared = True

    @torch.no_grad()
    def step(self, hidden, state):
        if not self._prepared:
            self._prepare()
        dev = hidden.device
        hin = hidden.contiguous()
        out = torch.empty(2304, dtype=torch.bfloat16, device=dev)

        S0, S1, S2 = state[0]["S"], state[1]["S"], state[2]["S"]
        cq0, ck0, cv0 = state[0]["cq"], state[0]["ck"], state[0]["cv"]
        cq1, ck1, cv1 = state[1]["cq"], state[1]["ck"], state[1]["cv"]
        cq2, ck2, cv2 = state[2]["cq"], state[2]["ck"], state[2]["cv"]

        ckv_old = state[3]["c_kv"]; krope_old = state[3]["k_rope"]
        pos = ckv_old.shape[0]
        ckv_new = torch.empty(pos + 1, 512, dtype=torch.bfloat16, device=dev)
        krope_new = torch.empty(pos + 1, 64, dtype=torch.bfloat16, device=dev)

        mega[(NPROG,)](
            hin, out, self.s_hidden, self.s_norm, self.s_proj, self.s_kva,
            self.s_conv, self.s_o, self.s_beta, self.s_qrope, self.s_qabs,
            self.s_ctx, self.s_wkb, self.s_h, self.s_router, self.s_topw,
            self.s_topidx, self.bar,
            self.kq_wq, self.kq_sc, self.kq_zr, self.kk_wq, self.kk_sc, self.kk_zr,
            self.kv_wq, self.kv_sc, self.kv_zr, self.kg_wq, self.kg_sc, self.kg_zr,
            self.ko_wq, self.ko_sc, self.ko_zr, self.kbeta, self.kconv,
            S0, S1, S2, cq0, ck0, cv0, cq1, ck1, cv1, cq2, ck2, cv2,
            self.mq_wq, self.mq_sc, self.mq_zr, self.ma_wq, self.ma_sc, self.ma_zr,
            self.mb_wq, self.mb_sc, self.mb_zr, self.mo_wq, self.mo_sc, self.mo_zr,
            ckv_old, krope_old, ckv_new, krope_new, pos,
            self.anorm, self.mnorm,
            self.g_wq, self.g_sc, self.g_zr, self.u_wq, self.u_sc, self.u_zr,
            self.d_wq, self.d_sc, self.d_zr, self.sg_wq, self.sg_sc, self.sg_zr,
            self.su_wq, self.su_sc, self.su_zr, self.sd_wq, self.sd_sc, self.sd_zr,
            self.router, self._step,
            NPROG, num_warps=4,
        )
        self._step += 1
        state[3]["c_kv"] = ckv_new
        state[3]["k_rope"] = krope_new
        return out, state
