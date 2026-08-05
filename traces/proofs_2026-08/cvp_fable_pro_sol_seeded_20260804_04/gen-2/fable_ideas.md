Below are six independent, deliberately nonconvergent sketches. None uses PCP machinery or the prohibited source.

### 1. Rank-condensed Veronese separator

**Mechanism.** From a polynomial-time affine basis \(v\) of the BMT pointed fiber, represent a mixed quadratic word by a coefficient matrix \(M\), not by all tensor coordinates. Stack explicit rank-condensers \(\Phi_i(M)\) so rank-one matrices retain the usual squared distance, while every rank-\(\ge2\) pointed matrix should activate many output blocks.

**Expected move.** Obtain tensor-like gap squaring in \(O(k^2\operatorname{polylog} k)\) rank instead of \(m^2\), provided low output weight forces \(M=vv^\top\).

**Obstruction check.** (1) **Bounded local signatures:** global message matrices, not bounded local views. (2) **Marginal/tableau:** no wire marginals. (3) **Local-view hierarchies:** no scopes. (4) **Phase lifts:** no phases. (5) **Integer exact fibers:** binary rank/support theorem, not slack scaling. (6) **Complete-assignment fingerprints:** \(O(k^2)\) matrix dictionary, no assignment columns. (7) **Tensor amplification:** directly addresses every mixed \(M\), not just pure powers. (8) **Exact transfer:** output is an explicit binary \(H,t\), so transfer applies.

**Falsification.** A rank-two pointed \(M\) is as cheap as the worst YES rank-one matrix, or output rank erases the exponent.

**Smallest experiment.** For existing \(q=3,m=8\) codes, enumerate all \(M\), testing all-eight and twisted-holonomy instances.

**Likely death.** Rank condensers detect rank but flatten Hamming support.

---

### 2. Formula-dependent nonabelian spectral lift

**Mechanism.** Put voltages from a nonabelian expander group on the formula-incidence graph and form its polynomial-size permutation lift. A satisfying assignment should admit one short pointed section, whereas nontrivial ordered holonomy should force any section to have large boundary by Cayley-graph expansion.

**Expected move.** Amplify one global consistency defect across polynomially many sheets without replicating the YES support across every sheet.

**Obstruction check.** (1) **Bounded local signatures:** outside only if columns encode whole lifted transitions; a bounded-degree local voltage signature remains covered. (2) **Marginal/tableau:** local state-transition linearization may re-enter its support-three attacks. (3) **Local-view hierarchies:** the sheet index records global holonomy rather than proper scopes. (4) **Phase lifts:** outside the stated single-valued, copy-stable model because the selector is formula-dependent, nonabelian, and multisection-valued. (5) **Integer exact fibers:** binary boundary expansion, no slacks. (6) **Complete-assignment fingerprints:** only graph-sheet columns. (7) **Tensor amplification:** no tensoring; enumerate every lifted-code word. (8) **Exact transfer:** applies if the lifted boundary system yields binary \(H,t\).

**Falsification.** A support-three splice or short nontrivial section survives.

**Smallest experiment.** Use \(S_3\) or \(A_4\) lifts of all-eight and twisted-cycle cores; enumerate sections and all superpositions.

**Likely death.** Universal completeness forces voltages to gauge-trivialize, or local transition rectangles return.

---

### 3. Compressed Macaulay/coordinate-ring shell

**Mechanism.** Form the Boolean formula ideal and compute a degree-\(r\) Macaulay quotient, but retain only normal-form basis elements reachable from the pointed affine fiber. Weight degree layers geometrically, aiming for sparse evaluation vectors at genuine Boolean solutions while virtual odd covers require high-degree normal forms.

**Expected move.** With \(r=\Theta(\log n)\), a polynomial Hilbert function could provide polynomial rank while turning constant local defects into polynomial weighted cost.

**Obstruction check.** (1) **Bounded local signatures:** not safely outside—if normal forms remain degree below an independently flippable cube, finite differences give a polynomial-support cheat. (2) **Marginal/tableau:** no proper marginals or gate transcripts. (3) **Local-view hierarchies:** growing global degree is outside the fixed-scope theorem, though output explosion is exactly its warning. (4) **Phase lifts:** irrelevant. (5) **Integer exact fibers:** quotient multiplication is global; bounded-degree truncation may nevertheless reproduce its repairs. (6) **Complete-assignment fingerprints:** basis consists of monomial classes, not assignments. (7) **Tensor amplification:** all quotient elements, including mixed monomials, must be enumerated. (8) **Exact transfer:** multiplication matrices over \(\mathbb F_2\) give binary syndrome systems.

**Falsification.** Hilbert rank becomes superpolynomial or a low-weight pseudoassignment survives.

**Smallest experiment.** Compute degree \(2\!-\!6\) Gröbner/Macaulay bases for all-eight, twisted-cycle, and tiny 3DM families.

**Likely death.** Low-degree pseudoexpectations persist until the quotient has exponential dimension.

---

### 4. Seeded sparse-recovery certificates with a protected OR selector

**Mechanism.** Use an explicit splitter family of hashes. For each seed, a shared sparse-recovery transcript certifies that a candidate support behaves like a matching; a high-distance selector code permits one cheap seed but should charge odd superpositions of several seed sectors.

**Expected move.** Every matching has some injective seed and a short transcript, while every illegal cover either collides under all seeds or pays selector distance—an asymmetric shared-coefficient mutation, not ordinary hashing.

**Obstruction check.** (1) **Bounded local signatures:** hash summaries are global, but bounded-degree transcript columns would still admit cube relations. (2) **Marginal/tableau:** serious exposure—bucket counts are affine marginals; the protected selector must defeat rectangle splices. (3) **Local-view hierarchies:** seeds are disconnected global views, not fixed connected scopes. (4) **Phase lifts:** no phases. (5) **Integer exact fibers:** binary transcripts avoid integer slacks. (6) **Complete-assignment fingerprints:** polynomial seeds and buckets only. (7) **Tensor amplification:** no tensoring; attack every cross-seed combination. (8) **Exact transfer:** applies to the assembled binary matrix.

**Falsification.** One illegal odd cover has a cheap seed, or three seed certificates XOR into a cheaper transcript.

**Smallest experiment.** Freeze splitters for \(m=8,9\); enumerate all seed-sector words on tiny 3DM, all-eight, and holonomy instances.

**Likely death.** Hashes isolate illegal supports just as well as legal ones, while selector cost raises the YES baseline.

---

### 5. Noncommutative-ABP dense fold

**Mechanism.** Express reachable mixed tensor coordinates as noncommutative polynomials computed by a formula-derived algebraic branching program. Use deterministic polynomial-identity testing for this restricted ABP space to choose a basis of matrix evaluations; fold coordinates only when their evaluations agree on the entire reachable mixed-word space.

**Expected move.** If reachable products have polynomial ABP width, preserve every mixed word exactly using polynomially many dense evaluations, avoiding both sampling and the full squarefree-monomial dimension.

**Obstruction check.** (1) **Bounded local signatures:** products have growing ordered degree and genuinely global variable order. (2) **Marginal/tableau:** evaluations are applied directly, not represented by gate transcripts. (3) **Local-view hierarchies:** no scope consistency. (4) **Phase lifts:** no phases. (5) **Integer exact fibers:** no slack repair. (6) **Complete-assignment fingerprints:** basis is of reachable ABP polynomials, not assignments. (7) **Tensor amplification:** arbitrary mixed words are the ABP space itself; equality must hold on all of it. (8) **Exact transfer:** the evaluation image is a binary linear code after binary matrix-entry expansion.

**Falsification.** Reachable ABP width or evaluation dimension grows exponentially, or the fold preserves equality but destroys weight.

**Smallest experiment.** Compute tensor-train/ABP ranks through powers \(2,3,4\) for existing \(m=8\!-\!12\) codes; exhaust all image words and relabelings.

**Likely death.** General BMT fibers generate the full squarefree function algebra, recreating the \(2^k\) wall.

---

### 6. AG list-recovery with one shared interpolation witness

**Mechanism.** Place triple coordinates at points of a small explicit algebraic curve. A selected matching and one shared low-pole rational function must jointly explain all three pair projections; list-recovery should force an illegal odd cover either to use a much larger pole divisor or to pay many disagreement columns.

**Expected move.** Replace independent inner encoding by a globally coupled coefficient vector, potentially separating legal permutation graphs from signed superpositions at polynomial block length.

**Obstruction check.** (1) **Bounded local signatures:** the interpolation witness is global and degree grows with the instance. (2) **Marginal/tableau:** no unary interfaces, although disagreement columns could recreate them. (3) **Local-view hierarchies:** one global function, not scope tables. (4) **Phase lifts:** irrelevant. (5) **Integer exact fibers:** algebraic list recovery rather than count slacks. (6) **Complete-assignment fingerprints:** curve points and function coefficients are polynomially many. (7) **Tensor amplification:** no tensor claim; all functions and disagreement superpositions require exact enumeration. (8) **Exact transfer:** expand \(\mathbb F_{2^s}\) symbols with a fixed binary simplex inner code, then form binary \(H,t\).

**Falsification.** A \(q+2\) odd cover interpolates with the same pole degree as a matching, or binary expansion flattens the ratio.

**Smallest experiment.** Genus-zero Reed–Solomon version at \(q=3,4\), jointly fitting all pair labels on tiny YES/NO, all-eight, and holonomy families.

**Likely death.** Arbitrary perfect matchings already require maximal interpolation degree, leaving no room to charge illegal covers.
