import torch, time
from torch.utils.cpp_extension import load_inline
cpp = "void run(torch::Tensor x, int64_t iters, int64_t blocks, int64_t threads);"
src = r'''
#include <torch/extension.h>
#include <cuda_runtime.h>
#include <cooperative_groups.h>
namespace cg = cooperative_groups;
__global__ void k(float* x, int iters){
    cg::grid_group grid = cg::this_grid();
    int t=blockIdx.x*blockDim.x+threadIdx.x;
    for(int i=0;i<iters;i++){ if(t==0)x[0]+=1.0f; grid.sync(); }
}
void run(torch::Tensor x, int64_t iters, int64_t blocks, int64_t threads){
    float* p=x.data_ptr<float>(); int it=iters;
    void* args[]={(void*)&p,(void*)&it};
    dim3 g(blocks),b(threads);
    cudaLaunchCooperativeKernel((void*)k,g,b,args,0,0);
    cudaDeviceSynchronize();
}
'''
mod=load_inline(name="sync_test",cpp_sources=cpp,cuda_sources=src,functions=["run"],extra_cuda_cflags=["-O3","-arch=sm_120"],verbose=False)
x=torch.zeros(16,device='cuda')
for blocks in (188,376):
    for threads in (256,512):
        mod.run(x,10,blocks,threads); torch.cuda.synchronize()
        t0=time.perf_counter(); N=20000
        mod.run(x,N,blocks,threads); torch.cuda.synchronize()
        dt=(time.perf_counter()-t0)/N
        print(f"blocks={blocks} threads={threads}: {dt*1e6:.3f} us/sync")
