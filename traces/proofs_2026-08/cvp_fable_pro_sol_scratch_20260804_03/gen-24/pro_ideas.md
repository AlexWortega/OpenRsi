No off-limits material was consulted. These are deliberately nonconvergent Generation-24 sketches.

1. **Translated E-type tensor amplifier**

**Mechanism / expected move.** Find a constant-rank lattice with legal and illegal translated cosets whose distance ratio is \(>1\), then tensor it \(k=\Theta(\log n)\) times. A translated analogue of Kitaoka’s E-type property would force every minimum vector in the illegal tensor coset to decompose, multiplying the ratio while keeping dimension polynomial.

**Obstruction audit.** G1/G7: no slack or radix residuals. G2/G3/G5: requires a genuine tensor-composition theorem, not local isolation. G6: targets, cosets, and unrestricted lattice vectors are explicit. G9/G11/G13/G15/G19: parity, affine lifts, and signed flows are included in each exact coset minimum, not assumed absent. G12: include zero/drop cosets. G14 becomes only a candidate base gadget. G20/G21 are addressed if ratios multiply. G22 is *not escaped yet*: translated/entangled tensor minima are the central lemma. G23’s finite-PSD objection is avoided only if that lemma is certified.

**Smallest experiment.** Enumerate rank-4–8 integral Gram matrices and half-integral targets; retain bases with legal/illegal ratio \(>1.02\), then exactly enumerate every vector in the twofold translated tensor through the predicted product radius.

**Falsification.** Any entangled vector below the product bound.

**Likely death.** E-type results concern unshifted tensor lattices, not arbitrary CVP cosets.

---

2. **Integral cosystolic obstruction complex**

**Mechanism / expected move.** Turn local assignment consistency into a cellular sheaf and unsatisfiability into a prescribed integral cycle. Seek an explicit complex where every signed filling of that cycle has \(\ell_2\)-norm \(N^{1/2+c}\), while a satisfying section gives a filling of norm \(O(\sqrt N)\).

**Obstruction audit.** G1/G7: no amplified scalar residual or radix. G2/G3/G5: overlap is encoded by one global boundary complex. G6: all boundary maps and targets must be emitted. G9/G11/G13/G15: affine pseudodistributions become signed chains and remain live unless the *integral* systolic bound covers them. G12: relative cycles model drops. G19: signed splicing is exactly the filling problem, so this directly tests rather than assumes it away. G14 supplies no theorem here. G20/G21 would follow from a polynomial systole-to-volume exponent. G22 is irrelevant unless complexes are tensor-composed. G23’s prior topological objection is avoided only by freezing every cell and map.

**Smallest experiment.** For contradictory clauses \(x\) and \(\neg x\), build the legal-transition 2-complex, designate accepting-minus-rejecting boundary \(c\), and solve \(\min\{\|y\|_2^2:\partial_2y=c,\ y\in\mathbb Z^f\}\); repeat after one explicit two-lift.

**Falsification.** A constant-support signed filling.

**Likely death.** Arbitrary SAT instances may not induce large systoles without recreating PCP-style gap amplification.

---

3. **Finite boundary-quotient norm transformer**

**Mechanism / expected move.** Represent every gadget by a lattice with boundary group \(Q=(\mathbb Z/2)^3\) and tabulate the exact minimum norm \(m(q)\) in every boundary coset. Search for a gluing operation whose unrestricted fiber minima satisfy a recursive contract \(m_{\mathrm{illegal}}^2\ge S\,m_{\mathrm{legal}}^2\), \(S>1\); repeated substitution would multiply the gap.

**Obstruction audit.** G1/G7: no slack, carry, or radix amplifier. G2/G3/G5: all overlap fibers are minimized exactly. G6: quotient maps, targets, and Gram matrices are internal. G9/G11/G13/G15/G19: their signed vectors are ordinary representatives in the enumerated cosets; none is filtered out. G12: zero/drop is a designated boundary state. G14 motivates, but does not prove, the contract. G20/G21 are precisely the recursive inequality. G22: all two-gadget entangled representatives must be enumerated. G23: this instantiates the gate’s requested finite-quotient reopening condition rather than repeating its unspecified proposal.

**Smallest experiment.** Enumerate dimensions 4–7, Gram entries in \(\{-2,-1,0,1,2\}\), all homomorphisms to \(Q\), half-integral targets, and every unrestricted two-gadget fiber; require identical legal completeness radii.

**Falsification.** Any illegal or drop fiber at most \(\sqrt S\) times legal radius.

**Likely death.** Fiber-product minima usually add rather than multiply, forcing \(S\le1\).

---

4. **Perfect-hash restriction fingerprints**

**Mechanism / expected move.** Replace fixed-degree moments by a polynomial-size perfect-hash family of \(k=O(\log n)\)-variable restrictions and store each bag’s complete Walsh spectrum. The hoped-for uncertainty statement is that every integral mass-one signed measure that is not a Dirac assignment exposes substantial negative Fourier energy on many isolating restrictions.

**Obstruction audit.** G1/G7: no slack or ordered residual. G2/G3/G5: restrictions cross many clause overlaps. G6: every bag selector and Walsh row is emitted. G9/G11: cube parity is detected once its support is isolated. G12: empty bags are explicit drop states. G13/G15: *not automatically escaped*—their global affine measure marginalizes through every bag; success requires a quantitative negativity bound, not mere detection. G19: test the two-negative splice’s induced restrictions. G14 is the \(k=2\) precursor without isolation. G20/G21 remain open unless exposed energy grows superlinearly relative to bag baseline. G22 does not apply absent tensoring. G23’s exponential-monomial objection is avoided because splitters use polynomially many \(O(\log n)\)-bags.

**Smallest experiment.** Generate a minimal perfect-hash family for the current four-variable instance; exactly score G7, G11, G13, G19-derived, all drop, and unrestricted low-anchor states.

**Falsification.** A non-Dirac mass-one signed measure whose every restricted marginal is one-hot or has only constant aggregate excess.

**Likely death.** The G13 measure may retain constant energy per bag, yielding only a constant ratio.

---

5. **Resolution-width/geometry dichotomy**

**Mechanism / expected move.** Run bounded-width resolution as a polynomial-time preprocessing branch: if it refutes the formula, output a fixed far CVP instance. Otherwise use width-\(w\) assignment bags and try to prove that every signed zero-residual lattice vector induces a width-\(w\) pseudoassignment; unsatisfiability without such a refutation should then force large geometric support.

**Obstruction audit.** G1/G7: no residual-only amplification. G2/G3/G5: bags cover the overlaps relevant to resolution clauses. G6: the prepass is a legitimate deterministic branch, and all remaining constraints are emitted. G9/G11/G13/G15: their affine pseudodistributions are exactly what the width correspondence must classify; they are not excluded a priori. G12: bag deletions must be included. G19: signed flows should map either to pseudoassignments or charged defects. G14 is the width-two finite case. G20/G21 require a theorem converting resolution width into polynomial excess. G22 is absent unless bag systems are tensorized. G23’s finite-hierarchy objection remains unless the dichotomy covers every width regime.

**Smallest experiment.** Enumerate unsatisfiable 3CNFs on at most five variables, compute exact resolution width and exact width-\(w\) bag-CVP minima, and search for a monotone lower-bound relation including drops.

**Falsification.** High resolution width but constant anchor excess.

**Likely death.** Intermediate widths cannot be exhaustively preprocessed in polynomial time and may give subpolynomial gaps.

---

6. **Delaunay exact-cover geometry**

**Mechanism / expected move.** Reduce 3SAT syntactically to Exact Cover, then realize every “choose exactly one incident set” constraint as an \(A_{r-1}\) deep-hole block whose nearest lattice points are precisely one-hot choices. Shared set coefficients glue blocks directly; signed and non-Boolean coefficients are judged by Voronoi distance rather than external Boolean checks. Seek a laminated substitution of deep holes where a violated exact-cover block incurs multiplicatively larger covering radius.

**Obstruction audit.** G1/G7: no slack or radix rows. G2/G3/G5: shared coefficients implement overlap globally. G6: the construction is a fixed target lattice. G9/G11/G13/G15: affine combinations remain unrestricted lattice points, but no compatible linear hash is assumed; exact Voronoi enumeration must charge them. G12: zero selections are ordinary drop vectors. G19: there is no flow representation. G14 supplies analogous finite evidence only. G20/G21 depend entirely on laminated radius multiplication. G22 remains live as an entangled lamination vector. G23’s “finite shell only” criticism applies unless a substitution theorem emerges.

**Smallest experiment.** Use sets \(S_1=\{1,2\}\), \(S_2=\{2,3\}\), which cannot cover each element exactly once; emit the three deep-hole blocks and enumerate coefficients in \([-3,3]^2\), then test one two-level lamination.

**Falsification.** A signed vector below the predicted laminated radius.

**Likely death.** Deep-hole penalties add, so one violated block gives only \(1+O(1/m)\) relative gap.

---

7. **Noncommutative holonomy with an integral spectral gap**

**Mechanism / expected move.** Label a constraint graph by elements of a finite nonabelian group and assign each vertex an integral vector in a fixed-point-free representation. Satisfiability gives a parallel section; inconsistent holonomy should make every nonzero integral section pay connection-Laplacian energy, potentially blocking the signed path splice without requiring nonnegative flow.

**Obstruction audit.** G1/G7: no slack or radix amplification. G2/G3/G5: holonomy is global around overlap cycles. G6: group matrices, anchors, target, and Laplacian rows are explicit. G9/G11/G13/G15: affine mixtures are arbitrary integral sections and remain covered only if the spectral inequality includes them. G12: the zero section is the principal drop attack and must be priced. G19 is attacked directly because there are no independently spliceable path edges. G14 gives no holonomy result. G20/G21 require polynomial frustration energy relative to anchor baseline; a constant Kazhdan gap is insufficient. G22 is absent unless representations are tensor-powered. G23’s prior transport objection is avoided only if common fixed spaces are computed exactly rather than inferred from transition equations.

**Smallest experiment.** Encode \(x\wedge\neg x\) using \(A_5\) permutation labels, pass to its four-dimensional integral augmentation representation, and exactly minimize anchor plus connection energy; then insert the G19 two-negative splice pattern.

**Falsification.** A nonzero exact section or a cheap zero/drop section.

**Likely death.** Spectral expansion supplies only constant relative energy, while anchors make the zero section competitive.

Classical hooks used here: Y. Kitaoka, *Arithmetic of Quadratic Forms* (1993), for E-type tensor lattices; R. Karp, “Reducibility Among Combinatorial Problems” (1972), for Exact Cover reductions; E. Ben-Sasson and A. Wigderson, “Short Proofs Are Narrow—Resolution Made Simple” (2001), for the resolution-width viewpoint.
