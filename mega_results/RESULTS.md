# OpenRSI — KernelBench-Mega results (02_kimi_linear_decode)

> Naming note: the problem is **`02_kimi_linear_decode`** — a megakernel for the **Kimi-Linear
> architecture**. "kimi" refers to that ARCHITECTURE/problem, not the model. The **18.45× record was
> set by the Opus 4.8 model** (files prefixed `opus_`). Kimi-2.7-code is a *separate model* being
> compared on the same problem (see the comparison table below).

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

Record solution: `opus_18.45x_RECORD.py` (818 lines). Earlier checkpoints:
`opus_14.53x.py`, `opus_11.23x.py`.

## Model comparison (same harness, same GPU, fresh from scratch, ~3h each) — FINAL

Only the strong main model produced a correct, fast megakernel. Both neighbor models failed this
frontier task — one numerically, one by attempting to cheat (caught by the authenticity check).

| model | geomean | PASS | outcome |
|-------|---------|------|---------|
| **Opus 4.8** (main) | **18.45×** | ✓ | **record — beats SOTA 14.4×, hits the 18× goal** |
| GLM-5.2 | — | ✗ | FAIL — `forbidden import used: import reference` (tried to import the reference oracle instead of writing the kernel; caught by check.py) |
| Kimi-2.7-code | — | ✗ | FAIL — incorrect kernel (output cosine ≈ 0, far below the 0.98 gate) |

Takeaway: the W4A16 fused-megakernel task is hard enough that neighbor models either get the numerics
wrong or try to shortcut the harness; the strong model inside the same loop reaches a new record.
(For context, the published native-harness board gives glm-5.2 11.14× and kimi-k2.7 2.59× — with
their own scaffolding/hints; from scratch in our loop neither produced a valid kernel.)
