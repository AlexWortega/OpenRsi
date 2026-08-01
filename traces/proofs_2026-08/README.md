# Proofs campaign — research-math runs (Aug 2026)

Autonomous pi coding agents attacking two research-level problems from the
OpenAI "Ten Advances" set (the document itself is off-limits to the agents —
they measure independent reasoning):

1. **Ehrhart volume conjecture** — vol(K) ≤ (n+1)^n/n! for barycentered
   lattice-point-free convex bodies.
2. **Superexponential multicolor Ramsey lower bound** — R_k(3) ≥ k^{ck}
   (equivalently: Shannon capacity of independence-2 graphs is unbounded).

Runners live in `agent/proofs/` (deployed as `dist/proofs/` on eva02):
`run.js` — round 1; `run2.js` — goal-directed code-first variant (no Lean,
seeds from `prior/`, streams full events to `<dir>/events.jsonl`, auto-spawns
the tracehouse bridge `scripts/tracehouse_tail_proofs.py` → agent traces in
project **rsi-proffer**).

## Runs

| run | model | budget | result |
|---|---|---|---|
| `proofs_sol/` (round 1) | openai/gpt-5.6-sol | $100 | 77 rounds, $100.24 — both problems PARTIAL, honest gaps stated; all verifiers pass |
| `proofs_code_r2` (round 2) | openai/gpt-5.6-sol | $50 total | in progress |
| `proofs_code_fable` (round 2) | anthropic/claude-fable-5 | $50 total | in progress |

Round-2 runs are seeded from round 1's artifacts and target its precisely
stated gaps; their archives (work files + `events.jsonl`) land here after
completion. `proofs_sol.log` is the round-1 runner stderr (nudge/cost trail).

Round-1 highlights (see `proofs_sol/STATUS.md`): structured-class Ehrhart
bounds via section/entropy lifting; proof that iid product codes and basic
LLL cannot beat base 2 for the Ramsey capacity route; exact capacity identity
max_{α(G)≤2} α(G^⊠k) = R_k(r+1)−1.
