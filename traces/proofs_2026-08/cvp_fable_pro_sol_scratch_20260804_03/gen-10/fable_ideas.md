## Generation 10 — divergent mechanisms

**Obstruction key.**  
**O1 Slack:** Gen-1 free integer slack annihilates amplified residuals.  
**O2 Composition:** Gen-2/3 local isolation collapses when clause marginals are freed or clauses overlap.  
**O3 Invalid embedding:** Gen-6 used external filters, changed references, and missed unrestricted/mod-2 vectors.  
**O4 Linear kernel:** Gen-7 radix rows cannot detect exact zero-residual signed selectors.  
**O5 Parity/padding:** Gen-9 degree-two cube parity has constant cost, survives padding, and gives a constant global bound.  
**O6 Scaling:** no uniform synthesis or dimension-dependent gap law exists.

### 1. Degree-three Walsh closure

**Mechanism.** Add global monomial variables through degree three and require each clause selector to match all eight Walsh characters of its three literals. The full \(8\times8\) Walsh transform uniquely determines a signed distribution, unlike degree-two moments.

**Expected move.** The seven-term parity repair acquires an integral cubic residual, which may then be scaled polynomially without increasing honest residual cost.

**Map check.** O1: no slack. O2: rows share global monomials rather than private marginals, but composition remains unproved. O3: every monomial variable and equality must be inside one fixed-target lattice; unrestricted coefficients are searched. O4: the cube kernel has nonzero top Walsh coefficient. O5: this is expressly outside the degree-two assumption, though padding still wins if cubic variables can absorb repairs. O6: no scaling theorem yet.

**Falsification.** A zero-residual signed selector after optimizing unrestricted global cubic variables, or ratio contraction under clause duplication.

**Experiment.** Add signed cubic-moment rows to the Gen-9 obstruction/control and exactly enumerate through anchor excess 24; first evaluate the displayed parity witness.

**Likely death.** Global cubic variables behave as unconstrained pseudo-products and absorb isolated clause repairs.

---

### 2. Odd-prime Construction-A selector code

**Mechanism.** Regard full clause-label deviations as symbols over \(\mathbb F_3\), couple them with a systematic expander-code parity matrix, and realize the congruences directly as a Construction-A lattice. A harmful deviation must then expose a nonzero balanced residue or become a codeword with large Hamming support.

**Expected move.** Replace fragile rational isolation by torsion plus code distance, yielding overlap-robust constant soundness before amplification.

**Map check.** O1: Construction A uses no optimized carry/slack columns. O2: checks span the global Tanner graph, not private clause fibers. O3: congruences are lattice membership conditions in a fixed target; no external filtering or mod-2 inference. O4: old zero real residual is irrelevant only if its full-label vector is outside the code kernel—this must be checked. O5: full labels, not degree-two moments, are coded; nevertheless the parity vector may be forced into the kernel by honest differences. O6: code distance alone gives at most a constant ratio.

**Falsification.** The cube repair lies in the \(\mathbb F_3\)-span of honest assignment differences, or a short balanced codeword survives overlap.

**Experiment.** For \(p=3,5\), compute that span on the nine-clause instance, then test all small systematic parity matrices.

**Likely death.** Any linear code containing all honest encodings also contains their affine-span cheats.

---

### 3. Cosystolic clause complex

**Mechanism.** Glue clause cubes into a three-dimensional incidence complex: selector deviations are 2-cochains, and their third finite difference is the coboundary on each clause 3-cell. Add integral coboundary rows and homology-pairing rows from a small cosystolic-expander lift.

**Expected move.** A local parity repair either creates many nonzero 3-cell syndromes or enters a nontrivial homology class whose shortest representative has growing support.

**Map check.** O1: no slack. O2: detection is global through shared faces, not fixed private marginals. O3: all boundary and homology rows must be emitted in the fixed lattice and audited over \(\mathbb Z\) by Smith form; mod-2 evidence alone is insufficient. O4: the former zero residual has nonzero third coboundary unless it becomes a boundary. O5: degree-three topology directly sees cube parity, but repeated satisfied clauses may still localize it. O6: polynomial gap requires an explicit family with quantitative systolic bounds.

**Falsification.** A bounded-support integral cocycle/boundary realizes the parity repair after two clauses are glued.

**Experiment.** Build the chain complex for two clauses sharing one or two variables; compute SNF and enumerate minimum-support cochains, then test the nine-clause complex.

**Likely death.** Arbitrary clause incidence creates contractible local bubbles with constant-size fillings.

---

### 4. Delaunay-shell legality gadget

**Mechanism.** Replace residual-based legality by pure Voronoi geometry: realize the seven legal labels as exactly the nearest lattice points to a clause target, with every other integral combination outside a large empty Delaunay shell. Glue clause lattices along variable-coordinate projections rather than by private syndrome rows.

**Expected move.** Signed affine combinations are charged directly even when every linear consistency residual vanishes.

**Map check.** O1: there are no slacks or residual annihilators. O2: local geometry does not assume fixed marginals, but fiber-product gluing could recreate short points and must be tested. O3: this is natively fixed-target CVP with unrestricted lattice coefficients. O4: exact residual kernels are irrelevant because distance comes from the nearest-point shell. O5: the parity vector is simply another lattice point and is included explicitly; no degree-two assumption. O6: an annulus ratio growing as \(N^c\), stable under gluing, is completely unproved.

**Falsification.** Parallelogram identities force a bounded-distance signed combination whenever seven legal points share one circumsphere.

**Experiment.** On one OR clause, optimize a rational Gram matrix with seven equidistant nearest points while enumerating coefficients in \([-2,2]^7\); then glue two copies and repeat.

**Likely death.** Euclidean PSD inequalities bound the second-shell ratio by a constant, and overlap worsens it.

---

### 5. Integral product-gap amplification

**Mechanism.** Start from a kernel-free constant-size clause/consistency gadget and iterate a product-code composition \(k=\Theta(\log n)\) times. If every nonzero integral defect branches into at least \(d>1\) defects per level while size grows by \(C\), the final residual support is \(d^k=n^{\log_C d}\).

**Expected move.** Convert a proved constant local separation into an explicit polynomial Euclidean gap with polynomial dimension, using a direct lattice product lemma rather than a PCP theorem.

**Map check.** O1: products contain no slack. O2: composition is the central theorem, not assumed from local isolation. O3: each product must emit one fixed basis/target and quantify over entangled integer coefficients. O4: not outside—an exact seed kernel tensors forever, so Gen-7 cannot seed it. O5: likewise Gen-9 parity must first be removed. O6: this mechanism specifically targets scaling, but dimension and distance recurrences remain unproved.

**Falsification.** An “entangled” tensor vector is shorter than every product witness, or dimension grows quasipolynomially.

**Experiment.** Tensor-square a tiny full-Walsh clause gadget and enumerate coefficients in \([-2,2]\); separately verify that the current Gen-9 parity vector indeed remains a zero-syndrome product vector.

**Likely death.** Arbitrary lattice sums defeat multiplicativity; proving the needed product theorem may effectively recreate forbidden PCP gap amplification.

---

### 6. Sparse Nullstellensatz dual lattice

**Mechanism.** Build the degree-\(d\) Macaulay system generated by \(x_i^2-x_i\) and the clause polynomials, and encode its dual affine functionals as lattice coefficients. Satisfying assignments give honest evaluation functionals; an unsatisfiable instance should force every normalized functional to violate some generated identity.

**Expected move.** Degree-three identities detect the cube-parity pseudo-distribution, while coefficient repetition or coding amplifies any integral violation.

**Map check.** O1: no clause slack. O2: the polynomial ideal is global across overlaps. O3: normalization and every moment identity must be actual lattice rows with a fixed reference; calculations over \(\mathbb Q\) and odd primes supplement, not replace, unrestricted CVP search. O4: the signed selector survives only if it extends to a degree-\(d\) pseudo-evaluation. O5: degree three is outside the degree-two parity kernel, though higher-degree pseudo-evaluations may replace it. O6: general formulas may require linear degree and exponentially many monomials.

**Falsification.** A normalized degree-\(d\) dual functional satisfies all rows on the nine-clause obstruction, or the first required degree already grows with \(n\).

**Experiment.** Construct exact degree-3 and degree-4 Macaulay matrices for the obstruction; compute rational/odd-prime nullspaces and enumerate minimum-anchor dual functionals.

**Likely death.** Classical Nullstellensatz degree lower bounds make any general polynomial-size realization impossible.

Classical ingredients invoked: Sipser–Spielman, *Expander Codes* (IEEE TIT, 1996); Conway–Sloane, *Sphere Packings, Lattices and Groups*, 3rd ed. (1999), for Construction A; Kaufman–Kazhdan–Lubotzky, *Isoperimetric Inequalities for Ramanujan Complexes and Topological Expanders* (GAFA, 2016); Beame–Impagliazzo–Krajíček–Pitassi–Pudlák, *Lower Bounds on Hilbert’s Nullstellensatz and Propositional Proofs* (PLMS, 1996).
