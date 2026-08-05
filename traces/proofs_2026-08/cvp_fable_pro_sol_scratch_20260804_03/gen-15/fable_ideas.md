I use the following obstruction names below:

- **O1—G1 slack annihilation:** free integer slacks erase amplified residuals.
- **O2—G2/3/5 noncomposition:** fixed-marginal local isolation fails once overlap frees marginals.
- **O3—G6 gate failure:** external filters, changed references, or modular bypasses are not CVP evidence.
- **O4—G7 zero kernel:** signed selectors can annihilate every linear/radix residual.
- **O5—G9/11 parity:** constant-cost seven-term parity survives bounded-degree moments, especially at unique scopes.
- **O6—G12 clause drop:** fingerprints charge parity but not deletion enough.
- **O7—G13 affine collision:** every compatible linear hash vanishes on a harmful honest-affine-span vector.
- **O8—G14 asymptotic drop:** unweighted pair bags have quadratic baseline but only linear deletion cost; affine lifts were not optimized.

### 1. Weighted sparse tensor hierarchy

**Mechanism.** Replace complete pair bags by a bounded-degree expander hierarchy of 2-, 4-, and 8-clause joint bags. Give level-\(j\) bag anchors weight \(\varepsilon_j\) but marginal checks weight \(W_j\gg\varepsilon_j\), aiming for completeness \(O(m)\) while deletion either creates a \(W_j\)-residual or propagates non-Boolean mass to \(m^\delta\) bags.

**Expected move.** Prove squared soundness \(R^2+\Omega(m^{1+\delta})\) against \(R^2=O(m)\).

**Obstructions.** O1: no slacks. O2: checks are shared globally, not private; expansion must prove composition. O3: emit every anchor/check and search unrestricted coefficients. O4: a zero kernel can still kill it unless tensor propagation excludes it. O5: full bag marginals replace unique moments. O6: deletion is explicitly weighted. O7: joint lifting is nonlinear in raw selectors, though affine collisions may lift. O8: sparse bags and tiny auxiliary anchors remove the quadratic baseline assumption.

**Falsification/experiment.** For minimally unsatisfiable chains at \(m=8,16,32\), generate degree-3 hierarchies and use SNF+MILP to optimize clause drops and zero-residual affine lifts.

**Likely death.** Sparse stopping sets support constant-density pseudodistributions.

---

### 2. Sparse integral Nullstellensatz lattice

**Mechanism.** Use Boolean equations \(x_i^2-x_i=0\) and clause equations \(\prod_{\ell\in C}(1-\ell)=0\). Build an integral Macaulay lattice whose coordinates are selected monomial multiples; an unsatisfiability certificate producing \(D\neq0\) in the constant coordinate can then be weighted enormously, while every satisfying evaluation annihilates all rows.

**Expected move.** Discover a formula-uniform polynomial-size sparse monomial basis yielding an integral certificate with polynomial bit complexity; amplify its nonzero constant coordinate by \(n^K\).

**Obstructions.** O1: no slack variables. O2: the certificate is global. O3: all monomial variables and equations must be emitted, with no “pseudoexpectation” filter. O4: a signed zero kernel is exactly a truncated pseudo-solution and survives unless the certificate lies in the chosen basis. O5: degree is adaptive, not capped at three. O6: contradiction is a zero-baseline residual, not a tag. O7: Veronese coordinates enlarge the raw encoding, but truncated affine collisions may persist. O8: no bag baseline.

**Falsification/experiment.** Compute rational rank, integer SNF, minimum certificate degree, and coefficient height for chains and small hard 3CNFs at degrees \(2\)–\(6\).

**Likely death.** Proof-complexity degree/size lower bounds force superpolynomial Macaulay dimension.  
(Classical hook: Beame–Impagliazzo–Krajíček–Pitassi–Pudlák–Woods, 1996.)

---

### 3. Homological obstruction amplifier

**Mechanism.** Represent local selector inconsistencies as integer chains in a formula-derived complex: honest assignments are fillings of the target boundary, while unsatisfiable encodings should leave a nontrivial homology class. Take a sparse homological product with an explicit high-cosystole complex so every such class has Euclidean support \(N^\delta\), without duplicating an honest anchor at every check.

**Expected move.** Reduce soundness to an integral systolic inequality and obtain polynomial distance from a bounded-degree chain complex.

**Obstructions.** O1: no residual slacks. O2: the boundary operator is global, so local circuits must extend through the complex. O3: boundary matrices and target are fully emitted; SNF verifies homology. O4: exact signed kernels remain dangerous if they are boundaries. O5: parity vectors are treated as cycles rather than moments, but may be null-homologous. O6: clause deletion creates a boundary defect intended to have large filling norm. O7: higher-cell coordinates escape the raw hash assumption, although an affine collision may still lift to a boundary. O8: bounded-degree complexes avoid quadratic bag baselines.

**Falsification/experiment.** Build the nine-clause chain complex, product it with the smallest explicit 2-complex available, compute SNF, and MILP-search the shortest harmful chain/filling.

**Likely death.** All selector attacks may be homologically trivial, or Hamming cosystole may not imply Euclidean CVP distance.  
(Classical hook: Tillich–Zémor homological products, 2009.)

---

### 4. Nonlinear coset-leader carry code

**Mechanism.** Map each legal local label to an equal-energy word \((u,f(u))\) in a genuinely nonlinear error-correcting code. Embed its coset-leader graph using integer carry coordinates, hoping that a nearby lattice vector must decode to one codeword, while affine mixtures of legal labels fail the nonlinear redundancy \(f\).

**Expected move.** Obtain a local shell theorem: honest labels have radius \(r\), every other unrestricted integer combination has distance at least \(n^c r\); consistency checks then glue decoded information bits.

**Obstructions.** O1: carries are emitted and code-constrained, but free carries could reproduce the G1 failure. O2: decoded information is globally shared. O3: exact lattice closure and all carries must be searched. O4: generator closure may create a zero syndrome. O5: nonlinear redundancy is not a bounded-moment test. O6: code distance should charge the zero-word/drop, subject to equal-energy accounting. O7: outside linear-hash assumptions because lifted coordinates use \(f(u)\); however lattice additivity may erase this distinction. O8: code length can be \(O(m)\), with no pair mesh.

**Falsification/experiment.** Exhaustively search nonlinear length-\(8\) or \(16\) codes for eight equal-energy label words; construct the carry lattice and enumerate its exact first two shells.

**Likely death.** Every lattice generated by nonlinear codewords sees their additive span, reinstating affine collisions.

---

### 5. Delaunay exact-disjunction gadget

**Mechanism.** Search for a rational positive-definite form \(Q\) and center \(c\) whose exact nearest integer points are precisely the seven satisfying labels of a clause, with all other integer points on a shell \(K\) times farther away. Glue clause gadgets only through heavily weighted equality coordinates; local legality is then geometric rather than a linear residual.

**Expected move.** Set \(K^2\gg m^{1+2c}\), giving completeness \(R^2=O(m)\) but polynomially larger cost for either an illegal local coefficient vector or inconsistent labels.

**Obstructions.** O1: no slacks. O2: overlap remains a real issue; weighted equality must exclude the G5 short circuit. O3: emit an exact rational Gram factor and enumerate unrestricted shells. O4: zero residual cannot bypass a positive-definite local shell. O5: parity is merely another non-nearest integer point. O6: the zero/drop vector must lie beyond the large second shell. O7: this directly penalizes the affine-collision vector rather than hashing it. O8: only \(O(m)\) local gadgets are anchored.

**Falsification/experiment.** Use SDP followed by rational reconstruction/MILP for seven legal points in dimensions \(7\)–\(12\), demand \(K\ge10\), and enumerate coefficients in a certified norm box.

**Likely death.** Delaunay geometry may impose a constant upper bound on the second-shell ratio once seven alternatives share one sphere.

---

### 6. Tensor-power shell amplification

**Mechanism.** First find a constant-dimensional clause gadget with a rigorously certified gap \(\rho>1\) and a stronger “primitive nearest vectors only” property. Tensor the gadget \(k=\Theta(\log n)\) times locally; if CVP distance and primitive rigidity multiply, local dimension is \(d^k=n^{O(1)}\) and the gap becomes \(\rho^k=n^c\).

**Expected move.** Prove that every near vector in the tensor lattice is a pure tensor of near vectors from the base gadget; then add zero-residual consistency between decoded labels.

**Obstructions.** O1: the base certificate must contain no free slack. O2: tensoring does not solve overlap, so gluing needs a separate composition lemma. O3: tensor bases and targets are emitted exactly. O4: any base zero kernel tensors forever; it is a hard prerequisite. O5: parity may become an entangled tensor vector rather than disappear. O6: clause drops must inherit multiplicative, not additive, cost. O7: Kronecker lifting is nonlinear in raw selectors, so the raw affine-span theorem does not directly apply. O8: amplification is local polynomial blow-up, not quadratic pair bags.

**Falsification/experiment.** Tensor-square the smallest candidate local Gram gadget and exactly enumerate vectors below the predicted \(\rho^2\) threshold, explicitly classifying non-pure minimizers.

**Likely death.** CVP minima are generally not multiplicative: entangled integer tensors can be much shorter than pure ones.
