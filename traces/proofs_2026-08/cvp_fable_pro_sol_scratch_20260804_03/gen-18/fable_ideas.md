I use the following obstruction labels: **O1** free-slack/exact-residual annihilation (G1/G7); **O2** short overlap kernels (G5); **O3** external-filter/reference/mod-2 invalidity (G6); **O4** bounded-degree parity relocation (G9/G11); **O5** absence of a dimension-growing ratio; **O6** integral affine-span lift (G13/G15); **O7** clause/bag drops (G12); **O8** finite-shell evidence without polynomial-size unrestricted composition (G14).

### 1. Logarithmic-degree splitter/Möbius lift
**Core trick.** Use an explicit perfect-hash family mapping variables into \(k=\Theta(\log n)\) colors. For each hash, introduce the complete \(2^k\)-entry signed assignment table and enforce exact Möbius marginals; every clause is evaluated inside every hash injective on its variables.

**Expected move.** Prove that a zero-residual legal pseudomeasure for an unsatisfiable formula needs large support or violates many hash tables; weight those residuals by \(W\) to obtain an \(N^c\) gap.

**Obstruction check.** O1: no slack/carries. O2: global hash tables, although overlap kernels remain possible. O3: all tables and checks enter one fixed-target CVP. O4: degree grows as \(\log n\), outside fixed-degree relocation. O5: requires an unproved quantitative splitter lemma. O6: specifically targets G13, but is not outside O6 until that affine measure fails some table. O7: replicated normalization should charge drops. O8: polynomial size for fixed small \(k/\log n\), but composition is unproved.

**Experiment.** Add the complete four-variable table to the nine-clause instance and exactly search through \(B+64\), including G13 and drops.

**Likely death.** Signed distributions may satisfy every logarithmic marginal; known hard formulas can require linear-degree reasoning.

---

### 2. Construction-A deep-hole assignment shell
**Core trick.** Seek a \(q\)-ary linear code whose Construction-A lattice has a target coset with the degree-three Veronese encodings of Boolean assignments as its designated nearest vectors, while every other lattice point is polynomially farther. Clause violation is linear in the Veronese coordinates and can therefore receive a huge zero-completeness weight.

**Expected move.** Reduce soundness to a code-theoretic “next-shell” theorem rather than enforcing Booleanity by local residuals.

**Obstruction check.** O1: no auxiliary slack. O2: one global shell, not composed clause gadgets. O3: parity checks define an unrestricted fixed-target lattice. O4: degree three is still exposed to parity unless the code geometry separates its affine image. O5: the sought next-shell ratio is exactly the missing scaling lemma. O6: not outside—any short affine combination of shell points is fatal. O7: omitted clauses still incur explicit violation coordinates. O8: Construction A is polynomial-size if the code is explicit; existence is open.

**Experiment.** For three variables and \(q\in\{5,7\}\), use MILP to search parity-check matrices making all eight Veronese points equidistant and enumerate the next coset shell exactly.

**Likely death.** The G13-style bounded-\(\ell_1\) affine dependence may force another lattice point within a constant multiple of the honest radius.

---

### 3. Expanding cut/cocycle lattice Booleanizer
**Core trick.** Represent assignments as cuts in an expander bundle: variable choices select shores, while subdivided clause hyperedges measure falsification. Use the integral cut or cocycle lattice and a half-integral target chosen so low-energy cochains should be genuine cuts; edge connectivity amplifies any inconsistent signed cochain.

**Expected move.** A structural Voronoi theorem would make non-Boolean coefficients pay \(\Omega(\lambda)\) edges, allowing one violated clause to carry polynomial weight.

**Obstruction check.** O1: no slack/carries. O2: overlap is absorbed into one global graph, but short cycles may reproduce O2. O3: emit the incidence basis and target directly. O4: mechanism is topological rather than bounded-moment. O5: requires expansion exceeding the honest cut baseline by \(N^{2c}\), presently unsupported. O6: raw selector affine lift does not directly apply, though signed sums of cuts may replace it. O7: deleting a clause edge should expose its incident expansion boundary. O8: explicit polynomial graphs exist, but the required Voronoi characterization does not.

**Experiment.** Build a small expander bundle for the all-eight-clause three-variable formula; enumerate unrestricted cocycles and compare the nearest genuine cut, signed cut, and edge-drop states.

**Likely death.** Cut differences themselves form short lattice vectors, and expansion may increase completeness and cheating energies proportionally.

---

### 4. Algebraic-number norm barrier
**Core trick.** Encode variable choices as algebraic integers with distinct conjugate signatures, and encode each clause defect as an element of an ideal. A nonzero defect has nonzero integral field norm; scale complementary embeddings so the product formula forces at least one large Euclidean coordinate.

**Expected move.** Replace residual repetition by a multiplicative invariant that integer slack cannot annihilate unless the clause ideal element is exactly zero.

**Obstruction check.** O1: algebraic norm detects nonzero defects, but an exact zero defect still bypasses it. O2: one global algebraic integer may avoid local overlap composition. O3: the full Minkowski embedding and ideal basis must be emitted; no external norm test is allowed. O4: not a fixed-degree moment scheme. O5: field discriminant/scaling must yield a polynomial ratio—unknown. O6: not outside if affine combinations remain exact zero ideal elements. O7: a drop changes an ideal coordinate and should have nonzero norm. O8: field degree and coefficient bit-length must stay polynomial; this is doubtful.

**Experiment.** In Sage, use an explicit degree-eight multiquadratic field for three bits, construct clause ideals for the eight-clause obstruction, emit its Minkowski lattice, and enumerate the nearest unrestricted vectors.

**Likely death.** Encoding \(n\) independent Boolean conjugate choices appears to require degree \(2^n\), while norm lower bounds alone are only constant.

---

### 5. Lossless-expander logarithmic bag list recovery
**Core trick.** Upgrade G14 from pair bags to \(k=\Theta(\log n)\)-variable bags selected by a deterministic splitter, and connect overlapping bags through a lossless expander. Full assignment marginals are retained; a list-recovery argument should turn any sufficiently low-anchor zero-residual state into one global Boolean assignment.

**Expected move.** Unsatisfiability then forces many expander-edge residuals, which can be weighted polynomially without affecting honest completeness.

**Obstruction check.** O1: no slack/carries. O2: expansion is intended to eliminate localized overlap circuits, but this is unproved for signed marginals. O3: all bag variables and edges form one unrestricted objective. O4: logarithmic bags escape fixed-degree parity. O5: needs a quantitative list-recovery bound strong enough relative to baseline. O6: G13 must become expensive in many isolating bags; otherwise O6 survives unchanged. O7: every dropped bag loses many normalization and overlap edges. O8: \(2^k\) is polynomial for fixed \(k/\log n\); unlike G14, an asymptotic composition theorem is explicitly required.

**Experiment.** Replace G14’s pair mesh by all four-variable bags on the current instance, then test padded copies with sparse expander interconnection and exact shell DP.

**Likely death.** Signed tables may agree on every overlap while remaining globally nonpositive, and charging them in every bag may still give only a constant ratio.

---

### 6. Reversible-verifier path lattice with no-backtracking weights
**Core trick.** Encode a reversible deterministic SAT verifier as a layered configuration graph whose honest lattice vectors are complete computation paths from an assignment state to acceptance. Couple forward and reverse edges with time-dependent weights so using an edge negatively, skipping a layer, or entering acceptance backward incurs a large uncancelled coordinate.

**Expected move.** Obtain a polynomial-size global consistency mechanism where acceptance cannot be synthesized from locally legal clause selectors.

**Obstruction check.** O1: no free carries; every transition variable is anchored and conserved. O2: global time flow replaces clause overlap, though short flow circulations are dangerous. O3: basis, target, conservation, and acceptance rows are all emitted. O4: verifier evaluates the full conjunction, not bounded moments. O5: the no-backtracking penalty must beat path baseline polynomially—unproved. O6: G13 cannot directly feed clause selectors, but affine combinations of complete computation paths may still pass. O7: dropping a transition breaks two conservation rows. O8: verifier graph is polynomial-size, but unrestricted signed-flow soundness is missing.

**Experiment.** Emit the complete reversible verifier graph for the three-variable obstruction and enumerate all unit flows through twice the honest path energy, explicitly allowing negative edges and cycles.

**Likely death.** An incidence lattice ignores orientation: signed flow can traverse transitions backward, and layer weighting may amplify honest and dishonest paths together.

---

### 7. Log-degree theta-body Gram synthesis
**Core trick.** Introduce squarefree monomials through degree \(k=\Theta(\log n)\), then search for a rational PSD Gram matrix whose null directions are exactly honest satisfying evaluations. Unlike G9/G11’s fixed metric, require an SOS/theta-body certificate covering every unrestricted integer vector, not merely an enumerated shell.

**Expected move.** A degree-\(k\) certificate would charge every parity kernel of support below \(2^k\); rational Cholesky realization gives the Euclidean CVP instance.

**Obstruction check.** O1: no slack; auxiliaries are explicit monomial coordinates. O2: all clauses share one global Gram form. O3: rational factor, center, and unrestricted basis must be emitted. O4: logarithmic degree is outside the killed fixed-degree mutation. O5: certificate must prove an \(N^c\) eigenvalue/distance law, currently absent. O6: G13 is included as a mandatory constraint, but triangle inequality may prevent separation. O7: every single- and multi-clause drop is included symbolically. O8: dimension is polynomial only for carefully sparse monomials; a full degree-\(\log n\) lift is quasipolynomial.

**Experiment.** Solve the exact rationalized SDP for the nine-clause instance using all degree-four monomials, then enumerate the unrestricted shell and padded disjoint copies.

**Likely death.** Either no separating Gram matrix exists because of short affine combinations, or polynomial-size sparsification destroys the SOS certificate.

Classical ingredient pointers only: Construction A—Conway and Sloane, *Sphere Packings, Lattices and Groups* (1999); splitters—Naor, Schulman, and Srinivasan (FOCS 1995); reversible computation—Bennett (1973); moment/SOS hierarchies—Lasserre (2001).
