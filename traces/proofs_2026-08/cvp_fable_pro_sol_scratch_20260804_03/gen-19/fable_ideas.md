I use the recurring obstruction labels as follows: **O1** free slack/carry bypass; **O2** short overlap kernels; **O3** exact-zero residual defeats amplification; **O4** parity relocation and clause drops; **O5** localized unsatisfiability/composition; **O6** the G13 integral affine lift; **O7** polynomial-size explicitness; **O8** dimension-growing gap. The sketches are deliberately unranked.

### 1. Noncommutative branching-program acceptance

**Core trick.** Compile formula evaluation into a polynomial-length width-5 permutation branching program, then encode a unit layered flow ending at ACCEPT. Unlike clausewise moments, the endpoint is determined by an ordered noncommutative product; every affine combination of complete rejecting paths still rejects.

**Expected move.** Force the G13 selector either to violate a transition/variable-consistency row or use many negative edges.

**Obstruction check.** **O1/slack:** all edges and consistency variables enter the emitted objective; no free slack. **O2/overlap:** global state couples clauses, although signed circulations may survive. **O3/zero residual:** not escaped if a spliced accepting flow exists. **O4/parity/drop:** global acceptance detects honest drops, but perhaps not signed flows. **O5/localization:** no spreading theorem yet. **O6/affine lift:** outside raw-selector assumptions because product state is nonlinear; local splicing remains unresolved. **O7/size:** polynomial by Barrington’s theorem. **O8/gap:** requires an Ω(length) negative-flow bound, presently absent.

**Falsification.** Any zero-residual accepting signed flow for the nine-clause obstruction.

**Experiment.** Emit its smallest layered permutation program; enumerate edge coefficients in `[-2,2]` with exact endpoint and query-consistency rows.

**Likely death.** Negative flow splices incompatible rejecting paths into ACCEPT.

---

### 2. Existential portfolio of incompatible centers

**Core trick.** G13 assumes every honest assignment must map compatibly to one target. Instead emit polynomially many hash-indexed blocks and let the CVP witness choose one block; every assignment need only be cheap in some block, allowing each block to linearly separate most assignments and their affine collisions.

**Expected move.** Cover all honest assignments while placing every known signed attack and drop far from every selectable center.

**Obstruction check.** **O1/slack:** block-selection coefficients are unrestricted and must be audited. **O2/overlap:** each block is global, not private. **O3/zero residual:** an attack cheap in one block kills it. **O4/parity/drop:** include both in center synthesis. **O5/localization:** portfolio coverage alone gives no composition. **O6/affine lift:** genuinely outside the “one hash constant on all honest encodings” assumption. **O7/size:** open—polynomial covering family is essential. **O8/gap:** needs zero-baseline separation followed by scaling; finite separation is insufficient.

**Falsification.** A signed mixture of block selectors and assignment selectors no farther than an honest point.

**Experiment.** On the 16 four-variable assignments, synthesize 4–8 integer centers by MILP, then emit columns indexed by `(block, assignment)` and exactly search the G13 shell.

**Likely death.** Polynomially many blocks cannot cover all assignments without one block containing a dangerous affine dependency.

---

### 3. Torsion-homology amplifier

**Core trick.** Map enlarged tuple-label defects to chains in an integral complex having a large torsion invariant. A nontrivial defect class cannot be filled integrally, or requires coefficients of order \(q\), converting a unit semantic defect into large Euclidean cost via Smith-normal-form arithmetic.

**Expected move.** Make pair-bag inconsistencies represent a torsion class rather than an ordinary residual that slack can cancel.

**Obstruction check.** **O1/slack:** filling chains are explicit anchored variables. **O2/overlap:** topology is global, although null-homologous local circuits remain. **O3/zero residual:** exact-zero defects bypass the construction completely. **O4/parity/drop:** only charged if the tuple-to-chain map sends them to nonzero classes. **O5/localization:** large systole would be needed. **O6/affine lift:** not escaped by a linear raw-selector map; enlarged pair/quadruple labels are mandatory. **O7/size:** sparse boundary matrices with prescribed SNF are polynomially explicit. **O8/gap:** \(q=N^\alpha\) has polynomial bit length, but a semantic nontriviality theorem is missing.

**Falsification.** G13 lifts to a boundary-zero chain, or a short filling exists despite torsion.

**Experiment.** Attach the G14 pair-bag matrix to a boundary block with SNF invariant \(q=5\); enumerate all known attacks and compute exact minimum fillings.

**Likely death.** Every harmful affine pseudodistribution maps to the zero homology class.

---

### 4. Unstable linear-dynamics amplifier

**Core trick.** Once any integer separator produces defect \(d\), append anchored states satisfying \(y_0=d,\ y_{i+1}=2y_i\). With objective
\[
W(d-y_0)^2+W\sum_i(y_{i+1}-2y_i)^2+\sum_i y_i^2,
\]
nonzero \(d\) costs roughly \(\min(W,4^L)d^2\), while honest \(d=0\) adds zero completeness cost.

**Expected move.** Turn a single unavoidable tuple-level defect into an \(N^c\) gap using \(L=\Theta(\log N)\).

**Obstruction check.** **O1/slack:** every auxiliary is anchored and every recurrence row emitted. **O2/overlap:** irrelevant after a global separator exists. **O3/zero residual:** completely vulnerable to \(d=0\). **O4/parity/drop:** amplified only when detected. **O5/localization:** one detected defect suffices, so no density premise. **O6/affine lift:** not escaped; G13 may give \(d=0\). **O7/size:** \(O(\log N)\) dimensions and polynomial-bit entries. **O8/gap:** explicitly supplies polynomial growth conditional on separation.

**Falsification.** An auxiliary assignment truncates the recurrence below the predicted exact minimum.

**Experiment.** Use \(L=6,W=4^7\), exhaust \(d\in[-3,3]\) and all feasible \(y_i\); then attach it to each nonzero G14 audit residual.

**Likely death.** The only attacks that matter—including G13—have exactly zero seed defect.

---

### 5. Superimposed-code aggregation of global ANDs

**Core trick.** Choose a deterministic constant-weight superimposed code on clauses. For each code row, build a balanced truth-table circuit computing the AND of the selected clauses and demand output one; any genuine false clause corrupts many zero-residual outputs rather than one local row.

**Expected move.** Spread clause drops and sparse unsatisfaction before applying a large output weight.

**Obstruction check.** **O1/slack:** every gate-table selector and wire equality must appear in the CVP objective. **O2/overlap:** clause outputs feed many global circuits, so rows are not private. **O3/zero residual:** a signed accepting gate history is fatal. **O4/parity/drop:** genuine drops spread; parity pseudogates may not. **O5/localization:** combinatorially escaped for honest assignments because one false clause hits many rows. **O6/affine lift:** complete rejecting histories cannot affinely produce output one, but locally consistent signed histories may. **O7/size:** \(O(m^2)\) gates suffices for a simple explicit code. **O8/gap:** a nonzero output can be weighted polynomially without increasing honest residual; gate-anchor baseline still needs accounting.

**Falsification.** A zero-output-residual signed gate assignment for the nine-clause formula.

**Experiment.** Use an 18-row binary code with each clause in nine rows; emit two-input AND tables and enumerate coefficients in `[-2,2]`.

**Likely death.** Signed gate selectors synthesize accepting aggregate histories not arising from any assignment.

---

### 6. Global Walsh bags as nonlinear norm fingerprints

**Core trick.** Add selectors for sampled variable subsets \(S\), and give each assignment on \(S\) its Walsh sign \(\chi_S\). Honest one-hot bags always contribute squared fingerprint one, whereas a signed distribution contributes \((\sum_a c_a\chi_S(a))^2\); thus the G13 affine lift remains linearly consistent but can become metrically expensive.

**Expected move.** Use deterministic splitters to sample enough subsets that every low-support signed pseudodistribution has many large Fourier coefficients.

**Obstruction check.** **O1/slack:** no slack; all bag selectors are anchored. **O2/overlap:** shared subset bags globally couple occurrences. **O3/zero residual:** fingerprints can still equal honest magnitudes exactly. **O4/parity/drop:** degree-four bags catch the known parity; higher-degree relocation remains. **O5/localization:** no composition theorem. **O6/affine lift:** outside compatible-linear-syndrome assumptions because separation is quadratic norm, not a vanishing linear hash. **O7/size:** fixed degree gives \(n^{O(d)}\); growing degree threatens polynomiality. **O8/gap:** the G13 \(\ell_1=9\) bound permits only a constant factor unless larger instances force growing signed mass.

**Falsification.** A low-anchor signed state with every sampled Walsh amplitude \(\pm1\).

**Experiment.** For four variables emit all 81 subset-assignment selectors, full marginal rows, and all 15 nonconstant Walsh fingerprints; exactly search through G15’s attack radius.

**Likely death.** Parity relocates beyond sampled degree, or constant-support affine attacks impose a constant-factor ceiling.

Classical ingredients: Barrington, *JCSS* 38 (1989); Naor–Schulman–Srinivasan, “Splitters,” *FOCS 1995*; Kautz–Singleton, “Nonrandom Binary Superimposed Codes,” *IEEE TIT* 10 (1964).
