I use five obstructions from the current map:

- **O1 Slack-zero:** non-Boolean integer slacks can annihilate every amplified residual.
- **O2 Affine-coordinate:** CVP coordinates must be affine-linear in lattice coefficients; quadratic Booleanity tests are invalid without linearization.
- **O3 Correlated cancellation:** joint integer directions may cancel all amplified blocks.
- **O4 Scaling:** repetition may increase completeness cost as fast as soundness, yielding no \(n^c\) gap.
- **O5 Evidence:** the eight-clause computation is finite and does not transfer automatically to other constructions.

## 1. Local satisfying-pattern simplices

**Core trick.** Give each clause seven integer selectors \(y_{c,a}\), one per satisfying local assignment, with linear equations \(\sum_a y_{c,a}=1\) and marginal consistency with global variables. Targeting the barycenter \((1/7,\ldots,1/7)\) makes the closest integral points in that affine hyperplane exactly the seven unit vectors; encode consistency defects through a high-distance integer code.

**Expected move.** Completeness has zero consistency syndrome. Soundness must either produce a codeword of weight \(\Omega(D)\) or use signed, non-one-hot selectors that leave the minimum simplex shell.

**Obstruction check.** **O1:** no clause slack exists. **O2:** selectors, marginals, and coding are affine. **O3:** not cleared—signed selectors may satisfy every consistency equation. **O4:** code coordinates cost zero in completeness, but the \(O(m)\) simplex baseline remains; require \(D\gg m\). **O5:** no extrapolation is assumed.

**Falsification.** Find an unsatisfiable instance with exact consistency and selector shell cost within \(O(1)\) of completeness.

**Smallest experiment.** Use the all-eight-clause formula, \(y_{c,a}\in[-2,2]\), and a 16-row binary or integer expander matrix; solve exactly by enumeration/MILP.

**Likely death.** The signed affine fiber contains near-unit decompositions encoding a fractional or cancellation-based satisfying assignment.

## 2. CRT/Construction-A syndrome spreading

**Core trick.** Replace freely adjustable equality slacks by congruence syndromes modulo several small primes. If every short witness has defects \(|d_i|<P=\prod p_j\), then a nonzero integer defect cannot vanish modulo every prime; a Construction-A code can spread its surviving residue over \(D\) coordinates.

**Expected move.** Valid Boolean selectors give zero syndrome, while any bounded nonzero defect pays \(\Omega(D)\) with no replicated completeness charge.

**Obstruction check.** **O1:** the old \((-1,0)\) slack is absent; adding multiples of primes is bounded out rather than cheaply anchored. **O2:** congruences are represented by affine lattice bases. **O3:** a combined defect divisible by \(P\), or an exact signed-selector solution, still cancels everything. **O4:** potentially favorable because only zero-completeness syndromes are spread; dimension-versus-\(D\) must be calculated explicitly. **O5:** this specifically tests, rather than assumes, the unsupported multi-prime branch.

**Falsification.** Exhibit a below-threshold witness whose defects are all zero or multiples of \(P\).

**Smallest experiment.** Primes \(2,3,5\), \(P=30\), 16-fold residue spreading, all-eight-clause formula, selectors in \([-3,3]\); enumerate every vector below the proposed radius.

**Likely death.** The real obstruction is an exact integral relaxation, so every modular syndrome is zero before coding.

## 3. Tensoring a complete CVP coset gadget

**Core trick.** Search for a homogenized tensor operation on lattice cosets under which completeness witnesses tensor and NO distances multiply. A uniform base ratio \(\gamma>1\), tensor-powered \(k=\Theta(\log N)\) times, would give \(\gamma^k=N^{\Omega(1)}\) while dimension grows exponentially in \(k\).

**Expected move.** Convert a genuine constant-gap, formula-uniform gadget into a polynomial gap without PCP-style constraint amplification.

**Obstruction check.** **O1:** tensoring does not repair a base exact-zero slack branch; the base gadget must already exclude it. **O2:** tensor-product lattices remain linear, but homogenizing an affine target without introducing rank-one constraints is unresolved. **O3:** “entangled” tensor-lattice vectors may be much closer than pure tensors. **O4:** this is aimed directly at scaling, but multiplicativity is only a hypothesis. **O5:** the observed \(\sqrt{27/19}\) on one formula is not a valid base lemma.

**Falsification.** Find a second-power vector closer than the product of the two base optima, or show completeness does not tensor.

**Smallest experiment.** Extract the explicit basis and target of the existing eight-clause gadget, implement one candidate homogenized Kronecker construction for \(k=2\), and solve exact CVP by branch-and-bound.

**Likely death.** Tensor-product minima are controlled by non-pure vectors, and affine coset distance is not multiplicative.

## 4. Number-field norm forcing

**Core trick.** Encode each affine defect as an algebraic integer and include all Minkowski embeddings. If a nonzero defect is forced into an ideal of norm \(Q\), the product formula plus AM–GM gives a Euclidean lower bound from its nonzero field norm, whereas a valid assignment has exactly zero defect.

**Expected move.** Obtain amplification from ideal norm or extension degree without duplicating the completeness shell coordinate-by-coordinate.

**Obstruction check.** **O1:** ideal forcing eliminates ordinary free slacks only if the selector system has no exact signed solution. **O2:** multiplication by fixed algebraic integers is an integer matrix in an integral basis, hence affine; no \(s(s-1)\) is used. **O3:** conjugates cannot cancel across orthogonal embedding blocks, but different selector defects may cancel before embedding. **O4:** one must compare \(Q^{1/[K:\mathbb Q]}\), discriminant, coefficient size, and final dimension; no polynomial gap is yet established. **O5:** this is a fresh explicit test of the previously unverified algebraic-number branch.

**Falsification.** Find a zero algebraic defect from signed selectors, or show the norm lower bound becomes subconstant relative to completeness after normalization.

**Smallest experiment.** Use \(K=\mathbb Q(\sqrt2)\), basis \(1,\sqrt2\), ideal \((3)\), and the eight-clause selector system; enumerate coefficients in \([-3,3]\).

**Likely death.** Units or degree dilute the additive Euclidean gain, while exact integral-relaxation cheats remain norm zero.

## 5. Homological systole amplification

**Core trick.** Represent variable choices and clause patterns as integer chains, with consistency defects given by a boundary map. Arrange that unsatisfiability creates a nonzero relative homology class, then lift the complex to one with large systole so every representative of that class has large support.

**Expected move.** Satisfying assignments are exact cycles, while NO instances pay \(\Omega(D)\) boundary or representative norm with zero amplified completeness cost.

**Obstruction check.** **O1:** no scalar clause slack is present, though adding boundaries may become its homological analogue. **O2:** chain and boundary maps are integral-linear. **O3:** cancellation by boundaries is exactly the issue tested by homology and Smith normal form; it is not assumed away. **O4:** a family with systole \(D\) and controlled cell count could yield scaling, but the exponent is unknown. **O5:** the finite formula only supplies the first complex, not an asymptotic theorem.

**Falsification.** Compute that the alleged obstruction class is zero, or find a constant-support representative in every tested lift.

**Smallest experiment.** Build the clause-variable incidence 2-complex for all eight clauses, take its smallest nontrivial 2-lifts, compute Smith normal forms, and use MILP to minimize support in each relevant coset.

**Likely death.** Homology naturally detects parity-like inconsistencies, whereas arbitrary OR-unsatisfiability may leave no nontrivial topological class.

## 6. Expander nullspace / Graver isolation

**Core trick.** Seek an integer measurement matrix \(A\) whose short points in the relevant affine fibers are exactly the one-hot local-pattern vectors. Expander-style sparse recovery or a lower bound on nonzero Graver elements could force every signed fake satisfying \(Az=b\) to have norm \(N^{1/2+c}\).

**Expected move.** Replace nonlinear Booleanity with a geometric integer nullspace property: valid assignments remain short, but every exact linear-relaxation cheat becomes long.

**Obstruction check.** **O1:** there are no independently adjustable slacks; cheats must lie in \(\ker_{\mathbb Z}A\). **O2:** the construction is entirely affine-linear. **O3:** correlated cancellation is precisely a short kernel or Graver vector, so it is directly searchable. **O4:** a polynomial lower bound on the shortest harmful kernel vector would provide the missing scaling move; none is known. **O5:** random small matrices provide only falsification evidence, not a reduction.

**Falsification.** Find a low-norm kernel vector that moves one legal selector configuration to a signed illegal one while preserving all marginals.

**Smallest experiment.** Generate all left-regular \(0/1\) matrices with 12–20 columns for a two-clause overlapping core, then enumerate \(\ker_{\mathbb Z}A\cap[-3,3]^n\) and compute relevant Graver elements.

**Likely death.** A single linear map cannot isolate a large, nonconvex SAT-dependent set without short differences between legal and illegal encodings.

## 7. Discriminant-group coset gluing

**Core trick.** Encode truth values as equal-norm representatives of cosets in a small lattice’s discriminant group, then glue variable and clause blocks using a high-distance subgroup code. Discreteness comes from coset geometry rather than polynomial Booleanity; a clause gadget would make its seven satisfying labels short and the eighth label distant.

**Expected move.** Consistent satisfying labels occupy a short glued-lattice shell, while either an inconsistent label word has code distance \(\Omega(D)\) or a falsifying local coset pays a large norm.

**Obstruction check.** **O1:** no free integer clause slack exists if short coset representatives are classified exactly. **O2:** Construction-A/glued lattices have explicit affine integer bases. **O3:** hidden glue words may combine several bad labels into a short lattice vector. **O4:** code distance can grow with zero consistency cost, but the local-shell baseline and final dimension require accounting. **O5:** the eight-clause case must be enumerated before any family claim.

**Falsification.** Prove that every projected subgroup relation is affine and therefore cannot realize the seven-of-eight OR relation, or find a short hidden glue word.

**Smallest experiment.** Enumerate binary Construction-A lattices from codes of length at most 8, with one or two auxiliary labels, and classify nearest representatives for all eight clause patterns.

**Likely death.** Subgroup closure forces affine relations; “all patterns except one” is non-affine unless nearest-shell geometry introduces auxiliaries that may themselves create cheats.

Classical ingredients invoked only as starting points: Construction A and lattice gluing (Conway–Sloane), expander codes (Sipser–Spielman, 1996), Graver bases (Graver, 1975), Minkowski embeddings/product-formula bounds, and Smith normal form. No prohibited document or derivative source was consulted.
