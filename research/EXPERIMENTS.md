# EXPERIMENTS

Fitness = mean ALE-Bench `performance` (private_eval, held-out cases) over the RSI problem set.
A row is a kept winner only when fitness improves AND the private judge is ACCEPTED (verified).

| exp_id | gen | change (one line) | problem(s) | status | performance | delta | verified | secs | note |
|--------|-----|-------------------|-----------|--------|-------------|-------|----------|------|------|
| 0 | 0 | baseline scaffold v0 (no RSI) | ahc008 | passed | 780–1096 | 0 | yes | 64–160 | Sonnet5; variance from early-stopping (1–3 evals) |
| 1 | 1 | outer rewrite: use full budget + SA/delta-eval + 11 AHC tips | ahc008 | passed | 1040 | +260 | yes | 168 | Opus diagnosed early-stop; ACCEPTED champion v1 |
| — | verify | champion v1 on held-out (never selected on) | ahc015 | passed | 1380 | — | yes | — | rank 314; generalizes to unseen problem |

Validated single-generation RSI: baseline→champion +260 on ahc008, generalizes to held-out ahc015
(1380). Full 6-generation, 3-problem MVP run (`runs/mvp1/`) in progress. See board.jsonl for the
machine log per generation.
