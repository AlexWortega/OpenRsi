Below, O1–O8 refer to the numbered obstruction map in `ORACLE_BRIEF.md`.

### 1. Log-memory tail-biting trellis compiler

**Core trick.** Order the 3DM columns and route each selection vector through a tail-biting trellis whose state is an \(r=\Theta(\log m)\)-bit BCH checksum. Use one column per transition \((j,s,b)\), global flow-conservation rows, and exact-cover rows; the \(2^r=\mathrm{poly}(m)\) states permit a polynomial explicit matrix.

**Expected move.** Inconsistent signed paths should create a long convolutional-code error event rather than a constant local repair.

**Obstruction check.** O1 bounded signatures: not escaped if transitions contain an independent affine cube. O2 marginal/tableau: directly threatens the bounded transition interfaces. O3 local-view hierarchy: the tail-biting equation is global, but local flow rows may still admit holonomy. O4 phase lifts: checksum state is multivalued and graph-dependent, outside scalar coboundary assumptions. O5 integer fibers: binary construction, outside. O6 fingerprints: no complete assignments. O7 tensor amplification: no tensoring. O8 exact transfer: applies if a binary gap survives.

**Falsification/test.** Implement \(r=2,3\) on all-eight and twisted \(q=3\) instances; enumerate every mixed flow word, recording worst YES, best NO, and rank.

**Likely death.** A support-three path splice at one merge state recreates O2.

---

### 2. Nonabelian sheaf-cosystolic encoding

**Core trick.** Put an \(S_3\)- or \(A_5\)-valued constraint bundle on a small expanding 2-complex and replace scalar phases by regular-representation matrices. The explicit binary matrix is the twisted coboundary \(\delta_\rho\); legal assignments are sparse flat sections, while inconsistent assignment holonomy should become a nontrivial cosystolic class.

**Expected move.** Cosystolic expansion could charge global odd holonomy linearly while controlling every mixed section.

**Obstruction check.** O1 bounded signatures: local section columns remain linear, so cube trades may persist. O2 marginals/tableaus: applicable if the construction reduces to edge restriction maps. O3 local-view hierarchy: outside only when included 2-cells capture the full dependency; proper connected scopes remain vulnerable. O4 phase lifts: outside its single-valued abelian phase assumptions. O5 integer fibers: binary. O6 fingerprints: polynomial sheaf stalks, not assignments. O7 tensor: absent. O8 exact transfer: immediate after binary soundness.

**Falsification/test.** Build the smallest triangulated torus/projective-plane bundle with \(S_3\) regular matrices; enumerate all-eight, twisted holonomy, and all mixed pointed words.

**Likely death.** Linearized sections may make odd affine sums of flat sections flat again.

---

### 3. Branch-width dichotomy fold

**Core trick.** Compute a rank decomposition of the BMT binary matroid. If branch-width is \(O(\log n)\), solve the fiber by dynamic programming; otherwise use certified high-connectivity cuts to define a code-dependent dense map  
\[
\Phi(W)=\big(R_i^{T}W R_j\big)_{(i,j)\in E},
\]
where \(R_i\) are separator bases and \(E\) is a sparse expander on cuts.

**Expected move.** Low-width instances are decided outright; high-width instances might force every NO mixed tensor matrix to remain visible across many independent separators, with polynomial output.

**Obstruction check.** O1 bounded signatures: base is global BMT incidence, not a local signature lift. O2 marginals and O3 local scopes: separator measurements are global. O4 phases: irrelevant. O5 integer fibers: binary. O6 fingerprints: no assignment grouping. O7 tensor amplification: explicitly occupies the surviving code-dependent dense-fold opening and must handle every mixed \(W\). O8 exact transfer: applies.

**Falsification/test.** Brute-force optimal branch decompositions for existing \(m=8\) YES/NO codes, construct \(\Phi\), and enumerate all reduced-square words plus all-eight/holonomy.

**Likely death.** Branch-width protects rank/nonzeroness, not Hamming support; YES may densify more than NO, as in prior condensers.

---

### 4. Connected-set Schur closure with cycle certificates

**Core trick.** Mutate I27 by indexing each feature by a distinct connected vertex set \(S\) of the incompatibility graph, not by a walk: add \(\prod_{j\in S}x_j\) for \(|S|\le r=\alpha\log n\), then BCH-encode features grouped by their cycle-boundary signature. With bounded incompatibility degree, the number of sets is polynomial and repeated traversal no longer creates fake amplification.

**Expected move.** Matchings activate no collision set; every small collision cycle or affine-closure cheat should activate a unique connected-set class many times.

**Obstruction check.** O1 bounded signatures: degree \(r\) still has an \((r+1)\)-cube trade of polynomial support; not escaped, but that upper bound may exceed the desired gap. O2 marginals: no proper marginals. O3 local scopes: uses growing logarithmic scopes, the stated opening, and explicitly includes short holonomy cycles. O4 phases: absent. O5 integer fibers: binary. O6 fingerprints: sparse graph sets, not assignments. O7 tensor: absent. O8 transfer: applies.

**Falsification/test.** Add all connected sets through size eight on all-eight and size nine on twisted holonomy; enumerate the full lifted span.

**Likely death.** Constructing the lifted span polynomially may require \(k^{\Theta(\log n)}\) monomials, or a longer hostile cycle may evade all sets.

---

### 5. Affine min-rank space plus lossless rank-to-support condenser

**Core trick.** Quadratize 3SAT and build an explicit affine matrix space \(\mathcal M_F\) in which rank-one matrices correspond exactly to satisfying assignments. Apply a frozen family of left/right rank condensers \(L_iMR_i\), encoding each nonzero extension-field output by a simplex block, so matrix rank becomes binary block support.

**Expected move.** YES has rank one; tensor/direct-sum powering could raise NO minimum rank before condensation, while the condenser keeps output polynomial and covers mixed matrices.

**Obstruction check.** O1 bounded signatures: bilinear equations have cube relations, but the proposed discriminator is global matrix rank; whether this escapes is unresolved. O2 tableaus: direct affine matrix equations avoid gate transcripts; quadratization may reintroduce them. O3 scopes: no local-view hierarchy. O4 phases: irrelevant. O5 integer fibers: finite-field rank, outside. O6 fingerprints: polynomial matrix entries. O7 tensor: condensation must beat the rank wall for every mixed matrix, not merely pure powers. O8 transfer: applies after binary support encoding.

**Falsification/test.** Construct rank spaces for all-eight and twisted instances over \(\mathbb F_4\); enumerate all matrices and all one-dimensional left/right projections.

**Likely death.** Condensers preserve nonzeroness but flatten rank classes, inflating rank-one YES support almost as much as NO.

---

### 6. Generalized Lawrence–Graver defect amplification

**Core trick.** Apply an \(r\)-fold generalized Lawrence lifting to the integer exact-cover matrix, using coupling rows that charge inter-copy disagreement while storing the common coefficient vector only once. Toric theory suggests primitive nonmatching fiber elements may acquire “type” \(\Omega(r)\), whereas a Boolean matching remains diagonal and sparse.

**Expected move.** Convert the \(q\) versus \(q+2\) integrality defect into many compulsory disagreement blocks without multiplying the full YES baseline by \(r\).

**Obstruction check.** O1 bounded signatures, O2 marginals, O3 scopes, and O4 phases: not the mechanism. O5 integer exact fibers: directly applicable unless the lifting proves that every old constant repair necessarily becomes high-type; this is the central danger. O6 fingerprints: no assignments. O7 tensor: Lawrence lifting is not a tensor product, though rank accounting remains mandatory. O8 exact transfer: unnecessary for direct CVP, but available after mod-two reduction.

**Falsification/test.** Form two- and three-copy Lawrence matrices for the existing \(q=3\) signed YES/NO fibers; enumerate coefficients in \([-2,2]\), including all-eight and holonomy-derived matrices.

**Likely death.** The old weight-\(q+2\) odd cover embeds diagonally, leaving the same additive ratio and confirming O5.

---

### 7. Fermionic/Pfaffian defect sectors

**Core trick.** Express the constraint system as a tensor network and apply holographic basis changes so equality and matching constraints become matchgates. Represent the residual non-matchgate part of each clause by explicit fermionic defect modes; global consistency is then measured by Pfaffians and low-order Pfaffian minors rather than a bounded-fan-in determinant circuit.

**Expected move.** A satisfying assignment occupies one Gaussian sector with sparse defect vector, while UNSAT should require many independent fermionic excitations; Pfaffian evaluation remains polynomial.

**Obstruction check.** O1 bounded signatures: clause residuals of bounded degree remain vulnerable unless the global Gaussian coupling destroys independent cubes. O2 tableaus: outside only if Pfaffian rows are written directly, not circuit-linearized. O3 local scopes: global covariance matrix is outside proper-scope assumptions. O4 phases: no scalar phase selector. O5 integer fibers: finite-field binary realization. O6 fingerprints: covariance entries are polynomially many. O7 tensor: no ordinary tensor amplification; arbitrary superposed Gaussian sectors still require proof. O8 transfer: applies to the final binary matrix.

**Falsification/test.** Decompose the three-variable OR signature over \(\mathbb F_2\) or \(\mathbb F_4\), then enumerate defect support for all-eight, holonomy, and every mixed sector.

**Likely death.** General OR has irreducible non-matchgate content, and low-order Pfaffian minors may admit the same support-three virtual clauses.
