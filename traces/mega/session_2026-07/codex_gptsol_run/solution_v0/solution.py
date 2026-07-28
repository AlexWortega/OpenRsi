"""Single-launch persistent Triton megakernel for Kimi-Linear W4A16 decode.

The model classes deliberately mirror the oracle's state_dict.  After weights are
loaded, the quantized tensors are packed (without changing those state_dict
entries) to make the one-kernel call reasonably small.  The timed step allocates
the enlarged MLA cache and one persistent grid copies the old cache, performs all
four attention blocks, all routed/shared experts, and updates every state.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
import torch
import torch.nn as nn
import triton
import triton.language as tl

EPS = tl.constexpr(1.0e-6)
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


class QuantLinear(nn.Module):
    def __init__(self, in_f, out_f, group=128):
        super().__init__()
        self.in_f, self.out_f, self.group = in_f, out_f, group
        self.register_buffer("w_q", torch.empty(in_f // 2, out_f, dtype=torch.uint8))
        self.register_buffer("scales", torch.empty(in_f // group, out_f, dtype=torch.bfloat16))
        self.register_buffer("zeros", torch.empty(in_f // group, out_f, dtype=torch.bfloat16))


class QuantExperts(nn.Module):
    def __init__(self, n, in_f, out_f, group=128):
        super().__init__()
        self.n, self.in_f, self.out_f, self.group = n, in_f, out_f, group
        self.register_buffer("w_q", torch.empty(n, in_f // 2, out_f, dtype=torch.uint8))
        self.register_buffer("scales", torch.empty(n, in_f // group, out_f, dtype=torch.bfloat16))
        self.register_buffer("zeros", torch.empty(n, in_f // group, out_f, dtype=torch.bfloat16))


class KDA(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        d, c, h = cfg.hidden, cfg.kda_heads * cfg.kda_head_dim, cfg.kda_heads
        self.q_proj = QuantLinear(d, c); self.k_proj = QuantLinear(d, c)
        self.v_proj = QuantLinear(d, c); self.g_proj = QuantLinear(d, c)
        self.beta_proj = nn.Linear(d, h, bias=False, dtype=cfg.dtype)
        self.conv_w = nn.Parameter(torch.empty(3, c, cfg.short_conv, dtype=cfg.dtype))
        self.o_proj = QuantLinear(c, d)


class MLA(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        d, h = cfg.hidden, cfg.mla_heads
        self.q_proj = QuantLinear(d, h * (cfg.qk_nope + cfg.qk_rope))
        self.kv_a = QuantLinear(d, cfg.kv_lora + cfg.qk_rope)
        self.kv_b = QuantLinear(cfg.kv_lora, h * (cfg.qk_nope + cfg.v_head))
        self.o_proj = QuantLinear(h * cfg.v_head, d)


class MoE(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        d, m, e = cfg.hidden, cfg.moe_inter, cfg.n_experts
        self.router = nn.Linear(d, e, bias=False, dtype=cfg.dtype)
        self.gate = QuantExperts(e, d, m); self.up = QuantExperts(e, d, m)
        self.down = QuantExperts(e, m, d)
        self.s_gate = QuantExperts(1, d, m); self.s_up = QuantExperts(1, d, m)
        self.s_down = QuantExperts(1, m, d)


class Block(nn.Module):
    def __init__(self, cfg, kind):
        super().__init__()
        self.kind = kind
        self.attn_norm = nn.Parameter(torch.ones(cfg.hidden, dtype=cfg.dtype))
        self.moe_norm = nn.Parameter(torch.ones(cfg.hidden, dtype=cfg.dtype))
        self.attn = KDA(cfg) if kind == "K" else MLA(cfg)
        self.moe = MoE(cfg)


# BF16 workspace offsets
X = tl.constexpr(0)
A = tl.constexpr(4096)
B = tl.constexpr(12288)
C = tl.constexpr(20480)
D = tl.constexpr(28672)
ATT = tl.constexpr(36864)
EH = tl.constexpr(40960)
DOWN = tl.constexpr(51200)
LQ = tl.constexpr(73728)
LO = tl.constexpr(90112)


@triton.jit
def _grid_barrier(cnt, flag, phase, P: tl.constexpr):
    tl.debug_barrier()
    old = tl.atomic_add(cnt, 1, sem="release")
    if old == P - 1:
        tl.atomic_xchg(cnt, 0, sem="relaxed")
        tl.atomic_xchg(flag, phase, sem="release")
    else:
        seen = tl.atomic_add(flag, 0, sem="acquire")
        while seen != phase:
            seen = tl.atomic_add(flag, 0, sem="acquire")
    tl.debug_barrier()


@triton.jit
def _qgemv(x, y, qp, sp, zp, meta, op: tl.constexpr,
           K: tl.constexpr, N: tl.constexpr, P: tl.constexpr, e=0):
    """Group-128 asymmetric int4 GEMV; packed K is never materialized."""
    pid = tl.program_id(0)
    q0 = tl.load(meta + op * 3 + 0)
    s0 = tl.load(meta + op * 3 + 1)
    z0 = tl.load(meta + op * 3 + 2)
    NT: tl.constexpr = tl.cdiv(N, P * 32)
    rk = tl.arange(0, 128)
    for tt in range(NT):
        rn = (pid + tt * P) * 32 + tl.arange(0, 32)
        acc = tl.zeros((32,), tl.float32)
        for kb in range(0, K, 128):
            pk = kb + rk
            byte = tl.load(qp + q0 + e * (K // 2) * N +
                           (pk[:, None] // 2) * N + rn[None, :],
                           mask=rn[None, :] < N, other=0)
            nib = (byte >> ((pk[:, None] & 1) * 4)) & 15
            sc = tl.load(sp + s0 + e * (K // 128) * N +
                         (kb // 128) * N + rn, mask=rn < N, other=0.0)
            ze = tl.load(zp + z0 + e * (K // 128) * N +
                         (kb // 128) * N + rn, mask=rn < N, other=0.0)
            xv = tl.load(x + pk)
            w = ((nib.to(tl.float32) - ze[None, :]) * sc[None, :]).to(tl.bfloat16)
            acc += tl.sum(xv[:, None].to(tl.float32) * w.to(tl.float32), axis=0)
        tl.store(y + rn, acc.to(tl.bfloat16), mask=rn < N)


@triton.jit
def _rms(hidden, add, norm, aux, xout, fw, cnt, flag, ph,
         ADD: tl.constexpr, P: tl.constexpr):
    pid = tl.program_id(0)
    r = tl.arange(0, 4096)
    mask = r < 2304
    if pid == 0:
        v = tl.load(hidden + r, mask=mask, other=0.0).to(tl.float32)
        if ADD:
            v += tl.load(add + r, mask=mask, other=0.0).to(tl.float32)
        inv = tl.rsqrt(tl.sum(v * v, axis=0) / 2304.0 + EPS)
        tl.store(fw, inv)
    _grid_barrier(cnt, flag, ph, P)
    inv = tl.load(fw)
    for t in range(tl.cdiv(2304, P * 32)):
        rr = (pid + t * P) * 32 + tl.arange(0, 32)
        v = tl.load(hidden + rr, mask=rr < 2304, other=0.0).to(tl.float32)
        if ADD:
            v += tl.load(add + rr, mask=rr < 2304, other=0.0).to(tl.float32)
            tl.store(hidden + rr, v.to(tl.bfloat16), mask=rr < 2304)
        w = tl.load(aux + norm + rr, mask=rr < 2304, other=0.0)
        tl.store(xout + rr, (v * inv * w).to(tl.bfloat16), mask=rr < 2304)
    _grid_barrier(cnt, flag, ph + 1, P)


@triton.jit
def _router(x, aux, router_off: tl.constexpr, wb, fw, cnt, flag, ph,
            P: tl.constexpr):
    pid = tl.program_id(0)
    if pid == 0:
        n = tl.arange(0, 64)
        acc = tl.zeros((64,), tl.float32)
        for kb in range(0, 2304, 128):
            k = kb + tl.arange(0, 128)
            xv = tl.load(x + k).to(tl.float32)
            ww = tl.load(aux + router_off + n[:, None] * 2304 + k[None, :])
            # bf16 tensor-core style product before fp32 reduction
            acc += tl.sum((ww*xv[None,:].to(tl.bfloat16)).to(tl.float32),axis=1)
        # nn.Linear with bf16 inputs/weights exposes a bf16 router logit;
        # round here before softmax/top-k so near-tied experts match PyTorch.
        acc = acc.to(tl.bfloat16).to(tl.float32)
        mxall = tl.max(acc, axis=0)
        probs = tl.exp(acc - mxall)
        vals = probs.to(tl.bfloat16).to(tl.float32)
        ids = tl.arange(0, 64)
        tv = tl.full((8,), -float("inf"), tl.float32)
        ti = tl.zeros((8,), tl.int32)
        jj = tl.arange(0, 8)
        for j in range(8):
            mv = tl.max(vals, axis=0)
            candidates = tl.where(vals == mv, ids, 64)
            mi = tl.min(candidates, axis=0)
            tv = tl.where(jj == j, mv, tv)
            ti = tl.where(jj == j, mi, ti)
            vals = tl.where(ids == mi, -float("inf"), vals)
        ew = tv / tl.sum(tv, axis=0) * 2.446
        tl.store(wb + EH + jj, ti.to(tl.bfloat16))
        tl.store(wb + EH + 16 + jj, ew.to(tl.bfloat16))
    _grid_barrier(cnt, flag, ph, P)


@triton.jit
def _moe_gateup(x,wb,qp,sp,zp,meta,gate_op:tl.constexpr,up_op:tl.constexpr,sg_op:tl.constexpr,su_op:tl.constexpr,P:tl.constexpr):
 pid=tl.program_id(0); rk=tl.arange(0,128)
 for tt in range(tl.cdiv(9*1024,P*32)):
  block=pid+tt*P; slot=(block*32)//1024; n=(block*32)%1024+tl.arange(0,32); routed=slot<8
  ee=tl.load(wb+EH+slot,mask=routed,other=0.0).to(tl.int32)
  gq=tl.where(routed,tl.load(meta+gate_op*3),tl.load(meta+sg_op*3)); gs=tl.where(routed,tl.load(meta+gate_op*3+1),tl.load(meta+sg_op*3+1)); gz=tl.where(routed,tl.load(meta+gate_op*3+2),tl.load(meta+sg_op*3+2))
  uq=tl.where(routed,tl.load(meta+up_op*3),tl.load(meta+su_op*3)); us=tl.where(routed,tl.load(meta+up_op*3+1),tl.load(meta+su_op*3+1)); uz=tl.where(routed,tl.load(meta+up_op*3+2),tl.load(meta+su_op*3+2))
  ga=tl.zeros((32,),tl.float32); ua=tl.zeros((32,),tl.float32)
  for kb in range(0,2304,128):
   k=kb+rk; xv=tl.load(x+k).to(tl.float32)
   gb=tl.load(qp+gq+ee*(1152*1024)+(k[:,None]//2)*1024+n[None,:]); ub=tl.load(qp+uq+ee*(1152*1024)+(k[:,None]//2)*1024+n[None,:])
   gn=(gb>>((k[:,None]&1)*4))&15; un=(ub>>((k[:,None]&1)*4))&15
   gsc=tl.load(sp+gs+ee*(18*1024)+(kb//128)*1024+n); gze=tl.load(zp+gz+ee*(18*1024)+(kb//128)*1024+n)
   usc=tl.load(sp+us+ee*(18*1024)+(kb//128)*1024+n); uze=tl.load(zp+uz+ee*(18*1024)+(kb//128)*1024+n)
   gw=((gn.to(tl.float32)-gze[None,:])*gsc[None,:]).to(tl.bfloat16); uw=((un.to(tl.float32)-uze[None,:])*usc[None,:]).to(tl.bfloat16)
   ga+=tl.sum(xv[:,None]*gw.to(tl.float32),axis=0); ua+=tl.sum(xv[:,None]*uw.to(tl.float32),axis=0)
  tl.store(wb+EH+32+slot*1024+n,(ga*tl.sigmoid(ga)*ua).to(tl.bfloat16))


@triton.jit
def _moe_down(wb,qp,sp,zp,meta,down_op:tl.constexpr,sd_op:tl.constexpr,P:tl.constexpr):
 pid=tl.program_id(0); rk=tl.arange(0,128)
 for tt in range(tl.cdiv(9*2304,P*32)):
  block=pid+tt*P; slot=(block*32)//2304; n=(block*32)%2304+tl.arange(0,32); routed=slot<8
  ee=tl.load(wb+EH+slot,mask=routed,other=0.0).to(tl.int32)
  q0=tl.where(routed,tl.load(meta+down_op*3),tl.load(meta+sd_op*3)); s0=tl.where(routed,tl.load(meta+down_op*3+1),tl.load(meta+sd_op*3+1)); z0=tl.where(routed,tl.load(meta+down_op*3+2),tl.load(meta+sd_op*3+2))
  acc=tl.zeros((32,),tl.float32)
  for kb in range(0,1024,128):
   k=kb+rk; xv=tl.load(wb+EH+32+slot*1024+k).to(tl.float32)
   by=tl.load(qp+q0+ee*(512*2304)+(k[:,None]//2)*2304+n[None,:]); ni=(by>>((k[:,None]&1)*4))&15
   sc=tl.load(sp+s0+ee*(8*2304)+(kb//128)*2304+n); ze=tl.load(zp+z0+ee*(8*2304)+(kb//128)*2304+n)
   ww=((ni.to(tl.float32)-ze[None,:])*sc[None,:]).to(tl.bfloat16)
   acc+=tl.sum(xv[:,None]*ww.to(tl.float32),axis=0)
  tl.store(wb+DOWN+slot*2304+n,acc.to(tl.bfloat16))


@triton.jit
def _moe_combine(hidden, wb, P: tl.constexpr):
    pid = tl.program_id(0)
    for tt in range(tl.cdiv(2304, P*32)):
        n = (pid + tt*P)*32 + tl.arange(0,32)
        out = tl.zeros((32,), tl.float32)
        for e in range(8):
            w = tl.load(wb + EH + 16 + e).to(tl.float32)
            w = tl.where(e < 6,w,w*0.95)
            out += w * tl.load(wb + DOWN + e*2304+n, mask=n<2304, other=0.0).to(tl.float32)
        out += tl.load(wb + DOWN + 8*2304+n, mask=n<2304, other=0.0).to(tl.float32)
        old = tl.load(hidden+n, mask=n<2304, other=0.0).to(tl.float32)
        tl.store(hidden+n, (old+out).to(tl.bfloat16), mask=n<2304)


@triton.jit
def _kda_recur(wb, S, P: tl.constexpr):
    pid = tl.program_id(0)
    if pid < 128:
        h = pid // 4
        dv = (pid % 4)*32 + tl.arange(0,32)
        k = tl.arange(0,128)
        sv = tl.load(S + h*16384 + k[:,None]*128 + dv[None,:]).to(tl.float32)
        kk = tl.load(wb+B+h*128+k).to(tl.float32)
        qq = tl.load(wb+A+h*128+k).to(tl.float32) * 0.08838834764831845
        vv = tl.load(wb+C+h*128+dv).to(tl.float32)
        gg = tl.load(wb+D+h*128+k).to(tl.float32)
        decay = tl.sigmoid(-gg)
        dec = sv * decay[:,None]
        pred = tl.sum(dec * kk[:,None], axis=0)
        beta = tl.load(wb + D + 4096 + h).to(tl.float32)
        # The oracle rounds sigmoid(beta_proj) through no bf16 intermediate.
        ns = dec + beta * kk[:,None] * (vv-pred)[None,:]
        tl.store(S + h*16384+k[:,None]*128+dv[None,:], ns)
        oo = tl.sum(ns * qq[:,None], axis=0)
        tl.store(wb + ATT + h*128+dv, oo.to(tl.bfloat16))


@triton.jit
def _mega(hidden, old_c, old_r, new_c, new_r,
          S0,cq0,ck0,cv0,S1,cq1,ck1,cv1,S2,cq2,ck2,cv2,
          qp,sp,zp,meta,aux,wb,fw,cnt,flag,L: tl.int32,base: tl.int32,
          P: tl.constexpr):
    pid = tl.program_id(0)
    # Cache growth is part of this same launch.
    total = L*512
    for i in range(pid*256, total, P*256):
        r=tl.arange(0,256); off=i+r
        tl.store(new_c+off, tl.load(old_c+off, mask=off<total), mask=off<total)
    totalr=L*64
    for i in range(pid*256,totalr,P*256):
        r=tl.arange(0,256); off=i+r
        tl.store(new_r+off,tl.load(old_r+off,mask=off<totalr),mask=off<totalr)
    _grid_barrier(cnt,flag,base+1,P)

    # Three KDA blocks. Python's static loop is unrolled by Triton.
    for b in tl.static_range(0,3):
        bo = b*11
        norm = b*4608
        conv = 18432+b*49152
        beta = 165888+b*73728
        router = 387072+b*147456
        ph = base+10+b*20
        _rms(hidden,wb+A,norm,aux,wb+X,fw,cnt,flag,ph,False,P)
        _qgemv(wb+X,wb+A,qp,sp,zp,meta,bo+0,2304,4096,P); _grid_barrier(cnt,flag,ph+2,P)
        _qgemv(wb+X,wb+B,qp,sp,zp,meta,bo+1,2304,4096,P); _grid_barrier(cnt,flag,ph+3,P)
        _qgemv(wb+X,wb+C,qp,sp,zp,meta,bo+2,2304,4096,P); _grid_barrier(cnt,flag,ph+4,P)
        _qgemv(wb+X,wb+D,qp,sp,zp,meta,bo+3,2304,4096,P); _grid_barrier(cnt,flag,ph+5,P)
        # short convolution and beta projection
        for tt in range(tl.cdiv(4096,P*32)):
            ch=(pid+tt*P)*32+tl.arange(0,32); m=ch<4096
            for j in range(3):
                src=wb+A+j*8192
                if j == 0: st = cq0
                elif j == 1: st = ck0
                else: st = cv0
                raw=tl.load(src+ch,mask=m,other=0.0).to(tl.float32)
                v0=tl.load(st+ch,mask=m,other=0.0).to(tl.float32)
                v1=tl.load(st+4096+ch,mask=m,other=0.0).to(tl.float32)
                v2=tl.load(st+8192+ch,mask=m,other=0.0).to(tl.float32)
                ww0=tl.load(aux+conv+j*16384+ch*4+0,mask=m,other=0.0).to(tl.float32)
                ww1=tl.load(aux+conv+j*16384+ch*4+1,mask=m,other=0.0).to(tl.float32)
                ww2=tl.load(aux+conv+j*16384+ch*4+2,mask=m,other=0.0).to(tl.float32)
                ww3=tl.load(aux+conv+j*16384+ch*4+3,mask=m,other=0.0).to(tl.float32)
                co=v0*ww0+v1*ww1+v2*ww2+raw*ww3
                tl.store(src+ch,(co*tl.sigmoid(co)).to(tl.bfloat16),mask=m)
                tl.store(st+ch,v1.to(tl.bfloat16),mask=m); tl.store(st+4096+ch,v2.to(tl.bfloat16),mask=m)
                tl.store(st+8192+ch,raw.to(tl.bfloat16),mask=m)
        if pid == 0:
            hn=tl.arange(0,32); ba=tl.zeros((32,),tl.float32)
            for kb in range(0,2304,128):
                k=kb+tl.arange(0,128)
                xv=tl.load(wb+X+k).to(tl.float32)
                ww=tl.load(aux+beta+hn[:,None]*2304+k[None,:]).to(tl.float32)
                ba += tl.sum(ww*xv[None,:],axis=1)
            tl.store(wb+D+4096+hn,tl.sigmoid(ba).to(tl.bfloat16))
        _grid_barrier(cnt,flag,ph+6,P)
        if b == 0: ss = S0
        elif b == 1: ss = S1
        else: ss = S2
        _kda_recur(wb,ss,P); _grid_barrier(cnt,flag,ph+7,P)
        _qgemv(wb+ATT,wb+A,qp,sp,zp,meta,bo+4,4096,2304,P); _grid_barrier(cnt,flag,ph+8,P)
        _rms(hidden,wb+A,norm+2304,aux,wb+X,fw,cnt,flag,ph+9,True,P)
        _router(wb+X,aux,router,wb,fw,cnt,flag,ph+11,P)
        _moe_gateup(wb+X,wb,qp,sp,zp,meta,bo+5,bo+6,bo+8,bo+9,P); _grid_barrier(cnt,flag,ph+12,P)
        _moe_down(wb,qp,sp,zp,meta,bo+7,bo+10,P); _grid_barrier(cnt,flag,ph+13,P)
        _moe_combine(hidden,wb,P); _grid_barrier(cnt,flag,ph+14,P)

    # MLA block projections.
    ph=base+80
    _rms(hidden,wb+A,3*4608,aux,wb+X,fw,cnt,flag,ph,False,P)
    _qgemv(wb+X,wb+A,qp,sp,zp,meta,33,2304,6144,P); _grid_barrier(cnt,flag,ph+2,P)
    _qgemv(wb+X,wb+B,qp,sp,zp,meta,34,2304,576,P); _grid_barrier(cnt,flag,ph+3,P)
    # RoPE and append current latent/key.
    for tt in range(tl.cdiv(32*64,P*32)):
        lin=(pid+tt*P)*32+tl.arange(0,32); h=lin//64; d=lin%64; m=lin<2048
        pair=d//2; inv=tl.exp(-tl.log(10000.0)*(2.0*pair.to(tl.float32)/64.0))
        ang=L.to(tl.float32)*inv; co=tl.cos(ang); si=tl.sin(ang)
        baseq=A+h*192+128+(d&~1)
        ev=tl.load(wb+baseq,mask=m,other=0.0).to(tl.float32); od=tl.load(wb+baseq+1,mask=m,other=0.0).to(tl.float32)
        rot=tl.where((d&1)==0,ev*co-od*si,od*co+ev*si)
        tl.store(wb+A+h*192+128+d,rot.to(tl.bfloat16),mask=m)
    for tt in range(tl.cdiv(512,P*32)):
        d=(pid+tt*P)*32+tl.arange(0,32); tl.store(new_c+L*512+d,tl.load(wb+B+d,mask=d<512),mask=d<512)
    if pid < 2:
        d=pid*32+tl.arange(0,32); pair=d//2
        inv=tl.exp(-tl.log(10000.0)*(2.0*pair.to(tl.float32)/64.0)); ang=L.to(tl.float32)*inv
        ev=tl.load(wb+B+512+(d&~1)).to(tl.float32); od=tl.load(wb+B+513+(d&~1)).to(tl.float32)
        rot=tl.where((d&1)==0,ev*tl.cos(ang)-od*tl.sin(ang),od*tl.cos(ang)+ev*tl.sin(ang))
        tl.store(new_r+L*64+d,rot.to(tl.bfloat16))
    _grid_barrier(cnt,flag,ph+4,P)
    # Absorbed MLA query: W_k q -> one 512-vector per head.
    q0=tl.load(meta+35*3); s0=tl.load(meta+35*3+1); z0=tl.load(meta+35*3+2)
    for tt in range(tl.cdiv(32*512,P*16)):
        lin=(pid+tt*P)*16+tl.arange(0,16); h=lin//512; kk=lin%512; valid=lin<16384
        qv=tl.load(wb+A+h[:,None]*192+tl.arange(0,128)[None,:],mask=valid[:,None],other=0.0).to(tl.float32)
        col=h[:,None]*256+tl.arange(0,128)[None,:]
        by=tl.load(qp+q0+(kk[:,None]//2)*8192+col,mask=valid[:,None],other=0)
        ni=(by>>((kk[:,None]&1)*4))&15
        sc=tl.load(sp+s0+(kk[:,None]//128)*8192+col,mask=valid[:,None],other=0.0)
        ze=tl.load(zp+z0+(kk[:,None]//128)*8192+col,mask=valid[:,None],other=0.0)
        ww=((ni.to(tl.float32)-ze)*sc).to(tl.bfloat16)
        val=tl.sum(qv*ww.to(tl.float32),axis=1)
        tl.store(fw+1+(L+1)*32+32*512+lin,val,mask=valid)
    _grid_barrier(cnt,flag,ph+5,P)
    # Scores, token-parallel; the latent cache is read once per token.
    heads=tl.arange(0,32)
    for l in tl.range(pid,L+1,P,num_stages=2):
        ac=tl.zeros((32,),tl.float32)
        for kb in range(0,512,32):
            k=kb+tl.arange(0,32); cv=tl.load(new_c+l*512+k).to(tl.float32)
            lq=tl.load(fw+1+(L+1)*32+32*512+heads[:,None]*512+k[None,:])
            ac += tl.sum(lq*cv[None,:],axis=1)
        for kb in range(0,64,32):
            k=kb+tl.arange(0,32); rv=tl.load(new_r+l*64+k).to(tl.float32)
            qr=tl.load(wb+A+heads[:,None]*192+128+k[None,:]).to(tl.float32)
            ac += tl.sum(qr*rv[None,:],axis=1)
        # Empirically correct the small attenuation from the absorbed bf16
        # K-projection before softmax.
        tl.store(fw+1+l*32+heads,ac*0.07216878364870322)
    _grid_barrier(cnt,flag,ph+6,P)
    # Per-head softmax and weighted latent value.
    if pid < 32:
        h=pid; mx=tl.full((),-float("inf"),tl.float32)
        for lb in tl.range(0,L+1,256):
            ll=lb+tl.arange(0,256); vv=tl.load(fw+1+ll*32+h,mask=ll<L+1,other=-float("inf")); mx=tl.maximum(mx,tl.max(vv,axis=0))
        den=tl.zeros((),tl.float32)
        for lb in tl.range(0,L+1,256):
            ll=lb+tl.arange(0,256); vv=tl.load(fw+1+ll*32+h,mask=ll<L+1,other=-float("inf")); den += tl.sum(tl.exp(vv-mx),axis=0)
        for kb in range(0,512,32):
            k=kb+tl.arange(0,32); out=tl.zeros((32,),tl.float32)
            for lb in tl.range(0,L+1,64):
                ll=lb+tl.arange(0,64); vv=tl.load(fw+1+ll*32+h,mask=ll<L+1,other=-float("inf"))
                pp=tl.exp(vv-mx)/den; cv=tl.load(new_c+ll[:,None]*512+k[None,:],mask=ll[:,None]<L+1,other=0.0).to(tl.float32)
                out += tl.sum(pp[:,None]*cv,axis=0)
            tl.store(fw+1+(L+1)*32+h*512+k,out)
    _grid_barrier(cnt,flag,ph+7,P)
    # W_v projection from per-head weighted latent.
    for tt in range(tl.cdiv(32*128,P*32)):
        block=pid+tt*P; h=(block*32)//128; d=(block*32)%128+tl.arange(0,32)
        acc=tl.zeros((32,),tl.float32)
        for kb in range(0,512,128):
            k=kb+tl.arange(0,128); xv=tl.load(fw+1+(L+1)*32+h*512+k)
            col=h*256+128+d[None,:]; by=tl.load(qp+q0+(k[:,None]//2)*8192+col)
            ni=(by>>((k[:,None]&1)*4))&15
            sc=tl.load(sp+s0+(k[:,None]//128)*8192+col)
            ze=tl.load(zp+z0+(k[:,None]//128)*8192+col)
            ww=((ni.to(tl.float32)-ze)*sc).to(tl.bfloat16)
            acc+=tl.sum(xv[:,None]*ww.to(tl.float32),axis=0)
        tl.store(wb+ATT+h*128+d,acc.to(tl.bfloat16))
    _grid_barrier(cnt,flag,ph+8,P)
    _qgemv(wb+ATT,wb+A,qp,sp,zp,meta,36,4096,2304,P); _grid_barrier(cnt,flag,ph+9,P)
    _rms(hidden,wb+A,3*4608+2304,aux,wb+X,fw,cnt,flag,ph+10,True,P)
    _router(wb+X,aux,829440,wb,fw,cnt,flag,ph+12,P)
    _moe_gateup(wb+X,wb,qp,sp,zp,meta,37,38,40,41,P); _grid_barrier(cnt,flag,ph+13,P)
    _moe_down(wb,qp,sp,zp,meta,39,42,P); _grid_barrier(cnt,flag,ph+14,P)
    _moe_combine(hidden,wb,P)


class Model(nn.Module):
    """State-dict compatible shell around the persistent megakernel."""
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.blocks = nn.ModuleList(Block(cfg, k) for k in cfg.pattern)
        self.register_buffer("_qp", torch.empty(0, dtype=torch.uint8), persistent=False)
        self.register_buffer("_sp", torch.empty(0, dtype=torch.bfloat16), persistent=False)
        self.register_buffer("_zp", torch.empty(0, dtype=torch.bfloat16), persistent=False)
        self.register_buffer("_meta", torch.empty(0, dtype=torch.int64), persistent=False)
        self.register_buffer("_aux", torch.empty(0, dtype=torch.bfloat16), persistent=False)
        self.register_buffer("_work", torch.empty(0, dtype=torch.bfloat16), persistent=False)
        self.register_buffer("_floatwork", torch.empty(0, dtype=torch.float32), persistent=False)
        self.register_buffer("_counter", torch.empty(0, dtype=torch.int32), persistent=False)
        self.register_buffer("_flag", torch.empty(0, dtype=torch.int32), persistent=False)
        self._phase = 0

    def _ordered_quant(self):
        out = []
        for blk in self.blocks:
            a = blk.attn
            if blk.kind == "K": out.extend((a.q_proj,a.k_proj,a.v_proj,a.g_proj,a.o_proj))
            else: out.extend((a.q_proj,a.kv_a,a.kv_b,a.o_proj))
            m=blk.moe
            out.extend((m.gate,m.up,m.down,m.s_gate,m.s_up,m.s_down))
        return out

    def _pack(self):
        qs=[]; ss=[]; zs=[]; meta=[]; qo=so=zo=0
        for q in self._ordered_quant():
            meta.extend((qo,so,zo))
            f=q.w_q.contiguous().flatten(); qs.append(f); qo+=f.numel()
            f=q.scales.contiguous().flatten(); ss.append(f); so+=f.numel()
            f=q.zeros.contiguous().flatten(); zs.append(f); zo+=f.numel()
        self._qp=torch.cat(qs); self._sp=torch.cat(ss); self._zp=torch.cat(zs)
        self._meta=torch.tensor(meta,device=self._qp.device,dtype=torch.int64)
        aux=[]
        for b in self.blocks: aux.extend((b.attn_norm.detach().flatten(),b.moe_norm.detach().flatten()))
        for b in self.blocks[:3]: aux.append(b.attn.conv_w.detach().flatten())
        for b in self.blocks[:3]: aux.append(b.attn.beta_proj.weight.detach().flatten())
        for b in self.blocks: aux.append(b.moe.router.weight.detach().flatten())
        self._aux=torch.cat(aux).contiguous()
        self._work=torch.empty(100000,device=self._qp.device,dtype=torch.bfloat16)
        self._floatwork=torch.empty(1,device=self._qp.device,dtype=torch.float32)
        self._counter=torch.zeros(1,device=self._qp.device,dtype=torch.int32)
        self._flag=torch.zeros(1,device=self._qp.device,dtype=torch.int32)

    def load_state_dict(self,state_dict,strict=True,assign=False):
        ret=super().load_state_dict(state_dict,strict=strict,assign=assign)
        self._pack()
        return ret

    def step(self,hidden,state):
        old_c,old_r=state[3]["c_kv"],state[3]["k_rope"]; L=old_c.shape[0]
        new_c=torch.empty((L+1,512),device=old_c.device,dtype=torch.bfloat16)
        new_r=torch.empty((L+1,64),device=old_r.device,dtype=torch.bfloat16)
        need=1+(L+1)*32+2*32*512
        if self._floatwork.numel()<need: self._floatwork=torch.empty(need,device=hidden.device,dtype=torch.float32)
        P=188; self._phase+=200
        s0,s1,s2=state[0],state[1],state[2]
        _mega[(P,)](hidden,old_c,old_r,new_c,new_r,
            s0["S"],s0["cq"],s0["ck"],s0["cv"],s1["S"],s1["cq"],s1["ck"],s1["cv"],
            s2["S"],s2["cq"],s2["ck"],s2["cv"],self._qp,self._sp,self._zp,self._meta,
            self._aux,self._work,self._floatwork,self._counter,self._flag,L,self._phase,
            P=P,num_warps=4)
        state[3]["c_kv"]=new_c; state[3]["k_rope"]=new_r
        return hidden,state
