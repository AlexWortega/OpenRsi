# TASK

Build a Recursive Self-Improvement (RSI) system on the **pi** agent skeleton and beat the
benchmarks from the referenced sources (KernelBench, ALE-Bench, …). Reproduce the AIDE² bi-level
loop from the Weco RSI blog: an outer agent rewrites an inner solver agent's own scaffold and keeps
the rewrite only if a **private** score (hidden test cases the inner agent can't see) improves.

- Run mode: interactive, long-running.
- Many hypotheses worth sweeping: yes — each outer-loop scaffold rewrite is one experiment.
- Sources: Weco RSI blog (AIDE²); arXiv 2502.13138 (AIDE = the inner tree-search agent);
  SakanaAI/ALE-Bench; earendil-works/pi (agent skeleton).

## Locked decisions
- Benchmark: **ALE-Bench Lite first** (CPU, deterministic local Docker judge), then KernelBench (V100).
- Compute: **eva01** ("kanbaru", 48 cores, Docker, 4× V100-32GB) — agent + judge co-located.
- Budget: MVP (~6–10 outer generations).
- Models (OpenRouter): all-strong — inner `claude-sonnet-5`, outer `claude-opus-4.8`.

## Fitness / metric
`performance` (0–3500, AtCoder-style) from ALE-Bench `private_eval`, averaged over the RSI problem
set. The inner agent optimizes only `public_eval` (visible cases); selection is on `private_eval`
(hidden) — the AIDE² anti-reward-hacking mechanism, built into ALE-Bench per problem.
