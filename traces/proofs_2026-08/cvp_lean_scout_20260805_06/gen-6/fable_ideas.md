I did not consult the prohibited document or derivative material. Finite experiments below are falsifiers only; promotion requires the indicated Lean 4 theorem.

1. **Oblivious Beneš-routing compiler**

**Mechanism.** Replace formula-specific wiring by a fixed Beneš/Waksman permutation network. NAND, COPY, switch, idle, and DROP become finitely many equal-energy brick colors; the formula selects switch colors and targets, while the recursive matrix topology is fixed.

**Expected frontier move.** Prove in Lean, by block induction, that after selector-preserving eliminations,
\[
M_r(F)=U_r\,\mathrm{HL}_r(A_\star)\,P_F,
\]
where \(P_F\) is a signed color-preserving permutation and \(U_r\) is formula-independent.

**Obstruction check.** All constraints are emitted, meeting the G1/G6/G7 no-filter requirement. Signed-affine attacks G2–3/G5/G9/G11/G13/G15/G19, DROP G12/Goal-G8, Gen-4 seam/Gen-5 physical flip, finite-growth G14/G28/G31/G32/G37/G38, G30 isometry, G33–34/Goals-G3–7 geometry, Goals-G1–2 splices, Goals-G11–12/killed COPY, toric exchange, and carry/lumpability remain downstream L2–L4 obligations.

**Falsification.** Any switch setting changes the integer kernel or Smith data beyond column permutation, or unequal switch energy appears.

**Smallest experiment.** Emit \(N=4\) networks for all \(24\) permutations, including physical/pair/DROP columns; compute explicit \(U_r,P_F\) and verify the kernel identity.

2. **Simple-homotopy collapse of wiring auxiliaries**

**Mechanism.** Realize each wire, fanout, and routing crossover as a contractible integral cell pair. Collapse these pairs using elementary chain contractions that never mix physical selector columns, leaving repeated gate bricks plus the single Lawrence sum constraint.

**Expected frontier move.** Formalize in Lean that a sequence of certified elementary collapses gives a selector-preserving chain isomorphism from every compiler complex to a colored higher-Lawrence complex.

**Obstruction check.** This emits all rows, addressing only G1/G6/G7’s filtering concern. G2–3/G5/G9/G11/G13/G15/G19 signed kernels, G12/Goal-G8 DROP, Gen-4 seam/Gen-5 flip, G14/G28/G31/G32/G37/G38 growth failures, G30, G33–34/Goals-G3–7, Goals-G1–2, Goals-G11–12/COPY, toric exchange, and carry/lumpability remain live; no energy or detection claim is made.

**Falsification.** Shared-variable fanout creates nontrivial integral \(H_1\), torsion, or a non-collapsible cycle depending on formula wiring.

**Smallest experiment.** Serialize two depth-two circuits with different fanout patterns. Produce explicit elementary collapse certificates and compare integral homology before attempting general Lean induction.

3. **Polarized Cayley embedding**

**Mechanism.** Give every variable occurrence an independent copy, encode NAND/COPY as fixed monomial configurations, and impose occurrence equality through polarization. Homogenization and a Cayley embedding may turn all equality glues into Lawrence sum rows rather than formula-specific constraints.

**Expected frontier move.** Prove a Lean block-elimination lemma showing the polarized matrix is selector-preservingly equivalent to a colored lifting of one \(A_\star\). If multiple irreducible Cayley types are unavoidable, this precisely refutes L1 and justifies moving the edge to F1.

**Obstruction check.** Explicit occurrence equalities satisfy the G1/G6/G7 emission gate. Toric quadratic exchange is directly applicable and is the primary danger; G2–3/G5/G9/G11/G13/G15/G19, DROP G12/Goal-G8, Gen-4/5 seam and flip, G14/G28/G31/G32/G37/G38, G30, G33–34/Goals-G3–7, Goals-G1–2, Goals-G11–12/COPY, and carry/lumpability remain unaddressed.

**Falsification.** Equality elimination is nonsaturated, requires formula-dependent tile types, or creates a quadratic exchange absent from the claimed Lawrence kernel.

**Smallest experiment.** Build two NANDs sharing one variable, compute saturation/SNF and the complete circuits, then verify or refute the exact Lawrence kernel formula.

4. **Colored graph-cover normal form**

**Mechanism.** Degree-reduce and pad the circuit incidence graph until every vertex has the same colored local star. It then becomes a finite colored cover of a fixed base graph; the compiler matrix is obtained from one base brick with formula dependence entirely in edge permutations.

**Expected frontier move.** Either prove in Lean that the cover boundary matrix is a restricted colored higher-Lawrence lifting, or prove that its cycle module cannot have Lawrence form. The latter cleanly refutes L1 rather than merely failing another candidate.

**Obstruction check.** Full incidences avoid G1/G6/G7 filtering. Cover cycles may reproduce G5/G15/G19 and Gen-4 seam attacks; physical colors are necessary against Gen-5. DROP G12/Goal-G8, G2–3/G9/G11/G13, G14/G28/G31/G32/G37/G38, G30, G33–34/Goals-G3–7, Goals-G1–2, Goals-G11–12/COPY, toric exchange, and carry/lumpability remain. Unbounded primitive cover cycles would also kill the proposed amendment by violating L2/F2.

**Falsification.** Girth yields primitive signed cycles with unbounded brick support, or padding cannot preserve common honest energy.

**Smallest experiment.** Convert three four-gate wiring graphs into covers of one colored bouquet; compare cycle modules and Graver support with the proposed lifting.

5. **Repair—or refute—the meaning of “row/column equivalent”**

**Mechanism.** Arbitrary unimodular column operations preserve Smith form but not selector support, Graver complexity, or Euclidean energy; nonorthogonal row operations likewise change residual norm. Prove that integral Euclidean isometries are exactly signed permutations, forcing L1 to distinguish kernel equivalence from metric-preserving compiler equivalence.

**Expected frontier move.** Amend L1 to permit row operations only for kernel classification and signed color-preserving permutations for selector/energy claims, with any residual Gram transported explicitly. This is a precise Lean-level correction to the roadmap edge.

**Obstruction check.** This meta-mechanism escapes none of G1/G6/G7, G2–3/G5/G9/G11/G13/G15/G19, DROP G12/Goal-G8, Gen-4/5, G14/G28/G31/G32/G37/G38, G30, G33–34/Goals-G3–7, Goals-G1–2, Goals-G11–12/COPY, toric exchange, or carry/lumpability. Instead it prevents those obstructions from being hidden by an equivalence that fails to preserve their hypotheses.

**Falsification.** ROADMAP already intended only signed permutations and metric-tracked row operations.

**Smallest experiment.** In Lean prove `GL_n(ℤ) ∩ O_n(ℝ)` consists of signed permutations; exhibit a shear sending kernel generator \(e_2\) to \((-N,1)\), changing norm and Graver geometry.

6. **Bar-resolution brick for Boolean relations**

**Mechanism.** Treat truth labels as basis elements of the Boolean relation algebra, COPY as the diagonal \(e_b\mapsto e_b\otimes e_b\), and NAND as multiplication \(e_a\otimes e_b\mapsto e_{\operatorname{NAND}(a,b)}\). Use the normalized bar resolution: its fixed differential supplies physical, pair, glue, normalization, and degeneracy/DROP coordinates, while depth is simplicial iteration.

**Expected frontier move.** Prove in Lean that the normalized bar complex contracts in positive degrees and that its depth-\(r\) kernel is exactly the higher-Lawrence kernel.

**Obstruction check.** Degeneracies make DROP explicit and all rows are emitted, satisfying the G1/G6/G7 format but not defeating G12/Goal-G8. Hochschild/bar cycles may realize G2–3/G5/G9/G11/G13/G15/G19, Gen-4/5, or Goals-G1–2. G14/G28/G31/G32/G37/G38, G30, G33–34/Goals-G3–7, Goals-G11–12/COPY, toric exchange, and carry/lumpability remain downstream.

**Falsification.** Normalization leaves a signed positive-degree cycle, or NAND multiplication is incompatible with the required contraction/common energy.

**Smallest experiment.** Emit normalized bar differentials through degree three and compare their integral kernels with the claimed Lawrence identity.

7. **Fixed universal-verifier tableau**

**Mechanism.** Avoid arbitrary circuit wiring entirely: load the 3CNF into the target of a fixed local verifier, and encode a polynomial-time assignment-checking tableau using finitely many transition tiles. Sweep and clock coordinates make every local transition an instance of one fixed brick; formula dependence is confined to the initial row.

**Expected frontier move.** Prove in Lean that the unrolled tableau matrix admits a fixed-brick Lawrence recursion, or identify the first unavoidable two-dimensional overlap and thereby refute L1’s applicability to universal computation.

**Obstruction check.** Every transition, clock, physical symbol, pair, normalization, and DROP row is emitted, meeting G1/G6/G7’s format. Signed tableau flows are vulnerable to G19/Goal-G1, with G2–3/G5/G9/G11/G13/G15, G12/Goal-G8, Gen-4/5, Goals-G2/G11–12 and killed COPY still live. No claim addresses G14/G28/G31/G32/G37/G38, G30, G33–34/Goals-G3–7, toric exchange, or carry/lumpability.

**Falsification.** Space-time overlap requires a growing alphabet/brick, or a two-negative accepting flow recreates G19.

**Smallest experiment.** Encode a fixed verifier for two variables and two clauses over three time steps; test the depth-\(1,2,3\) integer-kernel identity and enumerate primitive signed flows.
