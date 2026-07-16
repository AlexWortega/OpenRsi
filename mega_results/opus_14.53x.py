"""Fused single-launch megakernel for Kimi-Linear W4A16 hybrid decode (batch=1).

The whole per-token forward -- 3 KDA layers + 1 MLA layer, each with a 64-expert
MoE FFN, every int4 dequant-GEMV, the short causal conv, the KDA recurrent-state
update, the MLA latent-cache attention (absorbed), the MoE router/topk/experts,
both RMSNorms and the residual adds -- runs inside ONE cooperative CUDA kernel
launched exactly once per step(). Grid-wide barriers (cooperative_groups
grid.sync) sequence the fused phases; the int4 weights are streamed once and
dequantized on the fly (never materialized to bf16).

Layout / math match reference.py exactly (buffer names identical so the
reference weights load). The only algebraic change is the MLA "absorb": instead
of recomputing K/V for every past token each step, q_nope is absorbed through
the kv_b nope weight so scores are formed directly against the 512-d latent
cache, and the output is projected back through the kv_b value weight.

Perf notes (what makes this fast beyond the fused dequant-GEMV): profiling showed
the single-launch cooperative kernel is dominated by (1) grid.sync barrier count
(each ~0.6us fixed + phase-straggler serialization across 188 blocks) and (2)
single-wave, latency-bound weight GEMVs. So the hot path was tuned by
  - collapsing barriers: fold every zero-init into the preceding phase, compute
    the MoE softmax+topk redundantly per-block into shared (no grid barrier),
    run MLA rope in the same phase as qc (independent), fold the MLA PC-zero into
    the softmax barrier -- 50 -> ~39 dynamic barriers/step;
  - K-splitting the most under-subscribed GEMV (MoE down) across two threads so
    it runs ~2 waves and hides DRAM latency;
  - head-major SCO so the MLA softmax / pc reads are coalesced;
  - dropping the MLA scores per-token shared staging (read ckv directly,
    coalesced across the 16-thread head group -- no per-token __syncthreads);
  - staging pc[h,:] / q_nope[h,:] in shared for the block-per-head qc and o
    projections so the kv_b stream is reused.
"""
from __future__ import annotations

import torch
import torch.nn as nn
from torch.utils.cpp_extension import load_inline

GROUP = 128

# --------------------------------------------------------------------------- #
# module skeleton: identical buffer/param names to reference so load works
# --------------------------------------------------------------------------- #
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
# CUDA megakernel
# --------------------------------------------------------------------------- #
_CUDA_SRC = r'''
#include <torch/extension.h>
#include <cuda_runtime.h>
#include <cuda_bf16.h>
#include <cooperative_groups.h>
#include <math.h>
namespace cg = cooperative_groups;

#define HID 2304
#define KH 32
#define KD 128
#define CDIM 4096
#define SCV 4
#define MH 32
#define KVL 512
#define QN 128
#define QR 64
#define VH 128
#define NE 64
#define NA 8
#define MINT 1024
#define KDA_SCALE 0.08838834764831845f
#define MLA_SCALE 0.07216878364870322f
#define ROUTED_SCALING 2.446f
#define EPSN 1.0e-6f

// workspace float offsets
#define O_XRES   0
#define O_XN     (O_XRES+HID)
#define O_Q      (O_XN+HID)
#define O_K      (O_Q+CDIM)
#define O_V      (O_K+CDIM)
#define O_G      (O_V+CDIM)
#define O_O      (O_G+CDIM)
#define O_ATTN   (O_O+CDIM)
#define O_MQ     (O_ATTN+HID)
#define O_KVA    (O_MQ+(MH*(QN+QR)))
#define O_QC     (O_KVA+(KVL+QR))
#define O_PC     (O_QC+(MH*KVL))
#define O_KRNEW  (O_PC+(MH*KVL))
#define O_RLOG   (O_KRNEW+QR)
#define O_PROB   (O_RLOG+NE)
#define O_HEXP   (O_PROB+NE)
#define O_OEXP   (O_HEXP+((NA+1)*MINT))
#define O_MOUT   (O_OEXP+((NA+1)*HID))
#define O_WSEL   (O_MOUT+HID)
#define O_SCORES (O_WSEL+16)

typedef const unsigned char* pu8;
typedef const __nv_bfloat16* pbf;

// ---- block reductions (use static shared) ----
__device__ __forceinline__ float warpSum(float v){
  for(int o=16;o>0;o>>=1) v+=__shfl_down_sync(0xffffffff,v,o); return v;
}
__device__ __forceinline__ float warpMax(float v){
  for(int o=16;o>0;o>>=1) v=fmaxf(v,__shfl_down_sync(0xffffffff,v,o)); return v;
}
__device__ float blockSum(float v, float* sm, int tid, int bs){
  v=warpSum(v); int w=tid>>5, l=tid&31; if(l==0) sm[w]=v; __syncthreads();
  int nw=(bs+31)>>5; v=(tid<nw)?sm[tid]:0.f;
  if(w==0){ v=warpSum(v); if(l==0) sm[0]=v; } __syncthreads();
  float r=sm[0]; __syncthreads(); return r;
}
__device__ float blockMax(float v, float* sm, int tid, int bs){
  v=warpMax(v); int w=tid>>5, l=tid&31; if(l==0) sm[w]=v; __syncthreads();
  int nw=(bs+31)>>5; v=(tid<nw)?sm[tid]:-1e30f;
  if(w==0){ v=warpMax(v); if(l==0) sm[0]=v; } __syncthreads();
  float r=sm[0]; __syncthreads(); return r;
}

// Fused dequant-GEMV distributed over the WHOLE grid as (group, col) units so
// every SM stays busy even when N is small. Each thread streams one int4 weight
// column-group (64 packed bytes = 128 rows), dequantizes on the fly (never
// materializing the bf16 weight), and atomicAdds its partial dot into out[col]
// (out[] must be pre-zeroed, or pre-seeded for residual-accumulate paths). Four
// independent accumulators break the FMA dependency chain (latency hiding).
// Adjacent threads own adjacent columns, so the byte reads coalesce across a warp.
__device__ __forceinline__ void gemv_atomic(pu8 wq, pbf sc, pbf zr, const float* xs,
                                            float* out, int K, int N, int gt, int gT){
  int NG=K>>7;
  long tot=(long)N*NG;
  for(long idx=gt; idx<tot; idx+=gT){
    int col=idx%N; int g=idx/N;
    float s=__bfloat162float(sc[g*N+col]);
    float z=__bfloat162float(zr[g*N+col]);
    float d0=0,d1=0,d2=0,d3=0, xsum=0.f;
    int base=(g*64)*N + col;
    #pragma unroll 8
    for(int t=0;t<64;t+=4){
      unsigned char b0=wq[base+(t+0)*N], b1=wq[base+(t+1)*N], b2=wq[base+(t+2)*N], b3=wq[base+(t+3)*N];
      int k=g*128+2*t;
      float x0=xs[k],x1=xs[k+1],x2=xs[k+2],x3=xs[k+3],x4=xs[k+4],x5=xs[k+5],x6=xs[k+6],x7=xs[k+7];
      d0 += x0*(float)(b0&0xF)+x1*(float)(b0>>4);
      d1 += x2*(float)(b1&0xF)+x3*(float)(b1>>4);
      d2 += x4*(float)(b2&0xF)+x5*(float)(b2>>4);
      d3 += x6*(float)(b3&0xF)+x7*(float)(b3>>4);
      xsum += x0+x1+x2+x3+x4+x5+x6+x7;
    }
    atomicAdd(&out[col], s*((d0+d1+d2+d3) - z*xsum));
  }
}

// dequant single weight element W[i,col]
__device__ __forceinline__ float dqe(pu8 wq, pbf sc, pbf zr, int i, int col, int N){
  unsigned char b=wq[(i>>1)*N+col];
  float nib=(i&1)?(float)(b>>4):(float)(b&0xF);
  int g=i>>7;
  return (nib-__bfloat162float(zr[g*N+col]))*__bfloat162float(sc[g*N+col]);
}

extern __shared__ float smem[];   // dynamic shared (holds x / activations)

// ptr tables (int64 device arrays)
//  qw[19*3]: quant linears (b0:q,k,v,g,o; b1..; b2..; b3:q,kv_a,kv_b,o) -> wq,sc,zr
//  eb[4*6*3]: expert banks per block (gate,up,down,sgate,sup,sdown) base wq,sc,zr
//  sw[4*3]: attn_norm, moe_norm, router.weight
//  ksw[3*2]: KDA beta.weight, conv_w (blocks 0,1,2)
//  stp: state ptrs; KDA blocks -> S,cq,ck,cv ; MLA -> c_kv,k_rope
__global__ void __launch_bounds__(512,1) mega(
    const long* qw, const long* eb, const long* sw, const long* ksw, const long* stp,
    float* work, const __nv_bfloat16* hin, __nv_bfloat16* hout,
    int L, int* isel)
{
  cg::grid_group grid = cg::this_grid();
  int tid=threadIdx.x, bs=blockDim.x, bid=blockIdx.x, nb=gridDim.x;
  int gt=bid*bs+tid, gT=nb*bs;
  __shared__ float rsm[64];
  __shared__ int sisel[NA]; __shared__ float swsel[NA];   // per-block topk (redundant, saves a barrier)

  float* XRES=work+O_XRES; float* XN=work+O_XN;

  // load hidden -> XRES (fp32)
  for(int i=gt;i<HID;i+=gT) XRES[i]=__bfloat162float(hin[i]);
  grid.sync();

  int Lp = L+1;                 // MLA cache length incl new token
  int qi=0, ei=0, si=0, ki=0;   // running indices into ptr tables

  for(int b=0;b<4;b++){
    bool isK = (b<3);
    // ---- attn RMSNorm: XN = rmsnorm(XRES, attn_norm) ----
    {
      pbf wn=(pbf)sw[si*3+0];
      float loc=0.f; for(int i=tid;i<HID;i+=bs){ float v=XRES[i]; loc+=v*v; }
      float ss=blockSum(loc,rsm,tid,bs);
      float inv=rsqrtf(ss/HID+EPSN);
      for(int i=gt;i<HID;i+=gT) XN[i]=XRES[i]*inv*__bfloat162float(wn[i]);
      // fold the attn-gemv atomic-target zeroing into this phase (they aren't read
      // until the gemv, one barrier later) -> removes the dedicated zero barrier.
      if(isK){ float* Q=work+O_Q; for(int n=gt;n<4*CDIM;n+=gT) Q[n]=0.f; }   // Q,K,V,G contiguous
      else { for(int n=gt;n<MH*(QN+QR);n+=gT) (work+O_MQ)[n]=0.f; for(int n=gt;n<KVL+QR;n+=gT) (work+O_KVA)[n]=0.f; }
    }
    grid.sync();

    if(isK){
      // ===================== KDA =====================
      float* Q=work+O_Q; float* Kk=work+O_K; float* Vv=work+O_V; float* Gg=work+O_G;
      pu8 qwq=(pu8)qw[(qi+0)*3+0]; pbf qsc=(pbf)qw[(qi+0)*3+1]; pbf qzr=(pbf)qw[(qi+0)*3+2];
      pu8 kwq=(pu8)qw[(qi+1)*3+0]; pbf ksc=(pbf)qw[(qi+1)*3+1]; pbf kzr=(pbf)qw[(qi+1)*3+2];
      pu8 vwq=(pu8)qw[(qi+2)*3+0]; pbf vsc=(pbf)qw[(qi+2)*3+1]; pbf vzr=(pbf)qw[(qi+2)*3+2];
      pu8 gwq=(pu8)qw[(qi+3)*3+0]; pbf gsc=(pbf)qw[(qi+3)*3+1]; pbf gzr=(pbf)qw[(qi+3)*3+2];
      // 4 GEMVs batched into one grid stride, uint32-vectorized (4 cols/thread).
      { int NG=HID>>7; int N4=CDIM>>2; long tot=(long)N4*NG; int Nw=CDIM>>2;
        for(long id=gt; id<4*tot; id+=gT){
          int which=id/tot; long j=id%tot; int c4=j%N4; int g=j/N4; int col=c4<<2;
          pu8 wq; pbf sc,zr; float* out;
          if(which==0){wq=qwq;sc=qsc;zr=qzr;out=Q;} else if(which==1){wq=kwq;sc=ksc;zr=kzr;out=Kk;}
          else if(which==2){wq=vwq;sc=vsc;zr=vzr;out=Vv;} else {wq=gwq;sc=gsc;zr=gzr;out=Gg;}
          const unsigned int* w32=(const unsigned int*)(wq+(g*64)*CDIM+col);
          float d0=0,d1=0,d2=0,d3=0,xsum=0.f;
          #pragma unroll 8
          for(int t=0;t<64;t++){ unsigned int b=w32[t*Nw]; int k=g*128+2*t; float x0=XN[k],x1=XN[k+1]; xsum+=x0+x1;
            d0+=x0*(float)(b&0xF)+x1*(float)((b>>4)&0xF); d1+=x0*(float)((b>>8)&0xF)+x1*(float)((b>>12)&0xF);
            d2+=x0*(float)((b>>16)&0xF)+x1*(float)((b>>20)&0xF); d3+=x0*(float)((b>>24)&0xF)+x1*(float)((b>>28)&0xF); }
          const __nv_bfloat16* scg=sc+g*CDIM+col; const __nv_bfloat16* zrg=zr+g*CDIM+col;
          atomicAdd(&out[col+0],__bfloat162float(scg[0])*(d0-__bfloat162float(zrg[0])*xsum));
          atomicAdd(&out[col+1],__bfloat162float(scg[1])*(d1-__bfloat162float(zrg[1])*xsum));
          atomicAdd(&out[col+2],__bfloat162float(scg[2])*(d2-__bfloat162float(zrg[2])*xsum));
          atomicAdd(&out[col+3],__bfloat162float(scg[3])*(d3-__bfloat162float(zrg[3])*xsum));
        }
      }
      grid.sync();
      // ---- short conv (q,k,v) with silu + state update; beta ----
      pbf convw=(pbf)ksw[ki*2+1];           // (3, CDIM, 4)
      long* Sst=(long*)0;
      float* Sp =(float*)stp[b*4+0];
      __nv_bfloat16* cq=(__nv_bfloat16*)stp[b*4+1];
      __nv_bfloat16* ck=(__nv_bfloat16*)stp[b*4+2];
      __nv_bfloat16* cv=(__nv_bfloat16*)stp[b*4+3];
      // conv over 3*CDIM channels
      for(int idx=gt; idx<3*CDIM; idx+=gT){
        int which=idx/CDIM, c=idx%CDIM;
        float* valbuf = (which==0)?Q:((which==1)?Kk:Vv);
        __nv_bfloat16* st = (which==0)?cq:((which==1)?ck:cv);
        float p0=__bfloat162float(st[0*CDIM+c]);
        float p1=__bfloat162float(st[1*CDIM+c]);
        float p2=__bfloat162float(st[2*CDIM+c]);
        float val=valbuf[c];
        const __nv_bfloat16* wc=convw + which*CDIM*SCV + c*SCV;
        float o = p0*__bfloat162float(wc[0]) + p1*__bfloat162float(wc[1])
                + p2*__bfloat162float(wc[2]) + val*__bfloat162float(wc[3]);
        float so = o/(1.f+expf(-o));      // silu
        valbuf[c]=so;
        // update conv window: [p1,p2,val]
        st[0*CDIM+c]=st[1*CDIM+c]; st[1*CDIM+c]=st[2*CDIM+c]; st[2*CDIM+c]=__float2bfloat16(val);
      }
      // beta_proj (bf16 dense, (KH,HID)): WARP-PER-HEAD, no atomics. Global warp
      // `gw` owns head gw (KH=32 heads); its 32 lanes split the 2304-dim dot and
      // warp-reduce; lane 0 writes sigmoid. Tiny (32*2304), fills 32 warps.
      pbf betaw=(pbf)ksw[ki*2+0];          // (KH, HID)
      float* betabuf = work+O_KVA;         // temp (KH<=32)
      { int gw=gt>>5, lane=tid&31;
        if(gw<KH){ const __nv_bfloat16* wr=betaw+gw*HID;
          float acc=0.f;
          for(int k=lane;k<HID;k+=32) acc+=XN[k]*__bfloat162float(wr[k]);
          #pragma unroll
          for(int o=16;o>0;o>>=1) acc+=__shfl_down_sync(0xffffffff,acc,o);
          if(lane==0) betabuf[gw]=1.f/(1.f+expf(-acc));
        }
      }
      grid.sync();
      // ---- recurrence: one head per block ----
      float* Ob=work+O_O;
      for(int h=bid; h<KH; h+=nb){
        // load per-head vectors into shared
        float* eg=smem;         // KD
        float* kh=smem+KD;      // KD
        float* qh=smem+2*KD;    // KD (already *scale)
        float* vh=smem+3*KD;    // KD
        for(int d=tid; d<KD; d+=bs){
          float gg=Gg[h*KD+d];
          float sp=logf(1.f+expf(gg)); // softplus
          eg[d]=expf(-sp);
          kh[d]=Kk[h*KD+d];
          qh[d]=Q[h*KD+d]*KDA_SCALE;
          vh[d]=Vv[h*KD+d];
        }
        __syncthreads();
        float beta=betabuf[h];
        float* Sh=Sp + h*KD*KD;   // [dk,dv]
        // Use all 512 threads: 4 sub-threads per dv column split the 128-dk work.
        // Each sub computes a partial pred over its dk-range; the 4 partials are
        // combined via shared, then all 4 update their own S rows + accumulate o.
        float* psh=smem+4*KD;      // 4*KD scratch for pred partials
        int dv=tid&127, sub=tid>>7;      // sub in 0..3
        int dk0=sub*32, dk1=dk0+32;
        float pp=0.f;
        for(int dk=dk0;dk<dk1;dk++) pp += Sh[dk*KD+dv]*eg[dk]*kh[dk];
        psh[sub*KD+dv]=pp; __syncthreads();
        float pred=psh[dv]+psh[KD+dv]+psh[2*KD+dv]+psh[3*KD+dv];
        float vmp=vh[dv]-pred;
        float op=0.f;
        for(int dk=dk0;dk<dk1;dk++){
          float ns=Sh[dk*KD+dv]*eg[dk] + beta*kh[dk]*vmp;
          Sh[dk*KD+dv]=ns; op += ns*qh[dk];
        }
        psh[sub*KD+dv]=op; __syncthreads();
        if(sub==0) Ob[h*KD+dv]=psh[dv]+psh[KD+dv]+psh[2*KD+dv]+psh[3*KD+dv];
        __syncthreads();
      }
      grid.sync();
      // ---- o_proj + residual (K-split atomic into XRES) ----
      pu8 owq=(pu8)qw[(qi+4)*3+0]; pbf osc=(pbf)qw[(qi+4)*3+1]; pbf ozr=(pbf)qw[(qi+4)*3+2];
      gemv_atomic(owq,osc,ozr,work+O_O,XRES,CDIM,HID,gt,gT);
      grid.sync();
      qi+=5; ki+=1;
    } else {
      // ===================== MLA =====================
      float* MQ=work+O_MQ; float* KVA=work+O_KVA; float* QC=work+O_QC;
      float* PC=work+O_PC; float* KRN=work+O_KRNEW; float* SCO=work+O_SCORES;
      pu8 qwq=(pu8)qw[(qi+0)*3+0]; pbf qsc=(pbf)qw[(qi+0)*3+1]; pbf qzr=(pbf)qw[(qi+0)*3+2];
      pu8 awq=(pu8)qw[(qi+1)*3+0]; pbf asc=(pbf)qw[(qi+1)*3+1]; pbf azr=(pbf)qw[(qi+1)*3+2];
      int MQD=MH*(QN+QR); int KVAD=KVL+QR;   // MQ/KVA zeroed in attn-RMSNorm phase
      gemv_atomic(qwq,qsc,qzr,XN,MQ,HID,MQD,gt,gT);
      gemv_atomic(awq,asc,azr,XN,KVA,HID,KVAD,gt,gT);
      grid.sync();
      // ---- rope on q_rope (per head) and k_rope_new; cos/sin computed IN-KERNEL
      //      for pos=L (theta=10000): inv=theta^(-2j/QR), ang=L*inv. No host op.
      // q layout: head h -> MQ[h*192 + (0..127 nope, 128..191 rope)]
      for(int idx=gt; idx<MH*QR/2; idx+=gT){
        int h=idx/(QR/2), j=idx%(QR/2);
        float inv=__powf(10000.0f, -(2.0f*j)/(float)QR); float ang=(float)L*inv;
        float c=cosf(ang), s=sinf(ang);
        int base=h*(QN+QR)+QN;
        float e=MQ[base+2*j], o=MQ[base+2*j+1];
        MQ[base+2*j]=e*c-o*s; MQ[base+2*j+1]=o*c+e*s;
      }
      // k_rope_new: KVA[512 + 0..63]
      for(int j=gt;j<QR/2;j+=gT){
        float inv=__powf(10000.0f, -(2.0f*j)/(float)QR); float ang=(float)L*inv;
        float c=cosf(ang), s=sinf(ang);
        float e=KVA[KVL+2*j], o=KVA[KVL+2*j+1];
        KRN[2*j]=e*c-o*s; KRN[2*j+1]=o*c+e*s;
      }
      // ---- qc[h,i] = sum_d Wk[i,h*256+d] * q_nope[h,d] ---- (qc reads only
      // q_nope, independent of the rope above -> no barrier between; the single
      // barrier below covers both before scores).
      pu8 bwq=(pu8)qw[(qi+2)*3+0]; pbf bsc=(pbf)qw[(qi+2)*3+1]; pbf bzr=(pbf)qw[(qi+2)*3+2];
      int KVBN=MH*(QN+VH);   // 8192
      // block-per-head with q_nope[h,:] staged in shared (reused across all KVL i).
      { float* qnsh=smem;   // QN floats
        for(int h=bid; h<MH; h+=nb){
          for(int d=tid;d<QN;d+=bs) qnsh[d]=MQ[h*(QN+QR)+d];
          __syncthreads();
          int colb=h*(QN+VH);
          for(int i=tid;i<KVL;i+=bs){ float acc=0.f;
            for(int d=0; d<QN; d++) acc += dqe(bwq,bsc,bzr,i,colb+d,KVBN)*qnsh[d];
            QC[h*KVL+i]=acc; }
          __syncthreads();
        }
      }
      grid.sync();
      // ---- scores[l,h]: one l per block; 16 threads per head cooperate on the
      //      512-dim latent dot (uses all 512 threads). QC cached in shared. ----
      __nv_bfloat16* ckv=(__nv_bfloat16*)stp[b*4+0];
      __nv_bfloat16* krope=(__nv_bfloat16*)stp[b*4+1];
      float* qccache=smem;             // MH*KVL floats = 16384 (QC, reused per block)
      for(int i=tid;i<MH*KVL;i+=bs) qccache[i]=QC[i];
      __syncthreads();
      // 16 threads/head read ckv DIRECTLY from global (coalesced across the group),
      // no per-token shared staging / __syncthreads (that per-token barrier was the
      // old hot spot). Each block strides tokens; warp-shuffle reduces the dot.
      const int TPH=16; int myh=tid/TPH, sub=tid%TPH;
      const float* qch=qccache+myh*KVL; const float* qrh=MQ+myh*(QN+QR)+QN;
      for(int l=bid; l<Lp; l+=nb){
        float acc=0.f;
        if(l<L){ const __nv_bfloat16* cr=ckv+(long)l*KVL;
                 for(int i=sub;i<KVL;i+=TPH) acc += qch[i]*__bfloat162float(cr[i]); }
        else   { for(int i=sub;i<KVL;i+=TPH) acc += qch[i]*KVA[i]; }
        if(sub<QR){ float kr=(l<L)?__bfloat162float(krope[l*QR+sub]):KRN[sub]; acc += qrh[sub]*kr; }
        #pragma unroll
        for(int o=8;o>0;o>>=1) acc+=__shfl_down_sync(0xffffffff,acc,o);
        if(sub==0) SCO[myh*Lp+l]=acc*MLA_SCALE;   // head-major SCO for coalesced softmax/pc
      }
      grid.sync();
      // ---- softmax over l per head (one head per block) ----
      for(int h=bid; h<MH; h+=nb){
        float loc=-1e30f; float* shm=SCO+h*Lp;   // contiguous per-head row (coalesced)
        for(int l=tid;l<Lp;l+=bs) loc=fmaxf(loc,shm[l]);
        float mx=blockMax(loc,rsm,tid,bs);
        float ls=0.f;
        for(int l=tid;l<Lp;l+=bs){ float e=expf(shm[l]-mx); shm[l]=e; ls+=e; }
        float sm=blockSum(ls,rsm,tid,bs);
        float inv=1.f/sm;
        for(int l=tid;l<Lp;l+=bs) shm[l]*=inv;
      }
      // zero PC here (all blocks; PC untouched until the pc phase below) so the
      // dedicated PC-zero barrier is folded into the softmax barrier.
      for(int i=gt;i<MH*KVL;i+=gT) PC[i]=0.f;
      grid.sync();
      // ---- pc[h,i] = sum_l p[l,h]*ckv[l,i] : tokens distributed over ALL blocks,
      //      private MH*KVL shared accumulator per block, atomicAdd to PC. ----
      { const int TB=8;               // tokens per barrier pair (amortizes syncs)
        float* pcs=smem;               // MH*KVL floats
        float* crow=pcs+MH*KVL;        // TB*KVL
        float* prow=crow+TB*KVL;       // TB*MH
        for(int i=tid;i<MH*KVL;i+=bs) pcs[i]=0.f;
        __syncthreads();
        for(int lb=bid*TB; lb<Lp; lb+=nb*TB){
          int nt=Lp-lb; if(nt>TB)nt=TB;
          for(int t2=0;t2<nt;t2++){ int l=lb+t2;
            for(int i=tid;i<KVL;i+=bs) crow[t2*KVL+i]=(l<L)?__bfloat162float(ckv[l*KVL+i]):KVA[i];
            for(int h=tid;h<MH;h+=bs) prow[t2*MH+h]=SCO[h*Lp+l];
          }
          __syncthreads();
          for(int idx=tid; idx<MH*KVL; idx+=bs){ int h=idx/KVL,i=idx%KVL; float a=0.f;
            for(int t2=0;t2<nt;t2++) a+=prow[t2*MH+h]*crow[t2*KVL+i];
            pcs[idx]+=a; }
          __syncthreads();
        }
        for(int i=tid;i<MH*KVL;i+=bs) if(pcs[i]!=0.f) atomicAdd(&PC[i],pcs[i]);
      }
      grid.sync();
      // ---- o[h,d]=sum_i pc[h,i]*Wv[i,h*256+128+d] ---- block-per-head with pc[h,:]
      // staged in shared (coalesced load once, reused across all VH outputs).
      float* Ob=work+O_O;
      { float* pcsh=smem;   // KVL floats
        for(int h=bid; h<MH; h+=nb){
          for(int i=tid;i<KVL;i+=bs) pcsh[i]=PC[h*KVL+i];
          __syncthreads();
          int colb=h*(QN+VH)+QN;
          for(int d=tid; d<VH; d+=bs){ float acc=0.f;
            for(int i=0;i<KVL;i++) acc += pcsh[i]*dqe(bwq,bsc,bzr,i,colb+d,KVBN);
            Ob[h*VH+d]=acc; }
          __syncthreads();
        }
      }
      grid.sync();
      // ---- o_proj + residual (K-split atomic) ----
      pu8 owq=(pu8)qw[(qi+3)*3+0]; pbf osc=(pbf)qw[(qi+3)*3+1]; pbf ozr=(pbf)qw[(qi+3)*3+2];
      gemv_atomic(owq,osc,ozr,work+O_O,XRES,CDIM,HID,gt,gT);
      grid.sync();
      qi+=4;
    }

    // ===================== MoE =====================
    {
      float* MOUT=work+O_MOUT; float* HEXP=work+O_HEXP; float* OEXP=work+O_OEXP;
      float* RL=work+O_RLOG; float* PR=work+O_PROB; float* WSEL=work+O_WSEL;
      // moe RMSNorm -> XN
      pbf wn=(pbf)sw[si*3+1];
      float loc=0.f; for(int i=tid;i<HID;i+=bs){ float v=XRES[i]; loc+=v*v; }
      float ss=blockSum(loc,rsm,tid,bs);
      float inv=rsqrtf(ss/HID+EPSN);
      for(int i=gt;i<HID;i+=gT) XN[i]=XRES[i]*inv*__bfloat162float(wn[i]);
      // pre-zero the gate/up atomic targets here (HEXP/OEXP untouched until the
      // gate/up gemv, 3 barriers later) so the dedicated zero barrier is dropped.
      for(int i=gt;i<(NA+1)*MINT;i+=gT){ HEXP[i]=0.f; OEXP[i]=0.f; }
      grid.sync();
      // router logits (bf16 dense, (NE,HID)): warp-per-expert, coalesced+shuffle.
      pbf rw=(pbf)sw[si*3+2];
      { int gwp=gt>>5, lane=tid&31;
        if(gwp<NE){ const __nv_bfloat16* wr=rw+gwp*HID; float acc=0.f;
          for(int k=lane;k<HID;k+=32) acc+=XN[k]*__bfloat162float(wr[k]);
          #pragma unroll
          for(int o=16;o>0;o>>=1) acc+=__shfl_down_sync(0xffffffff,acc,o);
          if(lane==0) RL[gwp]=acc;
        }
      }
      grid.sync();
      // softmax + topk8 computed REDUNDANTLY per-block (thread 0) into shared --
      // every block already synced on RL above, so this needs only __syncthreads,
      // removing a whole grid barrier per MoE (4 barriers/step).
      if(tid==0){
        float mx=-1e30f; for(int e=0;e<NE;e++) mx=fmaxf(mx,RL[e]);
        float s=0.f; float pr[NE]; for(int e=0;e<NE;e++){ float v=expf(RL[e]-mx); pr[e]=v; s+=v; }
        for(int e=0;e<NE;e++) pr[e]/=s;
        float wsum=0.f;
        for(int j=0;j<NA;j++){
          int be=0; float bv=-1.f;
          for(int e=0;e<NE;e++) if(pr[e]>bv){bv=pr[e];be=e;}
          sisel[j]=be; swsel[j]=bv; pr[be]=-1.f; wsum+=bv;
        }
        float nrm=ROUTED_SCALING/(wsum+1e-9f);
        for(int j=0;j<NA;j++) swsel[j]*=nrm;
      }
      __syncthreads();
      // gate+up for 9 slots (8 routed + 1 shared). Accumulate gate->HEXP, up->OEXP
      // (temp), K-split over the whole grid, then combine silu(gate)*up in HEXP.
      pu8 gwq=(pu8)eb[(b*6+0)*3+0]; pbf gsc=(pbf)eb[(b*6+0)*3+1]; pbf gzr=(pbf)eb[(b*6+0)*3+2];
      pu8 uwq=(pu8)eb[(b*6+1)*3+0]; pbf usc=(pbf)eb[(b*6+1)*3+1]; pbf uzr=(pbf)eb[(b*6+1)*3+2];
      pu8 sgwq=(pu8)eb[(b*6+3)*3+0]; pbf sgsc=(pbf)eb[(b*6+3)*3+1]; pbf sgzr=(pbf)eb[(b*6+3)*3+2];
      pu8 suwq=(pu8)eb[(b*6+4)*3+0]; pbf susc=(pbf)eb[(b*6+4)*3+1]; pbf suzr=(pbf)eb[(b*6+4)*3+2];
      long gstr=(long)1152*MINT, gsstr=(long)18*MINT;   // gate/up per-expert stride
      int NGH=HID>>7;
      { int N4=MINT>>2; int Nw=MINT>>2; long per=(long)N4*NGH; long unit=(NA+1)*per; long tot=2*unit;
        for(long id=gt; id<tot; id+=gT){
          int isup=id>=unit; long j=isup?(id-unit):id;
          int slot=j/per; long r=j%per; int c4=r%N4; int g=r/N4; int m=c4<<2;
          pu8 wq; pbf sc,zr; float* out;
          if(!isup){ out=HEXP; if(slot<NA){int e=sisel[slot];wq=gwq+e*gstr;sc=gsc+e*gsstr;zr=gzr+e*gsstr;}else{wq=sgwq;sc=sgsc;zr=sgzr;} }
          else { out=OEXP; if(slot<NA){int e=sisel[slot];wq=uwq+e*gstr;sc=usc+e*gsstr;zr=uzr+e*gsstr;}else{wq=suwq;sc=susc;zr=suzr;} }
          const unsigned int* w32=(const unsigned int*)(wq+(g*64)*MINT+m);
          float d0=0,d1=0,d2=0,d3=0,xsum=0.f;
          #pragma unroll 8
          for(int t=0;t<64;t++){ unsigned int bb=w32[t*Nw]; int k=g*128+2*t; float x0=XN[k],x1=XN[k+1]; xsum+=x0+x1;
            d0+=x0*(float)(bb&0xF)+x1*(float)((bb>>4)&0xF); d1+=x0*(float)((bb>>8)&0xF)+x1*(float)((bb>>12)&0xF);
            d2+=x0*(float)((bb>>16)&0xF)+x1*(float)((bb>>20)&0xF); d3+=x0*(float)((bb>>24)&0xF)+x1*(float)((bb>>28)&0xF); }
          const __nv_bfloat16* scg=sc+g*MINT+m; const __nv_bfloat16* zrg=zr+g*MINT+m; float* o=out+slot*MINT+m;
          atomicAdd(&o[0],__bfloat162float(scg[0])*(d0-__bfloat162float(zrg[0])*xsum));
          atomicAdd(&o[1],__bfloat162float(scg[1])*(d1-__bfloat162float(zrg[1])*xsum));
          atomicAdd(&o[2],__bfloat162float(scg[2])*(d2-__bfloat162float(zrg[2])*xsum));
          atomicAdd(&o[3],__bfloat162float(scg[3])*(d3-__bfloat162float(zrg[3])*xsum));
        }
      }
      grid.sync();
      // combine silu(gate)*up into HEXP; simultaneously zero OEXP (freed after
      // its up-value is consumed) so the down atomicAdd target is pre-zeroed --
      // saves a whole grid-wide zero barrier. OEXP[0:(NA+1)*MINT] zeroed here,
      // the tail [(NA+1)*MINT:(NA+1)*HID] zeroed in the same grid stride below.
      for(int i=gt;i<(NA+1)*MINT;i+=gT){ float hg=HEXP[i]; HEXP[i]=(hg/(1.f+expf(-hg)))*OEXP[i]; OEXP[i]=0.f; }
      for(int i=gt+(NA+1)*MINT;i<(NA+1)*HID;i+=gT) OEXP[i]=0.f;
      grid.sync();
      // down: OEXP[slot*HID+d] = sum_m HEXP[slot,m]*Wdown[e][m,d], K-split atomic
      pu8 dwq=(pu8)eb[(b*6+2)*3+0]; pbf dsc=(pbf)eb[(b*6+2)*3+1]; pbf dzr=(pbf)eb[(b*6+2)*3+2];
      pu8 sdwq=(pu8)eb[(b*6+5)*3+0]; pbf sdsc=(pbf)eb[(b*6+5)*3+1]; pbf sdzr=(pbf)eb[(b*6+5)*3+2];
      long dstr=(long)512*HID, dsstr=(long)8*HID;
      // down-proj is the most under-subscribed gemv (half the threads would idle
      // in a single wave), so split each column's 64-iter K-reduction across TWO
      // threads (half=32 iters each) -> ~2 waves, hiding DRAM latency. Both halves
      // atomicAdd into the same OEXP column.
      { int NGM=MINT>>7; int N4=HID>>2; int Nw=HID>>2; long per=(long)2*N4*NGM; long tot=(long)(NA+1)*per;
        for(long id=gt; id<tot; id+=gT){
          int slot=id/per; long r=id%per; int half=r&1; long r2=r>>1; int c4=r2%N4; int g=r2/N4; int d=c4<<2;
          pu8 wq; pbf sc,zr; const float* hin2=HEXP+slot*MINT;
          if(slot<NA){int e=sisel[slot];wq=dwq+e*dstr;sc=dsc+e*dsstr;zr=dzr+e*dsstr;}else{wq=sdwq;sc=sdsc;zr=sdzr;}
          const unsigned int* w32=(const unsigned int*)(wq+(g*64)*HID+d);
          float d0=0,d1=0,d2=0,d3=0,xsum=0.f; int t0h=half*32,t1h=t0h+32;
          #pragma unroll 8
          for(int t=t0h;t<t1h;t++){ unsigned int bb=w32[t*Nw]; int k=g*128+2*t; float x0=hin2[k],x1=hin2[k+1]; xsum+=x0+x1;
            d0+=x0*(float)(bb&0xF)+x1*(float)((bb>>4)&0xF); d1+=x0*(float)((bb>>8)&0xF)+x1*(float)((bb>>12)&0xF);
            d2+=x0*(float)((bb>>16)&0xF)+x1*(float)((bb>>20)&0xF); d3+=x0*(float)((bb>>24)&0xF)+x1*(float)((bb>>28)&0xF); }
          const __nv_bfloat16* scg=sc+g*HID+d; const __nv_bfloat16* zrg=zr+g*HID+d; float* o=OEXP+slot*HID+d;
          atomicAdd(&o[0],__bfloat162float(scg[0])*(d0-__bfloat162float(zrg[0])*xsum));
          atomicAdd(&o[1],__bfloat162float(scg[1])*(d1-__bfloat162float(zrg[1])*xsum));
          atomicAdd(&o[2],__bfloat162float(scg[2])*(d2-__bfloat162float(zrg[2])*xsum));
          atomicAdd(&o[3],__bfloat162float(scg[3])*(d3-__bfloat162float(zrg[3])*xsum));
        }
      }
      grid.sync();
      // reduce with weights + residual
      for(int d=gt;d<HID;d+=gT){
        float acc=0.f;
        for(int slot=0;slot<NA;slot++) acc+=swsel[slot]*OEXP[slot*HID+d];
        acc+=OEXP[NA*HID+d];   // shared weight 1.0
        XRES[d]+=acc;
      }
      grid.sync();
      si+=1;
    }
  }
  // write output
  for(int i=gt;i<HID;i+=gT) hout[i]=__float2bfloat16(XRES[i]);
}

// launcher
static int g_blocks=0, g_threads=0, g_shmem=0;
void mega_launch(
    torch::Tensor qw, torch::Tensor eb, torch::Tensor sw, torch::Tensor ksw, torch::Tensor stp,
    torch::Tensor work, torch::Tensor hin, torch::Tensor hout,
    long L, torch::Tensor isel)
{
  int threads=512;
  int s1 = (int)((MH*KVL + KVL + QR + 512)*sizeof(float));   // MLA scores phase
  int s2 = (int)((MH*KVL + 8*KVL + 8*MH)*sizeof(float));     // MLA pc phase (TB=8)
  int shmem = s1>s2?s1:s2;                                     // ~70KB, occ still 1/SM
  if(g_blocks==0){
    cudaFuncSetAttribute((void*)mega, cudaFuncAttributeMaxDynamicSharedMemorySize, shmem);
    int nb=0;
    cudaOccupancyMaxActiveBlocksPerMultiprocessor(&nb,(void*)mega,threads,shmem);
    int dev; cudaGetDevice(&dev);
    int sm; cudaDeviceGetAttribute(&sm,cudaDevAttrMultiProcessorCount,dev);
    if(nb<1) nb=1;
    g_blocks = nb*sm; g_threads=threads; g_shmem=shmem;
  }
  const long* qwp=qw.data_ptr<long>(); const long* ebp=eb.data_ptr<long>();
  const long* swp=sw.data_ptr<long>(); const long* kswp=ksw.data_ptr<long>();
  const long* stpp=stp.data_ptr<long>();
  float* workp=work.data_ptr<float>();
  const __nv_bfloat16* hinp=(const __nv_bfloat16*)hin.data_ptr<at::BFloat16>();
  __nv_bfloat16* houtp=(__nv_bfloat16*)hout.data_ptr<at::BFloat16>();
  int* iselp=isel.data_ptr<int>();
  int Li=(int)L;
  void* args[]={(void*)&qwp,(void*)&ebp,(void*)&swp,(void*)&kswp,(void*)&stpp,
                (void*)&workp,(void*)&hinp,(void*)&houtp,(void*)&Li,(void*)&iselp};
  cudaError_t e=cudaLaunchCooperativeKernel((void*)mega,dim3(g_blocks),dim3(g_threads),args,g_shmem,0);
  if(e!=cudaSuccess) printf("mega launch err: %s\n", cudaGetErrorString(e));
}
'''

_CPP_SRC = r'''
#include <torch/extension.h>
void mega_launch(torch::Tensor qw, torch::Tensor eb, torch::Tensor sw, torch::Tensor ksw, torch::Tensor stp,
    torch::Tensor work, torch::Tensor hin, torch::Tensor hout, long L, torch::Tensor isel);
'''

_MOD = None


def _get_mod():
    global _MOD
    if _MOD is None:
        _MOD = load_inline(
            name="kimi_mega",
            cpp_sources=[_CPP_SRC],
            cuda_sources=[_CUDA_SRC],
            functions=["mega_launch"],
            extra_cuda_cflags=["-O3", "--use_fast_math"],
            verbose=False,
        )
    return _MOD


class Model(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.blocks = nn.ModuleList(Block(cfg, k) for k in cfg.pattern)
        self._built = False

    def _build_tables(self):
        # constant weight pointer tables (built once)
        qw = []
        for b in range(4):
            blk = self.blocks[b]
            a = blk.attn
            if blk.kind == "K":
                lins = [a.q_proj, a.k_proj, a.v_proj, a.g_proj, a.o_proj]
            else:
                lins = [a.q_proj, a.kv_a, a.kv_b, a.o_proj]
            for ln in lins:
                qw += [ln.w_q.data_ptr(), ln.scales.data_ptr(), ln.zeros.data_ptr()]
        eb = []
        for b in range(4):
            m = self.blocks[b].moe
            for bank in (m.gate, m.up, m.down, m.s_gate, m.s_up, m.s_down):
                eb += [bank.w_q.data_ptr(), bank.scales.data_ptr(), bank.zeros.data_ptr()]
        sw = []
        for b in range(4):
            blk = self.blocks[b]
            sw += [blk.attn_norm.data_ptr(), blk.moe_norm.data_ptr(), blk.moe.router.weight.data_ptr()]
        ksw = []
        for b in range(3):
            a = self.blocks[b].attn
            ksw += [a.beta_proj.weight.data_ptr(), a.conv_w.data_ptr()]
        dev = self.blocks[0].attn_norm.device
        self._qw = torch.tensor(qw, dtype=torch.int64, device=dev)
        self._eb = torch.tensor(eb, dtype=torch.int64, device=dev)
        self._sw = torch.tensor(sw, dtype=torch.int64, device=dev)
        self._ksw = torch.tensor(ksw, dtype=torch.int64, device=dev)
        self._mod = _get_mod()
        self._isel = torch.zeros(16, dtype=torch.int32, device=dev)
        self._built = True

    def step(self, hidden, state):
        if not self._built:
            self._build_tables()
        cfg = self.cfg
        dev = hidden.device
        L = state[3]["c_kv"].shape[0]
        # state pointers (rebuilt each step; c_kv grows)
        stp = []
        for b in range(4):
            st = state[b]
            if self.blocks[b].kind == "K":
                stp += [st["S"].data_ptr(), st["cq"].data_ptr(), st["ck"].data_ptr(), st["cv"].data_ptr()]
            else:
                stp += [st["c_kv"].data_ptr(), st["k_rope"].data_ptr(), 0, 0]
        stp = torch.tensor(stp, dtype=torch.int64, device=dev)
        wsize = (12 * 1024 + 200000) + (L + 1) * 32 + 4096
        work = torch.empty(int(wsize), dtype=torch.float32, device=dev)
        hin = hidden.contiguous().to(torch.bfloat16)
        hout = torch.empty(cfg.hidden, dtype=torch.bfloat16, device=dev)

        self._mod.mega_launch(self._qw, self._eb, self._sw, self._ksw, stp,
                              work, hin, hout, int(L), self._isel)

        # append new MLA latent token from workspace to grow the cache
        O_KVA = 2304 + 2304 + 4096 * 5 + 2304 + 32 * 192  # matches C offsets up to KVA
        O_KRNEW = O_KVA + (512 + 64) + 32 * 512 + 32 * 512
        c_kv_new = work[O_KVA:O_KVA + cfg.kv_lora].to(torch.bfloat16)
        k_rope_new = work[O_KRNEW:O_KRNEW + cfg.qk_rope].to(torch.bfloat16)
        st3 = state[3]
        st3["c_kv"] = torch.cat([st3["c_kv"], c_kv_new[None]], 0)
        st3["k_rope"] = torch.cat([st3["k_rope"], k_rope_new[None]], 0)
        return hout, state
