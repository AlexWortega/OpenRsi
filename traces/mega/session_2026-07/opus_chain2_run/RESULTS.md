# OpenRSI KernelBench-Mega (scaffold-RSI) results

Champion scaffold v0, mean geomean speedup: **23.178x**
Baseline (gen0): 23.178x  |  RSI delta: +0.000x

Edit mode: bounded  |  per-solve budget: 960min
Total OpenRouter cost: $75.02

## Champion domain knowledge
- The dominant cost at batch-1 decode is usually LAUNCH OVERHEAD, not flops and often more than bandwidth: ~100 tiny kernel launches/token x ~5-10us each is the bulk of the latency. Collapsing to ONE launch is the biggest single lever — this is literally why it is a megakernel benchmark. A fast GEMV that leaves the rest as separate launches caps at ~2-5x.
- Profile the LAUNCH COUNT, not just time: `nsys profile --stats=true python benchmark.py` then read the kernel-launch table (or torch.profiler key_averages count). Target launches-per-step = 1. 4-5x ~= dozens of launches still; 15-20x ~= a single fused grid. This number is the optimization objective.
- Fuse INCREMENTALLY into one kernel: pass a simple correct version, then pull one stage at a time (int4 dequant-GEMV -> RMSNorm -> conv -> KDA state update -> MLA latent attention -> MoE router -> 64 expert GEMVs -> shared expert -> residuals) into the SAME @triton.jit grid / CUDA __global__, re-checking correctness after each. An all-at-once megakernel from scratch is correctness-fragile and lands under the tolerance gate.
- Fuse the int4 unpack + per-group dequant directly INTO the GEMV so quantized weights stream once and are NEVER expanded to bf16 in memory (int4 = 1/4 the bytes). Materializing the dequantized bf16 weight then matmul-ing throws away the W4A16 bandwidth win and is almost always <= a few x. Read reference.py for the exact pack/unpack/group-size-128 asymmetric dequant.
- Parallelize the independent work across GPU blocks/warps inside the single launch: 64 MoE experts, 32 attention heads, tiles of each GEMV. A correct-but-serial megakernel (one block doing everything) can be ~10x slower than a well-parallelized one — expose the parallelism while staying one launch (persistent-kernel / grid-stride patterns).
- A persistent / grid-launched megakernel keeps state (KDA recurrent S[32,128,128], MLA latent cache, conv window) in registers / shared memory across the fused stages instead of round-tripping through global memory between per-op kernels — that avoids both the launches AND the intermediate global reads/writes.
- Standard levers inside the kernel, by usual impact: coalesced global weight access; stage reused small operands (group scales/zeros, router logits) in shared memory; block/tile sizes multiples of the warp (32) with good occupancy; minimize register spills (a huge megakernel can spill — watch ncu register usage); bf16 accumulate where tolerance allows. Profile the bottleneck stage and target IT.
- Match reference.py parameter names / dtypes / layouts exactly so the reference weights load and the cosine >= 0.98 gate compares apples to apples. Keep a slow eager path for your own debugging, but the TIMED path in step() must be the single fused kernel.
- Never fake the single launch: no torch.compile, no torch.cuda.CUDAGraph / make_graphed_callables, no per-op Python loop, no pure-torch fallback in the timed path. These score ZERO via the authenticity judge regardless of how fast benchmark.py looks. The published 19.35x 'record' was a CUDAGraph fake of exactly this kind — get the same speedup honestly by actually fusing.
