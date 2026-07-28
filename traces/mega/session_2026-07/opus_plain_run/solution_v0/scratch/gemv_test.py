import torch, time
from torch.utils.cpp_extension import load_inline

cpp = "torch::Tensor gemv(torch::Tensor x, torch::Tensor wq, torch::Tensor sc, torch::Tensor zr, int64_t K, int64_t N);"
src = r'''
#include <torch/extension.h>
#include <cuda_runtime.h>
#include <cuda_bf16.h>

// y[n] = sum_k x[k]*(unpack(wq)[k,n]-zeros[g,n])*scales[g,n], g=k/128
// wq: (K/2,N) uint8, sc/zr: (K/128,N) bf16, x: (K,) fp32
__global__ void gemv_kernel(const float* __restrict__ x,
                            const uint8_t* __restrict__ wq,
                            const __nv_bfloat16* __restrict__ sc,
                            const __nv_bfloat16* __restrict__ zr,
                            float* __restrict__ y, int K, int N){
    extern __shared__ float xs[];
    for(int i=threadIdx.x;i<K;i+=blockDim.x) xs[i]=x[i];
    __syncthreads();
    int n = blockIdx.x*blockDim.x + threadIdx.x;
    if(n>=N) return;
    int Kh = K/2;
    int ng = K/128;
    float acc = 0.f;
    for(int g=0; g<ng; ++g){
        float s = __bfloat162float(sc[g*N+n]);
        float z = __bfloat162float(zr[g*N+n]);
        int r0 = g*64;
        #pragma unroll 4
        for(int r=r0; r<r0+64; ++r){
            uint8_t b = wq[r*N+n];
            float lo = (float)(b & 0xF);
            float hi = (float)((b>>4)&0xF);
            acc += xs[2*r]   * (lo - z) * s;
            acc += xs[2*r+1] * (hi - z) * s;
        }
    }
    y[n]=acc;
}

torch::Tensor gemv(torch::Tensor x, torch::Tensor wq, torch::Tensor sc, torch::Tensor zr, int64_t K, int64_t N){
    auto y = torch::empty({N}, torch::TensorOptions().dtype(torch::kFloat32).device(x.device()));
    int threads=256; int blocks=(N+threads-1)/threads;
    size_t shmem = K*sizeof(float);
    gemv_kernel<<<blocks,threads,shmem>>>(x.data_ptr<float>(),
        (const uint8_t*)wq.data_ptr<uint8_t>(),
        (const __nv_bfloat16*)sc.data_ptr(), (const __nv_bfloat16*)zr.data_ptr(),
        y.data_ptr<float>(), K, N);
    return y;
}
'''
mod = load_inline(name="gemv_test", cpp_sources=cpp, cuda_sources=src, functions=["gemv"],
                  extra_cuda_cflags=["-O3","-arch=sm_120"], verbose=False)

import reference as R
torch.manual_seed(0)
K,N=2304,4096
ql = R.QuantLinear(K,N).cuda()
g=torch.Generator(device='cpu').manual_seed(5); ql.init_random(g)
x = torch.randn(K, device='cuda')
W = ql.weight_bf().float()
y_ref = x @ W
y = mod.gemv(x, ql.w_q, ql.scales, ql.zeros, K, N)
import torch.nn.functional as F
print("cos", F.cosine_similarity(y_ref, y, dim=0).item(), "max abs err", (y-y_ref).abs().max().item(), "scale", y_ref.abs().mean().item())
# timing
for _ in range(5): mod.gemv(x, ql.w_q, ql.scales, ql.zeros, K, N)
torch.cuda.synchronize()
t0=time.perf_counter(); it=1000
for _ in range(it): mod.gemv(x, ql.w_q, ql.scales, ql.zeros, K, N)
torch.cuda.synchronize()
dt=(time.perf_counter()-t0)/it
print(f"gemv {dt*1e6:.1f}us  {K*N/2/dt/1e9:.0f} GB/s int4")
