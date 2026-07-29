# Draft: asking kernelbench.com how to represent the seed-chain 23.18× result

The OpenRSI seed-chain reached a **median-of-3 `peak_fraction` = 23.18×**, verified authentic, on
`02_kimi_linear_decode` (RTX PRO 6000 Blackwell, `claude-opus-4-8`) — clearing the current published
record for that cell (14.399×). But it is a **chained RSI result, not an independent single solve**,
so it must NOT go on the per-(GPU, model) leaderboard (the cross-run contamination tripwire
auto-excludes it, and it would misrepresent what a single Opus run does — ~4–14×).

Records: `traces/mega/opus_chain_23x_run/`, kernel in `mega_results/opus_23.18x_*.py`, full trajectory
in `benchmark.md`. **Run a solo-GPU sequential isolated re-bench (check.py + benchmark.py) for a clean
number before sending.**

Post as a GitHub issue on `github.com/Infatoshi/kernelbench.com`, or DM the maintainer.

---

**Title:** Where do RSI / seed-chain results fit? (authentic 23.18× on 02_kimi_linear_decode, not a single-solve)

Hi — I built a small recursive-self-improvement harness on top of the mega bench (an outer loop that
evolves the agent's scaffold + **seed-chains** kernels: each run is seeded with the prior run's
`solution.py` and told to optimize it further).

On `02_kimi_linear_decode`, RTX PRO 6000 Blackwell, `claude-opus-4-8`, this reached a **median-of-3
`peak_fraction` of 23.18×**, which clears your current published record for that cell (14.399×). It's
**authentic** by your own checks: `check.py` PASS (cosine ~1.0 incl. numeric stress), and
`scripts/megakernel_evidence.py` reports `kernel_count.total = 3`, **all tripwires clear** (no
`graph`/`compile`/`codegen`/`obfuscation`), no forbidden imports — a real fused kernel, not a
CUDAGraph/torch trick.

**But I don't think this belongs in the per-(GPU, model) board, and I'd rather ask than mis-submit:**

1. It is **not an independent single solve**. It's a chain of 4 seeded runs (≈ 4 → 7.4 → 11.5 → 13.7 →
   23.18×), each handed the previous run's kernel. Your cross-run contamination tripwire auto-excludes
   runs whose transcript references another run's archive — which this is, by design.
2. A from-scratch single Opus run on my box lands in the ~4–14× range, consistent with your board. The
   23× is an **RSI-loop** number, a different thing from "model X solved it in one run."

So my question: **is there a place / category for optimization-loop or RSI results, or would you prefer
this as a methodology writeup rather than a leaderboard cell?** I'm happy to:
- provide the full run archive (result.json + solution.py + transcript + gpu marker) and do the
  mandatory sequential isolated re-bench (solo GPU) for a clean number, and/or
- run your `run_hard.sh` mega harness with Opus **from scratch, no seed**, and submit whatever that
  authentically gets for the per-model cell.

Not trying to game the board — just flagging an authentic-but-chained result and asking how you'd want
it represented. Thanks for the bench!
