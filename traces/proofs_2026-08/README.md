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
| `r2_sol/` (round 2) | openai/gpt-5.6-sol | $50 total | 21+5 rounds, $50.71 — both PARTIAL; ~10 Ramsey seed families banked (all fixed base ≤2.63), HNF tetrahedra enumerations, integer-simplex pigeonhole |
| `r2_fable/` (round 2) | anthropic/claude-fable-5 | $46 (killed hung at $29.17) | Ehrhart n=3 reduction to 1-D concave Lemma A′ (64/27, numerically supported, proof not closed); F_2^6 SAT sweeps |

Round-2 runs are seeded from round 1's artifacts and target its precisely
stated gaps; their archives (work files + `events.jsonl`) land here after
completion. `proofs_sol.log` is the round-1 runner stderr (nudge/cost trail).

Round-1 highlights (see `proofs_sol/STATUS.md`): structured-class Ehrhart
bounds via section/entropy lifting; proof that iid product codes and basic
LLL cannot beat base 2 for the Ramsey capacity route; exact capacity identity
max_{α(G)≤2} α(G^⊠k) = R_k(r+1)−1.

## Round 3 — Ramsey-only head-to-head (identical merged seeds, runner `agent/proofs/run3.js`)

| run | model | cost | result |
|---|---|---|---|
| `ramsey_sol/` | openai/gpt-5.6-sol | $25.14 | PARTIAL; 4 new universal capacity obstructions (shift complements ≤4, generalized ≤10, Kneser <3, 3-torsion), ~6 more families banked |
| `ramsey_fable/` | anthropic/claude-fable-5 | **$104.69 (4x overrun: one 8h round, budget checked only between rounds)** | PARTIAL, but **two new theorems**: **L₄ ≤ 64** (no triangle-free locally-4 coloring of K₆₅; rigidity theorem for K₁₆ + 303 kissat UNSAT cases with drat-trim-verified DRAT certificates + FKR 2004) — first strict failure of L_s ≤ 1+sL_{s−1}, so 50 ≤ L₄ ≤ 64; and the **cyclic⇒Schur ceiling lemma** — cyclic 5-color route capped at base 322^{1/5} ≈ 3.1735 < 3.19963 (closed), and beating classical base cyclically for k=6,7 is EQUIVALENT to improving Schur records S(6)≥536 / S(7)≥1680 |
| `ramsey_oracle/` | worker gpt-5.6-sol + oracle gpt-5.6-sol-pro (`scripts/ask_pro.py`) | $37.59 total (2 segments, 9 oracle calls) | PARTIAL; 5 oracle calls; universal permanent bound per(M) ≥ n!/C^n (C<5.38), anchored palettes killed via R(3,3)=6, fractional-cylinder lemma caps varying-domain families at Q^r; round 2 added a tensor fitting-rank obstruction and killed GQ-Tanner quotients and separated-permutation candidates |

Goal ladder for round 3+: (a) base > 3.199 record → (b) provably growing base →
(c) superexponential. None reached yet; the durable output is theorems that
close mechanism classes. Full event streams (`events.jsonl.gz`) archived per run.

## CVP campaign (ten-proofs ch.7 problem; worker sol thinking=high + oracle, $50, runner `agent/proofs/run5.js`)

`cvp_oracle/` — PCP-free polynomial-factor NP-hardness of Euclidean CVP from
3SAT. PARTIAL (negative diagnostics only), 8 oracle consultations, 40 passing
verifiers. Durable output: a rigorous obstruction map — every bounded-local
mechanism dies (affine extrapolation; alternating (d+1)-cube cheat for any
constant-degree local signature, surviving mixing/mod/tensoring/folding;
gauge-triviality theorem for copy-stable local phase lifts; unary-marginal
2x2-rectangle nonintegrality; tensor pointed-distance multiplicativity +
sampling lower bounds). Its final verdict: hardness must come from a genuinely
global norm-vs-integrality mechanism. Segment 1 ($50) ended by an over-aggressive 120-min round watchdog while
still active (lesson: activity-based, not nudge-based). Segment 2 (+$25, 10
oracle consultations total, 54 verifiers) extended the map to GLOBAL
mechanisms: CRT coupling, circuit tableaus with affine interfaces, Walsh
characters (integer closure needs all 2^n), fixed-prime fingerprints
(Hamming-type exponential row bound), bounded integer fingerprints (counting
obstruction), and naive univariate polynomial moments (finite-difference
extrapolation kills degree <= q-2) — each killed by an exact low-weight
witness in the tested model. Final verdict unchanged: a fundamentally
different polynomial-size sparse column model is required. Total CVP spend ~$75.

`cvp_ideate/` — run6 idea-search harness ($30.70): Fable-5 ideation oracle +
web literature scouts + IDEAS.md population (15 lines, mutate-before-bury) +
40% construction quarantine. PARTIAL, but the architecture delivered: 2 ideate
rounds produced 9 new mechanism lines (incl. RS error-budget shell I12,
Sidon shielding I13, Pfaffian+BCH I14, expander bundling I15 — still open);
Construction A (exact-cover quotient) wounded with a precise mutation path;
Construction B (odd-cyclic tensor fold) yielded a genuinely new proved coding
lemma — mixed-word bound delta_fold >= 1+ceil((delta^2-1)/ell) for any odd
group acting freely off the pointed coordinate — plus a residual-lineage
propagation theorem (14,773 verified recurrence transitions). Segment 2 (+$31.12): population grew to 25 lines; new proved content —
rank-two pointed determinant theorem, Pluecker count, disproof of all-partner
pointed multiplicativity, exact weighted set-support compression of pure-power
tensors; parity-check simplification proved vacuous on the BMT ladder. Final:
still PARTIAL, 2 promising lines (I07 fold, I21 homogenized tensor) + I12 RS
shell / I14 Pfaffian+BCH / I15 expander bundling left open. CVP total ~$137.
