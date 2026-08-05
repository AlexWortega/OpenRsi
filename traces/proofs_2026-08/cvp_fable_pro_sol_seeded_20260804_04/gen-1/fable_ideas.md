## 1. Syndrome-conditioned high-order jet fold

**Core trick / expected move.** Regard reduced pure-power words as multilinear polynomials on the affine syndrome fiber \(x_0+\ker H\). Keep a code-dependent family of order-\(q\) Hasse derivatives: a weight-\(q\) monomial has one top derivative, whereas weight \(q+2\) exposes \(\binom{q+2}{q}=\Theta(q^2)\); an explicit subspace design might retain this separation with polynomially many jets.

**Obstruction check.**  
1. **Bounded local signatures:** derivative order grows with \(q\), and directions depend globally on \(H\); outside fixed-degree/local-cube assumptions.  
2. **Marginal/tableau:** no proper marginals or gates.  
3. **Local-view hierarchies:** one global affine fiber, not scopes.  
4. **Phase lifts:** no phases.  
5. **Integer exact fibers:** not safely outside—mixed-polynomial cancellations may be constant-cost repairs.  
6. **Complete-assignment fingerprints:** jets act on a polynomial sparse dictionary, not assignment columns.  
7. **Tensor amplification:** deliberately discards most power-space dimensions; soundness must cover every mixed polynomial.  
8. **Exact transfer:** compatible if the jet image is binary; output rank equals retained jets.

**Smallest experiment / falsification.** For \(q=3,m\le10\), enumerate all mixed degree-3 words; greedily/ILP-select derivative directions and test all-eight, odd-holonomy, and tiny 3DM fibers. Falsify upon any NO mixed word with jet weight at most worst YES.

**Likely death.** Polynomially many jets miss a cancellation subspace, reproducing sampled-fold overfitting.

---

## 2. Prony–Hankel support certificate with an exterior shell

**Core trick / expected move.** Assign distinct field points \(a_j\) to triple columns and form moments \(s_r=\sum_j x_j a_j^r\). A support-\(q\) vector has Hankel rank at most \(q\), while a genuine support-\(q+2\) vector should expose a nonzero \((q+1)\)-minor; encode that zero-versus-nonzero defect with a high-distance outer code, giving nearly zero YES baseline.

**Obstruction check.**  
1. **Bounded local signatures:** minors have degree \(q+1\), globally coupling all selected triples; outside bounded degree, but any bounded-degree truncation is covered.  
2. **Marginal/tableau:** direct moments, not wire interfaces.  
3. **Local-view hierarchies:** global support rank sees holonomy only indirectly.  
4. **Phase lifts:** no phases.  
5. **Integer exact fibers:** determinant linearization may reintroduce exact low-cost repairs; not outside.  
6. **Complete-assignment fingerprints:** only \(O(m)\) triple moments, not assignment features.  
7. **Tensor amplification:** exterior powers must be sound for arbitrary mixed tensors, not merely \(x^{\otimes r}\).  
8. **Exact transfer:** requires a polynomial-row binary realization; explicit minors may violate rank accounting.

**Smallest experiment / falsification.** Over \(\mathbb F_{17}\), build \(q=3\) Hankel matrices for every signed/odd cover in the tiny 3DM suite; enumerate free linearized minor variables and all-eight/holonomy attacks.

**Likely death.** Arbitrary mixed lifts fake low Hankel rank, while explicit exterior coordinates are exponential.

---

## 3. Nonabelian holonomy with Fox-derivative rows

**Core trick / expected move.** Build a formula-dependent nonabelian presentation whose legal exact covers trace null words, while an inconsistent odd cover leaves nontrivial global holonomy. Evaluate Fox derivatives in several polynomial-size finite-group representations; expansion of the resulting group-algebra vector could force every nontrivial word to occupy many coordinates.

**Obstruction check.**  
1. **Bounded local signatures:** full ordered products are unbounded-degree global signatures; outside unless truncated.  
2. **Marginal/tableau:** no affine wire marginals if group products are inserted directly.  
3. **Local-view hierarchies:** targets the missing global dependency explicitly.  
4. **Phase lifts:** outside the proved theorem’s single-valued, copy-stable abelian/coboundary setting; nevertheless a broader gauge collapse is possible.  
5. **Integer exact fibers:** local relator implementations would fall back inside this obstruction; direct global representation rows are essential.  
6. **Complete-assignment fingerprints:** labels triples/relations, not complete assignments.  
7. **Tensor amplification:** no tensor is required; the analogue is every mixed group-algebra/Fox combination.  
8. **Exact transfer:** binary matrix coefficients permit transfer; representation degree and number must remain polynomial.

**Smallest experiment / falsification.** For the all-eight core and twisted cycle, search \(S_3\), \(D_{10}\), then \(A_5\) edge labels; construct regular-representation Fox matrices and enumerate every syndrome-fiber combination.

**Likely death.** Universal completeness forces the presentation to trivialize illegal words too, or abelianization restores the support-three trade.

---

## 4. Perfect-hash witness sectors with a global selector code

**Core trick / expected move.** Construct a deterministic polynomial family of colorings such that every perfect matching is isolated in at least one seed. In each seed, a BCH-like shell protects the isolated color profile; combine seeds using one global MDS selector rather than quotienting all legal witnesses, so odd affine superpositions should activate several expensive sectors.

**Obstruction check.**  
1. **Bounded local signatures:** seed profiles are global; local color signatures alone remain covered.  
2. **Marginal/tableau:** the selector must be one dense equation system, not bounded-fan-in disjunction gates.  
3. **Local-view hierarchies:** isolation is over whole matchings, including holonomy.  
4. **Phase lifts:** seeds are formula-dependent multivalued selectors, outside copy-stable phases.  
5. **Integer exact fibers:** a linear selector may admit constant-cost branch splicing; not outside.  
6. **Complete-assignment fingerprints:** only polynomial seeds are allowed, but successful isolation may implicitly demand exponentially many witness labels.  
7. **Tensor amplification:** no tensor; enumerate every mixed sector superposition.  
8. **Exact transfer:** straightforward for binary selector matrices, with total seed-block length explicitly counted.

**Smallest experiment / falsification.** On \(q=3\) 3DM, enumerate low-degree polynomial colorings, synthesize the smallest selector matrix by SAT/ILP, and attack all mixed coefficients, all-eight, and odd holonomy.

**Likely death.** Information-theoretic splitter size becomes exponential in \(q\), or three cheap sectors splice into a cheap illegal sector.

---

## 5. Tropical common-base valuation barrier

**Core trick / expected move.** View a 3DM matching as a common base of three partition matroids. Assign several lexicographic/tropical valuations to triples so that a legal common base has a uniquely minimal tropical monomial, while an odd cover violates a tropical Plücker relation; expose valuation digits as heavily separated integer coordinates, aiming for zero legal defect and polynomial illegal cost.

**Obstruction check.**  
1. **Bounded local signatures:** leading-term selection is global and degree \(q\), outside fixed-degree cubes.  
2. **Marginal/tableau:** direct tropical minors avoid gates; a circuit implementation does not.  
3. **Local-view hierarchies:** common-base valuation is global and can see odd holonomy.  
4. **Phase lifts:** no cycle phases.  
5. **Integer exact fibers:** digit/carry variables would re-enter the exact-fiber obstruction; valuations must be direct coefficients.  
6. **Complete-assignment fingerprints:** danger is real—explicit basis monomials are complete-witness columns and exponential.  
7. **Tensor amplification:** no ordinary tensor; all signed tropical cancellations require analysis.  
8. **Exact transfer:** this is direct integer CVP, so squared-gap and rank accounting must be proved separately.

**Smallest experiment / falsification.** For \(q=3\), search small integer valuations, enumerate every matching and signed odd cover, and test whether any polynomial-size valuation family separates them before constructing digit rows.

**Likely death.** Three-way common bases lack a polynomial determinant representation; succinct evaluation uses forbidden tableaux, while explicit monomials cost \(q!\).

---

## 6. Krawtchouk/Johnson weight transformer

**Core trick / expected move.** Map a binary vector \(x\) to parities on all \(k\)-subsets. Its image weight is exactly a Krawtchouk function \(f_k(|x|)\), independent of the witness’s location; search weighted combinations of \(k\)’s with \(f(q)\) small and \(f(q+2)\) polynomially larger, then compress the highly symmetric metric through the Johnson association algebra.

**Obstruction check.**  
1. **Bounded local signatures:** the map is linear, so it cannot erase an existing affine cube trade; only a base family without that trade can benefit.  
2. **Marginal/tableau:** no marginals.  
3. **Local-view hierarchies:** depends only on global weight, so holonomy is invisible except through added weight.  
4. **Phase lifts:** irrelevant.  
5. **Integer exact fibers:** binary parity avoids integer slacks; Euclidean spectral compression may reintroduce them.  
6. **Complete-assignment fingerprints:** rows index subsets of coordinates, not assignments, but their count may be exponential.  
7. **Tensor amplification:** this is a direct weight transform; mixed tensor words are inapplicable, but every fiber vector must be checked.  
8. **Exact transfer:** uncompressed binary rows transfer exactly; compressed Bose–Mesner rank must be polynomial and metric-exact.

**Smallest experiment / falsification.** For \(m\le16\), compute all \(f_k\), optimize nonnegative block weights, then explicitly test the tiny 3DM/all-eight/holonomy fibers and attempt a rational low-rank Gram realization.

**Likely death.** Polynomial-size \(k\) choices transform nearby small weights only linearly; useful \(k\) requires exponentially many rows.

---

## 7. Nonlinear filling area via a high-Dehn presentation

**Core trick / expected move.** Give each legal matching a short null-homotopy in a formula-dependent presentation, but route illegal odd superpositions through a group with a large Dehn function, so they require polynomially more 2-cells even when homologically trivial. Encode filling coefficients in an integer lattice, attempting to charge filling area rather than homology class.

**Obstruction check.**  
1. **Bounded local signatures:** word reduction is globally ordered and unbounded-degree.  
2. **Marginal/tableau:** outside only if null-homotopies are not assembled through local gate tables.  
3. **Local-view hierarchies:** explicitly distinguishes global filling from proper-scope consistency.  
4. **Phase lifts:** uses nonabelian fillings, not single-valued phases.  
5. **Integer exact fibers:** ordinary cellular boundary equations are exactly inside this obstruction; a genuinely nonlinear area theorem is required.  
6. **Complete-assignment fingerprints:** cells encode triples/relations, not assignments.  
7. **Tensor amplification:** no tensor; all signed combinations of fillings are the required mixed-word analogue.  
8. **Exact transfer:** a linear boundary lattice gives direct CVP, but output rank must count all cells and subdivision.

**Smallest experiment / falsification.** Build presentations for \(q=3\) instances; enumerate minimum van Kampen diagrams or solve bounded filling ILPs for every legal matching and odd cover, including all-eight and twisted holonomy cases.

**Likely death.** Passing to an abelian lattice forgets word order, and the XOR/sum of three cheap legal fillings is automatically another cheap filling.
