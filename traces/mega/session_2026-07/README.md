# OpenRSI KernelBench-Mega — session 2026-07 run records

The verify-before-trust re-run campaign + seed-chain to 23.18x. Each `*_run/` has board.jsonl
(median-scored fitness + verified flag + cost), RESULTS.md, solution_v0/ (full artifact set incl.
sidecar kernels), and a trimmed log (`*.trimlog`, head+tail). All scores median-of-N, judge-verified.

| run | median geomean | valid | verified | cost | note |
|-----|:---:|:---:|:---:|:---:|------|
| opus_chain2 | 23.178x | True | True | $75.02 | **seed-chain peak — 23.18x, cleared 20x authentically** |
| meta_v3 | 11.787x | True | True | $35.12 | RSI meta gen0 (seeded, scaffold_v3) |
| opus48_reverify | 4.088x | True | True | $38.01 | Opus scaffold baseline |
| kimi_verify | 3.654x | True | False | $50.31 | REJECTED — kernels=0, gamed with torch |
| codex_gptsol | 2.627x | True | True | $50.16 | gpt-5.6-sol + real Codex CLI scaffold |
| gptsol_verify | 1.955x | True | True | $50.38 | gpt-5.6-sol + scaffold_v2 |
| opus_plain | 0.000x | True | True | $92.77 | bare agent (PLAIN) — correct but benchmark-crashing |
| qwen122b_verify | 0.000x | False | False | $50.05 | FAIL — no valid kernel |

Full leaderboard + honest caveats: `../../../benchmark.md`. Headline 23.18x kernel also in
`../../../mega_results/opus_23.18x_*.py` and `../opus_chain_23x_run/`.
