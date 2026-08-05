No external search was used.

### 1. Layered assignment-trellis lattice

**Core trick.** Order the variables and build a layered DAG whose state remembers assignments to clauses crossing the current cut. Arcs assign the next variable; states or arcs that close a falsified clause are omitted. Encode unit-flow equations, source demand, and binary arc anchors directly as weighted CVP coordinates.

**Expected move.** A satisfying assignment gives a short path. If every low-norm integral unit flow decomposes into a legal path, weighting conservation rows by \(M=n^K\) creates a polynomial gap.

**Obstruction audit.** G1: no slack variables. G2–3: uses no local affine-isolation claim. G5: consistency is global flow, not private rows. G6: all conditions are internal coordinates. G7: the radix zero-kernel is irrelevant, but signed flows may be an analogous exact kernel. G9/G11: parity selectors do not automatically satisfy trellis flow. G12: dropping a layer violates conservation. G13: this is an extended state encoding, not a compatible linear hash of the 72 selectors.

**Smallest experiment.** Build all variable orders for the nine-clause instance, emit the exact flow lattice, and enumerate vectors through Boolean radius plus 24.

**Falsification.** Find a short signed unit flow without a directed accepting path. More fundamentally, trellis width may be exponential.

---

### 2. Explicit bag-lift with globally meshed marginal consistency

**Core trick.** Introduce one-hot selectors for assignments to bags containing two or three overlapping clauses, not merely individual clauses. Couple every shared subbag marginal through a deterministic expander, so the encoding is a genuine nonlinear lift of raw clause selectors but all lift relations are emitted linearly inside the lattice.

**Expected move.** The Generation-11 parity may fail to extend to consistent bag selectors; any repair would then create many expander disagreements. Increasing bag size \(k\) could trade \(n^{O(k)}\) dimension for growing distance.

**Obstruction audit.** G1: no residual slack. G2–3: does not reuse their fixed-marginal certificate. G5: rows are not private; bags cross clause boundaries. G6: no external filtering. G7: raw zero-residual selectors need not lift. G9/G11: pair/cubic parity is the primary target. G12: a clause drop changes every incident bag marginal. G13: the lift is not linear in raw selectors and is fully specified internally; nevertheless new signed bag circuits remain possible.

**Smallest experiment.** For the fixed nine clauses, add selectors for every pair of intersecting clauses, impose all clause marginals, and run exact shell DP through squared radius 108.

**Falsification.** A lifted parity or clause-drop circuit of constant excess kills fixed bag size. General formulas may require \(k=\Omega(n)\).

---

### 3. Homological systole amplifier

**Core trick.** Interpret normalization and overlap equations as a boundary map \(\partial_1:C_1\to C_0\), with harmful signed selectors as short cycles. Enlarge the encoding by tuple-indexed cells and choose \(\partial_2:C_2\to C_1\) so honest differences are boundaries while every target-coset representative for an unsatisfiable formula has large Euclidean systole.

**Expected move.** A high-systole chain complex would replace fragile row-wise consistency by a global topological obstruction: local cancellation could not erase a nontrivial homology class.

**Obstruction audit.** G1: no slack. G2–3/G5: local affine certificates are replaced by global homology. G6: both boundary maps are emitted in the lattice. G7: exact residual kernels become cycles and are explicitly audited. G9/G11: parity cycles should be filled or made long. G12: clause deletion creates a boundary defect. G13: raw-chain linear attachments would inherit the affine collision; therefore the experiment must use enlarged tuple cells, outside that assumption.

**Smallest experiment.** Construct the raw chain complex for the nine-clause instance; enumerate support-\(\le6\) candidate 2-cells, compute Smith forms, and exactly measure the shortest vector in the obstruction and control cosets.

**Falsification.** Preserving all honest representatives may force the affine-collision cycle to remain short, or polynomial-size complexes may have small systole.

---

### 4. Adversarially trained rational Gram metric

**Core trick.** Treat the Gram matrix \(Q\), center, and clause-block tags as variables in a cutting-plane SDP. Iteratively enumerate the nearest harmful integer vector, add a constraint making it expensive while keeping all honest assignment vectors within radius \(R\), then rationalize \(Q\) and verify an exact factorization.

**Expected move.** Unlike fixed moment or Walsh metrics, the construction simultaneously learns against parity, clause drops, overlap circuits, and newly discovered mixtures. A uniform separator theorem for bounded-coefficient shells could yield a dimension-dependent gap.

**Obstruction audit.** G1: no slack. G2–3/G5: no local composition assumption. G6: the final rational Gram factor is an explicit CVP instance. G7: the known zero-residual selector is included as a cut. G9/G11: generalizes, rather than repeats, their fixed two-parameter metrics. G12: all clause drops are mandatory cuts. G13: an affine identity does not preserve squared distance under negative affine coefficients, so common-target hashing is not assumed.

**Smallest experiment.** Enumerate the entire \([-2,3]^{72}\) shell via DP, alternate exact attack separation with a symmetry-reduced SDP, then certify a rational \(Q\) and its true minimum.

**Falsification.** The honest vectors’ affine geometry may force some harmful vector inside every admissible ellipsoid; asymptotic description size may also explode.

---

### 5. Symmetric-tensor gap composition

**Core trick.** Homogenize a finite CVP gadget and replace each honest representative \(v\) by its symmetric tensor \(v^{\otimes k}\). Build the lattice from symmetrized tensor products of original columns, hoping unsatisfiable distance multiplies while completeness norm follows the corresponding tensor power.

**Expected move.** If minima compose, the Generation-9 squared ratio \(4/3\) becomes \((4/3)^k\); \(k=\Theta(\log n)\) would give a polynomial factor. Symmetry or sparse support must compress the nominal tensor dimension.

**Obstruction audit.** G1: no slack. G2–5: composition is tensorial, not overlap-by-private-rows. G6: all tensor columns are emitted. G7: exact base kernels may persist as mixed tensors. G9/G11: not outside their obstruction—the constant parity vector is a base input, so tensor amplification must actually defeat its localization. G12: clause drops likewise tensorize. G13: \(h\mapsto h^{\otimes k}\) breaks the raw affine identity, but unrestricted lattice combinations need not remain rank one.

**Smallest experiment.** Form the symmetric square of the fixed obstruction and control restricted to the exact low-energy state space; search all rank-one, rank-two, and sparse unrestricted tensor attacks.

**Falsification.** “Entangled” integer vectors beat the product bound, or polynomial-factor amplification requires quasipolynomial dimension.

---

### 6. Integer Nullstellensatz moment lattice

**Core trick.** Introduce coordinates \(y_S\) for squarefree monomials and emit linearized Boolean relations plus every degree-\(\le d\) monomial multiple of each clause’s falsity polynomial. Honest assignments give rank-one integral moment vectors; unsatisfiability should force a nonzero ideal residual unless a low-degree integral pseudo-moment survives.

**Expected move.** Integer anchoring might make low-degree pseudo-solutions much more expensive than real or rational proof-complexity relaxations. Weighted ideal residuals could then provide the amplifier.

**Obstruction audit.** G1: no free slack. G2–5: consistency is through the global clause ideal. G6: every moment and ideal equation is internal. G7: the three-term selector kernel need not satisfy ideal multiples. G9/G11: this adds clause-polynomial consequences, not merely equality of moments. G12: dropping a clause block violates its constant-monomial equation. G13: this is an explicit nonlinear lift with internal linearized relations, not an undefined feature map; however those relations may still admit pseudo-moments.

**Smallest experiment.** Use degree \(d=4\) on the nine-clause obstruction and control; emit the integer matrix, compute SNF, and exactly enumerate the anchored shell.

**Falsification.** A constant-norm integral pseudo-moment survives. Known hard formulas may require \(d=\Omega(n)\), making the construction exponential.

---

### 7. Discriminant-group lattice gluing

**Core trick.** Replace unrestricted one-hot selector coefficients by short representatives of cosets in a small lattice quotient \(L^\*/L\). Assign local truth labels to cosets and glue occurrence residues using a global linear code; a disagreement then occupies a nonzero coset whose minimum Euclidean norm can be amplified by code distance.

**Expected move.** Satisfying assignments select compatible short coset leaders. An unsatisfied clause should require either a long local representative or a positive-density nonzero glue syndrome, without auxiliary carries or residual slack.

**Obstruction audit.** G1: no slack directions. G2–3/G5: compatibility is quotient-lattice gluing, not private affine rows. G6: the glued lattice and target are explicit. G7: raw signed-selector kernels are not automatically lattice relations, though lattice closure may recreate them. G9/G11: parity combinations must pay coset minima. G12: a dropped block leaves a glue syndrome. G13: this changes the coefficient lattice and is not a common linear hash of raw selectors.

**Smallest experiment.** Enumerate quotients \((\mathbb Z/2)^r\), \(r\le4\), assignments of eight labels to cosets, and length-nine binary glue codes; construct each exact lattice and compare obstruction/control CVP minima.

**Falsification.** Additive closure may force the forbidden label or affine-collision combination to have a short representative; seven-near/one-far local geometry may be impossible.

Classical tool pointers: Schrijver, *Combinatorial Optimization* (2003), for network-flow integrality; Sherali–Adams, *SIAM J. Discrete Math.* 3 (1990), for lift-and-project hierarchies; Conway–Sloane, *Sphere Packings, Lattices and Groups*, 3rd ed. (1999), for lattice gluing and Construction-D-style ideas.
