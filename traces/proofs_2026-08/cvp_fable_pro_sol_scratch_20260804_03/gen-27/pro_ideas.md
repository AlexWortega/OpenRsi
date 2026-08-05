I use the obstruction shorthand: G1 slack annihilation; G2/3 noncomposing local isolation; G5 overlap circuits; G6 external-filter invalidity; G7 exact signed kernels; G9/11 parity kernels; G12 drops; G13 affine collision; G14 finite-only pair-bag pass; G15 affine hierarchy lift; G19 signed-flow splice; and the gate’s G20/21 growth and G22 state-closure/entanglement requirements.

### 1. Recursively closed port-state lattice tiles
**Core trick.** Turn the G14 pair-bag gadget into a finite lattice tile whose ports record every bounded boundary marginal, including malformed and DROP states. Exact min-plus gluing of two tiles defines a transfer operator; seek bad-cost growth \(\lambda\) exceeding completeness growth \(\mu\), so depth \(d\) yields \((\lambda/\mu)^{d/2}=n^c\).

**Expected move.** A certified \(\lambda>\mu\) depth-two contract, rather than another isolated shell pass.

**Obstruction audit.** No slack/radix (G1/G7), local-isolation assumption (G2/3/G5), or external filtering (G6). Parity, drops, G13/G15 affine lifts, and G19 splices are explicit port classes. It upgrades G14 directly. Exhaustive state closure and unrestricted glued minimization address G20/21/G22, but only finite depth initially.

**Falsification.** Any unlisted minimizing port state, completeness mismatch, or \(\lambda\le\mu\).

**Smallest experiment.** Split the all-eight-clause three-variable core into two four-clause tiles; use G14 anchors and weight 25, enumerate every state through \(B+32\), glue two copies, and certify coefficient bounds from the Gram eigenvalue.

**Likely death.** An entangled state reenters cheaply, forcing \(\lambda=\mu\).

---

### 2. Compressed Boolean-ideal inconsistency
**Core trick.** Introduce squarefree moment variables \(y_S\), fix \(y_\varnothing=1\), and add linear rows obtained by multiplying each clause’s falsifying monomial by all monomials through degree \(d-3\). A satisfying assignment gives a Boolean moment vector; sufficiently high degree makes an unsatisfiable formula’s affine system inconsistent even over \(\mathbb Q\), allowing polynomially weighted residual amplification without slack.

**Expected move.** Find a polynomial-size compressed representation of high-degree elimination, making every unsatisfiable instance pay one integral residual of weight \(N^{1+2c}\).

**Obstruction audit.** G1/G7 vanish only when inconsistency is exact. This is global, not G2/3/G5 local composition, and every equation is emitted, satisfying G6. G9/11 parity is not outside the assumptions: it may survive below degree \(d\). Drops violate normalization (G12). G13/G15/G19 are replaced by low-degree pseudomoments, not automatically defeated. G14 and G20/21/G22 remain size/scaling obligations.

**Falsification.** A rational normalized pseudomoment for the unsatisfiable core.

**Smallest experiment.** For the eight clauses on three variables, use all eight moments \(y_S\), emit the degree-three matrix, compute SNF/rational inconsistency, then exactly minimize anchor plus weighted residuals against a seven-clause control.

**Likely death.** Required degree is linear, making the moment space exponential.

---

### 3. Delaunay-cell exclusion of signed coefficients
**Core trick.** Search for a rational ellipsoid whose boundary lattice points are precisely the legal port representatives of a gadget—a Delaunay cell—while every other lattice point lies beyond radius \(\rho R\). Glue cells by shared faces and test whether anisotropic rescaling gives a recursive empty-ellipsoid separation.

**Expected move.** Replace cancellation-prone residual amplification by a geometric “no intervening lattice point” theorem, with \(\rho\) increasing under composition.

**Obstruction audit.** There are no slacks, filters, or flows (G1/G6/G19), and overlap is part of the face gluing rather than G2/3/G5 private rows. Exact kernels, parity, and drops (G7/G9/11/G12) are simply candidate interior lattice points. G13 is **not** outside the assumptions: its affine combination is a lattice point and may forbid any useful ellipsoid. G15 is likewise tested geometrically. Unlike G14, recursion is the target; G20/21/G22 require full depth-two enumeration.

**Falsification.** The G13 point lies within every feasible legal circumellipsoid, or tensor gluing preserves only a constant ratio.

**Smallest experiment.** On the eight-clause core and satisfiable control, enumerate Gram matrices with entries in \([-2,2]\), solve exact rational center/radius inequalities, and enumerate all unrestricted vectors below \(1.2R\) using a certified eigenvalue bound.

**Likely death.** Triangle/affine geometry enforces only constant separation.

---

### 4. Nonlinear design fibers with integral trade distance
**Core trick.** Replace each pair-bag assignment by a fiber of block-design witnesses, retaining only its semantic point marginal. Measure the shortest integral **trade** between legal and harmful fibers; tensor products of designs might multiply trade energy even when ordinary code distance and linear syndromes do not.

**Expected move.** Obtain a family whose minimum harmful lift costs \(D^t\) while honest anchor cost grows only \(W^t\), with \(D/W>1\).

**Obstruction audit.** No slack, radix, or external filter (G1/G6/G7). Complete joint fibers address G2/3/G5. G9/11 attacks become low-weight trades; G12 becomes a missing-block trade. This is not merely G13’s fixed linear hash because every semantic vector has many unrestricted lifts—but if the cheapest lift is canonical-linear, G13 applies exactly. G15 and G19 become signed trades rather than hierarchy/flow arguments. G14 supplies the base bags only; tensor growth and full trade enumeration must satisfy G20/21/G22.

**Falsification.** A bounded-support Graver trade survives tensor squaring with additive rather than multiplicative cost.

**Smallest experiment.** Use the eight points and fourteen affine hyperplanes of \(\mathbb F_2^3\); attach hyperplane witnesses to one G14 bag, compute the complete integer kernel/Graver moves, then repeat for its tensor square.

**Likely death.** Small trades lift independently in one tensor factor.

---

### 5. Prony moments plus a sparse-or-expensive dichotomy
**Core trick.** View a signed cheat as an integral measure on complete assignments. First \(2K\) power moments of distinct assignment labels detect every nonzero measure supported on at most \(K\) atoms; prove separately that any representation using more than \(K\) atoms necessarily has anchor energy large enough for the desired gap.

**Expected move.** Choose polynomial \(K\): sparse G13/G19 combinations are detected algebraically, while dense combinations pay directly.

**Obstruction audit.** There is no free slack or radix (G1/G7), and moments are global rather than G2/3/G5 local checks; all rows are emitted (G6). Taking \(K\ge13\) detects the known G9/11/G13 combination if it really has a global atomic decomposition; drops are separate atoms (G12). G15/G19 are covered only if their signed vectors admit the same decomposition. Thus this is **not outside** Generation-26’s missing-support-lemma blocker. G14 and G20/21/G22 still demand a polynomial compositional implementation.

**Falsification.** A low-anchor local selector has no sparse global decomposition yet annihilates all implemented moments.

**Smallest experiment.** Explicitly use all sixteen assignments of the nine-clause four-variable obstruction, moments \(j=0,\dots,8\), and solve for the minimum-support integral measure projecting to each known G7/G11/G13/G19 attack.

**Likely death.** Local pseudodistributions require exponentially supported or nonexistent global measures, invalidating the dichotomy.

---

### 6. Integral relative systoles as inconsistency amplifiers
**Core trick.** Map selector inconsistency to a prescribed relative homology class in an integral chain complex, not merely to a nonzero boundary. Attach a polynomial-size cover or bounded-degree amplifier complex in which every representative of that class has large Euclidean support, while satisfying instances map to the zero class and use no amplifier coordinates.

**Expected move.** If the amplifier has size \(M=m^k\) and relative systole \(M^\alpha\), bad distance can exceed the \(O(\sqrt m)\) completeness radius by a polynomial factor.

**Obstruction audit.** No slack, local matrix isolation, or external filters (G1–G6). Exact kernels/parity (G7/G9/11) would have to be null-homologous; this must be checked, not assumed. Relative boundary conditions expose drops (G12). G13/G15/G19 affine combinations cannot erase a genuinely nonzero integral class, but establishing that semantic map is exactly the missing step. G14 is irrelevant except as a seed encoding. This directly targets—but is not yet outside—the Generation-26 topology objection and G20/21/G22 scaling/entanglement requirements.

**Falsification.** The unsatisfiable core maps to zero, a short boundary, or a torsion class killed in a small cover.

**Smallest experiment.** Build the selector-incidence mapping cylinder for the eight-clause core, attach a \(3\times3\) torus grid, compute relative SNF, and exactly find the shortest integral representative for every drop/parity/affine attack.

**Likely death.** Logical inconsistency remains a local boundary rather than a robust global class.
