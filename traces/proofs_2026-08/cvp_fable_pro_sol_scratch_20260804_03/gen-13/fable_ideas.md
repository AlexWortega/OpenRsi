No external search or off-limits material was used. These are deliberately unranked mechanisms.

### 1. Construction-A gluing with bounded-sum-free label hashes

**Core trick.** Assign every clause label a vector from a \(B_h\)-type set over \(\mathbb F_p^r\), then glue occurrences through a Construction-A lattice. Within the relevant norm shell, distinct short signed label combinations should have distinct syndromes, while honest consistent labels share a prescribed coset.

**Expected move.** A parity substitution or deleted clause acquires a nonzero torsion syndrome that can be weighted by \(n^{O(1)}\).

**Obstruction audit.** G1 RS slack: no slack variables. G2 bounded and G3 exact affine isolation: this is a global bounded-sum code, not fixed local marginals. G5 private-row overlap: full labels are glued, not merely shared marginals. G6 quotient invalidity: every congruence becomes an emitted lattice coordinate with one fixed target. G7 radix kernel: not escaped globally—any short zero hash kills it. G9 quadratic parity and G11 unique-cubic parity: choose \(h\ge7\) and include those signed sums in the collision prohibition. G12 clause drop: an affine normalization hash makes zero versus one label distinct.

**Experiment/falsification.** On the 72-selector instance, SAT-search \(p,r\) and hashes separating every shell vector through squared cost 108; then run exact DP. A collision or cheaper Construction-A lift falsifies it.

**Likely death.** Required \(h,p,r\) may grow too rapidly for polynomial dimension.

---

### 2. Coboundary-expanding complex for selector deviations

**Core trick.** Regard occurrence inconsistencies as integer cochains on a bounded-degree 2-complex covering the formula incidence graph. Emit boundary and coboundary operators as lattice coordinates; coboundary expansion should force any seeded defect to occupy many coordinates unless it is genuine homology.

**Expected move.** One false clause creates a defect of polynomial support, after which polynomial weighting yields the desired distance gap.

**Obstruction audit.** G1 RS slack: no residual slack exists. G2/G3 affine isolation: the certificate is global and topological, not a fixed local fiber. G5 private overlap: cells couple whole neighborhoods across clauses. G6 external filters: all conservation equations and targets are emitted. G7 exact radix kernel: not escaped—an integral cocycle or boundary with zero syndrome is fatal. G9 degree-two parity and G11 unique-cubic parity become small cycles; the mechanism works only if the chosen complex expands them. G12 clause drop has nonzero boundary because normalization is a 0-cell constraint.

**Experiment/falsification.** Attach the smallest candidate complex to the nine-clause graph; enumerate integral cochains of support at most seven and compute Smith normal form. Any parity/drop witness in kernel falsifies it.

**Likely death.** Formula defects may be boundaries, and constructing the necessary expansion may amount to forbidden PCP machinery.

---

### 3. Segre-style pair lift with joint clause selectors

**Core trick.** For edges of a bounded-degree expander on clauses, introduce \(8\times8\) joint-label selectors and enforce their two projections onto the original clause selectors. This linearizes a low-level Segre/product consistency condition: changing one local signed distribution must be lifted through all neighboring transportation tables.

**Expected move.** Cheap local parity or deletion attacks propagate to linearly many joint blocks while dimension remains polynomial.

**Obstruction audit.** G1 RS slack: there are no slacks. G2/G3 local isolation: no local-isolation assumption is used. G5 private overlap: edges compare complete labels, not only variable marginals. G6 quotient failure: projection, normalization, and consistency rows are all lattice coordinates with a fixed reference. G7 exact radix kernel: not escaped; an integral signed transportation circulation kills the proposal. G9 quadratic parity and G11 unique-cubic parity are outside the moment-only assumptions, but may still admit joint lifts. G12 clause drop violates every incident joint normalization, rather than losing one homogeneous tag.

**Experiment/falsification.** Put the nine clauses on a 3-regular multigraph, add 576 joint variables per edge, and use MILP plus exact shell verification to minimize the emitted quadratic objective.

**Likely death.** Signed transportation tables may lift every zero-mass marginal attack with only constant cost.

---

### 4. Totally real number-field norm moat

**Core trick.** Encode global selector syndromes as algebraic integers \(\alpha=\sum_i z_i\beta_i-\tau\) in a totally real field and append their full Minkowski embeddings via the trace Gram matrix. If \(\alpha\neq0\), the product formula and AM–GM give \(\sum_\sigma \sigma(\alpha)^2\ge [K:\mathbb Q]\), which can be polynomially weighted.

**Expected move.** Replace evaluation spreading by a genuine algebraic-integrality lower bound with no carry or slack directions.

**Obstruction audit.** G1 RS slack is outside because the norm is applied directly to a slack-free integral syndrome. G2/G3 local isolation and G5 private overlap are outside because \(\beta_i\) encode global labels. G6 external filters are avoided by emitting the exact trace form and fixed target. G7 exact kernel remains fatal if \(\sum z_i\beta_i=0\). G9 parity and G11 unique-cubic parity are detected only if the selected \(\beta_i\) are independent on those supports. G12 drop is detected by including a nonzero constant-bias basis element.

**Experiment/falsification.** In Sage, search a degree-16 totally real field and fingerprints separating the known parity/drop shell; emit the exact trace Gram and rerun DP.

**Likely death.** Equal completeness radius may conflict with algebraic independence, or required field degree may be too large.

---

### 5. Expander-walk tensor powering of a finite gap gadget

**Core trick.** Replace independent repetition by joint selectors indexed by length-\(k\) walks on a constant-degree expander over clause gadgets. Design the quadratic form as a walk-tensor product so completeness follows an honest assignment, while a local defect contaminates many correlated walk coordinates.

**Expected move.** If a genuine product inequality gives ratio \(g^k\), then \(k=\Theta(\log n)\) yields a polynomial gap with polynomially many walks.

**Obstruction audit.** G1 RS slack: repetition contains no slack. G2/G3 local isolation and G5 private overlap: coupling is global along walks. G6 external filtering: every transition and projection is emitted against one target. G7 radix kernel is not escaped—exact base kernels tensor to exact product kernels. Likewise G9 constant parity and G11 unique-cubic parity are inherited central falsifiers, not assumed away. G12 clause drop is outside the single-tag setting because every walk meeting the clause is charged, provided the product equations prevent rerouting.

**Experiment/falsification.** Build the \(k=2\) walk product of the nine-clause obstruction and control; compute exact minima by transfer-matrix DP rather than full enumeration. Failure to exceed the square of the base ratio kills multiplicativity.

**Likely death.** Inhomogeneous CVP distances may not tensor, and a successful theorem may effectively be prohibited parallel repetition/PCP.

---

### 6. Nullstellensatz certificate as a CVP dual separator

**Core trick.** Form a degree-\(d\) Macaulay system for clause polynomials and \(x_i^2-x_i\). For an unsatisfiable formula, seek an identity \(1=\sum_C q_C f_C+\sum_i r_i(x_i^2-x_i)\), then translate its coefficients into a dual vector certifying that every sufficiently close lattice vector has nonzero weighted residual.

**Expected move.** A global algebraic certificate could rule out all signed-selector kernels simultaneously rather than cataloguing local attacks.

**Obstruction audit.** G1 RS slack: the certificate includes Boolean equations and has no free slack. G2/G3 local isolation and G5 private overlap: the identity is formula-global. G6 external filters: every monomial relation must be emitted in the Macaulay lattice with an unchanged target. G7 exact kernel is excluded only if the selector-to-moment linearization faithfully pairs with the identity; otherwise it remains fatal. G9 quadratic parity and G11 unique-cubic parity are outside only when \(d>3\). G12 clause drop violates the constant/normalization component.

**Experiment/falsification.** Compute the minimum rational certificate degree for the nine-clause instance, clear denominators, build the corresponding moment lattice, and audit the known attacks plus the exact shell.

**Likely death.** General formulas may require exponential degree, monomial count, or coefficient norm.

Classical ingredients referenced: Bose–Chowla, “Theorems in the additive theory of numbers,” *Commentarii Mathematici Helvetici* 37 (1962/63); Sipser–Spielman, “Expander Codes,” *IEEE Transactions on Information Theory* 42 (1996).
