# Generation 17 — divergent mechanisms

For compact audits, the proved-obstruction map is:

- **O1 Slack annihilation (G1):** integer auxiliaries can zero amplified residuals.
- **O2 Overlap circuits (G2–5):** locally isolated fibers acquire short kernels under composition.
- **O3 Exact-kernel/filter failure (G6–7):** external restrictions are invalid, and zero residual defeats radix/modular amplification.
- **O4 Low-degree parity (G9–11, G16):** bounded-degree features admit relocated cube-derivative kernels.
- **O5 Drops (G12):** deleting a clause/block can beat equal-radius fingerprints.
- **O6 Affine lift (G13, G15–16):** the constant-\(\ell_1\) honest-affine combination threads linear enlarged encodings; equal-radius extensions face a triangle-inequality ceiling.
- **O7 No gap law (G14):** finite bag-shell separation does not compose into a polynomial gap.
- **O8 CVP gate:** the construction must emit an unrestricted fixed-target Euclidean CVP instance of polynomial dimension with explicit \(n^c\) soundness.

## 1. Delaunay empty-sphere gluing

**Core trick.** Realize satisfying assignments as vertices of a formula-specific Delaunay cell: all lie on a small empty sphere centered at the CVP target, while illegal signed combinations lie outside a hierarchically enlarged sphere. Glue clause cells through Delaunay fiber sums rather than residual equalities.

**Expected move.** Replace “penalize violated equations” by “classify every short lattice point geometrically,” potentially giving multiplicative separation through lexicographic heights.

**Audit.** **O1:** outside—no slack. **O2:** outside only if empty-sphere gluing survives overlaps. **O3:** no radix/filter, but unrestricted enumeration remains necessary. **O4:** no moment truncation. **O5:** block drops must be explicit nonvertex inequalities. **O6:** not automatically escaped; all global assignments cannot remain equal-radius, or the \(\ell_1=9\) ceiling returns. **O7:** requires an inductive Delaunay composition theorem. **O8:** rational Gram factorization is possible, but \(n^c\) is unproved.

**Smallest experiment.** SDP-search a rational Gram matrix/center for the eight-clause three-variable obstruction and each seven-clause deletion; enumerate coefficients in \([-2,2]\).

**Likely death.** Fiber gluing either creates unintended Delaunay vertices or scales completeness together with soundness.

## 2. Tensor-lattice rank rigidity

**Core trick.** Encode a global assignment as a pure tensor in a tensor product of clause lattices. Seek factors with the property that every sufficiently short tensor-lattice vector is decomposable; signed pseudodistributions have tensor rank at least two and should pay through secondary singular values.

**Expected move.** Recursive tensoring could multiply soundness ratios, with a tree tensor network attempting to retain polynomial dimension.

**Audit.** **O1:** no slack. **O2:** bonds are global, not private rows. **O3:** a zero linear syndrome can still have costly tensor rank. **O4:** not bounded-degree moments. **O5:** the zero/dropped factor must be enumerated. **O6:** only escaped if a quantitative rank-rigidity theorem beats the equal-radius triangle ceiling; otherwise not escaped. **O7:** recursive tensoring supplies a candidate composition law. **O8:** Kronecker bases give explicit CVP, but polynomial bond dimension is unresolved.

**Smallest experiment.** Tensor two Generation-14 bag lattices sharing a clause; exactly enumerate the G7 attack, G13 affine lift, all single-factor drops, and all vectors through \(4B/3\).

**Likely death.** Tensor dimension becomes exponential, or entangled short lattice vectors destroy decomposability.

## 3. Noncommutative holonomy gadget

**Core trick.** Assign literals generators of a small nonabelian group and make clauses transition between group states. A satisfying assignment has trivial holonomy around every prescribed cycle; unsatisfiability should create many nonidentity products whose matrix representations are Euclideanly separated.

**Expected move.** Affine combinations preserve linear marginals but not ordered group multiplication, directly targeting O6.

**Audit.** **O1:** no slack needed. **O2:** cycles traverse overlaps globally. **O3:** multiplicative holonomy is not a radix of a linear residual, although its eventual flow linearization may regain kernels. **O4:** no degree cutoff. **O5:** clause deletion must leave detectable broken cycles. **O6:** outside only before linearization; signed state flows may reconstruct the lift. **O7:** needs a cycle-expansion theorem giving polynomially many charged cycles. **O8:** permutation-representation blocks are integral, but every state/carry must remain unrestricted.

**Smallest experiment.** Use \(S_3\) or the mod-3 Heisenberg group on the eight-clause three-variable obstruction; compare exact minima after deleting one clause.

**Falsification.** A zero-holonomy signed circulation matching the G7/G13 projections.

**Likely death.** Arbitrary unsatisfiability need not induce nontrivial holonomy, and automaton linearization admits cancelling flows.

## 4. Secondary cohomology rather than ordinary cocycles

**Core trick.** Build a twisted chain complex where ordinary consistency is a primary cocycle condition, then measure a quadratic refinement, Bockstein, or Massey-type secondary operation. The G13 pseudodistribution can be a zero primary cocycle while still carrying nonzero secondary obstruction.

**Expected move.** Charge exactly the affine lifts that ordinary cosystolic expansion transmits unchanged.

**Audit.** **O1:** no free slack. **O2:** secondary operations are global overlap invariants. **O3:** exact primary kernels are intended inputs, not escapes. **O4:** not escaped automatically—a fixed quadratic operation may have a higher derivative kernel. **O5:** test whether drops trivialize the secondary class. **O6:** nonlinear secondary structure is outside linear gluing, but any linear CVP gadgetization may restore the affine lift. **O7:** needs a family with polynomial secondary cosystole. **O8:** no valid fixed-target lattice realization yet.

**Smallest experiment.** On the nine-clause instance, construct a mod-4 lift of the existing consistency complex and compute the Bockstein/quadratic value of the exact G13 coefficients, drops, and honest controls.

**Falsification.** The G13 lift has zero secondary class, or a nearby signed chain cancels it.

**Likely death.** Unsatisfiability does not uniformly force a secondary class; linearizing the operation recreates O6.

## 5. Macaulay rank and exterior-power amplification

**Core trick.** Represent the Boolean formula by its Boolean and clause-polynomial ideal. Use a degree-\(d\) Macaulay matrix, then exterior powers or maximal minors so that satisfiability produces a structured kernel vector while unsatisfiability forces an integer determinant away from zero.

**Expected move.** Determinant lower bounds could turn algebraic rank into Euclidean distance without selector marginals; compressed sparse-resultant structure might permit \(d=\Theta(\log n)\).

**Audit.** **O1:** no slack. **O2:** global ideal, not local fibers. **O3:** an exact syzygy remains fatal and is directly testable. **O4:** fixed \(d\) remains vulnerable; the proposal needs compressed growing degree. **O5:** dropping a polynomial must be audited. **O6:** raw-selector affine lift is outside the variables, but affine combinations of evaluations may create syzygies. **O7:** exterior powers offer a proposed multiplicative law. **O8:** explicit CVP conversion and polynomial exterior dimension are open.

**Smallest experiment.** Build degree \(1,2,3\) Macaulay matrices for all eight clauses on three variables and each seven-clause control; compute SNF, smallest minors, and the corresponding determinant-lattice minima.

**Falsification.** Unsatisfiable instances retain low-degree kernels or determinant separation stays constant.

**Likely death.** Required Nullstellensatz degree or exterior dimension is exponential.

## 6. Transfer-determinant compression of repeated checking

**Core trick.** Aggregate length-\(k\) clause-check walks into a polynomial-size transfer matrix instead of materializing all \(m^k\) tuples. Use characteristic-polynomial coefficients, determinants, or traces of exterior powers to make one persistent defect affect exponentially many walks.

**Expected move.** With \(k=\Theta(\log n)\), spectral decay might yield an \(n^c\) gap while the transfer matrix remains polynomial-size.

**Audit.** **O1:** no auxiliary residual slack in the conceptual version. **O2:** checks are globally walked. **O3:** exact invariant subspaces may null every aggregate. **O4:** degree grows logarithmically but is compressed, rather than explicitly enumerated. **O5:** walks must revisit dropped clauses often enough. **O6:** determinants are nonlinear, but linearizing their computation may commute with the affine lift. **O7:** spectral powering is the proposed gap law. **O8:** a carry-complete unrestricted CVP encoding is not yet supplied.

**Smallest experiment.** Form transfer matrices for the nine-clause obstruction and control at \(k=1,\ldots,4\); symbolically compute traces/minors on honest states, G13, G7, and drops before building any lattice.

**Falsification.** The harmful affine state occupies an invariant subspace with the same spectrum as a control.

**Likely death.** CVP linearization destroys multiplicative amplification, or the construction becomes a disguised unproved gap-amplification theorem.

## 7. Voltage-graph lift for large Graver distance

**Core trick.** Replace each shared marginal edge by a voltage-labeled lift. A local signed circuit closes in the base graph but changes sheets upstairs, so cancelling it requires a long lifted circuit; choose explicit lifts with large directed distance rather than merely random expansion.

**Expected move.** Turn the Generation-5 overlap kernel from weight \(O(1)\) into a polynomial-support Graver move.

**Audit.** **O1:** no slack. **O2:** directly targets overlap circuits by changing global closure. **O3:** exact kernels still exist, but should be long rather than invisible to radix rows. **O4:** unrelated to degree moments. **O5:** drops become open paths and need endpoint penalties. **O6:** not fully outside—affine combinations of complete lifted assignment paths still exist; their support must be proved polynomially large relative to completeness. **O7:** lift distance supplies a concrete composition invariant. **O8:** incidence matrices are integral and executable, but the ratio theorem is absent.

**Smallest experiment.** Add 3-, 5-, and 7-sheet voltage lifts to every Generation-5 two-clause overlap system; compute exact shortest integer kernels by SNF plus bounded \(\ell_1\) enumeration.

**Falsification.** Any sheet-closing kernel of weight at most eight.

**Likely death.** High-girth bounds are only logarithmic, or honest paths grow at the same rate as harmful circuits.

## 8. Sparse-mixture decoding via Prony moments

**Core trick.** Treat a harmful signed selector as a sparse mixture of global assignments. Perfect hashes plus power sums up to sparsity \(K\) can reconstruct its atoms; enforce clause legality atom-by-atom rather than merely on aggregate marginals.

**Expected move.** For \(K=9\), explicitly expose the atoms in the verified G13 affine combination, at least eliminating every constant-\(\ell_1\) affine lift.

**Audit.** **O1:** no slack in the abstract decoder. **O2:** atoms are global, so overlap is automatic. **O3:** aggregate zero moments through order \(K\) should imply the zero sparse measure. **O4:** only escapes kernels of support at most \(K\); larger derivative kernels remain. **O5:** a dropped atom/block must violate reconstruction normalization. **O6:** directly targets the \(\ell_1=9\) lift, but linear moment equalities alone still transmit it; nonlinear Hankel-rank/atomwise legality is essential. **O7:** no growing-gap law yet. **O8:** rank constraints have no valid CVP realization yet.

**Smallest experiment.** On all 16 four-variable assignments, compute deterministic perfect hashes and moments through order nine; verify exact recovery of the G13 coefficients and search for colliding signed measures of \(\ell_1\le 12\).

**Falsification.** A colliding legal sparse measure, or failure to encode Hankel rank without signed slack.

**Likely death.** Linearizing sparse recovery recreates O6; unrestricted attacks simply use more than \(K\) atoms.

**Classical inspiration:** Kitaoka, *Arithmetic of Quadratic Forms* (1993), for tensor-lattice rigidity; Gross–Tucker, *Topological Graph Theory* (1987), for voltage graphs; Cox–Little–O’Shea, *Using Algebraic Geometry* (1998), for Macaulay/resultant methods; Ben-Or–Tiwari (STOC 1988) for sparse interpolation.
