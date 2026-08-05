Using only the supplied campaign files and classical machinery:

### 1. Relative-cohomology transfer coordinate

**Mechanism.** Replace append-only rows on old selectors by selectors for complete `(left state, gate role, right state)` transitions. Seek a relative cocycle \(c\in H^1(X_{\rm gate},X_{\rm legal};P/P^2)\) vanishing on honest computation cells but pairing nontrivially with every adverse signed cycle; parent composition multiplies its lift by a uniformizer.

**Expected move.** Establish Q1’s missing seed and reduce Q2 to functoriality of the cocycle under gluing, followed by a Lean induction.

**Audit.** No slack/filter/radix (G1/G6/G7), local/private/bag/Walsh machinery (G2–3/G5/G14/G31/G38), tensor seed (G30), exterior/D4/E6 (G33–34, Goal G3–7), or \(A_5\) ring (Goal G2). DROP is a relative state (G12/Goal G8). G9/G11/G13/G15/G19/G32/G37, Goal G1, and the current `111` splice are **not escaped**: they must represent nonzero relative homology classes. Q2 would replace G28’s failed numerical recurrence. Goal G11–12 are avoided only by enlarging the state complex.

**Experiment.** Build the smallest NAND/COPY transition complex over \(\mathbb F_{17}\), insert all known signed cycles, and compute relative homology and separating cocycles.

**Falsifier.** Any adverse cycle homologous to legal cells.

**Likely death.** The `111` affine splice is already relatively null-homologous.

---

### 2. Exact-sequence/Nakayama tile

**Mechanism.** Model a tile by a short exact complex of projective \(\mathcal O\)-bimodules \(K\to C\to D\), with adverse classes represented by homology \(H\). Require the connecting map induced by gluing to equal multiplication by a quaternionic uniformizer on \(H\); projectivity would make repeated gluing exact and force one valuation gain per gate.

**Expected move.** Prove Q2 algebraically, without a finite transducer or carry-lumpability assumption. Promotion requires a Lean theorem formalizing exact gluing and the filtered Nakayama step.

**Audit.** G1/G6/G7 are absent; G2–3/G5/G14/G31/G38 and G30 concern different affine/bag/tensor constructions; G33–34 and Goal G2–7 are unused. DROP is included in \(H\) (G12/Goal G8). G9/G11/G13/G15/G19/G32/G37/Goal G1/current `111` remain genuine kernel tests, not assumed away. Exact multiplication by \(P\) would address G28. Goal G11–12 are outside only if \(C\) is genuinely enlarged beyond their selector modules.

**Experiment.** Enumerate rank-\(\le4\) matrices over \(\mathcal O/P^2\) satisfying NAND/COPY boundary tables; compute homology and the connecting map modulo \(P\).

**Falsifier.** Nonzero grade-zero homology or nonprojective seam torsion.

**Likely death.** Boolean boundary constraints force the current affine pseudosection into \(H\).

---

### 3. Pro-\(17\) covering-space holonomy

**Mechanism.** Lift the NAND/COPY transition graph to a finite quotient of a self-similar pro-\(17\) cover, with a sheet coordinate in a small Heisenberg \(17\)-group. Honest computations have trivial holonomy, while an adverse seam changes the central coordinate; the self-similarity map sends filtration level \(a\) to \(a+1\).

**Expected move.** Q2 becomes a monodromy theorem: every adverse chain has progressively deeper holonomy. An all-depth covering/path-lifting theorem must then be proved in Lean.

**Audit.** No G1/G6/G7 slack or filtering; no G2–3/G5/G14/G31/G38 metric bags; no G30 tensor, G33–34 exterior, Goal G2 group ring, or Goal G3–7 shell. DROP is an explicit vertex (G12/Goal G8). G9/G11/G13/G15/G19/G32/G37, Goal G1, and current `111` are **not outside**: all signed chains must be enumerated, not merely honest paths. Self-similar filtration targets G28. Goal G11–12 are avoided only through new sheet variables.

**Experiment.** Use the Heisenberg group over \(\mathbb Z/17^3\); SAT-search edge labels for four NAND states and two COPY orientations, including every known signed splice.

**Falsifier.** A signed chain with trivial holonomy at all three levels.

**Likely death.** Integral superpositions need not correspond to paths and may cancel monodromy.

---

### 4. Anisotropic quaternion norm-torsor

**Mechanism.** Let transition selectors index triples \((u,v,w)\) in a small quaternionic multiplication table, with legal states satisfying \(w=uv\). Choose role-dependent norm-one torsors so a false boundary would require a solution to an anisotropic reduced-norm equation over \(\mathbb Q_{17}\); multiplicativity of reduced norm would then supply Q2’s depth growth.

**Expected move.** Prove grade-zero exclusion by a local Hilbert-symbol calculation and transfer by \(\operatorname{Nrd}(xy)=\operatorname{Nrd}(x)\operatorname{Nrd}(y)\). Both implications require Lean proofs after a finite candidate is fixed.

**Audit.** No G1/G6/G7, G2–3/G5, G14/G31/G38, G30, G33–34, or Goal G3–7 assumptions. Unlike Goal G2, this uses a division order, not an \(A_5\) group ring. DROP is a table state (G12/Goal G8). G9/G11/G13/G15/G19/G32/G37/Goal G1/current `111` still apply to signed mixtures of table selectors. Goal G11–12 are escaped only if multiplication-table enlargement blocks their affine witnesses; G28 is addressed only if norm transfer is strict.

**Experiment.** Enumerate a role-separated \(16\)-entry table in \(\mathcal O/P^2\), then solve every false, DROP, and signed fiber exactly.

**Falsifier.** Any zero-defect signed table mixture.

**Likely death.** Anisotropy constrains points, not unrestricted integral affine combinations of points.

---

### 5. Lean affine-span no-go theorem

**Mechanism.** Refute the current roadmap edge formally: prove that any added linear coordinate factoring affinely through the frozen boundary is invisible to a normalized affine pseudosection. Instantiate
\[
s_{111}=-s_{001}+s_{011}+s_{101}
\]
to show that no append-only affine/quaternionic row on the existing selector module can seed Q2.

**Expected move.** Amend Q1 to require role-separated transition variables whose legal values do not factor through the old boundary. This is theorem-level progress rather than another finite kill.

**Audit.** This **embraces**, rather than escapes, G9/G11/G13/G15/G19/G32/G37, Goal G1/G11/G12, and the current kill as affine signed witnesses. G1/G6/G7; G2–3/G5; G12/Goal G8; G14/G31/G38; G28/G30; G33–34; and Goal G2–7 are outside the theorem’s assumptions because it concerns neither slack/filtering, overlap, metric DROP, recursion/tensor, bags, nor geometric shells.

**Experiment.** State `affine_pseudosection_invisible` over arbitrary \(\mathbb Z\)-modules in Lean and instantiate the three coefficients and every frozen NAND row.

**Falsifier.** A purported compatible linear row evaluating differently on the displayed combination.

**Likely death.** It deliberately says nothing about genuinely enlarged edge-state tiles—but precisely rules out the proposed append-only repair.

---

### 6. Noncatastrophic convolutional COPY

**Mechanism.** Replace scalar COPY by a terminated convolutional encoder over \(\mathbb F_{17}\), exposing its memory state at every seam. NAND injects an adverse syndrome, and a noncatastrophic encoder with column distance \(>d/4\) prevents that syndrome from being erased during the next four levels; a quaternionic accumulator then gains one valuation per four levels.

**Expected move.** Amend Q2 to block transfer, \(v_{i+4}\ge v_i+1\), which is sufficient because the existing Lean theorem proves \(17>2^4\). Formal progress requires a Lean proof from a basic polynomial generator matrix to the block-gain claim.

**Audit.** No G1/G6/G7, G2–3/G5, G14/G31/G38, G30, G33–34, Goal G2–7. DROP is a trellis state (G12/Goal G8). G9/G11/G13/G15/G19/G32/G37/Goal G1/current `111` remain mandatory signed-trellis tests. Block distance is the proposed escape from G28, not an assumption. Goal G11–12 are outside only after stateful encoding.

**Experiment.** Exhaust memory-two rate-\(1/2\) generators over \(\mathbb F_{17}\); enumerate all \(P^3\) signed trellises of length eight.

**Falsifier.** A zero-output adverse trellis or failed termination.

**Likely death.** Unrestricted coefficients create catastrophic codewords absent from ordinary coding-theory analyses.

---

### 7. Artin–Rees finite-to-infinite carry theorem

**Mechanism.** For one fixed tile, partition boundary classes and represent each class’s adverse zero-boundary kernels by submodules \(K\subset M\) over the local order. Prove an effective stabilization theorem for \(K\cap P^aM\): after a computable SNF/Artin–Rees index \(c\), checking graded injectivity through \(c+1\) implies it at every valuation.

**Expected move.** Turn the mandated \(P^2/P^3\) search into an actual Q2 proof—or rigorously show that no bounded lift audit can suffice. The stabilization theorem and its induction must be in Lean.

**Audit.** This supplies no escape from G9/G11/G13/G15/G19/G32/G37, Goal G1/G11/G12, or current `111`; those become elements of \(K\). It uses none of G1/G6/G7, G2–3/G5, G12/Goal G8 metric DROP, G14/G31/G38, G28/G30, G33–34, or Goal G2–7 machinery. DROP and internal kernels must receive their own submodules.

**Experiment.** Compute saturation chains for the killed affine tile and a tiny role-separated toy; extract the first stable exponent and verify it by SNF.

**Falsifier.** Stabilization index growing with composition depth or carry-dependent unions not representable by finitely many modules.

**Likely death.** NAND composition is a union of affine fibers, not one stable submodule, so Artin–Rees may not apply uniformly.
