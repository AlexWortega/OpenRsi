Below are five deliberately divergent, untested mutations. None uses the prohibited source.

### 1. Bounded-occurrence cluster Möbius lift

**Core trick.** Start from bounded-occurrence 3DM, making the triple-incompatibility degree constant. Add coordinates for every splitter-decorated connected induced cluster of at most \(r=\Theta(\log q)\) triples containing a collision; use the full Möbius basis on each cluster rather than repeated walk products, so matchings pay zero while duplicate walk traversals cannot masquerade as amplification.

**Expected move.** Output size is \(m(e\Delta)^r=\mathrm{poly}(m)\); prove every NO mixed word activates \(q^{\Omega(1)}\) minimal collision clusters.

**Obstruction check.** **Bounded signatures:** not escaped—degree \(r\) still admits \((r+1)\)-cube trades. **Marginals/tableaus:** no wire marginals. **Local hierarchies:** logarithmic scopes are outside the fixed-level theorem, but long odd holonomy remains uncovered. **Phase lifts:** no phases. **Integer fibers:** binary construction. **Fingerprints:** clusters, not complete assignments. **Tensor amplification:** no tensoring; soundness concerns the entire lifted span. **Exact transfer:** Gaussian elimination produces binary \(H,t\), so transfer applies.

**Smallest experiment.** Mutate `verify_nonbacktracking_schur_walks.py` to enumerate connected subsets and their ANF/Möbius features for \(r=2,3,4\), testing all-eight, holonomy, affine-closure, and held-out 3DM.

**Likely death.** A global alternating cube cancels every cluster feature.

---

### 2. Fermionic block-wedge dictionary

**Core trick.** Regard a triple \((a,b,c)\) as three fermionic creation operators. On overlapping vertex blocks \(B\) of logarithmic size, record exterior products in  
\(\Lambda(\mathbb F_2^B)^{\otimes3}\): a matching produces canonical volume elements, while multiplicity-three vertices in odd covers annihilate wedges. Use explicit splitters so every small multiplicity defect is isolated in many blocks.

**Expected move.** Obtain polynomial rank \(q\,2^{O(|B|)}\), constant YES support per block, and polynomial NO support from repeated annihilation patterns.

**Obstruction check.** **Bounded signatures:** not fully outside; block wedges have degree \(O(\log q)\), hence larger cubes may trade. **Marginals/tableaus:** exterior states are joint antisymmetric functions, not proper marginals. **Local hierarchies:** overlapping logarithmic blocks exceed fixed scope, but odd holonomy may still cancel. **Phase lifts:** antisymmetry is multivalued, not a copy-stable scalar phase. **Integer fibers:** binary exterior algebra. **Fingerprints:** only block states, no assignment columns. **Tensor amplification:** exterior products replace tensor powering; every span word still requires checking. **Exact transfer:** binary linearization yields \(H,t\).

**Smallest experiment.** For \(q=3\), use all vertex blocks of sizes two and three; construct exterior-state vectors for every affine-fiber point and enumerate their full span.

**Likely death.** Odd XORs of legal Fock states may annihilate exactly on all blocks.

---

### 3. Growing quasirandom nonabelian fold

**Core trick.** Replace the killed fixed \(A_4\) fold by a growing family \(G=\mathrm{SL}_2(\mathbb F_p)\). Assign canonical Sidon-like labels \(g_i\) to tensor coordinates and send ordered pair \((i,j)\) to buckets \(g_i a g_j^{-1}\) for several Cayley-expander probes \(a\), retaining binary matrix-coefficient blocks from multiple irreducible representations.

**Expected move.** Product-growth/quasirandomness might force every high-complexity NO mixed matrix to occupy many buckets, while Sidon labels keep legal pure squares sparse.

**Obstruction check.** **Bounded signatures:** not escaped—dense postprocessing preserves any pre-existing cube trade. **Marginals/tableaus:** no marginal interface, although base cheats survive. **Local hierarchies:** globally mixes all ordered pairs; odd holonomy is not automatically excluded. **Phase lifts:** formula-dependent nonabelian labels lie outside scalar coboundary classification. **Integer fibers:** binary. **Fingerprints:** labels coordinates, not assignments. **Tensor amplification:** exactly the surviving code-dependent dense-fold opening; must handle every mixed tensor word. **Exact transfer:** its binary image directly supplies \(H,t\).

**Smallest experiment.** Implement \(G=\mathrm{SL}_2(\mathbb F_5)\), eight canonical labels, two Cayley probes, and all six binary matrix coefficients; enumerate the existing hostile suite without label tuning.

**Likely death.** Quasirandomness controls rank/nonzeroness, not Hamming support; YES densifies faster than NO.

---

### 4. Voltage-lifted cosystolic classifier

**Core trick.** Build a formula-dependent voltage lift of the 3DM incidence complex into an explicit high-girth Cayley 2-complex. Legal matchings receive canonical one-sheet fillings, whereas an odd cover induces nontrivial nonabelian monodromy; binary syndrome rows record lifted boundaries and selected cosystolic checks.

**Expected move.** YES uses \(q+O(1)\) cells, while every NO chain either violates incidence or represents a class with systole \(qN^c\).

**Obstruction check.** **Bounded signatures:** local boundary rows do not escape cube trades; success requires genuinely global cosystolic rows. **Marginals/tableaus:** ordinary edge interfaces are covered, but direct deck-transformation rows are not proper marginals. **Local hierarchies:** the full lift sees global cycles, outside proper-scope assumptions; collision forests may remain invisible. **Phase lifts:** graph-dependent, multivalued voltages are outside copy-stable scalar phases. **Integer fibers:** binary chains. **Fingerprints:** polynomial cells, no assignments. **Tensor amplification:** no tensor; systole must cover every chain combination. **Exact transfer:** the boundary/cocycle matrix is already binary.

**Smallest experiment.** Attach an \(A_5\) voltage lift to the \(q=3\) holonomy and affine-closure dictionaries; enumerate lifted chain fibers and compare legal fillings with every mixed illegal chain.

**Likely death.** Linearity makes an odd XOR of cheap legal fillings another cheap filling, regardless of systole.

---

### 5. Function-field gonality shell

**Core trick.** Assign each triple a rational function on an explicit high-gonality curve. Legal matchings should sum to a fixed divisor class with a degree-\(q\) representative, while signed odd covers in the same incidence fiber are forced—by pole-order and Riemann–Roch constraints—to use a representative of degree \(\Omega(g)\).

**Expected move.** Taking genus \(g=qN^c\) would produce a polynomial distance gap using only polynomially many valuation and residue coordinates.

**Obstruction check.** **Bounded signatures:** growing-degree divisor data is outside fixed-degree cube assumptions; fixed jets would not be. **Marginals/tableaus:** valuations are global functions, not wire marginals. **Local hierarchies:** full divisor classes see global dependence and holonomy. **Phase lifts:** no local phases. **Integer fibers:** finite-field divisor arithmetic, not affine integer slacks. **Fingerprints:** one function per triple, not per assignment. **Tensor amplification:** no tensor; the gonality claim must cover the entire linear span. **Exact transfer:** expand field symbols with a simplex inner code, then compute binary \(H,t\).

**Smallest experiment.** On genus-one/two curves over \(\mathbb F_8\), search triple labels for the \(q=2\) all-eight and \(q=3\) suites; enumerate minimum divisor-support representatives.

**Likely death.** Requiring every legal matching to share a cheap class may force every odd affine combination into that class too.
