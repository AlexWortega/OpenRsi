# OpenRSI findings (shared board)
Generations run: 0
Baseline (gen-0) fitness: 4.6
Current champion: gen0 scaffold.v0 fitness=4.6
RSI delta: +0.0 over baseline
## Generation log
- gen0 v0: fitness=4.619 ACCEPTED ★champion — baseline mega scaffold (no RSI)
## Levers (shipped)
- Explicit AIDE draft/improve/debug tree search (OPENRSI_SOLVER=aide).
- Per-genre domain-knowledge routing (scaffold.domain_knowledge_by_genre).
- Scratch bash shell for the inner agent (OPENRSI_SCRATCH=on).
- Multi-candidate generations (OPENRSI_INNER_CANDIDATES best-of-N at the draft root).
- grok-build goal plan + direction checker (goal_plan.json + per-gen verdict above).
- KernelBench fast_p fitness on the RTX PRO 6000 (OPENRSI_KB_FITNESS=fast_p).
