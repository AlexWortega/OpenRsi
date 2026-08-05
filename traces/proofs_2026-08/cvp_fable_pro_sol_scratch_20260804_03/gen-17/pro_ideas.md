## Generation 17 — divergent mechanisms

I use this obstruction shorthand: **O1** slack annihilation (G1); **O2** local isolation fails under overlap (G2–5); **O3** external filters/reference changes are not CVP evidence (G6); **O4** exact signed linear/radix kernels (G7); **O5** constant-cost parity and unique-scope relocation, with growing degree non-polynomial (G9–11); **O6** clause drops (G12); **O7** G13 affine collision and constant-\(\ell_1\) triangle ceiling; **O8** affine lifting through codes, carries, bags, and hierarchies (G15–16); **O9** finite-shell success without composition (G14); **O10** need a polynomial-size fixed-target construction with an \(n^c\) gap.

### 1. Trade-resistant quasigroup computation

**Mechanism.** Compile the global AND of clause satisfactions into a balanced quasigroup circuit. Encode each multiplication-table transition by one-hot selectors, choosing tables whose smallest accepting-versus-rejecting integral Latin trade is conjecturally large; the G13 pseudodistribution would then have to become a large trade rather than pass gatewise.

**Expected move.** A depth-\(O(\log m)\) composition theorem turning constant local trade distance into \(m^\alpha\) coefficient norm.

**Audit.** O1: no slack. O2: transitions couple the whole circuit. O3: emit every selector and row. O4: zero residual is possible only via a Latin trade. O5: computes the full AND, not bounded moments. O6: missing gates violate flow/terminal rows. O7: rejecting transcripts are not assumed near the accepting target, so its triangle premise is avoided—unless an affine accepting transcript exists. O8: one-hot linearization may still transmit the affine lift; unresolved. O9/O10: require an explicit polynomial-size quasigroup family and trade-growth theorem.

**Experiment/falsification.** Build the nine-clause circuit over \(S_3\) and order-4 Latin squares; MILP-search the minimum accepting integral trade. A constant-support trade kills it.

---

### 2. Alternating Lawrence lifts of the pair-bag matrix

**Mechanism.** Apply \(r\) iterated Lawrence liftings to the G14 pair-bag incidence matrix, but alternate layer identifications through formula-dependent expander permutations. Lawrence lifting can turn small fiber moves into higher-type Graver moves; with \(r=\Theta(\log m)\), dimensions remain polynomial while a surviving move could acquire polynomial norm.

**Expected move.** Prove every unsatisfiable near-target fiber contains either a residual or a Graver element of norm \(m^\alpha\).

**Audit.** O1: no slack. O2: expander-permuted layers replace private overlap. O3: one explicit matrix and target. O4: exact kernels remain, but the claim concerns their Graver norm. O5: no fixed moment degree. O6: layer normalization should multiply drop cost, subject to audit. O7: **not yet outside**—the G13 vector may lift diagonally. O8: ordinary hierarchy lifting is exactly the danger; alternating identity couplings are the proposed mutation. O9: starts from G14 but seeks a composition lemma. O10: \(2^{O(r)}=\mathrm{poly}(m)\), if the norm exponent survives baseline accounting.

**Experiment/falsification.** Emit one and two alternating lifts of the 520-column matrix; use 4ti2 or exact MILP to minimize coefficient norm in the harmful fiber. A diagonal norm-\(O(1)\) lift kills it.

---

### 3. Multi-order “first violated clause” signatures

**Mechanism.** Replace linear sums of clause violations by the nonlinear identity of the first violated clause under many deterministic orders. A splitter family of orders should make every bounded-\(\ell_1\) signed collection of rejecting assignments have a nonzero histogram somewhere; encode each scan by a finite-state transcript.

**Expected move.** First eliminate the exact nine-term G13 collision, then recursively increase the detectable signed weight to \(m^\alpha\).

**Audit.** O1: no numerical slack. O2: each scan is global. O3: all automaton states and terminal checks enter the lattice. O4: raw residual-zero selectors need also forge every scan. O5: first-violation is a full Boolean function, not fixed-degree moments. O6: dropping a clause changes scans where it is first. O7: different rejecting assignments receive different signatures, so equal-radius compatibility is abandoned. O8: **not escaped automatically**—linear transcript mixtures may forge the nonlinear scan. O9: splitter recursion must yield an actual scaling theorem. O10: polynomially many orders/states are required; no PCP theorem is assumed.

**Experiment/falsification.** Compute violation sets of all 16 assignments and exhaust permutations to test the exact G13 coefficients; then encode the smallest separating orders as automata. A zero terminal-signature affine transcript kills it.

---

### 4. Twisted augmentation-ideal systole

**Mechanism.** Map occurrence inconsistencies to a chain complex whose edges carry a formula-dependent matrix local system, not scalar coefficients. Clause defects inject vectors in an augmentation ideal; the intended theorem is that unsatisfiability creates a nontrivial twisted homology class whose minimum integral representative has polynomial systole.

**Expected move.** Heavy residual scaling then yields an \(n^c\) gap because no short zero-coboundary pseudodistribution exists.

**Audit.** O1: no slack. O2: topology couples overlaps globally. O3: boundary matrices and target are explicit. O4: signed kernels become twisted cycles rather than disappearing by radix. O5: no moment truncation. O6: a drop has a nonzero boundary unless it completes a twisted cycle. O7: **not yet outside**—a linear representation can preserve the G13 affine combination. O8: ordinary cocycles were explicitly rejected; success requires proving the injected class is nonzero in the twisted system. O9: high systole supplies the missing composition law if formula defects map correctly. O10: use constant-rank matrices and a polynomial-size complex.

**Experiment/falsification.** On the nine-clause incidence complex, enumerate \(2\times2\) matrices over \(\mathbb F_3\), lift them integrally, and compute twisted homology plus the shortest harmful cycle. A zero class or constant-support representative kills it.

---

### 5. Grassmann–Plücker rank separation

**Mechanism.** Regard a globally consistent assignment transcript as a decomposable exterior tensor. Add Plücker-coordinate features so the G13 affine pseudodistribution, generically a secant point rather than a decomposable point, acquires rank-defect energy across many occurrence pairs.

**Expected move.** A quantitative distance-to-Grassmannian bound would spread one affine collision over \(\Omega(m^\alpha)\) minors.

**Audit.** O1: no slack. O2: minors join distant occurrences. O3: realize the resulting rational Gram matrix explicitly. O4: linear kernels are charged only if their Plücker image is nonzero. O5: this is rank geometry rather than a fixed list of local moments, although bounded minors may still admit cube parity. O6: include homogeneous normalization coordinates so deletion leaves rank/scale defects. O7: **not automatically outside**—affine combinations of Plücker points are valid lattice vectors. O8: linear marginal lifts still commute; decomposability itself is quadratic and presently unenforced. O9: needs a uniform secant-distance theorem. O10: all \(2\times2\) minors are polynomially many, but higher exterior degree cannot grow freely.

**Experiment/falsification.** Compute all occurrence-pair Plücker features for the 16 global assignments and the G13 coefficients; synthesize the smallest rational PSD metric separating parity and drops. Zero feature defect, or a new constant-support secant, kills it.

---

### 6. Formula-asymmetric Voronoi cone

**Mechanism.** Replace independent half-integral anchors by a global lattice basis with an inverse-\(M\)-matrix/obtuse-superbase Gram form. Engineer positive correlations so legal nonnegative flows remain cheap, while any negative selector coefficient triggers a discrete maximum principle and propagates energy through an expander.

**Expected move.** Prove every exact-residual unsatisfiable vector either is nonnegative—hence an honest assignment flow—or has norm \(m^\alpha\) above completeness.

**Audit.** O1: penalizes coefficients directly, not slack residuals. O2: the Gram matrix is global. O3: emit an exact rational factorization. O4: zero-residual signed kernels are the direct target. O5: no bounded-degree features. O6: normalization/expander boundary should charge drops. O7: formula-dependent radii intentionally abandon equal-radius treatment of all global assignments; nevertheless the triangle ceiling returns if all rejecting encodings remain near. O8: no added linear hierarchy, though an affine Gram cancellation may remain. O9: the maximum-principle inequality would be the composition theorem. O10: sparse Gram/factor dimension must stay polynomial.

**Experiment/falsification.** Solve an SDP on the nine-clause instance for a diagonally dominant rational Gram matrix separating G7, G11, G13, and all drops; rationalize it and run exact shell enumeration. SDP infeasibility or a constant-cost signed vector kills it.

---

### 7. Communication-gadget discrepancy lift

**Mechanism.** Replace each variable/occurrence interface by a small two-party gadget table, such as inner product, and tensor clause legality through the gadget. The hoped-for direct discrepancy statement is that any low-\(\ell_2\) signed measure with all legal local views must retain noticeable global rejection mass.

**Expected move.** Iterated gadget composition turns a local affine collision into a diffuse signed measure of norm \(m^\alpha\), without invoking a PCP theorem.

**Audit.** O1: no slack. O2: gadget blocks couple overlapping views. O3: the full tensor matrix, target, and unrestricted coefficients are emitted. O4: zero-marginal kernels may persist; discrepancy must rule out a short accepting one. O5: tensor depth replaces bounded moment degree while keeping constant gadget size. O6: erasure/drop vectors become large rectangles and must be included in the discrepancy bound. O7: rejection phases make honest rejecting codewords non-equidistant, but the old affine coefficients may tensor-lift. O8: plain linear marginal gadgets are not outside the affine-lift obstruction; a genuine discrepancy lower bound is essential. O9: tensorization is the proposed composition law. O10: \(O(\log m)\)-bit blocks must yield polynomial dimension and a direct proof.

**Experiment/falsification.** Use \(2\)- and \(3\)-bit inner-product gadgets on the nine-clause instance; LP/MILP-minimize signed \(\ell_2\) mass under legal views and acceptance. A constant-mass zero-rejection measure kills it.

### Classical pointers

The sketches use only standard pre-existing toolkits: Sturmfels, *Gröbner Bases and Convex Polytopes* (1996) for Lawrence/Graver constructions; Sipser–Spielman, “Expander Codes” (1996) for expansion-based composition intuition; Harris, *Algebraic Geometry* (1992) for Grassmann–Plücker geometry; and Kushilevitz–Nisan, *Communication Complexity* (1997) for discrepancy terminology.
