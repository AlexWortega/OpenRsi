These are deliberately independent, high-risk mechanisms—not promoted hardness claims.

### 1. Discriminant-code lattice gluing
**Mechanism.** Represent each local label by a glue coset in a code lattice’s discriminant group. Shared variables identify discriminant classes globally; satisfying assignments glue to the zero class, while an inconsistent selection should occupy a nonzero coset whose minimum norm is the code distance.

**Expected move.** Obtain soundness from coset minimum rather than weighted linear residuals.

**Obstruction check.** G1: no free clause slack. G2/G3: no fixed local affine fiber. G5: classes are globally shared, not private rows. G6: every coordinate is emitted. G7: no radix, although a zero-class attack survives. G9 PSD, G11 cubic, G12 Walsh: no moment/tag construction. G13 affine collision and G15 threading remain fatal if their lift has trivial class. G14 pair bags are unused. G19 has no flow. G20’s RM, carry-table, Graver, Plücker, sheaf, rank-one, and tensor assumptions are absent.

**Falsification.** Any zero-class signed selector within baseline plus 32.

**Smallest experiment.** Replace the 23 consistency rows of the nine-clause emitter by binary \([7,3,4]\) simplex-code Construction-A blocks; enumerate obstruction/control shells exactly.

**Likely death.** Affine mixtures glue to the zero discriminant class.

---

### 2. Boolean-quotient Macaulay obstruction
**Mechanism.** Work in \(\mathbb Z[x]/(x_i^2-x_i)\). Introduce squarefree moments \(y_S\) and Macaulay rows saying every low-degree multiple of every clause-falsification polynomial evaluates to zero; a satisfying assignment supplies a rank-one evaluation vector, while unsatisfiability should eventually force an integral residual.

**Expected move.** If degree \(d=O(\log m)\) suffices, a heavy residual block gives polynomial soundness with polynomially many moments.

**Obstruction check.** G1: no clause slack. G2/G3 and G5: not local affine isolation or private composition. G6: moments and normalization must all be emitted. G7’s signed kernel becomes a pseudo-moment and is a direct falsifier. G9/G11 are only degrees two/three; this raises degree systematically. G12 has no fingerprint. G13 affine collision and G15 affine threading are not escaped if they extend to degree \(d\). G14 is unrelated. G19 has no flow. G20’s vague Plücker/sheaf lifts are avoided by a fully specified Boolean quotient, but its affine-pseudodistribution objection still applies.

**Falsification.** An integral degree-\(d\) pseudo-evaluation with \(y_\varnothing=1\) and zero clause rows.

**Smallest experiment.** Emit degrees \(0,1,2,3\) for the all-eight-clauses three-variable formula and exactly minimize each lattice.

**Likely death.** Required Macaulay degree is linear, making the lift exponential.

---

### 3. Magnetic-holonomy flow
**Mechanism.** Augment a branching flow with twisted conservation in several integral matrix representations: traversing edge \(e\) transports a fiber by \(\rho(g_e)\). Ordinary signed circulations survive scalar conservation, but should fail twisted conservation whenever their cycles have nontrivial holonomy.

**Expected move.** Kill G19’s two-negative-edge splice without duplicating the full path space.

**Obstruction check.** G1 has no slack; G2/G3 and G5 concern selector fibers, not twisted homology. G6 requires all fiber coordinates be emitted. G7’s selector kernel is outside the flow model. G9 PSD, G11 cubic, and G12 Walsh use commutative features; holonomy is noncommutative. G13 affine combinations remain dangerous if all constituent paths have identical twisted boundary. G14/G15 bag or hierarchy lifts are absent. G19 is directly targeted, not assumed solved. G20’s carry, sheaf, and transition-splicing objections still apply if a common holonomy kernel exists; this is not tensor or rank-one amplification.

**Falsification.** A depth-independent signed accepting flow lying in every twisted kernel.

**Smallest experiment.** Add two \(SL_2(\mathbb Z)\) twisted systems to the reconstructed G19 witness, then rerun shell DP through anchor excess 16.

**Likely death.** Short commutator circulations have trivial holonomy in all polynomially many representations.

---

### 4. Delaunay-shell clause geometry
**Mechanism.** Replace independent half-integral anchors by a Delaunay polytope whose legal labels are lattice points on one empty sphere. Glue clause faces along variable faces so satisfying global labelings stay on the sphere, while forbidden or signed combinations should land beyond the next Delaunay shell.

**Expected move.** Enforce integrality geometrically, without linear legality rows that affine mixtures can cancel.

**Obstruction check.** G1 has no slack. G2/G3 use affine inconsistency, whereas this uses empty-sphere separation. G5 remains a required overlap test. G6 is avoided by emitting the actual Gram matrix and target. G7 zero residual does not imply same Delaunay shell. G9 is a fixed moment PSD metric; this searches exact lattice-shell geometry. G11/G12 have no moments or tags. G13 may still produce a nearby lattice point, so it is not automatically escaped. G14 supplies a comparison control only. G15 has no hierarchy. G19 has no flow. G20’s rank-one/tensor objection is absent; its “signed points remain” objection is precisely the test.

**Falsification.** Any signed legal combination on the first shell, or failure under two-clause overlap.

**Smallest experiment.** Enumerate integral positive-definite Gram matrices of dimension at most six and entries \(\le4\) seeking seven OR labels on one shell and the forbidden label beyond \(2R\).

**Likely death.** Delaunay-shell ratios are constant and collapse under gluing.

---

### 5. Polynomial-order Reed–Solomon violation fingerprints
**Mechanism.** Map each complete assignment’s clause-violation vector \(v\) injectively to \(\xi(v)\in\mathbb F_{p^s}\), then attach the Vandermonde syndrome  
\[
(1,\xi,\xi^2,\ldots,\xi^{2h-1}).
\]
Any mod-\(p\) relation supported on at most \(2h\) distinct violation patterns vanishes only trivially; choose \(h=m^c\) and \(p>h\).

**Expected move.** Force a zero-syndrome cheat to use more than \(m^c\) assignment states or coefficients of magnitude at least \(p\).

**Obstruction check.** G1 has no slack. G2/G3/G5 concern raw local measurements. G6 demands an explicit arithmetic lift. G7’s three-term kernel should be detected. G9/G11/G12 use bounded-degree local moments/tags. G13 applies only to compatible linear hashes of raw selectors; this is nonlinear in the violation vector, but its affine lift remains a threat. G14/G15 do not provide this fingerprint. G19 transition splicing may reappear in the power-computation circuit. G20’s fixed-\(h\) tag objection is addressed by \(h=m^c\); its unspecified-lift and signed-circuit objections are not.

**Falsification.** A low-anchor signed relation canceling all powers, or a constant-cost arithmetic-circuit splice.

**Smallest experiment.** On the 16 four-variable assignments, take \(h=9,p=11\) and test the exact G13 coefficients plus exhaustive \(\ell_1\le18\) relations.

**Likely death.** Polynomial-size computation of \(\xi^j\) reintroduces signed multiplication-table pseudodistributions.

---

### 6. Chvátal–Gomory contradiction lattice
**Mechanism.** Regard the clause system as a \(0/1\) integer program and generate deterministic Chvátal–Gomory cuts. Encode each rounding step with quotient/remainder coordinates; a short satisfying vector realizes all cuts, whereas an unsatisfiable formula deriving \(0\le-1\) should force a heavily weighted final residual.

**Expected move.** Replace selector legality by an integer-proof certificate whose rank may amplify sparse unsatisfaction.

**Obstruction check.** G1’s negative-slack cheat directly threatens remainder variables; it is not escaped without a remainder cage. G2/G3/G5 selector-fiber results do not apply. G6 requires inequalities, carries, and bounds inside the CVP instance. G7 zero kernels remain possible. G9/G11/G12 metrics and tags are unrelated. G13 affine mixtures appear as fractional points and may satisfy all low-rank cuts. G14/G15 do not imply cutting-plane rank. G19 has no flow. G20’s listed RM, Graver, sheaf, Plücker, rank-one, and tensor routes are absent, but its carry-table splicing objection applies.

**Falsification.** A zero-residual signed quotient/remainder assignment, or rapidly growing cut rank.

**Smallest experiment.** Generate two CG-closure rounds for the eight-clause three-variable obstruction, emit every quotient and remainder, and exactly compare against a satisfiable seven-clause control.

**Likely death.** Nonnegativity cannot be enforced linearly, and general formulas require exponential CG rank or proof size.

Classical antecedents: Macaulay matrices (Macaulay, 1902), Delaunay/Voronoi theory (Voronoi, 1908), Reed–Solomon/Vandermonde checks (Reed–Solomon, 1960), and Chvátal–Gomory cuts (Gomory, 1958; Chvátal, 1973).
