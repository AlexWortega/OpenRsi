Below are seven unranked mechanisms. They target the FRONTIER directly, except Sketch 7, which explicitly amends the roadmap toward Strategy 2.

### 1. Non-antipodal \(D_4\) triality with a complete ellipsoid certificate

**Core trick.** Keep the existing rational \(D_4\) Gram family, but replace antipodal truth labels by every ordered distinct non-antipodal pair. Exact ellipsoid enumeration—not midpoint testing—decides whether the legal NAND/COPY configurations are precisely the lattice points on or inside their common sphere.

**Expected move.** Produce a surviving empty Delaunay shell, then compute the unrestricted depth-two transfer table and test \(\lambda/\mu\ge65/64\).

**Obstruction audit.** G1/G6: no slack or filters. G2/G3/G14/G31/G38: a proved eigenvalue bound covers every integer point, not a named shell. G5: glue complete ports. G7/G9/G11/G12/G13/G15/G19/G32/G37/GD1: all kernel, parity, DROP, signed, and diagonal states remain unrestricted adverse states. G28: test growth directly. G30/GD2: no tensor or group ring. G33/G34: no exterior tags; the new labels lie outside the rejected family.

**Experiment.** Extend the existing verifier to all non-antipodal pairs in the three 8-sets, retaining the 952 Grams; use exact Fincke–Pohst enumeration for each feasible common sphere.

**Falsifier/death.** Every labeling has an interior malformed point, or surviving shells have \(\lambda\le\mu\).

---

### 2. Inverse Delaunay design by parity-separated secondary-cone cutting planes

**Core trick.** Choose legal coefficient vectors that are pairwise distinct modulo \(2\), eliminating integral legal-chord midpoints by construction. Jointly synthesize \(Q,c\) through the secondary cone: equal-radius equations for legal vectors, while exact CVP separation adds one violated malformed vector or depth-two transfer witness at a time.

**Expected move.** Either obtain a rational positive-definite NAND/COPY Gram with a certified \(65/64\) margin, or derive an exact Farkas certificate refuting this parity-separated template.

**Obstruction audit.** G1/G6: every coordinate is charged and emitted. G2/G3/G14/G31/G38: CVP cutting planes terminate only with a global ellipsoid certificate. G5: complete port coordinates enter the master problem. G7/G9/G11/G12/G13/G15/G19/G32/G37/GD1: each discovered exact-kernel, DROP, parity, signed, or diagonal witness becomes a mandatory cut; none is presumed absent. G28: depth-two inequality is synthesized explicitly. G30/GD2: no tensor/convolution. G33/G34: their infeasibility assumes frozen exterior vectors; these vectors are new.

**Experiment.** Use the four NAND words \(001,011,101,110\), mapped to \((a,b,c,ab,ac,bc)\in\mathbb Z^6\); solve exact rational master problems with \(-2\le z_i\le2\), then certify the resulting global bound.

**Falsifier/death.** The secondary cone is empty or witness generation cycles toward zero margin.

---

### 3. Construction-A code holes as ports

**Core trick.** Realize truth configurations as selected nearest lattice points to a Construction-A deep hole. Code minimum distance handles residue classes globally, while coordinatewise minimization inside each residue class supplies an exact all-integer outside-shell certificate.

**Expected move.** Find NAND/COPY labelings whose malformed residues have strictly larger decoding energy and whose syndrome-valued ports compose with \(\lambda/\mu\ge65/64\).

**Obstruction audit.** G1/G6: no slack or external syndrome filter. G2/G3: residue decomposition covers all \(\mathbb Z^D\). G5: glue complete syndromes and quotient coordinates. G7/G9/G11/G12/G13/G15/G19/G32/G37/GD1 are not automatically escaped: decode each corresponding kernel, parity, DROP, signed, and diagonal state exactly; reject collisions. G14/G31/G38: use the code-distance theorem, not finite extrapolation. G28: calculate transfer growth. G30: no tensor. G33/G34: no bivectors. GD2: no group ring.

**Experiment.** Enumerate the 16 residues of the extended \([8,4,4]\) Hamming code, its Construction-A hole orbits, and every four-vertex NAND labeling with integral syndrome ports; compute transfer minima by residue DP.

**Falsifier/death.** G13-type affine parity occupies the same syndrome as an honest state, or quotient energy dominates so legal and adverse growth coincide.

---

### 4. Hurwitz-quaternion norm tile

**Core trick.** Replace group-ring convolution by multiplication in the positive-definite Hurwitz quaternion order. Its norm is integral and multiplicative; units have norm \(1\), nonzero nonunits have norm at least \(2\), and there are no bicyclic zero divisors.

**Expected move.** Encode Boolean ports by non-antipodal quaternion units and prove that every false fused aggregate is either zero, separately charged, or a nonunit—giving enough norm separation for \(65/64\).

**Obstruction audit.** G1/G6: all multiplication selectors and carries are charged. G2/G3/G14/G31/G38: SNF plus exact norm-shell enumeration covers the full affine fiber. G5: glue the complete quaternion aggregate. G7/G9/G11/G12/G13/G15/G19/G32/G37/GD1 remain genuine threats; explicitly classify their aggregates rather than invoking positivity. G28: test exact transfer growth. G30: no tensor. G33/G34: fixed quaternion norm, not exterior metric repair. GD2: outside its assumption because this is a division order, not a group ring; nevertheless unintended units must be audited.

**Experiment.** Use the eight \(Q_8\) units, at most \(64\) multiplication selectors, enumerate Boolean-unit assignments, compute SNF fibers, and enumerate all vectors through the first nonunit shell.

**Falsifier/death.** A signed selector distribution evaluates to another unit—or zero—with honest boundary ports and low anchor cost.

---

### 5. Discrete-convexity no-go theorem for graph-cut/Voronoi-first-kind tiles

**Core trick.** Attempt to refute a broad frontier subclass. For an \(L^\natural\)-convex quadratic—or an obtuse-superbase lattice with the corresponding discrete midpoint inequality—partial minimization over auxiliaries preserves discrete midpoint convexity, but NAND legal states \(011\) and \(101\) force both \(001\) and malformed \(111\) into the minimizer set.

**Expected move.** Prove that no graph-cut, \(M\)-matrix, or Voronoi-first-kind certificate can realize an empty equal-radius NAND shell; amend the search to exclude that entire tractable geometry class.

**Obstruction audit.** G2/G3/G14/G31/G38: the argument quantifies symbolically over all integers. G28 is the conclusion: a malformed minimizer prevents strict growth. G1/G5/G6 and G7/G9/G11/G12/G13/G15/G19/G30/G32/G37/GD1/GD2 are encoding attacks; no encoding or hardness claim is made, so they are not assumed away. G33/G34 are covered only if their Gram satisfies the discrete-convex hypothesis; otherwise the theorem says nothing.

**Experiment.** Exhaust all \(3\)-port \(M\)-matrices with diagonal entries \(1,\dots,4\), off-diagonals \(-2,\dots,0\), half-integral centers, and one eliminated auxiliary; verify midpoint closure and search for a counterexample.

**Falsifier/death.** Partial minimization or the chosen lattice correspondence fails to preserve the required midpoint inequality.

---

### 6. Tropical nonlinear Perron–Frobenius certificate for transfer growth

**Core trick.** Once a tile has exact finite transfer closure, view binary-tree composition as a monotone homogeneous min-plus operator. A rational subeigenvector/potential can certify the adverse spectral growth rate globally; conversely, an adverse invariant ray or periodic orbit gives a reusable signed attack rather than another depth-two accident.

**Expected move.** Turn \(\lambda/\mu\ge65/64\) into an exact finite dual certificate, or refute a candidate by producing an adverse cycle with rate at most the legal rate.

**Obstruction audit.** G1/G5/G6 are prerequisites: the method cannot repair uncharged or incomplete tiles. G2/G3 require a separate exact outside-\(K\) Voronoi certificate; without it, this mechanism is invalid. G7/G9/G11/G12/G13/G15/G19/G32/G37/GD1 must be represented in \(K\) or covered outside it. G14/G31/G38: a subeigenvector proves all depths, avoiding finite extrapolation. G28 is exactly the spectral comparison. G30/GD2: no tensor or group ring. G33/G34: independent of tag geometry.

**Experiment.** Build an exact rational analyzer for the serialized G28 transfer table, recover its non-growth witness, then feed any surviving non-antipodal table into the same LP/cycle-mean engine.

**Falsifier/death.** Binary composition is not homogeneous on the proposed state quotient, or closure requires infinitely many port states.

---

### 7. Witt–Veronese prime lift of the legal-assignment sheaf

**Core trick.** Amend the roadmap from Strategy 1 to Strategy 2 if geometric searches keep failing. Enlarge each label by Teichmüller/Veronese coordinates and use a charged mapping-cone lift so honest \(0/1\) labels lift uniquely, while a defect in the saturated quotient is sent through Verschiebung and becomes coordinatewise divisible by an additional \(2\).

**Expected move.** Prove the honest-preserving prime-lift frontier by SNF over the complete chain complex, including nonlinear-feature coordinates represented by enlarged one-hot labels.

**Obstruction audit.** G1/G6: all ghost coordinates and carries are emitted. G2/G3/G14/G31/G38: saturation and SNF describe the entire integral fiber. G5: retain complete overlap marginals. G7/G9/G11/G12/G13/G15/G19/G32/G37/GD1 are explicit test classes; G13 is not automatically escaped because affine collisions may persist after Veronese lifting. G28 is inapplicable: amplification is valuation, not min-plus growth. G30/G33/G34/GD2: no tensor, exterior Gram, or group ring.

**Experiment.** On the nine-clause obstruction, build two Witt levels with degree-two label features, form the saturated honest-difference quotient, and compute SNF valuations for G13, G15, G19, DROP, and the full zero-residual affine fiber.

**Falsifier/death.** The quotient remains primitive, or a charged carry cancels the intended factor of \(2\).

Classical tools invoked: Fincke–Pohst, *Math. Comp.* 44 (1985); Conway–Sloane, *Sphere Packings, Lattices and Groups*; Murota, *Discrete Convex Analysis* (2003); Gaubert–Gunawardena, *Trans. AMS* 356 (2004); Conway–Smith, *On Quaternions and Octonions* (2003).
