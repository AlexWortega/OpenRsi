I use the following consolidated obstruction map: **K1** zero-residual slack/radix kernels (G1/G7); **K2** local isolation collapsing under overlap (G2–G5); **K3** external filters or changed references (G6); **K4** constant-cost low-degree parity (G9/G11); **K5** DROP (G12); **K6** honest-affine-span collision/hierarchy lift (G13/G15); **K7** signed splicing (G19); **K8** adverse growth no better than legal growth/additivity (G28/G32); **K9** unrestricted tensor entanglement/isometry (G30); **K10** common-sphere/positive-metric failure (G33/G34); **K11** finite shell without a scaling law (G14/G31).

### 1. Higher-Lawrence Graver amplifier

**Mechanism.** Apply asymmetric higher-Lawrence liftings to a complete overlap gadget, aiming to make every harmful zero-residual affine correction require a Graver element whose negative support grows faster than the honest diagonal radius. Unlike binary-code arguments, measure the exact integer Graver norm, including carries and doubled coordinates.

**Expected move.** Find a base matrix with depth-two adverse/legal growth ratio \(>1\), then prove the lifting recurrence.

**Checks.** K1: zero residual is allowed; cost must come from coefficient norm. K2: tested on composed overlaps, not isolated clauses. K3: emit \([2I;5A]\) and target. K4/K6: parity lifts remain feasible unless their norm grows—central test. K5: include zeroed bricks. K7: Graver enumeration includes negative coefficients. K8: exact adverse/legal comparison. K9: no tensor rank assumption. K10: honest diagonal copies have directly computable equal anchor radius. K11: unresolved until a recurrence is proved.

**Falsifier.** A bounded-norm lifted G13/G19 vector, or growth \(\lambda\le\mu\).

**Experiment.** Higher-Lawrence-lift one G5 two-clause overlap to depths 1–3; compute exact Graver bases and unrestricted CVP minima with 4ti2/Sage.

---

### 2. Native Delaunay-hole clause gates

**Mechanism.** Represent the eight local labels as lattice points around a genuine Delaunay hole, then make each clause target a nearby hole exposing precisely its seven satisfying vertices. Legality is supplied by Voronoi geometry rather than a linear syndrome; shared variables are glued through common face coordinates.

**Expected move.** Obtain a local “signed-combination tax” that survives two-gate gluing because nonvertex lattice points leave the empty ellipsoid.

**Checks.** K1: locally outside—no slack or amplified residual—but glue kernels remain possible. K2: not outside; two-gate composition must be searched. K3: use an explicit integral Gram, basis, and target. K4/K6: affine combinations need not stay on the Delaunay sphere, but could still be short. K5: test deleting an entire cell. K7: enumerate all signed lattice coefficients. K8: no growth theorem yet. K9: no tensoring. K10: Delaunay equations certify cosphericity and positive definiteness exactly. K11: remains fatal without a compositional empty-ellipsoid lemma.

**Falsifier.** Any G13-style point, DROP, or signed splice within the honest radius after two gates are glued.

**Experiment.** Enumerate positive-definite integral Gram matrices in dimensions 4–8 and rational centers; test the all-eight-clause three-variable core by exact Fincke–Pohst enumeration.

---

### 3. Hyperbolic monodromy on consistency fibers

**Mechanism.** Attach a small integer fiber to every occurrence and transport it along the occurrence graph using matrices such as \(H=\begin{pmatrix}2&1\\1&1\end{pmatrix}\). Honest assignments occupy a fixed zero-fiber, while a clause defect transported around incompatible cycles should be expanded by products of \(H\) and \(H^{-1}\).

**Expected move.** Replace additive copy growth by multiplicative holonomy: repairing one injected defect requires coefficients exponential in cycle depth.

**Checks.** K1: no slack, but a zero injected defect defeats the mechanism. K2: uses global cycles rather than private rows; still unproved. K3: all transport equations and anchors are emitted. K4/K6: if parity has zero twisted defect, it survives exactly—mandatory audit. K5: dropping a node creates boundary defects to enumerate. K7: signed fiber solutions are unrestricted. K8: hyperbolicity targets strict adverse growth directly. K9: no tensor/rank premise. K10: honest fibers are zero, so completeness radius is unchanged and exact. K11: requires a polynomial-size graph family and a holonomy lower bound.

**Falsifier.** A zero-fiber affine lift or a short stable-eigendirection repair.

**Experiment.** Add two-dimensional fibers to the nine-clause obstruction, enumerate edge labels from \(\{H^{\pm1},I\}\), and exactly compare obstruction/control minima through two graph lifts.

---

### 4. Discriminant-form lattice gluing

**Mechanism.** Use a lattice with discriminant group \(D=L^\*/L\) and quadratic form \(q\), assigning honest labels to equal-minimum glue classes. Couple clauses through an isotropic glue code so a harmful selector should land in an anisotropic class whose exact Euclidean coset minimum is large—not merely have nonzero Hamming syndrome.

**Expected move.** Convert algebraic incompatibility into a provable lower bound from discriminant-form minima.

**Checks.** K1: no residual amplifier. K2: glue is global, but short overlap classes may persist. K3: emit the glued lattice basis and shifted target. K4/K6: if G13 occupies an honest discriminant class, the mechanism dies immediately. K5: compute the class of every dropped bag. K7: coset minima quantify all signed representatives. K8: test glue concatenation rather than assume it. K9: no rank-one structure. K10: honest class minima and centers require exact theta-shell certification. K11: a finite glue pass gives no asymptotic gap without a minimum-growth theorem.

**Falsifier.** G13, DROP, or parity sharing a class with a short honest leader; or anisotropic minima growing only additively.

**Experiment.** Enumerate self-orthogonal ternary glue codes for \(A_2^k\), \(k\le4\); map the nine-clause attacks into \(D\), construct exact bases, and enumerate each relevant coset minimum.

---

### 5. Noncommutative group-algebra fingerprint

**Mechanism.** Encode labels by matrices from a finite nonabelian group and score their centered Fourier components across all nontrivial irreducible representations. Honest products have equal Plancherel norm, while contradictions are intended to occupy nontrivial conjugacy components whose energy is amplified in quasirandom groups.

**Expected move.** Detect signed pseudodistributions invisible to abelian moments by noncommuting word order.

**Checks.** K1: an exact identity-word attack still vanishes. K2: global ordered products may see overlap, but multiplication-table splicing is possible. K3: multiplication must be realized by explicit lattice columns, never externally checked. K4/K6: affine group-algebra combinations may still spoof every representation—directly test. K5: include the zero word and missing-factor states. K7: unrestricted signed group-algebra coefficients are searched. K8: minimum irrep dimension suggests growth but proves none. K9: no tensor rank assumption. K10: unitary blocks give equal local norm; the full global center still needs exact certification. K11: polynomial compilation and scaling remain open.

**Falsifier.** A signed multiplication-table flow evaluating to the accepting group element at constant excess.

**Experiment.** Use \(A_5\)’s exact integer permutation representations on the three-variable all-clauses core; emit meet-in-the-middle multiplication triples and exhaust the first signed shell.

---

### 6. Adversarial two-level Voronoi metric synthesis

**Mechanism.** Optimize the Gram matrix itself by column generation: alternate an SDP choosing a rational, incidence-equivariant positive-definite \(Q\) with an exact CVP oracle returning the cheapest unrestricted attack. Optimize a two-level objective—adverse growth divided by legal growth—rather than merely one-copy separation.

**Expected move.** Either discover cross-terms unlike fixed Walsh/exterior families, or certify that the chosen feature space cannot beat additivity.

**Checks.** K1: zero kernels are oracle attacks. K2: train directly on overlapping instances. K3: rationalize \(Q=C^\top C\), emit \(C,t\), and certify the shell. K4: include every parity placement. K5: include all bag/clause drops. K6: seed G13/G15 explicitly. K7: oracle coefficients range over all integers. K8: strict two-level growth is the optimization target. K9: two-copy oracle uses unrestricted coefficient matrices. K10: common-radius linear equations and \(Q\succ0\) are hard constraints. K11: even an optimum \(>1\) needs a symbolic recurrence; otherwise it remains finite evidence.

**Falsifier.** SDP optimum \(\lambda/\mu\le1\), failed rational factorization, or a new exact shell attack.

**Experiment.** Start from G31’s rank-72 space, permit all incidence-orbit Gram entries, and alternate exact one-/two-copy DP with rational SDP cuts.

---

### 7. Affine-lift closure theorem and automatic counterexample extractor

**Mechanism.** Formalize the broad class of gadgets obtained from complete encodings by linear local features, marginal maps, hierarchies, flows, or linearized products. Use Smith normal form and quadratic pullback to turn any bounded-coefficient affine pseudodistribution into a universal upper bound on the emitted CVP gap.

**Expected move.** Either eliminate a large family of doomed PCP-free constructions or identify the exact structural hypothesis a successful nonlinear lattice gadget must violate.

**Checks.** K1: detects exact residual kernels. K2: computes the composed overlap module. K3: accepts only emitted bases and fixed targets. K4: searches finite-difference/parity generators. K5: includes coordinate-deletion vectors. K6: explicitly computes the complete-encoding affine image. K7: works over \(\mathbb Z\), not nonnegative flows. K8: derives copy-composition upper bounds. K9: analyzes the full tensor coefficient module. K10: first checks exact cosphericity and positive definiteness. K11: reports finite bounds separately from genuine recurrences. Thus it evades none of K1–K11; it converts them into a reusable theorem.

**Falsifier.** An emitted linear-lift gadget whose predicted affine witness exists algebraically but whose exact CVP distance exceeds the bound.

**Experiment.** Build a verifier ingesting G7, G15, G19, and G32 matrices and automatically reconstructing their known witnesses and distance upper bounds.

Classical starting points only: J. E. Graver, *Math. Programming* 9 (1975), 207–226; J. H. Conway and N. J. A. Sloane, *Sphere Packings, Lattices and Groups*, 3rd ed. (1999); J.-P. Serre, *Linear Representations of Finite Groups* (1977).
