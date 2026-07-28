import os
import time
import torch
import torch.nn.functional as F

if "CUDA_HOME" not in os.environ:
    os.environ["CUDA_HOME"] = "/tmp/cudatk"

_CUDA_SRC = r'''
#include <torch/extension.h>
#include <ATen/cuda/CUDAContext.h>
#include <cuda_bf16.h>
#include <cuda_runtime.h>

using bf = __nv_bfloat16;
__device__ __forceinline__ float b2f(bf x){ return __bfloat162float(x); }
__device__ __forceinline__ bf f2b(float x){ return __float2bfloat16_rn(x); }

__device__ __forceinline__ float get_w(const unsigned char* w,
                                        const bf* s, const bf* z,
                                        int k, int n, int N){
    unsigned v = w[(k>>1)*N + n];
    v = (k & 1) ? (v >> 4) : (v & 15);
    return (float(v) - b2f(z[(k>>7)*N + n])) * b2f(s[(k>>7)*N + n]);
}

__global__ void int4gemv_warp_kernel(const unsigned char* __restrict__ w,
                                         const bf* __restrict__ s,
                                         const bf* __restrict__ z,
                                         const bf* __restrict__ x,
                                         bf* __restrict__ y,
                                         int M, int K, int N){
    int warp_id = threadIdx.x >> 5;
    int lane = threadIdx.x & 31;
    int n = blockIdx.x * (blockDim.x >> 5) + warp_id;
    int m = blockIdx.y;
    if (n >= N || m >= M) return;
    float acc = 0.0f;
    const bf* xm = x + m * K;
    #pragma unroll 4
    for (int k = lane; k < K; k += 32){
        acc = fmaf(b2f(xm[k]), get_w(w, s, z, k, n, N), acc);
    }
    #pragma unroll
    for (int offset = 16; offset > 0; offset >>= 1){
        acc += __shfl_down_sync(0xFFFFFFFF, acc, offset);
    }
    if (lane == 0){
        y[m * N + n] = f2b(acc);
    }
}

torch::Tensor int4gemv_warp(torch::Tensor w_q, torch::Tensor scales,
                            torch::Tensor zeros, torch::Tensor x){
    cudaStream_t stream = at::cuda::getCurrentCUDAStream();
    int M = x.size(0);
    int K = x.size(1);
    int N = w_q.size(1);
    auto y = torch::empty({M, N}, x.options());
    dim3 grid((N + 3) / 4, M);  // 4 outputs per block (128 threads / 32)
    int4gemv_warp_kernel<<<grid, 128, 0, stream>>>(
        w_q.data_ptr<uint8_t>(),
        reinterpret_cast<const bf*>(scales.data_ptr<at::BFloat16>()),
        reinterpret_cast<const bf*>(zeros.data_ptr<at::BFloat16>()),
        reinterpret_cast<const bf*>(x.data_ptr<at::BFloat16>()),
        reinterpret_cast<bf*>(y.data_ptr<at::BFloat16>()),
        M, K, N);
    C10_CUDA_KERNEL_LAUNCH_CHECK();
    return y;
}

torch::Tensor int4gemv(torch::Tensor w_q, torch::Tensor scales,
                       torch::Tensor zeros, torch::Tensor x){
    return int4gemv_warp(w_q, scales, zeros, x);
}
'''

from torch.utils.cpp_extension import load_inline
import shutil, pathlib
cache_dir = pathlib.Path.home() / '.cache' / 'torch_extensions' / 'py312_cu129' / 'int4gemv_test2'
shutil.rmtree(str(cache_dir), ignore_errors=True)
_ext = load_inline(
    name='int4gemv_test2',
    cpp_sources='torch::Tensor int4gemv(torch::Tensor, torch::Tensor, torch::Tensor, torch::Tensor);',
    cuda_sources=_CUDA_SRC,
    functions=['int4gemv'],
    extra_cuda_cflags=['-arch=sm_120', '-O3', '--use_fast_math'],
    verbose=True,
)
print('compiled', flush=True)

# correctness + speed for KDA output-like shape
from solution import QuantLinear
K, N = 4096, 2304
ql = QuantLinear(K, N).cuda()
ql.init_random(torch.Generator(device='cpu').manual_seed(1))
x = torch.randn(K, device='cuda', dtype=torch.bfloat16)

# correctness
y = _ext.int4gemv(ql.w_q, ql.scales, ql.zeros, x.unsqueeze(0)).squeeze(0)
y_ref = x @ ql.weight_bf()
cos = torch.nn.functional.cosine_similarity(y_ref.float(), y.float(), dim=0).item()
print('cos', cos, flush=True)

# benchmark
torch.cuda.synchronize()
nt = 500
for _ in range(50):  # warmup
    y = _ext.int4gemv(ql.w_q, ql.scales, ql.zeros, x.unsqueeze(0)).squeeze(0)
torch.cuda.synchronize()
t0 = time.perf_counter()
for _ in range(nt):
    y = _ext.int4gemv(ql.w_q, ql.scales, ql.zeros, x.unsqueeze(0)).squeeze(0)
torch.cuda.synchronize()
t_int4 = (time.perf_counter() - t0) / nt * 1e6

# bf16 ref
W = ql.weight_bf().t().contiguous()
for _ in range(50):
    y_ref = F.linear(x, W)
torch.cuda.synchronize()
t0 = time.perf_counter()
for _ in range(nt):
    y_ref = F.linear(x, W)
torch.cuda.synchronize()
t_bf16 = (time.perf_counter() - t0) / nt * 1e6
print(f'KDA output-like int4 {t_int4:.1f} us  bf16 {t_bf16:.1f} us  ratio {t_bf16/t_int4:.2f}x')
