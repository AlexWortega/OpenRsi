I use the following obstruction labels: **O1** RS/residual amplification defeated by free integer slack, including unchanged algebraic/multi-prime variants; **O2** fixed-marginal affine isolation is only local and constant-size; **O3** private-row overlap admits short and jointly compensating kernel moves; **O4** no polynomial dimension-gap law; **O5** no complete full-rank CVP basis/target/radius construction.

### 1. Global modular syndrome followed by an error-correcting code

**Core trick.** Replace private clause measurements by one global syndrome over \(\mathbb F_p\), containing normalization, every variable-consistency defect, and every false-clause indicator. Encode that syndrome with an explicit linear \([M,q,\delta M]_p\) code and realize the resulting coset through Construction A.

**Expected move.** If every illegal integer selector has nonzero syndrome, code distance gives squared soundness \(\Omega(M)\). Taking \(M=m^k\) against completeness \(O(m)\) would produce an explicit polynomial ratio.

**Map check.** O1: no free residual slack; every auxiliary column participates in the syndrome. O2: checks are global, not fixed-marginal local certificates. O3: joint overlap moves are allowed but must lie in the global syndrome kernel. O4: code distance supplies the proposed scaling law. O5: Construction A plus HNF can output a full-rank basis, but target and completeness accounting remain unfinished.

**Falsification.** Find a nonassignment signed selector with zero syndrome mod \(p\), or a short centered representative of a nonzero codeword.

**Smallest experiment.** Use the all-eight-clause core, \(p=3\), and the ternary \([13,3,9]\) simplex code; compute exact minimum distance by MILP and construct the lattice basis by HNF.

**Likely death.** Modular pseudoassignments annihilate the syndrome before coding.

---

### 2. Expander lift with direct energy rounding

**Core trick.** Make \(R\) copies of every variable and clause, route occurrences through an explicit constant-degree bipartite expander, and penalize disagreement across expander edges. Prove directly—not by invoking a PCP theorem—that either each variable fiber rounds to one value, forcing \(R\) lifted clause violations, or expansion exposes \(\Omega(R)\) disagreement edges.

**Expected move.** With shared anchors costing \(O(m)\) but lifted soundness \(\Omega(R)\), \(R=m^k\) would give ratio \(m^{(k-1)/2}\) in dimension \(O(Rm)\).

**Map check.** O1: no clause slack; penalties are selector disagreement and false-pattern coordinates. O2: this abandons the 18 local survivors. O3: all overlap moves are globally coupled through expander edges, though compensation remains possible. O4: the displayed \(R\)-law is explicit. O5: the block matrix is constructible and HNF gives a basis, but achieving shared rather than replicated completeness cost is unresolved.

**Falsification.** Find an integer selector configuration with few false-clause and disagreement coordinates despite unsatisfiability.

**Smallest experiment.** Lift the eight-clause core by \(R=4\) using \(K_{4,4}\) minus a matching; solve the exact closest-vector ILP, including joint signed moves.

**Likely death.** Completeness energy also scales as \(R\), leaving only a constant ratio; alternatively the rounding lemma effectively recreates forbidden PCP machinery.

---

### 3. Number-field norm amplifier without slack directions

**Core trick.** Map the complete global defect vector \(d=(d_0,\ldots,d_{q-1})\) to the algebraic integer \(\alpha=\sum d_i\theta^i\) in a degree-\(D>q\) number field, and place all Archimedean embeddings of \(\alpha\) in the CVP objective. If \(d\neq0\), then \(\alpha\neq0\), \(|N(\alpha)|\ge1\), and AM–GM gives \(\|\sigma(\alpha)\|_2\ge\sqrt D\).

**Expected move.** Set \(D=m^k\); if completeness stays \(O(\sqrt m)\), the absolute \(\sqrt D\) lower bound becomes polynomial.

**Map check.** O1: unlike the killed algebraic variant, no unmeasured slack may alter \(d\); this distinction must be verified. O2: embedding amplifies a global defect, not a fixed local fiber. O3: not escaped if a signed overlap move makes \(d=0\) before embedding. O4: \(D\) is the proposed gap parameter. O5: algebraic embeddings require rational approximation and separation bounds, so a legal rational basis/target is still missing.

**Falsification.** Find a zero global defect pseudoassignment, or show valid vectors have embedding norm comparable to soundness because of discriminant/height growth.

**Smallest experiment.** In Sage, use \(K=\mathbb Q(2^{1/8})\), encode the eight-clause defect coefficients, enumerate short selectors, and compare exact field norms and Minkowski norms.

**Likely death.** The pre-embedding defect map retains the Generation-5 kernel cheats.

---

### 4. CRT spreading plus a range certificate

**Core trick.** Measure each integral global defect modulo many small primes. A nonzero defect \(|d|\le B\) is divisible by at most \(\log_2 B\) distinct primes, so among \(L\) prime blocks it is nonzero in \(L-O(\log B)\); add digit/range rows intended to make \(|d|>B\) itself expensive.

**Expected move.** Valid assignments have defect zero in every block, while any invalid bounded defect pays \(\Omega(L)\) squared norm. Taking \(L=m^k\) proposes the required polynomial scaling.

**Map check.** O1: the killed multi-prime route allowed free slack to set the defect exactly to zero; here every auxiliary and carry must be measured. If that fails, O1 applies unchanged. O2: the measured quantity is global. O3: overlap circuits still kill the mechanism if they produce exact zero defect. O4: prime-count spreading gives the candidate law. O5: modular lattices have HNF bases, but the range gadget and completeness radius remain unspecified.

**Falsification.** Find a short choice of auxiliaries making \(d\) a primorial multiple, or a cheap carry chain defeating the range certificate.

**Smallest experiment.** Use primes \(2,3,5,7\) on the eight-clause core; include binary digit rows and solve the unbounded integer quadratic program exactly.

**Likely death.** Linear CVP constraints cannot certify a bounded integer range without introducing precisely the carry/slack directions being attacked.

---

### 5. Homological obstruction in a cosystolic complex

**Core trick.** Encode selector inconsistencies as cochains in a global chain complex built from the formula incidence structure. Arrange satisfiable instances so the target cochain is a coboundary, while unsatisfiability places it in a nonzero cohomology coset; a cosystolic lower bound would force every representative of that coset to have support \(\Omega(N)\).

**Expected move.** Construction A applied to the boundary matrix converts coset support into Euclidean distance \(\Omega(\sqrt N)\), with zero or controlled completeness distance.

**Map check.** O1: there are no residual slacks; auxiliaries are chains quotiented only by explicit boundaries. O2: the invariant is global homology, not fixed marginals. O3: jointly compensating overlap moves are exactly boundaries and therefore explicitly included in the quotient. O4: the cosystole is the scaling law. O5: boundary matrices and HNF yield a full-rank modular lattice and target, although the SAT-to-cohomology equivalence is unproved.

**Falsification.** Exhibit a small boundary-supported representative of the alleged unsatisfiable coset, or show that every formula-generated class is trivial.

**Smallest experiment.** Build the incidence complex of the eight-clause core times a 5-cycle; compute all mod-2 coset leaders and integral lifts by exhaustive linear algebra.

**Likely death.** Arbitrary 3SAT unsatisfiability does not naturally define a nontrivial cohomology class without a gap-producing preprocessing step.

---

### 6. Exterior-power / determinant rigidity

**Core trick.** Arrange global selector data as columns of an integer matrix that should be decomposable or rank one for a consistent assignment. Illegal configurations create a nonzero integral minor; premultiplying and postmultiplying by explicit totally nonsingular matrices can spread one nonzero minor across many coordinates of the compound matrix.

**Expected move.** An integral minor has magnitude at least one, while \(k\)-th compound spreading could yield \(\Omega(M^k)\) nonzero coordinates in dimension \(M^{O(k)}\), giving a polynomial norm law for fixed \(k\).

**Map check.** O1: no residual slack is used. O2: rank is a global invariant rather than local affine isolation. O3: overlap compensation is harmless only if it cannot preserve all minors. O4: compound-matrix support supplies the proposed amplifier. O5: the fatal missing step is linear realization—CVP does not automatically compute minors.

**Falsification.** After introducing lifted minor variables, find a short “fake Plücker” vector satisfying every linear incidence equation but not arising from any matrix.

**Smallest experiment.** Use \(2\times4\) selector matrices for the eight-clause core, introduce six \(2\times2\) minor variables, impose all linear relations available after fixing one column, and enumerate the integer kernel through squared norm \(16\).

**Likely death.** Decomposability is governed by quadratic Plücker relations, which a lattice coset cannot enforce linearly.

---

### 7. Boolean-algebra characters and Nullstellensatz fanout

**Core trick.** View assignments as characters of \(A=\mathbb Z[x_1,\ldots,x_n]/(x_i^2-x_i)\). Encode moments of a purported character and multiplication-table audits globally; an unsatisfiable formula has \(1\) in its Boolean clause ideal, so applying a genuine character would force a unit defect.

**Expected move.** Express a certificate as a balanced straight-line computation and fan each nonzero multiplication-gate defect into \(m^k\) audited coordinates. This would convert algebraic inconsistency into polynomial Euclidean energy without clause slack.

**Map check.** O1: clause violations are ideal identities, not residuals cancellable by free slack. O2: moments and multiplication audits are global. O3: private-row circuits are outside the model, but global pseudocharacters may replace them. O4: balanced fanout is only a proposed law; certificate degree and size must be polynomial. O5: no linear CVP construction yet enforces multiplicativity, positivity, or characterhood.

**Falsification.** Find an integral low-degree pseudocharacter satisfying all audited multiplication rows and clause equations with small norm.

**Smallest experiment.** For the eight-clause core, include all multilinear monomials through degree three, generate the truncated multiplication table, and compute exact rational and integer kernels plus the shortest non-character witness.

**Likely death.** General formulas require high-degree certificates, while linearized moments admit pseudocharacters unless one imports an SOS/PCP-strength theorem.

Classical ingredients referenced: Construction A as presented in Conway–Sloane, *Sphere Packings, Lattices and Groups*, 3rd ed. (1999); expander-code distance/rounding ideas from Sipser–Spielman, “Expander Codes,” *IEEE Transactions on Information Theory* 42 (1996).
