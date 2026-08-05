Any positive finite result below remains **FINITE** until its certificate is checked in Lean. No ranking is intended.

### 1. Generic skew-product avoidance

**Mechanism.** Compute the complete projected-fiber Markov basis \(G\). Parameterize pair tags by \(a_j,b_k\in\mathcal O/P^2\), with initial transfer
\[
F_g=\sum_{j,k}g_{jk}\,\bar a_j\,\sigma^{r(j,k)}(\bar b_k)\in P/P^2.
\]
Search simultaneously for a saturated COPY tile, common legal energy, and an assignment making every bad \(F_g\), false fiber, and DROP nonzero.

**Expected move.** A proof-carrying assignment would establish Q1 after Lean verifies the Markov-generation and arithmetic certificates.

**Falsification/experiment.** Dump the current \(N=8\) seam to `4ti2`; enumerate all rank-2–8 COPY signatures and solve the finite \(\mathbb F_{289}\) constraints by SAT. Death: legal equalities force some \(F_g=0\), or the alphabet is too small.

**Audit.** G1/G6/G7: no slack, filter, or radix. G2/G3/G5/G9/G11/G13/G15/G19/Goal G1/fresh toric exchange: escaped only if the **complete** enlarged Markov basis passes. G12/Goal G8: zero and DROP included. G14/G28/G31/G32/G37/G38: no scaling inference. G30: no tensor seed. G33/G34/Goals G3/G4/G5/G6/G7 and Goal G2: no killed geometry or \(A_5\) ring. Goals G11/G12/killed affine COPY: old witnesses are explicit constraints. Carry/lumpability: enumerate every \(P^3\) lift.

---

### 2. Universal toric-syzygy refutation

**Mechanism.** Treat all possible product tags as indeterminates and impose the legal-fiber/COPY equations in a polynomial ideal \(J\), including field equations. Search for a non-honest primitive \(g\) whose universal transfer polynomial satisfies \(F_g\in\sqrt J\); a Nullstellensatz certificate would show that **every** Q1 product-tag assignment kills that move.

**Expected move.** Refute the stated Q1 architecture and justify amending the roadmap from pair products to degree-three or history-bearing selectors.

**Falsification/experiment.** In Macaulay2/Singular, build \(J\) for the smallest `false111-COPY11-false111` seam and request membership certificates for its exchange polynomial. Lean can verify the resulting polynomial identity. Death: the displayed exchange is separable and no universal bad syzygy appears.

**Audit.** G1/G6/G7 and G12/Goal G8 are included as emitted-variable and DROP equations. G2/G3/G5/G9/G11/G13/G15/G19/Goal G1/fresh toric exchange are not assumed away: they generate candidate syzygies. G14/G28/G31/G32/G37/G38 and G30 are irrelevant because this refutes Q1 before recursion/tensoring. G33/G34/Goals G3/G4/G5/G6/G7 and Goal G2 use absent families. Goals G11/G12/killed affine COPY are the base witnesses. Carry/lumpability cannot rescue a universally zero initial class.

---

### 3. Quaternionic commutator-area tag

**Mechanism.** Label each left/right selector by two residues and emit both product coordinates \(a_jb_k\) and \(b_ka_j\). Their difference is a quaternionic commutator, the analogue of Heisenberg symplectic area: it vanishes on calibrated honest COPY pairs but can detect the affine `111` splice despite identical ordinary marginals.

**Expected move.** Produce an explicit nonzero \(P/P^2\) symbol for every non-honest primitive while retaining the surviving NAND energies and saturation.

**Falsification/experiment.** Search labels in \(\mathbb F_{17}^2\) for the current \(N=8\) NAND and the smallest saturated COPY code; enumerate the enlarged Graver basis and both orientations. Death: an isotropic primitive has zero commutator area, or legal calibration forces all labels into a commutative subfield.

**Audit.** G1/G6/G7: all commutators are emitted coordinates. G2/G3/G5/G9/G11/G13/G15/G19/Goal G1/fresh toric exchange: commutators are genuinely bilinear, but escape is claimed only after full Graver testing. G12/Goal G8: include DROP. G14/G28/G31/G32/G37/G38: no all-depth claim. G30: no tensoring. G33/G34/Goals G3/G4/G5/G6/G7 and Goal G2: no exterior-shell, \(D_4/E_6\), or group-ring assumptions. Goals G11/G12/killed affine COPY: test their exact vectors. Carry/lumpability: exhaust \(P^3\) representatives.

---

### 4. Second-compound rank detector

**Mechanism.** Replace each seam edge by joint selectors and attach a compressed second-compound tag \(u_j\wedge v_k\), mapped linearly into \(P/P^2\). Honest fibers are calibrated rank-one couplings; a signed splice that necessarily raises coupling rank should acquire a nonzero Plücker defect.

**Expected move.** Prove Q1 by finding a small representable matroid whose compound map separates every bad projected-fiber primitive.

**Falsification/experiment.** Use labels \(u_j,v_k\in\mathbb F_{17}^4\); SAT-search the \(6\)-coordinate wedge tags against the exact current Markov basis, then rebuild the enlarged basis to detect fake joint selectors. Death: a bad primitive is decomposable/rank-one or two bad compounds cancel.

**Audit.** G1/G6/G7: joint variables and constraints are emitted. G2/G3/G5/G9/G11/G13/G15/G19/Goal G1/fresh toric exchange: degree-two joint data lie outside old affine grading, conditional on re-auditing the enlarged Graver basis. G12/Goal G8: DROP tested. G14/G28/G31/G32/G37/G38: no finite-to-growth promotion. G30: no seed isometry. G33/G34: unlike the killed exterior tags, no shared cospherical completeness is required; Goals G3/G4/G5/G6/G7 and Goal G2 are unused. Goals G11/G12/killed affine COPY: exact witnesses included. Carry/lumpability: all \(P^3\) lifts checked.

---

### 5. Toric normalization and conductor class

**Mechanism.** Compute the affine semigroup \(S\) generated by honest joint NAND/COPY columns and its normalization \(\bar S\). If adverse splices are holes with nonzero class in a finite conductor or divisor-class quotient, emit that class through Construction-A-style congruence coordinates and map its \(17\)-primary part to \(P/P^2\).

**Expected move.** Either obtain a canonical transfer invariant independent of label choices, or refute this route by showing signed group completion annihilates every hole class.

**Falsification/experiment.** Feed the smallest seam matrix to Normaliz; enumerate \(\bar S\setminus S\) below the false-`111` energy and compute its class group and \(17\)-torsion. Death: unrestricted negative coefficients trivialize the conductor class—currently the likeliest outcome.

**Audit.** G1/G6/G7: congruences must be emitted, not filtered. G2/G3/G5/G9/G11/G13/G15/G19/Goal G1/fresh toric exchange: **not escaped** unless the class survives signed completion and the complete Graver basis. G12/Goal G8: zero/DROP classes included. G14/G28/G31/G32/G37/G38: no amplification claim. G30 absent. G33/G34/Goals G3/G4/G5/G6/G7 and Goal G2 absent. Goals G11/G12/killed affine COPY are direct test holes. Carry/lumpability requires class stability for every \(P^3\) lift.

---

### 6. Divided-power covariance code

**Mechanism.** Assign each selector a vector \(v_j\in\mathbb F_{17}^m\) and attach degree-two divided-power moments. The defect
\[
\sum_j c_jv_j^{[2]}-\Big(\sum_jc_jv_j\Big)^{[2]}
\]
vanishes on honest one-hot fibers but can detect normalized affine pseudosections; pair selectors linearize its cross terms, which are then embedded in the quaternionic graded component.

**Expected move.** Find a small Veronese/BCH-style alphabet separating the entire bad Markov basis, not merely `111`.

**Falsification/experiment.** For \(m=2,3\), SAT-search labels for the current NAND plus smallest COPY, then recompute the enlarged Graver basis. Death: a degree-two design or cube-parity primitive annihilates every covariance coordinate.

**Audit.** G1/G6/G7: no slack/filter/radix. G2/G3/G5/G9/G11/G13/G15/G19/Goal G1/fresh toric exchange: the map is quadratic rather than old-affine, but only a complete Graver pass establishes escape. G12/Goal G8: DROP included. G14/G28/G31/G32/G37/G38: finite separation is not called growth. G30 absent. G33/G34/Goals G3/G4/G5/G6/G7 and Goal G2 use unrelated families. Goals G11/G12/killed affine COPY: their exact pseudosections are mandatory tests. Carry/lumpability: verify divided-power symbols for every \(P^3\) section.

---

### 7. Tropical unique-initial-term test

**Mechanism.** Write candidate tag valuations as \(\alpha_j+\beta_k\). Require each bad Graver move to have a unique lowest-valuation product term, making cancellation impossible in the associated graded ring; legal fibers impose valuation ties. This becomes a finite disjunctive linear system.

**Expected move.** A feasible integer solution gives a very simple Q1 certificate. An infeasibility/Farkas certificate proves that rank-one valuation tags are necessarily homogeneous on some toric exchange, justifying residue-level or higher-order amendment.

**Falsification/experiment.** Solve the exact MILP for the current Markov basis with bounded \(\alpha,\beta\), then extract either exponents or an infeasible cycle; verify the inequalities in Lean. Death: the rectangular `111` exchange forces equal sums on all four terms.

**Audit.** G1/G6/G7 and G12/Goal G8 are explicit constraints. G2/G3/G5/G9/G11/G13/G15/G19/Goal G1/fresh toric exchange are not presumed escaped; the MILP directly tests them and may refute the mechanism. G14/G28/G31/G32/G37/G38 and G30 occur only later. G33/G34/Goals G3/G4/G5/G6/G7 and Goal G2 are unused. Goals G11/G12/killed affine COPY supply mandatory inequalities. Carry/lumpability is avoided only when the minimum is unique; ties require complete \(P^3\) enumeration.

---

### 8. Lean proof-carrying Q1 certificate

**Mechanism.** Define a Lean structure containing the integral NAND/COPY matrices, targets, Gram forms, saturation witnesses, finite projected-fiber basis, quaternion multiplication tables, and transfer values. Prove a theorem: conformal generation by the listed moves plus certified fiber minima implies all four clauses of Q1.

**Expected move.** Turn a successful search into the only permitted beyond-FINITE result: a kernel-checked Q1 theorem rather than another empirical pass.

**Falsification/experiment.** First formalize the existing \(N=8\) NAND determinant, legal energy \(8\), false energies \(160,64,56,56\), and the explicit affine `111` witness; then add a two-state COPY toy and prove the theorem rejects its splice. Death: formal conformal-generation or exact minimum certificates become larger than the candidate itself.

**Audit.** G1/G6/G7 are excluded by checking the actual emitted lattice. G2/G3/G5/G9/G11/G13/G15/G19/Goal G1/fresh toric exchange are covered by certified complete primitive generation, not named testing. G12/Goal G8 are explicit fibers. G14/G28/G31/G32/G37/G38 remain later lemmas; no inference is made. G30, G33/G34, Goals G3/G4/G5/G6/G7, and Goal G2 are unused. Goals G11/G12/killed affine COPY are regression theorems. Carry/lumpability requires quantified \(P^3\)-lift checks.

Classical tools invoked only: Graver bases, toric ideals, binomial-ideal certificates, affine-semigroup normalization, and divided powers.
