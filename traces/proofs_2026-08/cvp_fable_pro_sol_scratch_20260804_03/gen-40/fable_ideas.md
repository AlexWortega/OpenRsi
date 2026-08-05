All seven are speculative and deliberately nonconvergent. Each must pass an unrestricted-integer audit before promotion.

### 1. Coherent shared-block Gram synthesis

**Core trick.** Replace orthogonal clause/copy features by a single shared vector block whose cross terms are optimized by SDP. Honest global assignments need only be cospherical, while every known parity or DROP direction is required to accumulate coherently rather than additively.

**Expected move.** Obtain NO energy \(\Omega(m^{1+2c})\) against honest radius \(O(m)\), yielding distance ratio \(m^c\).

**Obstruction check.** G1/G7 slack and radix kernels are absent. G5/G19 private rows and flows are absent. G13 does not directly apply because honest images share a radius, not a common linear syndrome. G32/G37 are directly targeted: the Gram includes unrestricted cross-copy terms, unlike their orthogonal incidence family. G33/G34 concern only the frozen exterior tags. DROP (G12/G38) must be an explicit SDP constraint. G28/G30 are irrelevant. The G14/G31/G38 “finite shell only” objection remains until a scalable Gram formula is proved.

**Smallest experiment.** On the nine-clause pair, optimize a full rational \(72\times72\) Gram subject to equal radii for all 16 honest points, \(Q\succeq I\), and margins against every vector in the existing G31 shell plus the two-copy parity.

**Likely death.** Affine dependencies may imply an unknown universal quadratic cut extending G37.

---

### 2. Iterated Lawrence lifting and Graver-norm amplification

**Core trick.** Embed the formula’s consistency matrix into \(O(\log n)\) iterated Lawrence liftings, where primitive integer kernel moves can acquire rapidly growing norm. A satisfying assignment remains a unit-fiber point; an unsatisfiable zero-residual pseudosection should require a large Graver move, while nonzero residuals are polynomially weighted. This uses classical Lawrence/Graver geometry; see Sturmfels, *Gröbner Bases and Convex Polytopes* (1996).

**Expected move.** Prove minimum zero-residual anchor excess \(n^{\Omega(1)}\) with only polynomial rank and bit length.

**Obstruction check.** It directly replaces the failed local isolation of G2–G5 by a global integer-kernel claim. G1/G7 exact residual kernels are harmless only if their coefficient norm grows. It is **not automatically outside** G13/G15 or G19: their affine lift or signed splice may survive every Lawrence level, which is the primary falsifier. DROP receives a weighted normalization residual. G28/G30 and G33/G34 do not apply. G32/G37 additivity is avoided only if Graver norm genuinely grows under lifting. G14/G31/G38’s scaling objection remains until that theorem exists.

**Smallest experiment.** Apply one and two Lawrence lifts to the G38 matrix; use MILP/4ti2-style circuit enumeration to minimize anchor norm in the exact residual fiber for obstruction and control.

**Likely death.** Graver growth may occur only in irrelevant fibers, while the G13 pseudosection lifts with constant relative cost.

---

### 3. Integral unique-neighbor agreement on nonlaminar bags

**Core trick.** Put legal assignment functions on \(k=\Theta(\log n)\)-variable bags arranged by an explicit unique-neighbor expander, with complete restriction maps on overlaps. Seek an **integral signed-agreement theorem**: any normalized integral family of small \(\ell_2\)-norm whose restrictions agree must be a Dirac global assignment—not merely a real pseudodistribution. Expander-code intuition comes from Sipser–Spielman (1996), but the needed theorem is direct integer algebra, not an imported PCP theorem.

**Expected move.** Unsatisfiability forces either residual energy or signed-section norm \(n^{1/2+c}\).

**Obstruction check.** This extends G14/G38 beyond fixed pair/triple bags and differs from G15’s laminar tree. G13/G15 are not excluded by linearity alone; they are excluded only if the signed-agreement theorem is true. G5’s freed marginals are covered by many nonlaminar overlaps. G19 flows are absent. DROP violates many normalizations. G1/G7, G28/G30, and G33/G34 do not apply. G32/G37 additive copies are replaced by one global expander, but the fixed-shell objection remains without asymptotic proof.

**Smallest experiment.** Join two copies of the obstruction on eight variables, generate a fixed 3-regular bag-overlap graph with bags of three clauses, and MILP-search the shortest exact signed section.

**Likely death.** Möbius/parity signed measures may extend through every bag with norm only \(2^{O(k)}\), too small relative to construction size—or the theorem may effectively recreate PCP machinery.

---

### 4. Totally-real norm separator on tuple lifts

**Core trick.** Lift overlapping clause tuples, then assign their restriction defects algebraic-integer fingerprints in a totally real field of degree \(d=\Theta(\log n)\). Honest tuple systems give algebraic residual zero; any nonzero residual \(\alpha\) has positive integral trace norm \(\operatorname{Tr}(\alpha^2)\), which can be polynomially scaled without increasing honest radius.

**Expected move.** Reduce soundness to proving that every low-anchor harmful integer tuple system has a nonzero algebraic residual; amplification then follows arithmetically.

**Obstruction check.** G1/G7 and the prime-scaling criticism from G39 still apply to any exact kernel: number fields amplify nonzero residuals but never remove zero residuals. Thus G13/G15 remain fatal if their affine coefficients lift to the chosen tuples. G14/G38 suggest tuple lifts can break some such relations; G5 requires overlap-wide rather than private tags. G19 is irrelevant unless tuples are transition paths. DROP is charged by normalization before norm scaling. G32/G37 additivity is avoided only if one shared algebraic defect detects combined parity. G28/G30 and G33/G34 do not apply. Scaling remains unproved.

**Smallest experiment.** Add exact trace-form tags over \(\mathbb Q(2\cos(2\pi/11))\) to the G14 pair bags; enumerate all signed states through anchor excess 64 and test whether every nonhonest exact tuple system has positive trace norm.

**Likely death.** A G13-style exact tuple kernel survives, or the tuple width/field degree needed for separation becomes exponential.

---

### 5. E-type tensor amplification after Kannan homogenization

**Core trick.** Convert an inhomogeneous CVP seed into a shortest-vector problem by a carefully parameterized Kannan embedding, then self-tensor it. Seek a structural “E-type” theorem forcing every sufficiently short tensor to be decomposable, so a constant seed ratio \(\rho>1\) becomes \(\rho^k\) after \(k=\Theta(\log n)\) levels. Kitaoka’s *Arithmetic of Quadratic Forms* (1993) supplies classical E-type precedents, but not the required affine theorem.

**Expected move.** Polynomial dimension \(r^k\) and ratio \(n^{\log_r\rho}\).

**Obstruction check.** G30 killed an isometric seed, not tensor amplification for an asymmetric certified seed. G28’s min-plus recurrence is unrelated. G32/G37 additive parity is outside the intended multiplicative decomposition theorem—but remains a valid falsifier if parity tensors are short. G13/G19 signed vectors persist inside the seed and must already be above its gap. G1/G7 exact kernels and DROP can create short Kannan vectors and must be audited. G33/G34 are irrelevant. Unlike G14/G31/G38, this proposes an explicit recurrence, but no theorem currently validates it.

**Smallest experiment.** Kannan-homogenize the exact G31 obstruction/control pair, remove all seed isometries canonically, and enumerate rank-one versus rank-two coefficient tensors through the predicted two-level threshold.

**Likely death.** Kannan embeddings admit short last-coordinate-zero or entangled tensors; E-type control for homogeneous minima may not transfer to closest vectors.

---

### 6. Twisted integral cosystoles

**Core trick.** Encode consistency as a coboundary problem on an explicit bounded-degree 2-complex with a nontrivial integral local coefficient system. Satisfiable instances produce a short lift of the target cochain; unsatisfiable instances should represent a twisted class whose every integral representative has polynomial cosystolic norm. High-dimensional-expander constructions such as Lubotzky–Samuels–Vishne (2005) are possible host complexes.

**Expected move.** A deterministic integral filling inequality gives the polynomial CVP gap directly, without copy repetition.

**Obstruction check.** This is **not presently outside** G19: twisted chains are still signed chains after matrix emission, so a two-negative splice kills any candidate lacking an integral cosystolic theorem. G13/G15 affine pseudosections likewise become exact cocycles and must have provably large norm. G5 is addressed only if the complex has global expansion. G1/G7 residual amplification is secondary; the theorem concerns exact classes. DROP is the zero cochain and must be farther than completeness. G28/G30 and G33/G34 are irrelevant. G32/G37 additivity is avoided by a single global cosystole. G14/G31/G38’s finite-only objection remains until a formula-to-complex reduction is explicit.

**Smallest experiment.** Glue clause triangles for the nine-clause obstruction, enumerate small \(GL_2(\mathbb Z)\) edge monodromies, compute Smith forms, and exactly find the shortest representative of each twisted class.

**Likely death.** Short signed fillings persist, or constructing the required formula-sensitive expanding complex is essentially the forbidden gap-amplification problem in disguise.

---

### 7. Globally convex quadratization without selector fibers

**Core trick.** Abandon local one-hot selector systems. Quadratize the Boolean 3SAT energy using shared product ancillas, then search for a formula-global spectral repair making the entire quadratic form positive definite while adding a constant on the Boolean cube. Off-Boolean integers are controlled by strong convexity rather than normalization/slack rows.

**Expected move.** Find a repair whose honest radius grows only linearly while every unsatisfiable Boolean or non-Boolean point acquires \(n^{2c}\) additional squared energy.

**Obstruction check.** G1’s free slack is directly excluded only if unrestricted ancillas are certified; otherwise it reappears. G7/G13/G15 common-target selector collisions are outside the intended variable/product encoding, but affine identities among ancillas could recreate them. G5 and G19 do not apply. DROP becomes an off-cube integer point and is covered by the convexity bound. G32/G37 additivity remains a serious threat unless the repair has global cross-clause curvature. G28/G30 and G33/G34 are irrelevant. As with G14/G31/G38, a finite SDP pass alone gives no scaling theorem.

**Smallest experiment.** For the all-eight-clauses three-variable obstruction, enumerate standard quadratic ancilla substitutions, solve an exact/rationalized SDP for the minimum PSD repair, and exhaust all integer points in the eigenvalue-derived box against a satisfiable control.

**Likely death.** PSD repair may necessarily add baseline curvature comparable to the amplified clause penalty, collapsing the ratio to \(1+O(1/n)\).
