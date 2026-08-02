# STATUS

Updated: terminal adversarial audit and full verifier sweep.

## Main result: **PARTIAL**

No superexponential lower bound, growing-base family, or record base above 3.199 is proved in this run.

## Verified inherited facts used

- `python3 prior/round1/verify_ramsey.py` passes: explicit K_16/K_32 colorings, fixed-layer nonextension counts, and ternary obstruction.
- `python3 prior/sol/verify_ramsey.py` passes the same baseline.
- `(cd prior/sol && python3 verify_grotzsch_code.py)` passes: the Grötzsch graph is triangle-free and the 12-word strong-cube code is valid, giving fixed base `12^(1/3)`.
- `(cd prior/sol && python3 verify_f2_partitions.py)` passes: the finite `F_2^7`/5-color and `F_2^8`/6-color partitions are valid. These remain below the classical 3.199 base.

## Route assessment

1. **Generic/Cayley capacity searches: BANKED.** Random triangle-free, constant-weight, and 1,539 circulant instances gave no cube base above 2.154. These are heuristic non-results, but no scalable lower mechanism survived.
2. **Shift-graph complements. RIGOROUSLY BANKED.** The numerical LP rises to 3 at label size 12, but a simple universal fractional coloring gives `chi_f<=4`: for each bipartition `A∪B=[n]`, pairs `(a,b)` with `a∈A,b∈B` form an independent set, and uniform cut weights cover every vertex with total weight 4. Hence the complement's Shannon capacity is at most 4 for all `n`; this family cannot have growing base.
3. **Nilpotent 2-groups: BANKED.** Verified partitions use 3,5,9 colors for `UT(3,2),UT(4,2),UT(5,2)`. The pattern is highest-entry coloring with `binom(n,2)` colors and only one constant compression, hence fixed base near 2. `UT(5,2)`/8-color SAT timed out and min-conflicts stalled; no UNSAT claim. Heisenberg modulus 8/7-color likewise stalled at one conflict.

Kneser graphs were rejected because triangle-free members have `chi_f<3`. Generalized shift graphs were also rejected: after excluding the two looped constant patterns, binary labels and a degree-4 de Bruijn transition graph give a fractional coloring of weight at most 10 uniformly in tuple length and ground-set size.

Precise gap: no construction or proof presently makes the per-color base grow. A final broad rooted-word recursion scan with completely node-dependent pair colors again required color count proportional to depth; all formal high-base targets remained far from feasible. The iterated wreath 2-group tower has independently verified levels `(order,k)=(8,3),(128,6)`, bases `2,2.245`; its obvious recursion stays base 2, and sampled level-4/14-color composition stalled at one violation before being banked (even success would lower the base). Odd-prime `UT(3,5)` gives a verified `(125,6)` seed, base 2.236; `UT(3,7)`/7-color stalled at one and was banked. Affine groups, linear binary Cayley codes, and quadratic-form difference rules likewise showed fixed/decreasing base or immediate algebraic obstructions. None is goal-ladder progress. Fresh polynomial-evaluation templates reduce to fixed-base first-difference constructions. A broader SAT quotient of full permutation first-difference states did find independently verified colorings `(n!,k)=(24,5),(120,7),(720,10)`, but bases `1.89,1.98,1.93` remain constant-scale and below all useful benchmarks, so this route is banked. Three larger `F_2^d` partition trend tests all stalled at 34 violated lines and were terminated; a constant-weight subset scan stayed below cube base 2.154. A node-dependent permutation-tree relabeling was then tested: verified constructions are `(n!,k)=(24,5),(120,7),(720,10)` (the 9-color `n=6` SAT timed out), identical to the coarser quotient's constant-scale behavior. Simple inversion and recursive remaining-set templates likewise show no linear-color pattern. All are banked; no UNSAT claims are promoted.

## Terminal assessment

**PARTIAL, below goal-ladder item (a).** The best new verified seeds have bases at most `128^(1/6)=2.245`, below 3.199. No growing-base family is proved. The durable new rigorous results are negative/diagnostic: shift complements have capacity at most 4; generalized shift complements at most 10 (corrected during audit for looped constant patterns); Kneser complements in the triangle-free range have capacity below 3; universal color-only lexicographic reuse cannot save colors; and any inverse-closed product-free group partition is impossible in a group with 3-torsion.

`python3 experiments/verify_all_new_claims.py` passes for every finite construction promoted in this run, including the 61,949,040-triangle checks for both `K_720` descriptions. Inherited verifiers also pass. No bare SAT `UNSAT` result is promoted.

## Integrity

No forbidden document, copy, summary, or discussion was accessed or searched. No proof assistant is used.
