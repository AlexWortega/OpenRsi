I used only the attached campaign files. The following audit key is incorporated into every sketch:

- **A — objective/filter/DROP:** G1 RS slack, G6 filtered quotient, G7 radix kernel, G12 fingerprint DROP, Goal G8 augmented-Gram DROP.
- **B — signed/affine kernel:** G2–3, G5, G9, G11, G13, G15, G19 signed flow/splice; Goal G1–2, G11–12; affine COPY; Generation-4 seam, Generation-5 physical flip, Generation-6 Beneš/toric exchange, Generation-7 ghosts/COPY cycle.
- **C — scaling/composition:** G14, G28 \(\lambda\le\mu\), G31, G32, G37, G38, and carry/lumpability.
- **D — retired geometry/tensor:** G30 seed isometry, G33–34 exterior failure, Goal G3–5 D4, Goal G6–7 E6.
- **E — fixed-block tractability.**
- **F — Markov-versus-Graver.**

### 1. Formalize—and possibly refute—the statement of U0

**Core trick.** U0 is not yet a proposition: \(C_S\) is unspecified, and “finite colors” or “bounded width” must mean bounds uniform in \(S\); otherwise every finite matrix can receive unique colors. Define four inductive marked-matrix grammars with constants \(K,q,w\), and state U0 as  
\[
\forall K,q,w\;\exists S_0\;\forall S\ge S_0,\quad D_S\notin\mathcal G_{K,q,w}.
\]

**Expected move.** Amend U0 into U0a (Lean definitions and grammar soundness), U1a (actual serializer), then U0b (nonmembership invariant). This is justified because present U0 cannot be instantiated before U1 supplies \(C_S\).

**Falsification.** A standard fixed-block presentation not represented by the grammar, or a legal representation using \(S\)-dependent “fixed” blocks.

**Executable.** Implement `MarkedMatrix`, `EqualityExpansion`, and the four grammars in Lean; classify toy n-fold/tree-fold matrices and the existing \(8,16,32\) skeletons.

**Audit.** A–D are outside: no distance, signed soundness, recurrence, or retired gadget is asserted. E is exactly formalized. F is outside because no move basis is used.

**Likely death.** The literature’s class definitions resist one common grammar.

---

### 2. Incidence-treewidth certificate via equality-contraction minors

**Core trick.** Form the marked bipartite support graph \(G(D_S)\). A faithful auxiliary equality expansion contracts back to \(G(D_S)\), while every fixed-template n-fold, generalized n-fold, fixed-depth tree-fold, or two-stage graph has a tree decomposition of width bounded solely by its template; finite colors and permutations do nothing to treewidth.

**Expected move.** Exhibit an expander/grid minor of order \(\Omega(S^\alpha)\) in the detector subgraph, proving unbounded treewidth and hence U0.

**Falsification.** Either the serialized detector graph has uniformly bounded treewidth, or one target class admits unbounded treewidth despite fixed blocks.

**Executable.** Serialize sizes \(8,16,32\); use exact elimination/min-fill plus a certified bramble or grid-minor witness. In Lean prove: faithful equality contraction gives a graph minor; template grammars have width \(\le f(K)\); treewidth is minor-monotone.

**Audit.** A–D are outside because this is support-only classification, with no energy or composition claim. E is attacked directly. F is outside: no Markov-generation inference occurs.

**Likely death.** Separator rows may look expansive semantically while their actual incidence graph remains tree-like.

---

### 3. Finite-field cut-rank as an algebraic separator invariant

**Core trick.** For each marked row/column separation define the interface rank over \(\mathbb F_p\), using the off-diagonal transfer submatrix after eliminating private identity columns. Fixed-block grammars have a decomposition tree whose every interface rank is \(O_{K,q,w}(1)\); an explicit detector code should force \(\Omega(S^\alpha)\) rank on every balanced decomposition.

**Expected move.** Prove a rank-width-style lower bound for \(D_S\), preferably simultaneously for \(p=2,3,5\), excluding accidental modular collapse.

**Falsification.** Find a balanced recursive ordering with bounded cut-rank, or an equality expansion that reduces rank by more than its stated width.

**Executable.** Compute exact cut-rank profiles for \(S=8,16,32\) using branch-and-bound. Lean targets: rank submodularity, the fixed-template interface bound, and a precise \(+w\) stability lemma for equality elimination.

**Audit.** A–D are outside: no objective, malformed vector, recurrence, or old geometric family appears. E is the direct conclusion. F is outside because ranks concern the entire presentation, not Markov moves.

**Likely death.** Expander incidence need not have high rank over any chosen small field, and arbitrary equality splitting may defeat the proposed stability lemma.

---

### 4. Represented-matroid branch-width and a graphic detector minor

**Core trick.** Regard \(D_S=[I\;{-}C_S]\) as a rational represented matroid. Search for a graphic expander matroid minor arising from detector-flow columns; fixed block systems should be bounded-adhesion sums of constant matroids and therefore have uniformly bounded branch-width.

**Expected move.** A certified \(M(H_m)\) minor with \(H_m\) an expanding graph gives unbounded branch-width, invariant under row operations and marked permutations. Faithful equality expansions must be shown to add only bounded-adhesion series/parallel extensions.

**Falsification.** No growing graphic minor exists, a target fixed-block family has unbounded branch-width, or equality auxiliaries are not bounded-adhesion matroid extensions.

**Executable.** On the smallest serializer, pivot against the identity block, search deletion/contraction sequences producing cycle matrices, and verify ranks exactly over \(\mathbb Q\). Formalize minor rank certificates and bounded-adhesion sums in Lean.

**Audit.** A–D are outside because only linear dependence structure is classified; no distance or old gadget is reused. E is directly addressed. F is respected: branch-width uses all dependencies, not a Markov basis.

**Likely death.** The universal detector may be graph-expanding while its represented matroid has small branch-width.

---

### 5. Unbounded conformal-circuit type as a Graver obstruction

**Core trick.** Fixed n-fold templates have bounded “brick type” for conformally primitive kernel vectors; seek analogous bounds for the other three classes. Construct in \(D_S\) a primitive signed circuit meeting \(\Omega(S^\alpha)\) detector interfaces, with every proper conformal subvector rejected by an explicit row certificate.

**Expected move.** Such circuits contradict any uniform fixed-block representation and simultaneously exercise the full signed kernel rather than merely graph support.

**Falsification.** The circuit conformally decomposes, has a bounded-interface lift, or tree-fold/two-stage fixed templates genuinely permit unbounded primitive type.

**Executable.** Enumerate sparse circuits on \(S=8,16\), then certify primitiveness by orthant ILP/SNF. In Lean state `fixedBlock_graver_type_bound` separately for each grammar and prove projection stability for faithful equality lifts.

**Audit.** A is outside: circuit existence says nothing about CVP energy or DROP. B is inside: all affine, splice, flip, ghost, and cycle directions are allowed and primitiveness is unrestricted. C–D are outside. E is direct. F is handled correctly by Graver/conformal classification, never Markov generation.

**Likely death.** A bounded-width equality lift may destroy sign coherence, or no uniform Graver-type bound exists for one target class.

---

### 6. Model-theoretic finite-template obstruction via twin-width

**Core trick.** View a marked matrix as a finite relational structure: row/column sorts, finitely many entry labels, and marks. Fixed-block systems are finite interpretations of bounded-height labeled trees and should admit bounded-width contraction sequences, whereas bounded-degree detector expanders can have twin-width growing linearly.

**Expected move.** Prove the actual detector structure has unbounded twin-width, while uniform finite coloring, permutation, and local equality gadgets preserve a class-dependent bound.

**Falsification.** Produce bounded-width contraction sequences for the serialized detector family, or show a standard generalized/tree-fold construction is not an interpretation of bounded-height trees.

**Executable.** SAT-search optimal contraction sequences for sizes \(8,16\); generate explicit lower-bound obstructions from many pairwise-distinct detector neighborhoods. Lean can verify a supplied contraction sequence and prove the fixed-template upper bound.

**Audit.** A–D are outside because the invariant ignores targets, norms, signed witnesses, recursion, and retired gadgets. E is directly targeted. F is outside: no kernel generators are inferred.

**Likely death.** Equality expansion is not sufficiently local to preserve twin-width, or the universal topology has substantial hidden symmetry and bounded contractions.

---

### 7. Grammar recognizer seeking a constructive counterexample to U0

**Core trick.** Attack U0 adversarially: encode marked n-fold/generalized/tree-fold/two-stage recognition as SAT/SMT, including unknown permutations, finite color maps, and width-\(w\) equality expansions. A uniform decomposition pattern would refute U0 and prevent building later soundness on a false tractability exclusion.

**Expected move.** Either discover an explicit standard-class representation, or extract repeated UNSAT cores suggesting a pumping invariant: fixed templates force two detector interfaces to share one marked boundary type, while the compiler gives them distinct signatures.

**Falsification.** Any valid decomposition refutes the proposed U0 mechanism; conversely, isolated finite UNSAT results without a uniform pumping theorem are no progress.

**Executable.** Start with \(K\le4,q\le3,w\le2\) on sizes \(8,16\). Emit checkable decomposition certificates when SAT and DRAT/LRAT certificates when Booleanized UNSAT; formalize the eventual boundary-type pigeonhole lemma in Lean.

**Audit.** A–D are outside because this tests matrix syntax only. E is attacked in both directions, including honest refutation. F is outside: recognition does not substitute Markov moves for signed kernels.

**Likely death.** Quantification over every constant \(K,q,w\) prevents finite search from yielding a scalable theorem, and UNSAT cores may not stabilize.
