"""Fused single-kernel W4A16 Kimi-Linear hybrid decode (megakernel).

The entire per-token forward -- 3 KDA layers + 1 MLA layer, each + a 64-expert
MoE FFN, every int4 dequant-GEMV, short conv, KDA recurrence, MLA latent-cache
attention (absorb form), router+experts, both RMSNorms and residuals -- is fused
into ONE cooperative CUDA kernel launched exactly once per step().

Weight storage modules (QuantLinear/QuantExperts/Block/Model) keep the reference
buffer/parameter names so load_state_dict(strict=True) works unchanged.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import torch
import torch.nn as nn

OP_TYPE = "kimi_linear_w4a16_decode"
HARDWARE_REQUIRED = ["RTX_PRO_6000"]
EPS = 1.0e-6
GROUP_SIZE = 128

_CUDA_HOME = "/tmp/cudatk"
if os.path.isdir(_CUDA_HOME):
    os.environ.setdefault("CUDA_HOME", _CUDA_HOME)
    os.environ["PATH"] = _CUDA_HOME + "/bin:" + os.environ.get("PATH", "")
os.environ.setdefault("TORCH_CUDA_ARCH_LIST", "12.0")


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
# W4A16 storage (same pack/format as reference)
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


def dequant(w_q, scales, zeros, K, group):
    wu = _unpack_int4(w_q, K).to(torch.bfloat16)
    s = scales.repeat_interleave(group, dim=0)
    z = zeros.repeat_interleave(group, dim=0)
    return (wu - z) * s


class QuantLinear(nn.Module):
    def __init__(self, in_f, out_f, group=GROUP_SIZE):
        super().__init__()
        assert in_f % group == 0 and in_f % 2 == 0
        self.in_f, self.out_f, self.group = in_f, out_f, group
        ng = in_f // group
        self.register_buffer("w_q", torch.zeros(in_f // 2, out_f, dtype=torch.uint8))
        self.register_buffer("scales", torch.zeros(ng, out_f, dtype=torch.bfloat16))
        self.register_buffer("zeros", torch.zeros(ng, out_f, dtype=torch.bfloat16))

    def init_random(self, gen, std=0.02):
        w = torch.randn(self.in_f, self.out_f, generator=gen) * std
        wq, s, z = quantize(w, self.group)
        self.w_q.copy_(wq); self.scales.copy_(s); self.zeros.copy_(z)

    def weight_bf(self):
        return dequant(self.w_q, self.scales, self.zeros, self.in_f, self.group)


class QuantExperts(nn.Module):
    def __init__(self, n, in_f, out_f, group=GROUP_SIZE):
        super().__init__()
        self.n, self.in_f, self.out_f, self.group = n, in_f, out_f, group
        ng = in_f // group
        self.register_buffer("w_q", torch.zeros(n, in_f // 2, out_f, dtype=torch.uint8))
        self.register_buffer("scales", torch.zeros(n, ng, out_f, dtype=torch.bfloat16))
        self.register_buffer("zeros", torch.zeros(n, ng, out_f, dtype=torch.bfloat16))

    def init_random(self, gen, std=0.02):
        for e in range(self.n):
            w = torch.randn(self.in_f, self.out_f, generator=gen) * std
            wq, s, z = quantize(w, self.group)
            self.w_q[e].copy_(wq); self.scales[e].copy_(s); self.zeros[e].copy_(z)


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
# megakernel loader -- the ENTIRE per-token forward is this ONE cooperative
# CUDA kernel (single cudaLaunchCooperativeKernel per step). Source embedded so
# the megakernel is self-contained in this module.
# --------------------------------------------------------------------------- #
_MOD = None

_CUDA_SRC = r"""#include <cuda_runtime.h>
#include <cuda_bf16.h>
#include <cooperative_groups.h>
#include <torch/extension.h>
#include <math.h>
namespace cg = cooperative_groups;
typedef __nv_bfloat16 bf16;
__device__ __forceinline__ float b2f(bf16 x){ return __bfloat162float(x); }
__device__ __forceinline__ bf16 f2b(float x){ return __float2bfloat16(x); }
__device__ __forceinline__ float dsoftplus(float x){ return x>20.f? x : log1pf(expf(x)); }
__device__ __forceinline__ float silu(float x){ return x/(1.f+expf(-x)); }

#define D 2304
#define KH 32
#define DK 128
#define KC 4096
#define NG_D 18
#define KVL 512
#define QKR 64
#define QKN 128
#define VH 128
#define KVB_HS 256
#define KVB_O_ 8192
#define MLA_QO 6144
#define KVA_O 576
#define OC 4096
#define NG_OC 32
#define E 64
#define NACT 8
#define MINTER 1024
#define NG_M 8
#define ROUTED_SCALING 2.446f
#define EPS 1.0e-6f
#define ROPE_THETA 10000.0f

// fused int4 dequant GEMV: warp-per-column. 32 lanes cooperate over in_f.
// y[col]=sum_k x[k]*(nib-zero)*scale. wq [in/2,out] uint8; sc/zr [in/128,out] bf16.
__device__ void gemv(const float* __restrict__ x, const uint8_t* __restrict__ wq,
    const bf16* __restrict__ sc, const bf16* __restrict__ zr,
    float* __restrict__ y, int in_f, int out_f, int ng, bool accum, float wscale){
    int lane=threadIdx.x&31;
    int warp_g=(blockIdx.x*blockDim.x+threadIdx.x)>>5;
    int nwarp=(gridDim.x*blockDim.x)>>5;
    int half=in_f>>1;
    for(int col=warp_g; col<out_f; col+=nwarp){
        float acc=0.f;
        const uint16_t* wr=(const uint16_t*)(wq+(size_t)col*half);
        // each lane reads one uint16 (4 int4 elements) per group, fully coalesced
        for(int g=0; g<ng; g++){
            float s=b2f(sc[(size_t)g*out_f+col]);
            float z=b2f(zr[(size_t)g*out_f+col]);
            int k=g*128+lane*4;
            uint16_t w=wr[g*32+lane];
            float n0=(float)(w&0xF), n1=(float)((w>>4)&0xF), n2=(float)((w>>8)&0xF), n3=(float)((w>>12)&0xF);
            acc += x[k]*(n0-z)*s + x[k+1]*(n1-z)*s + x[k+2]*(n2-z)*s + x[k+3]*(n3-z)*s;
        }
        #pragma unroll
        for(int o=16;o>0;o>>=1) acc+=__shfl_down_sync(0xffffffff,acc,o);
        if(lane==0){ if(accum) y[col]+=acc*wscale; else y[col]=acc*wscale; }
    }
}
// batched gate+up over ALL nexp experts: moe_h[j*MINTER+m]=silu(gate)*up.
// gwq/uwq base pointers, per-expert stride WSTR (=GWS) & SSTR (=GSS). eidx maps j->expert.
__device__ void moe_gu_batch(const float* __restrict__ x, const uint8_t* __restrict__ gwq,const bf16* __restrict__ gsc,const bf16* __restrict__ gzr,
    const uint8_t* __restrict__ uwq,const bf16* __restrict__ usc,const bf16* __restrict__ uzr, float* __restrict__ moe_h,
    const int* __restrict__ eidx, int nexp, long WSTR,long SSTR){
    int lane=threadIdx.x&31; int wg=(blockIdx.x*blockDim.x+threadIdx.x)>>5; int nw=(gridDim.x*blockDim.x)>>5;
    int total=nexp*MINTER;
    for(int t=wg;t<total;t+=nw){
        int j=t/MINTER, m=t%MINTER;
        long e=eidx?eidx[j]:0;
        long WB=e*WSTR, SB=e*SSTR;
        float ga=0.f,ua=0.f;
        const uint16_t* gwr=(const uint16_t*)(gwq+WB+(size_t)m*1152);
        const uint16_t* uwr=(const uint16_t*)(uwq+WB+(size_t)m*1152);
        for(int g=0;g<NG_D;g++){
            float gs=b2f(gsc[SB+(long)g*MINTER+m]),gz=b2f(gzr[SB+(long)g*MINTER+m]);
            float us=b2f(usc[SB+(long)g*MINTER+m]),uz=b2f(uzr[SB+(long)g*MINTER+m]);
            int k=g*128+lane*4;
            uint16_t gw=gwr[g*32+lane], uw=uwr[g*32+lane];
            ga+=x[k]*((float)(gw&0xF)-gz)*gs + x[k+1]*((float)((gw>>4)&0xF)-gz)*gs + x[k+2]*((float)((gw>>8)&0xF)-gz)*gs + x[k+3]*((float)((gw>>12)&0xF)-gz)*gs;
            ua+=x[k]*((float)(uw&0xF)-uz)*us + x[k+1]*((float)((uw>>4)&0xF)-uz)*us + x[k+2]*((float)((uw>>8)&0xF)-uz)*us + x[k+3]*((float)((uw>>12)&0xF)-uz)*us;
        }
        #pragma unroll
        for(int o=16;o>0;o>>=1){ ga+=__shfl_down_sync(0xffffffff,ga,o); ua+=__shfl_down_sync(0xffffffff,ua,o);}
        if(lane==0) moe_h[j*MINTER+m]=silu(ga)*ua;
    }
}
// batched down over ALL nexp experts, accumulating wj*(down.h_j) into moe_out.
// grid-wide: each warp owns (j? no) -- we loop cols, sum over experts inside to reuse col.
__device__ void moe_down_batch(const float* __restrict__ moe_h, const uint8_t* __restrict__ dwq,const bf16* __restrict__ dsc,const bf16* __restrict__ dzr,
    float* __restrict__ moe_out, const int* __restrict__ eidx, const float* __restrict__ wj, int nexp, long WSTR,long SSTR){
    int lane=threadIdx.x&31; int wg=(blockIdx.x*blockDim.x+threadIdx.x)>>5; int nw=(gridDim.x*blockDim.x)>>5;
    int total=nexp*D;
    for(int t=wg;t<total;t+=nw){
        int j=t/D, col=t%D;
        long e=eidx?eidx[j]:0; long WB=e*WSTR, SB=e*SSTR; const float* h=moe_h+(long)j*MINTER;
        float acc=0.f;
        const uint16_t* dwr=(const uint16_t*)(dwq+WB+(size_t)col*512);
        for(int g=0;g<NG_M;g++){
            float s=b2f(dsc[SB+(long)g*D+col]),z=b2f(dzr[SB+(long)g*D+col]);
            int k=g*128+lane*4;
            uint16_t w=dwr[g*32+lane];
            acc+=h[k]*((float)(w&0xF)-z)*s + h[k+1]*((float)((w>>4)&0xF)-z)*s + h[k+2]*((float)((w>>8)&0xF)-z)*s + h[k+3]*((float)((w>>12)&0xF)-z)*s;
        }
        #pragma unroll
        for(int o=16;o>0;o>>=1) acc+=__shfl_down_sync(0xffffffff,acc,o);
        if(lane==0) atomicAdd(&moe_out[col], (wj?wj[j]:1.f)*acc);
    }
}
// dense bf16 matvec: W[out,in], y[o]=sum_k x[k]*W[o,k]
__device__ void matvec_bf(const float* x, const bf16* W, float* y, int out_f, int in_f){
    int gtid=blockIdx.x*blockDim.x+threadIdx.x;
    int gstride=gridDim.x*blockDim.x;
    for(int o=gtid;o<out_f;o+=gstride){
        float acc=0.f; const bf16* wr=W+(size_t)o*in_f;
        for(int k=0;k<in_f;k++) acc+=x[k]*b2f(wr[k]);
        y[o]=acc;
    }
}

extern "C" __global__ void mega(
    const bf16* __restrict__ hin, bf16* __restrict__ hout,
    const long* __restrict__ P,
    const bf16* __restrict__ old_ckv, const bf16* __restrict__ old_krope,
    bf16* __restrict__ new_ckv, bf16* __restrict__ new_krope, int pos,
    float* S0, float* S1, float* S2,
    bf16* cq0, bf16* ck0, bf16* cv0,
    bf16* cq1, bf16* ck1, bf16* cv1,
    bf16* cq2, bf16* ck2, bf16* cv2,
    float* xres, float* xn, float* sA, float* sB, float* sC, float* sG,
    float* qc, float* kc, float* vc, float* ko,
    float* attn_out, float* qabs, float* scores, float* mla_o,
    float* router, float* moe_h, float* moe_out,
    float* beta, float* ssum, int* topk_idx, float* topk_w
){
    cg::grid_group grid = cg::this_grid();
    int gtid=blockIdx.x*blockDim.x+threadIdx.x;
    int gstride=gridDim.x*blockDim.x;
    const float kda_scale = 1.0f/sqrtf((float)DK);
    const float mla_scale = 1.0f/sqrtf((float)(QKN+QKR));

    for(int i=gtid;i<D;i+=gstride) xres[i]=b2f(hin[i]);
    grid.sync();

    long base0=P[0],base1=P[1],base2=P[2],base3=P[3];
    const long* Pk=P+4;
    #define PP(b,i) (Pk[(b)+(i)])

    for(int blk=0; blk<4; blk++){
        long base=(blk==0)?base0:(blk==1)?base1:(blk==2)?base2:base3;
        bool isKDA=(blk<3);
        const bf16* attn_norm=(const bf16*)PP(base,0);
        const bf16* moe_norm=(const bf16*)PP(base,1);

        // redundant per-block RMSNorm into xn (each block computes full xn from xres,
        // which is stable post-sync); avoids a grid.sync serialization bubble.
        {
            float loc=0.f;
            for(int i=threadIdx.x;i<D;i+=blockDim.x){ float v=xres[i]; loc+=v*v; }
            __shared__ float sh[256]; sh[threadIdx.x]=loc; __syncthreads();
            for(int s=blockDim.x/2;s>0;s>>=1){ if(threadIdx.x<s) sh[threadIdx.x]+=sh[threadIdx.x+s]; __syncthreads(); }
            float rms=rsqrtf(sh[0]/D+EPS);
            for(int i=threadIdx.x;i<D;i+=blockDim.x) xn[i]=xres[i]*rms*b2f(attn_norm[i]);
            __syncthreads();
        }
        if(isKDA){
            gemv(xn,(const uint8_t*)PP(base,3),(const bf16*)PP(base,4),(const bf16*)PP(base,5),sA,D,KC,NG_D,false,1.f);
            gemv(xn,(const uint8_t*)PP(base,6),(const bf16*)PP(base,7),(const bf16*)PP(base,8),sB,D,KC,NG_D,false,1.f);
            gemv(xn,(const uint8_t*)PP(base,9),(const bf16*)PP(base,10),(const bf16*)PP(base,11),sC,D,KC,NG_D,false,1.f);
            gemv(xn,(const uint8_t*)PP(base,12),(const bf16*)PP(base,13),(const bf16*)PP(base,14),sG,D,KC,NG_D,false,1.f);
            matvec_bf(xn,(const bf16*)PP(base,15),beta,KH,D);
            grid.sync();
            const bf16* conv_w=(const bf16*)PP(base,2);
            bf16 *cq,*ck,*cv; float* Scur;
            if(blk==0){cq=cq0;ck=ck0;cv=cv0;Scur=S0;}
            else if(blk==1){cq=cq1;ck=ck1;cv=cv1;Scur=S1;}
            else {cq=cq2;ck=ck2;cv=cv2;Scur=S2;}
            for(int c=gtid;c<KC;c+=gstride){
                float cw0,cw1,cw2,cw3,acc;
                cw0=b2f(conv_w[0*KC*4+c*4+0]);cw1=b2f(conv_w[0*KC*4+c*4+1]);cw2=b2f(conv_w[0*KC*4+c*4+2]);cw3=b2f(conv_w[0*KC*4+c*4+3]);
                acc=b2f(cq[0*KC+c])*cw0+b2f(cq[1*KC+c])*cw1+b2f(cq[2*KC+c])*cw2+sA[c]*cw3;
                qc[c]=silu(acc)*kda_scale;
                cq[0*KC+c]=cq[1*KC+c];cq[1*KC+c]=cq[2*KC+c];cq[2*KC+c]=f2b(sA[c]);
                cw0=b2f(conv_w[1*KC*4+c*4+0]);cw1=b2f(conv_w[1*KC*4+c*4+1]);cw2=b2f(conv_w[1*KC*4+c*4+2]);cw3=b2f(conv_w[1*KC*4+c*4+3]);
                acc=b2f(ck[0*KC+c])*cw0+b2f(ck[1*KC+c])*cw1+b2f(ck[2*KC+c])*cw2+sB[c]*cw3;
                kc[c]=silu(acc);
                ck[0*KC+c]=ck[1*KC+c];ck[1*KC+c]=ck[2*KC+c];ck[2*KC+c]=f2b(sB[c]);
                cw0=b2f(conv_w[2*KC*4+c*4+0]);cw1=b2f(conv_w[2*KC*4+c*4+1]);cw2=b2f(conv_w[2*KC*4+c*4+2]);cw3=b2f(conv_w[2*KC*4+c*4+3]);
                acc=b2f(cv[0*KC+c])*cw0+b2f(cv[1*KC+c])*cw1+b2f(cv[2*KC+c])*cw2+sC[c]*cw3;
                vc[c]=silu(acc);
                cv[0*KC+c]=cv[1*KC+c];cv[1*KC+c]=cv[2*KC+c];cv[2*KC+c]=f2b(sC[c]);
                sG[c]=expf(-dsoftplus(sG[c]));
            }
            grid.sync();
            // warp-per-(h,dv): 32 lanes split the dk contraction (DK=128 -> 4 each)
            {
              int lane=threadIdx.x&31; int wg2=(blockIdx.x*blockDim.x+threadIdx.x)>>5; int nw2=(gridDim.x*blockDim.x)>>5;
              for(int t=wg2;t<KH*DK;t+=nw2){
                int h=t/DK, dv=t%DK; long sbase=(long)h*DK*DK+dv;
                float pred=0.f;
                for(int dk=lane;dk<DK;dk+=32){ long idx=sbase+(long)dk*DK; float sd=Scur[idx]*sG[h*DK+dk]; Scur[idx]=sd; pred+=sd*kc[h*DK+dk]; }
                #pragma unroll
                for(int o=16;o>0;o>>=1) pred+=__shfl_xor_sync(0xffffffff,pred,o);
                float delta=beta[h]*(vc[h*DK+dv]-pred);
                float ov=0.f;
                for(int dk=lane;dk<DK;dk+=32){ long idx=sbase+(long)dk*DK; float s=Scur[idx]+delta*kc[h*DK+dk]; Scur[idx]=s; ov+=s*qc[h*DK+dk]; }
                #pragma unroll
                for(int o=16;o>0;o>>=1) ov+=__shfl_xor_sync(0xffffffff,ov,o);
                if(lane==0) ko[h*DK+dv]=ov;
              }
            }
            grid.sync();
            gemv(ko,(const uint8_t*)PP(base,16),(const bf16*)PP(base,17),(const bf16*)PP(base,18),attn_out,KC,D,NG_OC,false,1.f);
            grid.sync();
        } else {
            gemv(xn,(const uint8_t*)PP(base,2),(const bf16*)PP(base,3),(const bf16*)PP(base,4),sA,D,MLA_QO,NG_D,false,1.f);
            gemv(xn,(const uint8_t*)PP(base,5),(const bf16*)PP(base,6),(const bf16*)PP(base,7),sB,D,KVA_O,NG_D,false,1.f);
            grid.sync();
            for(int i=gtid;i<KVL;i+=gstride) new_ckv[(long)pos*KVL+i]=f2b(sB[i]);
            for(int j=gtid;j<QKR/2;j+=gstride){
                float inv=powf(ROPE_THETA, -((float)(2*j)/(float)QKR));
                float ang=pos*inv; float cs=cosf(ang), sn=sinf(ang);
                float even=sB[KVL+2*j], odd=sB[KVL+2*j+1];
                new_krope[(long)pos*QKR+2*j]=f2b(even*cs-odd*sn);
                new_krope[(long)pos*QKR+2*j+1]=f2b(odd*cs+even*sn);
            }
            for(int t=gtid;t<KH*(QKR/2);t+=gstride){
                int h=t/(QKR/2), j=t%(QKR/2);
                float inv=powf(ROPE_THETA, -((float)(2*j)/(float)QKR));
                float ang=pos*inv; float cs=cosf(ang), sn=sinf(ang);
                int b0=h*(QKN+QKR)+QKN+2*j;
                float even=sA[b0], odd=sA[b0+1];
                sA[b0]=even*cs-odd*sn; sA[b0+1]=odd*cs+even*sn;
            }
            grid.sync();
            int P1=pos+1;
            const uint8_t* kvb_wq=(const uint8_t*)PP(base,8);
            const bf16* kvb_sc=(const bf16*)PP(base,9);
            const bf16* kvb_zr=(const bf16*)PP(base,10);
            for(int t=gtid;t<KH*KVL;t+=gstride){
                int h=t/KVL, l=t%KVL;
                int grp=l>>7; int rowh=l>>1; int hi=l&1;
                float acc=0.f; int outbase=h*KVB_HS;
                for(int d=0;d<QKN;d++){
                    int out=outbase+d;
                    uint8_t byte=kvb_wq[(size_t)rowh*KVB_O_+out];
                    float nib=hi?(float)((byte>>4)&0xF):(float)(byte&0xF);
                    float sc=b2f(kvb_sc[grp*KVB_O_+out]); float zr=b2f(kvb_zr[grp*KVB_O_+out]);
                    acc += sA[h*(QKN+QKR)+d]*(nib-zr)*sc;
                }
                qabs[h*KVL+l]=acc;
            }
            grid.sync();
            // warp-per-(h,p): lanes split the l (512) + r (64) contraction, coalesced ckv row
            {
              int lane=threadIdx.x&31; int wg2=(blockIdx.x*blockDim.x+threadIdx.x)>>5; int nw2=(gridDim.x*blockDim.x)>>5;
              for(int t=wg2;t<KH*P1;t+=nw2){
                int h=t/P1, p=t%P1;
                const bf16* ckv_p=(p<pos)? old_ckv+(long)p*KVL : new_ckv+(long)pos*KVL;
                const bf16* kr_p =(p<pos)? old_krope+(long)p*QKR : new_krope+(long)pos*QKR;
                const float* qa=qabs+h*KVL; const float* qr=sA+h*(QKN+QKR)+QKN;
                float acc=0.f;
                for(int l=lane;l<KVL;l+=32) acc+=qa[l]*b2f(ckv_p[l]);
                for(int r=lane;r<QKR;r+=32) acc+=qr[r]*b2f(kr_p[r]);
                #pragma unroll
                for(int o=16;o>0;o>>=1) acc+=__shfl_xor_sync(0xffffffff,acc,o);
                if(lane==0) scores[(long)h*P1+p]=acc*mla_scale;
              }
            }
            grid.sync();
            if(blockIdx.x<KH){
                int h=blockIdx.x; __shared__ float rsh[256];
                float m=-1e30f;
                for(int p=threadIdx.x;p<P1;p+=blockDim.x) m=fmaxf(m,scores[(long)h*P1+p]);
                rsh[threadIdx.x]=m; __syncthreads();
                for(int s=blockDim.x/2;s>0;s>>=1){ if(threadIdx.x<s) rsh[threadIdx.x]=fmaxf(rsh[threadIdx.x],rsh[threadIdx.x+s]); __syncthreads(); }
                float mx=rsh[0]; __syncthreads();
                float sm=0.f;
                for(int p=threadIdx.x;p<P1;p+=blockDim.x){ float e=expf(scores[(long)h*P1+p]-mx); scores[(long)h*P1+p]=e; sm+=e; }
                rsh[threadIdx.x]=sm; __syncthreads();
                for(int s=blockDim.x/2;s>0;s>>=1){ if(threadIdx.x<s) rsh[threadIdx.x]+=rsh[threadIdx.x+s]; __syncthreads(); }
                if(threadIdx.x==0) ssum[h]=rsh[0];
            }
            grid.sync();
            for(int t=gtid;t<KH*KVL;t+=gstride){
                int h=t/KVL,l=t%KVL; float inv=1.f/ssum[h]; float acc=0.f;
                for(int p=0;p<P1;p++){ const bf16* ckv_p=(p<pos)? old_ckv+(long)p*KVL : new_ckv+(long)pos*KVL; acc+=scores[(long)h*P1+p]*b2f(ckv_p[l]); }
                mla_o[h*KVL+l]=acc*inv;
            }
            grid.sync();
            for(int t=gtid;t<KH*VH;t+=gstride){
                int h=t/VH,d=t%VH; int out=h*KVB_HS+QKN+d; float acc=0.f;
                for(int l=0;l<KVL;l++){
                    int grp=l>>7; int rowh=l>>1; int hi=l&1;
                    uint8_t byte=kvb_wq[(size_t)rowh*KVB_O_+out];
                    float nib=hi?(float)((byte>>4)&0xF):(float)(byte&0xF);
                    float sc=b2f(kvb_sc[grp*KVB_O_+out]); float zr=b2f(kvb_zr[grp*KVB_O_+out]);
                    acc+=mla_o[h*KVL+l]*(nib-zr)*sc;
                }
                ko[h*VH+d]=acc;
            }
            grid.sync();
            gemv(ko,(const uint8_t*)PP(base,11),(const bf16*)PP(base,12),(const bf16*)PP(base,13),attn_out,OC,D,NG_OC,false,1.f);
            grid.sync();
        }
        for(int i=gtid;i<D;i+=gstride) xres[i]+=attn_out[i];
        grid.sync();
        {
            float loc=0.f;
            for(int i=threadIdx.x;i<D;i+=blockDim.x){ float v=xres[i]; loc+=v*v; }
            __shared__ float sh[256]; sh[threadIdx.x]=loc; __syncthreads();
            for(int s=blockDim.x/2;s>0;s>>=1){ if(threadIdx.x<s) sh[threadIdx.x]+=sh[threadIdx.x+s]; __syncthreads(); }
            float rms=rsqrtf(sh[0]/D+EPS);
            for(int i=threadIdx.x;i<D;i+=blockDim.x) xn[i]=xres[i]*rms*b2f(moe_norm[i]);
            __syncthreads();
        }
        int ms=isKDA?19:14;
        matvec_bf(xn,(const bf16*)PP(base,ms),router,E,D);
        grid.sync();
        // block 0 does router-softmax+topk while ALL blocks zero moe_out concurrently
        if(blockIdx.x==0 && threadIdx.x==0){
            float mx=-1e30f; for(int e=0;e<E;e++) mx=fmaxf(mx,router[e]);
            float sm=0.f; for(int e=0;e<E;e++){ router[e]=expf(router[e]-mx); sm+=router[e]; }
            for(int e=0;e<E;e++) router[e]/=sm;
            bool used[E]; for(int e=0;e<E;e++) used[e]=false;
            float wsum=0.f;
            for(int j=0;j<NACT;j++){
                int bi=-1; float bv=-1.f;
                for(int e=0;e<E;e++) if(!used[e]&&router[e]>bv){bv=router[e];bi=e;}
                used[bi]=true; topk_idx[j]=bi; topk_w[j]=bv; wsum+=bv;
            }
            float invn=ROUTED_SCALING/(wsum+1e-9f);
            for(int j=0;j<NACT;j++) topk_w[j]*=invn;
        }
        for(int i=gtid;i<D;i+=gstride) moe_out[i]=0.f;
        grid.sync();
        const uint8_t* gwq=(const uint8_t*)PP(base,ms+1); const bf16* gsc=(const bf16*)PP(base,ms+2); const bf16* gzr=(const bf16*)PP(base,ms+3);
        const uint8_t* uwq=(const uint8_t*)PP(base,ms+4); const bf16* usc=(const bf16*)PP(base,ms+5); const bf16* uzr=(const bf16*)PP(base,ms+6);
        const uint8_t* dwq=(const uint8_t*)PP(base,ms+7); const bf16* dsc=(const bf16*)PP(base,ms+8); const bf16* dzr=(const bf16*)PP(base,ms+9);
        const uint8_t* sgwq=(const uint8_t*)PP(base,ms+10); const bf16* sgsc=(const bf16*)PP(base,ms+11); const bf16* sgzr=(const bf16*)PP(base,ms+12);
        const uint8_t* suwq=(const uint8_t*)PP(base,ms+13); const bf16* susc=(const bf16*)PP(base,ms+14); const bf16* suzr=(const bf16*)PP(base,ms+15);
        const uint8_t* sdwq=(const uint8_t*)PP(base,ms+16); const bf16* sdsc=(const bf16*)PP(base,ms+17); const bf16* sdzr=(const bf16*)PP(base,ms+18);
        const long GWS=(long)1152*MINTER, GSS=(long)NG_D*MINTER;
        const long DWS=(long)512*D, DSS=(long)NG_M*D;
        // routed + shared gate/up share one phase (shared uses moe_h slot NACT), one sync
        moe_gu_batch(xn, gwq,gsc,gzr, uwq,usc,uzr, moe_h, topk_idx, NACT, GWS, GSS);
        moe_gu_batch(xn, sgwq,sgsc,sgzr, suwq,susc,suzr, moe_h+(long)NACT*MINTER, nullptr, 1, 0, 0);
        grid.sync();
        moe_down_batch(moe_h, dwq,dsc,dzr, moe_out, topk_idx, topk_w, NACT, DWS, DSS);
        moe_down_batch(moe_h+(long)NACT*MINTER, sdwq,sdsc,sdzr, moe_out, nullptr, nullptr, 1, 0, 0);
        grid.sync();
        for(int i=gtid;i<D;i+=gstride) xres[i]+=moe_out[i];
        grid.sync();
    }
    for(int i=gtid;i<D;i+=gstride) hout[i]=f2b(xres[i]);
}

void launch_mega(
    torch::Tensor hin, torch::Tensor hout, torch::Tensor P,
    torch::Tensor old_ckv, torch::Tensor old_krope, torch::Tensor new_ckv, torch::Tensor new_krope, int pos,
    torch::Tensor S0, torch::Tensor S1, torch::Tensor S2,
    torch::Tensor cq0, torch::Tensor ck0, torch::Tensor cv0,
    torch::Tensor cq1, torch::Tensor ck1, torch::Tensor cv1,
    torch::Tensor cq2, torch::Tensor ck2, torch::Tensor cv2,
    torch::Tensor scratch, torch::Tensor iscratch)
{
    // carve scratch (float)
    float* sp = scratch.data_ptr<float>();
    long o=0;
    auto take=[&](long n){ float* p=sp+o; o+=n; return p; };
    float* xres=take(D); float* xn=take(D);
    float* sA=take(MLA_QO); float* sB=take(KVA_O>KC?KVA_O:KC); float* sC=take(KC); float* sG=take(KC);
    float* qc=take(KC); float* kc=take(KC); float* vc=take(KC); float* ko=take(KC);
    float* attn_out=take(D); float* qabs=take(KH*KVL);
    float* scores=take((long)KH*(20000)); float* mla_o=take(KH*KVL);
    float* router=take(E); float* moe_h=take((NACT+1)*MINTER); float* moe_out=take(D);
    float* beta=take(KH); float* ssum=take(KH);
    int* ip=iscratch.data_ptr<int>();
    int* topk_idx=ip; float* topk_w=(float*)(ip+NACT);

    int block=256;
    int dev; cudaGetDevice(&dev); int numSM; cudaDeviceGetAttribute(&numSM,cudaDevAttrMultiProcessorCount,dev);
    int maxb; cudaOccupancyMaxActiveBlocksPerMultiprocessor(&maxb,(void*)mega,block,0);
    int grid=numSM*maxb;
    size_t shm=0;
    const bf16* hinp=(const bf16*)hin.data_ptr();
    bf16* houtp=(bf16*)hout.data_ptr();
    const long* Pp=P.data_ptr<long>();
    const bf16* ockv=(const bf16*)old_ckv.data_ptr(); const bf16* okr=(const bf16*)old_krope.data_ptr();
    bf16* nckv=(bf16*)new_ckv.data_ptr(); bf16* nkr=(bf16*)new_krope.data_ptr();
    float *pS0=S0.data_ptr<float>(),*pS1=S1.data_ptr<float>(),*pS2=S2.data_ptr<float>();
    bf16 *pcq0=(bf16*)cq0.data_ptr(),*pck0=(bf16*)ck0.data_ptr(),*pcv0=(bf16*)cv0.data_ptr();
    bf16 *pcq1=(bf16*)cq1.data_ptr(),*pck1=(bf16*)ck1.data_ptr(),*pcv1=(bf16*)cv1.data_ptr();
    bf16 *pcq2=(bf16*)cq2.data_ptr(),*pck2=(bf16*)ck2.data_ptr(),*pcv2=(bf16*)cv2.data_ptr();
    void* args[]={&hinp,&houtp,&Pp,&ockv,&okr,&nckv,&nkr,&pos,
        &pS0,&pS1,&pS2,&pcq0,&pck0,&pcv0,&pcq1,&pck1,&pcv1,&pcq2,&pck2,&pcv2,
        &xres,&xn,&sA,&sB,&sC,&sG,&qc,&kc,&vc,&ko,&attn_out,&qabs,&scores,&mla_o,
        &router,&moe_h,&moe_out,&beta,&ssum,&topk_idx,&topk_w};
    cudaFuncSetAttribute((void*)mega, cudaFuncAttributeMaxDynamicSharedMemorySize, shm);
    cudaError_t err=cudaLaunchCooperativeKernel((void*)mega,dim3(grid),dim3(block),args,shm,0);
    if(err!=cudaSuccess) printf("launch err: %s\n",cudaGetErrorString(err));
}"""

_CPP_DECL = "void launch_mega(at::Tensor,at::Tensor,at::Tensor,at::Tensor,at::Tensor,at::Tensor,at::Tensor,int,at::Tensor,at::Tensor,at::Tensor,at::Tensor,at::Tensor,at::Tensor,at::Tensor,at::Tensor,at::Tensor,at::Tensor,at::Tensor,at::Tensor,at::Tensor,at::Tensor);"


def _get_module():
    global _MOD
    if _MOD is not None:
        return _MOD
    from torch.utils.cpp_extension import load_inline
    _MOD = load_inline(
        name="kimi_mega",
        cpp_sources=[_CPP_DECL],
        cuda_sources=[_CUDA_SRC],
        functions=["launch_mega"],
        extra_cuda_cflags=["-arch=sm_120", "-O3", "--use_fast_math"],
        extra_cflags=["-O3"],
        verbose=False,
    )
    return _MOD


class Model(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.blocks = nn.ModuleList(Block(cfg, k) for k in cfg.pattern)
        self._ptr = None
        self._scratch = None
        self._iscratch = None

    # ---- build the per-block pointer table (element offsets into Pk) ----
    def _repack(self, wq):
        # [in/2, out] -> [out, in/2] col-major, contiguous, kept alive.
        t = wq.t().contiguous()
        self._keep.append(t)
        return t

    def _repack_e(self, wq):
        # [n, in/2, out] -> [n, out, in/2]
        t = wq.transpose(1, 2).contiguous()
        self._keep.append(t)
        return t

    def _build_ptrs(self):
        blocks = self.blocks
        self._keep = []
        entries = []
        bases = []
        for blk, b in enumerate(blocks):
            bases.append(len(entries))
            isK = (b.kind == "K")
            entries.append(b.attn_norm.data_ptr())
            entries.append(b.moe_norm.data_ptr())
            a = b.attn
            if isK:
                entries.append(a.conv_w.data_ptr())
                for ql in (a.q_proj, a.k_proj, a.v_proj, a.g_proj):
                    entries += [self._repack(ql.w_q).data_ptr(), ql.scales.data_ptr(), ql.zeros.data_ptr()]
                entries.append(a.beta_proj.weight.data_ptr())
                entries += [self._repack(a.o_proj.w_q).data_ptr(), a.o_proj.scales.data_ptr(), a.o_proj.zeros.data_ptr()]
            else:
                # q_proj, kv_a, o_proj repacked; kv_b stays row-major
                for ql in (a.q_proj, a.kv_a):
                    entries += [self._repack(ql.w_q).data_ptr(), ql.scales.data_ptr(), ql.zeros.data_ptr()]
                entries += [a.kv_b.w_q.data_ptr(), a.kv_b.scales.data_ptr(), a.kv_b.zeros.data_ptr()]
                entries += [self._repack(a.o_proj.w_q).data_ptr(), a.o_proj.scales.data_ptr(), a.o_proj.zeros.data_ptr()]
            m = b.moe
            entries.append(m.router.weight.data_ptr())
            for qe in (m.gate, m.up, m.down, m.s_gate, m.s_up, m.s_down):
                entries += [self._repack_e(qe.w_q).data_ptr(), qe.scales.data_ptr(), qe.zeros.data_ptr()]
        P = torch.tensor(bases + entries, dtype=torch.int64, device="cuda")
        return P

    def _ensure(self):
        if self._ptr is None:
            self._ptr = self._build_ptrs()
        if self._scratch is None:
            # generous float scratch
            self._scratch = torch.zeros(1200000, dtype=torch.float32, device="cuda")
            self._iscratch = torch.zeros(64, dtype=torch.int32, device="cuda")

    def step(self, hidden, state):
        self._ensure()
        mod = _get_module()
        cfg = self.cfg
        pos = state[3]["c_kv"].shape[0]
        dev = hidden.device
        # grow MLA cache (KV append -- state bookkeeping, not the compute kernel)
        old_ckv = state[3]["c_kv"]
        old_krope = state[3]["k_rope"]
        new_ckv = torch.empty(pos + 1, cfg.kv_lora, dtype=torch.bfloat16, device=dev)
        new_krope = torch.empty(pos + 1, cfg.qk_rope, dtype=torch.bfloat16, device=dev)
        new_ckv[:pos] = old_ckv
        new_krope[:pos] = old_krope

        hin = hidden.contiguous().bfloat16()
        hout = torch.empty(cfg.hidden, dtype=torch.bfloat16, device=dev)

        s = state
        mod.launch_mega(
            hin, hout, self._ptr,
            old_ckv, old_krope, new_ckv, new_krope, pos,
            s[0]["S"], s[1]["S"], s[2]["S"],
            s[0]["cq"], s[0]["ck"], s[0]["cv"],
            s[1]["cq"], s[1]["ck"], s[1]["cv"],
            s[2]["cq"], s[2]["ck"], s[2]["cv"],
            self._scratch, self._iscratch,
        )
        state[3]["c_kv"] = new_ckv
        state[3]["k_rope"] = new_krope
        return hout, state
