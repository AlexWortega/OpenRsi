I use the following obstruction key in every audit:

- **R:** G1 residual/slack annihilation.
- **L:** G2–G5 local isolation failing under overlap.
- **V:** G6 requirement that every constraint appear in the emitted CVP instance.
- **K:** G7/G9/G11 exact selector and parity kernels.
- **A:** G13/G15 honest-affine-span and hierarchy lifts.
- **F:** G19 signed-flow splicing.
- **D:** G12/G38 DROP or zero-vector attacks.
- **C:** G28/G30/G32/G37 isometry, additive composition, and parity cuts.
- **S:** G33/G34 equal-completeness failure.
- **X:** G14/G31/G38 fixed-shell success without scaling.

### 1. Expander-supported equal-radius Gram

**Mechanism.** Let \(x(a)\) be the selector encoding of global assignment \(a\). Solve exact Fourier-linear equations forcing \(x(a)^TQx(a)-2c^TQx(a)\) to be constant, while choosing the remaining PSD entries on a lossless-expander support to obtain integer-RIP against sparse deviations (cf. Sipser–Spielman, 1996). Honest points share a radius, not an image.

**Expected move.** A degree \(n^\epsilon\) expander could charge every low-support signed deviation by \(n^\epsilon\) without residual amplification.

**Audit.** **R/L/F:** no slack, private syndrome, or flow. **V:** emit rational \(Q,c\) and a rational sum-of-squares factor. **K/A:** direct selector energy can see zero-residual parity; G13’s common-image theorem does not apply, although its affine witness remains a live attack. **D:** include \(z=0\) among separation constraints. **C:** use one cross-copy expander rather than block sums; superadditivity remains unproved. **S:** certify radius equations before soundness. **X:** promotion requires a uniform RIP-plus-sparsity lemma.

**Falsification.** Exact SDP dual gives zero margin, or parity remains additive.

**Experiment.** On G31, enumerate 3-regular clause graphs, solve rational SDPs over all 16 honest points, then exact-search through 216.

**Likely death.** Equal-radius constraints may force precisely the G37 parity cut.

---

### 2. Torsion-cosystolic selector sheaf

**Mechanism.** Place free abelian groups on legal logarithmic-size bags and explicit restriction maps on a bounded-degree 2-complex. Engineer the augmented boundary matrix so a NO instance’s degree-one pseudosections represent a nonzero torsion class whose every integral representative has norm \(n^\epsilon\), not merely nonzero Smith invariant (Ramanujan-complex inspiration: Lubotzky–Samuels–Vishne, 2005).

**Expected move.** Exact signed consistency would become expensive through integral cosystole, while YES sections remain ordinary one-hot sections.

**Audit.** **R:** no slack residual. **L:** restrictions are globally coupled, not private clause rows. **V:** all boundary and augmentation rows are emitted integers. **K/A:** the proposed cosystole directly targets exact parity and affine pseudosections; it is not automatically outside them. **F:** no path-flow representation. **D:** augmentation maps zero to the wrong torsion class. **C:** growth comes from a growing torsion/cosystole parameter, not repetition. **S:** one-hot anchors give exact equal completeness. **X:** requires an explicit infinite complex family and integral inequality.

**Falsification.** Any zero-boundary signed pseudosection, or a unit-norm representative of the torsion class.

**Experiment.** Search 6–10 bags and \(\{-1,0,1\}\) restriction matrices; compute SNF and exact shortest affine representatives with MILP.

**Likely death.** Large torsion order need not imply a large Euclidean representative.

---

### 3. Discrete-convex barrier for signed branching flows

**Mechanism.** Retain a layered branching program, but replace G19’s diagonal anchors by a PSD “prefix-discrepancy” Gram containing laminar interval sums and nonbacktracking edge differences. Choose weights so every honest path has identical energy, while any negative splice creates discrepancies on many nested intervals (discrete-convex motivation: Murota, 2003).

**Expected move.** One negative edge should cost \(\Omega(L^{1+\epsilon})\), versus honest radius \(O(L)\).

**Audit.** **R/L:** neither residual slack nor private overlap isolation. **V:** prefix rows are explicit factor rows. **K/A:** residual-zero affine combinations are charged geometrically rather than by syndrome; no theorem yet excludes them. **F:** this directly mutates G19’s vulnerable objective instead of assuming signed flows absent. **D:** source/sink and zero flow are included in the barrier audit. **C:** intervals cross concatenation seams, so the metric is not additive or the G30 seed. **S:** equal path energy is an exact combinatorial identity to verify. **X:** needs a uniform signed-flow discrepancy theorem.

**Falsification.** A two-negative accepting flow with only \(O(L)\) prefix energy.

**Experiment.** Compile the eight-clause three-variable obstruction to the smallest layered DAG; enumerate all signed flows with at most four negative edges under depth-1–4 laminar metrics.

**Likely death.** A splice may shadow two honest paths and disturb only \(O(\log L)\) intervals.

---

### 4. Recursive mixed-radix coefficient locking

**Mechanism.** Replace each selector coefficient by a depth-\(d\) redundant signed-digit tree with emitted carry equations. Unlike G7, the tree amplifies noncanonical coefficients themselves: a negative root digit should force malformed descendants in \(b^d\) leaves (redundant-digit precedent: Avizienis, 1961).

**Expected move.** With \(d=\Theta(\log n)\), one signed selector could incur polynomial excess while honest canonical trees have only \(O(d)\) active digits.

**Audit.** **R:** carries are recursively encoded and anchored, not free slack. **L:** trees attach globally to every shared selector. **V:** every carry and digit coordinate is emitted. **K:** exact logical residual kernels still face digit noncanonicity. **A:** not outside G13/G15—the affine combination may lift through the entire digit tree, which is the decisive test. **F:** no flow semantics. **D:** zero misses every root normalization and propagates downward. **C:** proposed growth is a branching recurrence, not direct-sum repetition. **S:** canonical \(0/1\) trees must have identical support and radius. **X:** promotion requires a recurrence bounding unrestricted integer trees.

**Falsification.** The G13 coefficients extend with zero carries and merely additive anchor excess.

**Experiment.** Apply binary trees of depths 1–4 to the explicit G11/G13 parity coordinates; exact-DP the minimum tree cost.

**Likely death.** Linearity probably lets the affine lift thread every level, as in G15.

---

### 5. Finite-field chirp/projector fingerprints

**Mechanism.** Tag each local label by an integral Legendre-chirp vector over \(\mathbb F_p\), with clause-context phases arranged on an expander. Exact character identities enforce equal honest radius, while Weil correlation bounds aim to make any short signed combination nearly orthogonal (Weil, 1948).

**Expected move.** For support \(s\), obtain energy \(p\|h\|_2^2-O(\sqrt p\,\|h\|_1^2)\); taking polynomial \(p\) could charge G11/G13 parity strongly.

**Audit.** **R/L/F:** no slack, private isolation, or flow. **V:** Legendre tags are explicit integer factor rows. **K:** tags act directly on zero-residual selector deviations. **A:** honest points are equinorm rather than common-target, so G13’s compatible-syndrome premise fails; its actual vector must still be tested. **D:** zero and clause drops receive full tag/normalization accounting. **C:** context phases span copies, avoiding block additivity, but no growth theorem follows from coherence alone. **S:** exact cosphericity is the first gate, unlike G33’s assumed bivectors. **X:** Weil bounds must cover every low-energy support size uniformly.

**Falsification.** Completeness energies differ, or a parity vector lies in a low Fourier mode.

**Experiment.** Use \(p=17,29\) on G31; enumerate context phase rules, certify all 16 honest norms, then evaluate G7/G11/G13/DROP and the exact shell.

**Likely death.** Relevant signed supports may be too large for the coherence bound to remain positive.

---

### 6. Multiplicative ideal-norm amplification

**Mechanism.** Interpret malformed residuals as algebraic integers in a cyclotomic ring and compose gadgets by multiplication rather than Euclidean direct sum. Use the positive trace form \(\mathrm{Tr}(\alpha\bar\alpha)\) as an explicit rational Gram; nonzero ideal norms multiply across depth while roots of unity provide equal-norm honest states (standard background: Neukirch, 1999).

**Expected move.** Degree or composition depth \(\Theta(\log n)\) could turn a fixed nonzero algebraic defect into \(n^\epsilon\) trace energy.

**Audit.** **R:** no free integer slack. **L:** multiplication is global, not private overlap composition. **V:** emit companion matrices, trace Gram, center, and rational factor. **K/A:** this is not outside exact zero kernels—if parity maps to \(\alpha=0\), norm amplification does nothing. **F:** no flow. **D:** zero produces a nonzero normalization element before amplification. **C:** ideal norm is multiplicative, unlike G28/G32 addition; G30-style seed isometry must be checked. **S:** honest roots of unity have equal trace norm. **X:** needs a uniform lower bound controlling units and dimension growth.

**Falsification.** Any exact affine kernel maps to zero, or a unit makes conjugate energy highly unbalanced.

**Experiment.** Use \(\mathbb Q(\zeta_5)\); map the G31 parity and DROP defects into its integral basis, form one and two multiplicative levels, and enumerate coefficient matrices with \(\ell_1\le3\).

**Likely death.** G13’s exact zero relation may survive before the norm is applied.

---

### 7. Counterexample-guided global Gram synthesis

**Mechanism.** Treat the metric itself as the unknown: impose symbolic Fourier equations for equal completeness and PSD, ask an exact integer oracle for the cheapest malicious vector, then add its linear cutting plane in \(Q\). Iterate until obtaining either a rational metric with margin or an exact dual certificate explaining why the chosen feature language can never work.

**Expected move.** Discover cross-orbit terms missed by the hand-designed G31/G37 families, or obtain a reusable impossibility theorem.

**Audit.** **R/L/K/A/F/D:** seed the oracle with every recorded slack, overlap, parity, affine, signed-flow, and DROP witness; none is assumed excluded. **V:** only rationally factored final Grams count. **C:** include one-, two-, and three-copy inequalities simultaneously, so additive parity is an explicit cut. **S:** exact equal-radius equations precede optimization. **X:** a finite optimum is not promoted unless the dual has a symbolic \(n\)-parameter extension and bounded-support reduction.

**Falsification.** Rational infeasibility, a G37-type universal parity dual, or an unrestricted vector violating the claimed margin.

**Experiment.** Combine G31 Walsh, G38 bag, cross-clause, and prefix-flow features on the nine-clause instance; alternate exact shell DP/MILP with rationalized SDP cuts.

**Likely death.** The equal-completeness cone may contain no polynomial margin, and general separation is itself CVP-hard.
