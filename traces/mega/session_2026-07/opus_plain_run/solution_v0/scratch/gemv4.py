import os; os.environ.setdefault("CUDA_HOME","/tmp/cudatk")
import torch,time,torch.nn.functional as F
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
// variant 0: uint32 (4 cols) + shared x ; variant 2: uint4 (8 cols=2xuint32... actually 16 nibbles=... let's do 8 cols) + shared x
__global__ void bk(const float* x0,const int64_t* wqs,const int64_t* scs,const int64_t* zrs,
                   float* y,int K,int N,int nj,int iters,int variant){
    cg::grid_group grid=cg::this_grid();
    int ng=K/128,Nw=N/4;
    extern __shared__ float xsh[];
    // variant 2: 8 cols per thread -> ncol8=N/8
    int cols_per = (variant==2)?8:4;
    int ncolT=N/cols_per;
    int col_blocks=(ncolT+NT-1)/NT;int total_cb=col_blocks*nj;
    int ksplit=NB/total_cb;if(ksplit<1)ksplit=1;int gper=(ng+ksplit-1)/ksplit;int bid=blockIdx.x;
    for(int it=0;it<iters;it++){
        for(int i=bid*NT+threadIdx.x;i<nj*N;i+=NB*NT)y[i]=0.f;
        grid.sync();
        bool active=bid<total_cb*ksplit;
        int within=0,kt=0,j=0,cb=0,g0=0,g1=0,kbeg=0; const float* x=x0;
        if(active){within=bid%total_cb;kt=bid/total_cb;j=within/col_blocks;cb=within%col_blocks;g0=kt*gper;g1=min(ng,g0+gper);kbeg=g0*128;
            for(int i=threadIdx.x;i<(g1-g0)*128;i+=NT)xsh[i]=x[kbeg+i];}
        __syncthreads();
        int colT=cb*NT+threadIdx.x;
        if(active&&j<nj&&colT<ncolT){
            const uint8_t* wqb=(const uint8_t*)wqs[j];const bf16* sc=(const bf16*)scs[j];const bf16* zr=(const bf16*)zrs[j];
            if(variant==2){
                const uint64_t* wq64=(const uint64_t*)wqb; int Nw8=N/8;
                int n0=colT*8;
                float a[8]; for(int t=0;t<8;t++)a[t]=0;
                for(int g=g0;g<g1;++g){
                    const bf16* scg=sc+g*N+n0; const bf16* zrg=zr+g*N+n0;
                    float s[8],z[8];
                    #pragma unroll
                    for(int t=0;t<8;t++){s[t]=b2f(scg[t]);z[t]=b2f(zrg[t]);}
                    int r0=g*64;
                    #pragma unroll 4
                    for(int r=r0;r<r0+64;++r){
                        uint64_t w=wq64[r*Nw8+colT];float xa=xsh[2*r-kbeg],xb=xsh[2*r+1-kbeg];
                        #pragma unroll
                        for(int t=0;t<8;t++){uint8_t b=(w>>(8*t))&0xFF; a[t]+=xa*((float)(b&0xF)-z[t])*s[t]+xb*((float)((b>>4)&0xF)-z[t])*s[t];}
                    }
                }
                #pragma unroll
                for(int t=0;t<8;t++) atomicAdd(&y[j*N+n0+t],a[t]);
            } else {
                const uint32_t* wq32=(const uint32_t*)wqb;
                int n0=colT*4; float a0=0,a1=0,a2=0,a3=0;
                for(int g=g0;g<g1;++g){const bf16* scg=sc+g*N+n0;const bf16* zrg=zr+g*N+n0;
                    float s0=b2f(scg[0]),s1=b2f(scg[1]),s2=b2f(scg[2]),s3=b2f(scg[3]);
                    float z0=b2f(zrg[0]),z1=b2f(zrg[1]),z2=b2f(zrg[2]),z3=b2f(zrg[3]);int r0=g*64;
                    #pragma unroll 4
                    for(int r=r0;r<r0+64;++r){uint32_t w=wq32[r*Nw+colT];float xa=xsh[2*r-kbeg],xb=xsh[2*r+1-kbeg];
                        uint8_t b0=w&0xFF,b1=(w>>8)&0xFF,b2_=(w>>16)&0xFF,b3=(w>>24)&0xFF;
                        a0+=xa*((float)(b0&0xF)-z0)*s0+xb*((float)((b0>>4)&0xF)-z0)*s0;
                        a1+=xa*((float)(b1&0xF)-z1)*s1+xb*((float)((b1>>4)&0xF)-z1)*s1;
                        a2+=xa*((float)(b2_&0xF)-z2)*s2+xb*((float)((b2_>>4)&0xF)-z2)*s2;
                        a3+=xa*((float)(b3&0xF)-z3)*s3+xb*((float)((b3>>4)&0xF)-z3)*s3;}}
                atomicAdd(&y[j*N+n0],a0);atomicAdd(&y[j*N+n0+1],a1);atomicAdd(&y[j*N+n0+2],a2);atomicAdd(&y[j*N+n0+3],a3);
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
mod=load_inline(name="gemv4",cpp_sources=cpp,cuda_sources=src,functions=["run"],extra_cuda_cflags=["-O3","-arch=sm_120","--use_fast_math"],verbose=False)
data=torch.load('/tmp/gemv_w.pt')
def dequant(wq,sc,zr,K,N):
    wu=torch.empty((K,N),dtype=torch.uint8); wu[0::2]=wq&0xF; wu[1::2]=(wq>>4)&0xF
    s=sc.repeat_interleave(128,0); z=zr.repeat_interleave(128,0)
    return (wu.to(torch.float32)-z.float())*s.float()
for tag,nj in [('gu',18),('dn',9),('kda',4),('ko',1)]:
    wq,sc,zr,K,N=data[tag]; wq=wq.cuda();sc=sc.cuda();zr=zr.cuda()
    x=torch.randn(K,device='cuda'); W=dequant(*data[tag][:3],K,N).cuda(); y_ref=torch.cat([x@W]*nj)
    wqs=torch.tensor([wq.data_ptr()]*nj,dtype=torch.int64,device='cuda')
    scs=torch.tensor([sc.data_ptr()]*nj,dtype=torch.int64,device='cuda')
    zrs=torch.tensor([zr.data_ptr()]*nj,dtype=torch.int64,device='cuda')
    for var in (0,2):
        y=mod.run(x,wqs,scs,zrs,K,N,nj,1,var); cos=F.cosine_similarity(y_ref,y,dim=0).item()
        torch.cuda.synchronize();it=1000;t0=time.perf_counter()
        mod.run(x,wqs,scs,zrs,K,N,nj,it,var);torch.cuda.synchronize();dt=(time.perf_counter()-t0)/it
        print(f"{tag} K={K} N={N} nj={nj} var{var} cos {cos:.4f} {dt*1e6:.1f}us {nj*K*N/2/dt/1e9:.0f} GB/s")
