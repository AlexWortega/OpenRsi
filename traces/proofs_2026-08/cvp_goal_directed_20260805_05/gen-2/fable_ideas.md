I treat the frozen ordered-pair emitter as dead; none of the mechanisms below merely adds more linear marginals to it.

### 1. Diagonal-naturality no-go theorem

**Core trick.** Formalize a *copy-natural linear lift*: tuple columns admit \(D_k e_t=e_{(t,\ldots,t)}\), and every row orbit satisfies \(A_kD_k=U_kA_1\). Then any exact signed accepting flow \(s\) yields \(D_ks\) with zero residual and only \(O(\#\text{negative}(s))\) anchor excess over \(R_k^2\), refuting \(4/3\) amplification.

**Expected move.** Prove this for the entire row grammar allowed by ROADMAP Lemma 2, forcing an explicit amendment to non-natural/nonlinear selector tables.

**Falsification/test.** Symbolically enumerate transition, marginal, query, source, ACCEPT, and coherence row orbits on the minimal G19 support; check the intertwining identity for \(k=2,3\). Falsification is one completeness-preserving row orbit violating it.

**Likely death.** The theorem may cover only linear-natural lifts, leaving finite nonlinear composition tables untouched.

**Audit.** G1 RS slack: none. G2/G3 affine/Graver and unbounded fiber: proof is over all \(\mathbb Z\). G5 private overlap: full row orbits. G6 filtered quotient: all rows emitted. G7 radix kernel: exact kernels are the witness. G9/G11 parity, G12 DROP, G13 affine collision, G15 laminar lift, G19 signed flow: all quantified. G14/G31/G38 finite passes: no extrapolation. G28 min-plus: no tile claim. G30 tensor isometry: diagonal naturality is proved, not assumed. G32/G37 additive parity: covered. G33/G34 exterior/metric: unused.

---

### 2. Cosystolic covering complex

**Core trick.** Regard transition flows as integral 1-chains and attach 2-cells for every legal conservation/query-consistency square. Take deterministic finite covers whose relative chain complexes have cosystolic expansion: a non-honest accepting cycle should either bound an honest path certificate or have support—and hence anchor energy—expanded at every cover level.

**Expected move.** Replace tuple coherence by a topological lift proving \(4/3\) growth from a relative systolic inequality.

**Falsification/test.** Extract the minimal G19 splice complex, enumerate all two-sheet \(\mathbb Z_2\)-voltage covers, emit lifted incidence and 2-cell rows, and solve the unrestricted accepting MILP. Any lifted zero-residual splice below threshold kills the cover.

**Likely death.** The splice may be an integral boundary in every cover, so cosystolic expansion never sees it.

**Audit.** G1: no slack. G2/G3: integral homology and MILP are unbounded. G5: complete cell boundaries, not private rows. G6: every boundary condition is emitted. G7: zero kernels are charged only if homologically nontrivial—otherwise failure. G9/G11 parity and G13/G15 affine lifts are explicit cycles. G12 DROP is a relative-chain state. G19 is the seed. G14/G31/G38: no finite-shell inference; a cover theorem is required. G28: no frozen tile. G30: no tensor/rank-one premise. G32/G37: coupling is shared topology, not orthogonal addition. G33/G34: no exterior tags or metric repair.

---

### 3. Nonabelian group-algebra convolution tile

**Core trick.** Use Barrington’s \(A_5\) products directly. At each balanced node, introduce 3,600 selectors indexed by \((g,h)\in A_5^2\), parent port \(gh\), and all coordinates of the integral regular representation; Parseval-type group-algebra energy becomes the candidate coercive potential.

**Expected move.** Prove that a unit-mass signed convolution claiming ACCEPT is either a delta product from an honest path or gains \(4/3\) energy under composition.

**Falsification/test.** Build one two-child \(A_5\) tile, restrict leaves to transitions appearing in the minimal G19 splice, enumerate every integral port state through \(4\mu/3\), then compose two tiles exactly.

**Likely death.** Low-norm zero divisors or idempotents in \(\mathbb Z[A_5]\) may reproduce signed splicing.

**Audit.** G1: no slack. G2/G3: table plus recession analysis covers all integers. G5: complete group ports. G6: mass/product/ACCEPT are rows. G7: exact group-algebra kernels remain in the table. G9/G11 parity, G12 DROP, G13 affine, G15 zero-residual, G19 splice: seeded as adverse ports. G14/G31/G38: no finite extrapolation without a convolution theorem. G28: different 3,600-state group tile, but its \(\lambda>\mu\) warning applies honestly. G30: not literal Kronecker or rank-one. G32/G37: multiplication is nonadditive. G33/G34: integral permutation representations avoid exterior metrics.

---

### 4. Signed direct-product agreement code

**Core trick.** Encode overlapping windows of the transition transcript using a constant-degree Tanner complex: each check has selectors for complete legal local transcripts, and adjacent checks emit full marginal equalities. Unique-neighbor expansion should turn any sparse signed deviation into many violated checks; a dense deviation already pays large anchor norm.

**Expected move.** Prove a signed-integral agreement theorem, rather than importing the usual nonnegative direct-product test, and derive \(4/3\) growth per expansion level.

**Falsification/test.** Pad the minimal G19 splice to seven symbols, use the Fano-plane incidence graph with seven degree-three checks, enumerate all legal check selectors, and optimize unrestricted integers exactly.

**Likely death.** A Tanner pseudocodeword may preserve every marginal with constant negative support.

**Audit.** G1: no slack. G2/G3: theorem must quantify over all integral pseudocodewords. G5: complete overlap marginals. G6: no external consistency. G7: exact-code kernels are the primary falsifier. G9/G11/G32/G37 parity is seeded and checks overlap nonorthogonally. G12 DROP is included. G13 affine and G15 laminar lifts are unrestricted pseudocodewords. G19 supplies the seed. G14/G38: unlike their finite bag passes, promotion requires unique-neighbor scaling. G31: no finite ratio extrapolation. G28: not the frozen min-plus tile. G30: no tensor/rank-one assumption. G33/G34: ordinary one-hot anchors, not exterior geometry.

---

### 5. Higher Lawrence lifting and global Graver decomposition

**Core trick.** Replace ordered tuples by the \(r\)-th Lawrence lifting of the complete Barrington incidence matrix. Its integer kernel has a conformal Graver decomposition; the desired lemma becomes: every accepting Graver element either contains an honest accepting path or has type/norm growing by at least \(4/3\) per lift.

**Expected move.** Either obtain a rigorous all-integer decomposition proof or show that the G19 circuit has bounded Graver type at every \(r\), refuting this entire algebraic route.

**Falsification/test.** Extract the smallest submatrix supporting the two-negative splice, form its second Lawrence lifting, compute primitive circuits by exact kernel enumeration, and compare their CVP costs with \(4R_2^2/3\).

**Likely death.** Lawrence Graver complexity often stabilizes; a type-one diagonal circuit may persist forever.

**Audit.** G1: no slack. G2/G3: this is global exact Graver theory, not bounded local isolation. G5: lift uses the full incidence matrix. G6: all equations are emitted. G7: zero-kernel circuits are precisely analyzed. G9/G11 parity, G12 DROP, G13 affine, G15 zero-residual, G19 signed flow: included among circuits. G14/G31/G38: no shell extrapolation. G28: no min-plus recurrence. G30: Lawrence lifting is not literal tensoring and assumes no rank one. G32/G37: additive circuits are explicitly primitive candidates. G33/G34: no exterior tags or synthesized metric.

---

### 6. Truncated path signatures and shuffle coherence

**Core trick.** Replace layerwise moments by the truncated noncommutative signature of the transition word. Balanced interval selectors encode boundary states and degree-\(\le k\) words; Chen concatenation and shuffle identities are enforced through finite local selector tables, so honest paths are group-like while generic signed mixtures are not.

**Expected move.** Show that every falsely accepting integral signature either comes from an honest path or violates enough shuffle coordinates to gain \(4/3\) energy per degree.

**Falsification/test.** On the minimal G19 support, emit degree-two words and every exact concatenation/shuffle port, use one-hot interval anchors for equal completeness, and solve the unrestricted MILP below \(4R_2^2/3\).

**Likely death.** A signed combination of group-like signatures may itself satisfy all truncated shuffle identities; this would be a disguised diagonal embedding.

**Audit.** G1: no slack. G2/G3: complete port tables plus recession analysis cover all integers. G5: full signature ports, not private coordinates. G6: shuffle and acceptance are emitted. G7: exact signature kernels are searched. G9/G11 parity, G12 DROP, G13 affine, G15 laminar, G19 splice: explicitly seeded. G14/G31/G38: no finite-degree pass is promoted without induction. G28: not the frozen pair tile, though its growth failure is a mandatory test. G30: tensor words are used, but neither literal seed tensoring nor rank one is assumed. G32/G37: shuffle coupling is nonorthogonal. G33/G34: no exterior bivectors or metric repair.
