1. **Oblivious Beneš-routing normal form**

**Mechanism.** Replace arbitrary formula wiring by fixed \(2\times2\) COPY/SWAP switch bricks in a Beneš network. Formula-specific routing appears only in switch targets/colors; after eliminating switch auxiliaries by explicit unimodular operations, the remaining repeated gate blocks should satisfy the higher-Lawrence kernel identity.

**Expected move.** Prove L1 for balanced bounded-fanout circuits by reducing arbitrary wiring to a fixed topology.

**Obstruction audit.** G1/G6/G7: no slack, filtering, or radix amplification; the full matrix is emitted. G12/Goal-G8 DROP and Gen4 seam/Gen5 physical flips are explicit coordinates. G2–3/G5/G9/G11/G13/G15/G19, Goal-G1/G2/G11/G12, affine-COPY, and toric exchange remain L2 obligations. G14/G28/G30–34/G37/G38, Goal-G3–7, and carry/lumpability are downstream because no shell, tensor, geometry, or growth claim is made.

**Experiment.** For width four, route all 24 permutations through one NAND layer; serialize physical, pair, glue, normalization, and DROP rows. Compute exact \(UAV\) certificates and check the kernel identity through depth three. Then state the switch-elimination induction in Lean.

**Falsification/death.** A switch setting cannot be target-only while preserving common legal energy, or fanout creates an extra kernel class.

---

2. **Cellular-collapse certificate**

**Mechanism.** Interpret the complete compiler matrix as a boundary map of a colored integral CW complex: selectors are cells, glue rows are incidences, and each wiring gadget is a contractible attachment. A sequence of elementary collapses would give explicit unimodular row/column operations, leaving disjoint \(A_\star\)-cycles plus the single Lawrence sum-zero relation.

**Expected move.** Prove L1 by a topology-driven normal form—or refute it when reconvergent wiring creates nontrivial homology.

**Obstruction audit.** G1/G6/G7 are absent because no residual filtering or radix argument occurs. G12/Goal-G8 and the Gen4 seam/Gen5 physical flip are retained as cells. G2–3/G5/G9/G11/G13/G15/G19, Goal-G1/G2/G11/G12, affine-COPY, and toric exchange remain visible kernel classes for L2. G14/G28/G30–34/G37/G38, Goal-G3–7, and carry/lumpability concern later soundness mechanisms not asserted here.

**Experiment.** Build complexes for a two-gate tree, a fanout diamond, and a three-COPY cycle. Produce and replay elementary-collapse certificates; compare residual homology with the claimed Lawrence kernel. Formalize in Lean that one free-face collapse induces an integral kernel equivalence.

**Falsification/death.** Reconvergence leaves an \(H_1\) class depending on formula topology, so no fixed-brick normal form exists.

---

3. **Multi-Rees/SAGBI recognition**

**Mechanism.** Regard compiler columns as monomials and its integral kernel as a toric lattice ideal. Higher Lawrence liftings are multi-Rees constructions; seek a fixed term order under which recursive NAND/COPY gluing has a SAGBI basis consisting only of lifted \(A_\star\) relations and universal exchange binomials.

**Expected move.** A depth-independent Gröbner normal-form theorem proves L1 algebraically; an unavoidable new mixed binomial refutes it.

**Obstruction audit.** G1/G6/G7 do not apply: every exponent coordinate is emitted. DROP and physical/pair columns cover G12/Goal-G8 and Gen4/Gen5. G2–3/G5/G9/G11/G13/G15/G19 and Goal-G1/G2/G11/G12 remain possible toric relations. The toric quadratic exchange obstruction is directly tested, not assumed away. G14/G28/G30–34/G37/G38, Goal-G3–7, and carry/lumpability are downstream since no amplification is claimed.

**Experiment.** For one proposed full brick, use 4ti2/Singular to compute saturated lattice ideals at depths one through three. Reduce every generator against the conjectured lifted-plus-exchange basis and compare multigraded Hilbert series. If stable, formalize the recursive integer-kernel reduction in Lean.

**Falsification/death.** Saturation introduces depth-dependent mixed binomials involving physical selectors, defeating any finite Gröbner template.

---

4. **Marked arithmetic-matroid no-go**

**Mechanism.** Amend L1 to require *marked* equivalence: physical/anchor columns may only undergo color-preserving signed permutations, while arbitrary unimodular mixing is confined to zero-cost auxiliaries. Without this restriction, column equivalence does not preserve honest encodings or Euclidean energy; under it, circuit supports and arithmetic-matroid multiplicities can obstruct a Lawrence realization.

**Expected move.** Either refute naïve L1 using growing COPY-cycle circuits or identify exactly which universal-routing auxiliaries are necessary.

**Obstruction audit.** G30 is directly addressed: semantic energy cannot be transported through an arbitrary seed isometry. G1/G6/G7 remain outside because this is a full-matrix invariant. G12/Goal-G8 and Gen4/Gen5 are marked explicitly. G2–3/G5/G9/G11/G13/G15/G19, Goal-G1/G2/G11/G12, affine-COPY, and toric exchange remain live circuits. G14/G28/G31–34/G37/G38, Goal-G3–7, and carry/lumpability are downstream.

**Experiment.** Serialize closed COPY rings of lengths \(3,\dots,8\), including all physical and pair rows. Compute marked primitive circuits and test whether minimum brick support grows with ring length. In Lean, prove the alternating cycle vector is primitive under the declared marking.

**Falsification/death.** Auxiliary columns permit a marked local conformal decomposition, so the apparent long circuit is only a projection artifact.

---

5. **Typed-operad/PROP induction**

**Mechanism.** Model each full brick as a typed integer cospan and NAND, COPY, normalization, and glue as generators of a PROP. Prove a normal-form theorem: every balanced compiler term rewrites to a colored higher-Lawrence cospan, with variable reuse represented by an explicit COPY comonoid rather than formula-specific matrix rows.

**Expected move.** Turn L1 into a structural induction suitable for Lean rather than a depth-by-depth recognition experiment.

**Obstruction audit.** G1/G6/G7 are excluded because composition retains every coordinate and introduces no filter. DROP, pair seams, and physical selectors cover G12/Goal-G8 and Gen4/Gen5. G2–3/G5/G9/G11/G13/G15/G19, Goal-G1/G2/G11/G12, affine-COPY, and toric exchange remain equations whose kernel consequences belong to L2. G14/G28/G30–34/G37/G38, Goal-G3–7, and carry/lumpability are not implicated by a realization-only theorem.

**Experiment.** Implement typed matrices with pushout composition; enumerate all well-typed terms with at most four gates and compare their normal forms. State in Lean that kernel formation commutes with one generator-level pushout under a checkable saturation hypothesis.

**Falsification/death.** COPY’s Frobenius equations create loops/genus under DAG sharing, producing extra kernel summands absent from ordinary higher Lawrence liftings.

---

6. **Tree-fold replacement with a Lean sufficiency gate**

**Mechanism.** Expand variable occurrences and connect them by balanced equality trees, yielding a genuine fixed-block tree-fold matrix rather than forcing an ordinary higher Lawrence form. Amend L1 only if Lean proves both the exact signed-kernel recursion and a primitive-support bound strong enough to substitute for the constant \(K\) required by L2.

**Expected move.** Establish a rigorously sufficient tree-fold frontier, or kill the amendment by demonstrating depth-growing primitive support.

**Obstruction audit.** G15 is directly relevant: unlike the killed weighted laminar hierarchy, this claims only an exact full signed-kernel theorem, not energy amplification. G1/G6/G7 use no filtering; G12/Goal-G8 and Gen4/Gen5 are explicit blocks. G2–3/G5/G9/G11/G13/G19, Goal-G1/G2/G11/G12, affine-COPY, and toric exchange remain mandatory primitive classes. G14/G28/G30–34/G37/G38, Goal-G3–7, and carry/lumpability remain downstream.

**Experiment.** Generate complete depth-\(1,\ldots,5\) tree-fold matrices and compute maximum Graver support by level. In Lean, prove the exact kernel fiber-product formula for one parent with two children.

**Falsification/death.** Primitive support grows exponentially with depth, so no constant detector sparsity \(K\) survives and the roadmap amendment is insufficient.

---

7. **LDPC protograph lifts and monodromy obstruction**

**Mechanism.** Regularize the formula incidence graph with dummy COPY gates so it becomes a colored cover of one fixed protograph. The compiler is then a lifted parity-check matrix; test whether trivial voltage/monodromy is exactly the condition under which that lift is integrally equivalent to a higher Lawrence lifting.

**Expected move.** Prove L1 after eliminating monodromy through routing gadgets, or refute it by exhibiting formula-dependent cover homology. A graph-cover replacement is admissible only if it also obtains a bounded signed-primitive theorem.

**Obstruction audit.** G1/G6/G7 are outside because no slack, external quotient, or radix is used. G12/Goal-G8 and Gen4/Gen5 are represented by full variable-node types. G2–3/G5/G9/G11/G13/G15/G19, Goal-G1/G2/G11/G12, affine-COPY, and toric exchange remain pseudocodeword/primitive hazards. G14/G28/G30–34/G37/G38, Goal-G3–7, and carry/lumpability are downstream; no code-distance amplification is inferred.

**Experiment.** Enumerate all connected two- and three-lifts of the smallest NAND/COPY protograph. Compute integral kernels, voltage-cycle classes, and Graver supports; test equivalence precisely when all cycle voltages vanish. Formalize the one-cycle holonomy lemma in Lean.

**Falsification/death.** Nontrivial covers have large-support pseudocodewords, simultaneously blocking Lawrence equivalence and the constant-\(K\) replacement theorem.
