I did not consult or use the prohibited document. These are deliberately independent, equal-status directions.

### 1. Weighted laminar marginal hierarchy

**Core trick.** Put full assignment selectors only on \(O(\log m)\)-variable blocks, pass complete boundary marginals through a laminar separator tree, and weight disagreements increasingly toward the root. Unlike complete pair bags, total baseline stays near \(m\operatorname{polylog}m\); deleting one clause should create a first inconsistent ancestor whose penalty dominates all lower-level anchor mass.

**Expected move.** Obtain squared soundness \(\Omega(Bm^{2c})\) from one contradiction without a quadratic baseline.

**Obstruction audit.** G1: no slack. G2–3: no fixed-marginal local isolation. G5: constraints cross levels, not private rows. G6: every row and weight is emitted; optimization is unrestricted. G7/G9/G11: not excluded—their affine kernels may lift through all separators. G12: clause dropping remains possible but should cross a weighted ancestor. G13: raw-72 linear hashing does not apply to enlarged bag variables, although an affine-span analogue may. G14/gate: this is an explicit weighted, near-linear mutation; alternative lifts and fully executable certificates remain required.

**Falsification/experiment.** For minimally unsatisfiable chains with \(m=8,16,32\), optimize every clause drop and G11-style signed lift by MILP.

**Likely death.** High-width formulas force superpolynomial boundaries, or pseudo-marginals thread the hierarchy.

---

### 2. Batch-code amplification of Booleanity and carries

**Core trick.** Encode global assignment bits and clause-slack symbols as balanced digits inside one explicit systematic batch/expander code. Give every queried literal many disjoint parity reconstructions, emit every carry as a lattice coordinate, and evaluate each clause through all reconstruction triples; corrupting one illegal slack symbol should then force many code-coordinate deviations.

**Expected move.** Replace G1’s constant-cost slack change by a growing code-distance charge while retaining zero residual for honest assignments.

**Obstruction audit.** G1: no free slack; carries are coded and charged. G2–3: no local selector isolation. G5: checks are global code constraints. G6: all digits, carries, and decoder equations are emitted. G7: not excluded—an exact carry/codeword bypass would kill it. G9/G11: their clause-selector parity kernels are absent, but analogous signed codewords may exist. G12: no standalone fingerprint; decoder-block deletion remains a risk. G13: the raw-selector linear-hash theorem is outside the nonlinear digit lift, but a linearized implementation may re-enter it. G14/gate: baseline is linear-code size rather than pair-quadratic; minimum-indegree clause drops still require testing.

**Falsification/experiment.** Build a small BCH/LDPC code for chain instances \(m=8,16,32\); exact-search coefficients and carries in \([-2,2]\), including single-symbol and clause-drop attacks.

**Likely death.** Alternative carries preserve the codeword, or sufficient batch multiplicity is itself PCP-like.

---

### 3. Cosystolic chain-complex encoding

**Core trick.** Represent occurrence deviations as cochains on a bounded-degree 2-complex: consistency residuals are coboundaries, while zero-residual selector cheats become cocycles. Cosystolic expansion attacks non-cocycles through many violated faces and attacks nontrivial cocycles through a growing support lower bound.

**Expected move.** Turn the constant-support G7/G9/G11 attacks into either a large residual or a large zero-residual support, furnishing a genuine composition invariant.

**Obstruction audit.** G1: no slack. G2–3: no isolated clause fiber. G5: topology couples overlaps globally. G6: boundary matrices, targets, and anchors are all explicit; SNF can audit mod-2 bypasses. G7: directly targeted as a short cycle, but not automatically excluded. G9/G11: their parity vectors become candidate cocycles and must be enumerated. G12: a drop becomes a chain with boundary, unless supported on a cocycle. G13: raw-selector hashing is inapplicable, but an honest-affine collision may represent a homology class. G14/gate: bounded degree gives linear baseline and removes canonical low-indegree pair bags; it does not itself prove sufficient expansion or optimize affine lifts.

**Falsification/experiment.** Decorate a small explicit triangulated complex with the nine clauses; compute integer homology/SNF and exact-search cochains in \([-2,2]\). Repeat on chain families.

**Likely death.** Predicate-compatible complexes retain short homology classes, or support growth yields only a constant distance ratio.

---

### 4. Tensor-powered spherical separation

**Core trick.** Treat the finite G9 Gram separator as a constant alphabet geometry, then tensor its feature map \(k\) times. If every harmful base state has normalized correlation at most \(\rho<1\), product states lose correlation as \(\rho^k\); expander-walk sampling could keep \(k=\Theta(\log N)\) tensor coordinates polynomial.

**Expected move.** Convert a certified constant finite ratio into \(N^c\), provided arbitrary integer vectors obey a tensor-product soundness theorem.

**Obstruction audit.** G1: no slack. G2–3: no local isolation. G5: tensor coordinates couple factors globally. G6: emit the rational Kronecker Gram/factor and optimize unrestricted integers. G7: its exact residual kernel remains a bad base state, not an invisible residual. G9: supplies only the seed separation, not composition. G11: include unique-triple parity among base bad states. G12: all features are tensorized rather than one clausewise tag; drops may nevertheless dominate. G13: this is a quadratic metric, not a compatible linear syndrome; affine collisions remain legitimate vectors. G14/gate: no complete pair baseline, but sparse-unsatisfaction and alternative entangled lifts remain unresolved.

**Falsification/experiment.** Construct tensor squares and cubes of the exact G9 shell-state Gram; use DP/branch-and-bound to compare product, mixed, drop, and unrestricted integer minima.

**Likely death.** “Entangled” integer vectors beat every product witness, or the needed expander argument is PCP in disguise.

---

### 5. Compressed Macaulay/Nullstellensatz moment lift

**Core trick.** Introduce global Boolean moments \(y_S\), and emit the Boolean ideal equations and every clause polynomial multiplied by selected monomials. Raise degree to \(d=\Theta(\log N)\), but compress monomials through deterministic perfect-hash colorings and exterior signs so sparse certificate supports are preserved in polynomial dimension.

**Expected move.** Propagate a uniquely occurring false clause algebraically across many global moments, rather than relying on another local occurrence for comparison.

**Obstruction audit.** G1: no integer slack. G2–3: no local affine fiber. G5: equations are global ideal consequences. G6: all moment rows and compression maps are emitted; no external pseudoexpectation filter. G7/G9: their signed kernels become low-degree pseudo-evaluations and are not automatically excluded. G11: specifically addressed by multiplying the unique clause equation by outside monomials. G12: no clause tag; dropping a clause may still admit a pseudo-evaluation. G13: the raw linear hash theorem is outside the nonlinear monomial lift, although affine pseudo-distributions remain. G14/gate: no pair-bag baseline, but dimension and drop soundness are unproved.

**Falsification/experiment.** For the nine-clause pair, build degrees \(1\)–\(6\), exact-search signed moment vectors, then test candidate hash compressions for collisions.

**Likely death.** General formulas require linear degree, and compression aliases precisely the high-degree certificate needed for soundness.

---

### 6. Discriminant-group lattice gluing

**Core trick.** Replace clause selectors by equal-radius cosets of a small base lattice \(L\subset L^\ast\), exposing variable values as symbols in the discriminant group \(D=L^\ast/L\). Glue occurrence symbols using a regular outer code over \(D\); any inconsistency then occupies a nonzero coset with a certified minimum norm, with no auxiliary carry variables.

**Expected move.** Make both local signed combinations and clause deletions create a dense nontrivial glue syndrome while keeping baseline \(O(m)\).

**Obstruction audit.** G1: no slack or carry. G2–3: legality is coset geometry, not fixed-marginal isolation. G5: the outer glue code is global and regular. G6: emit the actual glued-lattice HNF and fixed target; audit all quotient classes. G7: not excluded—an attack may have zero discriminant syndrome. G9/G11: raw parity selectors are absent, but their effect may induce the trivial coset. G12: no independent fingerprint; deletion should violate many glue checks but must be verified. G13: the raw-72 theorem does not literally apply, though abelian quotient linearity may recreate its affine collision. G14/gate: regular \(O(m)\) gluing avoids complete-pair indegree attacks; alternative coset lifts require exact optimization.

**Falsification/experiment.** Enumerate rank-\(\le6\) integral Gram matrices whose discriminant group contains \((\mathbb Z/2)^3\); assign eight labels and sphere-decode the nine-clause and chain instances.

**Likely death.** Abelian closure forces the forbidden eighth label whenever the seven legal labels are admitted.

Classical mechanism pointers only: Sherali–Adams (1990); Sipser–Spielman, *Expander Codes* (1996); Ishai et al., *Batch Codes* (2004); Impagliazzo–Zuckerman (1989); Evra–Kaufman (2016); Conway–Sloane, *Sphere Packings, Lattices and Groups* (1999).
