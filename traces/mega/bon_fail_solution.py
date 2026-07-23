"""Fused single-launch W4A16 Kimi-Linear hybrid decode megakernel.

The entire per-token forward -- 3 KDA (gated-delta linear attention) blocks + 1
MLA (multi-head latent attention) block, each with a 64-expert MoE FFN, both
RMSNorms, residuals, the short causal conv, the KDA recurrent-state update, the
MLA latent-cache attention, the MoE router + expert GEMVs, and every int4
dequant-GEMV (fused, weights streamed once) -- runs in ONE persistent
cooperative Triton grid launch invoked exactly once per step().

Inter-phase ordering across the persistent grid uses a monotonic
arrival/release counter barrier (no host-side reset, so no extra launches).
"""
from __future__ import annotations

import torch
import torch.nn as nn
import triton
import triton.language as tl

EPS = 1.0e-6
GROUP_SIZE = 128


# --------------------------------------------------------------------------- #
# module skeleton (buffer/param names identical to reference)
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
# device helpers
# --------------------------------------------------------------------------- #
@triton.jit
def _bar(ARR, REL, GRID: tl.constexpr):
    my = tl.atomic_add(ARR, 1) + 1
    if my % GRID == 0:
        tl.atomic_add(REL, 1)
    ph = (my - 1) // GRID + 1
    done = tl.atomic_add(REL, 0)
    while done < ph:
        done = tl.atomic_add(REL, 0)


@triton.jit
def _gv(SCR, xoff, WQ, SC, ZR, wqoff, grpoff, K, N, yoff, pid,
        GRID: tl.constexpr, BK: tl.constexpr, BN: tl.constexpr, ADD: tl.constexpr):
    KH = K // 2
    n0 = pid * BN
    while n0 < N:
        ns = n0 + tl.arange(0, BN)
        mn = ns < N
        acc = tl.zeros([BN], tl.float32)
        kh0 = 0
        while kh0 < KH:
            kh = kh0 + tl.arange(0, BK)
            mk = kh < KH
            base = kh[:, None] * N + ns[None, :]
            m2 = mk[:, None] & mn[None, :]
            byte = tl.load(WQ + wqoff + base, mask=m2, other=0).to(tl.uint8)
            g = kh // 64
            gb = g[:, None] * N + ns[None, :]
            s = tl.load(SC + grpoff + gb, mask=m2, other=0).to(tl.float32)
            z = tl.load(ZR + grpoff + gb, mask=m2, other=0).to(tl.float32)
            lo = (byte & 0xF).to(tl.float32)
            hi = ((byte >> 4) & 0xF).to(tl.float32)
            xlo = tl.load(SCR + xoff + 2 * kh, mask=mk, other=0.0)
            xhi = tl.load(SCR + xoff + 2 * kh + 1, mask=mk, other=0.0)
            acc += tl.sum((lo - z) * s * xlo[:, None] + (hi - z) * s * xhi[:, None], axis=0)
            kh0 += BK
        if ADD:
            prev = tl.load(SCR + yoff + ns, mask=mn, other=0.0)
            tl.store(SCR + yoff + ns, prev + acc, mask=mn)
        else:
            tl.store(SCR + yoff + ns, acc, mask=mn)
        n0 += GRID * BN


# --------------------------------------------------------------------------- #
# the megakernel
# --------------------------------------------------------------------------- #
@triton.jit
def mega(
    HIN, OUT, SCR, TOPI, ARR, REL,
    PWQ, PSC, PZR, OFF,
    GWQ, GSC, GZR, UWQ, USC, UZR, DWQ, DSC, DZR,
    SGWQ, SGSC, SGZR, SUWQ, SUSC, SUZR, SDWQ, SDSC, SDZR,
    NORM, CONVW, BETAW, ROUTERW,
    S0, S1, S2, CQ0, CK0, CV0, CQ1, CK1, CV1, CQ2, CK2, CV2,
    CKV_IN, KR_IN, CKV_OUT, KR_OUT, L,
    GRID: tl.constexpr,
    D: tl.constexpr, CD: tl.constexpr, H: tl.constexpr, DK: tl.constexpr,
    E: tl.constexpr, NACT: tl.constexpr, MINTER: tl.constexpr,
    NOPE: tl.constexpr, ROPE: tl.constexpr, VH: tl.constexpr, KL: tl.constexpr,
    QDIM: tl.constexpr, KVA: tl.constexpr, KVBN: tl.constexpr, DBG: tl.constexpr,
    KDA_SCALE: tl.constexpr, MLA_SCALE: tl.constexpr, ROUT_SCALE: tl.constexpr,
    ROPE_THETA: tl.constexpr,
    # scratch offsets
    XN: tl.constexpr, QO: tl.constexpr, KO: tl.constexpr, VO: tl.constexpr, GO: tl.constexpr,
    QC: tl.constexpr, KC: tl.constexpr, VC: tl.constexpr, BETA: tl.constexpr,
    OO: tl.constexpr, ATT: tl.constexpr, HN: tl.constexpr, ROUTER: tl.constexpr,
    TOPW: tl.constexpr, GATET: tl.constexpr, UPT: tl.constexpr, HH: tl.constexpr, MOUT: tl.constexpr,
    MQ: tl.constexpr, MKVA: tl.constexpr, QP: tl.constexpr, QROPE: tl.constexpr,
    CTX: tl.constexpr, MO: tl.constexpr,
    BK: tl.constexpr, BN: tl.constexpr,
):
    pid = tl.program_id(0)
    Lp = L + 1

    # init running hidden X (fp32) := HIN (bf16)  -> stored at XN? no, need separate.
    # We keep the running hidden in scratch region MOUT-independent: use "OO..."? 
    # Use a dedicated fp32 hidden at offset HN? HN reused. Use XN? XN reused as norm out.
    # Dedicated hidden buffer: reuse ATT? no. We store hidden in OUT-adjacent scratch: use MO region? 
    # Simpler: keep hidden in SCR at fixed offset "HID" == QP? no.
    # We'll keep hidden in-place at scratch offset 'HIDX' passed as... use XN for norm output only.
    # -> keep running hidden at offset stored in variable region: use 'MOUT'? MOUT used by moe.
    # Decision: keep hidden at a stable offset = 'HID' := reuse 'CTX' start? messy.
    # Instead store running hidden in the *OUT would be bf16*. Keep fp32 hidden in SCR[HIDOFF].
    # We add a fixed region via 'MO' after use? To avoid confusion we use 'ROUTER'? small.
    # FINAL: running hidden fp32 lives at offset 'HIDX' = the 'QP' region is big; but reused in MLA.
    # We choose a truly separate region passed implicitly as 'CTX'+ H*512 ... -> use 'HH'? conflict.
    # -> Use offset 'BETA'? too small.
    # Cleanest: dedicate 'XN' for hidden AND norm? They differ. So we need one more region 'HID'.
    # We pass it as 'MO' + H*VH via constexpr HIDX below (added in python). Use HIDX.
    HIDX: tl.constexpr = MO + H * VH
    i = pid
    while i < D:
        tl.store(SCR + HIDX + i, tl.load(HIN + i).to(tl.float32))
        i += GRID
    _bar(ARR, REL, GRID)

    for blk in tl.static_range(4):
        norm_base = blk * 2 * D
        # ---------- attn rmsnorm ----------
        if pid == 0:
            idx = tl.arange(0, 4096)
            m = idx < D
            x = tl.load(SCR + HIDX + idx, mask=m, other=0.0)
            ms = tl.sum(x * x, axis=0) / D
            r = 1.0 / tl.sqrt(ms + 1.0e-6)
            w = tl.load(NORM + norm_base + idx, mask=m, other=0.0)
            tl.store(SCR + XN + idx, x * r * w, mask=m)
        _bar(ARR, REL, GRID)

        if blk < 3:
            # ============================ KDA ============================
            b = blk
            sq = b * 5
            # off table rows: q=sq,k=sq+1,v=sq+2,g=sq+3,o=sq+4
            # q,k,v,g GEMV (K=D, N=CD)
            _gv(SCR, XN, PWQ, PSC, PZR, tl.load(OFF + sq * 4 + 0), tl.load(OFF + sq * 4 + 1),
                D, CD, QO, pid, GRID, BK, BN, False)
            _gv(SCR, XN, PWQ, PSC, PZR, tl.load(OFF + (sq + 1) * 4 + 0), tl.load(OFF + (sq + 1) * 4 + 1),
                D, CD, KO, pid, GRID, BK, BN, False)
            _gv(SCR, XN, PWQ, PSC, PZR, tl.load(OFF + (sq + 2) * 4 + 0), tl.load(OFF + (sq + 2) * 4 + 1),
                D, CD, VO, pid, GRID, BK, BN, False)
            _gv(SCR, XN, PWQ, PSC, PZR, tl.load(OFF + (sq + 3) * 4 + 0), tl.load(OFF + (sq + 3) * 4 + 1),
                D, CD, GO, pid, GRID, BK, BN, False)
            _bar(ARR, REL, GRID)

            # ---------- conv + silu + gproc, beta ----------
            CQb = CQ0 if b == 0 else (CQ1 if b == 1 else CQ2)
            CKb = CK0 if b == 0 else (CK1 if b == 1 else CK2)
            CVb = CV0 if b == 0 else (CV1 if b == 1 else CV2)
            convbase = b * 3 * CD * 4
            c = pid
            while c < CD:
                # q
                cur = tl.load(SCR + QO + c)
                p0 = tl.load(CQb + 0 * CD + c).to(tl.float32)
                p1 = tl.load(CQb + 1 * CD + c).to(tl.float32)
                p2 = tl.load(CQb + 2 * CD + c).to(tl.float32)
                w0 = tl.load(CONVW + convbase + 0 * CD * 4 + c * 4 + 0)
                w1 = tl.load(CONVW + convbase + 0 * CD * 4 + c * 4 + 1)
                w2 = tl.load(CONVW + convbase + 0 * CD * 4 + c * 4 + 2)
                w3 = tl.load(CONVW + convbase + 0 * CD * 4 + c * 4 + 3)
                o = p0 * w0 + p1 * w1 + p2 * w2 + cur * w3
                o = o * (1.0 / (1.0 + tl.exp(-o)))
                tl.store(SCR + QC + c, o * KDA_SCALE)
                tl.store(CQb + 0 * CD + c, p1.to(tl.bfloat16))
                tl.store(CQb + 1 * CD + c, p2.to(tl.bfloat16))
                tl.store(CQb + 2 * CD + c, cur.to(tl.bfloat16))
                # k
                cur = tl.load(SCR + KO + c)
                p0 = tl.load(CKb + 0 * CD + c).to(tl.float32)
                p1 = tl.load(CKb + 1 * CD + c).to(tl.float32)
                p2 = tl.load(CKb + 2 * CD + c).to(tl.float32)
                w0 = tl.load(CONVW + convbase + 1 * CD * 4 + c * 4 + 0)
                w1 = tl.load(CONVW + convbase + 1 * CD * 4 + c * 4 + 1)
                w2 = tl.load(CONVW + convbase + 1 * CD * 4 + c * 4 + 2)
                w3 = tl.load(CONVW + convbase + 1 * CD * 4 + c * 4 + 3)
                o = p0 * w0 + p1 * w1 + p2 * w2 + cur * w3
                o = o * (1.0 / (1.0 + tl.exp(-o)))
                tl.store(SCR + KC + c, o)
                tl.store(CKb + 0 * CD + c, p1.to(tl.bfloat16))
                tl.store(CKb + 1 * CD + c, p2.to(tl.bfloat16))
                tl.store(CKb + 2 * CD + c, cur.to(tl.bfloat16))
                # v
                cur = tl.load(SCR + VO + c)
                p0 = tl.load(CVb + 0 * CD + c).to(tl.float32)
                p1 = tl.load(CVb + 1 * CD + c).to(tl.float32)
                p2 = tl.load(CVb + 2 * CD + c).to(tl.float32)
                w0 = tl.load(CONVW + convbase + 2 * CD * 4 + c * 4 + 0)
                w1 = tl.load(CONVW + convbase + 2 * CD * 4 + c * 4 + 1)
                w2 = tl.load(CONVW + convbase + 2 * CD * 4 + c * 4 + 2)
                w3 = tl.load(CONVW + convbase + 2 * CD * 4 + c * 4 + 3)
                o = p0 * w0 + p1 * w1 + p2 * w2 + cur * w3
                o = o * (1.0 / (1.0 + tl.exp(-o)))
                tl.store(SCR + VC + c, o)
                tl.store(CVb + 0 * CD + c, p1.to(tl.bfloat16))
                tl.store(CVb + 1 * CD + c, p2.to(tl.bfloat16))
                tl.store(CVb + 2 * CD + c, cur.to(tl.bfloat16))
                # gproc = -softplus(graw)
                gr = tl.load(SCR + GO + c)
                sp = tl.maximum(gr, 0.0) + tl.log(1.0 + tl.exp(-tl.abs(gr)))
                tl.store(SCR + GO + c, -sp)
                c += GRID
            if pid == 0:
                betab = b * H * D
                dd = tl.arange(0, 4096)
                mdd = dd < D
                xnv = tl.load(SCR + XN + dd, mask=mdd, other=0.0)
                for hh_ in range(H):
                    wv = tl.load(BETAW + betab + hh_ * D + dd, mask=mdd, other=0.0)
                    bacc = tl.sum(xnv * wv, axis=0)
                    tl.store(SCR + BETA + hh_, 1.0 / (1.0 + tl.exp(-bacc)))
            _bar(ARR, REL, GRID)

            # ---------- recurrence over (head, j) ----------
            Sb = S0 if b == 0 else (S1 if b == 1 else S2)
            it = pid
            ii = tl.arange(0, DK)
            while it < H * DK:
                h = it // DK
                j = it % DK
                sbase = h * DK * DK + j
                svec = tl.load(Sb + sbase + ii * DK)
                gvec = tl.load(SCR + GO + h * DK + ii)
                kvec = tl.load(SCR + KC + h * DK + ii)
                qvec = tl.load(SCR + QC + h * DK + ii)
                vj = tl.load(SCR + VC + h * DK + j)
                betah = tl.load(SCR + BETA + h)
                sdec = svec * tl.exp(gvec)
                pred = tl.sum(sdec * kvec, axis=0)
                snew = sdec + betah * kvec * (vj - pred)
                oj = tl.sum(snew * qvec, axis=0)
                tl.store(SCR + OO + h * DK + j, oj)
                tl.store(Sb + sbase + ii * DK, snew)
                it += GRID
            _bar(ARR, REL, GRID)

            # ---------- o_proj: ATT = OO @ Wo  (K=CD, N=D) ----------
            _gv(SCR, OO, PWQ, PSC, PZR, tl.load(OFF + (sq + 4) * 4 + 0), tl.load(OFF + (sq + 4) * 4 + 1),
                CD, D, ATT, pid, GRID, BK, BN, False)
            _bar(ARR, REL, GRID)
        else:
            # ============================ MLA ============================
            sq = 15  # q=15,kva=16,kvb=17,o=18
            # q GEMV (K=D,N=QDIM), kv_a GEMV (K=D,N=KVA)
            _gv(SCR, XN, PWQ, PSC, PZR, tl.load(OFF + sq * 4 + 0), tl.load(OFF + sq * 4 + 1),
                D, QDIM, MQ, pid, GRID, BK, BN, False)
            _gv(SCR, XN, PWQ, PSC, PZR, tl.load(OFF + (sq + 1) * 4 + 0), tl.load(OFF + (sq + 1) * 4 + 1),
                D, KVA, MKVA, pid, GRID, BK, BN, False)
            _bar(ARR, REL, GRID)

            # ---------- cache copy old->new; new token row; rope; qp sideways ----------
            # copy CKV_IN[L,KL] -> CKV_OUT[:L], KR_IN[L,ROPE]->KR_OUT[:L]
            tot = L * KL
            e = pid
            while e < tot:
                tl.store(CKV_OUT + e, tl.load(CKV_IN + e))
                e += GRID
            tot2 = L * ROPE
            e = pid
            while e < tot2:
                tl.store(KR_OUT + e, tl.load(KR_IN + e))
                e += GRID
            if pid == 0:
                # new c_kv row = MKVA[:KL]
                for d_ in range(KL):
                    tl.store(CKV_OUT + L * KL + d_, tl.load(SCR + MKVA + d_).to(tl.bfloat16))
                # rope for q_rope (per head) and k_rope (row L)
                for r in range(ROPE // 2):
                    freq = tl.exp(-(2.0 * r / ROPE) * tl.log(ROPE_THETA))
                    ang = L * freq
                    cs = tl.cos(ang)
                    sn = tl.sin(ang)
                    # k_rope
                    ke = tl.load(SCR + MKVA + KL + 2 * r)
                    ko_ = tl.load(SCR + MKVA + KL + 2 * r + 1)
                    tl.store(KR_OUT + L * ROPE + 2 * r, (ke * cs - ko_ * sn).to(tl.bfloat16))
                    tl.store(KR_OUT + L * ROPE + 2 * r + 1, (ko_ * cs + ke * sn).to(tl.bfloat16))
                    # q_rope per head
                    for h in range(H):
                        qe = tl.load(SCR + MQ + h * (NOPE + ROPE) + NOPE + 2 * r)
                        qo_ = tl.load(SCR + MQ + h * (NOPE + ROPE) + NOPE + 2 * r + 1)
                        tl.store(SCR + QROPE + h * ROPE + 2 * r, qe * cs - qo_ * sn)
                        tl.store(SCR + QROPE + h * ROPE + 2 * r + 1, qo_ * cs + qe * sn)
            # qp sideways GEMV: qp[h,d] = sum_o qnope[h,o]*Wkvb(d, h*256+o)
            wqoff = tl.load(OFF + 17 * 4 + 0)
            grpoff = tl.load(OFF + 17 * 4 + 1)
            oo = tl.arange(0, NOPE)
            p = pid
            while p < H * KL:
                h = p // KL
                d = p % KL
                colb = h * (NOPE + VH)
                byte = tl.load(PWQ + wqoff + (d // 2) * KVBN + colb + oo).to(tl.uint8)
                gidx = d // 128
                s = tl.load(PSC + grpoff + gidx * KVBN + colb + oo).to(tl.float32)
                z = tl.load(PZR + grpoff + gidx * KVBN + colb + oo).to(tl.float32)
                nib = tl.where((d % 2) == 0, (byte & 0xF).to(tl.float32), ((byte >> 4) & 0xF).to(tl.float32))
                w = (nib - z) * s
                qn = tl.load(SCR + MQ + h * (NOPE + ROPE) + oo)
                tl.store(SCR + QP + p, tl.sum(qn * w, axis=0))
                p += GRID
            _bar(ARR, REL, GRID)

            # ---------- flash attention head-parallel -> CTX[h,512] ----------
            if pid < H:
                h = pid
                dcol = tl.arange(0, KL)
                rcol = tl.arange(0, ROPE)
                qpv = tl.load(SCR + QP + h * KL + dcol)
                qrv = tl.load(SCR + QROPE + h * ROPE + rcol)
                m = -1.0e30
                den = 0.0
                acc = tl.zeros([KL], tl.float32)
                l0 = 0
                BL: tl.constexpr = 32
                while l0 < Lp:
                    ls = l0 + tl.arange(0, BL)
                    ml = ls < Lp
                    ckv = tl.load(CKV_OUT + ls[:, None] * KL + dcol[None, :],
                                  mask=ml[:, None], other=0.0).to(tl.float32)
                    kr = tl.load(KR_OUT + ls[:, None] * ROPE + rcol[None, :],
                                 mask=ml[:, None], other=0.0).to(tl.float32)
                    sc = tl.sum(ckv * qpv[None, :], axis=1) + tl.sum(kr * qrv[None, :], axis=1)
                    sc = sc * MLA_SCALE
                    sc = tl.where(ml, sc, -1.0e30)
                    blkmax = tl.max(sc, axis=0)
                    newm = tl.maximum(m, blkmax)
                    alpha = tl.exp(m - newm)
                    p_ = tl.exp(sc - newm)
                    den = den * alpha + tl.sum(p_, axis=0)
                    acc = acc * alpha + tl.sum(p_[:, None] * ckv, axis=0)
                    m = newm
                    l0 += BL
                ctx = acc / den
                tl.store(SCR + CTX + h * KL + dcol, ctx)
            _bar(ARR, REL, GRID)

            # ---------- o via Wvb: MO[h,j] = sum_d ctx[h,d]*Wkvb(d,h*256+128+j) ----------
            wqoff = tl.load(OFF + 17 * 4 + 0)
            grpoff = tl.load(OFF + 17 * 4 + 1)
            khr = tl.arange(0, KL // 2)
            p = pid
            while p < H * VH:
                h = p // VH
                j = p % VH
                col = h * (NOPE + VH) + NOPE + j
                byte = tl.load(PWQ + wqoff + khr * KVBN + col).to(tl.uint8)
                s = tl.load(PSC + grpoff + (khr // 64) * KVBN + col).to(tl.float32)
                z = tl.load(PZR + grpoff + (khr // 64) * KVBN + col).to(tl.float32)
                lo = (byte & 0xF).to(tl.float32)
                hi = ((byte >> 4) & 0xF).to(tl.float32)
                xlo = tl.load(SCR + CTX + h * KL + 2 * khr)
                xhi = tl.load(SCR + CTX + h * KL + 2 * khr + 1)
                acc = tl.sum((lo - z) * s * xlo + (hi - z) * s * xhi, axis=0)
                tl.store(SCR + MO + p, acc)
                p += GRID
            _bar(ARR, REL, GRID)

            # ---------- o_proj: ATT = MO @ Wo (K=CD, N=D) ----------
            _gv(SCR, MO, PWQ, PSC, PZR, tl.load(OFF + 18 * 4 + 0), tl.load(OFF + 18 * 4 + 1),
                CD, D, ATT, pid, GRID, BK, BN, False)
            _bar(ARR, REL, GRID)

        # ---------- residual + moe rmsnorm ----------
        if pid == 0:
            idx = tl.arange(0, 4096)
            m = idx < D
            x = tl.load(SCR + HIDX + idx, mask=m, other=0.0) + tl.load(SCR + ATT + idx, mask=m, other=0.0)
            tl.store(SCR + HIDX + idx, x, mask=m)
            ms = tl.sum(x * x, axis=0) / D
            r = 1.0 / tl.sqrt(ms + 1.0e-6)
            w = tl.load(NORM + norm_base + D + idx, mask=m, other=0.0)
            tl.store(SCR + HN + idx, x * r * w, mask=m)
        _bar(ARR, REL, GRID)

        # ============================ MoE ============================
        if pid == 0:
            dd = tl.arange(0, 4096)
            mdd = dd < D
            hnv = tl.load(SCR + HN + dd, mask=mdd, other=0.0)
            for ee in range(E):
                wv = tl.load(ROUTERW + blk * E * D + ee * D + dd, mask=mdd, other=0.0)
                tl.store(SCR + ROUTER + ee, tl.sum(hnv * wv, axis=0))
            # top-NACT of logits
            eidx = tl.arange(0, 64)
            logv = tl.load(SCR + ROUTER + eidx)
            lmax = 0.0
            ssum = 0.0
            for j in range(NACT):
                mx = tl.max(logv, axis=0)
                eqm = logv == mx
                ind = tl.min(tl.where(eqm, eidx, 64), axis=0)
                if j == 0:
                    lmax = mx
                tl.store(TOPI + j, ind)
                tl.store(SCR + TOPW + j, mx)
                logv = tl.where(eidx == ind, -1.0e30, logv)
            for j in range(NACT):
                ssum += tl.exp(tl.load(SCR + TOPW + j) - lmax)
            for j in range(NACT):
                wj = tl.exp(tl.load(SCR + TOPW + j) - lmax) / ssum * ROUT_SCALE
                tl.store(SCR + TOPW + j, wj)
            # zero MOUT
            tl.store(SCR + MOUT + dd, tl.zeros([4096], tl.float32), mask=mdd)
        _bar(ARR, REL, GRID)

        # routed experts
        for j in range(NACT):
            ex = tl.load(TOPI + j)
            wj = tl.load(SCR + TOPW + j)
            gwo = (blk * E + ex) * (D // 2) * MINTER
            ggo = (blk * E + ex) * (D // 128) * MINTER
            _gv(SCR, HN, GWQ, GSC, GZR, gwo, ggo, D, MINTER, GATET, pid, GRID, BK, BN, False)
            _gv(SCR, HN, UWQ, USC, UZR, gwo, ggo, D, MINTER, UPT, pid, GRID, BK, BN, False)
            n = pid
            while n < MINTER:
                gt = tl.load(SCR + GATET + n)
                ut = tl.load(SCR + UPT + n)
                tl.store(SCR + HH + n, wj * gt * (1.0 / (1.0 + tl.exp(-gt))) * ut)
                n += GRID
            _bar(ARR, REL, GRID)
            dwo = (blk * E + ex) * (MINTER // 2) * D
            dgo = (blk * E + ex) * (MINTER // 128) * D
            _gv(SCR, HH, DWQ, DSC, DZR, dwo, dgo, MINTER, D, MOUT, pid, GRID, BK, BN, True)
            _bar(ARR, REL, GRID)

        # shared expert (weight 1)
        swo = blk * (D // 2) * MINTER
        sgo = blk * (D // 128) * MINTER
        _gv(SCR, HN, SGWQ, SGSC, SGZR, swo, sgo, D, MINTER, GATET, pid, GRID, BK, BN, False)
        _gv(SCR, HN, SUWQ, SUSC, SUZR, swo, sgo, D, MINTER, UPT, pid, GRID, BK, BN, False)
        n = pid
        while n < MINTER:
            gt = tl.load(SCR + GATET + n)
            ut = tl.load(SCR + UPT + n)
            tl.store(SCR + HH + n, gt * (1.0 / (1.0 + tl.exp(-gt))) * ut)
            n += GRID
        _bar(ARR, REL, GRID)
        sdwo = blk * (MINTER // 2) * D
        sdgo = blk * (MINTER // 128) * D
        _gv(SCR, HH, SDWQ, SDSC, SDZR, sdwo, sdgo, MINTER, D, MOUT, pid, GRID, BK, BN, True)
        _bar(ARR, REL, GRID)

        # residual: hidden += MOUT
        i = pid
        while i < D:
            tl.store(SCR + HIDX + i, tl.load(SCR + HIDX + i) + tl.load(SCR + MOUT + i))
            i += GRID
        _bar(ARR, REL, GRID)
        if DBG >= 0:
            if blk == DBG:
                ii = pid
                while ii < D:
                    tl.store(OUT + ii, tl.load(SCR + ATT + ii).to(tl.bfloat16))
                    ii += GRID

    # write output
    i = pid
    while i < D:
        tl.store(OUT + i, tl.load(SCR + HIDX + i).to(tl.bfloat16))
        i += GRID


# --------------------------------------------------------------------------- #
# Model
# --------------------------------------------------------------------------- #
class Model(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.blocks = nn.ModuleList(Block(cfg, k) for k in cfg.pattern)
        self._prepared = False

    def _prepare(self):
        cfg = self.cfg
        dev = torch.device("cuda:0")
        D = cfg.hidden
        CD = cfg.kda_heads * cfg.kda_head_dim
        E = cfg.n_experts
        MINTER = cfg.moe_inter
        QDIM = cfg.mla_heads * (cfg.qk_nope + cfg.qk_rope)
        KVA = cfg.kv_lora + cfg.qk_rope
        KVBN = cfg.mla_heads * (cfg.qk_nope + cfg.v_head)

        # --- projection weights flat + offset table ---
        proj_list = []
        for b in range(3):
            blk = self.blocks[b]
            for name in ("q_proj", "k_proj", "v_proj", "g_proj", "o_proj"):
                proj_list.append(getattr(blk.attn, name))
        mla = self.blocks[3].attn
        for name in ("q_proj", "kv_a", "kv_b", "o_proj"):
            proj_list.append(getattr(mla, name))

        wq_parts, sc_parts, zr_parts = [], [], []
        off = torch.zeros(len(proj_list), 4, dtype=torch.int32)
        wqc = scc = 0
        for i, ql in enumerate(proj_list):
            wq = ql.w_q.to(dev).contiguous().view(-1)
            sc = ql.scales.to(dev).contiguous().view(-1)
            zr = ql.zeros.to(dev).contiguous().view(-1)
            off[i, 0] = wqc
            off[i, 1] = scc
            off[i, 2] = ql.in_f
            off[i, 3] = ql.out_f
            wq_parts.append(wq)
            sc_parts.append(sc)
            zr_parts.append(zr)
            wqc += wq.numel()
            scc += sc.numel()
        self.PWQ = torch.cat(wq_parts)
        self.PSC = torch.cat(sc_parts)
        self.PZR = torch.cat(zr_parts)
        self.OFF = off.to(dev)

        # --- experts: stack over blocks [4,E,...] ---
        def stack(attr):
            wqs, scs, zrs = [], [], []
            for b in range(4):
                qe = getattr(self.blocks[b].moe, attr)
                wqs.append(qe.w_q.to(dev).contiguous())
                scs.append(qe.scales.to(dev).contiguous())
                zrs.append(qe.zeros.to(dev).contiguous())
            return (torch.stack(wqs).contiguous().view(-1),
                    torch.stack(scs).contiguous().view(-1),
                    torch.stack(zrs).contiguous().view(-1))

        self.GWQ, self.GSC, self.GZR = stack("gate")
        self.UWQ, self.USC, self.UZR = stack("up")
        self.DWQ, self.DSC, self.DZR = stack("down")
        self.SGWQ, self.SGSC, self.SGZR = stack("s_gate")
        self.SUWQ, self.SUSC, self.SUZR = stack("s_up")
        self.SDWQ, self.SDSC, self.SDZR = stack("s_down")

        # --- dense fp32 ---
        norms = []
        for b in range(4):
            norms.append(self.blocks[b].attn_norm.data.float())
            norms.append(self.blocks[b].moe_norm.data.float())
        self.NORM = torch.cat(norms).to(dev).contiguous()
        convs = []
        for b in range(3):
            convs.append(self.blocks[b].attn.conv_w.data.float().contiguous().view(-1))
        self.CONVW = torch.cat(convs).to(dev).contiguous()
        betas = []
        for b in range(3):
            betas.append(self.blocks[b].attn.beta_proj.weight.data.float().contiguous().view(-1))
        self.BETAW = torch.cat(betas).to(dev).contiguous()
        routers = []
        for b in range(4):
            routers.append(self.blocks[b].moe.router.weight.data.float().contiguous().view(-1))
        self.ROUTERW = torch.cat(routers).to(dev).contiguous()

        # --- scratch layout ---
        H = cfg.mla_heads
        VH = cfg.v_head
        KL = cfg.kv_lora
        o = 0
        def alloc(n):
            nonlocal o
            s = o
            o += n
            return s
        self.XN = alloc(D)
        self.QO = alloc(CD); self.KO = alloc(CD); self.VO = alloc(CD); self.GO = alloc(CD)
        self.QC = alloc(CD); self.KC = alloc(CD); self.VC = alloc(CD)
        self.BETA = alloc(H)
        self.OO = alloc(CD)
        self.ATT = alloc(D)
        self.HN = alloc(D)
        self.ROUTER = alloc(E)
        self.TOPW = alloc(cfg.n_active)
        self.GATET = alloc(MINTER); self.UPT = alloc(MINTER); self.HH = alloc(MINTER)
        self.MOUT = alloc(D)
        self.MQ = alloc(QDIM); self.MKVA = alloc(KVA)
        self.QP = alloc(H * KL); self.QROPE = alloc(H * cfg.qk_rope)
        self.CTX = alloc(H * KL); self.MO = alloc(H * VH)
        # HIDX = MO + H*VH  (running hidden, D)
        self.SCRN = o + D
        self.SCR = torch.zeros(self.SCRN, dtype=torch.float32, device=dev)
        self.TOPI = torch.zeros(cfg.n_active, dtype=torch.int32, device=dev)
        self.ARR = torch.zeros(1, dtype=torch.int32, device=dev)
        self.REL = torch.zeros(1, dtype=torch.int32, device=dev)
        self.OUTBUF = torch.zeros(D, dtype=torch.bfloat16, device=dev)

        self.GRID = torch.cuda.get_device_properties(dev).multi_processor_count
        self.consts = dict(
            D=D, CD=CD, H=H, DK=cfg.kda_head_dim, E=E, NACT=cfg.n_active, MINTER=MINTER,
            NOPE=cfg.qk_nope, ROPE=cfg.qk_rope, VH=VH, KL=KL,
            QDIM=QDIM, KVA=KVA, KVBN=KVBN,
            KDA_SCALE=cfg.kda_head_dim ** -0.5,
            MLA_SCALE=(cfg.qk_nope + cfg.qk_rope) ** -0.5,
            ROUT_SCALE=cfg.routed_scaling, ROPE_THETA=float(cfg.rope_theta),
        )
        self._prepared = True

    def step(self, hidden, state):
        if not self._prepared:
            self._prepare()
        cfg = self.cfg
        # KDA states
        S = [state[i]["S"] for i in range(3)]
        CQ = [state[i]["cq"] for i in range(3)]
        CK = [state[i]["ck"] for i in range(3)]
        CV = [state[i]["cv"] for i in range(3)]
        mla_st = state[3]
        ckv_in = mla_st["c_kv"]
        kr_in = mla_st["k_rope"]
        L = ckv_in.shape[0]
        ckv_out = torch.empty(L + 1, cfg.kv_lora, dtype=torch.bfloat16, device=hidden.device)
        kr_out = torch.empty(L + 1, cfg.qk_rope, dtype=torch.bfloat16, device=hidden.device)

        c = self.consts
        mega[(self.GRID,)](
            hidden.contiguous(), self.OUTBUF, self.SCR, self.TOPI, self.ARR, self.REL,
            self.PWQ, self.PSC, self.PZR, self.OFF,
            self.GWQ, self.GSC, self.GZR, self.UWQ, self.USC, self.UZR, self.DWQ, self.DSC, self.DZR,
            self.SGWQ, self.SGSC, self.SGZR, self.SUWQ, self.SUSC, self.SUZR, self.SDWQ, self.SDSC, self.SDZR,
            self.NORM, self.CONVW, self.BETAW, self.ROUTERW,
            S[0], S[1], S[2], CQ[0], CK[0], CV[0], CQ[1], CK[1], CV[1], CQ[2], CK[2], CV[2],
            ckv_in, kr_in, ckv_out, kr_out, L,
            GRID=self.GRID,
            D=c["D"], CD=c["CD"], H=c["H"], DK=c["DK"], E=c["E"], NACT=c["NACT"], MINTER=c["MINTER"],
            NOPE=c["NOPE"], ROPE=c["ROPE"], VH=c["VH"], KL=c["KL"],
            QDIM=c["QDIM"], KVA=c["KVA"], KVBN=c["KVBN"],
            KDA_SCALE=c["KDA_SCALE"], MLA_SCALE=c["MLA_SCALE"], ROUT_SCALE=c["ROUT_SCALE"],
            ROPE_THETA=c["ROPE_THETA"],
            XN=self.XN, QO=self.QO, KO=self.KO, VO=self.VO, GO=self.GO,
            QC=self.QC, KC=self.KC, VC=self.VC, BETA=self.BETA,
            OO=self.OO, ATT=self.ATT, HN=self.HN, ROUTER=self.ROUTER,
            TOPW=self.TOPW, GATET=self.GATET, UPT=self.UPT, HH=self.HH, MOUT=self.MOUT,
            MQ=self.MQ, MKVA=self.MKVA, QP=self.QP, QROPE=self.QROPE, CTX=self.CTX, MO=self.MO,
            BK=256, BN=128, DBG=int(getattr(self, '_dbg', -1)), num_warps=4,
        )
        mla_st["c_kv"] = ckv_out
        mla_st["k_rope"] = kr_out
        return self.OUTBUF, state
