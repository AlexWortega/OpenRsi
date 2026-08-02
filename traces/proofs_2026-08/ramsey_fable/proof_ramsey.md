# Multicolor triangle Ramsey lower bounds — current write-up (this run)

Everything imported from `prior/round1/proof_ramsey.md` remains in force (verified
by `prior/round1/verify_ramsey.py`, rerun this session). This file adds the new
rigorous statements of this run.

## 1. Setting

`R_k(3)` = least `N` such that every `k`-coloring of `E(K_N)` has a monochromatic
triangle. A *symmetric sum-free `k`-partition of `Z_n`* is a partition
`Z_n \ {0} = S_1 ∪ ... ∪ S_k` with each `S_i = -S_i` and no `a, b ∈ S_i`
(allowing `a = b`) with `a + b ∈ S_i` (mod `n`).

**Difference-coloring lemma (classical).** A symmetric sum-free `k`-partition of
`Z_n` yields a triangle-free `k`-coloring of `K_n` (vertices `Z_n`, edge `{x,y}`
colored by the class of `x−y`; well-defined by symmetry; a monochromatic triangle
`x,y,z` gives `a=y−x, b=z−y, a+b=z−x` in one class). Hence `R_k(3) ≥ n+1`.

The classical base `3.19963 = 1073^{1/6}` comes from such a partition of
`Z_1073` (Fredricksen–Sweet 2000), amplified by lexicographic products.

## 2. New: an exact ceiling for the cyclic route

**Lemma (cyclic ⇒ Schur restriction).** If `Z_n` admits a symmetric sum-free
`k`-partition, then `m := floor((n−1)/2) ≤ S(k)`, where `S(k)` is the Schur
number (largest `m` such that `[1,m]` splits into `k` sum-free sets, equal
summands allowed). Equivalently `n ≤ 2S(k) + 2`.

**Proof.** Restrict each class to `{1, ..., m}`. For `a, b ≤ m` with `a + b ≤ m`
the sum `a + b` taken mod `n` equals the integer sum (since `a+b ≤ n−1`), so a
monochromatic integer triple `a, b, a+b` inside `[1,m]` would already violate
the mod-`n` sum-freeness. Hence the restricted classes form an integer sum-free
`k`-partition of `[1,m]`, so `m ≤ S(k)`. ∎

**Corollary (k = 5 closure).** Since `S(5) = 160` (Heule 2017, computer-assisted,
cited from literature and not re-verified here), every symmetric sum-free
5-partition has `n ≤ 322`, so the cyclic 5-color route is capped at per-color
base `322^{1/5} ≈ 3.1735 < 3.19963`. No search above `n = 322` is warranted.

**Corollary (goal-(a) reformulation for cyclic colorings).** A cyclic `k=6`
construction with base `> 1073^{1/6}` requires `n ≥ 1076`, hence `S(6) ≥ 537`,
improving the 25-year-old record `S(6) ≥ 536`; for `k = 7`, base `> 1073^{1/6}`
requires `n ≥ 3435`, hence `S(7) ≥ 1717` (known record `S(7) ≥ 1680`). Thus for
`k ∈ {5,6,7}` the cyclic route to goal (a) is *exactly* a Schur-record
improvement. (Search continues as a lottery; no claim.)

Machine check of the lemma's finite content: `verify_cyclic_ceiling.py`
exhaustively confirms, for all `n ≤ 45` and `k ≤ 3`, that whenever a symmetric
sum-free `k`-partition of `Z_n` exists (decided by brute force), the restriction
to `[1, floor((n−1)/2)]` is an integer sum-free partition, and cross-checks
`n ≤ 2S(k)+2` against the exact small Schur numbers `S(1)=1, S(2)=4, S(3)=13`.

## 3. New verified finite constructions (below record; recorded, not claimed as progress)

Dilation-invariant symmetric sum-free partitions found by SAT over coset
variables (all fully verified by `verify_cyclic_partition.py`):

- `Z_43` into 4 classes invariant under the index-21 subgroup of units
  (base `43^{1/4} ≈ 2.5607`; `R_4(3) ≥ 44` — far below the known `≥ 51`).
- `Z_41`, `Z_37` analogues; `Z_13` into 3 classes (base 2.3513).

These confirm the coset-SAT machinery but give no numerical advance; the route's
value was to compress the search space for the record targets, where all coset
instances tried at `p ∈ [900,1450]` (k=6) and `p ∈ [3434,4000]` (k=7), index
`t ≤ 96`, are UNSAT so far.

## 4. New: rigidity of extremal locally-3 colorings

Recall (round1, proved): `L_s` = max order of a triangle-free coloring in which
every vertex sees at most `s` colors (global palette unrestricted);
`L_1,L_2,L_3 = 2,5,16`, `L_s <= 1 + s L_{s-1}`, and at equality every vertex
sees exactly `s` colors with incident classes of size exactly `L_{s-1}`, each
inducing an extremal locally-`(s-1)` coloring.

**Theorem (global-palette collapse at s = 3).** Every triangle-free locally-3
edge-coloring of `K_16` uses exactly 3 colors globally.

**Proof.** `16 = 1 + 3 L_2`, so the coloring is extremal and the equality lemma
applies: every vertex sees exactly 3 colors, each on exactly 5 incident edges
(5-regularity in each incident color). Fewer than 3 global colors is impossible
(`R_2(3) = 6 <= 16`). Suppose some 4th color occurs globally. Every vertex sees
exactly 3 of the 4 colors, so misses exactly one; let `m_c` be the number of
vertices missing color `c`, so `m_0+m_1+m_2+m_3 = 16`. The color graph `G_c` is
5-regular precisely on the `16 - m_c` vertices not missing `c`; hence
`16 - m_c` is even (handshake) and `>= 10` (Mantel: a 5-regular triangle-free
graph has at least 10 vertices), i.e. every `m_c` is even and `<= 6`. The only
partitions of 16 into four even parts `<= 6` are `(6,6,4,0)`, `(6,6,2,2)`,
`(6,4,4,2)`, `(4,4,4,4)`.

First rule out `g >= 5` colors globally: by the equality lemma every color
incident to a vertex occupies exactly 5 of its edges, so every used color's
graph is 5-regular on its support; being triangle-free, its support has `>= 10`
vertices (Mantel). Summing support sizes over all used colors counts each
vertex exactly 3 times (each vertex sees exactly 3 colors), giving
`10 g <= 48`, i.e. `g <= 4`.

For `g = 4`, each of the four profiles above is refuted by exhaustive computer
search (independent C backtracker `experiments/rigidity_bt.c`, node counts
0.64/1.07/2.49/0.12 billion; cross-checked by CaDiCaL UNSAT on a different
encoding with sequential-counter cardinality constraints): no edge coloring of
`K_16` satisfies simultaneously (i) edge `(u,v)` avoids `miss(u)` and
`miss(v)`, (ii) no monochromatic triangle, (iii) every vertex 5-regular in each
of its 3 allowed colors. These constraints are implied for a hypothetical
4-color example, so none exists. Hence `g = 3`. Machine check:
`verify_local3_rigidity.py` (exit 0) re-derives the base case, checks the
profile-list completeness, compiles and re-runs the exhaustive refutation. ∎

**Corollary (structure of hypothetical `L_4 = 65`).** If a locally-4
triangle-free `K_65` exists, then around every vertex `v` the other 64 vertices
split into four classes of 16 (by the color of their edge to `v`), and by the
equality lemma each class induces an extremal locally-3 `K_16`, which by the
theorem uses EXACTLY 3 colors internally — 3 colors that exclude the class's
edge color to `v` (else a monochromatic triangle through `v`). So each of the
four classes carries a full `{3 colors} + 1` structure: at most
`4 + 4*3 = 16` colors are visible within distance structure of any one vertex,
and every vertex of a class sees its 3 internal colors plus the class color,
exhausting its local palette of 4. Consequently in an extremal `K_65` every
edge color between two classes of `v`'s partition is determined up to the
heavily constrained interplay of two 4-palettes. This makes the `L_4 = 65`
decision a far smaller SAT instance than the naive one.

## 5. New: `L_4 <= 64`

**Theorem.** There is no triangle-free locally-4 edge-coloring of `K_65`;
hence `L_4 <= 64` (strictly below the recursive bound `1 + 4 L_3 = 65`).

**Proof.** Suppose one exists. Fix `v0`. By extremality (`65 = 1+4L_3`) and the
equality lemma, the 64 other vertices split into classes `C_0..C_3` of size 16
by their `v0`-edge color (WLOG color `i` for `C_i`), every vertex sees exactly
4 colors each on exactly 16 incident edges, and each `C_i` induces an extremal
locally-3 `K_16`. By the rigidity theorem (§4), `C_i` uses exactly 3 internal
colors `pal_i` (none equal to `i`), and each vertex of `C_i` sees all three
internally (equality lemma at `s = 3`), plus color `i` on its `v0`-edge. Hence
all 16 vertices of `C_i` have the same palette `P_i = {i} ∪ pal_i` of size 4.
Exact degrees at `u ∈ C_i`: color `i` occurs on the `v0`-edge and never inside
`C_i`, so exactly 15 cross edges have color `i`; each `c ∈ pal_i` occurs on
exactly 5 internal edges (5-regularity in the extremal `K_16`), so exactly 11
cross edges. Cross edges `C_i–C_j` must be colored in `P_i ∩ P_j`. Capacity:
color `i` needs 15 cross slots at `u`, and edges to `C_j` can carry `i` only if
`i ∈ P_j`; so `i ∈ P_j` for some `j ≠ i`; similarly each `c ∈ pal_i` lies in
some other palette. Thus every used color lies in at least 2 of the four
palettes; the `P_i` have 16 slots total and colors `0–3` occupy at least 8, so
at most 4 further colors exist: WLOG the universe is `{0,...,7}`.

Up to the symmetry group (relabeling classes together with colors `0–3`, and
renaming extra colors), exactly 304 palette systems `(pal_0,...,pal_3)` pass
these capacity filters (enumeration re-checked from scratch by the verifier).
For each system the faithful constraint set — edge domains as above, no
monochromatic triangle, exact per-vertex degree counts (5 internal, 15/11
cross) — was encoded as CNF; kissat 4.0.4 returned UNSAT on 303 of the 304,
each certified by a DRAT proof checked with drat-trim. The remaining case,
`pal_i = {0,1,2,3} \ {i}`, is an ordinary triangle-free 4-coloring of `K_65`,
which would give `R_4(3) ≥ 66`, contradicting the published `R_4(3) ≤ 62`
(Fettes–Kramer–Radziszowski, "An upper bound of 62 on the classical Ramsey
number R(3,3,3,3)", 2004); this case is accepted by citation (a direct DRAT
certification is running but not required). Since a hypothetical locally-4
`K_65` realizes one of the 304 systems, none exists. ∎

Machine check: `verify_L4_64.py` (exit 0) re-enumerates the 304 systems,
verifies every recorded result is `VERIFIED-UNSAT`, and re-solves and
re-certifies random cases end-to-end (`--resolve N`).

**Significance.** `L_1, L_2, L_3 = 2, 5, 16` and now `50 ≤ L_4 ≤ 64` (lower
bound: ordinary 4-colorings are locally-4 and `R_4(3) ≥ 51`). The recursion
`L_s ≤ 1 + s L_{s-1}` is sharp at `s = 2, 3` but STRICTLY FAILS at `s = 4`.
This is the first failure of the factorial pattern in the local-palette
hierarchy: extremal towers of rigid neighborhoods do not persist. It is
negative evidence for (though not a refutation of) the local-seed route to
superexponential growth. The exact value of `L_4` remains open.

## 6. Status of the main statement

No superexponential lower bound is proved. The precise gap is unchanged:
a coherent family of colorings/codes with growing per-color base. This run's
cyclic–Schur lemma shows the most-searched family (cyclic/difference
colorings) cannot even reach goal (a) for `k ≤ 5` and reduces `k ∈ {6,7}` to
Schur-record questions; the `L_4 ≤ 64` theorem newly bounds the local-palette
hierarchy away from its factorial ceiling at the first open level.
