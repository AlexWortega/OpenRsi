No prohibited source was consulted. These are deliberately nonconvergent mechanism sketches, not hardness claims.

### 1. Sparse logarithmic-degree Veronese tags

**Core trick.** Lift each triple to a polynomial-size, formula-derived family of degree \(d=\Theta(\log n)\) squarefree monomials chosen by cover-free designs, rather than all degree-\(d\) monomials. Multiply each clause-defect coordinate by these global tags, then BCH-encode the resulting defect vector.

**Expected move.** A finite-difference repair now needs roughly \(2^d=n^{\Omega(1)}\) lifted columns, while a satisfying witness retains polynomial weight and rank.

**Obstruction check.** **Bounded signatures:** not excluded; its cube trade still exists, but has polynomial—not constant—support. **Marginal/tableau:** direct global monomials, no wire interfaces. **Local-view hierarchies:** logarithmic disconnected scopes; fixed-level theorem does not fully cover this, though Petersen flows threaten it. **Phase lifts:** no phases. **Integer fibers:** binary, without affine slacks. **Assignment fingerprints:** sparse monomials, not complete-assignment columns. **Tensor amplification:** no tensor; all mixed lifted words remain relevant. **Exact transfer:** produces binary \(H,t\), so transfer applies.

**Smallest experiment/falsification.** At \(q=3,m=8,d=3\), greedily build a cover-free monomial family and enumerate every mixed word on YES/NO, all-eight, and holonomy instances; record rank and baseline. Kill if any hostile cost is at most worst YES.

**Likely death.** Sparse designs miss a cube direction, or honest monomial support makes the YES baseline/output rank erase the gain.

---

### 2. Nonabelian global holonomy with Fox derivatives

**Core trick.** Label incidence edges by elements of a small nonabelian group and compute formula-wide transports relative to one spanning tree. Store Fox-derivative or regular-representation coordinates for every fundamental cycle, so inconsistent odd holonomy should create many nonzero matrix entries while a legal assignment has trivial transport.

**Expected move.** Convert one global inconsistency into support across many conjugates without tensoring or local phase replication.

**Obstruction check.** **Bounded signatures:** transports are global ordered products, not bounded-degree local signatures. **Marginal/tableau:** outside only if products are compiled directly; state-by-state multiplication would re-enter tableaux. **Local-view hierarchies:** every fundamental cycle is queried globally. **Phase lifts:** outside the proved single-valued abelian/coboundary model; selector is graph-dependent and nonabelian. **Integer fibers:** binary matrix coordinates, no slacks. **Assignment fingerprints:** polynomial edge/cycle dictionary. **Tensor amplification:** none; arbitrary mixed group-image words must still be checked. **Exact transfer:** binary-expand the regular representation and use \(H,t\).

**Smallest experiment/falsification.** Use \(S_3\), its six-dimensional regular representation, the twisted three-matching instance, all-eight, and the inherited \(q=3\) suite; enumerate the complete lifted span and rank.

**Likely death.** Computing prefix actions requires a local state tableau, or universal YES triviality forces the labels to gauge away just as in the phase theorem.

---

### 3. Deterministic isolation sectors without quotienting witnesses

**Core trick.** Use a polynomial candidate family of splitters/weightings and create a separate protected sector for each seed and possible total weight. In a “good” sector, a satisfying matching should be the unique minimum-weight legal object, allowing a BCH shell around that center without identifying all legal witnesses.

**Expected move.** Evade the affine-closure failure of I10: legal witnesses occupy separate sectors, so the XOR of three witnesses need not remain cheap.

**Obstruction check.** **Bounded signatures:** isolation is global, although bounded weight moments would still admit cube trades. **Marginal/tableau:** the outer OR-selector may fall under tableau attacks unless realized without local branch wires. **Local-view hierarchies:** no scope consistency. **Phase lifts:** no phases. **Integer fibers:** not based on affine count slacks. **Assignment fingerprints:** sectors index seeds/totals, not assignments. **Tensor amplification:** none; mixed cross-sector words are the main soundness target. **Exact transfer:** each sector can be binary syndrome decoding.

**Smallest experiment/falsification.** For every \(q=3,m=8\) dictionary, enumerate affine hash weights over \(\mathbb F_{11}\), sector totals, all legal matchings, and all odd covers; then enumerate the combined binary span, including all-eight and holonomy.

**Likely death.** No polynomial deterministic isolation family exists for arbitrary matching families, or the branch combiner recreates a support-three OR/tableau splice.

---

### 4. Splitter-localized exterior-rank profiles

**Core trick.** Apply a polynomial splitter family partitioning triples into blocks of size \(O(\log n)\). Within each block append all exterior/compound coordinates of formula-derived endpoint vectors; a matching should have a normalized full-rank Plücker profile, while an illegal odd cover should lose rank in many blocks.

**Expected move.** Turn combinatorial collision into many zero/nonzero rank defects while keeping every compound block polynomial-sized.

**Obstruction check.** **Bounded signatures:** determinants have logarithmic degree; cube relations remain but require polynomial support. **Marginal/tableau:** direct compound rows, no gate circuit. **Local-view hierarchies:** nonlocal splitter blocks; Petersen-style full-rank pseudo-covers remain possible. **Phase lifts:** none. **Integer fibers:** finite-field rank mechanism. **Assignment fingerprints:** columns are triples and compounds, not assignments. **Tensor amplification:** no product ladder; enumerate every mixed exterior word. **Exact transfer:** binary-expand field symbols, preferably with a fixed simplex inner code.

**Smallest experiment/falsification.** Over \(\mathbb F_4\), use all block sizes \(2,3\) on the \(q=3,m=8\) suite; enumerate all Plücker pivots and mixed words, plus all-eight and holonomy. Compare worst YES, best NO, and binary rank.

**Likely death.** An illegal odd cover is full-rank in every tested block, or pivot branching and compound baselines flatten support exactly as the rank condensers did.

---

### 5. Expander-coupled higher Lawrence lifting

**Core trick.** Replace the exact-cover matrix by a higher Lawrence configuration: several layers share global margins, while expander equations couple their interlayer circulations. Charge only circulation/Graver coordinates, aiming for zero auxiliary cost on a legal diagonal matching but \(\Omega(R)\) propagated cost for every signed nonmatching.

**Expected move.** Amplify an integrality defect through Graver complexity rather than tensor distance or replicated projection tables.

**Obstruction check.** **Bounded signatures:** global toric configuration, not a Boolean local signature. **Marginal/tableau:** layer margins are affine interfaces, so rectangle kernels are a real risk. **Local-view hierarchies:** expander-wide circulation is global, though local cycle witnesses may survive. **Phase lifts:** none. **Integer fibers:** this obstruction may apply; success requires proving that no constant-support exact-fiber Graver repair exists. **Assignment fingerprints:** polynomial layered triple dictionary. **Tensor amplification:** none; arbitrary signed combinations are intrinsic. **Exact transfer:** primarily direct integer CVP; a mod-2 specialization could use exact transfer.

**Smallest experiment/falsification.** Build \(R=3,4\) Lawrence lifts of tiny YES/NO 3DM matrices and enumerate coefficients in \([-2,2]\), including all-eight and holonomy; compute exact norms, rank, and Graver circuits.

**Likely death.** A constant-size toric circuit repairs every layer, or making honest circulations zero still forces an \(Rq\) diagonal baseline.

---

### 6. Tree-coded collision walks

**Core trick.** Mutate I27 by first using bounded-occurrence 3DM so the incompatibility graph has constant degree, then tag every rooted nonbacktracking walk with an ordered tree-code prefix syndrome. The prefix coordinates are intended to stop distinct collision walks from cancelling merely because they end at the same vertex or traverse the same short cycle.

**Expected move.** A single unavoidable collision activates \((\Delta-1)^{\Theta(\log q)}=q^{\Omega(1)}\) distinguishable prefixes using polynomially many coordinates.

**Obstruction check.** **Bounded signatures:** degree grows logarithmically, so the guaranteed cube trade is polynomial-sized rather than constant. **Marginal/tableau:** direct Schur/path features, no wires. **Local-view hierarchies:** logarithmic path scopes; fixed-level theorem is insufficient, but charged-flow attacks remain relevant. **Phase lifts:** deterministic prefix codes, not local phases. **Integer fibers:** binary lift. **Assignment fingerprints:** paths, not assignments. **Tensor amplification:** none; the entire Schur span must be enumerated. **Exact transfer:** outputs binary syndrome instances.

**Smallest experiment/falsification.** Extend the existing length-four walk verifier with rooted orientation and all prefix syndromes; rerun 10 YES, 200 NO, affine-closure, all-eight, and holonomy, measuring active rank rather than nominal coordinates.

**Likely death.** The hostile odd XOR cancels every collision monomial before coding, so a linear tree code has nothing left to protect.

---

### 7. Sparse Macaulay pointed-syzygy code

**Core trick.** Form the Boolean-clause ideal and a sparse Macaulay matrix at growing degree \(D\), with a distinguished constant-monomial coordinate. A satisfying assignment yields a pointed evaluation functional; multiplicity-code rows are meant to force every non-evaluation pointed syzygy to have polynomially larger support.

**Expected move.** Replace local assignment tables by one global algebraic-geometric consistency condition and derive soundness from elimination degree.

**Obstruction check.** **Bounded signatures:** fixed \(D\) is covered; only growing \(D\) escapes constant-support cube trades. **Marginal/tableau:** direct Macaulay equations, although truncated moments may themselves act as proper marginals. **Local-view hierarchies:** this resembles a global moment hierarchy; fixed degree is killed, sparse growing degree is not fully covered. **Phase lifts:** none. **Integer fibers:** finite-field syzygies, no count slacks. **Assignment fingerprints:** monomials rather than complete assignments. **Tensor amplification:** none; all pointed syzygies are mixed words. **Exact transfer:** binary Macaulay matrices transfer directly.

**Smallest experiment/falsification.** Construct degree \(D=3,4\) matrices for the all-eight formula, twisted holonomy, and tiny satisfiable formulas; enumerate pointed kernel/coset minima and rank after duplicate-row/column elimination.

**Likely death.** Degree or monomial count becomes exponential, or low-support pseudo-evaluations survive at every polynomial-size truncation.
