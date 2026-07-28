import torch
from torch.utils.cpp_extension import load_inline
cpp = "void run(torch::Tensor x);"
src = r'''
#include <torch/extension.h>
#include <cuda_runtime.h>
#include <cooperative_groups.h>
namespace cg = cooperative_groups;
__global__ void coopk(float* x, int n){
    cg::grid_group grid = cg::this_grid();
    int t = blockIdx.x*blockDim.x+threadIdx.x;
    if(t<n) x[t]+=1.0f;
    grid.sync();
    if(t<n) x[t]*=2.0f;
}
void run(torch::Tensor x){
    int n = x.numel();
    int threads=256; int blocks=(n+threads-1)/threads;
    float* p = x.data_ptr<float>();
    void* kargs[] = {(void*)&p, (void*)&n};
    dim3 g(blocks), b(threads);
    cudaError_t e = cudaLaunchCooperativeKernel((void*)coopk, g, b, kargs, 0, 0);
    if(e!=cudaSuccess) printf("launch err %s\n", cudaGetErrorString(e));
    cudaDeviceSynchronize();
}
'''
mod = load_inline(name="coop_test", cpp_sources=cpp, cuda_sources=src, functions=["run"], extra_cuda_cflags=["-O2","-arch=sm_120"], verbose=False)
x = torch.zeros(1000, device='cuda')
mod.run(x)
torch.cuda.synchronize()
print("result", x[:5].tolist(), "expected 2.0")
# check max blocks for cooperative launch
import ctypes
print("SMs", torch.cuda.get_device_properties(0).multi_processor_count)
