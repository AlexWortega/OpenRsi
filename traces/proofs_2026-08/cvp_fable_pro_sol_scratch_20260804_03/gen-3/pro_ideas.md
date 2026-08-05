I use the current obstruction map:

- **O1 — Free-slack annihilation:** residual-only amplification, including algebraic-number or multi-prime variants, vanishes through integer slack.
- **O2 — Bounded affine isolation:** the Generation-2 survivor may be a `[-3,3]` artifact.
- **O3 — Composition:** overlapping clauses may admit correlated signed kernel moves.
- **O4 — Sparse unsatisfaction:** one violated clause yields only constant local cost.
- **O5 — Missing CVP accounting:** no explicit basis, target, radii, or dimension-gap law.
- **O6 — Legality/scaling:** the construction must be deterministic, polynomial-size, unconditional, and PCP-free.

### 1. Modular wraparound barrier

**Mechanism.** Replace bounded affine isolation by an exact congruence: choose a prime \(q\) and measurements injective on harmful selector moves modulo \(q\). Any surviving integral cheat must then “wrap around,” forcing some coefficient or charged carry to have magnitude at least \(q\).

**Expected move.** Set \(q=n^\alpha\), obtaining polynomial soundness from a single harmful block without replicating residuals.

**Obstruction check.** **O1:** outside its assumptions because carries and selector deviations—not merely residuals—are charged. **O2:** modular injectivity and the minimum wraparound vector can be certified unboundedly by Smith/Hermite normal form plus exact CVP enumeration. **O3:** not escaped; shared-variable moves may cancel syndromes across blocks. **O4:** escaped if every nonzero global cheat requires a \(q\)-sized wrap. **O5:** congruences have a direct integer-lattice realization, but radii remain to be supplied. **O6:** \(q\) has polynomial bit length; no conjecture or PCP is needed.

**Falsification.** Find an \(O(1)\)-norm integral move with zero global syndrome.

**Smallest experiment.** Compute exact unbounded minima for the 18 survivors, then augment one with \(q=5,7\) congruence rows and enumerate the two-overlapping-clause lattice exactly.

**Likely death.** Rank deficiency produces \(q\)-independent correlated kernel vectors.

---

### 2. Encode the entire defect transcript

**Mechanism.** Let \(d\) contain every normalization, marginal, Booleanity-lift, and clause defect—never a free slack coordinate—and map it through a systematic linear code \(Gd\). A nonzero transcript then has many nonzero integral coordinates, while completeness has \(d=0\).

**Expected move.** A polynomial-length concatenated code could turn one nonzero defect into \(n^\alpha\) squared cost.

**Obstruction check.** **O1:** outside residual-only amplification because every escape direction is included in \(d\). **O2:** exact integer-kernel computation, not coefficient boxes, tests whether \(d\) can vanish. **O3:** global coding sees cross-clause cancellation only if it leaves a nonzero total transcript; exact signed zero-transcripts remain dangerous. **O4:** code distance amplifies one nonzero defect. **O5:** \(G\) is an explicit integer block in a CVP basis, though completeness anchors and final radii are unresolved. **O6:** explicit expander or concatenated codes are deterministic and polynomial-size, but the consistency layer must not smuggle in a PCP theorem.

**Falsification.** Exhibit a signed integral selector assignment with \(d=0\) for an unsatisfiable formula.

**Smallest experiment.** Build the full transcript for the all-eight-clause instance, encode it with a small systematic code, and solve the resulting unbounded integer minimum exactly.

**Likely death.** The affine relaxation has exact signed zero-defect points, which no code can amplify.

---

### 3. Totally-real algebraic norm amplification

**Mechanism.** Place each Booleanity or clause equation in a totally real number field of degree \(D\), and include all conjugate embeddings. For a nonzero algebraic integer \(\alpha\), \(|N(\alpha)|\ge1\); AM–GM then forces the sum of squared conjugate magnitudes to be at least \(D\).

**Expected move.** Taking \(D=n^\alpha\) amplifies even one nonzero equation, provided multiplication consistency is enforced without slack.

**Obstruction check.** **O1:** outside the killed form because Booleanity and multiplication-consistency equations are amplified too, in separate field components; no unamplified slack is allowed. **O2:** algebraic-integer ideals and trace forms permit exact, unbounded computation. **O3:** direct-summing equations prevents inter-clause conjugate cancellation, but fake lifted moments may make every equation zero. **O4:** one nonzero component already costs \(\Omega(\sqrt D)\). **O5:** an integral trace Gram matrix is explicit, but converting it to standard rational Euclidean CVP with controlled distortion is unresolved. **O6:** explicit fields can be polynomial-size; no conjecture is intended.

**Falsification.** Find a non-Boolean integral Veronese lift annihilating all amplified equations.

**Smallest experiment.** In Sage/PARI, use degrees \(2,4,6\) on the all-eight-clause formula, construct trace Gram matrices, and enumerate lifted integral cheats.

**Likely death.** Linearized multiplication admits exact pseudo-moments, or Euclidean realization destroys the norm bound.

---

### 4. Homogenized tensor powering

**Mechanism.** First homogenize a CVP instance so candidate differences appear as vectors \((Bz-t,1)\). Tensor \(k\) copies, hoping that YES witnesses tensor to norm \(R^k\) while every NO vector has norm at least \((\gamma R)^k\).

**Expected move.** Convert a genuine constant base gap into \(\gamma^k\), avoiding any assumption that many clauses are violated.

**Obstruction check.** **O1:** not escaped automatically; the base gadget must already eliminate free-slack cheats. **O2:** tensor minima can be tested by exact enumeration rather than boxes. **O3:** not outside—the decisive threat is an “entangled” tensor-lattice vector shorter than every pure tensor. **O4:** escaped if a tensor soundness theorem holds, because a single global base gap is powered. **O5:** homogenization gives a candidate basis and target, but the tensor-coset theorem is missing. **O6:** problematic: \(k=\Theta(\log n)\) usually makes dimension \(N^k\) quasipolynomial; symmetric or compressed tensors would need a new theorem.

**Falsification.** Find a rank-two entangled vector beating the predicted product lower bound at \(k=2\).

**Smallest experiment.** Tensor the smallest exact all-eight-clause CVP gadget with itself and enumerate the \(k=2\) coset minimum.

**Likely death.** Entangled vectors violate multiplicativity, followed by dimension blowup even if they do not.

---

### 5. Macaulay/resultant spectral separation

**Mechanism.** Encode Boolean equations and clauses as a polynomial system and form a bounded-degree Macaulay matrix. Satisfiability gives an evaluation vector annihilating the matrix; unsatisfiability gives a Nullstellensatz certificate, potentially convertible through a primal-dual block lattice into a distance lower bound.

**Expected move.** Reweight monomials so the smallest relevant nonzero minor—and hence separation—is inverse-polynomial or larger.

**Obstruction check.** **O1:** outside free-slack assumptions because there are no clause slacks; all polynomial equations enter globally. **O2:** ranks, minors, and Smith forms are exact and unbounded. **O3:** overlap is built into the single global ideal. **O4:** an unsatisfiable ideal has a global certificate even when only one clause fails per assignment. **O5:** the proposed primal-dual lattice still needs explicit completeness and soundness radii. **O6:** not escaped: effective Nullstellensatz degree may be exponential, violating polynomial size.

**Falsification.** Show that the first separating degree grows too quickly, or that integer minors become doubly exponentially ill-conditioned.

**Smallest experiment.** Build degree-\(D\) Macaulay matrices for the all-eight-clause instance for \(D=2,\ldots,8\); compute exact ranks, certificates, minors, and associated tiny CVP minima.

**Likely death.** Certificate degree or coefficient height is exponential, and reweighting enlarges completeness equally.

---

### 6. Sheaf cohomology plus cosystolic expansion

**Mechanism.** Regard satisfying local assignments as sections of a cellular sheaf over the variable-clause incidence complex. Unsatisfiability becomes a nontrivial consistency obstruction; product with an explicit cosystolic expander is intended to make every representative of that obstruction have polynomial support.

**Expected move.** Translate large cosystole into Euclidean distance using the integral coboundary matrix as the lattice basis.

**Obstruction check.** **O1:** outside scalar residual/slack assumptions because corrections are full cochains and their support is measured. **O2:** homology, torsion, and minimum representatives can be computed exactly on finite complexes. **O3:** overlaps are the gluing maps themselves, although higher-dimensional correlated fillings remain possible. **O4:** cosystolic expansion is specifically meant to spread one global obstruction. **O5:** coboundary matrices give an explicit lattice, but the target coset and YES radius need construction. **O6:** explicit complexes may be polynomial-size, but if the section-to-cosystole theorem is merely an agreement test in disguise, this violates the campaign’s PCP-free requirement.

**Falsification.** Find an unsatisfiable instance whose obstruction becomes a constant-support coboundary after the proposed product.

**Smallest experiment.** Build the sheaf for two overlapping OR clauses and the all-eight-clause core; product each with a tiny 2-complex and enumerate minimum integral cochain representatives.

**Likely death.** SAT unsatisfiability is not captured by a stable cohomology class, or the construction secretly recreates PCP machinery.

---

### 7. Rotating mixed-radix dominance

**Mechanism.** Use \(m\) global coordinates with cyclic clause orders. In coordinate \(i\), weight all defect digits by \(1,B,\ldots,B^{m-1}\), placing clause \(i\) at the highest digit; thus every nonzero Boolean defect is dominant in at least one coordinate.

**Expected move.** Since \(B^{m}\) has only \(O(m\log B)\) bits, one violated clause could produce exponentially large numeric distance with polynomial encoding length.

**Obstruction check.** **O1:** outside the killed residual-only form only if normalization, Booleanity, selectors, and carries are all weighted; free carries would reproduce Generation 1 immediately. **O2:** exact mixed-radix kernel enumeration must be unbounded. **O3:** rotating orders hinder but do not rule out signed cross-clause cancellation. **O4:** escaped for honest nonnegative defect digits because every clause is most significant once. **O5:** the weighted rows directly define an integer CVP matrix, but completeness norm and conditioning require accounting. **O6:** coefficient bit lengths are polynomial and construction deterministic; no PCP is used.

**Falsification.** Find a signed selector/carry vector whose dominant digits cancel in every rotation at \(O(1)\) norm.

**Smallest experiment.** Use the eight-clause core, eight cyclic orders, and \(B=3,5\); optimize carries exactly and enumerate signed selectors with a certified branch-and-bound radius.

**Likely death.** Lattice variables have signs, so mixed-radix uniqueness for bounded nonnegative digits does not apply; large weights may also inflate completeness.

Classical ingredients invoked: Sipser–Spielman, *Expander Codes* (IEEE TIT, 1996); Kitaoka, *Arithmetic of Quadratic Forms* (1993); Kollár, *Sharp Effective Nullstellensatz* (JAMS, 1988); Evra–Kaufman, *Bounded Degree Cosystolic Expanders of Every Dimension* (STOC, 2016).
