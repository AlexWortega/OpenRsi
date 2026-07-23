# OpenRSI KernelBench-Mega (scaffold-RSI) results

Champion scaffold v0, mean geomean speedup: **0.000x**
Baseline (gen0): 0.000x  |  RSI delta: +0.000x

Edit mode: bounded  |  per-solve budget: 1200min
Total OpenRouter cost: $11.13

## Champion domain knowledge
- At batch 1 decode is bandwidth-bound on the weight stream; the int4 weights are 1/4 the bytes of bf16 — but only if you NEVER materialize a dequantized bf16 weight. Fuse the int4 unpack + per-group dequant directly into the GEMV so you stream the int4 weights once.
- The timed step() must be a SINGLE kernel launch fusing the entire per-token forward (both KDA and MLA layers, every int4 dequant-GEMV, the conv, the KDA state update, the MLA latent-cache attention, the MoE router + expert GEMVs, both RMSNorms, residuals). Cutting launch overhead without fusing does not count.
- Keep a slow eager reference path for debugging, but the timed path must be the one fused kernel. Verify correctness only via `python check.py` (it tests every layer type + state update across seeds), never a hand-rolled spot-check.
- Coalesce global weight access; stage per-group scales/zeros in shared memory; pick block sizes that are multiples of 32; minimize register spills. Profile with the tools available before guessing.
