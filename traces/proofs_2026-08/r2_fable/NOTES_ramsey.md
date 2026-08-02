# Ramsey attack log (current run)

Gap: coherent family of correlated codes whose per-color base grows.

## Three code-driven routes

1. **F_2^6 sum-free 4-partition, decided by SAT.** Partition F_2^6\{0} into 4
   sum-free sets ⇔ triangle-free 4-coloring of K_64 of XOR type. Prior run's
   local search stalled at 1 bad line. SAT (63 vars ×4, 651 line-constraints,
   symmetry breaking) should decide it outright. If SAT: R_4(3) ≥ 65 (!), far
   beyond the known 51 — enormous. If UNSAT: sharpens the algebraic ceiling.
   First experiment: experiments/sat_f26.py.

2. **Cayley colorings over growing nonabelian/mixed groups.** For a group G,
   partition G\{1} into k symmetric product-free sets ⇒ R_k(3) > |G|.
   Search |G| vs k over small groups (SAT per group), look for per-color base
   |G|^{1/k} growing. First experiment: experiments/cayley_scan.py over
   abelian groups Z_m^a × Z_2^b and small nonabelian groups.

3. **Locally-s-colored seeds with large N (L_4 hunt).** L_4 ∈ [51?..65].
   SAT/local search for locally-4 triangle-free K_N, N=50..65, unlimited global
   palette. Any N with log N ≫ s log(base) feeds the seed criterion
   (log N = Ω(s log s), g = poly(s) ⇒ superexponential). First experiment:
   experiments/local4_search.py.

## Log
- Installed pysat. Prior verifiers pass.
- sat_f26k.py 5: SAT in seconds — F_2^6\{0} splits into 5 sum-free sets (classes
  11/22/11/11/8), verified. Not new numerically (R_5(3)>=65 << known), but a
  sanity check of the encoding.
- sat_f26k.py 4 (THE open case): CaDiCaL running >17 min, no answer yet. If SAT:
  R_4(3)>=65 beats known 51. If UNSAT: algebraic ceiling at F_2^6 for 4 colors.
- cayley_scan (cyclic Z_m, m<=~82 so far): min-k partitions give base n^(1/k)
  creeping up ~2.41 at (82,5). Schur-like growth, no sign of superexponential
  behavior from plain cyclic groups (expected — matches literature Schur numbers).
