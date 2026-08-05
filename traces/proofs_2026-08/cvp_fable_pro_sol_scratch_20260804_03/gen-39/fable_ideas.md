1. **Shell-canonical nonlinear graph code**

**Core trick.** Within the candidate shell, encode each coefficient \(z\) by a one-hot value register \(u_a\), \(a\in[-K,K]\), satisfying \(\sum u_a=1,\ \sum au_a=z\). If anchors force canonical registers, any lookup table \(h(z)\) becomes linear in \(u\); feed these values into an expander code with weight \(W=N^q\).

**Expected move.** Prove every NO-shell vector has nonzero coded residual, giving distance \(\Omega(W)\) versus YES radius \(O(\sqrt N)\).

**Obstruction audit.** G1 slack: absent. G2–3 fixed-fiber and G5 private overlap: unused. G6 filtering/mod-2: every equation is emitted and audited modulo small primes. G7 radix and G9/G11 parity: choose \(h\) to separate their kernels. G12/G38 DROP: not outside; weighted normalization must beat it. G13 affine-span: outside its *linear raw-selector* assumption. G14 pair bags, G15 hierarchy, G19 flow: unused. G28 min-plus/G30 tensor: no such composition. G31/G32/G37 additive metrics: distance comes after nonlinear lifting. G33/G34 exterior infeasibility: no exterior tags; one-hot states are equidistant.

**Experiment/falsifier.** Use \(K=3\), the 72-selector instance, and \(h(z)=(z^2,z^3\bmod 5)\); exhaust the shell. Kill on any noncanonical cheap register or zero-syndrome attack. Most likely death: signed \(u\)-registers recreate G13.

---

2. **Twisted-sheaf cosystolic gluing**

**Core trick.** Replace pairwise marginals by a bounded-degree 2-complex whose stalks are local satisfying assignments and whose restriction maps include formula-dependent permutations. Seek a complex with vanishing integral \(H^0\) for unsatisfiable instances and a cosystolic inequality: every normalized integer section is global or has \(\Omega(N)\) violated restrictions.

**Expected move.** Scale restriction rows by \(N^q\); absence of exact pseudosections then yields a polynomial Euclidean gap.

**Obstruction audit.** G1 slack and G7 radix: absent. G2–3 local isolation/G5 private overlap: replaced by global cohomology. G6 filters/mod-2: use emitted coboundary and augmentation rows; compute SNF over \(\mathbb Z\) and mod 2. G9/G11 parity and G13 affine lift: not automatically outside; they must be nontrivial cocycles. G12/G38 DROP: heavy augmentation addresses it, but must be proved. G14 pair bags/G15 hierarchy: not outside broadly; cosystolic expansion must supply their missing scaling theorem. G19 flow: higher-dimensional, though signed cocycles remain a danger. G28/G30: no tile or tensor. G31/G32/G37: no copy-additive metric. G33/G34: no sphere synthesis.

**Experiment/falsifier.** Build the smallest 2-complex over the nine-clause instance; compute rational/integral kernels and minimum residual for normalized chains. Kill on any G13 lift or residual-\(O(1)\) cocycle. Likely death: twisted \(H^0\) remains nonzero over \(\mathbb Q\).

---

3. **Arithmetic-height spherical fingerprints**

**Core trick.** Give every global assignment an equal-norm \(\{\pm1\}^m\) fingerprint, but scale carefully chosen character coordinates by distinct primes. Determinant/CRT bounds should force every nontrivial integral affine relation preserving all fingerprints to have coefficient height at least \(P=N^q\), converting affine pseudodistributions into large anchor cost.

**Expected move.** Retain exact equal completeness while pushing the smallest harmful affine combination beyond polynomial radius.

**Obstruction audit.** G1 slack: none. G2–3/G5 local overlap: fingerprints are formula-global. G6 filters/mod-2: characters and congruences must be explicit CVP coordinates. G7 exact radix kernel: tags depend on selector state, not residual order. G9/G11 parity: include characters detecting top parity. G12/G38 DROP: not outside; add a \(P\)-weighted global normalization character. G13 affine-span: the affine combination still exists, but its enlarged coordinates should have large height; thus only the zero-syndrome conclusion is avoided. G14/G15: no marginal hierarchy. G19: no flow. G28/G30: no frozen recursion/tensor. G31/G32/G37: global prime characters prevent copywise additivity. G33/G34: \(\pm1\) coordinates guarantee equal norm without bivectors or metric repair.

**Experiment/falsifier.** For all 16 assignments, greedily choose 20 characters and primes, then compute the shortest affine relation by exact lattice reduction/enumeration. Kill if the G13 coefficients remain short. Likely death: polynomially many locally realizable characters cannot achieve large height.

---

4. **Degree-one chains and systolic obstruction**

**Core trick.** Encode a witness as an integral degree-one cellular chain rather than a flow or marginal distribution. Clause violations remove designated cells; boundary and degree rows force every admissible signed chain to represent a fundamental class, while a systolic/intersection inequality should make that class cross many forbidden cells.

**Expected move.** Product complexes with systole \(N^{1/2+c}\) would give a polynomial distance ratio while honest fundamental chains retain mass \(O(N)\).

**Obstruction audit.** G1/G7 slack-radix: absent. G2–3/G5: no fixed local fibers or private rows. G6: boundary, degree, and forbidden-cell penalties are emitted; torsion is checked by SNF. G9/G11/G13: not outside—affine mixtures are signed degree-one chains, so the intersection theorem must charge them. G12/G38 DROP: degree augmentation excludes zero, provided its weight is scaled. G14/G15: topology replaces bag propagation. G19 signed flow: this is its higher-dimensional analogue, so signed splicing remains a direct risk. G28/G30: no min-plus or literal tensor. G31/G32/G37: no additive Gram composition. G33/G34: cell anchors give equal completeness without exterior tags.

**Experiment/falsifier.** Triangulate the three-variable cube, mark all eight forbidden assignment cells, and solve an ILP for the minimum degree-one signed chain. Kill on a two-negative splice. Likely death: any polynomial-size complex loses the required assignment intersection number.

---

5. **Synthesized tropical transfer gadget**

**Core trick.** Search for a finite boundary-state CVP gadget whose complete min-plus transfer matrix has legal cycle mean \(\mu\) and every adverse cycle mean \(\lambda>\mu\). Compose it by a replacement product with nonidentity seam permutations and state-dependent rebasing, producing ratio \((\lambda/\mu)^d\) at depth \(d\).

**Expected move.** A constant \(\lambda/\mu>1\) gives \(N^c\) after logarithmic depth.

**Obstruction audit.** G1/G7: no slack or radix. G2–3/G5: all freed-port states are included. G6: transfer entries come from unrestricted emitted CVP shells. G9/G11/G13 parity, G12/G38 DROP, and G19 signed splice: each must be an explicit adverse state, not filtered out. G14/G15: no claim from finite bags alone. G28 min-plus failure: directly relevant, but this escapes only its frozen tile, identity glue, and \(\lambda\le\mu\) table—not the broader warning. G30 isometry: no Kronecker tensor; reject any seed automorphism. G31/G32/G37: recurrence is tropical rather than additive quadratic coupling. G33/G34: no exterior completeness issue.

**Experiment/falsifier.** Enumerate rank-\(\le12\) gadgets with two-bit ports, exact shells, and all named attacks; use CP-SAT to select rows/weights, then compute minimum cycle means and depth-two tables. Kill if DROP yields \(\lambda\le\mu\). Most likely death: a universal zero/malformed cycle forbids strict separation.

---

6. **Noncommutative holonomy locks**

**Core trick.** Label incidence edges by elements of a small nonabelian group and require clause-variable loops to have prescribed holonomy. Emit multiplication-table selectors plus both left- and right-regular representation checks; signed conservation alone no longer certifies a valid product.

**Expected move.** An unsatisfiable formula creates many inconsistent loop products, amplified by an expander family of cycles and weight \(N^q\).

**Obstruction audit.** G1/G7: no slack or radix. G2–3/G5: consistency is loop-global, not private-marginal. G6: all multiplication and normalization rows are emitted and checked over characteristic divisors of \(|G|\). G9/G11 parity: noncommutative products can detect commutative moment kernels. G12/G38 DROP: weighted table normalization must defeat zero. G13 affine-span: outside raw linear hashing, but affine combinations of full group-table witnesses still exist and require audit. G14 pair bags: multiplication tables resemble bags, yet expander holonomy is new; scaling remains unproved. G15 hierarchy: no laminar lift. G19 flow: not outside signed group-algebra cycles. G28/G30: no tile/tensor. G31/G32/G37: loop products couple copies nonadditively. G33/G34: regular-representation one-hots are equal-radius.

**Experiment/falsifier.** Use \(S_3\), three generators, and the nine-clause instance; enumerate shell states with exact multiplication rows. Kill on an augmentation-ideal cycle with zero holonomy residual. Likely death: signed group-algebra identities splice just as cheaply as G19 flows.

---

7. **Delaunay assignment polytope**

**Core trick.** Construct a polynomial-dimensional lattice having exponentially many equal-radius Delaunay vertices indexed by assignments; clause satisfaction selects faces or cosets. Delaunay emptiness makes every other lattice point farther from the common center, while lattice joins or code-lattice lifts are intended to amplify the radial margin.

**Expected move.** Obtain a family where legal radius grows as \(N^{1/2}\) but the nearest point outside the satisfying-face union grows as \(N^{1/2+c}\).

**Obstruction audit.** G1 slack/G7 radix: absent. G2–3/G5: assignment geometry is global. G6: the lattice, center, and clause cosets must be rational and fully emitted. G9/G11 parity: becomes another lattice point whose radial cost is measured directly. G12/G38 DROP: not outside; omission faces must not contain a near central point. G13 affine-span: affine combinations remain lattice points, but Delaunay geometry—not a compatible syndrome—must make them far. G14/G15/G19: no bags, hierarchy, or flow. G28: no min-plus tile. G30: avoid literal tensor seeds and test automorphisms. G31/G32/G37: amplification comes from Delaunay joins, not orthogonal copy energy. G33/G34: common sphere is guaranteed by construction, not exterior tags.

**Experiment/falsifier.** Build a small Construction-A lattice for the eight three-bit assignments, impose all eight clauses, and enumerate exact nearest vectors and affine attacks. Kill if parity or DROP lies on the first two shells. Likely death: clause-face enforcement reintroduces short signed mixtures or only a constant radial margin.
