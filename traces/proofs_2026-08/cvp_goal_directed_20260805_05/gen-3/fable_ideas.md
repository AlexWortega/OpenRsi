The fixed target is the **Voronoi-coercive tile lemma**. The sketches below either attack that lemma directly or explicitly amend only its homogeneous-recursion edge.

### 1. Discrete-convex selector tile

**Mechanism.** Design the tile objective so each fixed-port selector fiber is \(M\)-convex: every nonminimum integer vector admits a cost-decreasing two-coordinate exchange. Equal-cost NAND/COPY states are prescribed minima; an exact exchange certificate then reduces unrestricted minimization to finitely many exchange-stable representatives without imposing coefficient bounds.

**Expected move.** Prove transfer closure and \(\lambda/\mu\ge65/64\) from symbolic exchange inequalities on a rational Gram matrix.

**Obstruction audit.** **G1**: no slack; all coordinates occur in the Gram form. **G2/G3**: the exchange theorem covers the entire integer fiber. **G5**: use complete ports. **G6**: all constraints are emitted. **G7, G9, G11, G12, G13, G15, G19** are not automatically escaped; kernels, parities, DROP, affine collisions, laminar lifts, and signed splices must be exchange-unstable. **G14/G31/G38**: no finite-shell extrapolation. **G28**: new nonseparable objective, but its failed growth test remains mandatory. **G30**: no tensoring. **G32/G37**: no orthogonal copy addition; coupled exchanges must handle compatible parity. **G33/G34**: no exterior tags. **GD1/GD2**: no ordered-pair or group-ring multiplication.

**Experiment.** Search 12-selector NAND tiles with Gram entries in \(\{0,\dots,8\}\); certify exchange inequalities by exact LP and enumerate exchange-stable points.

**Falsification.** A signed parity state is itself exchange-stable below the required ratio.

---

### 2. Inverse Delaunay design by secondary-cone inequalities

**Mechanism.** Treat legal selector vectors as prescribed vertices of one empty ellipsoid and adverse transfers as points required outside a \(65/64\)-expanded ellipsoid. Solve directly for a rational positive-definite Gram matrix, center, and Delaunay secondary cone; exact Voronoi-relevant-vector inequalities provide the unrestricted outside-shell certificate.

**Expected move.** Produce a literal certificate for the roadmap lemma rather than discovering geometry by \(D_4/E_8\) labeling alone.

**Obstruction audit.** **G1**: positive definiteness charges every selector and auxiliary. **G2/G3**: Voronoi-relevant vectors certify all lattice points. **G5**: prescribe full port vectors. **G6**: center and glue rows are emitted. **G7, G9, G11, G12, G13, G15, G19** are not outside the model; include their exact port vectors as forbidden inequalities and search for additional relevant vectors. **G14/G31/G38**: certification is global, not a shell pass. **G28**: changes the tile geometry, while retaining its exact transfer test. **G30**: no tensor product. **G32/G37**: require depth-two inequalities against duplicated parity states. **G33/G34**: Gram feasibility is unrestricted, not the failed exterior family. **GD1/GD2**: no flow diagonalization or convolution.

**Experiment.** In dimensions \(8,10,12\), prescribe four NAND and two COPY legal vertices; alternate exact SDP rationalization with exhaustive Voronoi-vector generation.

**Falsification.** Equal-radius legality forces a false-port lattice point onto the same Delaunay shell.

---

### 3. Discriminant-group glue tile

**Mechanism.** Build the tile as an overlattice of \(D_4^r\) or \(A_2^r\). Ports are discriminant-group cosets, and legal NAND configurations are equal-norm glue codewords; adverse states must either have a nonzero dual syndrome or occupy a syndrome-zero coset with a provably larger coset minimum.

**Expected move.** Obtain transfer closure from finite discriminant arithmetic and unrestricted coercivity from exact coset theta minima, not bounded coefficient enumeration.

**Obstruction audit.** **G1**: every glue representative is norm-charged. **G2/G3**: canonical coset decomposition covers all integer coefficients. **G5**: glue the complete discriminant port. **G6**: parity checks are lattice coordinates, not filters. **G7/G13** are not escaped: exact-kernel affine collisions may be syndrome-zero and require coset-minimum auditing. **G9/G11/G12/G15/G19** likewise enter as explicit cosets. **G14/G31/G38**: theta/coset certificates replace finite passes. **G28**: uses a different transfer algebra, but must still beat its observed \(\lambda\le\mu\). **G30**: direct-sum gluing, not seed tensoring. **G32/G37**: duplicated parity may be a glue codeword and is a mandatory test. **G33/G34**: no exterior metric synthesis. **GD1**: no ordered-pair lift. **GD2**: finite abelian discriminant addition, not group-ring multiplication or virtual units.

**Experiment.** Enumerate self-orthogonal binary glue codes for \(D_4^4\), label six port cosets, and compute exact coset minima with Fincke–Pohst.

**Falsification.** G13 parity lands in the legal glue subgroup with equal or smaller norm.

---

### 4. Relative-cohomology frustration tile

**Mechanism.** Represent ports as boundary \(0\)-cochains of a small weighted \(2\)-complex and selectors as integral \(1\)-cochains. Legal gates are flat extensions of equal energy; a false output creates a nontrivial relative cohomology class whose shortest integral representative should have strictly greater Hodge energy.

**Expected move.** Prove the gap using an exact relative systole plus a lattice Hodge decomposition, yielding a uniform certificate over all integral cochains.

**Obstruction audit.** **G1**: harmonic, boundary, and carry coordinates are all charged. **G2/G3**: integral Hodge/SNF decomposition covers the full chain group. **G5**: the complete boundary cochain is the port. **G6**: cocycle and normalization rows are emitted. **G7, G9, G11, G13, G15, G19** are not escaped: exact signed cocycles are the central danger and must have trivial class or high norm. **G12**: a dropped face must create charged relative boundary. **G14/G31/G38**: use a systolic theorem, not shell inference. **G28**: changes the coercive invariant from min-plus bag cost to cohomology. **G30**: no tensor. **G32/G37**: compatible parity may cancel cohomology and must be tested at depth two. **G33/G34**: no exterior tags. **GD1/GD2**: no flow moments or group rings.

**Experiment.** Enumerate complexes with at most 8 vertices, 16 edges, and 10 faces; compute relative SNF and exact shortest representatives for all six gate boundaries.

**Falsification.** A false boundary is homologous to a legal one through a constant-norm signed cocycle.

---

### 5. Universal affine-midpoint refutation search

**Mechanism.** Attempt to disprove the frontier: derive an integer affine relation among equal-cost legal NAND/COPY states whose port is FALSE or malformed. Combine that relation with the parallelogram identity for every positive-definite quadratic form; a bounded relation could force an adverse transfer of cost at most legal growth independently of the chosen Voronoi geometry.

**Expected move.** Establish \(\lambda\le\mu\) for a broad class—such as affine selector tiles with linear complete ports—thereby forcing a roadmap amendment.

**Obstruction audit.** **G1/G6**: relations include every emitted slack, carry, and normalization coordinate. **G2/G3**: this is an unbounded algebraic attack, not enumeration. **G5**: equality is required on complete ports. **G7/G13** are the prototype exact-kernel/affine collisions; **G9/G11/G12/G15/G19** are included as candidate relations. **G14/G31/G38**: the conclusion would be symbolic, not extrapolated. **G28**: seeks to generalize its observed growth failure. **G30**: no tensor assumption. **G32/G37**: additive parity relations are explicit generators. **G33/G34**: quantifies over every positive-definite Gram, so exterior repair cannot help if the relation exists. **GD1/GD2**: diagonal flows and bicyclic units are additional generators, not assumptions.

**Experiment.** For all port codebooks of size at most 8 and selector supports at most 16, use MILP to find affine relations of \(\ell_1\)-norm at most 12, then symbolically optimize their worst-case quadratic ratio.

**Falsification.** Auxiliary coordinates make all false-port affine relations arbitrarily long or energy-unbounded.

---

### 6. Alternating two-species macrotile amendment

**Mechanism.** Replace the roadmap’s per-tile inequality by two tile species \(A,B\). Each may admit a cheap adverse state, but port renaming makes the cheap states incompatible; prove that the min-plus product \(T_BT_A\), rather than either factor, has adverse/legal ratio at least \((65/64)^2\).

**Expected move.** Amend only Lemma 2/3’s homogeneous edge: recurse in two-level macrotiles using an exact tropical potential and separate Voronoi certificates for \(A\) and \(B\).

**Obstruction audit.** **G1**: both species charge every coordinate. **G2/G3**: each outside-shell certificate is unrestricted. **G5**: complete ports pass between phases. **G6**: phase and glue coordinates are emitted. **G7, G9, G11, G12, G13, G15, G19** are not structurally excluded; their \(A\!\to\!B\) transitions must be listed in the complete operator. **G14/G31/G38**: growth follows from a certified product potential, not finite pass extrapolation. **G28**: explicitly outside its frozen homogeneous recursion, while preserving exact min-plus auditing. **G30**: composition, not Kronecker tensoring. **G32/G37**: compatible parity is the primary two-phase cycle to exclude. **G33/G34**: no exterior tags. **GD1/GD2**: no ordered-pair diagonal or group-ring product.

**Experiment.** Search pairs of \(D_4^2\) tiles with at most 20 port states; compute exact transfer matrices and solve rational tropical-potential inequalities for \(T_BT_A\).

**Falsification.** DROP or parity forms a low-cost period-two cycle.
