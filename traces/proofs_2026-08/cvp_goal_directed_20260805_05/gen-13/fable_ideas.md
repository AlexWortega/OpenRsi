No ranking intended; these mechanisms deliberately pull in different directions.

### 1. Relative Dehn-function bags

**Mechanism / move.** Amend Strategy 1’s graph cover to a bounded-degree 2-complex: selector vectors are integral 2-chains and marginal equations are boundary equations. Seek an explicit family with superlinear relative \(\ell_2\)-filling, so an unsatisfiable boundary requires \(\|z\|_2^2\ge N^{1+1/32}\). This amendment is justified because ordinary graph expansion controls support, not coefficient magnitude.

**Audit.** G1/G6/G7: no slack, external quotient, or carry. G12 DROP is an allowed chain. G2/G3: full integral fiber. G14/G31/G38: requires a scalable Dehn theorem, not finite extrapolation. G5; G9/G11; G13; G15; G19; GD1/ordered splice are explicit chain classes, not escaped. G28/G32/G37: no transfer table or additive-copy metric. G30: no tensor. GD2/A5: no convolution. G33/G34: no exterior Gram. D4 midpoint/non-antipodal/independent recombination; E6 bounded/unbounded ports; F289/N8: no shell, affine port, quaternion, or finite gate.

**Experiment.** Attach triangular 2-cells to the \(6,8,10\)-vertex parity expanders; compute SNF and exact minimum-norm fillings.

**Falsification/death.** A uniformly bounded integral filling, or a rational filling whose denominators clear cheaply.

---

### 2. Multi-prime Bockstein tower

**Mechanism / move.** Refine Strategy 1 with \(O(\log N)\) arithmetic covers. Emit integral Bockstein equations so every adverse saturated-kernel class must vanish modulo \(p_i^{k_i}\); if it survives all earlier levels, its coefficients become divisible by \(P=\prod p_i^{k_i}\ge N^{1/64}\), yielding the required anchor growth.

**Audit.** G1/G6/G7: quotient and carry data are represented by emitted SNF/Bockstein rows, with no free digits. G12: zero/DROP is audited modulo every prime. G2/G3: divisibility is proved on the complete unbounded lattice. G14/G31/G38: the tower scales explicitly. G5; G9/G11; G13; G15; G19; GD1/diagonal splice are not outside assumptions—the prime signatures must detect each. G28/G32/G37: no min-plus or copywise metric. G30: no Kronecker product. GD2/A5: no group algebra. G33/G34: no exterior repair. D4 midpoint/non-antipodal/independent recombination; E6 bounded/unbounded ports; F289/N8: none of their geometric or quaternion assumptions occur.

**Experiment.** For G38’s 12 bags, compute adverse classes over \(\mathbb Z/2^k,\,\mathbb Z/3^k\), \(k\le3\), including G13/G19/diagonal seeds.

**Falsification/death.** A primitive torsion-free affine pseudosection invisible at every prime.

---

### 3. Constant-\(\ell_1\) affine-radius no-go

**Mechanism / move.** Try to refute Strategy 3. If a zero-residual adverse selector has an affine representation \(x=\sum_i a_i h_i\), \(\sum_i a_i=1\), by equal-radius honest encodings with constant \(\|a\|_1\), then every linear walk map satisfies  
\[
\|Lx-c\|\le \|a\|_1R.
\]
A constant-\(\ell_1\) lift of G13 therefore upper-bounds the NO/YES ratio independently of \(d\), contradicting \((65/64)^d\) eventually.

**Audit.** This directly uses G13 affine collision and potentially G9/G11 parity and G32/G37 additivity; it is not outside them. G1/G6/G7 and G12 are irrelevant because the witness has zero emitted residual and is not DROP. G2/G3 hold via an explicit integral vector. G14/G31/G38 are tested after lifting. G5/G15/G19/GD1/ordered splice remain alternative witnesses. G28 and G30 are absent. GD2/A5, G33/G34, all D4 obstructions, E6 bounded/unbounded ports, and F289/N8 have absent structural assumptions.

**Experiment.** Symbolically lift the known 16-assignment G13 coefficients into Strategy 3’s \(d=1,2,3\) walk selectors and check every row exactly.

**Falsification/death.** Legality or occurrence tagging may destroy the affine identity; then the no-go proves nothing.

---

### 4. Magnus–Fox leading-word invariant

**Mechanism / move.** Attack Strategy 2 using classical Magnus–Fox calculus: place each occurrence-tagged history in a noncommutative augmentation ideal and emit selected Fox derivatives as prefix coordinates. The first nonzero leading word cannot cancel across distinct occurrences; repeated derivatives should force branching mass and potentially the \(33/32\) recurrence without a finite-state table.

**Audit.** G1/G6/G7: all derivative, COPY, and boundary equations are emitted. G12: augmentation-zero/DROP is included. G2/G3: invariant applies to arbitrary integral coefficients. G14/G31/G38 are unrelated finite-bag passes. G5; G9/G11; G13; G15; G19; GD1/ordered splice must be checked as augmentation-ideal identities, not assumed away. G28/G32/G37: no fixed min-plus or additive-copy argument. G30: no tensoring. GD2/A5: crucially, this is the free monoid, not quotient convolution, so bicyclic units lack their multiplication identity. G33/G34, all D4 cases, E6 bounded/unbounded ports, and F289/N8 use absent geometry/algebra.

**Experiment.** Emit Fox derivatives through order three for the smallest depth-two NAND/COPY tree; compare exact minima at depths \(1,2,3\).

**Falsification/death.** An augmentation-ideal syzygy may let diagonal combinations cancel every selected derivative with only linear mass.

---

### 5. Prefix-poset Möbius countersection

**Mechanism / move.** Attempt to refute Strategy 2 via Möbius inversion on the prefix tree. Prefix equations are a zeta transform; construct a sparse signed combination of complete histories whose Möbius transform is supported only at the false root and COPY seams. If its support grows polynomially or linearly in \(h\), exponential adverse growth is impossible.

**Audit.** G1/G6/G7: the proposed witness satisfies emitted equations exactly. G12 DROP is one Möbius atom and is included. G2/G3: search is over the saturated integral incidence algebra. G14/G31/G38 do not apply. G5 private overlap, G9/G11 parity, G13 affine collision, G15 laminar lift, G19 signed flow, and GD1/ordered splice are candidate Möbius circuits rather than escaped cases. G28 is avoided because no transfer table is asserted; G32/G37 predict the likely additive witness. G30: no tensor. GD2/A5: no convolution units. G33/G34, D4 midpoint/non-antipodal/independent recombination, E6 bounded/unbounded ports, and F289/N8 have absent assumptions.

**Experiment.** Build exact prefix/COPY matrices for depths \(2\)–\(5\); use SNF plus MILP to minimize negative support for a false root.

**Falsification/death.** Occurrence-specific COPY fibers may make the Möbius determinant expand exponentially—evidence for, rather than against, FRONTIER.

---

### 6. Property-\((T)\) incidence groupoid

**Mechanism / move.** Amend Strategy 3’s scalar signs to small rational orthogonal representations attached to incidence arrows, drawn from explicit finite quotients of a property-\((T)\) group. Honest assignments form parallel sections of equal radius; a Kazhdan inequality would force every nontrivial signed section into an expanding nonbacktracking representation component.

**Audit.** G1/G6/G7: no filters or carries; transports are direct feature rows. G12 DROP has a nonparallel component and must be included. G2/G3: coercion must hold on the whole integral selector module. G14/G31/G38: representation dimension and walk depth scale, so no finite extrapolation. G5; G9/G11; G13; G15; G19; GD1/diagonal splice are explicitly tested for invariant-subrepresentation leakage. G28/G32/G37: no min-plus or orthogonal copy-additivity premise. G30: walk powers are not literal Kronecker tensors. GD2/A5: no convolution multiplication. G33/G34: no exterior tags. D4 midpoint/non-antipodal/independent recombination; E6 bounded/unbounded ports; F289/N8: no corresponding shell, port, or quaternion assumptions.

**Experiment.** Use the smallest \(2\)- or \(3\)-dimensional rational representation available; optimize transports on the nine-clause instance for \(d=1,2,3\).

**Falsification/death.** The harmful affine section may lie entirely in the trivial representation; property \((T)\) may give only additive, not multiplicative, separation.

---

### 7. Sparse Gowers-derivative walk features

**Mechanism / move.** Replace low-degree moments in Strategy 3 by \(\{\pm1\}\)-valued polynomial-phase features along walks. A non-rank-one signed local distribution has a first nonzero discrete derivative; a Reed–Muller dual-distance or uncertainty argument could force many nonzero phase coordinates at each depth while every honest assignment retains identical norm.

**Audit.** G1/G6/G7: phases act directly on selectors, with no slack, quotient, or carry. G12: DROP changes the constant phase and is audited. G2/G3: the theorem must cover unrestricted integral phase sums. G14/G31/G38: \(d=\Theta(\log m)\) and a sparse evaluation set provide a genuine family. G5; G9/G11; G13; G15; G19; GD1/ordered splice remain mandatory derivative-zero cases. Unlike G13’s killed raw linear syndrome, nonlinear lifted phases need not be constant on the honest affine span—but this must be tested. G28/G32/G37: no fixed transfer/additive metric. G30: no literal tensor. GD2/A5, G33/G34, all D4 obstructions, E6 bounded/unbounded ports, and F289/N8 have absent assumptions.

**Experiment.** Enumerate quadratic and cubic phases for \(d=1,2,3\) on the nine-clause and two-copy parity instances; solve exact zero-residual minima.

**Falsification/death.** G13 may annihilate every phase visible on one walk, or polynomial feature count may become superpolynomial.
