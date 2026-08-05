1. **Principal-angle operator inequality.** Rewrite the \(k\)-lift energy as a quadratic form on the affine ACCEPT fiber, then quotient by exact transition, marginal, and query-consistency subspaces. Seek a rational operator inequality showing that the least eigenvalue on the remaining “incoherent” subspace multiplies by \(4/3\) under one coherent lift.

**Expected move.** Prove the FRONTIER over \(\mathbb R\), which immediately covers unrestricted integers.

**Falsification/experiment.** For the minimal G19 splice, construct exact \(k=1,2\) quotient matrices and certify the generalized eigenvalue using rational LDL decomposition. Any eigenvalue below \(4/3\), rounded to an integer vector by exact branch-and-bound, kills the route. Most likely death: a low-energy fractional accepting direction.

**Obstruction audit.** G1 slack/G7 radix: neither is used. G2 affine isolation/G3 unbounded fiber: the inequality covers all reals. G5 overlap/G6 filtered quotient: all tuple rows remain in the matrix. G9/G11 parity, G12 DROP, G13 affine collision, G15 laminar lift, G19 splice, G32 additive parity, and G37 parity cut are not assumed absent—they lie in the tested subspace. G14/G31/G38 finite passes are not extrapolated. G28 min-plus, G30 literal seed tensor, and G33/G34 exterior metrics are unused.

2. **Global Graver augmentation of the accepting fiber.** Introduce charged residual variables so the objective is separable convex subject to one integral system, then use global Graver augmentation theory (Graver, 1975), not local affine isolation. Classify primitive sign-compatible moves of the full \(k\)-lift and try to prove that every accepting nonpath requires enough costly primitive moves to yield \(4/3\) growth.

**Expected move.** Reduce the FRONTIER to a finite inequality for primitive global circuits; alternatively expose one primitive counterexample.

**Falsification/experiment.** Run `4ti2` on the smallest G19 program after contracting forced layers, first at \(k=1\), then \(k=2\); evaluate every Graver element exactly. Most likely death: enormous primitive circuits whose residual effects cancel while coefficient cost stays small.

**Obstruction audit.** G1/G7: residual variables are charged, with no slack amplification. G2/G3: this is a global unbounded Graver basis, not bounded local isolation. G5/G6: complete emitted rows define the fiber. G9/G11/G12/G13/G15/G19/G32/G37: their vectors must decompose and are explicit falsifiers; no positivity is assumed. G14/G31/G38: no finite-shell scaling claim. G28: no frozen tile recurrence. G30: no rank-one tensoring. G33/G34: no tag metric. A cheap Graver representative of any named attack honestly kills the mechanism.

3. **Relative homology and cosystolic expansion.** Regard transition conservation as a boundary operator and repeated-query identifications as attached 2-cells; an accepting signed splice becomes a relative integral cycle. Identify the coherent \(k\)-lift with a product complex and seek a Künneth-compatible cosystolic inequality whose product expansion is at least \(4/3\).

**Expected move.** Either prove that every nontrivial ACCEPT-relative homology class expands multiplicatively, or refute the FRONTIER by finding a cheap persistent class.

**Falsification/experiment.** Extract the conservation closure of the two-negative G19 splice, compute Smith normal form and weighted cosystolic minima for its square, and compare with \(4R_2^2/3\). Most likely death: the complex has a free or torsion class with constant-size representatives under products.

**Obstruction audit.** G1/G7: no residual spreading. G2/G3: integral homology and SNF are unbounded certificates. G5/G6: every gluing row is a cell, never an external filter. G9/G11 parity, G12 DROP, G13 affine collision, G15 lift, G19 splice, G32/G37 additive parity are not excluded; they become candidate cycles. G14/G31/G38 finite passes are unused. G28 min-plus and G30 seed tensor are replaced by a product theorem for complexes. G33/G34 exterior geometry is irrelevant. G5 private-overlap failure specifically appears as extra homology and therefore falsifies rather than evades the test.

4. **Low-degree Nullstellensatz separator.** Encode honest paths by Boolean transition variables and place conservation, repeated queries, and ACCEPT in an ideal. Since the NO instance has no consistent accepting path, search for an integral/rational Nullstellensatz identity whose degree-\(k\) monomials are exactly represented by ordered tuple columns; bound the certificate norm so Cauchy–Schwarz forces \(4/3\) energy growth.

**Expected move.** Convert algebraic infeasibility into the FRONTIER inequality without nonnegativity or rank-one assumptions.

**Falsification/experiment.** On a contracted G19 splice, solve the degree-2 Macaulay system exactly and optimize the smallest certificate norm; compare its induced lower bound with \(4/3\). Most likely death: certificate degree or coefficient norm grows with \(L\), not with logarithmic \(k\).

**Obstruction audit.** G1/G7: no slack or radix. G2/G3: an ideal identity holds for every integer—and real—vector after linearization. G5/G6: all consistency polynomials are emitted. G9/G11/G12/G13/G15/G19/G32/G37 are not automatically escaped; each may define a low-degree pseudo-solution and thus kill the certificate. G14/G31/G38: no finite shell is extrapolated. G28/G30: neither tile recursion nor literal tensoring is used. G33/G34: no exterior metric. G13 remains especially dangerous: an affine collision surviving all degree-\(k\) monomials falsifies the mechanism.

5. **Tuple-level expander-code fingerprint — conditional amendment to Lemma 2.** Attach direct, charged simplex/BCH-style coordinates to ordered transition tuples, with symbols given by degree-\(k\) functions of the complete tuple label. Honest paths retain equal radius, while a nonpath signed measure should acquire a nonzero codeword whose distance supplies multiplicative energy.

**Expected move.** Amend the coherent lift only if a deterministic code gives at least \(4/3\) additional squared cost per level.

**Falsification/experiment.** For the G19 \(k=2\) lift, enumerate small primes and all degree-two tuple characters, then MILP-optimize the unrestricted accepting fiber. Most likely death: a tuple-level affine collision annihilates every compatible fingerprint.

**Obstruction audit.** G1 slack/G7 radix: symbols are direct coordinates; no carries or free slack. G2/G3: MILP and the proposed theorem quantify over all integers. G5/G6: full tuple ports and code coordinates are emitted. G13 is outside the proved raw-selector obstruction only because features live on enlarged tuples; its tuple analogue would kill this amendment. G9/G11 parity, G12 DROP, G15 lift, G19 splice, G32/G37 parity remain mandatory code tests. G14/G31/G38 finite passes are not reused. G28 has no tile recursion; G30 is formula-aware, not literal seed tensoring. G33/G34 are irrelevant because orthogonal simplex anchors guarantee completeness.

6. **Exact Presburger/min-plus pumping attack.** Treat a fixed-\(k\) unrestricted flow search as a weighted automaton whose state records the complete boundary tuple flow, repeated-query totals, and accumulated quadratic cost. Presburger elimination can produce either a closed recurrence proving the claimed lower bound or a pumpable low-mean cycle yielding arbitrarily long counterexamples.

**Expected move.** Preferentially refute the FRONTIER by turning the local G19 splice into a scalable family; a positive minimum-cycle certificate would instead support it.

**Falsification/experiment.** Build the exact \(k=2\) automaton for the smallest splice after forced-layer contraction and compute its minimum cycle mean. Most likely death: query totals make the exact state space unbounded or doubly exponential.

**Obstruction audit.** G1/G7: exact coefficient cost is retained. G2/G3: Presburger states represent all integers, not a box. G5/G6: complete interfaces are state coordinates and emitted rows. G9/G11/G12/G13/G15/G19/G32/G37 are explicit initial/pump states, not assumed away. G28 is avoided only if closure is proved for the complete S1 boundary, unlike its frozen reduced tile. G14/G31/G38 are not extrapolated finite passes. G30 literal tensoring and G33/G34 metric synthesis are unused. A semilinear cheap DROP or parity cycle honestly refutes the roadmap lemma.

7. **Signed hypercontractivity on occurrence cubes.** View an accepting flow as a signed measure on independently queried variable occurrences; consistency is the diagonal subcube, and the \(k\)-lift records degree-\(k\) marginals. Use Fourier/Krawtchouk analysis to lower-bound the \(\ell_2\) norm of any signed measure supported on accepting inconsistent words while matching diagonal marginals.

**Expected move.** Prove a chi-square growth inequality of \((4/3)^k\), or identify a low-degree dual polynomial refuting that constant.

**Falsification/experiment.** For the minimal G19 splice, construct the degree-\(\le2\) moment matrix, compute its exact Christoffel function on the accepting support, and recover the extremal signed measure. Most likely death: acceptance contains a small orthogonal array indistinguishable from the diagonal through degree \(k\).

**Obstruction audit.** G1/G7: the bound concerns coefficient norm, not residual amplification. G2/G3: the extremal problem permits arbitrary real signed measures. G5/G6: all occurrence marginals are included. G9/G11 parity, G13 affine collision, G15 lift, G19 splice, G32/G37 additive parity are precisely low-degree designs and may kill it; G12 DROP is included as mass loss. G14/G31/G38 finite passes supply no premise. G28/G30 recursion and literal tensors are unused. G33/G34 exterior metrics are unused. Unlike G31, success requires a theorem for every \(k\), not a finite Walsh shell.
