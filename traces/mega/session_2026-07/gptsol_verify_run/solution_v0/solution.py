"""Single-launch persistent CUDA megakernel for Kimi-Linear W4A16 decode.

The CUDA grid executes all four blocks and synchronizes between dependent
phases with a resident-grid software barrier.  Int4 weights are unpacked and
dequantized in registers; no dequantized weight matrix is ever materialized.
MLA uses the latent (absorbed) formulation rather than expanding every cached
latent through kv_b.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import os
os.environ.setdefault("CUDA_HOME", "/tmp/cudatk")
import torch
import torch.nn as nn
from torch.utils.cpp_extension import load_inline

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


class QuantLinear(nn.Module):
    def __init__(self, in_f, out_f, group=128):
        super().__init__()
        self.in_f, self.out_f, self.group = in_f, out_f, group
        self.register_buffer("w_q", torch.zeros(in_f // 2, out_f, dtype=torch.uint8))
        self.register_buffer("scales", torch.zeros(in_f // group, out_f, dtype=torch.bfloat16))
        self.register_buffer("zeros", torch.zeros(in_f // group, out_f, dtype=torch.bfloat16))


class QuantExperts(nn.Module):
    def __init__(self, n, in_f, out_f, group=128):
        super().__init__()
        self.n, self.in_f, self.out_f, self.group = n, in_f, out_f, group
        self.register_buffer("w_q", torch.zeros(n, in_f // 2, out_f, dtype=torch.uint8))
        self.register_buffer("scales", torch.zeros(n, in_f // group, out_f, dtype=torch.bfloat16))
        self.register_buffer("zeros", torch.zeros(n, in_f // group, out_f, dtype=torch.bfloat16))


class KDA(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        d, C, H = cfg.hidden, cfg.kda_heads * cfg.kda_head_dim, cfg.kda_heads
        self.q_proj = QuantLinear(d, C); self.k_proj = QuantLinear(d, C)
        self.v_proj = QuantLinear(d, C); self.g_proj = QuantLinear(d, C)
        self.beta_proj = nn.Linear(d, H, bias=False, dtype=cfg.dtype)
        self.conv_w = nn.Parameter(torch.empty(3, C, cfg.short_conv, dtype=cfg.dtype))
        self.o_proj = QuantLinear(C, d)


class MLA(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        d, H = cfg.hidden, cfg.mla_heads
        self.q_proj = QuantLinear(d, H * (cfg.qk_nope + cfg.qk_rope))
        self.kv_a = QuantLinear(d, cfg.kv_lora + cfg.qk_rope)
        self.kv_b = QuantLinear(cfg.kv_lora, H * (cfg.qk_nope + cfg.v_head))
        self.o_proj = QuantLinear(H * cfg.v_head, d)


class MoE(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        d, m, E = cfg.hidden, cfg.moe_inter, cfg.n_experts
        self.router = nn.Linear(d, E, bias=False, dtype=cfg.dtype)
        self.gate = QuantExperts(E, d, m); self.up = QuantExperts(E, d, m)
        self.down = QuantExperts(E, m, d)
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


_CUDA = r'''
#include <torch/extension.h>
#include <ATen/cuda/CUDAContext.h>
#include <cuda.h>
#include <cuda_bf16.h>
#include <cuda_runtime.h>
#include <vector>

using bf = __nv_bfloat16;
constexpr int NB=111, NT=128, D=2304, C=4096, NE=64, TOP=8, MI=1024;

__device__ __forceinline__ float b2f(const bf x) { return __bfloat162float(x); }
__device__ __forceinline__ bf f2b(float x) { return __float2bfloat16_rn(x); }
__device__ __forceinline__ float silu(float x) { return x/(1.0f+__expf(-x)); }

// The product is rounded to bf16, exactly as the oracle's materialized weight.
__device__ __forceinline__ float qw(const unsigned char* q, const bf* s, const bf* z,
                                    int k, int n, int N) {
  unsigned v=q[(k>>1)*N+n]; v=(k&1)?(v>>4):(v&15);
  // Match bf16 dequantization's two elementwise rounding points: subtract,
  // then multiply.  This is important before long recurrent KDA updates.
  float d=b2f(f2b(float(v)-b2f(z[(k>>7)*N+n])));
  return b2f(f2b(d*b2f(s[(k>>7)*N+n])));
}
__device__ __forceinline__ float gemv1(const float* x, const unsigned char* q,
                                       const bf* s, const bf* z, int K,int N,int n) {
  float a0=0.f,a1=0.f;
  #pragma unroll 8
  for(int k=0;k<K;k+=2) {a0=fmaf(x[k],qw(q,s,z,k,n,N),a0);a1=fmaf(x[k+1],qw(q,s,z,k+1,n,N),a1);}
  return a0+a1;
}
__device__ __forceinline__ float gemvr(const float* x, const unsigned char* q,
                                       const bf* s, const bf* z, int K,int N,int n,int k0,int k1) {
  float a=0.f;
  for(int k=k0;k<k1;k++) a=fmaf(x[k],qw(q,s,z,k,n,N),a);
  return a;
}

__device__ void grid_bar(int* cnt,int* sense,int goal) {
  __syncthreads();
  if(threadIdx.x==0) {
    __threadfence();
    int old=atomicAdd(cnt,1);
    if(old==NB-1) { __threadfence(); atomicExch(cnt,0); __threadfence(); atomicExch(sense,goal); }
    else while(atomicAdd(sense,0)<goal) __nanosleep(64);
  }
  __syncthreads();
}

template<class T> __device__ __forceinline__ T* P(const unsigned long long* p,int layer,int i) {
  return reinterpret_cast<T*>(p[layer*40+i]);
}
__device__ float block_sum(float v) {
  __shared__ float sh[128]; sh[threadIdx.x]=v; __syncthreads();
  for(int d=64;d;d>>=1){if(threadIdx.x<d) sh[threadIdx.x]+=sh[threadIdx.x+d]; __syncthreads();}
  return sh[0];
}
__device__ float block_max(float v) {
  __shared__ float sh[128]; sh[threadIdx.x]=v; __syncthreads();
  for(int d=64;d;d>>=1){if(threadIdx.x<d) sh[threadIdx.x]=fmaxf(sh[threadIdx.x],sh[threadIdx.x+d]); __syncthreads();}
  return sh[0];
}

__global__ void mega(const unsigned long long* pp, bf* hidden,
 float* S0,bf* cq0,bf* ck0,bf* cv0, float* S1,bf* cq1,bf* ck1,bf* cv1,
 float* S2,bf* cq2,bf* ck2,bf* cv2,
 const bf* csrc,const bf* rsrc,bf* cdst,bf* rdst,int L,int copy_cache,
 float* w,int* sync) {
  int bid=blockIdx.x,t=threadIdx.x;
  int* cnt=sync; int* sense=sync+1; int phase=atomicAdd(sense,0);
  // workspace layout (floats)
  float* xn=w;                    // 2304
  float* proj=xn+2304;            // 4*4096 (or MLA q + kv)
  float* avec=proj+16384;         // 4096
  float* part=avec+4096;          // 7*2304
  float* mh=part+7*2304;          // 9*1024
  float* mout=mh+9*1024;          // 9*2304
  float* route=mout+9*2304;       // routing workspace
  float* qabs=route+32;           // 32*512
  float* scores=qabs+16384;       // 32*(L+1), allocated dynamically beyond here
  int LT=L+1;
  float* stats=scores+32*LT;      // part max/sum, head max/sum = 320
  float* cw=stats+320;            // 32*512

  float* SS[3]={S0,S1,S2}; bf* CQS[3]={cq0,cq1,cq2};
  bf* CKS[3]={ck0,ck1,ck2}; bf* CVS[3]={cv0,cv1,cv2};

  for(int layer=0;layer<4;layer++) {
    // attention RMSNorm.  Only block zero reduces; the whole grid then consumes xn.
    if(bid==0) {
      float ss=0.f; for(int i=t;i<D;i+=NT){float a=b2f(hidden[i]);ss+=a*a;}
      ss=block_sum(ss);
      __shared__ float inv; if(t==0) inv=rsqrtf(ss/D+1.e-6f); __syncthreads();
      for(int i=t;i<D;i+=NT) xn[i]=b2f(f2b(b2f(hidden[i])*inv*b2f(P<bf>(pp,layer,0)[i])));
    }
    grid_bar(cnt,sense,++phase);

    if(layer<3) {
      // q,k,v,g: one 128-thread tile per block and one matrix quadrant per 32 blocks.
      for(int task=bid;task<128;task+=NB) { int which=task>>5,tile=task&31,n=tile*128+t;
      const unsigned char* q=P<unsigned char>(pp,layer,2+which*3);
      const bf* s=P<bf>(pp,layer,3+which*3); const bf* z=P<bf>(pp,layer,4+which*3);
      proj[which*C+n]=b2f(f2b(gemv1(xn,q,s,z,D,C,n))); }
      grid_bar(cnt,sense,++phase);

      // short convolution and gate; beta is computed by the first 32 lanes.
      for(int n=bid*NT+t;n<C && bid<32;n+=NB*NT) {
        for(int j=0;j<3;j++) {
          bf* hist=j==0?CQS[layer]:(j==1?CKS[layer]:CVS[layer]);
          const bf* conv=P<bf>(pp,layer,15);
          float a=b2f(hist[n])*b2f(conv[(j*C+n)*4]);
          a+=b2f(hist[C+n])*b2f(conv[(j*C+n)*4+1]);
          a+=b2f(hist[2*C+n])*b2f(conv[(j*C+n)*4+2]);
          a+=proj[j*C+n]*b2f(conv[(j*C+n)*4+3]);
          avec[j*C+n]=b2f(f2b(silu(a)));
          hist[n]=hist[C+n]; hist[C+n]=hist[2*C+n]; hist[2*C+n]=f2b(proj[j*C+n]);
        }
        avec[3*C+n]=1.f/(1.f+__expf(proj[3*C+n])); // exp(-softplus(g))
      }
      if(bid==0 && t<32) {
        float a=0; const bf* bw=P<bf>(pp,layer,14);
        for(int k=0;k<D;k++) a=fmaf(xn[k],b2f(bw[t*D+k]),a);
        route[t]=1.f/(1.f+__expf(-b2f(f2b(a))));
      }
      grid_bar(cnt,sense,++phase);

      // A thread owns (head,value-channel), allowing both reductions over key dim.
      for(int j=bid*NT+t;j<C;j+=NB*NT) {
        int h=j>>7,dv=j&127, base=h*16384+dv;
        float pred=0.f;
        for(int dk=0;dk<128;dk++) {
          int ix=base+dk*128; float sv=SS[layer][ix]*avec[3*C+h*128+dk];
          SS[layer][ix]=sv; pred=fmaf(sv,avec[C+h*128+dk],pred);
        }
        float out=0.f,delta=avec[2*C+j]-pred,beta=route[h];
        for(int dk=0;dk<128;dk++) {
          int ix=base+dk*128; float sv=SS[layer][ix];
          sv+=beta*avec[C+h*128+dk]*delta; SS[layer][ix]=sv;
          out=fmaf(sv,avec[h*128+dk]*(1.f/sqrtf(128.f)),out);
        }
        avec[j]=b2f(f2b(out));
      }
      grid_bar(cnt,sense,++phase);
      // output projection, seven-way K reduction to occupy 126 blocks.
      for(int task=bid;task<126;task+=NB) {
        int tile=task/7,sp=task%7,n=tile*128+t;
        if(n<D){int k0=C*sp/7,k1=C*(sp+1)/7; part[sp*D+n]=gemvr(avec,P<unsigned char>(pp,layer,16),P<bf>(pp,layer,17),P<bf>(pp,layer,18),C,D,n,k0,k1);}
      }
      grid_bar(cnt,sense,++phase);
    } else {
      // MLA q and kv_a in one output-parallel phase.
      for(int n=bid*NT+t;n<6720;n+=NB*NT) {
        if(n<6144) proj[n]=b2f(f2b(gemv1(xn,P<unsigned char>(pp,layer,2),P<bf>(pp,layer,3),P<bf>(pp,layer,4),D,6144,n)));
        else {int m=n-6144; proj[n]=b2f(f2b(gemv1(xn,P<unsigned char>(pp,layer,5),P<bf>(pp,layer,6),P<bf>(pp,layer,7),D,576,m)));}
      }
      grid_bar(cnt,sense,++phase);
      // Copy a newly-fed cache into private growable storage (only first call/state).
      if(copy_cache) {
        for(long long i=(long long)bid*NT+t;i<(long long)L*512;i+=(long long)NB*NT) cdst[i]=csrc[i];
        for(long long i=(long long)bid*NT+t;i<(long long)L*64;i+=(long long)NB*NT) rdst[i]=rsrc[i];
      }
      for(int i=bid*NT+t;i<512;i+=NB*NT) cdst[(long long)L*512+i]=f2b(proj[6144+i]);
      for(int i=bid*NT+t;i<64;i+=NB*NT) {
        float inv=powf(10000.f,-float((i>>1)*2)/64.f),ang=L*inv,co=cosf(ang),si=sinf(ang);
        float a=proj[6144+512+(i&~1)],b=proj[6144+512+(i&~1)+1];
        rdst[(long long)L*64+i]=f2b((i&1)?b*co+a*si:a*co-b*si);
      }
      // Rotate each q pair in one thread: separate even/odd writers can race
      // because this is an in-place transform.
      for(int pair=bid*NT+t;pair<1024;pair+=NB*NT) {
        int h=pair>>5,d=(pair&31)*2;
        float inv=powf(10000.f,-float(d)/64.f),ang=L*inv,co=cosf(ang),si=sinf(ang);
        int n=h*192+128+d; float a=proj[n],b=proj[n+1];
        proj[n]=b2f(f2b(a*co-b*si)); proj[n+1]=b2f(f2b(b*co+a*si));
      }
      grid_bar(cnt,sense,++phase);
      // Absorb B_k into q: qabs[h,c] = sum_d B_k[c,h,d] q[h,d].
      for(int ix=bid*NT+t;ix<16384;ix+=NB*NT) {
        int h=ix>>9,c=ix&511; float a=0;
        for(int d0=0;d0<128;d0++) a=fmaf(proj[h*192+d0],qw(P<unsigned char>(pp,layer,8),P<bf>(pp,layer,9),P<bf>(pp,layer,10),c,h*256+d0,8192),a);
        qabs[ix]=a;
      }
      grid_bar(cnt,sense,++phase);
      // Four token partitions per head compute and retain latent scores.
      for(int task=bid;task<128;task+=NB){ int h=task>>2,pa=task&3,lo=LT*pa/4,hi=LT*(pa+1)/4; float lm=-INFINITY;
        for(int l=lo+t;l<hi;l+=NT){float a=0; for(int c=0;c<512;c++) a=fmaf(qabs[h*512+c],b2f(cdst[(long long)l*512+c]),a);
          float rr=0;for(int d0=0;d0<64;d0++) rr=fmaf(proj[h*192+128+d0],b2f(rdst[(long long)l*64+d0]),rr);
          a=(a+rr)*(1.f/sqrtf(192.f));scores[h*LT+l]=a;lm=fmaxf(lm,a);}
        lm=block_max(lm);if(t==0)stats[task]=lm;
      }
      grid_bar(cnt,sense,++phase);
      if(bid==0 && t<32){float m=-INFINITY;for(int p0=0;p0<4;p0++)m=fmaxf(m,stats[t*4+p0]);stats[128+t]=m;}
      grid_bar(cnt,sense,++phase);
      for(int task=bid;task<128;task+=NB){ int h=task>>2,pa=task&3,lo=LT*pa/4,hi=LT*(pa+1)/4;float sm=0,m=stats[128+h];
        for(int l=lo+t;l<hi;l+=NT){float e=__expf(scores[h*LT+l]-m);scores[h*LT+l]=e;sm+=e;}
        sm=block_sum(sm);if(t==0)stats[160+task]=sm;
      }
      grid_bar(cnt,sense,++phase);
      if(bid==0 && t<32){float s=0;for(int p0=0;p0<4;p0++)s+=stats[160+t*4+p0];stats[288+t]=1.f/s;}
      grid_bar(cnt,sense,++phase);
      // Softmax-weighted latent, four blocks/head and coalesced latent channels.
      for(int task=bid;task<128;task+=NB){int h=task>>2,pa=task&3,c=pa*128+t;float a=0,iv=stats[288+h];
       for(int l=0;l<LT;l++)a=fmaf(scores[h*LT+l]*iv,b2f(cdst[(long long)l*512+c]),a);cw[h*512+c]=a;}
      grid_bar(cnt,sense,++phase);
      // Apply B_v only after reducing the cache in latent space.
      for(int n=bid*NT+t;n<C;n+=NB*NT){int h=n>>7,dv=n&127;float a=0;
        for(int c=0;c<512;c++)a=fmaf(cw[h*512+c],qw(P<unsigned char>(pp,layer,8),P<bf>(pp,layer,9),P<bf>(pp,layer,10),c,h*256+128+dv,8192),a);
        avec[n]=b2f(f2b(a));}
      grid_bar(cnt,sense,++phase);
      for(int task=bid;task<126;task+=NB){int tile=task/7,sp=task%7,n=tile*128+t;if(n<D){int k0=C*sp/7,k1=C*(sp+1)/7;part[sp*D+n]=gemvr(avec,P<unsigned char>(pp,layer,11),P<bf>(pp,layer,12),P<bf>(pp,layer,13),C,D,n,k0,k1);}}
      grid_bar(cnt,sense,++phase);
    }
    // finish attention residual and compute MoE RMS.
    if(bid==0){
      float ss=0;for(int n=t;n<D;n+=NT){float a=0;for(int sp=0;sp<7;sp++)a+=part[sp*D+n];hidden[n]=f2b(b2f(hidden[n])+b2f(f2b(a)));float v=b2f(hidden[n]);ss+=v*v;}
      ss=block_sum(ss);__shared__ float iv;if(t==0)iv=rsqrtf(ss/D+1.e-6f);__syncthreads();
      for(int n=t;n<D;n+=NT)xn[n]=b2f(f2b(b2f(hidden[n])*iv*b2f(P<bf>(pp,layer,1)[n])));
    }
    grid_bar(cnt,sense,++phase);
    // Router and exact top-8 normalization (softmax's common denominator cancels).
    if(bid==0){
      if(t<64){float a=0;const bf* rw=P<bf>(pp,layer,20);for(int k=0;k<D;k++)a=fmaf(xn[k],b2f(rw[t*D+k]),a);proj[t]=b2f(f2b(a));}
      __syncthreads();if(t==0){bool used[64]={};float den=0;
        for(int j=0;j<8;j++){int bi=0;float bv=-INFINITY;for(int e=0;e<64;e++)if(!used[e]&&proj[e]>bv){bv=proj[e];bi=e;}used[bi]=1;route[j]=(float)bi;route[16+j]=bv;}
        float mx=route[16];for(int j=0;j<8;j++){route[16+j]=__expf(route[16+j]-mx);den+=route[16+j];}
        den=fmaxf(den,1.e-20f);
        for(int j=0;j<8;j++)route[16+j]=route[16+j]/den*2.446f;route[8]=0.f;route[24]=1.f;}
    }
    grid_bar(cnt,sense,++phase);
    // Fused gate/up for eight routed experts plus the shared expert.
    for(int task=bid;task<72;task+=NB){int sl=task>>3,tile=task&7,n=tile*128+t;bool sh=sl==8;int e=sh?0:(((int)route[sl])&63);
      const unsigned char* g=P<unsigned char>(pp,layer,sh?30:21);const bf* gs=P<bf>(pp,layer,sh?31:22);const bf* gz=P<bf>(pp,layer,sh?32:23);
      const unsigned char* u=P<unsigned char>(pp,layer,sh?33:24);const bf* us=P<bf>(pp,layer,sh?34:25);const bf* uz=P<bf>(pp,layer,sh?35:26);
      if(!sh){g+=(long long)e*(D/2)*MI;gs+=(long long)e*(D/128)*MI;gz+=(long long)e*(D/128)*MI;u+=(long long)e*(D/2)*MI;us+=(long long)e*(D/128)*MI;uz+=(long long)e*(D/128)*MI;}
      float ga=0,ua=0;for(int k=0;k<D;k++){float xx=xn[k];ga=fmaf(xx,qw(g,gs,gz,k,n,MI),ga);ua=fmaf(xx,qw(u,us,uz,k,n,MI),ua);}mh[sl*MI+n]=silu(ga)*ua;
    }
    grid_bar(cnt,sense,++phase);
    // Expert down projections.
    for(int task=bid;task<9*18;task+=NB){int sl=task/18,tile=task%18,n=tile*128+t;bool sh=sl==8;int e=sh?0:(((int)route[sl])&63);
      const unsigned char* q=P<unsigned char>(pp,layer,sh?36:27);const bf* s=P<bf>(pp,layer,sh?37:28);const bf* z=P<bf>(pp,layer,sh?38:29);
      if(!sh){q+=(long long)e*(MI/2)*D;s+=(long long)e*(MI/128)*D;z+=(long long)e*(MI/128)*D;}
      mout[sl*D+n]=gemv1(mh+sl*MI,q,s,z,MI,D,n);
    }
    grid_bar(cnt,sense,++phase);
    for(int n=bid*NT+t;n<D;n+=NB*NT){float a=mout[8*D+n];for(int sl=0;sl<8;sl++)a=fmaf(route[16+sl],mout[sl*D+n],a);hidden[n]=f2b(b2f(hidden[n])+b2f(f2b(a)));}
    grid_bar(cnt,sense,++phase);
  }
}

void launch(torch::Tensor pp,torch::Tensor hidden,std::vector<torch::Tensor> st,
 const torch::Tensor& csrc,const torch::Tensor& rsrc,torch::Tensor cdst,torch::Tensor rdst,
 int64_t L,bool copy,torch::Tensor work,torch::Tensor sync) {
  cudaStream_t stream=at::cuda::getCurrentCUDAStream();
  mega<<<NB,NT,0,stream>>>((unsigned long long*)pp.data_ptr(),(bf*)hidden.data_ptr(),
   (float*)st[0].data_ptr(),(bf*)st[1].data_ptr(),(bf*)st[2].data_ptr(),(bf*)st[3].data_ptr(),
   (float*)st[4].data_ptr(),(bf*)st[5].data_ptr(),(bf*)st[6].data_ptr(),(bf*)st[7].data_ptr(),
   (float*)st[8].data_ptr(),(bf*)st[9].data_ptr(),(bf*)st[10].data_ptr(),(bf*)st[11].data_ptr(),
   (bf*)csrc.data_ptr(),(bf*)rsrc.data_ptr(),(bf*)cdst.data_ptr(),(bf*)rdst.data_ptr(),(int)L,(int)copy,
   (float*)work.data_ptr(),(int*)sync.data_ptr());
  C10_CUDA_KERNEL_LAUNCH_CHECK();
}
PYBIND11_MODULE(TORCH_EXTENSION_NAME,m){m.def("launch",&launch);}
'''

_EXT = None


def _extension():
    global _EXT
    if _EXT is None:
        _EXT = load_inline(name="kimi_mega_b120_final67", cpp_sources="", cuda_sources=_CUDA,
                           functions=None, extra_cuda_cflags=["-O3", "--use_fast_math", "-maxrregcount=82"], verbose=False)
    return _EXT


class Model(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.blocks = nn.ModuleList(Block(cfg, k) for k in cfg.pattern)
        self._ptrs = None
        self._work = None
        self._sync = None
        self._cache_c = None
        self._cache_r = None
        self._cache_source = None

    @staticmethod
    def _q(dst, base, q):
        dst[base:base + 3] = [q.w_q.data_ptr(), q.scales.data_ptr(), q.zeros.data_ptr()]

    def _make_ptrs(self, device):
        p = [0] * (4 * 40)
        for li, b in enumerate(self.blocks):
            o = li * 40
            p[o], p[o + 1] = b.attn_norm.data_ptr(), b.moe_norm.data_ptr()
            if li < 3:
                for j, q in enumerate((b.attn.q_proj, b.attn.k_proj, b.attn.v_proj, b.attn.g_proj)):
                    self._q(p, o + 2 + 3 * j, q)
                p[o + 14], p[o + 15] = b.attn.beta_proj.weight.data_ptr(), b.attn.conv_w.data_ptr()
                self._q(p, o + 16, b.attn.o_proj)
            else:
                self._q(p, o + 2, b.attn.q_proj); self._q(p, o + 5, b.attn.kv_a)
                self._q(p, o + 8, b.attn.kv_b); self._q(p, o + 11, b.attn.o_proj)
            p[o + 20] = b.moe.router.weight.data_ptr()
            for base, q in ((21,b.moe.gate),(24,b.moe.up),(27,b.moe.down),
                            (30,b.moe.s_gate),(33,b.moe.s_up),(36,b.moe.s_down)):
                self._q(p, o + base, q)
        self._ptrs = torch.tensor(p, dtype=torch.int64, device=device)
        self._sync = torch.zeros(2, dtype=torch.int32, device=device)

    def step(self, hidden, state):
        if self._ptrs is None or self._ptrs.device != hidden.device:
            self._make_ptrs(hidden.device)
        src_c, src_r = state[3]["c_kv"], state[3]["k_rope"]
        L = src_c.shape[0]
        source = (src_c.data_ptr(), src_r.data_ptr(), L)
        copy = self._cache_source != source
        if copy:
            # A generous decode tail avoids allocation in all timed iterations.
            self._cache_c = torch.empty((L + 1024, 512), dtype=torch.bfloat16, device=hidden.device)
            self._cache_r = torch.empty((L + 1024, 64), dtype=torch.bfloat16, device=hidden.device)
            self._cache_source = source
        need = 2304 + 16384 + 4096 + 7*2304 + 9*1024 + 9*2304 + 32 + 16384 + 32*(L+1) + 320 + 16384
        if self._work is None or self._work.numel() < need:
            self._work = torch.empty(need + 4096, dtype=torch.float32, device=hidden.device)
        flat = []
        for i in range(3):
            s = state[i]
            flat += [s["S"], s["cq"], s["ck"], s["cv"]]
        _extension().launch(self._ptrs, hidden, flat, src_c, src_r, self._cache_c, self._cache_r,
                            L, copy, self._work, self._sync)
        state[3]["c_kv"] = self._cache_c[:L + 1]
        state[3]["k_rope"] = self._cache_r[:L + 1]
        self._cache_source = (self._cache_c.data_ptr(), self._cache_r.data_ptr(), L + 1)
        return hidden, state
