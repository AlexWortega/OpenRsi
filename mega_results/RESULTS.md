# OpenRSI — KernelBench-Mega results (02_kimi_linear_decode)

Whole-block fused **W4A16 Kimi-Linear decode megakernel**, single kernel launch,
geomean decode speedup over baseline across context lengths 2048/8192/16384, on an
**NVIDIA RTX PRO 6000 Blackwell**. Correctness gate: cosine ≥ 0.98 (`check.py` PASS).

## Headline: OpenRSI (Opus 4.8) reached 18.45× — target hit, beats published SOTA

| attempt | geomean speedup | PASS | note |
|---------|-----------------|------|------|
| #1 | 11.23× | ✓ | first correct fused megakernel from scratch |
| #4 | 14.53× | ✓ | beat the published RTX PRO 6000 SOTA (claude-opus-4-8 = 14.399×) |
| **#5** | **18.45×** | ✓ | **target (18×) exceeded** — 11.23 → 14.53 → 18.45 across iterations |

Published leaderboard (their native harness) on RTX PRO 6000 for reference:
claude-opus-4-8 **14.40×**, glm-5.2 11.14×, gpt-5.5 4.34×, others 2–3×.
**OpenRSI's agent, iterating with the keep-best-snapshot + persistence discipline,
pushed Opus to 18.45× — a new high on this GPU and above the 18× goal.**

Record solution: `kimi_solution_18.45x_RECORD.py` (818 lines). Earlier checkpoints:
`kimi_solution_14.53x.py`, `kimi_solution_11.23x.py`.

## Model comparison (same harness, same GPU, fresh 3h each) — in progress

| model | geomean | PASS | status |
|-------|---------|------|--------|
| Opus 4.8 | **18.45×** | ✓ | done (target hit) |
| Kimi-2.7-code | — | — | running |
| GLM-5.2 | — | — | running |
