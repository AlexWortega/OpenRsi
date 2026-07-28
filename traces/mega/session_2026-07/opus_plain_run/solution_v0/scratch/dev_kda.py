import os
os.environ.setdefault("CUDA_HOME","/tmp/cudatk")
import torch, torch.nn.functional as F, copy
from torch.utils.cpp_extension import load_inline
import reference as R

cpp = "torch::Tensor kda_attn(int64_t Wtab, int64_t Stab, torch::Tensor hid, torch::Tensor scratch);"
src = r'''
#include <torch/extension.h>
#include <cuda_runtime.h>
#include <cuda_bf16.h>
#include <cooperative_groups.h>
namespace cg=cooperative_groups;
typedef __nv_bfloat16 bf16;
#define NB 188
#define NT 256
#define GRID (NB*NT)
#define D 2304
#define HK 32
#define DK 128
#define C 4096
__device__ __forceinline__ float b2f(bf16 v){return __bfloat162float(v);}

// W table indices for a KDA block
#define W_ANORM 0
#define W_MNORM 1
#define W_Q 2
#define W_K 5
#define W_V 8
#define W_G 11
#define W_O 14
#define W_BETA 17
#define W_CONV 18

__device__ void gemv_i4(const float* x,const uint8_t* wq,const bf16* sc,const bf16* zr,
    float* y,int K,int N){
    const uint32_t* wq32=(const uint32_t*)wq; int Nw=N/4,ncol4=N/4,ng=K/128;
    int col_blocks=(ncol4+NT-1)/NT; int ksplit=NB/col_blocks; if(ksplit<1)ksplit=1;
    int gper=(ng+ksplit-1)/ksplit; int bid=blockIdx.x;
    if(bid>=col_blocks*ksplit) return;
    int cb=bid%col_blocks, kt=bid/col_blocks;
    int col4=cb*NT+threadIdx.x; if(col4>=ncol4) return;
    int n0=col4*4; int g0=kt*gper,g1=min(ng,g0+gper);
    float a0=0,a1=0,a2=0,a3=0;
    for(int g=g0;g<g1;++g){
        const bf16* scg=sc+g*N+n0; const bf16* zrg=zr+g*N+n0;
        float s0=b2f(scg[0]),s1=b2f(scg[1]),s2=b2f(scg[2]),s3=b2f(scg[3]);
        float z0=b2f(zrg[0]),z1=b2f(zrg[1]),z2=b2f(zrg[2]),z3=b2f(zrg[3]);
        int r0=g*64;
        #pragma unroll 4
        for(int r=r0;r<r0+64;++r){
            uint32_t w=wq32[r*Nw+col4]; float xa=x[2*r],xb=x[2*r+1];
            uint8_t b0=w&0xFF,b1=(w>>8)&0xFF,b2_=(w>>16)&0xFF,b3=(w>>24)&0xFF;
            a0+=xa*((float)(b0&0xF)-z0)*s0+xb*((float)((b0>>4)&0xF)-z0)*s0;
            a1+=xa*((float)(b1&0xF)-z1)*s1+xb*((float)((b1>>4)&0xF)-z1)*s1;
            a2+=xa*((float)(b2_&0xF)-z2)*s2+xb*((float)((b2_>>4)&0xF)-z2)*s2;
            a3+=xa*((float)(b3&0xF)-z3)*s3+xb*((float)((b3>>4)&0xF)-z3)*s3;
        }
    }
    if(ksplit==1){y[n0]=a0;y[n0+1]=a1;y[n0+2]=a2;y[n0+3]=a3;}
    else{atomicAdd(&y[n0],a0);atomicAdd(&y[n0+1],a1);atomicAdd(&y[n0+2],a2);atomicAdd(&y[n0+3],a3);}
}
__device__ __forceinline__ void zero_buf(float* y,int N){
    int gid=blockIdx.x*NT+threadIdx.x; for(int i=gid;i<N;i+=GRID)y[i]=0.f;
}
// scratch offsets
#define S_XN 0
#define S_Q (D)
#define S_K (D+C)
#define S_V (D+2*C)
#define S_G (D+3*C)
#define S_BETA (D+4*C)
#define S_ATTN (D+4*C+HK)

__global__ void kda_attn_k(const int64_t* W,const int64_t* St,float* hid,float* scr){
    cg::grid_group grid=cg::this_grid();
    int tid=threadIdx.x; int gid=blockIdx.x*NT+tid;
    // rmsnorm hid->xn
    const bf16* anorm=(const bf16*)W[W_ANORM];
    __shared__ float ss;
    // compute sumsq via block0 broadcast? simpler: each block computes independently into shared then we need global. Do: block-stride reduce with atomics into scr[S_ATTN-1]? Use a temp.
    // Simple approach: block 0 computes rmsnorm fully, others wait.
    if(blockIdx.x==0){
        float acc=0; for(int i=tid;i<D;i+=NT) acc+=hid[i]*hid[i];
        __shared__ float red[NT]; red[tid]=acc; __syncthreads();
        for(int s=NT/2;s>0;s>>=1){ if(tid<s) red[tid]+=red[tid+s]; __syncthreads(); }
        float inv=rsqrtf(red[0]/D + 1e-6f);
        for(int i=tid;i<D;i+=NT) scr[S_XN+i]=hid[i]*inv*b2f(anorm[i]);
    }
    grid.sync();
    // gemv q,k,v,g
    zero_buf(scr+S_Q,C); zero_buf(scr+S_K,C); zero_buf(scr+S_V,C); zero_buf(scr+S_G,C);
    grid.sync();
    gemv_i4(scr+S_XN,(const uint8_t*)W[W_Q],(const bf16*)W[W_Q+1],(const bf16*)W[W_Q+2],scr+S_Q,D,C); grid.sync();
    gemv_i4(scr+S_XN,(const uint8_t*)W[W_K],(const bf16*)W[W_K+1],(const bf16*)W[W_K+2],scr+S_K,D,C); grid.sync();
    gemv_i4(scr+S_XN,(const uint8_t*)W[W_V],(const bf16*)W[W_V+1],(const bf16*)W[W_V+2],scr+S_V,D,C); grid.sync();
    gemv_i4(scr+S_XN,(const uint8_t*)W[W_G],(const bf16*)W[W_G+1],(const bf16*)W[W_G+2],scr+S_G,D,C); grid.sync();
    // conv + silu for q,k,v ; g just softplus-neg ; beta
    // conv_w [3,C,4]; states cq,ck,cv bf16 [3,C]
    const bf16* conv=(const bf16*)W[W_CONV];
    bf16* cq=(bf16*)St[1]; bf16* ck=(bf16*)St[2]; bf16* cv=(bf16*)St[3];
    // process channels across grid
    for(int c=gid;c<C;c+=GRID){
        // q
        float qv=scr[S_Q+c], kv=scr[S_K+c], vv=scr[S_V+c];
        // window = [cq0,cq1,cq2,qv]; w=conv[0,c,:]
        #define CONVCH(BUF,IDX,VAL,OUT) {\
            float w0=b2f(conv[(IDX)*C*4 + c*4 + 0]);\
            float w1=b2f(conv[(IDX)*C*4 + c*4 + 1]);\
            float w2=b2f(conv[(IDX)*C*4 + c*4 + 2]);\
            float w3=b2f(conv[(IDX)*C*4 + c*4 + 3]);\
            float p0=b2f(BUF[0*C+c]),p1=b2f(BUF[1*C+c]),p2=b2f(BUF[2*C+c]);\
            float o=p0*w0+p1*w1+p2*w2+VAL*w3;\
            float sig=o/(1.f+expf(-o));\
            OUT=sig;\
            /* update state: shift */\
            BUF[0*C+c]=__float2bfloat16(p1);BUF[1*C+c]=__float2bfloat16(p2);BUF[2*C+c]=__float2bfloat16(VAL);\
        }
        float qo,ko,vo;
        CONVCH(cq,0,qv,qo); CONVCH(ck,1,kv,ko); CONVCH(cv,2,vv,vo);
        scr[S_Q+c]=qo; scr[S_K+c]=ko; scr[S_V+c]=vo;
        // g: -softplus(g)
        float gg=scr[S_G+c]; scr[S_G+c]=-log1pf(expf(gg));
    }
    // beta = sigmoid(x @ beta_w.T), beta_w [H,d]
    if(blockIdx.x==0){
        const bf16* bw=(const bf16*)W[W_BETA];
        for(int h=tid;h<HK;h+=NT){
            float acc=0; for(int i=0;i<D;i++) acc+=scr[S_XN+i]*b2f(bw[h*D+i]);
            scr[S_BETA+h]=1.f/(1.f+expf(-acc));
        }
    }
    grid.sync();
    // KDA state update: one head per block (32 heads). S[h] is [DK,DV]=128x128
    float* Sst=(float*)St[0];
    float scale=rsqrtf((float)DK);
    for(int h=blockIdx.x; h<HK; h+=NB){
        float* Sh=Sst + h*DK*DK;
        // load q,k,v for head
        // pred[j]=sum_i Sh[i,j]*exp(g[i])*k[i]; then update; o[j]=sum_i Snew[i,j]*q[i]
        // step1: apply decay S[i,j]*=exp(g[i]); compute pred[j]
        // We'll compute per (i,j) with 256 threads over 128x128=16384 => 64 each
        __shared__ float qh[DK], kh[DK], gh[DK], betas;
        for(int i=tid;i<DK;i+=NT){ qh[i]=scr[S_Q+h*DK+i]*scale; kh[i]=scr[S_K+h*DK+i]; gh[i]=expf(scr[S_G+h*DK+i]); }
        if(tid==0) betas=scr[S_BETA+h];
        __syncthreads();
        __shared__ float pred[DK];
        // pred[j]=sum_i Sh[i,j]*gh[i]*kh[i]
        for(int j=tid;j<DK;j+=NT){
            float acc=0;
            for(int i=0;i<DK;i++){ float sij=Sh[i*DK+j]*gh[i]; acc+=sij*kh[i]; }
            pred[j]=acc;
        }
        __syncthreads();
        __shared__ float vh[DK];
        for(int j=tid;j<DK;j+=NT) vh[j]=scr[S_V+h*DK+j];
        __syncthreads();
        // update S and compute o[j]
        __shared__ float oh[DK];
        for(int j=tid;j<DK;j+=NT) oh[j]=0.f;
        __syncthreads();
        // each thread handles set of (i,j): iterate i, accumulate into oh[j] via... need per-j accumulation. Do per-j like pred.
        for(int j=tid;j<DK;j+=NT){
            float diff=vh[j]-pred[j];
            float acc=0;
            for(int i=0;i<DK;i++){
                float sij=Sh[i*DK+j]*gh[i] + betas*kh[i]*diff;
                Sh[i*DK+j]=sij;
                acc+=sij*qh[i];
            }
            oh[j]=acc;
        }
        __syncthreads();
        for(int j=tid;j<DK;j+=NT) scr[S_ATTN+h*DK+j]=oh[j]; // o in [C] layout? attn scratch reused as o pre-oproj
    }
    grid.sync();
    // o_proj gemv: input o[C], weight o_proj [C,d]-> out d. store into hid? we output attn_out to scr area then caller adds.
    // reuse scr[S_Q..] region? Put o at S_ATTN (size C). out d -> write to a buffer; use S_XN region? xn no longer needed. Put out at hid? we need residual add outside. Write attn_out to scr[S_ATTN + C]? ensure space. We'll just overwrite hid = hid + out here for test we output out.
    // zero output region
    float* outp = scr + S_ATTN + C; // attn_out [d]
    zero_buf(outp,D); grid.sync();
    gemv_i4(scr+S_ATTN,(const uint8_t*)W[W_O],(const bf16*)W[W_O+1],(const bf16*)W[W_O+2],outp,C,D); grid.sync();
    // hid += out (residual) -- for test just copy out to hid
    for(int i=gid;i<D;i+=GRID) hid[i]=outp[i];
}

torch::Tensor kda_attn(int64_t Wtab,int64_t Stab,torch::Tensor hid,torch::Tensor scr){
    const int64_t* W=(const int64_t*)Wtab; const int64_t* St=(const int64_t*)Stab;
    float* h=hid.data_ptr<float>(); float* s=scr.data_ptr<float>();
    void* args[]={(void*)&W,(void*)&St,(void*)&h,(void*)&s};
    dim3 g(NB),b(NT); cudaLaunchCooperativeKernel((void*)kda_attn_k,g,b,args,0,0);
    cudaError_t e=cudaDeviceSynchronize(); if(e!=cudaSuccess)printf("err %s\n",cudaGetErrorString(e));
    return hid;
}
'''
mod=load_inline(name="dev_kda",cpp_sources=cpp,cuda_sources=src,functions=["kda_attn"],extra_cuda_cflags=["-O3","-arch=sm_120"],verbose=False)

torch.manual_seed(0)
cfg=R.build_config({"n_experts":64})
m=R.Model(cfg).cuda().eval()
st=R.init_state(cfg,2048,0)
h=R.init_token(cfg,0)
blk=m.blocks[0]; kda=blk.attn
# torch mirror attn
st_t=copy.deepcopy(st[0])
xn=R._rmsnorm(h,blk.attn_norm)
with torch.no_grad():
    o_t = kda.step(xn, st_t)  # this is reference KDA.step using its own conv etc.
# Build W table
def qlp(ql): return [ql.w_q.data_ptr(), ql.scales.data_ptr(), ql.zeros.data_ptr()]
W=[blk.attn_norm.data_ptr(), blk.moe_norm.data_ptr()]
W+=qlp(kda.q_proj)+qlp(kda.k_proj)+qlp(kda.v_proj)+qlp(kda.g_proj)+qlp(kda.o_proj)
W+=[kda.beta_proj.weight.data_ptr(), kda.conv_w.data_ptr()]
Wt=torch.tensor(W,dtype=torch.int64,device='cuda')
# state table
S=[st[0]["S"].data_ptr(), st[0]["cq"].data_ptr(), st[0]["ck"].data_ptr(), st[0]["cv"].data_ptr()]
St=torch.tensor(S,dtype=torch.int64,device='cuda')
hid=h.float().clone()
scr=torch.zeros(2_000_000,device='cuda')
out=mod.kda_attn(Wt.data_ptr(),St.data_ptr(),hid,scr)
torch.cuda.synchronize()
print("attn out cos", F.cosine_similarity(o_t.float(), out.float(), dim=0).item())
print("S cos", F.cosine_similarity(st_t["S"].float().flatten(), st[0]["S"].float().flatten(),dim=0).item())
