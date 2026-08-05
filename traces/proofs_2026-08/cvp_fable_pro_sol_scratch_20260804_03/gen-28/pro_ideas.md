### Obstruction key
**A** G1/G7 free-slack or exact-residual kernels; **B** G2–3/G5 local isolation failing under overlap; **C** G6 external filtering/mod-2 bypass; **D** G9/G11 constant-cost parity; **E** G12 clause drop; **F** G13/G15 honest-affine lift; **G** G14 finite shell without composition; **H** G19 signed-flow splice; **I** G20/G21 missing polynomial relative growth; **J** G22/G27 nonclosed recursion; **K** G27 clipping-diagonal, tensor-diagonal, finite-holonomy, Lawrence-layer, unsupported-global-moment, and linear-homology blockers.

## 1. Witt-vector gate tower

**Mechanism.** Compile “some clause is violated” as a Boolean arithmetic circuit, but encode every gate by its first \(t\) 2-adic/Witt digits, including all carry variables and table normalizations. A signed gate-table solution surviving level \(j\) should either be honest or force divisibility by \(2^j\).

**Expected move.** With \(t=\Theta(\log n)\), an illegal exact fiber would require coefficient norm \(2^{\Omega(t)}=n^{\Omega(1)}\), while honest evaluation uses one table entry per gate.

**Audit.** A: no free carries, though an exact tower kernel remains fatal. B: wires are globally identified, not private marginals. C: all digits enter the CVP objective; search is unrestricted. D: computes the full OR, not bounded-degree moments. E: dropping a gate violates every digit normalization, but possibly only \(O(t)\) cost. F: Teichmüller lifting is nonlinear, so the raw affine collision does not automatically lift. G: no reliance on the pair-bag pass. H: signed table splices remain explicitly possible. I: valuation growth is the proposed law. J: bounded digit/carry ports give a candidate finite closure. K: no clipping, tensor, holonomy, Lawrence, moments, or homology.

**Experiment/falsifier.** Emit the nine-clause circuit for \(t=3\), enumerate the exact shell including G13/G19 seeds. Kill on any zero-residual signed evaluation below \(2^{2t}\).

**Likely death.** A cross-level signed carry cycle.

---

## 2. Torsion-free noncommutative path signatures

**Mechanism.** Label circuit transitions by unitriangular integer matrices and record truncated ordered products—the discrete analogue of a path signature. Conservation sees only degree one, whereas the G19 splice should create nonzero commutator or higher iterated-product coordinates.

**Expected move.** A balanced product tree of nilpotency class \(t\) could force the first illegal accepting object into a central coordinate of magnitude \(L^{\Omega(t)}\), with honest paths remaining unit-sized.

**Audit.** A: signature coordinates act on transitions themselves, not residual slack. B: order-sensitive global products replace private overlap rows. C: every product-table selector is a lattice coefficient. D: parity mixtures need also match ordered products. E: a dropped segment breaks interval products, although boundary cancellation may be cheap. F: linear affine combinations are not group-like, but signed table lifts must be tested. G: supplies a new recurrence, not inherited composition. H: directly targets signed flow splicing. I: central-coordinate growth is the intended polynomial law. J: interval products form explicit tree ports. K: torsion-free nilpotent growth is outside finite-group holonomy; no clipping, naive tensor, Lawrence, moments, or homology.

**Experiment/falsifier.** Add class-2 Heisenberg coordinates to a 20–40-layer reduction of the G19 program and exactly search anchor excess \(0,8,16,24\). Kill if its two-negative accepting flow extends with zero central residual.

**Likely death.** Signed multiplication-table combinations fake group-likeness at constant cost.

---

## 3. Veronese–secant rank detector

**Mechanism.** Lift each assignment/bag state to squarefree Veronese coordinates through degree \(d\). Honest states are rank-one points; affine pseudodistributions such as G13 typically have higher secant rank, detectable by catalecticant or Plücker coordinates implemented through local lookup tables.

**Expected move.** Exterior minors of increasing order could turn bounded signed rank into many nonzero integral coordinates, yielding polynomial energy while legal rank-one states retain fixed norm.

**Audit.** A: detection is on lifted selectors, not residual amplification. B: full lifted coordinates are shared across overlaps. C: lookup and compound coordinates must all be emitted. D: choosing \(d>3\) escapes the tested low-degree parity kernel. E: normalization minors may detect drops, but zero vectors make this uncertain. F: the raw affine collision need not lift; however the same affine combination of complete lifted assignment vectors always exists and is a mandatory attack. G: no composition follows from G14. H: signed-flow vectors become higher-rank candidates. I: minor-count growth supplies the proposed law. J: bounded catalecticant boundary data may close. K: symmetric-power diagonal shortcuts may apply, so this is **not** outside that blocker; other K assumptions are unused.

**Experiment/falsifier.** Augment G14 with all degree-4 squarefree coordinates on four variables and \(2\times2\) catalecticants; search through \(B+64\), seeded by G13/G19/drop states.

**Likely death.** A low-rank signed secant extension, especially a diagonal lift, preserves every emitted minor.

---

## 4. Dual Macaulay/Nullstellensatz lattice

**Mechanism.** Stop encoding witnesses. Form the Macaulay operator for \(x_i^2-x_i\) and clause polynomials; satisfiability gives an evaluation functional annihilating its rows, while unsatisfiability may give an integral certificate representing \(1\). Embed the operator and target dually so certificate height, rather than local residual count, controls CVP distance.

**Expected move.** A polynomial-degree, polynomial-height certificate dichotomy could be amplified by determinantal divisors or several small primes, without requiring local unsatisfaction density.

**Audit.** A: syzygies are exposed directly; there is no slack amplifier. B: the construction is formula-global. C: the Macaulay lattice and target must be fully emitted. D: degree rises adaptively beyond cubic parity. E: clause deletion changes the ideal rather than merely removing one selector. F: affine witness collisions are irrelevant unless they induce a dual annihilator. G: no reliance on pair bags. H: no flows. I: certificate degree/height must provide the polynomial law. J: no recursive state closure is assumed. K: this squarely faces the unsupported-global-degree/compression blocker and is **not outside it**; other K mechanisms are absent.

**Experiment/falsifier.** For the nine-clause obstruction and control, build exact Macaulay matrices at degrees \(3,4,5\), compute Smith forms and exact dual CVP minima.

**Likely death.** General unsatisfiable formulas require exponential Macaulay dimension or certificate height, and the dual embedding may reverse the desired completeness/soundness direction.

---

## 5. Stabilizer-frame uncertainty penalty

**Mechanism.** Realify a small qudit phase-space frame and tag each local pattern simultaneously in computational and Fourier/stabilizer coordinates. Honest assignments lie in a protected code subspace; signed quasidistributions should be unable to remain sparse and low-energy in both complementary frames.

**Expected move.** Concatenating an explicitly decoded CSS-like block could multiply illegal “negativity” while legal codewords are isometrically embedded, potentially producing \(n^c\) separation.

**Audit.** A: tags apply directly to selectors. B: stabilizers couple overlapping blocks globally. C: use an exact rational Gram matrix and unrestricted coefficients. D: complementary frames should expose Walsh parity. E: erasure/drop syndromes are standard state classes, but may be cheap. F: affine mixtures remain linear vectors, though generally leave the protected subspace; test explicitly. G: requires its own concatenation theorem. H: signed flows become quasidistributions. I: concatenated negativity is the proposed growth law. J: syndrome plus logical state gives finite ports if decoding closes. K: the tensor-diagonal/entangled shortcut directly threatens concatenation, so this is **not outside it**; clipping, holonomy, Lawrence, moments, and homology are unused.

**Experiment/falsifier.** Use ternary two-qutrit blocks, exact two-dimensional real embeddings of cube roots, and tag the nine-clause selectors; enumerate through the control radius plus 32.

**Likely death.** An entangled diagonal state has low energy in both frames and reproduces G13 at constant overhead.

---

## 6. Fully frozen min-plus gap tile

**Mechanism.** Turn the G14 pair-bag construction into a literal finite tile: fix its lattice, target, full-rank factor, port coordinates, glue matrix, and matched control. Enumerate every bounded port representative into named LEGAL, ILLEGAL, DROP, G13, G19, and MALFORMED classes, then compute the exact depth-two min-plus transfer operator.

**Expected move.** An exhaustive closure inequality
\[
T_{\mathrm{illegal}}(2)\ge \lambda T_{\mathrm{illegal}}(1),\qquad
T_{\mathrm{legal}}(2)\le \mu T_{\mathrm{legal}}(1),\quad \lambda>\mu
\]
would provide a concrete route to polynomial recursive separation.

**Audit.** A/D/E/F/H: exact-kernel, parity, drop, affine, and signed-flow states are explicit classes, not omitted attacks. B: gluing frees all port marginals during enumeration. C: coefficient bounds come only from the Gram eigenvalue. G: directly addresses G14’s missing composition. I: \(\lambda>\mu\) is the required law. J: this is specifically the frozen closure audit demanded by G22/G27. K: no clipping, tensor-product norm claim, finite holonomy, Lawrence layers, unsupported moments, or homology.

**Experiment/falsifier.** Glue two reduced G14 tiles along one fixed two-clause port permutation; enumerate all unrestricted fibers through the eigenvalue-derived bound and emit the complete cost table.

**Likely death.** An unlisted malformed boundary state cancels across the seam, or \(\lambda\le\mu\).

---

## 7. High-order dissociated selector tags

**Mechanism.** Give lifted local patterns explicit \(B_h\)/dissociated integer tags so no signed relation of \(\ell_1\)-weight at most \(h\) cancels, while variable-complement tags cancel on honest global assignments. Increase \(h=\Theta(\log n)\); any exact harmful relation should then require coefficient norm \(n^{\Omega(1)}\).

**Expected move.** This attacks selector relations before they become zero residuals, unlike G7 radix amplification after a raw kernel has formed.

**Audit.** A: no free slack and tags see raw selector choices. B: tags are global across occurrences. C: all large integers are explicit with polynomial bit length. D: choose \(h\) above the seven-term parity support. E: a drop leaves an uncancelled tag. F: choose \(h\ge\|\alpha_{\mathrm{G13}}\|_1\), but completeness-compatible honest differences may force shorter relations—mandatory audit. G: no reliance on pair-bag composition. H: include transition tags above the G19 splice weight. I: growing dissociation order is the proposed polynomial law. J: no recursive truncation is required. K: no clipping, tensor, holonomy, Lawrence, moments, or homology.

**Experiment/falsifier.** Construct a Bose–Chowla-style \(B_{13}\) tag set for the 72 selectors, solve exact linear equations imposing all 16 honest cancellation conditions, then test G7/G11/G13/G19/drop vectors.

**Likely death.** Honest completeness equations themselves create a short affine relation, proving strong dissociation incompatible with an unknown satisfying assignment.

Classical inspirations only: K.-T. Chen’s iterated path products; Macaulay matrices; CSS stabilizer codes; and Bose–Chowla \(B_h\) sets. No theorem from these sources is being treated as a soundness result here.
