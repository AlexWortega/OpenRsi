import os, torch
os.environ.setdefault("CUDA_HOME","/tmp/cudatk")
import megakernel_src as _mk
from torch.utils.cpp_extension import load_inline
MOD = load_inline(name="kimi_occ", cpp_sources=_mk.CPP + "\nint get_nb();\n",
    cuda_sources=_mk.CUDA + r"""
int get_nb(){
  int numSM=0,dev=0; cudaGetDevice(&dev);
  cudaDeviceGetAttribute(&numSM,cudaDevAttrMultiProcessorCount,dev);
  size_t shmem=8192*sizeof(float);
  cudaFuncSetAttribute((void*)mega_kernel,cudaFuncAttributeMaxDynamicSharedMemorySize,shmem);
  int perSM=0; cudaOccupancyMaxActiveBlocksPerMultiprocessor(&perSM,(void*)mega_kernel,NT,shmem);
  cudaFuncAttributes a; cudaFuncGetAttributes(&a,(void*)mega_kernel);
  printf("numSM=%d perSM=%d nregs=%d shmem_static=%zu maxthreads=%d\n",numSM,perSM,a.numRegs,a.sharedSizeBytes,a.maxThreadsPerBlock);
  return numSM*perSM;
}
""",
    functions=["mega_launch","get_nb"],
    extra_cuda_cflags=["-O3","-arch=sm_120","--use_fast_math"], verbose=False)
print("nb=",MOD.get_nb())
