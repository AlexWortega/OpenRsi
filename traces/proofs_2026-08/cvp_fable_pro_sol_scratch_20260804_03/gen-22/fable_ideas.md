## Generation 22 — divergent mechanisms

### 1. Iterated sketched pair-bag lift
**Mechanism.** Extend G14 by repeatedly lifting bag states to quadratic joint states, then compressing each outer-product layer with an explicit integral TensorSketch/sign matrix. After \(d=\lceil\log\log n\rceil\) rounds, an affine mixture should retain zero residual but acquire multiplicatively growing anchor energy, while honest rank-one lifts retain controlled norm.

**Expected move.** Prove a restricted-isometry lemma for all integral mixtures of \(\ell_1\)-mass at most \(n^\alpha\), yielding excess \(B\,n^{2c}\).

**Obstruction audit.** G1: no slack. G2/3/5: global lift, not private fixed-marginal isolation. G6: emit every selector, row, target, and unrestricted bound. G7: exact kernels are charged by lifted norm, not residual. G9/11: effective degree grows, rather than stopping at cubic. G12: a dropped bag is replicated upward. G13/G15: **not excluded**—their affine lift remains zero-residual; norm growth is the entire conjecture. G14: this explicitly seeks its missing scaling law. G19: no flow. G20/21: require polynomial sketch width and compare excess to baseline.

**Falsification / likely death.** Kill if the G13 coefficients maintain \(O(B)\) energy; likely death is sketch collision or superpolynomial joint-selector tables.

**Experiment.** Add one 64-coordinate signed quadratic sketch to G14 and exactly optimize the nine-clause obstruction/control through \(B+128\).

---

### 2. Multistage Lawrence–Graver rigidity
**Mechanism.** Embed clause consistency into an \(r\)-stage Lawrence lifting whose integer kernel has deliberately large Graver moves in selected coordinates. With \(r=\Theta(\log n)\) and constant branching, the matrix remains polynomial-size while a harmful exact-fiber correction could require norm \(2^{\Omega(r)}\).

**Expected move.** Reduce every unsatisfiable zero-residual selector to a conformal Graver move, then lower-bound its norm relative to the honest baseline.

**Obstruction audit.** G1: no slack. G2/3/5: global multistage coupling replaces private local rows. G6: the affine matrix itself is the emitted CVP instance. G7: zero residual is allowed but should require a long move. G9/11: no bounded moments. G12: drops are kernel corrections and must also be long. G13/G15: **still applicable**; affine combinations lie in the fiber, so the lifting must enlarge rather than eliminate them. G14: unrelated to fixed pair bags. G19: no path conservation. G20/21: the required lemma is explicitly \(\|g\|^2/B\ge n^{2c}\) with polynomial matrix size.

**Falsification / likely death.** Kill upon any bounded-support circuit at depth two; benign differences between honest encodings probably generate such circuits.

**Experiment.** Apply two and three Lawrence stages to the G14 incidence matrix; use exact MILP/Graver enumeration to minimize the G11 harmful fiber and all single-bag drops.

---

### 3. Cosystolic homological-product amplifier
**Mechanism.** Interpret the initial CVP defect as a coset in an integral chain complex and tensor that complex with an explicit bounded-degree complex having growing cosystole. A nontrivial defect class should then require large chain norm, without copying clause anchors proportionally.

**Expected move.** First prove the nine-clause defect is nonzero in Smith homology; then establish a product lower bound \(\operatorname{dist}(t,\operatorname{im}\partial)\ge n^cR\).

**Obstruction audit.** G1: no slack. G2/3/5: global quotient metric, not local overlap composition. G6: boundaries, basis, target, and unrestricted coset search are explicit. G7: **not outside it** if the signed selector is already a boundary. G9/11: no moments. G12: a drop has nonzero boundary unless supported by a small filling. G13/G15: **decisive and unresolved**—affine pseudosections may make the class trivial before amplification. G14: not a pair-bag argument. G19: no accepting flow, though signed chains are analogous. G20/21: product size and cosystole-to-baseline ratio must be polynomially quantified.

**Falsification / likely death.** Immediate kill if the G7 or G13 attack represents the zero class; this is the most likely outcome.

**Experiment.** Build the integer mapping complex for the nine-clause instance, compute Smith normal form, then take one product with a small explicit 2-complex and enumerate the target-coset systole.

---

### 4. Splitter-selected cyclic-polytope bags
**Mechanism.** Choose polynomially many \(k=\lceil\log n\rceil\)-variable bags using an explicit splitter family, and encode each bag assignment by an integral moment-curve vertex \((1,t,\ldots,t^{2s})\), \(s=\Theta(\log n)\). Neighborliness and Vandermonde conditioning should make every low-support signed pseudodistribution expensive on a bag that separates its underlying assignments.

**Expected move.** Prove that every harmful mixture of support at most \(n^\alpha\) is separated on many bags, giving polynomial aggregate energy.

**Obstruction audit.** G1: no slack. G2/3/5: high-overlap splitter bags, not private clauses. G6: all bag columns and targets are emitted. G7: exact marginal kernels may remain, but fingerprints should charge them. G9/11: degree grows logarithmically with only polynomially many selected bags. G12: each clause occurs in many normalized bags. G13/G15: **not formally escaped**; their affine mixture threads all linear rows, so coefficient energy must supply the gap. G14: logarithmic bags replace pairs. G19: no flow. G20/21: \(2^k=\operatorname{poly}(n)\), but the baseline ratio still needs proof.

**Falsification / likely death.** Kill if the 13-term G13 mixture has only constant relative excess; that is the likely failure.

**Experiment.** On the four-variable obstruction, use all four-variable bags with moment-curve degree 8 and exactly compare G13, drops, and the unrestricted optimum against a satisfiable control.

---

### 5. Frozen two-representation magnetic holonomy
**Mechanism.** Augment the G19 branching program with transported fibers in both the integral four-dimensional standard representation of \(A_5\) and its exterior square. Every edge uses a specified permutation matrix; source and sink fibers fix the required total holonomy, while edge selectors must transport both representations simultaneously.

**Expected move.** Show that the known signed splice cannot realize both twisted boundaries with anchor excess \(O(1)\).

**Obstruction audit.** G1: no slack. G2/3/5: global ordered transport. G6: matrices, fibers, rows, target, and control are frozen. G7: exact signed kernels remain the test. G9/11: no moments. G12: dropping a layer breaks two transported fibers. G13/G15: affine combinations sharing both boundaries still survive, so this is only outside their assumptions if accepting traces differ in a representation-sensitive invariant. G14: no bags. G19: this is a genuine mutation, but remains within its signed-splicing danger. G20/21: dimension is linear in program length; test relative, not absolute, excess.

**Falsification / likely death.** Any zero-residual splice through baseline \(+16\) kills it. Most likely all complete accepting traces have the same boundaries, so affine splicing persists automatically.

**Experiment.** Add the two fibers to the existing G19 instance and rerun its shell DP/MILP through anchor excess 16.

---

### 6. Sparse Plücker-secant penalties
**Mechanism.** For every selected four-clause rectangle, attach joint-selector columns carrying exterior-square/Plücker coordinates of its two clause-pair marginals. Honest restrictions are decomposable points of a Grassmannian; mixtures of incompatible assignments should leave its low secant varieties and acquire large antisymmetric energy.

**Expected move.** Establish that any zero-residual harmful selector of coefficient mass \(K\) creates \(\Omega(K^2)\) nonzero Plücker coordinates across an expander family of rectangles.

**Obstruction audit.** G1: no slack. G2/3/5: cross-clause rectangles rather than private marginals. G6: tags are fixed column coordinates, not external determinant tests. G7: its signed kernel should have nonzero wedge energy. G9/11: these are cross-clause antisymmetric features, not singleton/cubic moments. G12: normalized rectangle tags replicate drops. G13/G15: **not excluded**—an affine combination of fully lifted honest encodings remains legal; the proposal relies on its tag norm growing. G14: uses four-clause secants beyond pair bags. G19: no flow. G20/21: \(O(m^4)\) constant-alphabet rectangles are polynomial, but baseline domination is unproved.

**Falsification / likely death.** Kill if the explicit G13 combination lies in the same low secant with \(O(B)\) norm; localization may preserve it exactly.

**Experiment.** Add all four-clause Plücker tags to the nine-clause instance and optimize the known G7/G11/G13 attacks before attempting unrestricted shell search.

---

### 7. Valuated-matroid exchange curvature
**Mechanism.** Pass through an exact-cover/three-matroid encoding in which honest assignments are common bases, then realize base exchanges as lattice generators. Assign explicit expander-derived valuations so a locally feasible but globally non-base integer point must cross many expensive exchange circuits; squared Euclidean distance supplies the separable convex energy.

**Expected move.** Prove an exchange-curvature theorem: absence of a common base forces valuation excess \(B\,n^{2c}\), even for unrestricted signed integer combinations.

**Obstruction audit.** G1: no slack. G2/3/5: global base exchange, not local affine isolation. G6: ground set, exchange generators, valuation coordinates, and target are all emitted. G7: zero-residual signed points remain possible but should incur exchange energy. G9/11: no moments. G12: deletion violates many valued rank layers. G13/G15: **not outside them** unless discrete convexity charges affine base mixtures; this must be tested directly. G14: no fixed pair-bag claim. G19: no flow. G20/21: valuation excess must beat the full common-base baseline, and all weights need polynomial bit length.

**Falsification / likely death.** A single cheap alternating exchange cycle kills the mechanism; likely only constant excess follows from one missing exact-cover element.

**Experiment.** Convert the all-eight-clauses core to exact cover, construct its exchange lattice, and exactly minimize the valued quadratic objective over signed coefficients versus all \(0/1\) bases.

**Classical touchstones:** Graver (1975) on integer test sets; Gale’s cyclic-polytope construction; Tillich–Zémor (2009) on homological products; Pham–Pagh (2013) on TensorSketch; Dress–Wenzel (1992) on valuated matroids.
