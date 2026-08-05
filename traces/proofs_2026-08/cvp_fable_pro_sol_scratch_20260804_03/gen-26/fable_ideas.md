Below, “full fiber” means all integer coefficients are searched, with no externally imposed legality filter.

### 1. Generalized-weight spherical code lift

**Core trick.** Encode each global assignment by a systematic binary codeword \(C(x)\), centered at \(1/2\), so every honest assignment has equal radius. Couple clause selectors to projections of \(x\), and encode the clause-violation vector by a second high-distance code centered at zero; generalized Hamming weights should make low-coefficient affine mixtures non-Boolean on many coordinates.

**Expected move.** One violated clause produces \(\Omega(N)\) zero-centered energy, while G13-type negative mixtures acquire \(\Omega(N)\) shell excess.

**Obstruction audit.** G1: no slack. G2/3: unused. G5: coupling is global, not private-row, but composition remains unproved. G6: carries must be emitted and unrestricted. G7: escaped only if every exact selector kernel leaves the code shell. G9/G11: not bounded-degree moments. G12: dropping a clause creates a coded erasure. G13/G15: directly targeted, not yet escaped—linear code constraints may preserve their affine collision. G19: no flow. G14: finite success gives no scaling. G20/21 require an explicit code-family law; G22 requires the complete joint fiber. G25 degree/phase/group/Lawrence/Macaulay/Delaunay/Plücker assumptions are unused.

**Falsification/test.** Emit the nine-clause instance using the extended Golay \([24,12,8]\) code; exact-solve matched control and obstruction.

**Likely death.** The G13 coefficients also cancel the violation word.

---

### 2. Expander support condenser plus perfect hashing

**Core trick.** Add a sparse expander measurement whose energy is intended to prove: any vector within shell excess \(K\) differs from some honest encoding on at most \(O(K)\) variables. Then use an explicit \(k\)-perfect hash family and full Walsh tables on hashed buckets, with \(k=\Theta(\log n)\); a parity perturbation is detected once all its support is isolated.

**Expected move.** Convert metric closeness into the missing support bound, making polynomially many logarithmic-width tests sufficient.

**Obstruction audit.** G1: no slack. G2/3: replaces local isolation globally. G5: expander rows cross overlaps. G6: support is proved from the objective, not filtered. G7: exact kernels must either expand or be hashed. G9/G11: their parity support is explicitly isolated. G12: drops expand in the measurement graph. G13/G15: low-support affine lifts are hashed; high-support lifts must pay condenser energy. G19: splice support is treated identically. G14: requires an asymptotic expansion theorem. G20/21: potential recurrence comes from \(k=\Theta(\log n)\); G22 requires solving the combined fiber. G25’s degree blind spot is addressed only conditional on the support lemma; its other six mechanism blockers are inapplicable.

**Falsification/test.** On eight variables, combine a 3-regular lossless-expander candidate with \(k=4\) hashes; search both the known nine-clause attacks and an injected five-variable parity.

**Likely death.** A high-support integer circulation may have zero expander syndrome and constant anchor excess.

---

### 3. Recursively closed min-plus NAND tile

**Core trick.** Search for one fixed lattice tile whose unrestricted port-conditioned CVP costs implement NAND, including explicit TRUE, FALSE, DROP, and malformed states. Demand a min-plus contract closed under gluing: after scale \(S\), every illegal parent state costs at least \(\rho>1\) times the legal radius, including entangled child representatives.

**Expected move.** A balanced NAND circuit of depth \(O(\log n)\) would amplify the ratio to \(\rho^{\Theta(\log n)}=n^c\).

**Obstruction audit.** G1: no slack residual. G2/3/G5: replaced by an exact compositional port theorem. G6: every port fiber is unrestricted and emitted. G7: zero-residual signed selectors are malformed states. G9/G11: no moment truncation. G12: DROP is an explicit state. G13/G15: affine lifts must appear in the cost table. G19: signed splices are included as malformed fibers. G14: the recurrence, not a finite shell, supplies scaling. G20/21 are exactly the required contract; G22 is handled by minimizing over the full glued fiber. G25’s bounded-Delaunay criticism still applies unless an eigenvalue bound and exact recursive table are certified; the other six blockers are unused.

**Falsification/test.** Enumerate small integral Gram matrices for a two-input NAND tile with at most 12 coefficients, then exact-compose two tiles at depth two.

**Likely death.** Quadratic geometry may force an entangled representative cheaper than every statewise min-plus composition.

---

### 4. Integer cosystolic-cover amplifier

**Core trick.** Represent consistency defects as integral cochains on a concrete bounded-degree 2-complex; clause falsification should create a prescribed nontrivial relative cohomology class. Lift the complex through explicit covers with cosystolic expansion, so every integral representative of that class has support polynomially larger than a satisfiable boundary.

**Expected move.** Signed selectors become chains rather than exceptional cheats; expansion would lower-bound their norm uniformly.

**Obstruction audit.** G1: no slack. G2/3/G5: overlap is encoded by shared boundary maps. G6: boundary, carry, and parity coordinates are emitted. G7: exact kernels are cycles and must be classified homologically. G9/G11: parity becomes a cohomology class, not a degree blind spot. G12: drops have relative boundary. G13/G15: affine lifts may be boundaries—this is not yet escaped. G19: signed flows become integral 1-chains. G14: finite systole is insufficient. G20/21 require polynomial cover growth; G22 requires shortest representatives after gluing. G25’s topology objection is only partially answered by specifying maps and classes; formula-to-class correspondence remains open. Its other six blockers are unused.

**Falsification/test.** Use the six-vertex triangulation of \(\mathbb{RP}^2\), attach one clause gadget, form its smallest nontrivial cover, compute SNF, and exactly find shortest representatives of every relative class.

**Likely death.** The formula defect becomes a boundary, or integral carries produce a short representative invisible mod 2.

---

### 5. Algebraic-integer norm barrier

**Core trick.** Map every emitted defect into an algebraic integer \(\alpha\in\mathbb Z[\zeta_p]\) and include all conjugate embeddings as Euclidean coordinates. If \(\alpha\neq0\), the integral field norm and AM–GM give \(\sum_\sigma|\sigma(\alpha)|^2\ge [K:\mathbb Q]\), permitting polynomial amplification by choosing polynomial field degree.

**Expected move.** Obtain RS-like spreading without root counting, evaluation collisions, or free algebraic slack.

**Obstruction audit.** G1: outside its slack assumption, but not its zero-residual failure. G2/3/G5: no isolation or composition theorem. G6: embeddings and all coefficients are emitted. G7: an exact residual kernel still gives \(\alpha=0\). G9/G11: not low-degree moments. G12: a drop is charged if included in \(\alpha\). G13/G15: fixed linear embeddings preserve affine collisions, so these remain fatal candidates. G19: signed-flow residuals may likewise vanish. G14: degree supplies scaling only after base nonvanishing. G20/21 depend on baseline accounting; G22 is the simultaneous kernel problem. G25’s fixed-label linearity blocker applies; degree/hash, group, Lawrence, Macaulay, Delaunay, and Plücker blockers do not.

**Falsification/test.** Take \(p=17\), encode all nine-instance residual rows as coefficients of \(\alpha=\sum r_j\zeta_{17}^j\), emit the Minkowski Gram matrix, and exact-solve.

**Likely death.** G7 or G13 yields \(\alpha=0\) identically, making field degree irrelevant.

---

### 6. Discrete-convex sanitizer for accepting flows

**Core trick.** Retain a branching-program semantics but replace edgewise anchors by a laminar family of interval inventories with an \(M\)-convex quadratic energy. Seek an exchange theorem saying every minimum-energy integral unit flow is nonnegative and path-like; any negative path coefficient must create inventory imbalance across many scales.

**Expected move.** Eliminate G19’s two-negative accepting splice before adding an output-rejection amplifier.

**Obstruction audit.** G1: no slack. G2/3/G5: irrelevant unless tiles are composed. G6: inventories are objective coordinates, not filters. G7: exact flow kernels are charged by energy rather than residuals. G9/G11: no moments. G12: zero-flow drops need explicit inventory pricing. G13: affine path combinations remain possible unless strict exchange excludes them. G15: directly relevant—if inventories only enforce marginals, its hierarchy lift survives. G19: this is a proposed repair, not yet outside its assumptions. G14: finite path sanitation gives no gap. G20/21 require a scale-stable exchange inequality; G22 requires joint minimization over inventories. G25’s group-tag and Lawrence criticisms are avoided, but its recursive-contract requirement remains; other blockers are unused.

**Falsification/test.** Apply dyadic interval inventories to the exact 3,250-layer G19 flow, first on a 16-layer extracted splice, and solve the unrestricted accepting fiber under several analytically normalized \(M\)-matrix Grams.

**Likely death.** The signed splice may preserve every inventory, or its \(O(\log L)\) excess may be negligible relative to completeness radius.
