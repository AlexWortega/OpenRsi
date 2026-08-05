I did not use or consult the prohibited document or related material.

**Obstruction key:** O1 bounded local signatures; O2 marginal/tableau encodings; O3 local-view hierarchies; O4 phase lifts; O5 integer exact fibers; O6 complete-assignment fingerprints; O7 tensor amplification/compression; O8 exact syndrome-to-CVP transfer.

1. **Permutahedral Delaunay shell — untested**

**Core trick.** Search for a polynomial-dimensional rational quadratic form whose equal nearest lattice points encode every permutation table, while every signed row-sum-one nonpermutation is polynomially farther. Couple the three pair projections of 3DM to three such orbit shells without making their table entries explicit objective variables.

**Expected move.** Replace I18’s linear permutation-table baseline by a multiplicative Voronoi gap.

**Checks.** O1: outside only if built from a global orbit lattice, not local-view columns; otherwise cube trades kill it. O2/O3: no marginals or scopes. O4: no phases. O5: non-affine nearest-orbit geometry is outside its slack assumptions, but a standard table realization is not. O6: uses Coxeter generators, not assignment fingerprints. O7: no amplification claim; its reduced square must still pass all mixed words. O8: require polynomial rank, bit size, and honest shell radius accounting.

**Smallest experiment.** For \(q=3\), use SDP/linear inequalities to seek a positive-definite Gram matrix separating all six permutations from every signed table in \([-2,2]^9\); then attach tiny 3DM and test all-eight, holonomy, and the reduced square.

**Likely death.** Parallelogram identities force an illegal affine combination onto the same or a comparable ellipsoid shell.

2. **Deterministic isolation menu plus protected centers — untested**

**Core trick.** Construct a polynomial family of linear hashes \(h_s\) such that some branch isolates a satisfying matching from every syndrome solution below an amplified cutoff. For each \((s,h_s(x))\), use a BCH-type shell, then combine branches through a selector that permits one sparse center but charges odd superpositions of branches.

**Expected move.** Obtain canonical-witness behavior without actually finding the witness.

**Checks.** O1: hashes are global; a local selector would re-enter O1. O2/O3: no view consistency, but a bounded-fan-in branch selector is covered and forbidden. O4: this is a genuinely formula-dependent global selector, outside O4’s local-phase theorem. O5: binary construction, no integer slacks. O6: hashes sparse matching vectors, not all assignments. O7: no tensor dependence; nevertheless enumerate every mixed word after one square. O8: the branch/target menu must be polynomial and YES baseline include selector cost.

**Smallest experiment.** On all \(q=3,m=8\) dictionaries, enumerate affine hashes of 1–4 bits; find the smallest family isolating each perfect matching from all covers of weight at most five. Build the literal block-selector syndrome and attack all-eight and holonomy.

**Likely death.** Polynomial deterministic isolation is unavailable, or the selector admits the same rectangle/odd-branch splice as I05/I10.

3. **Nonabelian filling-area amplifier — untested mutation of I11**

**Core trick.** Replace linear homology by a finite group presentation: matching exchanges are short relators, legal witnesses bound \(O(q)\)-area van Kampen diagrams, while illegal odd covers—even when homologically trivial—should require \(q^{1+c}\) area. Encode bounded diagram positions as syndrome columns, augmented by nonabelian labels or Fox derivatives to prevent XORing three cheap legal fillings.

**Expected move.** Separate affine-closure cheats by filling area rather than homology class.

**Checks.** O1/O2: outside only if whole relator words are columns; cell-by-cell interfaces are covered. O3: global Dehn area sees holonomy. O4: no scalar phases. O5: nonlinear reduced-word validity is outside affine fibers, but linearizing it may restore exact repairs. O6: no assignment columns. O7: independent of tensors; test all mixed words after any product. O8: the finite diagram complex and binary boundary matrix must remain polynomial, including area baseline.

**Smallest experiment.** Build presentations for the 32 affine-closure counterexamples from `verify_exchange_quotient.py`; breadth-first enumerate diagrams through area 12 and compare matching versus illegal boundary areas. Also test all-eight and twisted holonomy.

**Likely death.** Any polynomial binary chain encoding linearizes fillings, so XORs of three cheap legal diagrams remain cheap; preserving nonabelian reduction requires an exponential tableau.

4. **Noncommutative ABP hitting-set lift — untested**

**Core trick.** Represent assignments as source-to-sink paths in a layered algebraic branching program whose edge labels are noncommuting clause symbols. Evaluate the whole path polynomial on a fixed polynomial family of matrices; accepting paths should have a sparse designated signature, whereas every mixed superposition in an unsatisfiable fiber should survive on many evaluations by noncommutative identity testing.

**Expected move.** Turn global ordered consistency, rather than rank alone, into Hamming support.

**Checks.** O1: matrix entries have path-length degree, not bounded local degree. O2: ordinary path-flow rows are bounded interfaces and remain vulnerable; success requires dense transfer rows to enforce pathness. O3: paths span the whole formula, including odd holonomy. O4: no phases. O5: binary evaluations, no slacks. O6: polynomial edge dictionary, not assignment columns. O7: evaluations must be checked against every mixed tensor word, not pure paths. O8: count binary-expanded matrix entries and worst YES support.

**Smallest experiment.** Encode the three-variable all-eight formula and twisted-cycle instance in depth 3–6 ABPs; exhaust \(2\times2\) matrices over \(\mathbb F_4\), freeze a tiny evaluation family, and enumerate the full lifted span and reduced square.

**Likely death.** Path-flow pseudoassignments survive the evaluations, or matrix expansion preserves nonzeroness but repeats I30’s YES-dense/NO-sparse support flattening.

5. **Sparse Koszul/resultant systole — untested**

**Core trick.** Regard Boolean clauses as a sparse polynomial system and construct a truncated Koszul or Macaulay complex directly from their monomial supports. A satisfying assignment should induce a short homology representative; in an unsatisfiable system, effective Nullstellensatz exactness plus expansion of the differential is hoped to force every representative of the target class to have polynomially larger support.

**Expected move.** Obtain a genuinely global algebraic dictionary with a norm-versus-ideal-membership theorem.

**Checks.** O1: outside only when truncation degree grows beyond every available Boolean cube. O2/O3: no marginal tables or scopes. O4: no phase labels. O5: global ideal membership is not bounded-degree slack, although constant truncation is covered. O6: columns are sparse monomials/syzygies, not complete assignments. O7: no tensor premise; any later power must enumerate mixed cycles. O8: Macaulay rank and monomial count must be polynomial, with sparse SAT representative explicitly bounded.

**Smallest experiment.** Construct degree \(D=2,3,4\) complexes for all eight 3-clauses, a satisfiable deletion, and twisted holonomy; compute minimum-weight representatives by exhaustive linear algebra, then square the smallest cases.

**Likely death.** Useful Nullstellensatz degree is \(\Theta(n)\), making the monomial complex exponential; low degree recreates finite-difference pseudoassignments.

6. **Divided-power defect sectors — untested**

**Core trick.** In a divided-power/Witt algebra, Boolean coefficients have no repeated-index sector, while \(z_j=-1,2,\ldots\) create nonzero terms such as \(\binom{z_j}{2}\). Lift exact-cover vectors into selected repeated-index ghost components and protect those components with a high-distance code, aiming to amplify I18’s constant integrality defect without replicating its \(q\) honest baseline.

**Expected move.** Charge signed non-Boolean coefficients multiplicatively while Boolean matchings pay zero auxiliary cost.

**Checks.** O1: growing divided-power degree is outside bounded-degree cubes; fixed degree is not. O2/O3/O4: no marginals, scopes, or phases. O5: genuinely nonlinear coefficient ghosts are outside affine slack assumptions, but any bounded-fan-in multiplication tableau is covered. O6: coordinates are coefficient-indexed, not assignment-indexed. O7: linearizing pure powers risks I22’s mixed-word dimension wall; all mixed lifts must be tested. O8: count ghost coordinates and square-row weights, not just symbolic degree.

**Smallest experiment.** For the 40 tiny I18 instances, compute degree-2/3 ghost signatures for every \(z\in[-2,2]^8\); then form the linear span of lifted Boolean fiber points and enumerate every mixed word, including all-eight and holonomy.

**Likely death.** Ghost coordinates are nonlinear in lattice coefficients; their polynomial linearization either admits mixed cancellations or requires exponentially many monomials.

7. **Global rearrangeable-routing congestion shell — untested**

**Core trick.** Encode each pair-projection permutation as \(q\) globally chosen source-to-sink paths in a Beneš/superconcentrator network. Use squared edge congestion, recursively weighted across network levels, so valid permutations have low-disjoint routings while a signed nonpermutation simultaneously consistent with all three projections should create many unavoidable collisions.

**Expected move.** Convert one local integrality defect into congestion across \(\Theta(\log q)\) global layers.

**Checks.** O1: whole-path columns are global; switch-view columns are covered. O2: conventional flow conservation factors through bounded interfaces and is obstructed; only a path-column formulation escapes. O3: all routing layers jointly see holonomy. O4: no phases. O5: quadratic congestion is global, but ordinary integer edge loads retain I18-style baselines. O6: polynomial path dictionary, not assignments, provided canonical path count is polynomial. O7: no tensor reliance; reduced-square mixed words still require attack. O8: include \(q\log q\) legal routing cost, path-column count, and final binary rank.

**Smallest experiment.** Use the \(q=3\) or padded \(q=4\) Beneš network; enumerate all path routings for legal permutations and every signed pair-table arising in the tiny 3DM suite. Optimize fixed level weights before freezing, then test all-eight and holonomy.

**Likely death.** Rectangle superpositions splice legal routings, while congestion raises the YES baseline as quickly as the defect—reproducing I18/I19 in network form.
