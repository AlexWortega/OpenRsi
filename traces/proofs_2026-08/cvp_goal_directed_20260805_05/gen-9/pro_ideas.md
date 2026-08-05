All sketches target Strategy 1’s **robust integral agreement-lift lemma**. Sketches 3 and 4 explicitly propose conditional amendments; Sketch 6 seeks a no-go theorem.

### 1. Twisted unimodular holonomy

**Core trick.** Replace scalar overlap equations by \(d_e=u_v-T_eu_w\), where small \(T_e\in SL_k(\mathbb Z)\) fix the honest-label subspace but act with Kazhdan-style spectral gap on its complement. Add bounded face equations so SNF certifies that the twisted cycle module is saturated; then real expansion could imply integral energy growth.

**Expected move.** Prove the \(257/256\) inequality by separating honest invariants from affine, cut, and twisted-cycle sectors.

**Falsification/experiment.** On all twelve G38 bags, use one \(K_{3,3}\) replacement and enumerate \(2\times2\) unimodular labels with entries in \([-2,2]\). Compute depth-two minima, matched radius, twisted homology SNF, and the exact G13/G15/G19 witnesses.

**Obstruction audit.** G1/G6/G12/DROP: outside—no slack and every row is emitted. G2/G3/G14/G31/G38: outside only if the proof is uniform over \(\mathbb Z\), not a shell. G5: complete overlaps. G7, G9/G11/G13/G15, G19/GD1: not outside; holonomy must charge them. G28/G32/G37: uses twisted spectral energy, not additive composition. G30: no tensor. G33/G34, D4 triality/non-antipodal/independent recombination, and both E6 port no-gos: no shell, tags, or affine ports. GD2: no group ring.

**Likely death.** Any action fixing all honest sections may also fix their harmful affine span.

---

### 2. Torsion-free two-complex filling

**Core trick.** Lift the bag graph to a bounded-degree integral 2-complex: edge coordinates record disagreements and face coordinates record circulations. Seek \(H_1(X;\mathbb Z)=0\), saturated boundary image, and an integral filling inequality \(\|c\|^2\le C\|\partial c\|^2\), converting every signed cycle into charged face energy.

**Expected move.** Supply exactly the roadmap’s cut/cycle/saturated decomposition and prove FRONTIER through a cosystolic gap.

**Falsification/experiment.** Add every length-four face to one depth-two \(K_{3,3}\) G38 lift. Compute \(\operatorname{SNF}(\partial_2)\), integral homology, shortest nonboundary cycle, filling constant, and exact NO/YES minima.

**Obstruction audit.** G1/G6/G12/DROP: all anchors, faces, and normalizations emitted. G2/G3/G14/G31/G38: a uniform filling theorem would cover all coefficients and sizes. G5: faces use complete overlaps. G7 and G19/GD1: not outside—the homology calculation must eliminate their exact cycles. G9/G11/G13/G15: not outside; zero-cycle affine sections need a separate stalk term. G28/G32/G37: 2-dimensional filling, not min-plus/additive coupling. G30: no tensor. G33/G34, all D4 failures, and both E6 failures: no metric shell or port projection. GD2: no convolution.

**Likely death.** Bounded-degree complexes may retain free \(H_1\), torsion, or poor integral filling despite real expansion.

---

### 3. Level-indexed CRT agreement lift

**Core trick.** At level \(j\), compare overlaps modulo several explicit primes and emit every quotient/carry variable with coercive anchor weight. A discrepancy is either Archimedean-large or nonzero modulo a chosen prime; CRT uniqueness below the energy-derived coefficient bound then forbids an exact hidden kernel.

**Expected move.** Amend \(\mathcal L\) to explicit level-indexed \(\mathcal L_j\). This is justified because the needed prime product depends on \(R_j\), absent from the fixed-lift lemma; rank growth remains constant and bit complexity polynomial.

**Falsification/experiment.** Apply primes \(17,19\) to one two-level G38 \(K_{3,3}\) lift. Emit carries explicitly, derive the coefficient bound, and solve the exact unrestricted CVP plus SNF kernels.

**Obstruction audit.** G1/G6/G12/DROP: not outside until a carry-energy inequality is proved; all such coordinates are emitted. G2/G3/G14/G31/G38: CRT proof must be bound-uniform, not finite extrapolation. G5: complete overlaps. G7: directly targeted. G9/G11/G13/G15 and G19/GD1: not outside; enumerate their congruence classes. G28/G32/G37: multiplicative CRT separation, not additive recurrence. G30: no tensor. G33/G34, D4, E6: no shells or ports. GD2: no group ring, though unit-like carry cancellation remains possible.

**Likely death.** Carries may reproduce G1 at constant cost, or varying weights may destroy fixed legal multiplier \(\mu\).

---

### 4. Regular-matroid compilation

**Core trick.** Amend Lemma 1 so the global disagreement matrix has a bounded-size totally unimodular extension, hence defines a regular matroid. Integral cut/cycle decomposition is then primitive and torsion-free; ordinary expander estimates can be applied without losing information when passing from real to integral modules.

**Expected move.** Prove FRONTIER for “regular legal sheaves,” then show every balanced selector sheaf admits a rank-\(\le4096\) regular extension.

**Falsification/experiment.** Run TU recognition on the G38 overlap matrix and search signed-column extensions of size at most twice its rank. If found, apply one cubic expander lift and compute exact depth-two minima and circuit decomposition.

**Obstruction audit.** G1/G6/G12/DROP: legality and normalization remain emitted. G2/G3/G14/G31/G38: TU gives an all-\(\mathbb Z\) structural statement, not a shell. G5: full marginals enter the common matrix. G7: saturation removes torsion but not genuine kernels—so not outside. G9/G11/G13/G15 and G19/GD1: also not automatically outside; their regular circuits must gain expander energy. G28/G32/G37: uses matroidal decomposition rather than fixed min-plus/additivity. G30: no tensor. G33/G34, all D4 and E6 obstructions: no shell or port map. GD2: no group algebra.

**Likely death.** SAT legality may have no constant-size TU extension; affine parity circuits can survive even in regular matroids.

---

### 5. Finite-field projective tomography

**Core trick.** Replace ordinary marginals by line sums of selector distributions under an embedding of labels into \(\mathbf P^2(\mathbb F_p)\). Each lift uses several transverse projective directions; finite-geometry incidence distance should force any non-delta signed distribution to produce many disagreement coordinates while honest labels retain equal radius.

**Expected move.** Obtain scalable coding-theoretic amplification without PCP tests: every line-sum coordinate is explicitly part of the CVP objective.

**Falsification/experiment.** Use \(p=3\), all thirteen projective lines, and the twelve G38 bags. Compute the integer kernel and exact costs of DROP, G13, G15, G19, and every kernel vector through anchor excess \(64\).

**Obstruction audit.** G1/G6/G12/DROP: no slack; line sums and normalization are charged. G2/G3/G14/G31/G38: only escaped by a general integer tomography theorem, not this finite test. G5: all projective directions are globally compared. G7 and G9/G11/G13/G15: not outside; zero-tomography affine mixtures are the decisive threat. G19/GD1: signed distributions are included. G28/G32/G37: code-distance growth, not additive metric coupling. G30: no literal tensor. G33/G34, D4, E6: no exterior/Voronoi/port geometry. GD2: no group ring.

**Likely death.** Any deterministic feature of an honest assignment may lift the G13 affine combination exactly, making every line sum vanish.

---

### 6. Affine-functoriality no-go theorem

**Core trick.** Attempt to refute FRONTIER for every lift whose canonical honest lift is affine in the original selector vector. Affine pseudosections with coefficients summing to one then lift with zero residual; a generalized Rayleigh quotient can test whether some such direction grows by at most the legal multiplier \(\mu\).

**Expected move.** Either produce an exact universal counterexample or prove that any viable lift must introduce a genuinely non-affine enlarged encoding, thereby amending the roadmap’s admissible lift class.

**Falsification/experiment.** For each connected degree-\(\le4\) replacement graph on at most eight vertices, lift the sixteen honest global G38 sections, apply the known G13 affine coefficients, and compare its exact energy ratio with \(\mu\).

**Obstruction audit.** G1/G6/G12/DROP: evaluate the complete emitted objective. G2/G3/G14/G31/G38: symbolic affine identities hold for all coefficients, not just shells. G5: allow complete overlaps. G7, G9/G11/G13/G15, G19/GD1: these supply candidate witnesses rather than assumptions being escaped. G28/G32/G37: no positive composition claim. G30: no tensor assumption. G33/G34, D4, E6: irrelevant because the theorem concerns linear selector lifts. GD2: no group-ring hypothesis.

**Likely death.** Canonical lifting may be nonlinear in old selectors through new joint labels, so the affine witness need not exist.

---

### 7. Rational quadratic dissipation certificate

**Core trick.** Search for a rational PSD potential \(P\) on the complete SNF disagreement state such that each lift step satisfies
\[
E_{\rm out}+\Phi_{\rm out}\ge \frac{257}{256}(E_{\rm in}+\Phi_{\rm in}).
\]
Verify it on every residue class by completing squares over the full integer lattice; summing cancels potentials and proves all-depth growth.

**Expected move.** Turn FRONTIER into a finite exact certificate while still quantifying over arbitrary coefficients.

**Falsification/experiment.** For one G38 \(K_{3,3}\) lift, synthesize \(P\) numerically, reconstruct it rationally, then certify each SNF class by exact LDL elimination. Include the matched control and named attacks.

**Obstruction audit.** G1/G6/G12/DROP: their coordinates appear in \(E\). G2/G3/G14/G31/G38: residue-wise quadratic certification is all-\(\mathbb Z\), unlike bounded shells. G5: state contains complete overlaps. G7, G9/G11/G13/G15, G19/GD1: not outside; each must satisfy the same inequality. G28: unlike fixed min-plus tables, this is a parametric quadratic certificate over the saturated module. G32/G37: additive parity may directly disprove feasibility. G30: no tensor. G33/G34, D4, E6: no shell synthesis. GD2: no convolution algebra.

**Likely death.** Compatible parity witnesses may force an exact dual certificate showing no positive dissipation potential exists.
