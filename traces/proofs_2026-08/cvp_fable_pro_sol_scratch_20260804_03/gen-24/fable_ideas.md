Below are six independent mechanisms. None is promoted; each has an immediate kill test.

### 1. Integral quadratic “gate moat”

**Mechanism.** Search for a rational positive-definite quadratic form whose unrestricted integer minima over port fibers realize NAND: legal Boolean fibers have radius \(R\), while every illegal or non-Boolean fiber has radius at least \(SR\), \(S>1\). Port identification and Schur complementation would compose a balanced circuit; depth \(\Theta(\log n)\) could yield \(S^{\Theta(\log n)}=n^c\).

**Expected move.** Replace linear residual enforcement by genuinely quadratic geometry with a multiplicative fiber-minimum contract.

**Obstruction audit.** G1/G7 slack and radix kernels assume amplified linear residuals, absent here. G2/G3/G5 local affine isolation does not apply directly, but overlap must be tested. G6 is avoided by optimizing all integer variables. G9/G11 is **not escaped**: this remains PSD geometry, so parity may remain cheap. G12 drops, G13/G15 affine mixtures, and G19 signed splices require explicit enumeration. G14’s finite-only problem remains until the composition identity is proved. G20/G21 scaling is exactly the unproved contract. G22 tensor entanglement is irrelevant.

**Smallest experiment.** Enumerate \(4\!-\!6\)-variable integral Gram matrices with entries in \([-4,4]\), half-integral centers, and all integer points in a certified radius; then compose two NAND copies.

**Falsification/death.** A parallelogram or convexity inequality may force some signed illegal fiber within the legal radius.

---

### 2. Discriminant-coset legality transformer

**Mechanism.** Use the eight residue classes of \(2\mathbb Z^3\subset\mathbb Z^3\) as clause labels, declaring seven legal and one illegal. Search over positive-definite Gram forms, targets, and small overlattices so the seven legal cosets have equal minimum \(R\), the illegal coset has minimum \(>SR\), and fiber-product gluing preserves this ratio recursively.

**Expected move.** Make legality a nearest-representative property of a finite discriminant group rather than a linear syndrome.

**Obstruction audit.** G1/G7 do not cover coset minima. G2/G3/G5 remain relevant because gluing may create short representatives; no escape is claimed. G6 is avoided by enumerating unrestricted coset representatives. G9/G11 moment parity is absent. G12 drops become explicit zero/forgotten-port cosets. G13/G15 affine lifts and G19 signed splices could still produce cheap representatives and are primary tests. G14’s finite pass is insufficient; a fiber-product theorem is required. G20/G21 would follow only from a verified multiplicative contract. G22 is inapplicable. This repairs the G23 complaint by freezing the quotient and port alphabet.

**Smallest experiment.** Enumerate \(3\times3\) integral Gram matrices with bounded entries, rational targets of denominator two, and all two-gadget gluings for every polarity.

**Falsification/death.** Discriminant-group parallelogram identities may force the illegal coset no farther than one legal coset after gluing.

---

### 3. Spherical tensor amplification with an entanglement audit

**Mechanism.** Homogenize base encodings onto one sphere, so distance is controlled by correlation. Under tensor powers, decomposable NO correlations would shrink as \(\rho^k\), while YES tensors remain coherent; \(k=\Theta(\log n)\) would create a polynomial gap if every short lattice tensor were forced to be nearly decomposable.

**Expected move.** Prove a lattice-specific rank-one theorem, perhaps after alternating or symmetric projection, rather than assuming tensor minima multiply.

**Obstruction audit.** G1/G7 linear kernels may become costly after tensoring but are not automatically removed. G2/G3/G5 are unrelated locally. G6 requires unrestricted tensor-lattice optimization. G9/G11 parity and G13/G15 affine lifts may tensor into low-rank attacks. G12 drops must be included as tensors with missing factors. G19 signed splices may become entangled tensors. G14 supplies only a possible base gadget, not amplification. G20/G21 is the desired correlation law. **G22 applies directly**: entangled short vectors are the central unresolved obstruction, not escaped.

**Smallest experiment.** Form the symmetric square of the G7 72-selector Gram instance, project to the symmetric basis, and use exact MILP/branch-and-bound to search below the best decomposable obstruction and matched-control radii.

**Falsification/death.** One rank-two entangled lattice vector beating the decomposable threshold kills the mechanism immediately.

---

### 4. Ramified-ideal valuation amplifier

**Mechanism.** Encode states in the Minkowski embedding of a fixed number ring. Legal transitions multiply by units, while a false clause should force the accumulated state into \((\pi)\); recursive composition would force divisibility by \(\pi^d\), and the algebraic norm would convert valuation \(d=\Theta(\log n)\) into polynomial Euclidean length.

**Expected move.** Obtain amplification from multiplicative ideal valuation rather than additive residual magnitude or radix position.

**Obstruction audit.** G1/G7 do not cover multiplicative valuation, unless its implementation degenerates into carries. G2/G3/G5 overlap remains unresolved. G6 demands that all ideal coefficients and representatives be lattice variables. G9/G11 parity has no direct valuation guarantee. G12 drops may map to zero or a low-valuation ideal element. G13/G15 affine combinations and G19 signed flows are severe: selector-linearized multiplication may let them synthesize a unit. G14 gives no valuation composition theorem. G20/G21 would follow from valuation accumulation versus completeness radius. G22 may reappear if ideal products are implemented by tensor lattices.

**Smallest experiment.** Use \(\mathbb Z[i]\), \(\pi=1+i\), two binary multiplication gadgets, and exhaust all selector coefficients in \([-2,2]\); test whether an illegal signed state can retain valuation zero.

**Falsification/death.** Linearized multiplication tables will probably admit a G19-style signed splice producing a unit or zero.

---

### 5. Non-normal tree-fold coefficient expansion

**Mechanism.** At each composition node, transport port vectors through label-dependent integer matrices with an expanding direction, such as conjugates of \(\begin{pmatrix}2&1\\1&1\end{pmatrix}\). Honest labels stay on designated unit vectors, but any incompatible affine combination should acquire coefficients growing like \(\lambda^d\) across depth \(d\), even when every linear residual is zero.

**Expected move.** Amplify the norm of exact-kernel attacks themselves, rather than penalizing a residual they annihilate.

**Obstruction audit.** G1/G7 residual-zero attacks are explicitly targeted. G2/G3 local isolation is not enough; G5 overlap must be built into merge tests. G6 is avoided by emitting every transport row. G9/G11 parity may lie in an invariant nonexpanding subspace. G12 drops require dedicated absorbing states. G13/G15 is the primary obstruction: evaluate their exact affine coefficients through every level. G19 signed paths may switch matrices to follow contracting directions. G14 lacks this coefficient-growth law. G20/G21 would be supplied by \(\lambda^{\Theta(\log n)}\), if completeness remains small. G22 is irrelevant unless transports are tensorized.

**Smallest experiment.** Propagate the explicit G13 coefficient vector through every depth-\(1\) to depth-\(4\) binary tree using all \(2\times2\) matrices with entries in \([-2,2]\); exactly search zero-residual shells.

**Falsification/death.** Unimodularity or label switching may always expose a stable/contracting direction, reproducing G15 at constant ratio.

---

### 6. Construction-A homology with verified cosystolic covers

**Mechanism.** Build a finite chain complex with lattice
\[
L=\operatorname{im}\partial_2+p\mathbb Z^{E}.
\]
Clause labels are explicit 2-cells attached along variable-port edges, and the CVP target is the aggregate boundary demand. Satisfying assignments give short fillings; an unsatisfied formula should leave a nonzero homology class whose minimum representative grows under a sequence of explicitly verified covers.

**Expected move.** Make signed cancellation subject to a global systolic lower bound; logarithmically many constant-degree covers could yield polynomial distance.

**Obstruction audit.** G1/G7 additive residual amplification is absent. G2/G3/G5 becomes the question whether port gluing creates a short boundary. G6 is avoided because chains are unrestricted integers modulo the emitted Construction-A lattice. G9/G11 parity may become a short cycle. G12 drops are relative-homology classes and must be searched. G13/G15 affine lifts may be boundaries; G19 signed splices are literally signed chains, so only a proved systole defeats them. G14 gives no cover law. G20/G21 requires cosystole growth faster than filling baseline. G22 is irrelevant. Unlike the unspecified G23 topology route, all cells, boundaries, and targets are explicit.

**Smallest experiment.** Attach the all-eight-clause three-variable instance to a small triangulated complex, enumerate all two-sheeted covers, and compute every target-coset minimum by SNF plus exact CVP.

**Falsification/death.** Formula ports will likely introduce a constant-size filling that survives every cover.

Classical conceptual sources: Rosenberg (1975) on quadratic pseudo-Boolean reductions; Graver (1975) on integer kernel bases; Conway–Sloane (1999) on Construction A and lattice cosets.
