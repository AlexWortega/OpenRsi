## 1. Affine-coset-aware relative-weight condenser

**Core trick.** Treat the reduced tensor instance as the flagged pair \(K\subset D=K+\langle v\rangle\), not merely the kernel \(K\). Construct a canonical stack of dense maps \(P_s\) satisfying \(P_sv\notin P_sK\), selected using relative-rank profiles of \((D,K)\), and weight blocks so that sparse representatives of the pointed coset concentrate while other pointed words activate many blocks.

**Expected move.** Compress 64 tensor coordinates while retaining more of the \(25/9\) NO/YES ratio than generator-type or polar shortening.

**Obstruction check.** **Bounded local signatures:** inherited cube-trade words remain; linear maps do not erase their relations, so this is not outside that obstruction for such words. **Marginal/tableau:** no marginal or gate transcript. **Local-view hierarchies:** uses the complete affine pair globally. **Phase lifts:** no phase. **Integer exact fibers:** binary construction. **Complete-assignment fingerprints:** columns remain the sparse 3DM dictionary. **Tensor amplification:** asymmetric, target-dependent dense maps—not fixed puncturing or type merging—but mixed words still require enumeration. **Exact transfer:** directly compatible after producing \(H',t'\).

**Falsification/experiment.** On all-eight, holonomy, and one \(q=3,m=8\) YES/NO pair, use SAT/MILP to find \(8\)-to-\(r\) maps constrained by \(Pv\notin PK\); enumerate every image word. Kill if any hostile pointed kernel occurs or best NO \(\le\) worst YES.

**Likely death.** Relative-rank profiles protect nonzeroness, not Hamming support.

---

## 2. Perfect-hash zeon powering

**Core trick.** For each splitter \(h:[m]\to[r]\), lift \(x\) to coefficients of  
\[
\prod_{j:x_j=1}(1+y_{h(j)})\quad\text{in}\quad \mathbb F_2[y_1,\ldots,y_r]/(y_i^2).
\]
A perfect-hash family ensures every small support has injectively colored subsets, potentially retaining \(\binom{|x|}{r}\)-type growth using only \(2^{O(r)}\operatorname{poly}(m)\) coordinates.

**Expected move.** Obtain powered support with \(r=\Theta(\log m)\), avoiding full pure-power dimension and random-sampling failures.

**Obstruction check.** **Bounded local signatures:** degree is \(r\); the cube theorem still applies to independently flippable cubes larger than \(r\), so this is not fully outside it. **Marginal/tableau:** direct global monomials, no wire interfaces. **Local-view hierarchies:** splitters see arbitrary global subsets. **Phase lifts:** none. **Integer exact fibers:** binary. **Complete-assignment fingerprints:** no assignment columns, provided the lifted span is generated symbolically. **Tensor amplification:** structured deterministic discard, not exact tensor representation; all mixed lifted words must be checked. **Exact transfer:** compatible.

**Falsification/experiment.** For \(m=8,r=3\), use all \(3^8\) colorings, construct lifted spans for all-eight, holonomy, and existing 3DM fibers, then enumerate minima. Kill if hostile affine XORs lose all colorful terms.

**Likely death.** Symbolically constructing the lifted span may itself require exponentially many Boolean functions; cube cancellations may persist asymptotically.

---

## 3. Nonabelian holonomy with Fox-derivative coordinates

**Core trick.** Associate the ordered incidence structure with a word in a finite nonabelian group; legal matchings admit a short null-homotopy, whereas collisions or twisted permutations should create nontrivial holonomy. Encode lifted paths using Fox derivatives or twisted boundary matrices over several finite representations, so orientation survives rather than collapsing to ordinary \(\mathbb F_2\)-homology.

**Expected move.** Charge odd permutation holonomy and illegal affine covers by representation support or filling length.

**Obstruction check.** **Bounded local signatures:** genuinely global word order may remove independent local cubes; any bounded-degree truncation does not. **Marginal/tableau:** outside only if twisted boundaries are emitted directly; a local path automaton re-enters tableau assumptions. **Local-view hierarchies:** the complete closed walk is measured. **Phase lifts:** graph-dependent, multivalued selectors lie outside the coboundary theorem; copy-stable single-valued versions do not. **Integer exact fibers:** not an affine slack repair. **Complete-assignment fingerprints:** polynomial group-state dictionary is intended. **Tensor amplification:** no tensoring, but every mixed chain remains relevant. **Exact transfer:** binary expansion yields \(H,t\).

**Falsification/experiment.** Use \(UT_3(\mathbb F_3)\) or \(S_3\), build twisted boundary columns for all-eight and the twisted three-matching instance, and enumerate every pointed combination.

**Likely death.** Succinctly enforcing prefixes requires local state interfaces, while direct global columns may be exponential; characteristic-two representations may also abelianize the crucial obstruction.

---

## 4. Error-locator elimination over an algebraic curve

**Core trick.** Replace local matching tables by the elimination ideal of  
\[
Ax=\mathbf1,\qquad x_i^2-x_i=0,
\]
and represent a fiber point through its global locator polynomial \(\Lambda_x(Z)=\prod_{i:x_i=1}(Z-\alpha_i)\). Hasse derivatives and evaluations on an explicit curve would encode symmetric powers of the error divisor compactly, with AG-code distance intended to amplify locator-degree differences.

**Expected move.** Turn weight \(q\) versus \(q+2\) into many derivative/evaluation disagreements without enumerating tensor coordinates.

**Obstruction check.** **Bounded local signatures:** locator degree grows globally; low-degree truncations remain covered. **Marginal/tableau:** direct elimination/evaluation, not gate tableaux. **Local-view hierarchies:** depends on the full support divisor. **Phase lifts:** none. **Integer exact fibers:** finite-field algebra, not count slacks. **Complete-assignment fingerprints:** outside only if a polynomial Gröbner/resultant representation is generated without listing fiber points. **Tensor amplification:** symmetric powering is compressed algebraically; arbitrary mixed locator combinations remain the central soundness issue. **Exact transfer:** binary trace expansion is compatible.

**Falsification/experiment.** In Sage, for \(q=3,m=8\) over \(\mathbb F_{17}\), eliminate the Boolean fiber, compute locator evaluations through derivative order three, binary-expand, and enumerate the resulting span plus hostile instances.

**Likely death.** Elimination size may be exponential or implicitly decide perfect matching; virtual mixed locators may have much smaller support than genuine locators.

---

## 5. Twisted higher-Lawrence lifting and Graver growth

**Core trick.** Place several copies of the 3DM incidence fiber in a higher-Lawrence lifting, coupled through sheet-dependent unimodular transforms of pair-projection coordinates. The intended toric phenomenon is that a Boolean matching has a coherent low-norm lift, while a signed odd cover requires a large Graver move across many incompatible sheets.

**Expected move.** Multiply the \(q\) versus \(q+2\) integrality defect without paying \(q\) independently in every projection table.

**Obstruction check.** **Bounded local signatures:** coupling is global, but affine local sheet repairs may still survive. **Marginal/tableau:** no bounded-fan-in transcript; pair projections alone remain vulnerable to rectangle kernels. **Local-view hierarchies:** every sheet contains the full incidence system. **Phase lifts:** sheet twists are not phases, although coboundary-like untwisting is possible. **Integer exact fibers:** this is dangerously close; if a constant-cost affine repair survives all twists, Obstruction 5 applies directly. **Complete-assignment fingerprints:** polynomial triple/sheet variables. **Tensor amplification:** Lawrence lifting is additive, not tensor multiplication. **Exact transfer:** unnecessary for direct CVP, though parity reduction remains available.

**Falsification/experiment.** Use three sheets of the \(q=3,m=8\) systems, deterministic Vandermonde/unimodular twists, and exact search over coefficients in \([-2,2]\); include diagonal odd covers, all-eight, and holonomy.

**Likely death.** Repeating the same illegal cover in every sheet may neutralize all couplings, or legal coherence may restore the linear YES baseline.

---

## 6. Noncommutative collision transfer operators

**Core trick.** Mutate Schur walks by replacing scalar walk monomials with entries of a labeled transfer operator
\[
T_x=\sum_{(i,j)\in E}x_ix_j\,E_{ij}\otimes L_{ij},
\]
where \(E\) is the triple-incompatibility graph and \(L_{ij}\) are deterministic noncommuting matrices. Output entries of \(T_x,T_x^2,\ldots,T_x^r\); matchings have \(T_x=0\), while collisions generate orientation-sensitive words that cannot cancel merely by sharing endpoints.

**Expected move.** Preserve I27’s finite collision amplification while defeating the all-eight and three-matching cancellations of commutative walk features.

**Obstruction check.** **Bounded local signatures:** degree \(2r\), so large flippable cubes remain an honest threat. **Marginal/tableau:** direct global matrix products, unless implemented through gate transcripts. **Local-view hierarchies:** walks can span the whole incompatibility graph. **Phase lifts:** no scalar phase. **Integer exact fibers:** binary nonlinear lift. **Complete-assignment fingerprints:** polynomially many edge/matrix coordinates. **Tensor amplification:** not ordinary tensoring or puncturing; soundness must cover the entire mixed lifted span. **Exact transfer:** compatible after binary expansion.

**Falsification/experiment.** Freeze \(r=4\), \(L_{ij}\in M_4(\mathbb F_2)\) from canonical companion-matrix words, then rerun the I27 YES/NO suite, all-eight, holonomy, and affine-closure attacks.

**Likely death.** Polynomial identities in small matrix algebras or affine XORs may still annihilate every transfer block; increasing matrix size may destroy polynomial output accounting.
