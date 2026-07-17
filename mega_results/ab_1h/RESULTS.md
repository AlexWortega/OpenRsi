# KernelBench-Mega A/B — single-agent vs AIDE tree, hard-capped 1h

Task: **Kimi-Linear W4A16 whole-block decode megakernel** (`02_kimi_linear_decode`), one fused
single-launch kernel, correctness cosine ≥ 0.98, geomean decode speedup over ctx 2048/8192/16384 vs
`baseline.py`. Hardware: **RTX PRO 6000 Blackwell Server Edition** (RunPod, secure). Model: **Opus 4.8**
for both arms. Each arm hard-capped at exactly **3600 s** (`timeout -s KILL 3600`), run sequentially
on the one GPU. Fresh clean slate (no seeded `solution.py`).

## Result

| arm | approach | correct? | **geomean @1h** | ctx 2048 / 8192 / 16384 |
|-----|----------|:--------:|:---------------:|-------------------------|
| **A — single-agent** (`src/mega/run.ts`) | one uninterrupted trajectory | ✓ PASS | **4.00×** | 5.11 / 3.95 / 3.16× |
| **B — AIDE tree** (`src/mega/aideRun.ts`) | goal-plan → draft/improve/debug | ✓ PASS | **3.08×** | 2.88 / 2.98 / 3.39× |

**At a strict 1 h, the single-agent arm won: 4.00× vs 3.08×.** Both produced a *correct*, fused,
single-launch megakernel — the harness and both approaches work end-to-end.

## AIDE tree trace (arm B)

The new stack's search is fully visible (grok-build goal plan wrote 4 gating criteria first):

| node | kind | parent | PASS | geomean |
|------|------|--------|:----:|:-------:|
| 0 | draft | — | ✓ | 2.00× |
| 1 | draft | — | ✓ | 1.02× (dud) |
| 2 | improve | 0 | ✓ | 2.45× |
| 3 | improve | 2 | ✓ | **3.15×** |
| 4 | draft | — | (cut off by 1h cap) | — |

Clean monotonic improve-chain off the best draft: 2.00 → 2.45 → 3.15×. Final measured 3.08×
(≈ node3, timing noise). The ε-explore policy spent node1 on a weak second draft (1.02×) and started
a fresh draft (node4) at ~52 min that the hard cap killed before it could pay off.

## Honest read

- **Why single-agent won here:** on this task one deep, uninterrupted line of iteration got further
  than splitting the 1h budget across multiple drafts + the goal-planner/critique overhead. The AIDE
  structure trades depth for breadth; under a tight 1h budget on a task where the *best single line*
  matters most, depth won.
- **Where AIDE looks better:** its progress is legible (every attempt scored + kept) and both its
  drafts passed — vs single-agent's high run-to-run variance (an earlier *uncapped* run of the same
  single-agent needed **~1h35m to first commit a passing kernel**, then reached 2.33× by 1h44m; this
  capped run happened to pass fast and reach 4.00×). AIDE's flatter curve (3.39× at the longest
  context) also suggests a more bandwidth-robust kernel.
- **Caveat — n=1 per arm.** Opus is non-deterministic and this task is high-variance (compare the two
  single-agent trajectories above). One run each is a data point, not a verdict. A fair conclusion
  needs several seeds per arm and/or the 3h budget the 18.45× record used.
- **A cheap AIDE fix suggested by the trace:** drop ε-explore (or forbid new drafts in the last ~20%
  of budget) so late time goes to *improving* the champion instead of an unfinishable fresh draft.

Artifacts: `single_agent_4.00x.py`, `aide_3.08x.py`, `goal_plan.json`, `node{0..3}_*.json`.
