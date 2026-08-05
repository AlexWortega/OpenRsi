# Idea population

## Generation 1: RS residual spreading — killed in its tested slack form

Selected Pro proposal 1, the best survivor of cross-review. Mechanism: evaluate an integral clause-residual polynomial at 64 points, so any nonzero degree-7 residual has at least 57 nonzero integral evaluations. Expected move: soundness norm at least `sqrt(57)`. Falsification: integer slack values make every residual zero while paying only an unamplified anchor cost.

`experiments/verify_rs_slack_cheat.py` realizes the attack on the unsatisfiable formula containing all eight clauses on three variables. With half-integral anchors `(2z-1)^2`, its exact finite squared optimum is 27 versus Boolean baseline 19, a ratio `sqrt(27/19)`: a false clause uses slack `(-1,0)` and all amplified coordinates vanish. This kills residual-only RS amplification with free integer slack directions; it does not rule out amplifying Booleanity itself.

## Generation 2: affine/Graver isolation — bounded survivor

Selected Pro proposal 6, the only proposal surviving opponent review. Mechanism: replace nonlinear Booleanity by an integer nullspace property that excludes signed selector relaxations. Expected move: a measurement matrix leaves no short harmful kernel direction. Falsification: every tested matrix retains such a direction.

`experiments/verify_affine_isolation_core.py` exhausts all degree-one left-regular `0/1` matrices with 12 columns and 1–3 rows on one falsified OR core, searching selector and auxiliary coefficients in `[-3,3]`. All 1- and 2-row matrices retain squared-norm-2 cheats. Of 531,441 three-row matrices, 18 isolate the harmful fiber in the tested box. This is a finite survivor, not a reduction or scaling lemma; it warrants testing overlap composition and higher column degree.

## Generation 3: exact affine-fiber audit — local survivor certified

Selected Fable proposal 1, also required before Pro proposal 1 by both reviews. Mechanism: replace boxed isolation by an exact arithmetic certificate for the unbounded affine fiber. Expected move: a left-kernel/Smith-type obstruction proves no signed selector cheat exists over all integers. Falsification: a rational or integer harmful point, especially one of squared norm at most 4.

`experiments/verify_affine_isolation_unbounded.py` constructs all 18 Generation-2 survivors. For each of seven legal one-hot references it finds an integral vector `w` with `w^T A=0` but `w^T b != 0`, and independently row-reduces the system over `Q`. All 126 harmful affine systems are inconsistent even over `Q`; the bounded observation was not a box artifact. This remains a constant-size local fact and does not address overlap or polynomial gap scaling.

## Generation 5: private-row overlap composition — killed

Selected Pro proposal 1, matching the mandatory overlap audit selected by both reviews. Mechanism: keep clause syndrome rows private and identify only shared variable marginals, hoping local affine isolation composes. Expected move: every harmful composed fiber remains inconsistent or has no integer point of squared norm at most 4. Falsification: a short integer kernel circuit preserves normalization, private measurements, and shared marginals.

`experiments/verify_overlap_composition.py` covers all 5,832 ordered survivor-pair/overlap/polarity systems for one or two shared variables and 95,256 compatible one-hot reference pairs. Every system has a nonzero integer kernel move of squared norm at most 4, supported in one clause. Thus the certified fixed-marginal local obstruction does not survive when unshared marginals are freed. Private clause syndromes and their proposed occurrence blow-up are killed in this form; unrelated global mechanisms are not ruled out.

## Generation 6: global honest-difference quotient — invalidated at gate

The constrained search found no exact or binary zero quotient syndrome among 156,880 filtered deviations. The gate correctly rejected this as CVP evidence: normalization and consistency were external filters, distances changed reference, and the nine-clause four-variable instance has an unrestricted mod-2 bypass. The finite SNF and filtered-enumeration outputs remain reproducible but do not certify the emitted lattice.

## Generation 7: multi-order radix barrier — killed at finite size

Only Pro Proposal 5 survived cross-review for one bounded test. Mechanism: put all normalization, legality, and occurrence-consistency residuals into the lattice, then encode every cyclic base-33 ordering so a bounded nonzero residual has a leading digit. Expected move: nonzero residuals exceed the Boolean completeness radius. Falsification: an exact signed-selector residual kernel, which every radix row maps to zero.

`experiments/verify_multiorder_radix_barrier.py` emits a fixed-target 154-dimensional basis with 72 selector anchors, 41 raw checks, and 41 cyclic radix rows, and checks its canonical column HNF. On the nine-clause instance the exact unrestricted squared CVP minimum is 80 versus Boolean completeness squared radius 72. The minimizer has zero residual: for assignment `0000`, clause 0 replaces forbidden `000` by `011 + 100 - 111`; all other clauses use honest one-hot labels. Thus all radix coordinates vanish and the distance ratio is only `sqrt(80/72)`. This kills this linear radix mutation on the finite obstruction, not all radix constructions or any asymptotic class.

## Generation 9: global degree-two PSD metric — finite 1.1 survivor

Only Fable proposals survived cross-review; Proposal 1 alone was authorized for a repaired bounded test. The predeclared two-parameter metric uses anchors plus all-pairs consistency of global singleton and pair moments. Its Gram form is `Q=4I+25 A^T A`, so it is rational positive definite and incidence-equivariant.

`experiments/verify_global_psd_metric.py` emits exact Gram/center/factor data for the nine-clause obstruction and a fixed satisfiable nine-clause control. The old `011+100-111` attack gets nonzero residual. Exact signed low-weight search instead finds the seven-term cube-parity kernel at anchor excess 24. Consequently the exact unrestricted squared minima are 96 and 72, giving finite distance ratio `sqrt(4/3)>1.1`. This passes only the prescribed finite test; the constant-cost parity kernel supplies no composition theorem or growing gap.

## Generation 11: all available cubic moments — killed on the fixed instance

Both reviews authorized only the common cubic-moment proposal. Mechanism: add every all-pairs squarefree cubic moment row to charge the Generation-9 parity kernel. Expected move: raise the obstruction minimum above 96 while preserving control minimum 72. Falsification: any cubic-zero signed selector with constant anchor excess, or no increase in the obstruction minimum.

`experiments/verify_degree3_global_psd_metric.py` emits the unrestricted metric `Q=4I+25 A_{<=3}^T A_{<=3}` and exactly searches all zero-residual states through anchor excess 24. The inherited clause-3 parity is charged, but clause 1 is the unique occurrence of global triple `(0,2,3)`; the same seven-term parity there has no cubic comparison row. The exact squared minima remain 96 and 72. This kills only this fixed cubic mutation and establishes no asymptotic claim.

## Generation 12: dimension-9 spherical Walsh fingerprint — killed by clause drop

Both reviews left only global PSD/spherical-fingerprint synthesis as an executable bounded direction. The selected Pro Proposal 6 candidate adds one top-Walsh tag coordinate per clause. Every one-hot label has tag norm one, so all honest nine-clause encodings gain the same squared radius `H=9`; a seven-term parity changes one tag from magnitude one to seven. Expected move: obstruction distance squared strictly above `(4/3)(72+9)=108`. Falsification: any unrestricted vector at or below 108.

`experiments/verify_spherical_parity_fingerprint.py` emits `Q=4I+25 A_{<=3}^T A_{<=3}+F^T F` and exactly enumerates the full shell through 108. Cube parity rises to 153, but dropping clause 0 gives anchor 72, residual cost 25, and fingerprint cost 8, totaling 105. The control minimum is 81. Thus this explicit fingerprint has squared ratio `35/27<4/3`; this finite kill does not rule out other Gram or tag families.

## Generation 13: raw-selector syndrome compatibility — killed by an affine collision

The only conditional coding survivors required a compatibility audit before emitting Construction-A carries. Mechanism: choose linear syndrome rows in the orthogonal complement of all differences among the 16 globally consistent one-hot encodings, then use code distance on any nonzero syndrome. Expected move: every known low-anchor harmful selector has nonzero maximal compatible syndrome. Falsification: one harmful selector in the honest affine span.

`experiments/verify_selector_code_compatibility.py` computes the maximal 58-dimensional compatible syndrome space over `p=2,3,5,127`. The Generation-11 unique-triple parity, at anchor excess 24, is an exact integral affine combination of the 16 honest encodings with coefficient sum one. Its syndrome is therefore zero for every compatible linear hash over every modulus. This kills the raw 72-selector linear Construction-A/code mutation before carries or scaling; it does not address nonlinear or enlarged encodings.

## Generation 14: complete pair-bag lift — finite shell pass

Only Fable Proposal 2 survived cross-review. Mechanism: replace raw clause selectors by joint selectors for every intersecting clause pair and equate complete clause-label marginals across the full pair mesh. Expected move: prevent G7/G11 and drop attacks from remaining local. Falsification: any unrestricted obstruction vector through baseline `B+32`, or control minimum different from `B`.

`experiments/verify_pair_bag_lift.py` emits 520 pair-bag selectors and 612 normalization, legality, and full-marginal rows for `||2z-1||^2+25||Az-b||^2`. It proves no obstruction vector exists through `552=B+32`; the control exact minimum is `B=520`. The G11 affine collision lifts only with anchor excess 928, G7 fails to extend on seven incident bags, and all audited bag/clause drops exceed the shell. This is a finite pass only; fixed pair bags have no composition theorem or growing-gap law.

## Generation 15: weighted sparse laminar hierarchy — killed by zero-residual affine lift

Both reviews selected only the weighted sparse/laminar hierarchy for one preregistered falsification. The frozen adjacent-pair tree has clause leaves and 2-, 4-, 8-, and 9-clause assignment nodes, unscaled anchor weights `1` and `1/16`, residual weight `16`, and `delta=1/2`. Its integral squared-distance scaling has baseline `B=18560` and threshold `T=B+256*9^(3/2)=25472`. Expected move: weighted ancestors force any harmful lift above `T`. Falsification: a harmful unrestricted vector below `T`, especially at zero residual.

`experiments/verify_weighted_laminar_hierarchy.py` emits all 200 selectors and 210 rows. The Generation-13 affine coefficients lift the G11 parity through every hierarchy node with exactly zero residual. Leaf anchor excess is 6144 and eight internal nodes add 256, giving total 24960, which is 512 below `T`. Single-leaf drops are expensive, but the affine pseudodistribution threads the hierarchy. This kills only the frozen hierarchy and weights, not all sparse hierarchies.

## Generation 19: width-5 Barrington accepting flow — killed by signed splicing

Only Fable Proposal 1 survived. Mechanism: compile the balanced CNF to a width-5 permutation branching program, emit unit-flow, ACCEPT sink, and repeated-query rows, and rely on the nonlinear ordered product to prevent the G13 affine rejection mixture from accepting. Expected move: no integral exact ACCEPT fiber for the obstruction. Falsification: any zero-residual accepting signed flow.

`experiments/verify_barrington_signed_flow.py` emits a 3,250-layer program with 22,754 unrestricted coefficients and 17,555 rows. Exact shell DP exhausts anchor excess at most 8 and then finds an accepting exact-flow vector at excess 16, using two coefficients `-1`. Since a nonzero integral residual costs at least 25, the exact obstruction and control squared minima are 22,770 and 22,754. This kills the emitted flow encoding and supplies no composition or growing-gap result.

## Generation 28: frozen reduced pair-tile recursion — finite growth failure

Only Pro proposals survived cross-review; Proposal 6 was the sole authorized bounded falsifier. Its mechanism is complete full-assignment ports and exact min-plus composition of two frozen reduced G14 tiles. Expected move: illegal cost growth `lambda` strictly larger than legal growth `mu`. Falsification: nonclosure, a cheap attack, control mismatch, or `lambda<=mu`.

`experiments/verify_frozen_minplus_pair_tile.py` serializes two same-variable pair bags per tile, identity glue, all six port classes, a matched control, and the complete unrestricted tables through squared radius 57. The depth-two obstruction and control exact squared minima are 57 and 32. Depth-one adverse and legal minima are 32 and 16, so `lambda=57/32<mu=32/16=2`. DROP, G13, and exact two-negative G19 diagonal seeds cost 132, 303, and 221. This is a finite failure of this recursion rule, not a composition theorem or asymptotic result.

## Generation 30: literal tensor of the G28 depth-one seed — killed by seed isometry

Only Fable proposals survived cross-review; Proposal 3 was the sole authorized bounded test. Its mechanism is literal Kronecker multiplication of a fixed integer factor and target. Expected move: the exact NO/YES squared-distance ratio should satisfy `R_2>R_1`. Falsification: `R_2<=R_1` or an unrestricted entangled shortcut.

`experiments/verify_literal_tensor_seed_isometry.py` emits the rank-16 G28 right-tile factors `C=[2I;5A]`, their targets, and the rank-256 tensor-product rules. Swapping assignment coordinates 0 and 7 in both bags maps the alleged NO seed exactly to its control, including factor rows and target. Tensoring this permutation pairs every unrestricted integer coefficient matrix, so `R_1=R_2=1` without a rank-one assumption. The attack shell through 31,285 has coefficient bound `[-60,60]`; DROP, best diagonal G13/G19, and a rank-two malformed state cost 4,356, 31,285, 11,749, and 4,420. Exact search of all 131,585 matrices with `l1<=2` also agrees across the pair. This kills only this serialized seed pair, not arbitrary tensor lattices.

## Generation 31: equal-radius Walsh Gram — finite strict-four-thirds shell pass

Only Pro proposals survived cross-review; Proposal 7 was the sole authorized bounded audit. Its mechanism is to add discrepancy rows whose values differ across honest encodings but whose norms are equal, avoiding a common linear syndrome. Expected move: an obstruction squared distance strictly above `4/3` of the control. Falsification: factor/center failure, control mismatch, or any unrestricted obstruction vector through the threshold.

`experiments/verify_equal_radius_walsh_gram.py` freezes nine full `H_8` Walsh blocks and residual scale 10, giving `Q=12I+100A^T A`. Every globally consistent one-hot encoding has discrepancy energy 144, and the control exact minimum is 144. The derived shell interval is `[-3,3]`. Exact moment DP eliminates every zero-residual obstruction vector through 192, while complete enumeration of the 2,701 vectors that could have residual square one finds minimum residual square 7. Hence the finite obstruction minimum lies in `[193,216]`, for certified squared ratio at least `193/144>4/3`; G13/G11 parity gives the upper bound 216 and the repaired clause drop costs 236. This is a finite pass only, with no composition or dimension-gap law.

## Generation 32: cross-copy moment coupling — killed by additive parity

Both populations had one cross-review survivor. Pro Proposal 1 was selected because it directly tests composition of the Generation-31 finite pass with a fully emitted two-copy instance. Its mechanism couples two copies by every shared global moment row through degree three. Expected move: strict superadditivity `d_2^2>2d_1^2` while the matched control remains 288. Falsification: control mismatch or any unrestricted vector at or below `2d_1^2`.

`experiments/verify_crosscopy_walsh_composition.py` first exhausts the one-copy shell and proves `d_1^2=216`. It then emits two 9-clause copies sharing variables 0 and 1, with 125 cross-copy moment rows, rank 144, and coefficient interval `[-4,5]` through threshold 432. Residual-branch accounting proves the matched control exact minimum is 288. Compatible G11/G13 parity blocks in clauses 1 and 10 preserve all shared moments and give a zero-residual vector of cost `432=2d_1^2`. Thus strict growth fails. This finitely kills this coupling rule only.

## Generation 33: exterior bivector coherence — rejected by completeness

Only Fable proposals survived cross-review; Proposal 6 was the sole selectable bounded mutation. Its mechanism puts six Plücker coordinates for each local label into one shared exterior block, hoping signed parity adds coherently while honest encodings remain on a common sphere. Expected move: pass exact equal-completeness certification before one/two-copy soundness search. Falsification: no canonical incidence-sign rule admits a rational common center and radius.

`experiments/verify_exterior_bivector_completeness.py` freezes label `t` as `v(t) wedge v(t+1)` for `v(t)=(1,t,t^2,t^3)` and exhausts all `2^9=512` clause-sign rules. For both the matched control and obstruction, every 16-point common-sphere system has coefficient rank 4 and augmented rank 5. Thus zero sign rules are cospherical, even with an arbitrary rational center. The candidate is rejected before factor/target or shell construction, exactly as preregistered. This kills only this explicit bivector/sign family.

## Generation 34: positive-definite repair of exterior tags — exactly infeasible

Only Fable proposals survived cross-review; Proposal 1 alone was authorized as a completeness-only repair of Generation 33. Its mechanism searches one shared rational `6x6` metric `G`, separate formula centers, `trace(G)=1`, and `G>=I/100`. Expected move: make both 16-point honest sets cospherical. Falsification: exact infeasibility or singular-only solutions.

`experiments/verify_exterior_metric_repair_infeasible.py` eliminates the center/radius variables using affine dependencies of the honest points and audits all 512 sign rules. Every rule gives the same rank-10 homogeneous constraint row space on the 21 Gram entries. Its exact RREF contains the unit equation `G[1,1]=0`, contradicting the lower-bound requirement `G[1,1]>=1/100`. Therefore no positive-definite rational repair exists in this frozen tag family, and no factor or soundness shell is authorized. This is a finite algebraic rejection only.

## Generation 37: two-level incidence metric synthesis — killed by a universal parity cut

Only Pro proposals survived cross-review; repaired Proposal 6 was selected as the sole bounded two-level metric test. The frozen family gives orthogonal weights `alpha,beta>=0` to G31 anchor/Walsh blocks, with `72(alpha+beta)=1`, and retains every within/cross-copy residual row. Expected move: a positive margin `delta` above twice a fixed one-copy adverse witness. Falsification: an exact cutting plane `delta<=0`.

`experiments/verify_twolevel_metric_parity_cut.py` emits rational one-/two-copy factors, legal squared radii 1 and 2, and uniform bounds `I/18<=Q<=275416 I`. The one-copy parity has feature costs `(anchor,Walsh,residual^2)=(96,120,0)`, while two compatible copies have `(192,240,0)`. Hence for every metric in the normalized family, their costs satisfy `W_2=2W_1`, yielding the exact universal cut `delta<=0`. At the explicit rational metric `alpha=beta=1/144`, exact costs are `3/2` and `3`; strict two-level growth is impossible. This finitely kills only this orthogonal incidence-orbit family.

## Generation 38: 3-clause splitter bags — finite B+64 pass

Only Pro proposals survived cross-review; Proposal 5 was authorized for the sole bounded falsifier. Its mechanism uses a minimum 12-bag separating family so every clause support of size at most four is isolated somewhere, with selectors only for assignments satisfying all clauses in a bag. Expected move: prevent the G13 affine pseudodistribution from extending through larger overlapping bags. Falsification: control mismatch, exact G13 lift, or any obstruction vector through `B+64`.

`experiments/verify_splitter_clause_bags.py` emits 117 obstruction selectors, 119 control selectors, 12 normalization rows, and 968 complete pairwise marginal rows. The control exact minimum is 119. Eleven obstruction bags contain all four variables. Any nonconstant integer coordinate across those bags contributes at least 10 pairwise residual energy; if all agree, their common legal support is empty and 11 normalizations fail. Hence raw residual square is at least 3, excluding every vector through `117+64=181`. The projected G13 vector costs 6883 and DROP costs 417. This is a finite pass only; no splitter scaling or polynomial gap follows.
