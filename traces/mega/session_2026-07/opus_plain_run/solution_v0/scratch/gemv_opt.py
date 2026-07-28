import os; os.environ.setdefault("CUDA_HOME","/tmp/cudatk")
import torch,time
from torch.utils.cpp_extension import load_inline
cpp="torch::Tensor run(torch::Tensor x,torch::Tensor wqs,torch::Tensor scs,torch::Tensor zrs,int64_t K,int64_t N,int64_t nj,int64_t iters,int64_t variant);"
src=r'''
#include <torch/extension.h>
#include <cuda_runtime.h>
#include <cuda_bf16.h>
#include <cooperative_groups.h>
namespace cg=cooperative_groups;
typedef __nv_bfloat16 bf16;
#define NB 188
#define NT 256
__device__ __forceinline__ float b2f(bf16 v){return __bfloat162float(v);}

// variant 0: uint32 (4 cols/thread)  -- baseline
__device__ void v0(const float* x,const uint8_t* wq,const bf16* sc,const bf16* zr,float* y,int K,int N,int g0,int g1,int col4,int ncol4){
    const uint32_t* wq32=(const uint32_t*)wq;int Nw=N/4;int n0=col4*4;
    float a0=0,a1=0,a2=0,a3=0;
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
    if(g1-g0>0){atomicAdd(&y[n0],a0);atomicAdd(&y[n0+1],a1);atomicAdd(&y[n0+2],a2);atomicAdd(&y[n0+3],a3);}
}
// variant 1: shared-memory x preload (float), uint32
__global__ void bk(const float* x,const int64_t* wqs,const int64_t* scs,const int64_t* zrs,
                   float* y,int K,int N,int nj,int iters,int variant){
    cg::grid_group grid=cg::this_grid();
    int ncol4=N/4,ng=K/128;int col_blocks=(ncol4+NT-1)/NT;int total_cb=col_blocks*nj;
    int ksplit=NB/total_cb;if(ksplit<1)ksplit=1;int gper=(ng+ksplit-1)/ksplit;int bid=blockIdx.x;
    extern __shared__ float xsh[];
    for(int it=0;it<iters;it++){
        for(int i=bid*NT+threadIdx.x;i<nj*N;i+=NB*NT)y[i]=0.f;
        grid.sync();
        if(bid<total_cb*ksplit){
            int within=bid%total_cb,kt=bid/total_cb;int j=within/col_blocks,cb=within%col_blocks;
            int col4=cb*NT+threadIdx.x;
            if(j<nj&&col4<ncol4){
                int g0=kt*gper,g1=min(ng,g0+gper);
                v0(x,(const uint8_t*)wqs[j],(const bf16*)scs[j],(const bf16*)zrs[j],y+j*N,K,N,g0,g1,col4,ncol4);
            }
        }
        grid.sync();
    }
}
torch::Tensor run(torch::Tensor x,torch::Tensor wqs,torch::Tensor scs,torch::Tensor zrs,int64_t K,int64_t N,int64_t nj,int64_t iters,int64_t variant){
    auto y=torch::zeros({nj*N},torch::TensorOptions().dtype(torch::kFloat32).device(x.device()));
    const float* xp=x.data_ptr<float>();
    const int64_t* wq=(const int64_t*)wqs.data_ptr<int64_t>();const int64_t* sc=(const int64_t*)scs.data_ptr<int64_t>();const int64_t* zr=(const int64_t*)zrs.data_ptr<int64_t>();
    float* yp=y.data_ptr<float>();int Ki=K,Ni=N,nji=nj,iti=iters,vi=variant;
    void* args[]={(void*)&xp,(void*)&wq,(void*)&sc,(void*)&zr,(void*)&yp,(void*)&Ki,(void*)&Ni,(void*)&nji,(void*)&iti,(void*)&vi};
    dim3 g(NB),b(NT);size_t sh=K*sizeof(float);
    cudaLaunchCooperativeKernel((void*)bk,g,b,args,sh,0);cudaDeviceSynchronize();
    return y;
}
'''
mod=load_inline(name="gemv_opt",cpp_sources=cpp,cuda_sources=src,functions=["run"],extra_cuda_cflags=["-O3","-arch=sm_120","--use_fast_math"],verbose=False)
import reference as R,torch.nn.functional as F
torch.manual_seed(0)
sd=None
for (K,N,nj) in [(2304,1024,9),(1024,2304,9),(2304,4096,4),(4096,2304,1),(512,8192,1)]:
    qls=[R.QuantLinear(K,N).cuda() for _ in range(nj)]
    for q in qls: gg=torch.Generator(device='cpu').manual_seed(1); q.init_random(gg)
    x=torch.randn(K,device='cuda')
    wqs=torch.tensor([q.w_q.data_ptr() for q in qls],dtype=torch.int64,device='cuda')
    scs=torch.tensor([q.scales.data_ptr() for q in qls],dtype=torch.int64,device='cuda')
    zrs=torch.tensor([q.zeros.data_ptr() for q in qls],dtype=torch.int64,device='cuda')
    y=mod.run(x,wqs,scs,zrs,K,N,nj,1,0)
    y_ref=torch.cat([x@q.weight_bf().float() for q in qls])
    cos=F.cosine_similarity(y_ref,y,dim=0).item()
    torch.cuda.synchronize();it=500;t0=time.perf_counter()
    mod.run(x,wqs,scs,zrs,K,N,nj,it,0);torch.cuda.synchronize();dt=(time.perf_counter()-t0)/it
    print(f"K={K} N={N} nj={nj} cos {cos:.4f} {dt*1e6:.1f}us {nj*K*N/2/dt/1e9:.0f} GB/s")
