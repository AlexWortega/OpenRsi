## Generation 38 obstruction legend

- **O1:** G1 RS slack annihilation; G7 exact zero-residual radix kernel.  
- **O2:** G2–3 isolation requires fixed marginals; G5 overlap creates short kernel moves.  
- **O3:** G6 used external filters/reference changes rather than emitted CVP coordinates.  
- **O4:** G9/G11 low-degree parity; G13 honest-affine-span collision; G15 affine lift through a hierarchy.  
- **O5:** G12 clause drop; G14 pair bags pass only a finite shell, with no scaling law.  
- **O6:** G19 signed accepting-flow splicing.  
- **O7:** G28 unfavorable min-plus growth; G30 seed isometry and unrestricted tensor entanglement.  
- **O8:** G31 only finite separation; G32 additive parity; G37 universal additive metric cut.  
- **O9:** G33 noncospherical exterior tags; G34 no positive-definite metric repair.

### 1. Cyclotomic unit-rigidity blocks

**Core trick.** For each eight-label selector \(z\), add the full Minkowski embedding of \(a(z)=\sum_{t=0}^7z_t\zeta_{11}^t\). Honest labels are roots of unity of equal norm; Kronecker’s theorem plus \(\operatorname{Tr}(a\bar a)\ge [K:\mathbb Q]\) suggests that a normalized non-one-hot block must pay strictly more unless it represents another root of unity.

**Expected move:** Replace “detect a residual” by an intrinsic integer-energy separation of signed selectors.

**Audit:** O1 outside: zero residual cannot erase the embedding. O2 not outside—overlap may align minimum-energy units. O3 all embeddings are emitted. O4 outside raw common-syndrome assumptions because honest tags differ but have equal norm. O5 drops need an emitted normalization weight exceeding saved trace; G14 scaling remains open. O6–O7 use neither flows nor tensor/min-plus composition. O8 not outside if copies are merely added. O9 outside: the canonical embedding is automatically Euclidean and cospherical.

**Smallest experiment:** On the nine-clause instance with \(q=11\), enumerate normalized \(z\in[-3,3]^8\), classify minimum-trace units, then rerun the G31 shell with cyclotomic Gram blocks.

**Likely death:** Unexpected normalized cyclotomic units reproduce parity at honest energy.

---

### 2. Fully checked Reed–Solomon computation tableau

**Core trick.** Encode every layer of a deterministic formula-evaluation circuit as an entire Reed–Solomon codeword, not sampled PCP queries. Realize multiplication gates with joint symbol selectors and the star-product containment \(RS_k\star RS_k\subseteq RS_{2k-1}\), then re-encode after each depth block.

**Expected move:** Any incorrect gate tableau should violate a linear fraction of emitted coordinates; repeated re-encoding could turn one false output into growing Euclidean cost.

**Audit:** O1 outside: no free clause slack or residual-only radix map. O2 outside private-row assumptions because each codeword globally couples a layer. O3 every coordinate and gate relation is emitted. O4 outside the raw 72-selector hash, but not outside general affine pseudocodewords. O5 a dropped layer violates codeword normalization in many coordinates; scaling still unproved. O6 no path-flow conservation. O7 no literal tensor or frozen min-plus rule. O8 re-encoding couples levels rather than summing independent copies. O9 no exterior/common-sphere synthesis.

**Smallest experiment:** Over \(\mathbb F_{17}\), use an \([8,3]\) RS code for a tiny contradictory circuit, emit joint gate selectors, and enumerate coefficients in \([-2,2]\).

**Falsification:** A zero-residual signed tableau accepting the contradiction.

**Likely death:** Star-product selectors admit a low-weight affine pseudocodeword.

---

### 3. Integral cosystolic-expansion encoding

**Core trick.** Place variable choices on a cochain complex and represent clause inconsistency by a twisted coboundary. Use a small explicit high-dimensional expander so an integral cochain is either close to a genuine assignment coboundary or has a large coboundary/cosystolic norm.

**Expected move:** Reinterpret signed parity and overlap cheats as small integral cocycles, then exclude them by a global expansion inequality rather than local gadget isolation.

**Audit:** O1 outside: cost is a boundary norm, not amplified slack residual. O2 outside if the proved expansion is global; otherwise short overlap-supported cocycles kill it. O3 all boundary matrices are emitted. O4 parity/affine lifts are exactly the cocycles being tested, so not assumed away. O5 deleting a cell exposes all incident boundaries; polynomial expansion remains open. O6 G19 is one-dimensional scalar flow, whereas this uses higher-dimensional twisted boundaries. O7 no tensor or min-plus recurrence. O8 one expanding complex replaces additive copies. O9 no exterior tag or fitted common sphere.

**Smallest experiment:** Build the complete two-complex on six vertices, attach a two-clause contradiction, and use Smith normal form plus MILP to find the shortest nonassignment integral cocycle.

**Falsification:** A norm-\(O(1)\) cocycle supported near one clause.

**Likely death:** Expansion over fields fails over unrestricted integers because of torsion or boundaries.

---

### 4. Nonabelian holonomy against signed flow splicing

**Core trick.** Mutate the G19 branching program by assigning each transition a noncommuting matrix and enforcing representation-valued transport in addition to scalar conservation. Honest paths have a prescribed endpoint holonomy, while a signed splice that conserves scalar flow should generally fail at least one twisted conservation equation.

**Expected move:** Obtain a “twisted spectral gap” for accepting signed flows using several small finite-group representations.

**Audit:** O1 outside: no slack/radix amplification. O2 global ordered transport replaces private marginal rows. O3 every matrix-coordinate equation is emitted. O4 outside raw selector moments, though affine combinations lying in every twisted kernel remain possible. O5 path deletion violates multiple twisted rows; no asymptotic bound yet. O6 directly outside G19’s scalar-flow assumptions. O7 no tensor or min-plus composition. O8 ordered noncommutative products are not additive copy features. O9 no exterior sphere or Gram repair.

**Smallest experiment:** Construct a width-3, four-layer contradictory program; label edges by the two-dimensional irreducible representation of \(S_3\); enumerate all accepting vectors with \(\ell_1\le6\), comparing scalar and twisted kernels.

**Falsification:** The G19-style two-negative accepting flow survives every chosen representation.

**Likely death:** Twisted conservation is still linear and admits representation-invisible signed cycles.

---

### 5. Splitter-indexed logarithmic bags

**Core trick.** Replace complete pair bags by joint selectors on \(O(\log n)\)-sized clause sets chosen from an explicit perfect-hash/splitter family. Arrange that every deviation supported on at most \(s\) clauses is isolated by some bag; deviations with support \(>s\) must already pay large anchor excess.

**Expected move:** Prove a sparse/dense dichotomy: splitter bags kill all low-support parity and drop attacks, while dense attacks are expensive without residual amplification.

**Audit:** O1 exact kernels must extend through every bag, so radix is irrelevant. O2 outside private pair overlap because bags cross arbitrary small supports. O3 all bag coordinates are emitted. O4 not outside: the G13/G15 global affine pseudodistribution may lift through every bag and is the primary falsifier. O5 outside G14’s fixed-pair assumption; a scaling theorem is still absent. O6 no flow. O7 no frozen seam or literal tensor. O8 splitter recursion may still permit additive compatible attacks, so not outside. O9 no exterior metric.

**Smallest experiment:** For nine clauses, generate a minimal family separating every support of size at most four, emit 3/4-clause bags, and solve the zero-residual ILP plus shell \(B+64\).

**Falsification:** The known 16-assignment affine coefficients lift exactly.

**Likely death:** Logarithmic bags either become superpolynomial or inherit the hierarchy affine lift.

---

### 6. Delaunay empty-sphere gadget gluing

**Core trick.** Realize legal local labels as vertices of an integral Delaunay polytope around a common empty sphere, then glue gadgets by lattice fiber products along shared faces. Instead of penalizing violated equations, soundness would follow because inconsistent or signed combinations are not vertices and lie outside the glued empty sphere.

**Expected move:** Seek a geometric composition rule where NO empty-sphere radius grows faster than the honest covering radius.

**Audit:** O1 outside: there is no residual block to annihilate. O2 not outside—fiber-product gluing may introduce short overlap lattice points. O3 the lattice and center are explicit. O4 affine parity matters only if it becomes an interior lattice point, which enumeration tests. O5 the origin/drop may enter the sphere; this is an immediate gate. O6 no flow. O7 outside the tested min-plus and Kronecker rules, though gluing could exhibit analogous bad growth. O8 shared centers can create nonadditive cross terms. O9 outside: Delaunay construction supplies common spheres and positive-definite metrics by definition.

**Smallest experiment:** Use \(A_2\) simplex gadgets for a two-variable contradiction, glue two copies along one face, and enumerate all lattice points through the honest radius.

**Falsification:** Any signed or dropped interior point.

**Likely death:** Empty-sphere radii add quadratically, giving no polynomial ratio.

---

### 7. Division-algebra norm composition

**Core trick.** Encode local error symbols in an integral quaternion order and compose levels by quaternion multiplication. Honest symbols are norm-one units, while a nonzero defect cannot disappear because the quaternion algebra has no zero divisors and its norm is multiplicative.

**Expected move:** Replace unrestricted tensor rank with a fixed-dimensional multiplicative invariant, potentially giving \(N(e_1e_2)=N(e_1)N(e_2)\) without Kronecker entanglement.

**Audit:** O1 not outside: linearizing multiplication with joint selectors may introduce an exact slack kernel. O2 multiplication is global across composed blocks, not private marginal overlap. O3 all product-table selectors must be emitted. O4 not outside—affine pseudoproducts are the central danger. O5 normalization can charge drops; scaling is unproved. O6 no accepting flow. O7 outside G30’s literal tensor and seed isometry if an asymmetric seed is used; unrestricted joint selectors remain analogous entanglement. O8 multiplicative norm is not an additive Gram orbit. O9 no exterior tags/common-sphere SDP.

**Smallest experiment:** Use Lipschitz quaternions \(\{1,i,j,k\}\), two four-symbol factors, and a full multiplication-table selector; enumerate coefficients in \([-2,2]\) and compare one- versus two-level NO/YES ratios.

**Falsification:** A zero-residual pseudoproduct with norm below the product of factor minima.

**Likely death:** Bilinear linearization restores exactly the signed mixtures division was meant to prevent.

Classical ingredients invoked here are Kronecker’s theorem on algebraic integers on the unit circle, Reed–Solomon codes (Reed–Solomon, 1960), Kazhdan/Garland-style spectral expansion, perfect-hash splitters (Naor–Schulman–Srinivasan, 1995), Delaunay empty-sphere theory, and Hurwitz quaternion norm composition.
