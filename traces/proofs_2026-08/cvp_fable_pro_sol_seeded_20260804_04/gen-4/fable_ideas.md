Obstruction labels below are repeated explicitly in each sketch: **O1 bounded local signatures; O2 marginal/tableau encodings; O3 local-view hierarchies; O4 phase lifts; O5 integer exact fibers; O6 complete-assignment fingerprints; O7 tensor amplification; O8 exact syndrome-to-CVP transfer.**

### 1. Splitter-expanded, cycle-erased Schur avalanche

**Mechanism.** Mutate I27 by replacing raw incompatibility walks with collision-rooted, vertex-simple walks in a bounded-degree splitter expansion of the 3DM conflict graph. Construct the lifted code symbolically from the ANFs of these walk products, rather than enumerating affine-fiber points.

**Expected move.** With walk length \(r=\Theta(\log q)\), polynomially many features might keep every matching at weight \(q\) while making each collision seed \(q^{\Omega(1)}\) distinct paths.

**Obstructions.** O1: outside only if growing-degree features lack an independently flippable \((r+1)\)-cube; otherwise O1 kills it. O2: no marginal tables. O3: global disconnected splitter paths, not proper connected scopes. O4: no phases. O5: binary, not integer fibers. O6: paths, not assignment columns. O7: no tensoring; every mixed lift word must still be checked. O8: directly compatible once \(H,t\) are explicit.

**Falsification/test.** Implement \(r=2,\dots,6\) on all-eight, twisted three-matching, and existing \(q=3\) suites; enumerate every mixed word and include nominal rank. Kill if either hostile word remains shell-free or rank exponent fails to beat base.

**Likely death.** A higher-dimensional affine cube cancels all selected monomials.

---

### 2. Canonical polar-butterfly folding of reduced tensors

**Mechanism.** Canonicalize the reduced tensor code’s matroid, recursively partition coordinates by shortening/contraction rank, apply the resulting CNOT butterfly \(T_F\), then retain a fixed rank-profile-selected set of outputs \(P_FT_Fx\). Unlike puncturing, every retained coordinate is a dense, formula-dependent XOR.

**Expected move.** Polarization might concentrate sparse satisfiable representatives into “good” synthetic coordinates while spreading every NO mixed word, giving subquadratic output length after a squaring step.

**Obstructions.** O1: dense linear processing cannot repair an existing cube trade, so all-eight remains a direct threat. O2: no marginals or gates. O3: no scopes. O4: no phases. O5: binary only. O6: acts on a sparse code, not assignment fingerprints. O7: explicitly occupies the unruled code-dependent dense-fold opening and must cover arbitrary mixed tensor words. O8: compatible after deriving a parity check for the image.

**Falsification/test.** On every tiny YES/NO reduced square, freeze one rank-profile recursion, enumerate all mixed words, and test all-eight and holonomy under relabelings. Require better worst-YES/best-NO rank exponent than unfurled \(25/9\).

**Likely death.** The butterfly creates low-weight NO cancellations before genuine polarization appears.

---

### 3. Fox-Jacobian twisted homology

**Mechanism.** Build a CSP presentation complex and choose formula-derived nonabelian voltages. Fox derivatives produce boundary matrices over \(\mathbb F_2[G]\); replacing each group element by its regular permutation matrix gives an explicit binary complex without multiplication tableaus.

**Expected move.** A satisfying assignment should define a sparse section, while inconsistent odd holonomy becomes a twisted homology class whose support is forced large by an expanding finite quotient \(G\).

**Obstructions.** O1: columns are global group-ring boundaries, not bounded-degree Boolean signatures. O2: no proper marginals, although any later gate compilation would re-enter O2. O3: detects fundamental-group holonomy globally. O4: outside its single-valued copy-stable phase assumptions only if the formula-derived regular action is genuinely multivalued; otherwise coboundary trivialization applies. O5: binary. O6: no assignment enumeration. O7: no tensor requirement. O8: compatible with the resulting binary boundary matrix.

**Falsification/test.** Use \(G=S_3\) and \(A_4\); construct Fox matrices for the all-eight core, twisted cycle, and one tiny YES/NO 3DM pair; enumerate pointed relative cycles.

**Likely death.** Universal YES completeness forces the voltage system to be gauge-trivial, or illegal cycles remain boundaries.

---

### 4. Sparse Macaulay–Koszul pointed code

**Mechanism.** Represent 3SAT by its Boolean polynomial ideal over \(\mathbb F_2\), but retain only clause-connected monomials and their Koszul syzygies. A satisfying assignment induces a pointed evaluation functional; use the sparse Macaulay relation matrix as a parity check and charge omitted relations with slack coordinates.

**Expected move.** Growing algebraic degree could detect all-eight trades and holonomy simultaneously, while clause-connected expansion might keep the monomial family polynomial and force NO pseudo-evaluations to use polynomially many slacks.

**Obstructions.** O1: fixed-degree truncations are squarely covered; survival requires effective degree growing with \(n\) and no free larger cube. O2: direct global relations avoid gate tables. O3: outside fixed-scope levels only if syzygies span global clause geometry. O4: no phases. O5: binary. O6: monomials are a sparse dictionary, not complete assignments. O7: no tensoring. O8: directly compatible.

**Falsification/test.** Generate degree \(D=2,3,4\) sparse Macaulay matrices for all-eight, twisted holonomy, and \(q=3\) 3DM; enumerate every pointed kernel word and count rows/columns.

**Likely death.** Low-degree pseudoexpectations survive, while the degree needed to remove them makes the matrix superpolynomial.

---

### 5. Multi-sketch trellis with shared nondeterministic choices

**Mechanism.** Stream clauses through polynomial-width trellises that retain only linear sketches \(h_j(a)\) of the partial assignment. Couple many deterministic subspace-design sketches through one shared set of literal-choice columns, so a true assignment traces compatible paths in every trellis while a splice must collide consistently across all sketches.

**Expected move.** A polynomial family of \(O(\log n)\)-bit states could replace the exponential verifier configuration graph; recursive sketch layers might turn one inconsistent splice into many Hamming charges.

**Obstructions.** O1: each sketch is linear, but the global path dictionary is not a bounded-degree local signature; cube splices remain possible. O2: ordinary wire coupling would fall under tableau/rectangle kernels, so the mechanism survives only with one global shared-choice checksum. O3: temporal paths are global scopes. O4: no phases. O5: binary. O6: polynomial trellis states, not assignments. O7: no tensoring. O8: compatible.

**Falsification/test.** For three variables, use all nonzero \(2\)-bit linear sketches; build explicit flow-incidence matrices for all-eight and twisted instances and enumerate mixed paths. Then test \(3\)-bit sketches on the existing suite.

**Likely death.** Communication-complexity collisions permit different assignments in different trellises, recreating the rectangle splice.

---

### 6. Higher Lawrence lifting and Graver-complexity amplification

**Mechanism.** Apply iterated Lawrence lifting to the exact-cover configuration: copies satisfy their own incidence equations while identity blocks globally couple coefficient differences. Toric geometry suggests that nonconformal illegal relations may require increasingly large Graver moves even though a legal matching has a simple diagonal lift.

**Expected move.** For lift order \(r=O(\log q)\), seek YES norm \(O(rq)\) but NO norm \(\Omega(r^{1+c}q)\), with matrix size only \(O(r)\) times the base size. Test both the integer lattice and its mod-2 syndrome analogue.

**Obstructions.** O1: not a local Boolean signature construction. O2: no truth tables. O3: coupling is global across copies. O4: no phases. O5: **not outside**—the lifted system remains an affine integer exact fiber, so constant-cost repairs may persist. O6: sparse triple dictionary. O7: Lawrence lifting is not tensor multiplication, though common-multiplier accounting remains relevant. O8: only the mod-2 version transfers exactly; integer-only success misses the stated route.

**Falsification/test.** Form second and third Lawrence lifts of all \(q=3\) hostile instances; enumerate signed coefficients in a certified radius and exact binary coset leaders.

**Likely death.** The original support-three or signed repair lifts diagonally with only linear overhead.
