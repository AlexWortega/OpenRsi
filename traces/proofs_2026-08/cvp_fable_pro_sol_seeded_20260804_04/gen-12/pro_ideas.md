Obstruction labels below: **O1 bounded local signatures; O2 marginal/tableau encodings; O3 local-view hierarchies; O4 phase lifts; O5 integer exact fibers; O6 complete-assignment fingerprints; O7 tensor amplification; O8 exact syndrome-to-CVP transfer.**

### 1. Laurent-product integrality certificate
**Core trick.** For each first-part vertex \(a\), form  
\[
f_a(U,V)=\sum_{(a,b,c)}z_{abc}U^bV^c,\qquad F_z=\prod_a f_a .
\]
In the Laurent polynomial ring, \(F_z=U^{\sum b}V^{\sum c}\) iff every \(f_a\) is a monomial; together with the three incidence equations, this exactly characterizes a signed perfect matching.

**Expected move.** Obtain a zero-baseline global defect: legal matchings all produce the same monomial, while every signed nonmatching produces extra coefficients.

**Map check.** O1: degree \(q\), genuinely global. O2: no marginals unless compiled as an arithmetic tableau—then O2 applies. O3: no scopes. O4: no phases. O5: nonlinear product, outside affine/count slacks. O6: no assignment columns, although coefficient space may explode. O7: not tensor amplification; all mixed lifted products still require checking. O8: applies only after polynomial-rank binary linearization.

**Experiment/falsification.** For \(q=2,3\), enumerate \(z\in[-2,2]^m\), compute coefficient vectors \(F_z\), their mixed span, all-eight and holonomy minima, and rank. Kill if an illegal mixed word hits the target monomial or rank grows exponentially.

**Likely death.** Any polynomial arithmetic-branching-program linearization reintroduces tableau splicing; direct coefficient expansion has tensor-rank growth.

---

### 2. Growing noncommutative PIT fold
**Core trick.** Canonicalize generator columns \(g_i\), assign each \(g_i\) several generic full-rank matrices \(X_i^{(s)}\in M_r(\mathbb F_{2^k})\), and fold tensor coordinate \((i,j)\) to the coefficients of \(X_i^{(s)}X_j^{(s)}\). Concatenate a deterministic noncommutative-PIT evaluation family and encode each nonzero matrix block by a simplex inner code.

**Expected move.** Compress \(m^2\) coordinates to \(\operatorname{poly}(r,k)\) while a hitting-set argument prevents every low-weight NO mixed matrix from vanishing.

**Map check.** O1: map acts on global generator types, not Boolean local views. O2: no wire interfaces. O3: no scopes. O4: no phases. O5: binary construction. O6: polynomial sparse dictionary, not assignments. O7: exactly the surviving code-dependent dense-fold opening, not puncturing or a pure catalyst. O8: applies directly; report binary rank, not nominal block count.

**Experiment/falsification.** On existing \(m=8\) families, use \(r=2,3\), all field matrices from a frozen seed family, and enumerate every mixed word, all-eight, holonomy, relabelings, worst YES, best NO, and exact rank. Kill on a pointed kernel or exponent below the unfurled square.

**Likely death.** PIT protects nonzeroness, while simplex conversion flattens support; low-rank NO words may survive in only one block.

---

### 3. Canonical ellipsoidal preconditioning of the integer fiber
**Core trick.** For \(Az=\mathbf1\), compute the analytic center and Hessian of the fractional matching polytope, then use a rational PSD Gram matrix \(Q(A)\) that heavily weights kernel directions approaching nonintegral faces. Realize \(z^TQz\) by an explicit sum-of-squares integer embedding.

**Expected move.** A YES matching should remain moderately short, while every signed NO exact-fiber point—although only two units worse in ordinary norm—could be polynomially longer in the instance-dependent Mahalanobis metric.

**Map check.** O1: no local signature. O2: no tableau. O3: no scopes. O4: no phases. O5: outside its residual-row scaling model because the coefficient norm itself is globally preconditioned; its constant repair may nevertheless remain short. O6: no assignment fingerprints. O7: no tensoring. O8: not automatically applicable because this is direct Euclidean CVP; any binary conversion needs separate proof and rank accounting.

**Experiment/falsification.** For all tiny 3DM instances, compute a log-barrier Hessian, rationally round it, enumerate signed exact points, and optimize \(\lambda\). Include all-eight/holonomy-derived fibers and every lattice combination. Kill if worst YES grows as fast as best NO, bit complexity explodes, or \(Q\) has superpolynomial realization rank.

**Likely death.** Nearby signed repairs probably remain nearby under every efficiently computable ellipsoid that cannot recognize integrality.

---

### 4. Formula-dependent nonabelian sheaf
**Core trick.** Put a small nonabelian representation on the incidence complex and define transport along canonical global paths, not edge-local phases. A satisfying assignment yields a sparse flat section in one representation sector; inconsistent holonomy should create a cosystolic defect spread by an expander sheaf.

**Expected move.** Noncommuting path products may prevent the support-three and odd-XOR cancellations that defeat scalar phases and ordinary homology.

**Map check.** O1: outside only when columns contain full global path words; a local transport table is covered. O2: direct global block rows avoid marginals; gate compilation does not. O3: paths span the whole graph. O4: formula-dependent, multivalued nonabelian selectors are outside the single-valued copy-stable coboundary theorem. O5: binary, not integer fibers. O6: fibers are representation coordinates, not assignments. O7: no tensor product; all mixed sections still need cosystolic soundness. O8: applies after explicit binary expansion, with representation dimension included.

**Experiment/falsification.** Freeze \(S_3\) or \(D_8\), enumerate path-label rules on all-eight and twisted holonomy, build the full binary generator, and enumerate every pointed mixed section. Require universal completeness over every satisfying assignment and positive NO distance.

**Likely death.** Universal completeness may force the global transports to be gauge-equivalent to trivial ones; regular representations also create large cancellation sectors.

---

### 5. Toric Gröbner filtration of exact covers
**Core trick.** Treat the 3DM incidence matrix as a toric semigroup and compute a code-dependent Gröbner degeneration of its toric ideal. Represent columns by sparse multiplication operators on standard monomials up to filtration \(K\); legal squarefree matching factorizations should stay in filtration zero, while signed nonmatching factorizations should cross many initial-ideal layers.

**Expected move.** Convert integrality defect into filtration distance without enumerating matchings, potentially yielding a sparse global algebraic dictionary.

**Map check.** O1: normal form is global and unbounded-degree. O2: no bounded-fan-in transcript if multiplication operators are written directly. O3: no local scopes. O4: no phases. O5: outside affine polynomial-count slacks; the invariant is toric normal-form depth. O6: standard monomials are not complete assignments, but their count may be exponential. O7: no ordinary tensoring; arbitrary mixed operator words must be tested. O8: applies once operators are converted to a polynomial-rank binary syndrome system.

**Experiment/falsification.** In Sage/Macaulay2, compute toric ideals for \(q=2,3,4\), enumerate Laurent signed covers, and measure normal-form depth plus multiplication-module rank. Explicitly attack all-eight, holonomy, and affine mixed combinations.

**Likely death.** Low-degree Markov moves probably connect illegal covers to legal filtration cheaply; otherwise the standard-monomial module likely becomes exponential.

---

### 6. Sparse-defect permutation sketches with list recovery
**Core trick.** Prove first that any signed row-sum-one table of squared norm at most \(q+2K\) differs from some permutation on only \(O(K)\) rows. Use splitters and list-recoverable Reed–Solomon sketches to describe those exceptional rows, sharing one selector across all three pair projections rather than paying the \(3q\) table baseline.

**Expected move.** Legal permutations receive a polylogarithmic selector representation; every low-excess nonpermutation violates many outer-code blocks, while already-heavy points need no shell.

**Map check.** O1: a genuinely global list-recovery selector is outside bounded-degree signatures; linear sketches alone are not. O2: ordinary hashed marginals have rectangle kernels, so the nonlinear global selector is essential. O3: no scope hierarchy. O4: no phases. O5: aims to remove, rather than rescale, the table baseline. O6: sketches permutations, not assignments, but information-theoretic description length is a danger. O7: no tensoring. O8: applies only if the selector union has an explicit fixed-target binary linear realization.

**Experiment/falsification.** For \(q=3,4\), enumerate all signed tables in \([-2,2]\), nearest permutations, frozen splitters, and the complete mixed selector span; then test 3DM all-eight and holonomy instances.

**Likely death.** Compressing all \(q!\) permutation choices into sparse fixed-target linear sectors may be impossible; rectangle superpositions may return immediately.

---

### 7. Asymmetric voltage lift of 3DM
**Core trick.** Lift each triple by permutations of a deck group \(G\), but target only selected Fourier/character syndromes rather than all sheets. A perfect matching consists of disjoint edges, so its sheet labels can be chosen independently; a colliding odd cover creates voltage cycles whose nontrivial holonomy should activate many expander-code character blocks.

**Expected move.** Amplify collision defects without multiplying the YES support by \(|G|\), unlike ordinary sheet replication.

**Map check.** O1: global voltage-cycle signatures are high-degree; edge-local versions remain vulnerable. O2: no proper marginals if character rows are direct. O3: full lift cycles are global. O4: graph-dependent, multivalued sheet choices fall outside the proved single-valued phase theorem, though they are very close to it. O5: binary. O6: no assignment fingerprints. O7: not a pure tensor catalyst or puncture; every mixed lifted cover must be bounded. O8: directly applicable with rank equal to retained character rows.

**Experiment/falsification.** Use \(G=\mathbb Z_3,S_3\), enumerate all voltage assignments for the all-eight and twisted \(q=3\) dictionaries, build exact syndrome matrices, and enumerate every mixed word. Require sparse lifts for every matching, no pointed kernels, and improved rank exponent.

**Likely death.** Independent sheet choices may recreate support-three splices; enforcing global sheet coherence risks the phase-coboundary theorem or a \(|G|\)-sized YES baseline.
