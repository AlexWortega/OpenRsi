"""Fused single-launch megakernel for Kimi-Linear W4A16 hybrid decode (batch=1).

The entire per-token forward -- 3 KDA layers + 1 MLA layer, each with its
64-expert MoE FFN, every int4 dequant-GEMV, the short causal conv, the KDA
recurrent-state update, the MLA latent-cache attention (absorb form), both
RMSNorms and the residuals -- runs in ONE cooperative CUDA grid launch. Blocks
persist for the whole step and synchronize between dependent phases with
cg::this_grid().sync(); intermediate activations live in a global scratch arena.

The int4 unpack + per-group asymmetric dequant is fused directly into each GEMV:
weights are streamed once as int4 (never materialized to bf16). AWQ/GPTQ pack
format: w_q (in//2,out) uint8, group-128 scales/zeros (in//128,out) bf16,
w[k,n]=(unpack(w_q)[k,n]-zeros[k//128,n])*scales[k//128,n], accumulated in fp32.

Not imported: any prebuilt quant/model/attention/MoE library, or reference/
baseline. The module tree mirrors reference.py so it loads the reference weights.
"""
from __future__ import annotations

import torch
import torch.nn as nn
from torch.utils.cpp_extension import load_inline

GROUP_SIZE = 128

# --------------------------------------------------------------------------- #
# Module tree: same registered buffer/param names as reference.py so the
# reference state_dict loads. These carry weights only; compute is the kernel.
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
        self.scale = Dk ** -0.5


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
# CUDA megakernel
# --------------------------------------------------------------------------- #
_CUDA_SRC = r"""
#include <cuda_bf16.h>
#include <cooperative_groups.h>
namespace cg = cooperative_groups;

#define D 2304
#define C 4096
#define NH 32
#define DK 128
#define NEXP 64
#define NACT 8
#define INTER 1024
#define KVLORA 512
#define QKNOPE 128
#define QKROPE 64
#define VHEAD 128
#define MLAQ 6144
#define KVAOUT 576
#define KVBOUT 8192
#define NSLOT 38
#define EPS 1e-6f
#define THETA 10000.0f
#define ROUTED_SCALING 2.446f

// scratch offset indices
#define O_HID 0
#define O_XN 1
#define O_QRAW 2
#define O_KRAW 3
#define O_VRAW 4
#define O_GRAW 5
#define O_Q 6
#define O_K 7
#define O_V 8
#define O_BETA 9
#define O_EXPG 10
#define O_O 11
#define O_QOUT 12
#define O_KVA 13
#define O_QROPE 14
#define O_QA 15
#define O_CTX 16
#define O_ROUTER 17
#define O_SELW 18
#define O_HPROD 19
#define O_RED 20
#define O_SCORES 21

typedef const unsigned char* pcu8;
typedef const __nv_bfloat16* pcbf;

__device__ __forceinline__ float bf(const __nv_bfloat16 x){ return __bfloat162float(x); }
__device__ __forceinline__ float sigmoidf(float x){ return 1.0f/(1.0f+__expf(-x)); }
__device__ __forceinline__ float siluf(float x){ return x*sigmoidf(x); }

// warp computes one output col of a fused dequant-GEMV. Weight is TRANSPOSED:
// wT laid out (OUT, IN/2) so a warp reads a column's int4 bytes contiguously
// (coalesced) and splits the reduction across the 32 lanes. x is fp32.
__device__ __forceinline__ float gemv_col_warp(const float* x,int IN,pcu8 wT,
        pcbf scb,pcbf zrb,int OUT,int col,int lane){
    int half=IN>>1;
    const uchar4* wp=(const uchar4*)(wT+(size_t)col*half);
    int nvec=half>>2;                       // bytes/4 (each uchar4 -> 8 k-values)
    float acc=0.f;
    for(int vb=lane; vb<nvec; vb+=32){
        int k=vb<<3;                        // first k covered
        int g=k>>7;
        float scale=bf(scb[g*OUT+col]);
        float zero=bf(zrb[g*OUT+col]);
        uchar4 by=wp[vb];
        acc += scale*( x[k  ]*((float)(by.x&0xF)-zero) + x[k+1]*((float)(by.x>>4)-zero)
                     + x[k+2]*((float)(by.y&0xF)-zero) + x[k+3]*((float)(by.y>>4)-zero)
                     + x[k+4]*((float)(by.z&0xF)-zero) + x[k+5]*((float)(by.z>>4)-zero)
                     + x[k+6]*((float)(by.w&0xF)-zero) + x[k+7]*((float)(by.w>>4)-zero) );
    }
    #pragma unroll
    for(int o=16;o;o>>=1) acc+=__shfl_xor_sync(0xffffffff,acc,o);
    return acc;
}

// full-output warp-per-column GEMV; loads src into shared xs (block) first
__device__ void gemv_all_warp(const float* src,int IN,pcu8 wT,pcbf scb,pcbf zrb,
        int OUT,float* dst,int addb,float* xs,int warpid,int nwarps,int lane){
    for(int i=threadIdx.x;i<IN;i+=blockDim.x) xs[i]=src[i];
    __syncthreads();
    for(int n=warpid;n<OUT;n+=nwarps){
        float v=gemv_col_warp(xs,IN,wT,scb,zrb,OUT,n,lane);
        if(lane==0){ if(addb) dst[n]+=v; else dst[n]=v; }
    }
}

extern "C" __global__ void mega(
    const long* Wptr, const int* off,
    const __nv_bfloat16* hin, __nv_bfloat16* hout,
    float* sc, int* selidx,
    const long* Sp,const long* cqp,const long* ckp,const long* cvp,
    const long* ckvo,const long* ckvn,const long* kro,const long* krn,
    int L)
{
    cg::grid_group grid = cg::this_grid();
    __shared__ float xs[C];
    __shared__ float xg[C/128];
    __shared__ float red[256];
    int gtid = blockIdx.x*blockDim.x + threadIdx.x;
    int T = gridDim.x*blockDim.x;
    int lane = threadIdx.x & 31;
    int warpid = gtid >> 5;
    int nwarps = T >> 5;

    const int HID=off[O_HID], XN=off[O_XN], QRAW=off[O_QRAW], KRAW=off[O_KRAW],
        VRAW=off[O_VRAW], GRAW=off[O_GRAW], Q=off[O_Q], K=off[O_K], V=off[O_V],
        BETA=off[O_BETA], EXPG=off[O_EXPG], OO=off[O_O], QOUT=off[O_QOUT],
        KVA=off[O_KVA], QROPE=off[O_QROPE], QA=off[O_QA], CTX=off[O_CTX],
        ROUTER=off[O_ROUTER], SELW=off[O_SELW], HPROD=off[O_HPROD],
        RED=off[O_RED], SCORES=off[O_SCORES];
    const float scale_kda = rsqrtf((float)DK);
    const float scale_mla = rsqrtf((float)(QKNOPE+QKROPE));

    // init HID from bf16 input
    for(int i=gtid;i<D;i+=T) sc[HID+i]=bf(hin[i]);
    grid.sync();

    for(int layer=0; layer<4; ++layer){
        const long* W = Wptr + layer*NSLOT;
        #define WQL(i) ((pcu8)W[i])
        #define BFL(i) ((pcbf)W[i])

        // ---- rmsnorm(HID, attn_norm) -> XN ----
        if(gtid==0) sc[RED]=0.f; grid.sync();
        { float p=0.f; for(int i=gtid;i<D;i+=T){ float v=sc[HID+i]; p+=v*v; } atomicAdd(&sc[RED],p); }
        grid.sync();
        { float inv=rsqrtf(sc[RED]/(float)D+EPS);
          for(int i=gtid;i<D;i+=T) sc[XN+i]=sc[HID+i]*inv*bf(BFL(0)[i]); }
        grid.sync();

        if(layer<3){
            // ================= KDA =================
            // q/k/v/g projections + beta
            gemv_all_warp(&sc[XN],D,WQL(2),BFL(3),BFL(4),C,&sc[QRAW],0,xs,warpid,nwarps,lane);
            gemv_all_warp(&sc[XN],D,WQL(5),BFL(6),BFL(7),C,&sc[KRAW],0,xs,warpid,nwarps,lane);
            gemv_all_warp(&sc[XN],D,WQL(8),BFL(9),BFL(10),C,&sc[VRAW],0,xs,warpid,nwarps,lane);
            gemv_all_warp(&sc[XN],D,WQL(11),BFL(12),BFL(13),C,&sc[GRAW],0,xs,warpid,nwarps,lane);
            { pcbf bw=BFL(17);
              for(int wn=warpid;wn<NH;wn+=nwarps){ float a=0.f; for(int k=lane;k<D;k+=32) a+=sc[XN+k]*bf(bw[wn*D+k]);
                #pragma unroll
                for(int o=16;o;o>>=1) a+=__shfl_xor_sync(0xffffffff,a,o);
                if(lane==0) sc[BETA+wn]=sigmoidf(a); } }
            grid.sync();

            // short conv (kernel 4) + silu, update conv windows; expg
            { pcbf cw=BFL(18);
              float* cq=(float*)cqp[layer]; float* ck=(float*)ckp[layer]; float* cv=(float*)cvp[layer];
              // cq/ck/cv are bf16 windows (3,C)
              __nv_bfloat16* CQ=(__nv_bfloat16*)cqp[layer];
              __nv_bfloat16* CK=(__nv_bfloat16*)ckp[layer];
              __nv_bfloat16* CV=(__nv_bfloat16*)cvp[layer];
              (void)cq;(void)ck;(void)cv;
              for(int c=gtid;c<C;c+=T){
                  // q (idx0)
                  float w0=bf(cw[0*C*4+c*4+0]),w1=bf(cw[0*C*4+c*4+1]),w2=bf(cw[0*C*4+c*4+2]),w3=bf(cw[0*C*4+c*4+3]);
                  float p0=bf(CQ[0*C+c]),p1=bf(CQ[1*C+c]),p2=bf(CQ[2*C+c]);
                  float cur=sc[QRAW+c];
                  sc[Q+c]=siluf(p0*w0+p1*w1+p2*w2+cur*w3)*scale_kda;
                  CQ[0*C+c]=__float2bfloat16(p1); CQ[1*C+c]=__float2bfloat16(p2); CQ[2*C+c]=__float2bfloat16(cur);
                  // k (idx1)
                  w0=bf(cw[1*C*4+c*4+0]);w1=bf(cw[1*C*4+c*4+1]);w2=bf(cw[1*C*4+c*4+2]);w3=bf(cw[1*C*4+c*4+3]);
                  p0=bf(CK[0*C+c]);p1=bf(CK[1*C+c]);p2=bf(CK[2*C+c]);
                  cur=sc[KRAW+c];
                  sc[K+c]=siluf(p0*w0+p1*w1+p2*w2+cur*w3);
                  CK[0*C+c]=__float2bfloat16(p1); CK[1*C+c]=__float2bfloat16(p2); CK[2*C+c]=__float2bfloat16(cur);
                  // v (idx2)
                  w0=bf(cw[2*C*4+c*4+0]);w1=bf(cw[2*C*4+c*4+1]);w2=bf(cw[2*C*4+c*4+2]);w3=bf(cw[2*C*4+c*4+3]);
                  p0=bf(CV[0*C+c]);p1=bf(CV[1*C+c]);p2=bf(CV[2*C+c]);
                  cur=sc[VRAW+c];
                  sc[V+c]=siluf(p0*w0+p1*w1+p2*w2+cur*w3);
                  CV[0*C+c]=__float2bfloat16(p1); CV[1*C+c]=__float2bfloat16(p2); CV[2*C+c]=__float2bfloat16(cur);
                  // expg = exp(-softplus(g_raw)) = sigmoid(-g_raw)
                  sc[EXPG+c]=sigmoidf(-sc[GRAW+c]);
              }
            }
            grid.sync();

            // per-head gated-delta state update -> O
            { float* S=(float*)Sp[layer];
              for(int t=gtid;t<NH*DK;t+=T){
                  int h=t>>7, dv=t&127;
                  float pred=0.f;
                  for(int dk=0;dk<DK;dk++){
                      float s=S[h*16384+dk*128+dv];
                      pred += s*sc[EXPG+h*128+dk]*sc[K+h*128+dk];
                  }
                  float bv=sc[BETA+h], vv=sc[V+h*128+dv];
                  float oacc=0.f;
                  for(int dk=0;dk<DK;dk++){
                      int idx=h*16384+dk*128+dv;
                      float s=S[idx]*sc[EXPG+h*128+dk];
                      float snew=s + bv*sc[K+h*128+dk]*(vv-pred);
                      S[idx]=snew;
                      oacc += snew*sc[Q+h*128+dk];
                  }
                  sc[OO+t]=oacc;
              }
            }
            grid.sync();
        } else {
            // ================= MLA (absorb) =================
            gemv_all_warp(&sc[XN],D,WQL(2),BFL(3),BFL(4),MLAQ,&sc[QOUT],0,xs,warpid,nwarps,lane);
            gemv_all_warp(&sc[XN],D,WQL(5),BFL(6),BFL(7),KVAOUT,&sc[KVA],0,xs,warpid,nwarps,lane);
            grid.sync();

            // rope + grow caches
            { __nv_bfloat16* CKVN=(__nv_bfloat16*)ckvn[layer];
              const __nv_bfloat16* CKVO=(const __nv_bfloat16*)ckvo[layer];
              __nv_bfloat16* KRN=(__nv_bfloat16*)krn[layer];
              const __nv_bfloat16* KRO=(const __nv_bfloat16*)kro[layer];
              if(CKVN!=CKVO){ for(int idx=gtid; idx<L*KVLORA; idx+=T) CKVN[idx]=CKVO[idx]; }
              for(int r=gtid; r<KVLORA; r+=T) CKVN[L*KVLORA+r]=__float2bfloat16(sc[KVA+r]);
              if(KRN!=KRO){ for(int idx=gtid; idx<L*QKROPE; idx+=T) KRN[idx]=KRO[idx]; }
              int npair = QKROPE/2; // 32
              int total = npair + NH*npair;
              for(int t=gtid; t<total; t+=T){
                  if(t<npair){
                      int i=t;
                      float invf=__expf(-((float)(2*i)/(float)QKROPE)*logf(THETA));
                      float ang=(float)L*invf, cc=cosf(ang), ssn=sinf(ang);
                      float e=sc[KVA+KVLORA+2*i], o=sc[KVA+KVLORA+2*i+1];
                      KRN[L*QKROPE+2*i]=__float2bfloat16(e*cc-o*ssn);
                      KRN[L*QKROPE+2*i+1]=__float2bfloat16(o*cc+e*ssn);
                  } else {
                      int idx=t-npair; int h=idx/npair; int i=idx%npair;
                      float invf=__expf(-((float)(2*i)/(float)QKROPE)*logf(THETA));
                      float ang=(float)L*invf, cc=cosf(ang), ssn=sinf(ang);
                      float e=sc[QOUT+h*192+QKNOPE+2*i], o=sc[QOUT+h*192+QKNOPE+2*i+1];
                      sc[QROPE+h*QKROPE+2*i]=e*cc-o*ssn;
                      sc[QROPE+h*QKROPE+2*i+1]=o*cc+e*ssn;
                  }
              }
            }
            grid.sync();

            int n = L+1;
            // qa[h,r] = sum_d q_nope[h,d]*Wk_dq[r, h*256+d]
            { pcu8 wq=WQL(8); pcbf scb=BFL(9); pcbf zrb=BFL(10);
              for(int t=gtid; t<NH*KVLORA; t+=T){
                  int h=t/KVLORA, r=t%KVLORA;
                  int g=r>>7; int par=r&1; int rowbyte=(r>>1)*KVBOUT;
                  float acc=0.f;
                  for(int d=0; d<QKNOPE; d++){
                      int col=h*256+d;
                      unsigned char b=wq[rowbyte+col];
                      float nib = par?(float)(b>>4):(float)(b&0xF);
                      acc += sc[QOUT+h*192+d]*((nib-bf(zrb[g*KVBOUT+col]))*bf(scb[g*KVBOUT+col]));
                  }
                  sc[QA+h*KVLORA+r]=acc;
              }
            }
            grid.sync();

            // scores[h,l]
            { __nv_bfloat16* CKVN=(__nv_bfloat16*)ckvn[layer];
              __nv_bfloat16* KRN=(__nv_bfloat16*)krn[layer];
              for(int t=gtid; t<NH*n; t+=T){
                  int h=t/n, l=t%n;
                  float dr=0.f;
                  for(int r=0;r<KVLORA;r++) dr += sc[QA+h*KVLORA+r]*bf(CKVN[l*KVLORA+r]);
                  float dp=0.f;
                  for(int d=0;d<QKROPE;d++) dp += sc[QROPE+h*QKROPE+d]*bf(KRN[l*QKROPE+d]);
                  sc[SCORES+h*n+l]=(dr+dp)*scale_mla;
              }
            }
            grid.sync();

            // softmax over l per head (one block per head)
            if(blockIdx.x<NH){
                int h=blockIdx.x; int base=SCORES+h*n; int tid=threadIdx.x, bd=blockDim.x;
                float m=-1e30f;
                for(int i=tid;i<n;i+=bd) m=fmaxf(m,sc[base+i]);
                red[tid]=m; __syncthreads();
                for(int s=bd>>1;s>0;s>>=1){ if(tid<s) red[tid]=fmaxf(red[tid],red[tid+s]); __syncthreads(); }
                m=red[0]; __syncthreads();
                float sum=0.f;
                for(int i=tid;i<n;i+=bd){ float e=__expf(sc[base+i]-m); sc[base+i]=e; sum+=e; }
                red[tid]=sum; __syncthreads();
                for(int s=bd>>1;s>0;s>>=1){ if(tid<s) red[tid]+=red[tid+s]; __syncthreads(); }
                float inv=1.0f/red[0]; __syncthreads();
                for(int i=tid;i<n;i+=bd) sc[base+i]*=inv;
            }
            grid.sync();

            // ctx[h,r] = sum_l p[l,h]*ckv[l,r]
            { __nv_bfloat16* CKVN=(__nv_bfloat16*)ckvn[layer];
              for(int t=gtid; t<NH*KVLORA; t+=T){
                  int h=t/KVLORA, r=t%KVLORA;
                  float acc=0.f;
                  for(int l=0;l<n;l++) acc += sc[SCORES+h*n+l]*bf(CKVN[l*KVLORA+r]);
                  sc[CTX+h*KVLORA+r]=acc;
              }
            }
            grid.sync();

            // o[h,d] = sum_r ctx[h,r]*Wv_dq[r, h*256+128+d]
            { pcu8 wq=WQL(8); pcbf scb=BFL(9); pcbf zrb=BFL(10);
              for(int t=gtid; t<NH*VHEAD; t+=T){
                  int h=t/VHEAD, d=t%VHEAD;
                  int col=h*256+QKNOPE+d;
                  float acc=0.f;
                  for(int r=0;r<KVLORA;r++){
                      int g=r>>7; unsigned char b=wq[(r>>1)*KVBOUT+col];
                      float nib=(r&1)?(float)(b>>4):(float)(b&0xF);
                      acc += sc[CTX+h*KVLORA+r]*((nib-bf(zrb[g*KVBOUT+col]))*bf(scb[g*KVBOUT+col]));
                  }
                  sc[OO+h*VHEAD+d]=acc;
              }
            }
            grid.sync();
        }

        // ---- o_proj: HID += Wo . O ----
        gemv_all_warp(&sc[OO],C,WQL(14),BFL(15),BFL(16),D,&sc[HID],1,xs,warpid,nwarps,lane);
        grid.sync();

        // ================= MoE =================
        // rmsnorm(HID, moe_norm) -> XN
        if(gtid==0) sc[RED]=0.f; grid.sync();
        { float p=0.f; for(int i=gtid;i<D;i+=T){ float v=sc[HID+i]; p+=v*v; } atomicAdd(&sc[RED],p); }
        grid.sync();
        { float inv=rsqrtf(sc[RED]/(float)D+EPS);
          for(int i=gtid;i<D;i+=T) sc[XN+i]=sc[HID+i]*inv*bf(BFL(1)[i]); }
        grid.sync();

        // router logits (warp per expert)
        { pcbf rw=BFL(19);
          for(int e=warpid;e<NEXP;e+=nwarps){ float a=0.f; for(int k=lane;k<D;k+=32) a+=sc[XN+k]*bf(rw[e*D+k]);
            #pragma unroll
            for(int o=16;o;o>>=1) a+=__shfl_xor_sync(0xffffffff,a,o);
            if(lane==0) sc[ROUTER+e]=a; } }
        grid.sync();
        // softmax + top-8 (single thread)
        if(gtid==0){
            float mx=-1e30f; for(int e=0;e<NEXP;e++) mx=fmaxf(mx,sc[ROUTER+e]);
            float pr[NEXP]; float s=0.f;
            for(int e=0;e<NEXP;e++){ pr[e]=__expf(sc[ROUTER+e]-mx); s+=pr[e]; }
            for(int e=0;e<NEXP;e++) pr[e]/=s;
            bool used[NEXP]; for(int e=0;e<NEXP;e++) used[e]=false;
            float wsum=0.f;
            for(int j=0;j<NACT;j++){
                int bi=-1; float bv=-1e30f;
                for(int e=0;e<NEXP;e++){ if(!used[e] && pr[e]>bv){ bv=pr[e]; bi=e; } }
                used[bi]=true; selidx[j]=bi; sc[SELW+j]=pr[bi]; wsum+=pr[bi];
            }
            float invn = ROUTED_SCALING/(wsum+1e-9f);
            for(int j=0;j<NACT;j++) sc[SELW+j]*=invn;
        }
        grid.sync();

        // gate/up for 8 routed + 1 shared -> hprod[slot,m] (warp per (slot,col))
        { for(int i=threadIdx.x;i<D;i+=blockDim.x) xs[i]=sc[XN+i];
          __syncthreads();
          int totw = 9*INTER;
          for(int wt=warpid; wt<totw; wt+=nwarps){
              int slot=wt/INTER, m=wt%INTER;
              pcu8 gwq,uwq; pcbf gsc,gzr,usc,uzr;
              if(slot<NACT){
                  int e=selidx[slot];
                  gwq=WQL(20)+(size_t)e*1152*INTER; gsc=BFL(21)+(size_t)e*18*INTER; gzr=BFL(22)+(size_t)e*18*INTER;
                  uwq=WQL(23)+(size_t)e*1152*INTER; usc=BFL(24)+(size_t)e*18*INTER; uzr=BFL(25)+(size_t)e*18*INTER;
              } else {
                  gwq=WQL(29); gsc=BFL(30); gzr=BFL(31);
                  uwq=WQL(32); usc=BFL(33); uzr=BFL(34);
              }
              float go=gemv_col_warp(xs,D,gwq,gsc,gzr,INTER,m,lane);
              float uo=gemv_col_warp(xs,D,uwq,usc,uzr,INTER,m,lane);
              if(lane==0) sc[HPROD+slot*INTER+m]=siluf(go)*uo;
          }
        }
        grid.sync();

        // down -> HID (residual add, weighted) (warp per (slot,col))
        { int totw=9*D;
          for(int wt=warpid; wt<totw; wt+=nwarps){
              int slot=wt/D, d=wt%D;
              pcu8 dwq; pcbf dsc,dzr; float wgt;
              if(slot<NACT){
                  int e=selidx[slot];
                  dwq=WQL(26)+(size_t)e*512*D; dsc=BFL(27)+(size_t)e*8*D; dzr=BFL(28)+(size_t)e*8*D;
                  wgt=sc[SELW+slot];
              } else {
                  dwq=WQL(35); dsc=BFL(36); dzr=BFL(37); wgt=1.0f;
              }
              float o=gemv_col_warp(&sc[HPROD+slot*INTER],INTER,dwq,dsc,dzr,D,d,lane);
              if(lane==0) atomicAdd(&sc[HID+d], wgt*o);
          }
        }
        grid.sync();
        #undef WQL
        #undef BFL
    }

    for(int i=gtid;i<D;i+=T) hout[i]=__float2bfloat16(sc[HID+i]);
}

#include <c10/cuda/CUDAStream.h>

void mega_launch(
    torch::Tensor Wptr, torch::Tensor off, torch::Tensor hin, torch::Tensor hout,
    torch::Tensor scratch, torch::Tensor selidx,
    torch::Tensor Sp, torch::Tensor cqp, torch::Tensor ckp, torch::Tensor cvp,
    torch::Tensor ckvo, torch::Tensor ckvn, torch::Tensor kro, torch::Tensor krn,
    int64_t L)
{
    const long* Wp=(const long*)Wptr.data_ptr<int64_t>();
    const int* offp=(const int*)off.data_ptr<int32_t>();
    const __nv_bfloat16* hinp=(const __nv_bfloat16*)hin.data_ptr();
    __nv_bfloat16* houtp=(__nv_bfloat16*)hout.data_ptr();
    float* scr=(float*)scratch.data_ptr<float>();
    int* sel=(int*)selidx.data_ptr<int32_t>();
    const long* Spp=(const long*)Sp.data_ptr<int64_t>();
    const long* cqpp=(const long*)cqp.data_ptr<int64_t>();
    const long* ckpp=(const long*)ckp.data_ptr<int64_t>();
    const long* cvpp=(const long*)cvp.data_ptr<int64_t>();
    const long* ckvop=(const long*)ckvo.data_ptr<int64_t>();
    const long* ckvnp=(const long*)ckvn.data_ptr<int64_t>();
    const long* krop=(const long*)kro.data_ptr<int64_t>();
    const long* krnp=(const long*)krn.data_ptr<int64_t>();
    int Li=(int)L;

    void* args[]={&Wp,&offp,&hinp,&houtp,&scr,&sel,&Spp,&cqpp,&ckpp,&cvpp,
                  &ckvop,&ckvnp,&krop,&krnp,&Li};
    int threads=256, nb=0;
    cudaOccupancyMaxActiveBlocksPerMultiprocessor(&nb,(void*)mega,threads,0);
    int dev; cudaGetDevice(&dev);
    cudaDeviceProp pr; cudaGetDeviceProperties(&pr,dev);
    int grid=nb*pr.multiProcessorCount;
    cudaLaunchCooperativeKernel((void*)mega,dim3(grid),dim3(threads),args,0,
                                at::cuda::getCurrentCUDAStream());
}
"""

_CPP_SRC = r"""
#include <torch/extension.h>
void mega_launch(
    torch::Tensor Wptr, torch::Tensor off, torch::Tensor hin, torch::Tensor hout,
    torch::Tensor scratch, torch::Tensor selidx,
    torch::Tensor Sp, torch::Tensor cqp, torch::Tensor ckp, torch::Tensor cvp,
    torch::Tensor ckvo, torch::Tensor ckvn, torch::Tensor kro, torch::Tensor krn,
    int64_t L);
"""

_MOD = None


def _get_mod():
    global _MOD
    if _MOD is None:
        _MOD = load_inline(
            name="kimi_mega",
            cpp_sources=[_CPP_SRC],
            cuda_sources=[_CUDA_SRC],
            functions=["mega_launch"],
            extra_cuda_cflags=["-O3", "--use_fast_math",
                               "-gencode=arch=compute_120,code=sm_120"],
            with_cuda=True,
            verbose=False,
        )
    return _MOD


# offsets (in floats) into the scratch arena
_SIZES = [
    ("HID", 2304), ("XN", 4096), ("QRAW", 4096), ("KRAW", 4096), ("VRAW", 4096),
    ("GRAW", 4096), ("Q", 4096), ("K", 4096), ("V", 4096), ("BETA", 32),
    ("EXPG", 4096), ("O", 4096), ("QOUT", 6144), ("KVA", 576), ("QROPE", 2048),
    ("QA", 16384), ("CTX", 16384), ("ROUTER", 64), ("SELW", 8), ("HPROD", 9216),
    ("RED", 64),
]


def _offsets():
    offs = []
    cur = 0
    for _, sz in _SIZES:
        offs.append(cur)
        cur += sz
    offs.append(cur)  # SCORES offset
    return offs, cur


_OFFS, _SCORES_OFF = _offsets()


class Model(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.blocks = nn.ModuleList(Block(cfg, k) for k in cfg.pattern)
        self._built = False

    def _build(self):
        self._ext = _get_mod()
        dev = self.blocks[0].attn_norm.device
        NSLOT = 38
        ptrs = torch.zeros(4 * NSLOT, dtype=torch.int64)
        self._keep = []  # keep transposed-weight tensors alive

        def P(layer, slot, t):
            ptrs[layer * NSLOT + slot] = t.data_ptr()

        def T2(t):  # transpose (in//2, out) -> (out, in//2), contiguous
            tt = t.t().contiguous()
            self._keep.append(tt)
            return tt

        def T3(t):  # transpose (n, in//2, out) -> (n, out, in//2)
            tt = t.transpose(1, 2).contiguous()
            self._keep.append(tt)
            return tt

        for i, blk in enumerate(self.blocks):
            P(i, 0, blk.attn_norm)
            P(i, 1, blk.moe_norm)
            a = blk.attn
            if blk.kind == "K":
                for j, ql in enumerate((a.q_proj, a.k_proj, a.v_proj, a.g_proj)):
                    P(i, 2 + 3 * j, T2(ql.w_q)); P(i, 3 + 3 * j, ql.scales); P(i, 4 + 3 * j, ql.zeros)
                P(i, 17, a.beta_proj.weight)
                P(i, 18, a.conv_w)
            else:
                P(i, 2, T2(a.q_proj.w_q)); P(i, 3, a.q_proj.scales); P(i, 4, a.q_proj.zeros)
                P(i, 5, T2(a.kv_a.w_q)); P(i, 6, a.kv_a.scales); P(i, 7, a.kv_a.zeros)
                # kv_b stays in original (in//2,out) layout for absorb loops
                P(i, 8, a.kv_b.w_q); P(i, 9, a.kv_b.scales); P(i, 10, a.kv_b.zeros)
            P(i, 14, T2(a.o_proj.w_q)); P(i, 15, a.o_proj.scales); P(i, 16, a.o_proj.zeros)
            mo = blk.moe
            P(i, 19, mo.router.weight)
            for base, qe in ((20, mo.gate), (23, mo.up), (26, mo.down),
                             (29, mo.s_gate), (32, mo.s_up), (35, mo.s_down)):
                P(i, base, T3(qe.w_q)); P(i, base + 1, qe.scales); P(i, base + 2, qe.zeros)

        self._Wptr = ptrs.to(dev)
        self._off = torch.tensor(_OFFS, dtype=torch.int32, device=dev)
        self._selidx = torch.zeros(8, dtype=torch.int32, device=dev)
        self._built = True

    def _setup_state(self, state, dev):
        """One-time per-trajectory: pin KDA pointers, preallocate a growable MLA
        cache buffer, and build a single device pointer table. Detects a fresh
        trajectory by identity of the KDA S tensor."""
        cfg = self.cfg
        mla_i = cfg.pattern.index("M")
        st = state[mla_i]
        L0 = int(st["c_kv"].shape[0])
        cap = L0 + 4096  # room to grow during a timed sweep
        buf_ckv = torch.empty(cap, cfg.kv_lora, dtype=torch.bfloat16, device=dev)
        buf_kr = torch.empty(cap, cfg.qk_rope, dtype=torch.bfloat16, device=dev)
        buf_ckv[:L0].copy_(st["c_kv"]); buf_kr[:L0].copy_(st["k_rope"])
        st["c_kv"] = buf_ckv[:L0]; st["k_rope"] = buf_kr[:L0]
        self._mla_i = mla_i
        self._buf_ckv = buf_ckv; self._buf_kr = buf_kr
        self._cap = cap

        # host pointer table: [Sp(4) cqp ckp cvp ckvo ckvn kro krn] = 32 int64.
        # MLA cache buffers slice from index 0, so old/new share a constant
        # base data_ptr across steps -> set once, no per-step H2D.
        pt = torch.zeros(32, dtype=torch.int64)
        for i, blk in enumerate(self.blocks):
            s = state[i]
            if blk.kind == "K":
                s["S"] = s["S"].contiguous()
                s["cq"] = s["cq"].contiguous(); s["ck"] = s["ck"].contiguous(); s["cv"] = s["cv"].contiguous()
                pt[i] = s["S"].data_ptr()
                pt[4 + i] = s["cq"].data_ptr(); pt[8 + i] = s["ck"].data_ptr(); pt[12 + i] = s["cv"].data_ptr()
        base_ckv = buf_ckv.data_ptr(); base_kr = buf_kr.data_ptr()
        pt[16 + mla_i] = base_ckv; pt[20 + mla_i] = base_ckv
        pt[24 + mla_i] = base_kr; pt[28 + mla_i] = base_kr
        self._pt_host = pt
        self._pt_dev = pt.to(dev)
        self._state_key = state[0]["S"].data_ptr()
        # preallocated scratch sized for capacity, reused every step
        self._scratch = torch.empty(_SCORES_OFF + cfg.mla_heads * (cap), dtype=torch.float32, device=dev)
        self._hout = torch.empty(cfg.hidden, dtype=torch.bfloat16, device=dev)

    def step(self, hidden, state):
        if not self._built:
            self._build()
        cfg = self.cfg
        dev = hidden.device
        mla_i = getattr(self, "_mla_i", cfg.pattern.index("M"))
        if (not hasattr(self, "_state_key")) or state[0]["S"].data_ptr() != self._state_key \
           or state[mla_i]["c_kv"].data_ptr() != self._buf_ckv.data_ptr():
            self._setup_state(state, dev)
            mla_i = self._mla_i

        st = state[mla_i]
        L = int(st["c_kv"].shape[0])
        if L + 1 > self._cap:  # grow
            self._setup_state(state, dev); st = state[mla_i]; L = int(st["c_kv"].shape[0])

        hidden = hidden.contiguous().to(torch.bfloat16)
        hout = self._hout
        scratch = self._scratch

        new_ckv = self._buf_ckv[:L + 1]
        new_kr = self._buf_kr[:L + 1]
        # in-place append: old and new share storage, so the kernel's copy loop
        # is a no-op (skipped because ptrs equal) -- kernel only writes row L.
        pt = self._pt_dev
        self._ext.mega_launch(
            self._Wptr, self._off, hidden, hout, scratch, self._selidx,
            pt[0:4], pt[4:8], pt[8:12], pt[12:16],
            pt[16:20], pt[20:24], pt[24:28], pt[28:32], L)

        st["c_kv"] = new_ckv
        st["k_rope"] = new_kr
        return hout, state
