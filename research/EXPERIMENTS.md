# EXPERIMENTS

Fitness = mean ALE-Bench `performance` (private_eval, held-out cases) over the RSI problem set.
A row is a kept winner only when fitness improves AND the private judge is ACCEPTED (verified).

| exp_id | gen | change (one line) | problem(s) | status | performance | delta | verified | secs | note |
|--------|-----|-------------------|-----------|--------|-------------|-------|----------|------|------|
| 0 | 0 | baseline scaffold v0 (no RSI) | ahc008 | passed | 1096 | 0 | yes | 160 | Sonnet5, rank 495, evals 3/6, $0.14 |

_(RSI generations append here as the loop runs; see runs/openrsi/board.jsonl for the machine log.)_
