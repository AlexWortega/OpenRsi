# OpenRSI findings (shared board)
Generations run: 2
Baseline (gen-0) fitness: 0.0
Current champion: gen2 scaffold.v2 fitness=1.0
RSI delta: +1.0 over baseline
## Generation log
- gen0 v0: fitness=0.000 ACCEPTED ★champion — baseline mega scaffold (no RSI)
- gen1 v1: fitness=0.324 ACCEPTED ★champion — [survived critique] Root cause of the 0 is a missing/broken solution.py, so the first, highest-value step is to guarantee a passing baseline
- gen2 v2: fitness=0.989 ACCEPTED ★champion — [survived critique] A speedup below 1 means the fused kernel is under-parallelized, not just launch-bound. I add guidance to use a persisten
## Levers (shipped)
- Explicit AIDE draft/improve/debug tree search (OPENRSI_SOLVER=aide).
- Per-genre domain-knowledge routing (scaffold.domain_knowledge_by_genre).
- Scratch bash shell for the inner agent (OPENRSI_SCRATCH=on).
- Multi-candidate generations (OPENRSI_INNER_CANDIDATES best-of-N at the draft root).
- grok-build goal plan + direction checker (goal_plan.json + per-gen verdict above).
- KernelBench fast_p fitness on the RTX PRO 6000 (OPENRSI_KB_FITNESS=fast_p).
