import torch, time
from torch.utils.cpp_extension import load_inline
cpp = "torch::Tensor run(torch::Tensor x, torch::Tensor wq, torch::Tensor sc, torch::Tensor zr, int64_t K, int64_t N, int64_t iters);"
src = r'''
#include <torch/extension.h>
#include <cuda_runtime.h>
#include <cuda_bf16.h>
#include <cooperative_groups.h>
namespace cg=cooperative_groups;
#define NB 188
#define NT 256
// persistent cooperative grid does one GEMV (split-K + atomics) `iters` times
__global__ void mgk(const float* __restrict__ x, const uint8_t* __restrict__ wq,
    const __nv_bfloat16* __restrict__ sc, const __nv_bfloat16* __restrict__ zr,
    float* __restrict__ y, int K, int N, int iters){
    cg::grid_group grid=cg::this_grid();
    const uint32_t* wq32=(const uint32_t*)wq; int Nw=N/4; int ncol4=N/4; int ng=K/128;
    // choose ksplit so col_blocks*ksplit ~ NB
    int col_blocks=(ncol4+NT-1)/NT;
    int ksplit=NB/col_blocks; if(ksplit<1)ksplit=1;
    int gper=(ng+ksplit-1)/ksplit;
    int bid=blockIdx.x;
    int cb=bid % col_blocks; int kt=bid / col_blocks;
    for(int it=0; it<iters; ++it){
        // zero
        for(int i=bid*NT+threadIdx.x; i<N; i+=NB*NT) y[i]=0.f;
        grid.sync();
        if(kt<ksplit){
            int col4 = cb*NT + threadIdx.x;
            if(col4<ncol4){
                int n0=col4*4;
                int g0=kt*gper, g1=min(ng,g0+gper);
                float a0=0,a1=0,a2=0,a3=0;
                for(int g=g0;g<g1;++g){
                    const __nv_bfloat16* scg=sc+g*N+n0; const __nv_bfloat16* zrg=zr+g*N+n0;
                    float s0=__bfloat162float(scg[0]),s1=__bfloat162float(scg[1]),s2=__bfloat162float(scg[2]),s3=__bfloat162float(scg[3]);
                    float z0=__bfloat162float(zrg[0]),z1=__bfloat162float(zrg[1]),z2=__bfloat162float(zrg[2]),z3=__bfloat162float(zrg[3]);
                    int r0=g*64;
                    #pragma unroll 4
                    for(int r=r0;r<r0+64;++r){
                        uint32_t w=wq32[r*Nw+col4]; float xa=x[2*r],xb=x[2*r+1];
                        uint8_t b0=w&0xFF,b1=(w>>8)&0xFF,b2=(w>>16)&0xFF,b3=(w>>24)&0xFF;
                        a0+=xa*((float)(b0&0xF)-z0)*s0+xb*((float)((b0>>4)&0xF)-z0)*s0;
                        a1+=xa*((float)(b1&0xF)-z1)*s1+xb*((float)((b1>>4)&0xF)-z1)*s1;
                        a2+=xa*((float)(b2&0xF)-z2)*s2+xb*((float)((b2>>4)&0xF)-z2)*s2;
                        a3+=xa*((float)(b3&0xF)-z3)*s3+xb*((float)((b3>>4)&0xF)-z3)*s3;
                    }
                    __syncwarp();
                }
                atomicAdd(&y[n0],a0);atomicAdd(&y[n0+1],a1);atomicAdd(&y[n0+2],a2);atomicAdd(&y[n0+3],a3);
            }
        }
        grid.sync();
    }
}
torch::Tensor run(torch::Tensor x, torch::Tensor wq, torch::Tensor sc, torch::Tensor zr, int64_t K, int64_t N, int64_t iters){
    auto y=torch::zeros({N},torch::TensorOptions().dtype(torch::kFloat32).device(x.device()));
    const float* xp=x.data_ptr<float>(); const uint8_t* wqp=(const uint8_t*)wq.data_ptr<uint8_t>();
    const __nv_bfloat16* scp=(const __nv_bfloat16*)sc.data_ptr(); const __nv_bfloat16* zrp=(const __nv_bfloat16*)zr.data_ptr();
    float* yp=y.data_ptr<float>(); int Ki=K,Ni=N,iti=iters;
    void* args[]={(void*)&xp,(void*)&wqp,(void*)&scp,(void*)&zrp,(void*)&yp,(void*)&Ki,(void*)&Ni,(void*)&iti};
    dim3 g(NB),b(NT); cudaLaunchCooperativeKernel((void*)mgk,g,b,args,0,0); cudaDeviceSynchronize();
    return y;
}
'''
mod=load_inline(name="persistent_gemv",cpp_sources=cpp,cuda_sources=src,functions=["run"],extra_cuda_cflags=["-O3","-arch=sm_120"],verbose=False)
import reference as R, torch.nn.functional as F
torch.manual_seed(0)
for (K,N) in [(2304,16384),(2304,1024),(1024,2304),(4096,2304),(512,8192)]:
    ql=R.QuantLinear(K,N).cuda(); g=torch.Generator(device='cpu').manual_seed(5); ql.init_random(g)
    x=torch.randn(K,device='cuda'); W=ql.weight_bf().float(); y_ref=x@W
    y=mod.run(x,ql.w_q,ql.scales,ql.zeros,K,N,1); cos=F.cosine_similarity(y_ref,y,dim=0).item()
    torch.cuda.synchronize(); it=300; t0=time.perf_counter()
    y=mod.run(x,ql.w_q,ql.scales,ql.zeros,K,N,it); torch.cuda.synchronize()
    dt=(time.perf_counter()-t0)/it
    print(f"K={K} N={N} cos {cos:.5f} {dt*1e6:.1f}us {K*N/2/dt/1e9:.0f} GB/s")
