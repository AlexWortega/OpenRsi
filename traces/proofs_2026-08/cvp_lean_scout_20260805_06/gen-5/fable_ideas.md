Below are six deliberately non-ranked mechanisms. Every construction experiment uses a fully serialized NAND/fusion/COPY tile—not another margin-only completion.

### 1. Tropical Sidon valuations

**Mechanism.** Assign pair cell \((i,j)\) the product tag
\[
a_i b_j=\Pi^{A_i+B_j}u_{ij},
\]
where the sums \(A_i+B_j\) form a widely spaced Sidon set. Spacing beyond every coefficient valuation in the old projected Graver basis gives each nonzero movement a unique least-valuation term, which cannot cancel in a valued division ring.

**Expected move.** Prove Q1 by a Lean unique-minimum lemma plus a checked complete-Graver certificate.

**Falsification.** A primitive with zero pair projection, tied effective minimum, or malformed lift below \(17E\).

**Smallest experiment.** Build the full \(N=8\) NAND plus explicit two-bit COPY/fusion matrix; compute its old projected Graver basis, choose exponents, then recompute the enlarged basis and exact shell.

**Obstruction audit.** Emitted rows/no slack or filtering avoid G1/G6/G7. Tropical products—not affine checksums—address G2–3, G5, G9, G11, G13–15, G19, G31–32, G37–38, Goal G1, and the toric exchange, but only a full audit establishes this. Enumerate DROP for G12/Goal G8 and retest Goal G11/G12. No tensor, exterior, A5, D4, or E6 invokes G30, G33–34, Goal G2–7. G28 growth and carry/lumpability remain unsolved downstream.

---

### 2. MDS array of product transfers

**Mechanism.** Amend Q1’s single \(F_{289}\) symbol to a constant array of \(r\) product symbols
\[
T_\ell(i,j)=a_i^{(\ell)}b_j^{(\ell)}.
\]
Choose them as a full-spark parity-check map on the surviving seam-direction space; the existing three-direction Lean obstruction explicitly justifies needing \(r>1\).

**Expected move.** Show every nonhonest projected primitive has nonzero syndrome, then prove in Lean that componentwise graded-division transfer suffices for Q2–Q3.

**Falsification.** Rank-one product restrictions force a determinant identically zero, or recomputation creates a new zero-syndrome primitive.

**Smallest experiment.** On a complete serialized tile, calculate the surviving seam lattice by SNF and exhaust \(r=2,3\) label arrays over \(F_{289}\); emit determinant and Graver certificates.

**Obstruction audit.** No slack/filter/radix means G1/G6/G7 do not apply. Full-spark detection specifically targets the affine, parity, bag, and splice kernels G2–3, G5, G9, G11, G13–15, G19, G31–32, G37–38, Goal G1, and the fresh exchange; it is not established before recomputation. DROP handles G12/Goal G8. Goal G11’s grade-zero attack motivates multiple channels; Goal G12 is retested. G30, G33–34, A5/D4/E6 Goal G2–7 are unused. G28 and carry/lumpability still require proofs.

---

### 3. High-girth voltage-cover seam

**Mechanism.** Replace each pair selector by lifts in a finite voltage cover of the seam incidence graph. Designated honest NAND/COPY transitions close on prescribed sheets, while every short nonhonest toric circuit acquires nonidentity voltage and therefore violates lifted conservation before any transfer cancellation is possible.

**Expected move.** Amend Q1 by structurally eliminating all projected primitives below the \(17E\) shell; use a product tag only on the remaining circuit classes. Formalize in Lean that projection of a closed lifted walk has trivial voltage.

**Falsification.** A low-energy signed circulation closes in the cover, especially a lifted diagonal splice.

**Smallest experiment.** Serialize the full \(N=8\) tile, enumerate voltage assignments in \(C_2,C_3,S_3\), and recompute the enlarged Graver basis and exact \(17E\) shell.

**Obstruction audit.** Sheet-conservation rows are emitted, so G1/G6/G7 are outside the model. The cover adds coherence absent from G2–3/G5/G13–15, but G19 and Goal G1 show that flow encodings can still splice; only the full signed-Graver audit confronts G9/G11/G19/G31–32/G37–38 and the toric exchange. DROP must be tested for G12/Goal G8. No tensor/exterior/A5/D4/E6 uses G30/G33–34/Goal G2–7. Goal G11/G12 are retested. G28 and carry/lumpability remain downstream.

---

### 4. Low-energy-shell transfer dichotomy

**Mechanism.** Do not require \(T(g)\neq0\) for every abstract primitive. Amend Q1 to the operational statement: every unrestricted malformed lift with energy below \(17E\) has nonzero initial transfer; zero-transfer movements are permitted only outside that shell.

**Expected move.** Prove in Lean that this shell version is sufficient for the Q2–Q3 path argument, then synthesize a rational pair-dependent Gram that pushes the known zero-tag kernel above \(17E\).

**Falsification.** Any exact zero-transfer malformed vector below \(17E\), including DROP.

**Smallest experiment.** Jointly optimize the full tile’s rational Gram and target by exact SDP/CEGIS, enforce common legal energy, then certify the complete shell using diagonal-dominance bounds and Lean-checked enumeration.

**Obstruction audit.** This directly absorbs G12/Goal G8 DROP and the fresh toric exchange rather than pretending to separate them. Exact unrestricted shell enumeration also includes G2–3, G5, G9, G11, G13–15, G19, G31–32, G37–38, Goal G1; no named-attack-only inference is allowed. Emitted constraints exclude G1/G6/G7. It uses no tensor, exterior, A5, D4, or E6, so G30/G33–34/Goal G2–7 are inapplicable. Goal G11/G12 are rebuilt. G28 and carry/lumpability remain unproved; the Lean sufficiency lemma is essential to justify the roadmap amendment.

---

### 5. Higher-degree cyclic division algebra

**Mechanism.** Replace the quaternion algebra by a constant-degree cyclic division algebra whose residue division algebra has dimension \(m>2\) over \(F_{17}\). A single leading symbol can then inject three or more surviving seam directions without becoming a direct product with zero divisors.

**Expected move.** Amend Q1’s algebra while preserving the graded-division argument of Q2; prove in Lean the dimension/injectivity statement and exact positivity of the trace form.

**Falsification.** Failure to realize a positive-definite maximal order and two-sided prime, or a new zero-transfer primitive after full serialization.

**Smallest experiment.** First test degree \(4\) in the finite skew field model \(F_{17^4}[X;\sigma]\); if it passes, construct one explicit totally definite cyclic algebra/order in Sage and enumerate its first two prime-adic shells.

**Obstruction audit.** The larger residue dimension directly escapes Goal G11 and the three-symbol \(F_{17}^2\) dependency, while Goal G12 NAND and the toric exchange still require full audit. Division avoids Goal G2’s A5 zero divisors. Emitted rows avoid G1/G6/G7; enlarged-Graver testing confronts G2–3, G5, G9, G11–15, G19, G31–32, G37–38, Goal G1, and DROP G12/Goal G8. No tensor/exterior/D4/E6 invokes G30/G33–34/Goal G3–7. G28 and carry/lumpability are not automatically solved.

---

### 6. Lean energy-dimension no-go theorem

**Mechanism.** Strengthen the existing three-transfer dependency from coefficient weight to actual CVP energy. Precisely: if three integrally independent, pairwise \(C\)-orthogonal malformed seam directions survive all non-transfer rows, each has squared \(C\)-energy at most \(E/64\), and maps into one \(F_{17}^2\) symbol, then a nonzero zero-transfer integral combination has energy at most \(3E<17E\).

**Expected move.** A Lean proof would refute every single-symbol Q1 candidate satisfying these checkable hypotheses, forcing the multi-channel or structural roadmap amendment.

**Falsification.** Full candidates lack three such directions, orthogonality fails, or their exact Gram makes every dependency cost at least \(17E\).

**Smallest experiment.** State and prove the quadratic-form lemma in Lean, instantiate it on the killed completion as regression, then make future serializers emit the \(3\times3\) restricted Gram and row-survival certificates.

**Obstruction audit.** This is a conditional refutation, not an escape from G1–G38. It directly covers the fresh toric exchange and, when witnesses satisfy the rows, G19/Goal G1 and the affine/parity/bag kernels G2–3, G5, G9, G11, G13–15, G31–32, G37–38. DROP G12/Goal G8 needs a separate witness. G1/G6/G7, G28/G30, G33–34, Goal G2–7, Goal G11/G12, and carry/lumpability are neither solved nor invoked.
