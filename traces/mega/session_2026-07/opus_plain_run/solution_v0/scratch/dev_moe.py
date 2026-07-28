import os
os.environ.setdefault("CUDA_HOME","/tmp/cudatk")
import torch, torch.nn.functional as F, copy
from torch.utils.cpp_extension import load_inline
import reference as R

cpp = "torch::Tensor moe(int64_t Wtab,torch::Tensor hid,torch::Tensor scr);"
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
#define E 64
#define NACT 8
#define MI 1024
#define ROUTED 2.446f
__device__ __forceinline__ float b2f(bf16 v){return __bfloat162float(v);}
// gemv from expert weight base: wq[in/2,out], sc/zr[in/128,out]
__device__ void gemv_i4(const float* x,const uint8_t* wq,const bf16* sc,const bf16* zr,float* y,int K,int N){
    const uint32_t* wq32=(const uint32_t*)wq;int Nw=N/4,ncol4=N/4,ng=K/128;
    int col_blocks=(ncol4+NT-1)/NT;int ksplit=NB/col_blocks;if(ksplit<1)ksplit=1;
    int gper=(ng+ksplit-1)/ksplit;int bid=blockIdx.x;if(bid>=col_blocks*ksplit)return;
    int cb=bid%col_blocks,kt=bid/col_blocks;int col4=cb*NT+threadIdx.x;if(col4>=ncol4)return;
    int n0=col4*4;int g0=kt*gper,g1=min(ng,g0+gper);float a0=0,a1=0,a2=0,a3=0;
    for(int g=g0;g<g1;++g){const bf16* scg=sc+g*N+n0;const bf16* zrg=zr+g*N+n0;
        float s0=b2f(scg[0]),s1=b2f(scg[1]),s2=b2f(scg[2]),s3=b2f(scg[3]);
        float z0=b2f(zrg[0]),z1=b2f(zrg[1]),z2=b2f(zrg[2]),z3=b2f(zrg[3]);int r0=g*64;
        #pragma unroll 4
        for(int r=r0;r<r0+64;++r){uint32_t w=wq32[r*Nw+col4];float xa=x[2*r],xb=x[2*r+1];
            uint8_t b0=w&0xFF,b1=(w>>8)&0xFF,b2_=(w>>16)&0xFF,b3=(w>>24)&0xFF;
            a0+=xa*((float)(b0&0xF)-z0)*s0+xb*((float)((b0>>4)&0xF)-z0)*s0;
            a1+=xa*((float)(b1&0xF)-z1)*s1+xb*((float)((b1>>4)&0xF)-z1)*s1;
            a2+=xa*((float)(b2_&0xF)-z2)*s2+xb*((float)((b2_>>4)&0xF)-z2)*s2;
            a3+=xa*((float)(b3&0xF)-z3)*s3+xb*((float)((b3>>4)&0xF)-z3)*s3;}}
    if(ksplit==1){y[n0]=a0;y[n0+1]=a1;y[n0+2]=a2;y[n0+3]=a3;}
    else{atomicAdd(&y[n0],a0);atomicAdd(&y[n0+1],a1);atomicAdd(&y[n0+2],a2);atomicAdd(&y[n0+3],a3);}
}
__device__ __forceinline__ void zero_buf(float* y,int N){int gid=blockIdx.x*NT+threadIdx.x;for(int i=gid;i<N;i+=GRID)y[i]=0.f;}
// W: 0 mnorm, 1 router_w(bf16 [E,D]), 2 gate wq base,3 sc,4 zr (stride per expert = in/2*out etc precomputed? pass strides). We'll pass sep ptrs.
// Layout of W: [mnorm, router, gate_wq,gate_sc,gate_zr, up_wq,up_sc,up_zr, down_wq,down_sc,down_zr, sgate..., sup..., sdown...]
#define S_XN 0
#define S_ROUT D
#define S_H  (D+E)      /* hidden buf: [MI] gate, [MI] up, [D] downtmp */
#define S_OUT (S_H+2*MI+D)  /* moe out [D] */
__global__ void moe_k(const int64_t* W,float* hid,float* scr){
    cg::grid_group grid=cg::this_grid();
    int tid=threadIdx.x,gid=blockIdx.x*NT+tid;
    const bf16* mnorm=(const bf16*)W[0];
    if(blockIdx.x==0){
        float acc=0;for(int i=tid;i<D;i+=NT)acc+=hid[i]*hid[i];
        __shared__ float red[NT];red[tid]=acc;__syncthreads();
        for(int s=NT/2;s>0;s>>=1){if(tid<s)red[tid]+=red[tid+s];__syncthreads();}
        float inv=rsqrtf(red[0]/D+1e-6f);
        for(int i=tid;i<D;i+=NT)scr[S_XN+i]=hid[i]*inv*b2f(mnorm[i]);
    }
    grid.sync();
    // router logits [E] = xn @ router_w.T ; router_w [E,D]
    if(blockIdx.x==0){
        const bf16* rw=(const bf16*)W[1];
        for(int e=tid;e<E;e+=NT){ float acc=0; for(int i=0;i<D;i++) acc+=scr[S_XN+i]*b2f(rw[e*D+i]); scr[S_ROUT+e]=acc; }
    }
    grid.sync();
    // softmax over E, topk 8, normalize*ROUTED. Do on block0 single thread (E=64 small).
    __shared__ int topi[NACT]; __shared__ float topw[NACT];
    if(gid==0){
        float mx=-1e30f; for(int e=0;e<E;e++) mx=fmaxf(mx,scr[S_ROUT+e]);
        float sm=0; for(int e=0;e<E;e++){ float p=expf(scr[S_ROUT+e]-mx); scr[S_ROUT+e]=p; sm+=p; }
        for(int e=0;e<E;e++) scr[S_ROUT+e]/=sm;
        // topk 8
        float sumw=0;
        for(int j=0;j<NACT;j++){ float best=-1;int bi=-1; for(int e=0;e<E;e++){ if(scr[S_ROUT+e]>best){best=scr[S_ROUT+e];bi=e;} } topi[j]=bi; topw[j]=best; scr[S_ROUT+bi]=-2.f; sumw+=best; }
        for(int j=0;j<NACT;j++) topw[j]=topw[j]/(sumw+1e-9f)*ROUTED;
        // store to scr for all blocks
        for(int j=0;j<NACT;j++){ scr[S_ROUT+j]=topw[j]; ((int*)scr)[S_ROUT+NACT+j]=topi[j]; }
    }
    grid.sync();
    zero_buf(scr+S_OUT,D); grid.sync();
    // strides per expert for gate/up (in=D,out=MI): wq D/2*MI, sc/zr D/128*MI
    // down (in=MI,out=D): wq MI/2*D, sc/zr MI/128*D
    long gu_wq=(long)(D/2)*MI, gu_sz=(long)(D/128)*MI;
    long dn_wq=(long)(MI/2)*D, dn_sz=(long)(MI/128)*D;
    for(int j=0;j<NACT;j++){
        int e=((int*)scr)[S_ROUT+NACT+j]; float wj=scr[S_ROUT+j];
        // gate -> S_H via silu, up multiply. compute gate then up.
        zero_buf(scr+S_H,MI); grid.sync();
        gemv_i4(scr+S_XN,(const uint8_t*)W[2]+e*gu_wq,(const bf16*)W[3]+e*gu_sz,(const bf16*)W[4]+e*gu_sz,scr+S_H,D,MI); grid.sync();
        // silu in place, but need up too. put up in tmp region S_H+MI
        zero_buf(scr+S_H+MI,MI); grid.sync();
        gemv_i4(scr+S_XN,(const uint8_t*)W[5]+e*gu_wq,(const bf16*)W[6]+e*gu_sz,(const bf16*)W[7]+e*gu_sz,scr+S_H+MI,D,MI); grid.sync();
        for(int i=gid;i<MI;i+=GRID){ float g=scr[S_H+i]; float sig=g/(1.f+expf(-g)); scr[S_H+i]=sig*scr[S_H+MI+i]; }
        grid.sync();
        // down: in MI out D, accumulate wj*result into S_OUT. gemv writes atomically to a tmp then add. Use tmp S_H+2*MI [D].
        zero_buf(scr+S_H+2*MI,D); grid.sync();
        gemv_i4(scr+S_H,(const uint8_t*)W[8]+e*dn_wq,(const bf16*)W[9]+e*dn_sz,(const bf16*)W[10]+e*dn_sz,scr+S_H+2*MI,MI,D); grid.sync();
        for(int i=gid;i<D;i+=GRID) scr[S_OUT+i]+=wj*scr[S_H+2*MI+i];
        grid.sync();
    }
    // shared expert (1): W[11..13] gate,14..16 up,17..19 down
    {
        zero_buf(scr+S_H,MI); grid.sync();
        gemv_i4(scr+S_XN,(const uint8_t*)W[11],(const bf16*)W[12],(const bf16*)W[13],scr+S_H,D,MI); grid.sync();
        zero_buf(scr+S_H+MI,MI); grid.sync();
        gemv_i4(scr+S_XN,(const uint8_t*)W[14],(const bf16*)W[15],(const bf16*)W[16],scr+S_H+MI,D,MI); grid.sync();
        for(int i=gid;i<MI;i+=GRID){ float g=scr[S_H+i]; float sig=g/(1.f+expf(-g)); scr[S_H+i]=sig*scr[S_H+MI+i]; }
        grid.sync();
        zero_buf(scr+S_H+2*MI,D); grid.sync();
        gemv_i4(scr+S_H,(const uint8_t*)W[17],(const bf16*)W[18],(const bf16*)W[19],scr+S_H+2*MI,MI,D); grid.sync();
        for(int i=gid;i<D;i+=GRID) scr[S_OUT+i]+=scr[S_H+2*MI+i];
        grid.sync();
    }
    for(int i=gid;i<D;i+=GRID) hid[i]=scr[S_OUT+i];
}
torch::Tensor moe(int64_t Wtab,torch::Tensor hid,torch::Tensor scr){
    const int64_t* W=(const int64_t*)Wtab;float* h=hid.data_ptr<float>();float* s=scr.data_ptr<float>();
    void* args[]={(void*)&W,(void*)&h,(void*)&s};dim3 g(NB),b(NT);
    cudaLaunchCooperativeKernel((void*)moe_k,g,b,args,0,0);
    cudaError_t e=cudaDeviceSynchronize();if(e!=cudaSuccess)printf("err %s\n",cudaGetErrorString(e));
    return hid;
}
'''
mod=load_inline(name="dev_moe",cpp_sources=cpp,cuda_sources=src,functions=["moe"],extra_cuda_cflags=["-O3","-arch=sm_120"],verbose=False)

torch.manual_seed(0)
cfg=R.build_config({"n_experts":64})
m=R.Model(cfg).cuda().eval()
h=R.init_token(cfg,0)
blk=m.blocks[0]; moe=blk.moe
xn=R._rmsnorm(h,blk.moe_norm)
with torch.no_grad():
    o_t=moe.step(xn)
def eb(qe): return [qe.w_q.data_ptr(),qe.scales.data_ptr(),qe.zeros.data_ptr()]
W=[blk.moe_norm.data_ptr(), moe.router.weight.data_ptr()]
W+=eb(moe.gate)+eb(moe.up)+eb(moe.down)
W+=eb(moe.s_gate)+eb(moe.s_up)+eb(moe.s_down)
Wt=torch.tensor(W,dtype=torch.int64,device='cuda')
hid=h.float().clone()
scr=torch.zeros(2_000_000,device='cuda')
out=mod.moe(Wt.data_ptr(),hid,scr)
torch.cuda.synchronize()
print("moe out cos", F.cosine_similarity(o_t.float(),out.float(),dim=0).item())
