I did not consult the prohibited document or any account of it.

1. **Nakayama-style filtered pullback theorem**

**Mechanism.** Model each tile as a saturated map of free \(\mathcal O\)-modules. Prove in Lean: if  
\[
\delta_{\rm parent}=\pi T\delta_{\rm child}+r,\quad r\in P^{a+2},
\]
and \(\operatorname{gr}(T)\) is injective on every adverse class, then valuation \(a\) becomes exactly \(a+1\); pullbacks preserve this under composition.

**Expected move.** Reduce Q2 to finitely checkable matrices plus one all-depth Lean theorem.

**Falsification.** A mod-\(P\) kernel or nonsaturated pullback.

**Experiment.** Implement `FilteredTransfer.lean` for explicit additive filtrations, then instantiate one NAND–COPY depth-two matrix.

**Audit.** G1/G7: no slack/radix; G6: no external filter; G2–3/G5: all saturated unrestricted glued fibers quantified. G9/G11/G13/G15/G32/G37: no commutative moment/additive metric. G12/Goal-G8: DROP is adverse. G14/G31/G38: no shell extrapolation. G28/G30: no frozen min-plus/tensor seed. G19/Goal-G1: signed states included. Goal-G2: division order, not \(A_5\) ring. G33–34, Goal-G3–5, Goal-G6–7: no exterior/D4/E6 ports. Goal-G11: redundant, not canonical module. Goal-G12 is used, not escaped; COPY remains required.

2. **Finite adverse transducer and zero-gain-cycle test**

**Mechanism.** Quotient every boundary state modulo legal states and \(P^2\), producing a finite weighted transition graph whose edge weight is valuation gain. Prove in Lean that a reachable zero-gain cycle pumps to arbitrarily deep pseudosections; absence of such cycles yields gain \(\ge(d-C)/L\), an explicit weakening of Q2 still sufficient after parameter adjustment.

**Expected move.** Either refute Q2 constructively or replace it by certified average growth.

**Falsification.** The quotient fails to lift because higher carries affect transitions.

**Experiment.** Build the complete graph for the known NAND and the first passing \(N\le8\) COPY; run SCC/minimum-cycle-mean and emit a witness or potential.

**Audit.** G1/G7: no slack/radix; G6: transitions come from emitted rows; G2–3/G5: saturation and unrestricted signed lifts are prerequisites. G9/G11/G13/G15/G32/G37: states are \(P\)-adic, not moment metrics. G12/Goal-G8: DROP is a vertex. G14/G31/G38: the Lean pumping theorem, not a shell, supplies depth. G28/G30: not frozen min-plus/tensoring. G19/Goal-G1: splices are states. Goal-G2: division order. G33–34, Goal-G3–5, Goal-G6–7: unrelated geometry. Goal-G11 avoided. Goal-G12 supplies only NAND; COPY remains open.

3. **Maschke decomposition as a COPY no-go test**

**Mechanism.** First classify COPY tiles equivariant under swapping their two ports. Since \(2\) is invertible mod \(17\), the idempotents \((1\pm\tau)/2\) split every associated-graded module into symmetric and antisymmetric parts; determine whether DROP or \(01/10\) must then possess a grade-zero pseudosection.

**Expected move.** Refute the natural symmetric COPY class, or prove that Q1 must deliberately break port symmetry.

**Falsification.** A saturated equivariant COPY whose adverse fibers avoid both summands.

**Experiment.** Enumerate orbit-multisets for \(N=4,\ldots,8\), compute the two eigenspace fibers, and formalize the representation-theoretic implication in Lean.

**Audit.** G1/G7/G6: no slack, radix, or filtering. G2–3/G5: theorem concerns complete unrestricted fibers, not fixed marginals. G9/G11/G13/G15/G32/G37: no moment metric. G12/Goal-G8: DROP is one classified fiber. G14/G31/G38: structural no-go, not finite-shell growth. G28/G30: no recursion or tensor seed. G19/Goal-G1: signed pseudosections are central. Goal-G2: no group ring. G33–34, Goal-G3–5, Goal-G6–7: no exterior/D4/E6 shell. Goal-G11 irrelevant to COPY. Goal-G12 survives unchanged; this may show it cannot acquire symmetric COPY.

4. **Extension-field block transfer code**

**Mechanism.** Amend Q2 from per-gate growth to macro-tile growth. Collect \(m\) consecutive defect symbols in \(\mathbb F_{289^r}\), apply an explicit Reed–Solomon/Vandermonde checksum, and multiply each nonzero checksum by \(P^m\); a Lean block lemma would show every nonzero adverse window gains \(m\) valuations.

**Expected move.** Permit local cancellation while retaining exponential growth over \(O(\log S)\)-sized blocks.

**Falsification.** An unrestricted signed defect stream lies in the checksum kernel, or memory/DROP costs destroy completeness.

**Experiment.** Take \(m=2,r=1\); glue NAND–COPY–NAND, emit both checksums, and enumerate all fibers modulo \(P^3\).

**Audit.** G1/G7: no free slack or radix residual; G6: memory/checksums are emitted. G2–3/G5: all signed macro-fibers included. G9/G11/G13/G15/G32/G37: coding acts on post-tile \(P\)-defects, not raw-selector compatible hashes or additive moments. G12/Goal-G8: zero-memory DROP included. G14/G31/G38: Lean block induction supplies scaling. G28/G30: new block recurrence, no frozen seed. G19/Goal-G1: signed streams quantified. Goal-G2: division order. G33–34, Goal-G3–7: unrelated geometry. Goal-G11 avoided. Goal-G12 remains the NAND seed; COPY and macro-completeness are unresolved.

5. **Finite-field incidence variety and Nullstellensatz synthesis**

**Mechanism.** For each COPY signature multiset, treat coupling entries as variables over \(\mathbb F_{289}\). Encode grade-zero pseudosections, failed grade-one transfer, saturation minors, and DROP as incidence varieties; elimination either produces a good parameter point or proves the bad projection covers the parameter space.

**Expected move.** Synthesize Q1/Q2 data or prove a whole bounded-rank family impossible.

**Falsification.** Every parameter lies on a bad component, or certificates become intractably large.

**Experiment.** Start with \(N_{\rm COPY}=4\) and one fixed redundant NAND orientation; include \(x^{289}-x\) equations and inverse variables for nonvanishing minors. Lean-check the resulting polynomial identities and a composition-closure lemma.

**Audit.** G1/G7/G6: no slack/radix/external quotient. G2–3/G5: incidence equations include unrestricted glued fibers and saturation. G9/G11/G13/G15/G32/G37: this studies noncommutative graded transfer, not moments. G12/Goal-G8: DROP is an explicit component. G14/G31/G38: only the Lean closure lemma permits extrapolation. G28/G30: no frozen recursion/tensor isometry. G19/Goal-G1: signed coefficients are variables. Goal-G2: no \(A_5\) zero divisors. G33–34, Goal-G3–7: no shell geometry. Goal-G11 avoided. Goal-G12 is fixed input; COPY may still be impossible.

6. **Fitting-ideal volume amplification**

**Mechanism.** Replace a scalar defect by a constant-rank packet. Track the \(r\)-th Fitting ideal—equivalently maximal minors of the underlying integral transfer matrix—so scalar kernels are allowed, but Cauchy–Binet forces packet volume to acquire \(P^r\) per level; Hadamard then forces at least one Euclidean component to be exponentially large.

**Expected move.** Amend Q2 to rank-\(r\) transfer and preserve a positive, possibly divided-by-\(r\), exponent.

**Falsification.** An adverse computation collapses packet rank, or legal packet energy grows at the same rate.

**Experiment.** For \(r=2\), duplicate the NAND boundary, search \(2\times2\) couplings to each COPY candidate, and test all maximal minors modulo \(P^2\). Formalize minor-valuation induction in Lean.

**Audit.** G1/G7/G6: no slack/radix/filtering. G2–3/G5: full packet fibers and overlaps included. G9/G11/G13/G15/G32/G37: multiplicative Fitting ideals replace additive moments. G12/Goal-G8: rank-zero DROP is adverse. G14/G31/G38: Lean induction gives depth. G28/G30: not frozen min-plus/tensoring. G19/Goal-G1: signed rank collapse is tested. Goal-G2: division order. G33–34: exterior algebra is only a proof invariant, not an emitted bivector tag or sphere; Goal-G3–7 geometry is absent. Goal-G11 avoided. Goal-G12 is merely replicated; COPY remains required.

7. **Universal-cover provenance routing**

**Mechanism.** Unfold the balanced circuit to a formula and assign each child edge a disjoint provenance summand. A parent prefixes the path label and multiplies that summand by \(P\); defects from different children never occupy the same coordinate, so signed cancellation cannot erase the selected adverse root-to-leaf chain.

**Expected move.** Amend Q2/Q3 jointly: prove valuation growth by disjoint support, with a Lean bound \(n=O(S\log S)\) or another explicit polynomial.

**Falsification.** Variable-consistency COPY networks cause superpolynomial unfolding, or signed states cross provenance channels through an unguarded glue.

**Experiment.** Emit the depth-two NAND–COPY tree with left/right-tagged channels and exhaust grade zero/one; then prove the path-support induction in Lean.

**Audit.** G1/G7/G6: no slack/radix/filtering. G2–3: unrestricted channel fibers included. G5 private-row overlap is outside because provenance rows propagate to the root rather than freeing unshared marginals. G9/G11/G13/G15/G32/G37: no moment/additive coupling. G12/Goal-G8: DROP is routed as adverse. G14/G31/G38: Lean path induction supplies scaling. G28/G30: no frozen recursion/isometric seed. G19/Goal-G1: diagonal splices are explicitly cross-channel states. Goal-G2: no group ring. G33–34, Goal-G3–7: no shell geometry. Goal-G11 avoided. Goal-G12 supplies NAND only; COPY and polynomial unfolding are genuine obligations.
