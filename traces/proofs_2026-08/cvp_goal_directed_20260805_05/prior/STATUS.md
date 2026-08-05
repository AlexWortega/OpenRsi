# Status

**OPEN — no hardness lemma established.**

Generation 1 produced one exact finite counterexample. In the tested RS-amplified affine clause gadget with 64 evaluations, integer slack directions annihilate the full residual block. The exact squared objective is 27 against Boolean baseline 19 (distance ratio `sqrt(27/19)`), rather than acquiring residual squared cost at least 57. Residual-only RS amplification is killed in this form; algebraic-number and multi-prime variants with the same unamplified slack mechanism inherit the same causal defect.

Verified by `python3 experiments/verify_rs_slack_cheat.py` (exit 0).

Generation 2 leaves one bounded finite survivor: among all tested degree-one left-regular 12-column matrices, 18 of the 531,441 three-row matrices isolate the signed-selector fiber in `[-3,3]`; no one- or two-row matrix does. Verified by `python3 experiments/verify_affine_isolation_core.py` (exit 0).

Generation 3 removes the box caveat for exactly those 18 matrices. Integral left-kernel certificates and exact rational elimination prove all 126 associated harmful affine fibers empty over `Q`, hence over `Z`. Verified by `python3 experiments/verify_affine_isolation_unbounded.py` (exit 0).

Generation 4 produced no implementation result. Generation 5 kills private-row composition of the local survivor: all 5,832 tested ordered two-clause overlap systems have a nonzero integer kernel move of squared norm at most 4, covering 95,256 compatible references. The local certificate depends on fixing all three marginals and does not survive freeing unshared marginals. Verified by `python3 experiments/verify_overlap_composition.py` (exit 0).

Generation 6's constrained quotient output was invalidated at gate: normalization and consistency were external filters, the audit changed references, and the nine-clause instance has an unrestricted mod-2 bypass. Its finite SNF calculation is not CVP soundness evidence.

Generation 7 kills the selected multi-order radix mutation on that nine-clause instance. The emitted 154-dimensional fixed-target lattice contains all 72 anchors, 41 raw checks, and 41 cyclic base-33 residual rows. Its exact unrestricted squared minimum is 80 versus Boolean completeness squared radius 72. The minimizer is a zero-residual signed selector (`011 + 100 - 111` in the sole clause falsified by `0000`), so every radix coordinate vanishes. Verified by `python3 experiments/verify_multiorder_radix_barrier.py` (exit 0). This is a finite counterexample to the tested mutation only.

Generation 9 gives a finite pass for the sole authorized survivor, a two-parameter incidence-equivariant global PSD metric. Exact rational factor/Gram/center data are emitted for both the obstruction and a satisfiable overlapping control. Their exact unrestricted squared minima are 96 and 72, so the finite distance ratio is `sqrt(4/3)>1.1`. The unsatisfiable nearest vector is nevertheless the seven-term degree-two cube-parity kernel, at constant anchor excess 24. Verified by `python3 experiments/verify_global_psd_metric.py` (exit 0).

Generation 11 kills the authorized fixed cubic extension on the same instances. Cubic rows charge the inherited clause-3 parity, but global triple `(0,2,3)` has only one clause occurrence, allowing the same seven-term parity in clause 1 with zero residual and anchor excess 24. Exact unrestricted squared minima remain 96 and 72. Verified by `python3 experiments/verify_degree3_global_psd_metric.py` (exit 0).

Generation 12 kills one explicit surviving spherical-fingerprint candidate. A dimension-9 clausewise top-Walsh tag raises cube parity to squared distance 153 and gives honest squared radius 81, but an unrestricted clause-drop vector has exact squared distance 105, below the prescribed `4/3` threshold 108. The control exact minimum is 81. Verified by `python3 experiments/verify_spherical_parity_fingerprint.py` (exit 0). Other global Gram/tag families remain untested.

Generation 13 kills the bounded raw-selector linear-code mutation at its required compatibility audit. Over `p=2,3,5,127`, honest differences have rank 14 and maximal compatible syndrome dimension 58. The Generation-11 anchor-excess-24 parity is an integral affine combination of honest encodings with coefficients summing to one, so every compatible linear syndrome is exactly zero on it. Verified by `python3 experiments/verify_selector_code_compatibility.py` (exit 0). Nonlinear and enlarged encodings are not covered.

Generation 14 gives a finite shell pass for the sole surviving complete pair-bag lift. Its 520 selectors and 612 emitted rows have no obstruction vector through squared radius `B+32=552`; the satisfiable control exact minimum is `B=520`. The G11 affine collision lifts only at squared distance 1448, while reconstructed G7 and drop attacks fail the audited shell. Verified by `python3 experiments/verify_pair_bag_lift.py` (exit 0). No fixed-level composition or growing-gap result follows.

Generation 15 kills one preregistered weighted sparse laminar hierarchy. The 200-selector hierarchy has exact control minimum `B=18560` and proposed threshold `T=25472`, but the G13 affine coefficients lift the G11 parity through every level with zero residual at squared distance 24960. Verified by `python3 experiments/verify_weighted_laminar_hierarchy.py` (exit 0). This does not rule out other sparse hierarchies or weight rules.

Generation 19 kills the sole surviving width-5 Barrington flow encoding. The fully emitted 22,754-variable, 17,555-row instance has a zero-residual accepting signed flow with two `-1` coefficients and anchor excess 16. Exact obstruction and control squared minima are 22,770 and 22,754. Verified by `python3 experiments/verify_barrington_signed_flow.py` (exit 0). No signed-flow lower bound or growing gap follows.

Generation 28 exhausts the sole authorized frozen reduced pair-tile recursion through squared radius 57. The rank-32 obstruction/control exact squared minima are 57 and 32. Complete depth-one tables have adverse and legal minima 32 and 16, so the tested growth factors are `lambda=57/32<mu=2`. The emitted partition includes DROP, G13, G19, and all remaining malformed ports. Verified by `python3 experiments/verify_frozen_minplus_pair_tile.py` (exit 0). This finite rule fails its required growth inequality.

Generation 30 kills the sole authorized literal-tensor test on the serialized G28 depth-one seed pair. A coordinate swap `0<->7` maps the alleged NO factor and target exactly to the control; its tensor square pairs every unrestricted integer coefficient matrix. Thus `R_1=R_2=1`, rather than `R_2>R_1`. The complete named-attack shell is paired algebraically, and 131,585 matrices with `l1<=2` are searched exactly. Verified by `python3 experiments/verify_literal_tensor_seed_isometry.py` (exit 0). This is finite evidence about this seed pair only.

Generation 31 gives a finite strict-four-thirds shell pass for the sole authorized equal-radius Gram. The exact control squared minimum is 144. Exhaustive zero-residual moment DP and residual-one low-base enumeration prove no obstruction vector through 192; a parity witness gives upper bound 216. Thus the finite obstruction minimum lies in `[193,216]`, with certified squared ratio at least `193/144>4/3`. Verified by `python3 experiments/verify_equal_radius_walsh_gram.py` (exit 0). No composition or dimension-dependent growth follows.

Generation 32 kills the selected cross-copy composition rule. Exact DP determines the one-copy obstruction minimum `d_1^2=216`, and residual-branch accounting gives two-copy control minimum 288. Despite 125 cross-copy degree-at-most-three moment rows, two compatible parity witnesses have zero residual and cost `432=2d_1^2`; strict superadditivity fails. Verified by `python3 experiments/verify_crosscopy_walsh_composition.py` (exit 0). This is finite evidence about this coupling only.

Generation 33 rejects the sole selectable exterior-bivector mutation at its preregistered completeness gate. For all 512 clause-incidence sign rules, the 16 honest control points have common-sphere system rank 4 and augmented rank 5; the obstruction has the same failure. No rational center exists, so no factor/target or soundness shell is authorized. Verified by `python3 experiments/verify_exterior_bivector_completeness.py` (exit 0). This kills only the explicit Vandermonde-bivector family.

Generation 34 rejects the authorized positive-definite repair of those tags. Across all 512 sign rules, exact center-eliminated equal-sphere constraints have one common rank-10 RREF containing `G[1,1]=0`. This contradicts the preregistered `G>=I/100`, which requires `G[1,1]>=1/100`. Verified by `python3 experiments/verify_exterior_metric_repair_infeasible.py` (exit 0). No factor or shell follows from this finite infeasibility result.

Generation 37 kills the authorized two-level incidence-orbit metric family. Under every normalized anchor/Walsh weighting, the fixed one-copy parity costs `96alpha+120beta`, while two compatible copies cost exactly twice that and annihilate all cross residuals. The exact cut is `delta<=0`; at the emitted rational metric the costs are `3/2` and 3, with control minima 1 and 2. Verified by `python3 experiments/verify_twolevel_metric_parity_cut.py` (exit 0). This does not optimize arbitrary Gram families.

Generation 38 gives a finite `B+64` pass for the authorized 12 splitter bags. The obstruction rank is 117 and no unrestricted vector exists through 181; the matched control exact minimum is 119. Eleven full-variable bags force any residual-square-at-most-two state to one common distribution, but their common legal support is empty and normalization then fails in 11 rows. Verified by `python3 experiments/verify_splitter_clause_bags.py` (exit 0). No bag-family scaling or growing ratio is established.

No hardness lemma or dimension-dependent gap is established.

Target: Prove a deterministic polynomial-time many-one reduction from 3SAT to Euclidean GapCVP with approximation factor n^c for an explicit absolute c>0, without PCP and without unproved conjectures.
