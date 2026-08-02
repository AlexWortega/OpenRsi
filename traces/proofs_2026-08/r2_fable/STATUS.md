# STATUS (current run)

Seeded from prior/ (verified: both prior verifiers exit 0 as of this run's start).

## Problem 1 — Ehrhart volume conjecture: **PARTIAL** (inherited)

Rigorous (from prior/proof_ehrhart.md, trusted after re-verification):
- Symmetric: vol <= 2^n; controlled asymmetry K ⊂ -ρK: vol <= (2ρ)^n.
- Section/entropy lifting: with a primitive interior axial chord and a centered
  (or ρ-asymmetric) zero section, vol(K) <= 2 A_{n-1} (resp. w(2ρ)^{n-1}).
- Projection–fiber factorizations, flags, products, pyramids: structured classes.

**Gap (target of this run):** arbitrary asymmetric bodies with no good primitive
direction — n=3 complete case is the primary intermediate target.

## Problem 2 — Superexponential R_k(3) lower bound: **PARTIAL** (inherited)

Rigorous (from prior/proof_ramsey.md, trusted): R_k(3) > 2^k baseline; K_16
3-coloring, exact capacity identity max_{α≤2} α(G^⊠k) = R_k(3)−1; iid product
codes / first moment / expurgation / basic LLL cannot beat base 2; effective-
capacity criterion (poly witness power + poly growing base ⇒ k^{ck}).

**Gap (target of this run):** a coherent family of correlated codes / colorings
whose per-color base grows with k.

## This run's progress

- (start) environment set up; pysat installed; experiments/ created.

Honest assessment: both problems OPEN at the main-statement level, PARTIAL
overall. Everything claimed above is backed by prior verifiers that pass here.
