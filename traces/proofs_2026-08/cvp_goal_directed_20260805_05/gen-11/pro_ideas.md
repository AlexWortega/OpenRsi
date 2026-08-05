All seven sketches target the **ramified adverse-filtration lemma**. They are intentionally nonconvergent: five try to prove it, one is a proof-or-counterexample engine, and one amends the quaternion edge.

### 1. Skew-Rees associated-graded certificate

**Mechanism.** Filter the complete selector/carry complex by \(\mathfrak P^j\) and form its skew Rees complex; locally,  
\[
\operatorname{gr}_{\mathfrak P}\mathcal O\simeq \mathbb F_{17^2}[\tau;\mathrm{Frob}].
\]
Design NAND/COPY modules so the adverse associated-graded differential is block-triangular and has no homology below grade \(h\). Filtered induction would then force either a nonzero grade-\(h\) defect or a representative whose selector norm already exceeds that defect’s trace norm.

**Expected move.** Prove FRONTIER through exactness of every graded adverse quotient, rather than enumerating attacks.

**Falsification/death.** Any grade-zero homology class with false boundary—most likely the G13 affine class—kills the construction.

**Experiment.** Enumerate \(\le8\)-selector modules over \(\mathbb F_{289}\); compute graded homology at depths one and two, then lift survivors and audit by SNF.

**Audit.** No slack/filter/radix/free target (G1,G6,G7,G12/DROP); no bounded-shell inference (G2,G3,G14,G31,G38). G5,G9,G11,G13,G15 and G19,GD1,ordered-pair splice are **not outside**: they must appear as graded homology and kill candidates. No min-plus/additive/tensor step (G28,G32,G37,G30). Division excludes GD2/A5 zero divisors. No exterior metric (G33,G34), D4 midpoint/non-antipodal/recombination shell, or E6 bounded/unbounded affine port. The balanced circuit is connected, avoiding padding dilution.

---

### 2. Noncatastrophic skew-convolutional code

**Mechanism.** Expand coefficients in Teichmüller–\(\mathfrak P\) digits and make recursive gates a systematic convolutional encoder over the Ore ring \(\mathbb F_{289}[D;\mathrm{Frob}]\). A false root becomes a nonzero terminal syndrome; noncatastrophicity plus linear column-distance growth forces either \(h\) charged digits or a surviving state multiplied by \(\mathfrak P^h\). Every digit carry and syndrome equation is emitted.

**Expected move.** Replace the desired adverse-filtration inequality by a classical code-distance statement uniform in depth.

**Falsification/death.** The likely failure is a zero-syndrome affine pseudosection: nonlinear semantic labels may still become linear after selectorization.

**Experiment.** Exhaust memory-one \(2\times3\) skew encoders with four Boolean port states; test NAND/COPY semantics and depth-two unrestricted minima.

**Audit.** G1,G6,G7,G12/DROP are excluded by emitted digit/carry equations. G2,G3,G14,G31,G38 require a symbolic noncatastrophic theorem, not finite extrapolation. G5,G9,G11,G13,G15 and G19,GD1,ordered-pair are **not excluded**; exact syndrome tests must detect them. G28,G32,G37 are avoided by column distance, not additive supergrowth; G30 is absent. The division order avoids GD2/A5. G33,G34, all D4 obstructions, and both E6 affine-port no-gos concern unused geometries. A single connected encoder defeats padding dilution.

---

### 3. Dieudonné-determinant transfer invariant

**Mechanism.** Encode each gate as a small block transfer matrix over \(D\), with all matrix products expanded through emitted selector/product-table coordinates. Arrange the false-root boundary so a designated boundary matrix has Dieudonné-determinant valuation at least \(h\); add a quasideterminant coordinate to ensure the witness is nonzero. Determinant valuation is additive for arbitrary full-rank matrix couplings, not only rank-one substitutions.

**Expected move.** Prove FRONTIER by converting every unrestricted adverse coupling into a high-valuation determinant or a singularity with large selector charge.

**Falsification/death.** Signed couplings may make the boundary matrix singular at nearly legal cost; determinant \(0\) then supplies no nonzero \(\alpha\).

**Experiment.** Search \(2\times2\) transfer matrices with \(\le6\) selectors over \(\mathcal O/\mathfrak P^2\); compose two gates and enumerate all singular and nonsingular adverse states.

**Audit.** G1,G6,G7,G12/DROP are excluded only if every multiplication/carry/boundary row is emitted. G2,G3,G14,G31,G38 require an all-matrix determinant proof. G5,G9,G11,G13,G15 and G19,GD1,ordered-pair are **not outside**; they are mandatory singular cases. No G28/G32/G37 recurrence or G30 tensor. GD2/A5 is also **not automatically escaped**, since matrix algebras contain nilpotents; determinant must neutralize them. G33,G34, D4, and E6 assumptions are absent. Connected transfer composition avoids padding.

---

### 4. Bruhat–Tits tree coercion

**Mechanism.** Use the Bruhat–Tits tree of \(\mathrm{PGL}_2(D_{17})\). Boolean ports are oriented residue directions; NAND/COPY modules are finite convex correspondences, and recursion glues them along geodesics. If legal correspondences have zero Busemann drift while every false-root chain crosses one additional wall per level, Cartan displacement gives valuation \(h\), hence reduced-norm energy.

**Expected move.** Prove FRONTIER as an integral filling inequality in a tree, including arbitrary signed chains.

**Falsification/death.** Oppositely oriented signed chains may cancel all Busemann drift while retaining the false boundary.

**Experiment.** Restrict to four residue directions in the radius-two ball of the \(290\)-regular tree; enumerate \(\le8\)-selector correspondences and solve the depth-two integral chain problem.

**Audit.** All incidence, wall, and boundary rows must be emitted, excluding G1,G6,G7,G12/DROP. A tree filling theorem, not finite shells, addresses G2,G3,G14,G31,G38. G5,G9,G11,G13,G15 and G19,GD1,ordered-pair are **not outside**; they are signed chains in the filling problem. No min-plus/additive/tensor argument (G28,G32,G37,G30). GD2/A5 convolution is absent, though analogous unipotent cancellation remains possible. G33,G34, D4 midpoint/non-antipodal/recombination, and E6 affine ports use different finite Euclidean shells. The tree is attached to one connected circuit, so padding cannot dilute displacement.

---

### 5. Congruence-subgroup commutator amplifier

**Mechanism.** Encode truth in opposite root subgroups \(x_+(a),x_-(b)\subset \mathrm{SL}_2(\mathcal O)\). AND is detected by their commutator and NAND by complementing its output; congruence calculus gives  
\[
[U^r,U^s]\subseteq U^{r+s}.
\]
Balanced substitution could therefore push a false root rapidly down the congruence filtration. A Hall-basis normal form would classify arbitrary products and signed selector couplings.

**Expected move.** Prove a stronger-than-linear valuation recursion, then weaken it to FRONTIER.

**Falsification/death.** A commuting graded direction, or cancellation between opposite commutators, may leave a valuation-zero false-root unit.

**Experiment.** Implement \(\mathcal O/\mathfrak P^4\), enumerate Boolean root-subgroup labels, verify NAND tables, and exhaust depth-two Hall words of selector excess at most \(16\).

**Audit.** Emitted collection/carry rows avoid G1,G6,G7,G12/DROP. A uniform Hall theorem is needed beyond G2,G3,G14,G31,G38. G5,G9,G11,G13,G15 and G19,GD1,ordered-pair are **not outside**; they must reduce to nontrivial Hall coordinates. No G28/G32/G37 min-plus/additivity and no G30 tensor. Because \(\mathrm{M}_2(D)\) has nilpotents, GD2/A5 is **not escaped automatically**. No G33/G34 exterior tags, D4 shells, or E6 affine ports. Balanced connected compilation handles padding.

---

### 6. \(p\)-adic automaton as a proof-or-counterexample engine

**Mechanism.** Freeze a candidate gate library and express “depth \(h\), false root, defect valuation \(<h\), and subthreshold charge” as recursive digit constraints over \(\mathbb Q_{17}\). Exact \(p\)-adic cell decomposition or a minimized tree automaton can yield a pumping theorem: either bad states disappear for all \(h\), proving FRONTIER, or a reachable cycle generates explicit counterexamples at every depth.

**Expected move.** Classify the complete saturated adverse quotient algorithmically rather than guessing named attacks.

**Falsification/death.** The state space may not stabilize because archimedean energy bounds retain increasingly many coefficient digits.

**Experiment.** Generate exact adverse digit automata for depths \(1\)–\(4\), minimize them, and search for a cycle preserving false boundary with valuation deficit.

**Audit.** Here no obstruction is assumed away: G1,G6,G7,G12/DROP are explicit residual states; G5,G9,G11,G13,G15, G19,GD1,ordered-pair, and GD2/A5 are seeded states. G2,G3,G14,G31,G38 are addressed only if pumping proves all-depth/all-coefficient coverage. Unlike G28,G32,G37, this is not inference from a finite min-plus table; a formal pumping certificate is required. G30 is absent. G33,G34, D4 midpoint/non-antipodal/recombination, and E6 bounded/unbounded ports are irrelevant to the frozen quaternion library. Connected-circuit size is part of the automaton, exposing any padding failure.

---

### 7. Multi-ramified-prime amendment

**Mechanism.** Amend Strategy 2 to a definite quaternion algebra ramified at  
\[
\{\infty,17,19,23\},
\]
and require one CRT-compatible gate library across the three residue fields. The revised frontier asks for a nonzero defect in  
\[
\mathfrak P_{17}^h\mathfrak P_{19}^h\mathfrak P_{23}^h
\]
or equivalent charged energy. Reduced norm then gains at least \((17\cdot19\cdot23)^h\), potentially overwhelming legal module growth.

**Expected move.** Remove valuation-zero bypasses that survive at one prime; this explicitly amends the fixed-\(17\) roadmap edge.

**Falsification/death.** An integral affine pseudosection survives every prime simultaneously, or no small gate table satisfies all three residue semantics.

**Experiment.** Search one common \(\le8\)-selector NAND/COPY support by finite-field linear algebra at all three primes; combine by CRT and perform a depth-two SNF audit.

**Audit.** All rows are emitted, avoiding G1,G6,G7,G12/DROP; proof must remain uniform beyond G2,G3,G14,G31,G38. G5,G9,G11,G13,G15 and G19,GD1,ordered-pair are **not outside**—a common integral instance kills the amendment. No G28/G32/G37 or G30. Division excludes GD2/A5 zero divisors at each ramified place. G33,G34, D4, and E6 concern unused constructions. Connected compilation handles padding.

Classical ingredients invoked here include Dieudonné’s noncommutative determinant, Bruhat–Tits buildings as presented in Serre’s *Trees* (1980), maximal orders as in Reiner’s *Maximal Orders* (1975), and standard filtered-complex spectral sequences.
