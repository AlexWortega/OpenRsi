# ROADMAP.md

## Target

Prove, without PCP machinery or unproved conjectures, a deterministic polynomial-time many-one reduction from 3SAT of size \(m\) to Euclidean GapCVP of rank \(n=\operatorname{poly}(m)\) with approximation factor \(n^c\) for an explicit absolute \(c>0\).

Every normalization, consistency, carry, and boundary condition must be emitted in the lattice. Soundness always quantifies over unrestricted integer coefficients.

The ordered-pair Barrington lift and the \(A_5\) convolution tile are retired: diagonal signed flows and bicyclic group-ring units respectively defeat their proposed growth laws.

---

## Strategy 1 — Voronoi-coercive gate recursion

Replace flow moments and convolution by a gate whose complete integer transfer behavior follows from a certified Delaunay/Voronoi shell. This retains recursive amplification but changes the coercive mechanism.

### Lemmas

1. **Balanced explicit-circuit lemma.**  
   Deterministically transform \(F\) into a bounded-fanout NAND/COPY circuit \(C_F\) of size \(m^{O(1)}\) and depth
   \[
   d\ge \lfloor\log_2m\rfloor,\qquad d=O(\log m),
   \]
   such that every input assignment has a unique legal evaluation and the output is TRUE exactly when it satisfies \(F\).

2. **FRONTIER — Voronoi-coercive tile lemma.**  
   Construct fixed rational Euclidean NAND and COPY tiles, each with at most \(D\le256\) integer selector columns and finite port codebook \(K\), satisfying:

   - all legal truth-table configurations have the same squared cost;
   - all coefficients, ports, and gluing conditions are lattice coordinates;
   - the complete unrestricted min-plus transfer operator is closed on \(K\);
   - vectors whose port is outside \(K\) are separated by an exact Voronoi certificate, not by bounded enumeration;
   - if \(\mu\) is legal energy growth and \(\lambda\) is the minimum growth of FALSE, DROP, signed, or malformed states, then
     \[
     \lambda/\mu\ge65/64;
     \]
   - the inequality holds for every \(z\in\mathbb Z^D\), including affine parity vectors, diagonal signed flows, and arbitrary auxiliary coefficients.

3. **Recursive shell theorem.**  
   Glue tiles using only emitted equality rows. Exact min-plus composition and the coercive outside-shell certificate imply that a false root above a depth-\(h\) subtree has squared-distance ratio at least \((65/64)^h\) over a legal subtree. Equal-radius completeness is preserved.

4. **Gap accounting lemma.**  
   Compile \(C_F\) with rank \(n\le m^6\). If \(F\) is satisfiable, an honest evaluation attains radius \(R\); otherwise Lemma 3 gives
   \[
   \operatorname{dist}(y,L)\ge (65/64)^{d/2}R\ge n^{1/700}R
   \]
   after fixed padding for small \(m\).

**Why sufficient.** Lemma 1 supplies the Boolean computation; Lemma 2 controls every integer gate state; Lemma 3 propagates adverse energy through logarithmic depth; Lemma 4 converts this into a polynomial CVP gap.

**Crux.** Finding a Delaunay port geometry with \(\lambda>\mu\). Unlike the killed \(A_5\) tile, coercivity must come from a positive-definite Voronoi barrier rather than multiplication in a ring with virtual units.

**First experiment.** Enumerate NAND/COPY port labelings in products of the \(D_4\) and \(E_8\) Delaunay cells. For each labeling, construct the depth-two transfer table and compute unrestricted minima by exact Fincke–Pohst enumeration. Reject unless an exact covering-radius certificate handles all points outside the enumerated shell and \(\lambda/\mu\ge65/64\).

---

## Strategy 2 — Prime-adic torsion tower for legal-assignment sheaves

Replace real-norm amplification by arithmetic divisibility. Signed pseudosections may exist, but an inconsistent one must acquire an additional factor of a fixed prime at every lift.

### Lemmas

1. **Legal-assignment sheaf lemma.**  
   Convert \(F\) to a bounded-degree clause-variable incidence complex \(X_0\). Each clause vertex carries only its seven satisfying labels; each overlap carries complete assignment marginals. A genuine normalized global section exists exactly when \(F\) is satisfiable.

2. **FRONTIER — honest-preserving prime-lift lemma.**  
   For \(q=2\), construct a deterministic constant-size lift operator \(X\mapsto\widetilde X\) with integral auxiliary ports such that:

   - every honest \(0/1\) section lifts uniquely and without changing its local norm;
   - every auxiliary or carry variable is charged in the Euclidean objective;
   - for every normalized zero-residual integral pseudosection \(z\) that is not an honest section, its defect class satisfies
     \[
     \nu_2([\widetilde z])\ge \nu_2([z])+1;
     \]
   - the statement is over the complete integral chain groups, not a bounded set of named attacks.

3. **Torsion-to-norm lemma.**  
   After \(t\) lifts, any non-honest zero-residual normalized pseudosection has
   \[
   \|z\|_2^2\ge 4^tR_t^2.
   \]
   Any nonzero emitted residual is given integral weight \(M_t\ge2^tR_t\), so it obeys the same lower bound.

4. **Polynomial tower and GapCVP lemma.**  
   Take \(t=\lfloor\log_2m\rfloor\). If each lift expands rank by at most \(64\), then \(n\le m^{10}\). Satisfiable instances have radius \(R_t\), while unsatisfiable instances have distance at least \(2^tR_t\), yielding \(n^{1/11}\)-GapCVP hardness after padding.

**Why sufficient.** Unsatisfiability excludes honest sections. Lemmas 2–3 force every remaining integral vector—zero-residual or not—to have exponentially larger norm. Lemma 4 keeps the tower polynomial.

**Crux.** Honest labels generate primitive difference lattices, so naive congruence rows are defeated by affine combinations. The lift must create formula-dependent torsion without introducing free carries or excluding honest sections.

**First experiment.** On the nine-clause G13/G15 obstruction, enumerate depth-two lifts with edge maps \(U=I+2N\), \(N_{ij}\in\{-1,0,1\}\), and at most two charged carry coordinates per edge. For each candidate, use SNF to describe the unrestricted zero-residual affine fiber and exact CVP enumeration to test whether every non-honest point has fourfold squared-norm growth. Seed the search with G13 parity, G15 laminar lift, G19 splice, and clause drops.

---

## Obstruction audit

| Obstruction | Strategy 1 escape | Strategy 2 escape |
|---|---|---|
| **G1 RS slack cheat** | No free slack; every tile coefficient is charged. | Carries are emitted and charged; residual-zero fibers are audited. |
| **G2 affine/Graver isolation; G3 unbounded fiber audit** | Voronoi certificate covers all \(\mathbb Z^D\). | SNF/valuation statements quantify over full integral chain groups. |
| **G5 private-row overlap failure** | Complete ports are glued. | Complete overlap marginals are used. |
| **G6 invalid filtered quotient** | No external filters. | Normalization and all carries are emitted. |
| **G7 radix zero kernel** | Exact kernels remain subject to tile energy growth. | Exact kernels must gain \(2\)-adic valuation and norm. |
| **G9 degree-two parity; G11 cubic parity** | Included among unrestricted adverse ports. | Included among integral pseudosections. |
| **G12 clause drop** | DROP is an adverse transfer state. | Normalization defects pay weighted residual cost. |
| **G13 affine collision** | No compatible linear-hash claim; the all-integer tile theorem must charge it. | Formula-dependent torsion must act on its exact affine lift. |
| **G14 pair-bag finite pass** | No bag extrapolation. | No inference from a finite shell. |
| **G15 laminar zero-residual lift** | Covered as a malformed exact-kernel state. | Primary valuation test case. |
| **G19 signed flow** | No flow decomposition; splice is explicitly adverse. | Splice is seeded in the full affine fiber. |
| **G28 min-plus growth failure** | Advances only with a different tile and exact \(\lambda>\mu\). | Does not use min-plus recursion. |
| **G30 tensor seed isometry** | No tensoring. | No tensoring or paired seeds. |
| **G31 finite Walsh pass** | Requires a uniform recursion theorem. | Requires a valuation theorem. |
| **G32 additive parity; G37 universal parity cut** | Nonorthogonal gate transfer must strictly grow compatible copies. | Each lift raises valuation even for compatible copies. |
| **G33 bivector incompleteness; G34 metric-repair infeasibility** | Uses certified Delaunay cells, not exterior tags. | Uses integral torsion, not Gram synthesis. |
| **G38 finite splitter pass** | Unrelated mechanism. | Scaling comes from prime lifts, not splitter-shell extrapolation. |
| **GD1 diagonal closure of ordered-pair lifts** | No moment or diagonal tensor lift. | Diagonal attacks must acquire valuation. |
| **GD2 bicyclic group-ring units** | No convolution or group ring. | No multiplicative algebra. |

---

## Recommendation

Attempt **Strategy 1** first. It has a constant-size frontier, exact unrestricted certification machinery, and directly replaces both recently killed constructions.

**FRONTIER lemma:** the Voronoi-coercive tile lemma.

**First experiment:** exact depth-two NAND/COPY transfer search over \(D_4/E_8\) Delaunay-cell products, with Fincke–Pohst minima and a rigorous outside-shell covering certificate, testing \(\lambda/\mu\ge65/64\).

## Frontier status — goal-directed Generation 3

**Finite rejection of the repaired `D4` triality family; the Voronoi-coercive tile lemma remains unproved.** Only repaired Pro proposal 5 survived. Its causal mechanism was nonorthogonal coupling among the three 24-cell triality classes; the expected move was an empty equal-legal-radius NAND/COPY shell with exact outside-state coercivity, and an interior DROP or malformed point was the falsifier.

`experiments/verify_d4_triality_midpoint_obstruction.py` exactly covers 2,924,544 retained positive-definite label/Gram candidates. Antipodal COPY legal states have midpoint zero in the coefficient lattice, strictly inside every common sphere. Legal NAND states `011` and `101` similarly have malformed midpoint `(0,0,output-1)` strictly inside. The minimum exact inward deficits are `3/4` and `17/4`. Therefore no candidate admits the required Delaunay/Voronoi outside-shell certificate, so factor and depth-two transfer construction stop at the preregistered gate. This finite result does not rule out non-antipodal or unrelated Voronoi codebooks.

### Goal-directed Generation 4

**Finite rejection of the full prescribed non-antipodal `D4` grid; the FRONTIER remains open.** Both reviews retained only the non-antipodal continuation. Its causal mechanism was elimination of integral antipodal midpoints; its expected move was an empty equal-radius NAND sphere, and any false port on or inside that sphere was the falsifier.

`experiments/verify_nonantipodal_d4_nand_obstruction.py` exactly covers 631,701,504 candidates using a machine-checked reduction to 43 interaction signatures and 952 Grams. Equal legal NAND costs imply false-port excesses `-A+B+C,-A+B,-A+C,A`; their minimum is never positive. There are 528,417,792 strict interior cases and 103,283,712 ties. Thus every equal-radius candidate already contains an adverse Boolean point on or inside its shell; candidates without a center fail completeness. COPY and transfer tables are not authorized. This kills the declared `D4` grid, not arbitrary Voronoi-coercive tiles.

### Goal-directed Generation 5

**Finite rejection of the independent-coupling `D4` grid; the FRONTIER remains open.** Both reviews retained only the mutation `Q=K(x,y,z) tensor I4`. Its causal mechanism was independent control of the three Boolean interactions; the expected move was a strictly separated Boolean NAND shell followed by a global lattice certificate, and any malformed in-shell point was the falsifier.

`experiments/verify_independent_d4_recombination_obstruction.py` covers 2,239,488,000 candidates and finds 24,344,064 with all false Boolean ports strictly outside, so the mutation passes that preliminary gate. Every survivor nevertheless fails global emptiness. Coordinate separability lets one recombine a changed coordinate between legal `001` and `011` into two malformed `2D4*` points whose energies sum to twice the legal radius; at least one is on or inside. COPY and transfer tables therefore stop. This finite result kills the frozen independent grid but leaves nonseparable coordinate Grams and other Voronoi codebooks open.

### Goal-directed Generation 6

**The explicit `E6` Gosset shell is empty, but the prescribed port-map family is rejected; the FRONTIER remains open.** Only repaired Fable proposal 3 survived. Its causal mechanism was to start from an irreducible certified Delaunay cell and classify all shell vertices as legal NAND ports. The expected move was a complete four-word image under a bounded integral map, and any malformed or missing image was the falsifier.

`experiments/verify_e6_gosset_port_map_obstruction.py` constructs the 27-vertex minuscule cell and proves it is exactly the closed radius-`4/3` shell by an exact coefficient bound and enumeration. It then covers all `3^18` maps with entries in `{-1,0,1}` by enumerating 729 possible rows. Only the zero row takes two-valued-compatible shell values, and it is constant, so no map reaches all four NAND words. COPY and transfer tables stop. This finite result rejects the bounded map family, not larger maps, other port encodings, or other Delaunay cells.

### Goal-directed Generation 7

**All rational affine ports on the fixed `E6` shell are classified and fail NAND; the FRONTIER remains open.** Both reviews selected only coefficient-unbounded affine closure. Its causal mechanism was exact interpolation on an affine basis; the expected move was a NAND projection or a complete affine no-go, with any nonconstant NAND triple falsifying the latter.

`experiments/verify_e6_unbounded_affine_port_no_go.py` certifies affine rank six and solves all 128 binary assignments on seven independent shell vertices. Only constant rows zero and one remain binary-valued on all 27 vertices. Their eight triples have singleton images and realize none of 32 translated/relabelled NAND relations. Thus the affine-port branch of this certified shell is closed, but redundant/nonlinear ports, COPY, transfer closure, and the general Voronoi-coercive lemma remain open.

### Goal-directed Generation 8

**The frozen bounded augmented-Gram family is exactly infeasible; the FRONTIER remains open.** Only repaired Fable proposal 3 survived. Its causal mechanism was a free rational extended Gram with a diagonal-dominance tail certificate; the expected move was legal energy 64 and adverse energy at least 65, while an unrestricted DROP below 65 was the falsifier.

`experiments/verify_augmented_gram_drop_obstruction.py` gives a two-inequality certificate. The zero selector has false NAND port `000` and energy equal to the bottom-right extended-Gram entry `s`. The family bound gives `s<=64`, but soundness requires `s>=65`, hence `0>=1`. No Gram or transfer table is authorized. This kills only the prescribed entry-bound/legal-radius normalization; rescaled or otherwise frozen augmented tiles remain open.
