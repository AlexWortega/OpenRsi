I use these obstruction labels in every audit: **S** = Generation-1 free-slack annihilation; **L** = fixed-marginal local isolation failing under overlap; **U** = constraints imposed only by the verifier, not the lattice; **P** = four-variable odd-component mod-2 bypass; **T** = changing-reference rather than single-target auditing; **X** = exponentially listed assignment relations; **G** = bounded evidence or constant-distance repetition without a polynomial gap.

### 1. Tensor amplification of an unrestricted affine-coset gap

**Core trick.** Search for a constant-dimensional lattice coset whose legal selector states have radius \(R\), while every harmful signed state has radius at least \((1+\epsilon)R\), with no externally imposed constraints. Tensor only this constant amplifier \(k=\Theta(\log N)\) times and attach it to each global syndrome, aiming for ratio \((1+\epsilon)^k=N^c\) in polynomial dimension.

**Expected move.** Prove a multiplicative minimum-distance theorem for the chosen affine cosets, not ordinary direct sums.

**Obstruction check.** **S:** no slack variables. **L:** amplification follows a global syndrome; constructing that syndrome remains unresolved, so L could still kill it. **U:** all conditions must occur in the emitted basis. **P:** use integral, not binary, syndromes; mixed-tensor analogues remain possible. **T:** one tensor target only. **X:** a constant tile has explicit generators. **G:** logarithmic tensor depth would supply the missing polynomial law if multiplicativity holds.

**Falsification.** A mixed-rank tensor vector below the predicted product radius.

**Smallest experiment.** Tensor each Generation-3 local survivor with itself; exactly enumerate the unrestricted doubled coset, then repeat using the saved nine-clause four-variable instance.

**Likely death.** Tensor cancellation makes coset minima submultiplicative.

---

### 2. Superincreasing “no-carry” selector locking

**Core trick.** Give every local truth-table label a dissociated mixed-radix signature and couple clause selectors directly to global variable-choice coefficients. Choose the radix from an assumed soundness-radius coefficient bound, so a close vector cannot use signed selectors or carries to imitate another label.

**Expected move.** Any non-Boolean close vector has a first unmatched digit costing \(W=N^{c+1}\), while an honest satisfying vector pays only the unscaled anchor cost.

**Obstruction check.** **S:** no residual slack exists. **L:** signatures reference global variables, not private/free marginals; whether this truly eliminates overlap circuits is the main test. **U:** every digit equation and scale is embedded in the lattice. **P:** exact integer uniqueness replaces mod-2 coding. **T:** all assignments are compared with one target. **X:** one signature per occurrence is polynomial; large entries still have polynomial bit length. **G:** the explicit weight \(W\) promises a polynomial gap, conditional on the no-carry lemma.

**Falsification.** An unrestricted close vector with signed selectors whose large digits cancel.

**Smallest experiment.** Build the mixed-radix basis for the all-eight-clause core and the nine-clause edge-cover formula; solve exact bounded CVP while deriving coefficient bounds from the tested radius rather than imposing them externally.

**Likely death.** The target must accommodate both Boolean choices, creating affine dependencies that defeat dissociation.

---

### 3. Number-field ideal syndromes with unit caging

**Core trick.** Encode each nonzero consistency or clause syndrome as an algebraic integer in a prescribed ideal coset and include all Minkowski embeddings as Euclidean coordinates. Add a coefficient cage intended to prevent multiplication by units, so the field norm forces at least one conjugate to be polynomially large.

**Expected move.** With degree \(\Theta(\log N)\), a nonzero ideal class would create an \(N^c\)-scale conjugate while honest syndromes vanish.

**Obstruction check.** **S:** unlike Generation 1’s algebraic-number variant, no slack may solve the syndrome exactly; otherwise S applies unchanged. **L:** use one global ideal module; local ideals alone remain vulnerable to overlap circuits. **U:** embeddings, ideal generators, and cages must all be actual basis rows. **P:** no mod-2 quotient, though odd-prime or unit analogues may exist. **T:** one Minkowski target. **X:** polynomial defining data if field degree is logarithmic. **G:** norm growth is the proposed asymptotic law, not repetition.

**Falsification.** A unit or short ideal element keeping every embedding near the completeness radius.

**Smallest experiment.** Use quadratic and quartic fields on the all-eight core; enumerate unrestricted algebraic coefficients, then run the four-variable parity-bypass instance.

**Likely death.** Dirichlet-unit balancing neutralizes the large conjugate, leaving only a \(\sqrt{\log N}\) effect.

---

### 4. Homological syndrome with a high-systole mapping cone

**Core trick.** Represent occurrence consistency and clause legality as boundary maps of an integral chain complex. Attach the formula complex to an explicit high-systole complex through a mapping cone, aiming to make every unsatisfied assignment induce a nontrivial homology class whose shortest representative has polynomial support.

**Expected move.** Completeness gives a boundary of small norm; soundness gives a nonzero class requiring \(\Omega(N^{2c})\) squared norm.

**Obstruction check.** **S:** there are no equation-solving slacks. **L:** homology is global; private clause cycles are killed only if the attachment map is injective on them. **U:** boundary matrices define the actual lattice. **P:** work integrally or with several odd torsion orders, but the odd-component witness may reappear as homology and must be checked. **T:** one fixed chain target. **X:** sparse boundary matrices are polynomial-size. **G:** systolic growth would be the dimension-dependent theorem.

**Falsification.** A short boundary adjustment trivializing the class, especially one supported on a single clause.

**Smallest experiment.** Form mapping cones for the two-clause overlap systems and the nine-clause edge-cover instance; compute SNF plus exact shortest representatives of every relevant coset.

**Likely death.** Formula attachment introduces low-systole handles even when the ambient complex has large systole.

---

### 5. A formula-dependent deep hole with a legal first shell

**Core trick.** Seek a lattice and single deep-hole target whose entire first nearest-vector shell encodes globally consistent Boolean assignments. Clause rows perturb satisfying shell points only slightly, while every unsatisfying or signed configuration is forced onto a second shell with polynomially larger radius.

**Expected move.** Replace linear enforcement of nonnegativity by a geometric shell gap: illegality means leaving the legal Voronoi face.

**Obstruction check.** **S:** no slack or residual cancellation. **L:** legality is global shell membership, not fixed local marginals; a short overlap circuit would manifest as an extra first-shell vector. **U:** unrestricted nearest-vector enumeration is exactly the soundness question. **P:** no binary quotient. **T:** intrinsically one fixed deep-hole target. **X:** require a sparse polynomial basis, not an assignment list. **G:** the second/first-shell ratio must be proved \(N^c\), rather than merely constant.

**Falsification.** Any signed pseudoassignment appearing on the first shell, or a universal geometric bound forcing adjacent-shell ratios near one.

**Smallest experiment.** Search dimensions 4–12 for integral Gram matrices whose nearest vectors realize the eight assignments of the three-variable core; then add its eight clause perturbations and enumerate two shells exactly.

**Likely death.** Euclidean lattices with exponentially many first-shell vectors may necessarily have a nearby second shell.

---

### 6. Expanderized deterministic computation histories

**Core trick.** Compile formula evaluation into a deterministic Boolean circuit and encode complete gate histories using truth-table selectors. Replicate each wire over an explicit expander and enforce every propagation edge in the lattice, so forcing the output to “accept” on an unsatisfiable formula should spread inconsistency across many coordinates.

**Expected move.** An integral Poincaré-type lemma turns one false output into \(\Omega(N)\) violated propagation coordinates, iterated to obtain a polynomial distance ratio.

**Obstruction check.** **S:** gate tables use no free residual slack. **L:** shared wires are globally expander-coupled, not freed private marginals; signed gate-table circuits remain a direct threat. **U:** all gate and propagation checks are basis coordinates. **P:** use integer or odd-modulus checks and test the known parity instance. **T:** one accepting-history target. **X:** circuit and expander are polynomial-size. **G:** all edges are checked deterministically; the required spectral-to-Euclidean amplification theorem is still absent.

**Falsification.** A signed harmonic history that interpolates between inconsistent gates with low energy.

**Smallest experiment.** Encode one OR gate, then the four-variable nine-clause checker, using cycles and 3-regular expanders; solve unrestricted exact CVP for increasing replication sizes.

**Likely death.** Selector combinations realize low-energy fractional/signed histories despite expansion.

---

### 7. Compressed Nullstellensatz moment obstruction

**Core trick.** Use Boolean and clause polynomials to build a sparse moment lattice: satisfying assignments give evaluation vectors annihilating all ideal rows. For unsatisfiable formulas, a compressed arithmetic-circuit Nullstellensatz certificate would make every approximately consistent moment vector violate a coded block of coordinates.

**Expected move.** Obtain a polynomial-size straight-line representation of the relevant certificate action, then spread its nonzero constant term without listing assignments or monomials.

**Obstruction check.** **S:** no integer slack can zero a false clause polynomial unless the moment equations themselves admit it. **L:** the ideal is global, so overlap is included; low-degree pseudo-moments may nevertheless reproduce the short circuits. **U:** moment and certificate operators must be explicit lattice rows. **P:** work over \(\mathbb Z\) and audit reductions modulo several primes, including the known mod-2 bypass. **T:** use one affine moment target. **X:** circuit compression is intended to replace exponential assignment differences, but is wholly unproved. **G:** certificate degree/height must yield polynomial Euclidean separation.

**Falsification.** A low-degree signed pseudoexpectation satisfying every emitted row on the nine-clause instance.

**Smallest experiment.** Generate degree-2 through degree-4 Macaulay matrices for both finite cores; compute exact affine coset minima and modular kernels.

**Likely death.** General unsatisfiable 3-CNFs require exponentially large degree or certificate representation.
