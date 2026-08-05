I did not use external sources. Each mechanism targets **U0 only**; none is offered as a soundness or gap lemma.

### 1. Row-basis-invariant column-matroid branchwidth

**Mechanism.** Let \(M_S\) be the marked column matroid of \(D_S=[I\mid-C_S]\), over both \(\mathbb Q\) and selected \(\mathbb F_p\). Prove in Lean that the actual detector routing induces tangles of unbounded order, while each fixed-template \(n\)-fold, generalized \(n\)-fold, tree-fold, and two-stage matrix has template-bounded branchwidth; faithful bounded-width equality expansion must retain \(M_S\) as a minor.

**Expected move.** A compiled theorem `unbounded_bw → U0`, stronger than support-treewidth and invariant under unimodular row rebasing.

**Audit.** G1 RS, G6 filtering, G7 radix; G2–3 affine, G5 overlap, G9 parity, G11 triple, G13 affine-span, G15 laminar, G19 flow/splice; G12/Goal-G8 DROP; G14 bags, G28 growth, G31 Walsh, G32 additive parity, G37 cut, G38 splitters; G30 isometry; G33–34 exterior; Goal G1 diagonal, G2 A5, G3–5 D4, G6–7 E6, G11 grade-zero, G12 redundant-NAND/affine-COPY/toric; Gen4 seam, Gen5 flip, Gen6 Beneš/marking, Gen7 ghosts/COPY-cycle; carry/lumpability and Markov–Graver are outside assumptions: no metric, gadget, recurrence, or move-generation claim. Fixed-block and Gen8 rebasing are addressed directly.

**Experiment/falsifier.** Serialize actual \(C_8\); compute exact \(\mathbb F_2\) branchwidth and a replayable tangle certificate. It likely dies because one target class has unbounded branchwidth or identity pairing yields a narrow decomposition.

---

### 2. Whole toric-ideal fiber-product width

**Mechanism.** Associate to \(D_S\) its complete toric ideal \(I_{D_S}\), not a Markov basis. Seek an indispensable primitive binomial crossing \(k\) independently programmable detector regions, and prove that fixed-template classes admit bounded-width iterated toric-fiber-product decompositions; row rebasing preserves the ideal, while faithful equality gadgets become eliminable variables.

**Expected move.** Lean formalizes kernel-ideal invariance and an elimination theorem; a growing indispensable-crossing invariant proves U0.

**Audit.** G1 RS, G6 filtering, G7 radix; G2–3 affine, G5 overlap, G9 parity, G11 triple, G13 affine-span, G15 laminar, G19 flow/splice; G12/Goal-G8 DROP; G14 bags, G28 growth, G31 Walsh, G32 additive parity, G37 cut, G38 splitters; G30 isometry; G33–34 exterior; Goal G1 diagonal, G2 A5, G3–5 D4, G6–7 E6, G11 grade-zero, G12 redundant-NAND/affine-COPY/toric; Gen4 seam, Gen5 flip, Gen6 Beneš/marking, Gen7 ghosts/COPY-cycle; carry/lumpability are outside assumptions because no CVP soundness is asserted. Markov-versus-Graver is met by using the entire kernel ideal, not generated moves. Fixed-block is direct; Gen8 rebasing is neutralized algebraically.

**Experiment/falsifier.** For actual \(C_8\), enumerate circuits by exact SNF, test conformal decomposability, and compute minimal separator elimination sets. It likely dies if local circuits generate the whole ideal or fixed \(n\)-fold ideals possess equally global indispensable binomials.

---

### 3. Coding-theoretic tensor-network bond dimension

**Mechanism.** Over \(\mathbb F_p\), form the full indicator tensor of the code \(\ker(D_S\bmod p)\). Fixed-template constructions should have constant bond dimension along their defining decomposition, whereas \(k\) independently routed detector channels should create a flattening of rank \(p^k\); bounded equality gadgets are local tensor contractions, and row rebasing leaves the code unchanged.

**Expected move.** Prove in Lean four class-specific bond-dimension bounds and one explicit high-rank flattening for the serializer.

**Audit.** G1 RS, G6 filtering, G7 radix; G2–3 affine, G5 overlap, G9 parity, G11 triple, G13 affine-span, G15 laminar, G19 flow/splice; G12/Goal-G8 DROP; G14 bags, G28 growth, G31 Walsh, G32 additive parity, G37 cut, G38 splitters; G30 isometry; G33–34 exterior; Goal G1 diagonal, G2 A5, G3–5 D4, G6–7 E6, G11 grade-zero, G12 redundant-NAND/affine-COPY/toric; Gen4 seam, Gen5 flip, Gen6 Beneš/marking, Gen7 ghosts/COPY-cycle; carry/lumpability and Markov–Graver do not apply: this is exact finite-field representation complexity, not amplification or move classification. Fixed-block is direct; Gen8 support/rebasing is avoided because tensor rank depends on the kernel code.

**Experiment/falsifier.** Emit actual \(D_8\), compute all balanced flattening ranks over \(\mathbb F_2,\mathbb F_3\), and search a low-bond decomposition. It likely dies because the identity columns permit pairing each syndrome coordinate locally.

---

### 4. Marked \(p\)-adic deletion–contraction profile

**Mechanism.** Replace displayed support by an arithmetic invariant: for every marked deletion/contraction pair, record the Smith elementary divisors of the resulting lattice map. Prove fixed-template systems have bounded separator torsion-rank profiles, while the actual detector family has \(k\) independent \(p\)-adic defects; unimodular row rebasing changes none of these data, and faithful equality expansion adds only unit factors.

**Expected move.** A Lean theorem turns an unbounded hereditary Smith profile into exclusion from each of the four classes.

**Audit.** G1 RS, G6 filtering, G7 radix; G2–3 affine, G5 overlap, G9 parity, G11 triple, G13 affine-span, G15 laminar, G19 flow/splice; G12/Goal-G8 DROP; G14 bags, G28 growth, G31 Walsh, G32 additive parity, G37 cut, G38 splitters; G30 isometry; G33–34 exterior; Goal G1 diagonal, G2 A5, G3–5 D4, G6–7 E6, G11 grade-zero, G12 redundant-NAND/affine-COPY/toric; Gen4 seam, Gen5 flip, Gen6 Beneš/marking, Gen7 ghosts/COPY-cycle; carry/lumpability and Markov–Graver are outside assumptions. Unlike G6 filtering, deletions are invariants of the full marked \(D_S\), not external CVP constraints. Fixed-block and Gen8 row-basis sensitivity are addressed directly.

**Experiment/falsifier.** Exhaust marked deletions of actual \(D_8\) up to eight columns, emit SNF certificates, and compare cumulative controls. It likely dies because the identity block trivializes torsion or fixed templates accumulate unbounded torsion.

---

### 5. Myhill–Nerode index of exact separator behavior

**Mechanism.** Treat a matrix fragment as a finite-state transducer over \(\mathbb F_p\): two boundary assignments are equivalent when every legal continuation extends either both or neither to a kernel vector. Fixed-template grammars should have bounded exact Myhill–Nerode index, while a programmable \(k\)-wire reconvergence system supplies \(p^k\) distinguishable boundary contexts; equality auxiliaries preserve projected behavior.

**Expected move.** Define all four grammars and prove their congruence bounds in Lean, then exhibit distinguishing continuations from actual detector rows.

**Audit.** G1 RS, G6 filtering, G7 radix; G2–3 affine, G5 overlap, G9 parity, G11 triple, G13 affine-span, G15 laminar, G19 flow/splice; G12/Goal-G8 DROP; G14 bags, G28 growth, G31 Walsh, G32 additive parity, G37 cut, G38 splitters; G30 isometry; G33–34 exterior; Goal G1 diagonal, G2 A5, G3–5 D4, G6–7 E6, G11 grade-zero, G12 redundant-NAND/affine-COPY/toric; Gen4 seam, Gen5 flip, Gen6 Beneš/marking, Gen7 ghosts/COPY-cycle; carry/lumpability and Markov–Graver are inapplicable: no energy or recurrence is claimed. Fixed-block is direct; Gen8 rebasing is avoided because projected solution relations are presentation-invariant.

**Experiment/falsifier.** On actual \(C_8\), enumerate boundary assignments and minimize the continuation automaton exactly. It likely dies if global template rows already yield unbounded index or detector contexts collapse semantically.

---

### 6. Constructive refutation by certified grammar synthesis

**Mechanism.** Attack U0 adversarially: formalize exact grammars for the four classes and use SAT/e-graph search to synthesize a row/column permutation, bounded equality expansion, and optionally bounded unimodular rebasing for actual \(D_8,D_{16}\). If a uniform recursive certificate appears, prove it in Lean and refute U0; if only depth \(O(\log S)\) is possible, amend U0 to exclude constant parameters specifically, after verifying the tractability theorem does not cover growing depth.

**Expected move.** Either a genuine counterexample to U0 or a sharply formalized roadmap edge with quantified parameters.

**Audit.** G1 RS, G6 filtering, G7 radix; G2–3 affine, G5 overlap, G9 parity, G11 triple, G13 affine-span, G15 laminar, G19 flow/splice; G12/Goal-G8 DROP; G14 bags, G28 growth, G31 Walsh, G32 additive parity, G37 cut, G38 splitters; G30 isometry; G33–34 exterior; Goal G1 diagonal, G2 A5, G3–5 D4, G6–7 E6, G11 grade-zero, G12 redundant-NAND/affine-COPY/toric; Gen4 seam, Gen5 flip, Gen6 Beneš/marking, Gen7 ghosts/COPY-cycle; carry/lumpability and Markov–Graver are outside assumptions. Fixed-block is tested directly; Gen8’s support/rebasing warning motivates the certificate search rather than being assumed away.

**Experiment/falsifier.** Freeze one grammar and synthesize the minimum-width representation of actual \(D_8\), with a Lean checker for certificates. It likely dies from grammar ambiguity or nonuniform decompositions that do not extrapolate.
