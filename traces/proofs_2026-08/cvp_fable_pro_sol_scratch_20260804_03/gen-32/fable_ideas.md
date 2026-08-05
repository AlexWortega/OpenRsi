## 1. Noncommuting expander-coupled Gram forms

**Mechanism.** Replace G31’s block-diagonal Walsh factor by edge terms  
\(\|U_{e,c}z_c-U_{e,d}z_d\|^2\), where the \(U\)’s are noncommuting signed representations and clause blocks form an explicit expander. Balance diagonal terms so every honest global assignment has equal energy.

**Expected move.** Prove a recurrence \(R_{t+1}\ge(1+\varepsilon)R_t\) under graph lifts; logarithmic depth would yield a polynomial ratio.

**Obstruction audit.** G1 slack—none; G2/3 isolation—global rather than local; G5 overlap—rows are shared, not private; G6 quotient—all coordinates emitted; G7 radix—no radix, though exact kernels remain possible; G9/G11 parity—edge forms should spread it; G12 drop—charged by expansion; G13 affine collision—not a common-target hash; G14 pair bags—compatible but coupled; G15 hierarchy—cyclic, not laminar; G19 flow—absent; G28 min-plus—nonidentity spectral seams; G30 tensor—reject seed isometries first; G31 Walsh—removes isotropy, but not its constant-gap cap without growth.

**Experiment/falsification.** On the prescribed 18-clause two-copy union, enumerate small signed-permutation \(U_e\)’s, certify control minimum 288, and search through \(2d_1^2\). Kill on a cheap parity/drop or no strict growth.

**Likely death.** A bounded-support affine mixture simultaneously isotropizes all edge forms.

---

## 2. Plücker/compound-matrix lift of pair bags

**Mechanism.** Map each joint bag label to a decomposable bivector \(u(a)\wedge u(b)\), retaining all Plücker coordinates and shared-clause contractions. Exterior powers turn rank-one consistency into curved secant geometry; compound matrices also compose multiplicatively.

**Expected move.** Establish that every malformed integral secant has growing Plücker energy while honest decomposable states retain equal radius.

**Obstruction audit.** G1—no slack; G2/3—secant separation, not fixed affine-fiber isolation; G5—contractions cross overlaps; G6—all lifts emitted; G7—exact linear kernels may survive, so not outside it; G9/G11—higher wedges target cube parity; G12—normalization wedge charges zero blocks; G13—not a common syndrome, although affine secants remain dangerous; G14—strict enlargement of pair bags; G15—affine hierarchy lifts may still survive; G19—no flow; G28—no frozen min-plus rule; G30—compound composition is not literal seed tensoring, but isometries must be checked; G31—nonorthogonal anisotropic Gram, not \(H_8^TH_8=8I\).

**Experiment/falsification.** Add bivector columns to the G14 manifest and first evaluate G7, G11/G13, and every one-bag drop; then exhaust through \(B+32\). Kill if any known attack’s energy is unchanged.

**Likely death.** Decomposable points have short integral secant identities—Plücker analogues of cube parity.

---

## 3. Integral homology with a large systole

**Mechanism.** Regard clause labels as 2-cells, consistency equations as boundaries, and the target as a prescribed relative homology class. Glue formula complexes through explicit expander covers so an unsatisfied instance admits no short integral representative, while a satisfying assignment supplies a canonical chain.

**Expected move.** Obtain an integral systole \(N^{1/2+c}\) against a YES norm \(O(\sqrt N)\), or exclude bad zero-boundary chains and then scale boundary coordinates polynomially.

**Obstruction audit.** G1—no slack; G2/3—asks for a global kernel theorem; G5—uses shared boundaries; G6—all chain equations emitted; G7—zero-residual cycles are central, not avoided; G9/G11 parity—becomes a short cycle, so not outside; G12—drops have boundary; G13—affine collisions may be cycles; G14—pair bags can serve as 2-cells; G15—hierarchy mixtures may become boundaries; G19—signed splicing is exactly an integral-cycle threat; G28—expander covers replace identity recursion; G30—no tensor seed; G31—different geometry, but still needs genuine growth.

**Experiment/falsification.** Build the G14 incidence complex and its smallest two 2-lifts; compute SNF, enumerate primitive cycles through excess 64, and compare relative systoles for obstruction/control.

**Likely death.** Cube-parity or signed-flow attacks become constant-size null-homologous cycles in every cover.

---

## 4. Number-field norm barrier

**Mechanism.** Label selector states by algebraic integers in a degree-\(D\) field and measure errors using the rational trace Gram \(Q_{ij}=\mathrm{Tr}(\alpha_i\overline{\alpha_j})\), with orthogonal padding equalizing honest energies. The product formula makes every nonzero algebraic error have nonzero integral norm, potentially forcing a large conjugate under recursively chosen weights.

**Expected move.** With \(D=\Theta(\log n)\), turn nonzero selector error into \(n^{\Omega(1)}\) Euclidean energy without carry or slack variables.

**Obstruction audit.** G1—no slack; G2/3—quantitative global isolation; G5—one field element aggregates overlaps; G6—trace coordinates are emitted; G7—not radix, but exact algebraic kernels remain fatal; G9/G11—parity must have nonzero field image; G12—zero blocks violate a padded normalization coordinate; G13—not a common-target syndrome, though affine combinations may balance conjugates; G14—can label pair bags; G15—affine lifts are not automatically excluded; G19—no flow; G28—norm multiplication suggests a new recurrence; G30—not tensoring an isometric seed; G31—anisotropic trace Gram, but finite constant caps may persist.

**Experiment/falsification.** Use degree-4 and degree-8 real cyclotomic subfields on the 72-selector instance; enumerate the G31 shell and compare minimum conjugate energy of parity, drop, and honest vectors.

**Likely death.** Units balance all conjugates, leaving only an \(O(D)\) additive penalty.

---

## 5. Truncated noncommutative path signatures

**Mechanism.** Strengthen the Barrington encoding with ordered tensor signatures of transitions through degree \(k\), following Chen’s iterated-integral multiplicativity (K.-T. Chen, 1958). Honest paths satisfy linear prefix recurrences, whereas splicing paths with negative coefficients should leave an ordered-word discrepancy invisible to ordinary conservation.

**Expected move.** Show that an exact accepting signed flow matching degree-\(k\) signatures needs \(2^{\Omega(k)}\) negative support; choose \(k=\Theta(\log n)\) and polynomially scale the first unmatched signature row.

**Obstruction audit.** G1—no slack; G2/3—global ordered isolation; G5—prefix data cross every layer; G6—all signature states emitted; G7—zero signature kernels remain possible; G9/G11—unordered parity should be visible in ordered words; G12—path drops violate degree zero; G13—affine path mixtures remain a threat; G14—unrelated bag enlargement; G15—not laminar marginal propagation; G19—direct strengthening, therefore not outside its signed-splicing obstruction; G28—no min-plus tile; G30—tensor algebra is used, but not literal CVP seed tensoring; G31—non-Gram mechanism.

**Experiment/falsification.** Add degree-two signatures to the existing G19 verifier and run exact shell DP through anchor excess 32. Kill if the two-negative accepting flow lifts exactly or merely moves to four negatives.

**Likely death.** Every finite truncation admits a Möbius-cancellation flow of constant support.

---

## 6. Nonlinear-symbol sheaf expander code

**Mechanism.** Cover the incidence graph by constant-size variable windows; each window has one-hot full-assignment symbols, restriction maps on overlaps, and an outer expander code on disagreement symbols (classical inspiration: Sipser–Spielman, *Expander Codes*, 1996). Unlike G13, coding occurs after enlarging to window symbols rather than hashing raw clause selectors.

**Expected move.** Prove the exact integral zero-syndrome fiber consists only of honest global assignments. Then any NO vector has a nonzero integral syndrome, whose coordinates can be scaled by \(N^c\) at no completeness cost.

**Obstruction audit.** G1—no slack; G2/3—global integer-fiber claim; G5—overlaps participate in Tanner checks; G6—all checks emitted; G7—exact signed pseudocodewords remain fatal; G9/G11—windows containing parity support should detect it; G12—drops create many failed checks; G13—raw-hash assumption is avoided, but affine global mixtures may lift; G14—generalizes pair bags; G15—its affine hierarchy counterexample directly threatens this and is not escaped automatically; G19—no path flow; G28—expander decoding replaces fixed min-plus composition; G30—no literal tensor; G31—coding rather than isotropic Gram.

**Experiment/falsification.** Use radius-two windows on the nine-clause obstruction, a 3-regular Tanner graph, and exact SNF plus shortest-kernel search through excess 64.

**Likely death.** The G13 affine coefficients define an exact signed section on every finite window.
