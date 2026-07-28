import torch, time
from torch.utils.cpp_extension import load_inline

cpp = "torch::Tensor gemv(torch::Tensor x, torch::Tensor wq, torch::Tensor sc, torch::Tensor zr, int64_t K, int64_t N, int64_t ksplit);"
src = r'''
#include <torch/extension.h>
#include <cuda_runtime.h>
#include <cuda_bf16.h>

// split-K: block (kt along y? ) grid.x = n tiles, grid.y = ksplit
__global__ void gemv_kernel(const float* __restrict__ x,
                            const uint8_t* __restrict__ wq,
                            const __nv_bfloat16* __restrict__ sc,
                            const __nv_bfloat16* __restrict__ zr,
                            float* __restrict__ y, int K, int N, int ksplit){
    int n = blockIdx.x*blockDim.x + threadIdx.x;
    int kt = blockIdx.y;
    int ng = K/128;
    int gper = (ng + ksplit -1)/ksplit;
    int g0 = kt*gper, g1 = min(ng, g0+gper);
    if(n>=N) return;
    float acc=0.f;
    for(int g=g0; g<g1; ++g){
        float s = __bfloat162float(sc[g*N+n]);
        float z = __bfloat162float(zr[g*N+n]);
        int r0=g*64;
        #pragma unroll 8
        for(int r=r0;r<r0+64;++r){
            uint8_t b=wq[r*N+n];
            acc += x[2*r]   * ((float)(b&0xF) - z)*s;
            acc += x[2*r+1] * ((float)((b>>4)&0xF)-z)*s;
        }
    }
    if(ksplit==1) y[n]=acc; else atomicAdd(&y[n], acc);
}

torch::Tensor gemv(torch::Tensor x, torch::Tensor wq, torch::Tensor sc, torch::Tensor zr, int64_t K, int64_t N, int64_t ksplit){
    auto y = torch::zeros({N}, torch::TensorOptions().dtype(torch::kFloat32).device(x.device()));
    int threads=256; dim3 blocks((N+threads-1)/threads, ksplit);
    gemv_kernel<<<blocks,threads>>>(x.data_ptr<float>(),
        (const uint8_t*)wq.data_ptr<uint8_t>(),
        (const __nv_bfloat16*)sc.data_ptr(), (const __nv_bfloat16*)zr.data_ptr(),
        y.data_ptr<float>(), K, N, ksplit);
    return y;
}
'''
mod = load_inline(name="gemv_test2", cpp_sources=cpp, cuda_sources=src, functions=["gemv"],
                  extra_cuda_cflags=["-O3","-arch=sm_120"], verbose=False)

import reference as R, torch.nn.functional as F
torch.manual_seed(0)
K,N=2304,4096
ql = R.QuantLinear(K,N).cuda()
g=torch.Generator(device='cpu').manual_seed(5); ql.init_random(g)
x = torch.randn(K, device='cuda')
W = ql.weight_bf().float(); y_ref = x @ W
for ks in (1,4,8,16):
    y = mod.gemv(x, ql.w_q, ql.scales, ql.zeros, K, N, ks)
    cos=F.cosine_similarity(y_ref,y,dim=0).item()
    for _ in range(5): mod.gemv(x, ql.w_q, ql.scales, ql.zeros, K, N, ks)
    torch.cuda.synchronize(); t0=time.perf_counter(); it=2000
    for _ in range(it): mod.gemv(x, ql.w_q, ql.scales, ql.zeros, K, N, ks)
    torch.cuda.synchronize(); dt=(time.perf_counter()-t0)/it
    print(f"ksplit={ks} cos {cos:.5f} {dt*1e6:.1f}us {K*N/2/dt/1e9:.0f} GB/s")
