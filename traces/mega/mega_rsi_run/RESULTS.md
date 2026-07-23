# OpenRSI KernelBench-Mega (scaffold-RSI) results

Champion scaffold v2, mean geomean speedup: **0.989x**
Baseline (gen0): 0.000x  |  RSI delta: +0.989x

Edit mode: bounded  |  per-solve budget: 45min
Total OpenRouter cost: $25.94

## Champion domain knowledge
- At batch-1 decode you are bandwidth-bound on the weight stream; int4 weights are 1/4 the bytes of bf16 ONLY if you never materialize a dequantized bf16 weight in DRAM. In the GEMV inner loop, load one int4-packed weight tile, unpack (two 4-bit nibbles per byte) into registers, apply per-group scale/zero from shared memory, and immediately multiply-accumulate against the activation — dequant lives in registers/SMEM, weights are streamed from DRAM exactly once.
- The timed step() must be a SINGLE kernel launch fusing the entire per-token forward (both KDA and MLA layers, every int4 dequant-GEMV, the conv, the KDA state update, the MLA latent-cache attention, the MoE router + expert GEMVs, both RMSNorms, residuals). Cutting launch overhead without fusing does not count.
- Keep a slow eager reference path for debugging, but the timed path must be the one fused kernel. Verify correctness only via `python check.py` (it tests every layer type + state update across seeds), never a hand-rolled spot-check.
- Coalesce global weight access; stage per-group scales/zeros in shared memory; pick block sizes that are multiples of 32; minimize register spills. Profile with the tools available before guessing.
- Sanity-check the int4 fusion is actually winning: compare the fused single-launch kernel's decode latency to a variant that dequantizes to bf16 then GEMVs. If they tie, your dequant path is materializing bf16 or the weights are cache-resident — verify with a bandwidth profile (achieved GB/s vs int4 byte count) before tuning block sizes.
- A single launch does NOT mean a single threadblock. Under-parallelization is the usual cause of speedup<1: size the ONE grid to fill every SM (launch grid = num_SMs * CTAs-per-SM), partition weight rows/experts across persistent CTAs so they stream disjoint int4 tiles concurrently, and sequence the dependent stages (KDA->conv->state->MLA->MoE->norms) INSIDE that launch via a grid-wide barrier (cooperative-groups grid.sync(), or an atomic arrive/wait counter in global memory). This satisfies the one-launch rule while recovering full DRAM bandwidth.
- After each change, check achieved occupancy and SM utilization (e.g. nsight/ncu or nvidia-smi dmon): if only a few SMs are active during the megakernel, you are serializing work that should be spread across persistent CTAs. Target near-100% SM coverage before touching block sizes.
