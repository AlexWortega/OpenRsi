I did not consult the prohibited document or derivative material.

**Audit key used in every sketch.**  
**K:** G1 RS slack, G6 filtered quotient, G7 radix kernel, G2–3 affine isolation, G5 private overlap, G9 parity, G11 unique-triple parity, G13 affine-span collision, G15 laminar lift, G19 signed flow/splice, Goal G1 diagonal splice, Goal G2 \(A_5\) zero divisors, Goal G11 grade-zero, Goal G12 redundant NAND, killed affine COPY, toric exchange, Generation-4 seam, Generation-5 physical flip.  
**D:** G12 fingerprint DROP; Goal G8 augmented-Gram DROP.  
**R:** G14 pair bags, G28 \(\lambda\le\mu\), G31 Walsh shell, G32 additive parity, G37 parity cut, G38 splitter bags, carry/lumpability.  
**X:** G30 seed isometry, G33–34 exterior tags, Goal G3–5 \(D_4\), Goal G6–7 \(E_6\).

### 1. Equal-radius state splitting instead of compatible syndromes

**Mechanism.** Give each local honest switch state a separate standard-basis mark \(e_i\), measured from the common center \(\frac1q\mathbf1\). All honest states then have equal energy, but the fatal four-state exchange has mark \(e_1-e_2-e_3+e_4\neq0\); switch settings are separately pinned by targets.

**Expected move.** Amend L1 so honest states need equal norm, not equal linear syndrome. This directly exits G13’s assumption that every compatible row takes one common value on honest encodings.

**Audit.** K: no slack/filter/radix; all coordinates are emitted. Toric exchange is charged, but every other K witness still requires a full signed-kernel audit. D: include zero and all partial state drops explicitly. R: outside this L1-only claim; no growth is asserted. X: no tensor, exterior, \(D_4\), or \(E_6\); test marked isometries separately.

**Smallest experiment/falsifier.** Add four centered one-hot marks to the killed `54x76` switch, clear denominators, and rerun all 384 fibers, DROP, Hamming-one/two, and support-\(\le10\) kernel search.

**Likely death.** A higher-support affine relation among marked honest states, or legal-energy mismatch after global gluing.

---

### 2. Prove the marked Lawrence normal-form theorem in Lean

**Mechanism.** Separate the abstract algebra from brick discovery. For
\[
L_r(A)=\begin{bmatrix}I_r\otimes A\\ \mathbf1^\top\otimes I\end{bmatrix},
\]
formally prove
\[
\ker_{\mathbb Z}L_r(A)=\{(u_i):Au_i=0,\ \sum_i u_i=0\},
\]
and prove transport through unimodular row maps, marked signed column permutations, and auxiliary Gram pullbacks.

**Expected move.** This makes L1 reducible to an explicit finite certificate \(M_r=P_rL_r(A_\star)Q_r\), rather than informal pattern recognition. It is genuine beyond-FINITE progress if completed in Lean.

**Audit.** K and D are not evaded: the theorem transports exact kernels and DROP energies and therefore cannot hide any listed witness. R is outside because no amplification follows. X is outside except G30: the theorem explicitly restricts semantic isometries to signed permutations.

**Smallest experiment/falsifier.** Implement `MarkedLawrence.lean` first for arbitrary \(A\) and \(r=2\), then general finite \(r\). Ask Python/SNF to produce \(P,Q\) for one depth-one candidate.

**Likely death.** The theorem is easy, but no complete compiler matrix admits the required marked factorization; auxiliary Gram transport may also destroy common energy.

---

### 3. Arithmetic-matroid obstruction to L1

**Mechanism.** Refute candidate L1 realizations using invariants preserved by marked integral equivalence: contract auxiliary columns, retain semantic colors, and record circuit supports plus Smith torsion after reduction modulo several primes. A true higher Lawrence family has repeated brick-local arithmetic matroids and tightly constrained cross-brick circuits.

**Expected move.** Prove that a fanout diamond or three-COPY cycle necessarily has a colored circuit/monodromy signature impossible for any fixed \(A_\star\). That would refute the current L1 edge and justify moving to finite-type toric gluing.

**Audit.** K/D are possible witnesses, not assumptions; this test can refute L1 before soundness, but a matching invariant solves none of them. R and X are outside because no distance amplification or geometric seed is used. G30 is handled by proving invariance only under permitted signed semantic permutations.

**Smallest experiment/falsifier.** Serialize the smallest complete fanout diamond; contract auxiliaries; compute colored circuits and SNF data over \(\mathbb Z\) and \(p=2,3,5\). In Lean, prove preservation of the chosen invariant under allowed row operations and marked permutations.

**Likely death.** The invariant may be too coarse, or auxiliary contraction may erase exactly the obstruction needed to distinguish Lawrence form.

---

### 4. Cellular completion: kill seam homology with fixed 2-cells

**Mechanism.** Regard COPY/fanout wiring as a cellular sheaf: selectors are 0-cochains, glue variables are 1-cochains, and seam cheats are \(H_1\) classes. Add fixed 2-cell rows filling every local COPY cycle, then use elementary collapses to reduce the resulting contractible complex to a higher-Lawrence normal form.

**Expected move.** Prove L1 by a topological induction rather than Beneš switch algebra. Alternatively, a surviving \(H_1\) class gives a structural refutation and identifies the exact missing row.

**Audit.** K: Generation-4 seam, toric exchange, G19 splice, and physical flips become explicit chain classes; G13 affine-span attacks in \(H_0\) are not automatically cured and remain mandatory. D: zero and deleted-cell states are explicit. R: outside L1; no recurrence. X: no tensor or listed lattice geometry.

**Smallest experiment/falsifier.** Build the chain matrices for one fanout diamond and one three-COPY cycle. Compute integral \(H_1\) by SNF before/after adding triangles; then prove in Lean that an elementary free-face collapse preserves the integral kernel up to marked equivalence.

**Likely death.** Filling all cycles may require formula-dependent or unboundedly many cell types, contradicting the fixed-brick requirement.

---

### 5. Finite-group regular-representation router

**Mechanism.** Encode switch states in the regular permutation module \(\mathbb Z[G]\), with routing implemented by fixed permutation matrices and formula choices placed only in targets. Decompose the full compiler into augmentation and nontrivial representation components; seek a uniform kernel theorem componentwise.

**Expected move.** A representation-theoretic normal form could turn arbitrary routing into repeated copies of one fixed brick while retaining marked semantic coordinates. Start with \(G=C_2\), then the width-four switch group.

**Audit.** K: Goal G2 \(A_5\) zero divisors and G19 signed splicing apply directly, not externally; enumerate augmentation-zero signed kernels before promotion. All other K attacks remain full-matrix tests. D is explicit in the augmentation component. R is outside L1. X is outside, but G30 requires checking that NO/control targets are not related by group-coordinate permutations.

**Smallest experiment/falsifier.** Emit a two-switch \(C_2\) diamond using \(2\times2\) regular permutation matrices. Compute exact kernels, augmentation torsion, honest energy, DROP, and all signed vectors in \(\{-1,0,1\}^{m}\).

**Likely death.** Integral group rings contain cheap zero-divisor/augmentation relations; rational Fourier decomposition may not lift to an integral marked equivalence.

---

### 6. Cayley-embedded toric compiler as a conditional roadmap amendment

**Mechanism.** Replace one universal Lawrence brick by finitely many Cayley-embedded tiles whose legal words are vertices \((e_{\text{color}},w)\). Require each tile to have a squarefree unimodular triangulation and glue only along common simplex faces, aiming to force saturation and compatible projections by construction.

**Expected move.** This amends L1 to F1 only if Sketch 3 supplies a marked invariant excluding standard higher Lawrence form. The intended theorem is that simplex-face gluing preserves saturation and yields a finite signed move alphabet.

**Audit.** K: every physical, pair, glue, and normalization coordinate belongs to the Cayley grading, avoiding G6-style filtering; nevertheless toric exchange, G13, G19, and physical flips remain explicit signed-Graver gates. D is a vertex/fiber test. R remains unresolved—especially G28 and bounded-Markov-versus-Graver growth. X is outside.

**Smallest experiment/falsifier.** Cayley-embed one NAND, both COPY orientations, and their smallest diamond. Use Normaliz/4ti2 to test normality, compatible projections, Markov bases, and complete Graver bases; formalize simplex-face saturation for two tiles in Lean.

**Likely death.** Normality may hold while signed Graver support grows under repeated gluing—the exact F2 crux.

---

### 7. Presburger CEGIS for a complete bounded brick plus Lean induction

**Mechanism.** Treat the brick entries, colors, target offsets, and auxiliary markings as bounded integer unknowns. Alternate SMT synthesis against exact counterexamples: kernel identities, equal legal energy, DROP, affine exchange, physical flips, and marked depth-\(1,2,3\) equivalence are all constraints; discovered attacks are fed back as cuts.

**Expected move.** Either synthesize a complete small brick and extract a Lean-checkable local rewrite certificate, or prove UNSAT for a sharply defined bounded class. A Lean theorem must show the rewrite rules imply L1 for every depth; otherwise the output remains merely finite.

**Audit.** K and D are all encoded as unrestricted counterexample queries, not external filters. R is outside the synthesis unless the Lean induction additionally proves an all-depth cost statement. X is excluded syntactically—no tensor or \(D_4/E_6\) seed—while G30 is checked by canonical marked forms.

**Smallest experiment/falsifier.** Bound entries to \(\{-1,0,1\}\), four colors, and at most 16 auxiliaries; synthesize the full switch+NAND+two-COPY+diamond brick. Validate candidates with SNF independently of SMT.

**Likely death.** The search space explodes, or depth three passes without any finite local rewrite system sufficient for an all-depth Lean proof.
