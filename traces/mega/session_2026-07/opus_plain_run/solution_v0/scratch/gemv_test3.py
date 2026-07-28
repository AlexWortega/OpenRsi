import torch, time
from torch.utils.cpp_extension import load_inline

cpp = "torch::Tensor gemv(torch::Tensor x, torch::Tensor wq, torch::Tensor sc, torch::Tensor zr, int64_t K, int64_t N, int64_t ksplit);"
src = r'''
#include <torch/extension.h>
#include <cuda_runtime.h>
#include <cuda_bf16.h>
// each thread handles 4 consecutive columns via uint32 loads
__global__ void gemv_kernel(const float* __restrict__ x,
                            const uint8_t* __restrict__ wq,
                            const __nv_bfloat16* __restrict__ sc,
                            const __nv_bfloat16* __restrict__ zr,
                            float* __restrict__ y, int K, int N, int ksplit){
    int col4 = blockIdx.x*blockDim.x + threadIdx.x;   // which group of 4 cols
    int n0 = col4*4;
    int kt = blockIdx.y;
    int ng = K/128;
    int gper = (ng + ksplit -1)/ksplit;
    int g0 = kt*gper, g1 = min(ng, g0+gper);
    if(n0>=N) return;
    const uint32_t* wq32 = (const uint32_t*)wq;   // stride N/4 per row
    int Nw = N/4;
    float acc0=0,acc1=0,acc2=0,acc3=0;
    for(int g=g0; g<g1; ++g){
        const __nv_bfloat16* scg = sc + g*N + n0;
        const __nv_bfloat16* zrg = zr + g*N + n0;
        float s0=__bfloat162float(scg[0]),s1=__bfloat162float(scg[1]),s2=__bfloat162float(scg[2]),s3=__bfloat162float(scg[3]);
        float z0=__bfloat162float(zrg[0]),z1=__bfloat162float(zrg[1]),z2=__bfloat162float(zrg[2]),z3=__bfloat162float(zrg[3]);
        int r0=g*64;
        #pragma unroll 4
        for(int r=r0;r<r0+64;++r){
            uint32_t w = wq32[r*Nw + col4];
            float xa = x[2*r], xb = x[2*r+1];
            uint8_t b0=w&0xFF, b1=(w>>8)&0xFF, b2=(w>>16)&0xFF, b3=(w>>24)&0xFF;
            acc0 += xa*((float)(b0&0xF)-z0)*s0 + xb*((float)((b0>>4)&0xF)-z0)*s0;
            acc1 += xa*((float)(b1&0xF)-z1)*s1 + xb*((float)((b1>>4)&0xF)-z1)*s1;
            acc2 += xa*((float)(b2&0xF)-z2)*s2 + xb*((float)((b2>>4)&0xF)-z2)*s2;
            acc3 += xa*((float)(b3&0xF)-z3)*s3 + xb*((float)((b3>>4)&0xF)-z3)*s3;
        }
    }
    if(ksplit==1){ y[n0]=acc0;y[n0+1]=acc1;y[n0+2]=acc2;y[n0+3]=acc3; }
    else { atomicAdd(&y[n0],acc0);atomicAdd(&y[n0+1],acc1);atomicAdd(&y[n0+2],acc2);atomicAdd(&y[n0+3],acc3); }
}
torch::Tensor gemv(torch::Tensor x, torch::Tensor wq, torch::Tensor sc, torch::Tensor zr, int64_t K, int64_t N, int64_t ksplit){
    auto y = torch::zeros({N}, torch::TensorOptions().dtype(torch::kFloat32).device(x.device()));
    int threads=256; int ncol4=N/4; dim3 blocks((ncol4+threads-1)/threads, ksplit);
    gemv_kernel<<<blocks,threads>>>(x.data_ptr<float>(),(const uint8_t*)wq.data_ptr<uint8_t>(),
        (const __nv_bfloat16*)sc.data_ptr(),(const __nv_bfloat16*)zr.data_ptr(),y.data_ptr<float>(),K,N,ksplit);
    return y;
}
'''
mod = load_inline(name="gemv_test3", cpp_sources=cpp, cuda_sources=src, functions=["gemv"],
                  extra_cuda_cflags=["-O3","-arch=sm_120"], verbose=False)
import reference as R, torch.nn.functional as F
torch.manual_seed(0)
K,N=2304,4096
ql = R.QuantLinear(K,N).cuda(); g=torch.Generator(device='cpu').manual_seed(5); ql.init_random(g)
x = torch.randn(K, device='cuda'); W=ql.weight_bf().float(); y_ref=x@W
for ks in (8,16,24,32,48):
    y = mod.gemv(x, ql.w_q, ql.scales, ql.zeros, K, N, ks)
    cos=F.cosine_similarity(y_ref,y,dim=0).item()
    for _ in range(5): mod.gemv(x, ql.w_q, ql.scales, ql.zeros, K, N, ks)
    torch.cuda.synchronize(); t0=time.perf_counter(); it=2000
    for _ in range(it): mod.gemv(x, ql.w_q, ql.scales, ql.zeros, K, N, ks)
    torch.cuda.synchronize(); dt=(time.perf_counter()-t0)/it
    print(f"ksplit={ks} cos {cos:.5f} {dt*1e6:.1f}us {K*N/2/dt/1e9:.0f} GB/s")
