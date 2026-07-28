# OpenRSI KernelBench-Mega (scaffold-RSI) results

Champion scaffold v0, mean geomean speedup: **1.955x**
Baseline (gen0): 1.955x  |  RSI delta: +0.000x

Edit mode: bounded  |  per-solve budget: 2880min
Total OpenRouter cost: $50.38

## Champion domain knowledge
- Diagnose WHY it's slow before changing anything: is it memory-bandwidth bound or compute bound? For decode / small-batch, it is usually bandwidth-bound on the weight stream — the fix is to move fewer bytes, not do fewer flops.
- If weights are quantized (int4/int8/W4A16/AWQ/GPTQ style), the #1 speed bug is MATERIALIZING the dequantized full-precision weight then matmul-ing — that throws away the quantization bandwidth win. FUSE the dequant directly into the GEMV/matmul so quantized weights stream once and are never expanded in memory. A kernel that dequantizes-to-full-then-matmuls is almost always <= 1x.
- Parallelize the independent work across GPU blocks/warps: experts in an MoE, heads in attention, rows/tiles of a matmul. A correct-but-serial kernel (one block doing everything) can be ~10x slower than baseline — expose the parallelism.
- Standard GPU levers, in order of usual impact: coalesced global memory access; stage reused data (scales, small operands) in shared memory; block/tile sizes that are multiples of the warp (32) with good occupancy; minimize register spills; mixed precision where tolerance allows. Profile the slowest op and target IT — do not guess.
- Fewer kernel launches only helps if you were launch-bound; fusing into one launch gives NO speedup by itself unless the fused kernel also removes the real bottleneck (bandwidth/parallelism). Don't confuse 'one launch' with 'fast'.
- Incremental fusion beats big-bang: pass a simple correct version first, then fuse/optimize ONE stage at a time, re-checking correctness after each — an ambitious all-at-once fused kernel from scratch is correctness-fragile and often lands just under the tolerance gate.
- Match the reference's parameter names / dtypes / layouts exactly so weights load and the correctness gate compares apples to apples; read the reference for the precise quant format, group size, and epsilon rather than assuming.
