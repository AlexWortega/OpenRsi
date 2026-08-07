# Notes

## Generation 1 finite result

Only Pro proposals survived cross-review. Proposal 1 was selected because it has a precise algebraic amplifier and the shared slack-cheating objection is directly falsifiable.

For all eight 3-literal sign clauses on `x,y,z`, encode each clause sum `L` by `r=L-1-a-b` with integer slack bits and spread the eight residuals by 64 integer evaluations. Using half-integral anchor cost `(2z-1)^2`, exact search found squared objective 27 versus Boolean baseline 19, not an added nonzero-residual cost of at least 57: a Boolean assignment has one false clause, whose slack pair `(-1,0)` makes its residual zero while adding only 8 anchor units. All residuals then vanish.

The verifier checks 68,921 variable assignments in `[-20,20]^3`, exhaustively optimizes each slack pair over `[-20,20]^2`, and checks all 524,288 Boolean assignments of variables and slack bits to rule out a residual-zero point at baseline 19. Integrality, the box bound, and a polynomial root bound certify the global squared optimum 27. This is finite evidence against this explicit gadget, not an asymptotic theorem.

## Generation 2 finite result

Only Pro proposal 6 survived cross-review. Its causal mechanism is affine/Graver isolation: add sparse measurements so any signed local-pattern selector preserving normalization and marginals requires a long integer kernel move. The expected bounded move was exclusion of every harmful signed selector; falsification was a short move for every candidate matrix.

The exact experiment uses one falsified OR clause at global marginals `(0,0,0)`, seven satisfying-pattern selectors, and five auxiliary columns. It covers every 1–3 row degree-one left-regular `0/1` matrix (up to 531,441 matrices), enumerates selectors in `[-3,3]^7`, and exactly optimizes auxiliaries in `[-3,3]^5`. All 1- and 2-row matrices have squared-norm-2 harmful moves. Eighteen 3-row matrices isolate the tested harmful fiber; the remaining matrices have minimum 2 or 4. Thus the bounded experiment did not falsify the mechanism, but supplies no family, composition, dimension-gap law, or hardness lemma.

## Generation 3 finite result

Both populations survived cross-review, but both reviews made exact unbounded audit of the 18 Generation-2 survivors the mandatory first experiment. Fable proposal 1 was selected because its congruence/left-kernel mechanism directly resolves the box-artifact obstruction. Expected move: certify the harmful affine fiber empty over all integers. Falsification: any rational/integer solution, with a short solution killing the mechanism immediately.

For every survivor and each of its seven legal one-hot references, the verifier constructs the full 7-by-12 affine system. It finds an integral left-kernel certificate `w` with `w^T A=0` while `|w^T b|` is 1, 2, or 3. Independent exact rational elimination also declares all 126 systems inconsistent. Thus no unbounded closest-vector enumeration is needed: the fibers are empty already over `Q`. This validates only the constant local isolation fact; overlap, explicit CVP accounting, sparse-unsatisfaction amplification, and a dimension-gap law remain open.

## Generation 5 finite result

Generation 4 produced no result packet, so Generation 5 executed the overlap audit unanimously required by the new reviews. Pro proposal 1 was selected. Its causal mechanism was private local syndrome rows plus shared marginal equalities; the expected move was retention of local inconsistency under overlap. Falsification was a low-weight signed selector circuit preserving every composed row.

The verifier first checks the canonical 18-survivor hash `41a55873...e49c3`, then covers all ordered survivor pairs, one/two shared-variable choices, relative polarities, and compatible one-hot reference pairs. Across 5,832 systems and 95,256 references, every case has a nonzero integer kernel move of squared norm at most 4. A representative move changes clause-one selectors by `[-1,0,1,1,-1,0,0]`, leaves auxiliaries and clause two fixed, and preserves the selected shared marginal. This kills this private-row overlap mechanism at finite size. It does not establish a general impossibility theorem or any asymptotic result.

## Generation 6 finite result

The constrained quotient calculations are reproducible, but the gate invalidated them as CVP evidence. Normalization and consistency were search filters rather than lattice coordinates, the audit changed references, and the supplied nine-clause instance has an unrestricted mod-2 bypass. The seven unit SNF invariants and 156,880 filtered checks therefore establish no soundness fact for the emitted basis.

## Generation 7 finite counterexample

Only Pro Proposal 5 survived cross-review for a bounded falsification. Its causal mechanism is ordered radix amplification: every nonzero bounded residual should have a leading base-33 digit in each cyclic ordering. The expected move was a distance above the Boolean completeness scale; falsification was an exact residual kernel.

The emitted fixed-target lattice has 72 selector coefficients and dimension 154. Its objective is exactly `||2z-1||^2 + ||Az-b||^2 + ||R(Az-b)||^2`, where the 41 rows of `A` are nine normalizations, nine legality checks, and 23 occurrence-consistency checks, and `R` contains all 41 cyclic base-33 orders. There are no slack, carry, or externally filtered coordinates. A canonical column-HNF hash checks the embedded lattice.

The nine falsification edges cover all 16 assignments, so no Boolean vector reaches squared radius 72. Exact low-weight search finds a zero-residual signed selector at squared distance 80: at global marginals `0000`, clause 0 uses `011 + 100 - 111` and the other clauses are one-hot. Anchor excess is 8 and every raw/radix residual is zero. The anchor bound and a derived Boolean residual digit bound of 7 prove 80 is the exact unrestricted minimum. This is a finite kill of this mutation, not an asymptotic theorem.

## Generation 9 finite result

Only Fable Proposal 1 survived opponent review for implementation. Causal mechanism: a global positive-definite quadratic metric can charge old affine-kernel directions through cross-clause terms. Expected move: exact unsatisfiable distance above `1.1` times a satisfiable control radius. Falsification: failure of positive definiteness/rational realization, or any unrestricted signed vector at or below that threshold.

The fixed template has two shared integer parameters and emits normalization, legality, and every pairwise equality of global degree-one/two moments. Its exact rational factor satisfies `Q=4I+25 A^T A`, hence `lambda_min(Q)>=4`. The satisfiable nine-clause control has exact squared minimum 72. On the obstruction, the former three-term attack has squared distance 305, but exact dynamic programming over all 959 derived local states through anchor excess 24 finds a zero-residual seven-term cube-parity vector. It proves exact squared minimum 96 and finite ratio `sqrt(4/3)>1.1`. The centered eigenvalue bound gives `|z_i|<4` through radius squared 96.

This is a finite pass, not a hardness lemma. The nearest vector already exhibits the known low-degree parity kernel at constant extra cost, so no polynomial gap or arbitrary-overlap law follows.

## Generation 11 finite counterexample

Both opponent reviews selected only degree-raising global moments for a bounded audit. The causal mechanism was that a cubic consistency row should detect the Generation-9 seven-term degree-two parity kernel. The expected move was an obstruction minimum above 96 with control minimum 72; falsification was a cubic-zero constant-anchor selector or failure to raise the minimum.

The fully emitted objective is `||2z-1||^2 + 25||A_{<=3}z-b||^2`, with normalization, legality, and all-pairs squarefree moment consistency through degree three. The inherited clause-3 parity now has residual squared norm 1 and distance squared 121. Exact signed-state DP nevertheless finds anchor excess 24 in clause 1: global triple `(0,2,3)` occurs there only once, so no pairwise cubic row compares its changed top moment. The obstruction and control exact unrestricted squared minima remain 96 and 72. This is a finite kill of the tested mutation, not a statement about growing-degree systems.

Verified by `python3 experiments/verify_degree3_global_psd_metric.py`.

## Generation 12 finite counterexample

The surviving bounded direction was global equal-radius PSD/fingerprint separation. Pro Proposal 6 was selected with the predeclared dimension-9 top-Walsh tag `[-1,1,1,-1,1,-1,-1,1]`, one coordinate per clause. Its causal mechanism makes every honest local one-hot contribute one while a seven-term parity contributes 49. The expected move was obstruction distance squared above the prescribed `4/3` threshold `108` for completeness squared radius `72+9=81`; any unrestricted point through 108 was the falsification condition.

The emitted objective is `||2z-1||^2+25||A_{<=3}z-b||^2+||Fz||^2`. Exact shell DP covers all coefficients through 108 using the derived interval `[-2,3]`, includes normalization and legality costs, and accumulates every all-pairs moment residual. The old cube-parity vector costs 153. A cheaper vector sets all eight selectors of clause 0 to zero and uses compatible one-hot labels elsewhere: anchor 72, one normalization residual costing 25, and fingerprint cost 8, for exact obstruction minimum 105. The control exact minimum is 81, so the finite squared ratio is `35/27<4/3`.

Verified by `python3 experiments/verify_spherical_parity_fingerprint.py`. This kills only the explicit Walsh candidate, not the entire fingerprint or global-PSD population.

## Generation 13 finite compatibility obstruction

The two cross-reviews left only raw-selector Construction-A/expander coding as a bounded conditional survivor, and both required compatibility with all globally consistent encodings before any lattice amplification. The causal mechanism was a maximal linear syndrome annihilating every honest difference while detecting each harmful shell vector. The expected move was a nonzero syndrome for all known attacks; a harmful honest-affine-span collision was the falsification condition.

For each `p` in `{2,3,5,127}`, the 15 differences among the 16 consistent one-hot encodings have rank 14, so their orthogonal complement is the maximal 58-dimensional compatible syndrome space. The G5 representative embeddings, G7 three-term attack, G9 parity, and all 144 simple clause drops have nonzero maximal syndrome in this audit. The Generation-11 unique-triple parity does not: with lexicographic assignments its exact integral affine coefficients are `[1,-1,-1,1,0,0,0,0,-1,1,1,-1,1,0,0,0]`, which sum to one and reconstruct the harmful selector coordinatewise. Hence every linear hash taking all honest encodings to one target also takes this anchor-excess-24 selector to that target, over the integers and every modulus.

Verified by `python3 experiments/verify_selector_code_compatibility.py`. This finite result kills raw linear hashes on these 72 selectors; no claim is made about nonlinear or enlarged encodings.

## Generation 14 finite pair-bag pass

Only Fable Proposal 2 survived. Its causal mechanism replaces each raw clause selector by joint assignment selectors on every clause pair, then enforces bag normalization, both endpoint legality marginals, and canonical-star equality of every full eight-label clause marginal. The expected move was exclusion of all obstruction vectors through the repaired baseline shell `B+32`; a vector in that shell or a control minimum other than `B` was the falsification condition.

There are 36 bags: seven have 8 union assignments and 29 have 16, giving `B=520`. The emitted matrix has 612 rows and objective `||2z-1||^2+25||Az-b||^2`. Through anchor excess 32 at most four bags can be non-Boolean, so every clause retains a Boolean incident bag in the degree-eight complete mesh. Zero residual then propagates one legal one-hot full marginal per clause; exact backtracking finds no globally compatible legal label tuple for the obstruction. If a residual is nonzero within the shell, its cost 25 leaves anchor excess below 8, forcing Boolean coefficients and exactly one residual row; normalization, replicated legality, and one-hot marginal structure each rule out that case. Thus no obstruction vector exists through 552. An honest control vector attains the universal anchor lower bound 520, proving its exact minimum.

The integral G11 affine collision does lift, but its 29 four-variable bags each pay excess 32, for total excess 928. The G7 marginal is nonextendable on seven bags incident to its attacked clause. Every single-bag and single-clause drop from the control lies above 552. Verified by `python3 experiments/verify_pair_bag_lift.py`. This is finite evidence only.

## Generation 15 finite hierarchy counterexample

Both cross-reviews retained only the weighted sparse/laminar hierarchy. Before testing, the mutation was frozen as the deterministic adjacent-pair tree on the nine clauses, with clause leaves followed by 2-, 4-, 8-, and 9-clause nodes. Unscaled leaf/internal anchor weights are `1` and `1/16`, every normalization, leaf-legality, and parent-child full-marginal residual has weight `16`, and `delta=1/2`. Multiplying squared distance by 256 gives an integral factor, baseline `B=18560`, and threshold `T=B+256*9^(3/2)=25472`. The expected move was exclusion of every harmful vector below `T`; a zero-residual affine lift was the primary falsifier.

The emitted instance has 200 unrestricted integral selectors and 210 residual rows. Using the exact Generation-13 coefficients `[1,-1,-1,1,0,0,0,0,-1,1,1,-1,1,0,0,0]`, take the corresponding affine combination of all 16 globally consistent hierarchy encodings. Every node normalization and parent-child marginal is exact, and the leaf marginals reproduce the legal G11 parity selector, so residual energy is zero. Its leaf anchor is 24576 and internal anchor is 384, totaling 24960, or 512 below the threshold. The control exact minimum is `B`; direct single-leaf drops cost at least 149632.

Verified by `python3 experiments/verify_weighted_laminar_hierarchy.py`. This finitely kills only the preregistered hierarchy/weight rule; it is not a general sparse-hierarchy impossibility result.

## Generation 19 finite signed-flow counterexample

Only Fable Proposal 1 survived cross-review. Its causal mechanism compiles the formula into a balanced width-5 permutation branching program: every complete honest path for the obstruction rejects, so the G13 affine combination of complete paths also rejects. Source, ACCEPT sink, conservation, transition edges, and repeated-query totals are all emitted. The expected move was an empty integral ACCEPT fiber; any exact accepting signed flow was the preregistered falsifier.

The deterministic Barrington compiler produces 3,250 layers: 1,300 queried layers and 1,950 constant permutation layers. Constant layers use five edge variables and queried layers ten; four shared query variables give rank 22,754. The emitted objective has 17,555 residual rows and is `||2z-1||^2+25||Az-b||^2`. Exact DP over flow vectors and shared query totals exhausts every integral vector with anchor excess at most 8 and finds none. At excess 16 it reconstructs an exact ACCEPT flow with two coefficients `-1`, all other coefficients Boolean, and every residual zero.

Thus the obstruction exact unrestricted squared minimum is 22,770. Any nonzero integral residual costs at least 25 above the universal anchor baseline, so it cannot beat the signed flow. A matched satisfiable control has an honest accepting path and exact minimum 22,754. Verified by `python3 experiments/verify_barrington_signed_flow.py`. This is a finite kill of the emitted flow encoding only.

## Generation 28 finite recursion-rule failure

Only Pro Proposal 6 survived opponent review for a bounded experiment. Its causal mechanism was exhaustive full-port min-plus composition: if malformed states cannot disappear at a seam, illegal transfer cost might grow faster than legal cost. The expected move was `lambda>mu`; falsification included nonclosure, control mismatch, a cheap DROP/G13/G19 state, or `lambda<=mu`.

The frozen rank-32 obstruction has four eight-coordinate same-variable pair bags, 36 emitted checks, identity as its sole allowed seam permutation, and objective `||2z-1||^2+25||Az-b||^2`. Its eight legality rows forbid all eight assignments. The matched control duplicates forbidden assignment zero in place of seven, leaving assignment seven legal. The anchor block certifies `Q>=4I`; squared radius 57 gives the unrestricted coefficient interval `[-2,3]` because the other 31 anchor squares contribute at least 31.

Exact enumeration gives 20 entries in each depth-one transfer table. The complete depth-two obstruction table through 57 has eight ILLEGAL entries, all cost 57; the control table has one LEGAL entry at 32 and six ILLEGAL entries at 57. A zero-residual obstruction state is impossible because all four ports would agree, all eight coordinates would be forced to zero, and normalization would require sum one. Thus 57 and 32 are exact obstruction/control minima. Depth-one adverse and legal minima are 32 and 16, yielding `lambda=57/32<mu=2`. The partition includes every integral state as LEGAL, ILLEGAL, DROP, G13, G19, or MALFORMED; diagonal DROP, G13, and exact two-negative G19 seeds cost 132, 303, and 221.

Verified by `python3 experiments/verify_frozen_minplus_pair_tile.py`. This is finite evidence that the serialized reduced recursion rule fails its growth test; it is not an asymptotic statement.

## Generation 30 finite tensor-seed isometry

Only Fable Proposal 3 survived opponent review for implementation. Its causal mechanism was literal tensor multiplication: for a frozen integer factor `C`, target `y`, and matched control, unrestricted distances to `C tensor C` and `y tensor y` might improve the NO/YES squared ratio. The expected move was `R_2>R_1`; `R_2<=R_1` or an entangled shortcut was the falsifier.

The frozen G28 depth-one right-tile seeds each have rank 16, ambient dimension 30, factor `C=[2I;5A]`, and target `y=[1;5b]`. The alleged NO forbids assignments `{4,5}` and `{6,7}` in its two bags; the control forbids `{4,5}` and `{6,0}`. Swapping coordinates 0 and 7 in both bags gives exact coefficient and ambient row permutations with `C_YES P=Q C_NO` and `y_YES=Q y_NO`. Their tensor squares therefore pair every unrestricted integral `16x16` matrix by `Z_YES=(P tensor P)Z_NO`. Both one-copy exact minima are 16, and the unrestricted two-copy minima are equal, so `R_1=R_2=1`; their unknown common two-copy minimum is only bounded here between 256 and 1,888.

The first shell containing named diagonal DROP, G13, G19, and rank-two MALFORMED representatives has squared radius 31,285. Since the product singular value is at least 4 and the product target norm is 66, every coefficient in that shell lies in `[-60,60]`; the isometry bijects the complete shells. The named costs are 4,356, 31,285, 11,749, and 4,420. A separate exact search checks all 131,585 coefficient matrices with `l1<=2`; zero is best there at 4,356 for both seeds.

Verified by `python3 experiments/verify_literal_tensor_seed_isometry.py`. This is a finite kill of the serialized G28 depth-one seed pair, not a theorem about arbitrary tensor products.

## Generation 31 finite equal-radius Gram pass

Only Pro Proposal 7 survived opponent review for implementation. Its causal mechanism was equal-radius discrepancy geometry: honest encodings may have different Walsh vectors but identical norm, so the G13 common-syndrome obstruction does not directly apply. The expected move was obstruction squared distance strictly above `4/3` of the exact control radius. Factor/center failure, control mismatch, or any unrestricted vector through the boundary was the falsification condition.

The frozen rank-72 factor has 298 rows and objective `||2z-1||^2+||Fz||^2+100||Az-b||^2`, where `F` is nine block-diagonal copies of `H_8` and `A` contains normalization, legality, and all-pairs squarefree moment checks through degree three. Thus `F^T F=8I` and `Q=12I+100A^T A`; the exact rational center and factor are emitted. Every globally consistent one-hot selector has anchor-plus-Walsh energy 144. A satisfying control witness attains 144, and any lower vector would need zero residual, where normalized/legal integer blocks cost at least 16 each, proving the control exact minimum.

For the obstruction, total cost through 192 permits residual square only zero or one. In the zero branch, normalization and legality reduce each clause to 364 signed states of local cost at most 64; exact moment DP has layer counts `[364,4030,4103,979,153,56,13,3,0]`, so no global state survives. In the residual-one branch, base cost is at most 92. The complete 2,701-vector enumeration—zero, one `1`, one `-1`, or two `1` coordinates—finds minimum residual square 7. Therefore no unrestricted vector exists through 192. The G11/G13 parity has cost 216, so the obstruction minimum is only bounded as `193<=d_NO^2<=216`; the certified finite squared ratio is at least `193/144>4/3`. The clause-drop witness costs 236.

Verified by `python3 experiments/verify_equal_radius_walsh_gram.py`. This finite pass supplies no scalable synthesis, recurrence, or hardness lemma.

## Generation 32 finite cross-copy composition failure

Both proposal populations had a cross-review survivor. Pro Proposal 1 was selected as the most direct bounded test of the missing Generation-31 composition law. Its causal mechanism was cross-copy moment coupling: two obstruction copies share variables 0 and 1, and all degree-at-most-three moment rows span both copies. The expected move was strict superadditivity `d_2^2>2d_1^2` with exact control minimum 288. A control mismatch or any unrestricted vector of cost at most `2d_1^2` was the falsifier.

The verifier first extends the one-copy search through 216. Any malformed local block would cost at least `108+8*16=236`, so every candidate is normalized/legal. There are 959 possible local signed blocks, with costs 16, 40, 64, or 88. Exact all-pairs moment DP has layer counts `[959,2396,891,192,63,26,15,7,1]` and proves the exact one-copy obstruction minimum `d_1^2=216`.

The two-copy rank-144 obstruction uses 18 Walsh blocks, residual scale 10, and 433 checks, including 125 cross-copy moment rows. Through squared radius 432 the derived coefficient interval is `[-4,5]`. The matched control has an honest witness at 288. Below 288, raw residual square is zero or one: zero residual forces 18 normalized/legal blocks of base at least 16; a sole moment residual costs at least 388; and a sole local residual costs at least `17*16+8+100=380`. Thus the control exact minimum is 288.

Take the one-copy G11/G13 parity witness in clause 1 of each copy, using compatible shared values `x_0=x_1=1`. Each parity preserves all proper moments, so every within-copy and cross-copy row is exact. The combined vector has base 432 and zero residual. Therefore `d_2^2<=432=2d_1^2`, falsifying strict superadditivity without needing further shell search.

Verified by `python3 experiments/verify_crosscopy_walsh_composition.py`. This is a finite kill of this coupling rule, not a general composition theorem.

## Generation 33 finite exterior-tag completeness failure

Only Fable proposals survived opponent review. Proposal 6 was selected because a shared exterior block is the only surviving mechanism with genuinely cross-clause Gram terms, but its preregistered first gate was exact equal completeness. The expected move was a common sphere for all 16 globally consistent encodings under a canonical clause-incidence sign rule. Failure of every sign rule to admit a rational center was the immediate falsifier, before any soundness shell.

For local label `t in {0,...,7}`, the verifier freezes `v(t)=(1,t,t^2,t^3)` and the six coordinates of `v(t) wedge v(t+1)` in order `(01,02,03,12,13,23)`. All eight tags are distinct integral decomposable bivectors and satisfy the Plücker relation exactly. For each of the 512 vectors of clause signs in `{-1,+1}^9`, it sums selected tags in one shared six-dimensional block for all 16 global assignments.

A center `c` would need to solve `2(p_i-p_0).c=||p_i||^2-||p_0||^2` for the other 15 honest points. Exact rational rank computation gives `(rank A,rank[A|b])=(4,5)` for every sign rule, for both the satisfiable control and obstruction. Hence neither formula has a cospherical rule. Even the best zero-centered control rule has squared-norm spread 9,340,400 across its honest encodings. The verifier also emits exact left-kernel inconsistency certificates for the all-negative representative.

Verified by `python3 experiments/verify_exterior_bivector_completeness.py`. Since the required completeness sphere fails, no CVP factor/target or attack-shell claim is made. This is a finite kill of this tag/sign family only.

## Generation 34 finite metric-repair infeasibility

Only Fable Proposal 1 survived for implementation, solely as a completeness gate. It retains the Generation-33 bivectors but allows one shared rational symmetric metric `G`, separate control/obstruction centers and radii, `trace(G)=1`, and `G-(1/100)I` positive semidefinite. The expected move was restored equal completeness; exact infeasibility or a singular-only solution was the falsifier.

For one formula and sign rule, let `p_i` be the 16 honest exterior points. Equal `G`-radius with some center is equivalent, after writing `h=Gc`, to requiring the values `p_i^T G p_i` to lie in the column space of `[1,p_i]`. Every affine dependency `alpha` therefore gives the homogeneous exact constraint `sum_i alpha_i p_i^T G p_i=0` on the 21 upper-triangular entries of `G`.

The verifier constructs these constraints separately for control and obstruction and combines them for each of all 512 sign rules. Every combined matrix has rank 10, the same pivot columns and the same exact RREF. That RREF contains the unit row for upper-triangle coordinate `(1,1)`, forcing `G[1,1]=0`. Positive semidefiniteness of `G-(1/100)I` instead forces `G[1,1]>=1/100`, an exact contradiction independent of the trace normalization. This is a facial-reduction/algebraic infeasibility certificate, not a numerical SDP conclusion.

Verified by `python3 experiments/verify_exterior_metric_repair_infeasible.py`. No rational factor, center, or shell is claimed because the preregistered completeness gate fails. This kills only the repaired Generation-33 family.

## Generation 37 finite universal parity cut

Only Pro proposals survived opponent review. The repaired Proposal 6 test was selected because it is the only authorized experiment optimizing the missing two-level adverse-versus-legal margin. The frozen composition uses orthogonal copy-local G31 anchor and Walsh feature blocks plus all within-copy and cross-copy moment residual rows. Its rational family has `alpha,beta>=0`, `72(alpha+beta)=1`, and residual squared weight 100. The expected move was a strict margin `delta>0` above twice a fixed valid one-copy adverse witness; `delta<=0` was the falsifier.

Every satisfying control has squared radius 1 in one copy and 2 in two copies. The family is uniformly positive definite: the coefficient Gram has base eigenvalue `4alpha+8beta>=1/18`; a trace bound gives `Q<=275416 I`. The verifier emits full rational factors for one-/two-copy obstruction and control. The representative point `alpha=beta=1/144` has factor `(1/12)[2I;F]` plus residual block `10A`; its exact control minima are 1 and 2.

The exact G11/G13 one-copy parity has anchor 96, Walsh energy 120, and zero residual, so its family cost is `W_1=96alpha+120beta`. Two compatible parity copies have anchor 192, Walsh energy 240, and every cross-copy residual zero, so `W_2=192alpha+240beta=2W_1`. Therefore any soundness constraint requiring every two-copy NO vector to cost at least `2W_1+delta` immediately yields the exact cutting plane `delta<=0`. At the emitted metric, the one-copy obstruction exact minimum is `3/2` and the two-copy parity costs 3.

Verified by `python3 experiments/verify_twolevel_metric_parity_cut.py`. The negative cut makes a shell search unnecessary for strict growth. This is a finite kill of the frozen orthogonal incidence-orbit metric family, not a global optimum theorem for arbitrary Grams.

## Generation 38 finite splitter-bag pass

Only Pro Proposal 5 survived for implementation. Its causal mechanism was a sparse/dense splitter dichotomy: a family of 3/4-clause bags isolates every nonempty clause support of size at most four, while each bag carries only assignments satisfying all its clauses. The expected bounded move was exclusion of the known affine lift and every unrestricted obstruction vector through `B+64`. Control mismatch, an exact G13 lift, or a shell vector was the falsifier.

A deterministic set-cover MILP over 210 candidate bags and 837 isolation requirements certifies minimum cardinality 12; the emitted lexically refined family consists of 12 triples. Each bag has normalization, and every bag pair has every shared-variable marginal equality. This gives 980 checks. The obstruction has `B=117` legal selectors; the matched control has `B=119` and an honest assignment at its universal anchor lower bound, proving exact control minimum 119.

Eleven obstruction bags contain all four variables. Their pairwise marginal rows are therefore coordinatewise equalities on the 16 global assignments. If any assignment coordinate differs among 11 integral bag vectors, the sum of its all-pairs squared differences is at least 10. Thus raw residual square at most two forces all 11 full distributions to agree. Their common legal support is empty because their clauses collectively forbid every global assignment, so the common vector is zero; then all 11 normalization residuals equal `-1`, another contradiction. Therefore every obstruction vector has raw residual square at least three whenever it could enter the shell. Since `25*3>64`, no unrestricted vector exists through 181. The anchor-derived coefficient interval is `[-3,4]`.

The direct projected G13 affine vector has anchor 333 and raw residual square 262, for total 6883. The all-zero DROP vector costs 417. Verified by `python3 experiments/verify_splitter_clause_bags.py`. This finite pass supplies no logarithmic-size bag family, relative-growth recurrence, or hardness lemma.

## Goal-directed Generation 1 finite counterexample

Both cross-reviews permit only the G19 `k=2` ordered-tuple audit as the first experiment. Fable proposal 1 supplies the adversarial mechanism: test whether the exact two-negative accepting flow closes under the emitted coherence equations. The expected move against FRONTIER was a zero-residual point below `(4/3)^2R_2^2`; the falsifier was any such unrestricted integral point.

The verifier hash-locks and reruns the G19 exact seed search, then emits a rank-224,282 lift with 348,451 rows: ordered transition pairs, both unary marginals, pair/unary source and ACCEPT flow, all conservation rows, complete repeated-query totals and query marginals, plus off-diagonal-zero/diagonal-idempotence rows. The pure product `s tensor s` misses 14 diagonal rows (residual square 20). The stronger signed diagonal embedding `diag(s)` satisfies every row exactly. It has six `-1` coordinates and anchor excess 48, so its squared cost is 224,330. A matched honest control attains the universal anchor lower bound `R_2^2=224282`; hence the witness is below `4R_2^2/3` and `16R_2^2/9` by exact integer comparisons.

This finite result refutes the displayed amplification inequality for this explicit complete linear pair lift. It does not compute the unrestricted `k=2` optimum and does not rule out a differently specified nonlinear/enlarged construction.

Verified by `python3 experiments/verify_k2_barrington_tensor_splice.py`.

## Goal-directed Generation 2 finite counterexample

Only Fable proposals survived. Proposal 3 was selected because opponent review authorized only its complete `A5` depth-two transfer test. The mechanism was nonabelian multiplication/Fourier energy; the expected move was a `33/32` adverse-versus-legal squared-growth certificate for some `1<=a,b<=12`; the falsifier was any unrestricted legal-boundary virtual product below it.

The verifier uses lexicographic `A5`, with the hash-locked G19 ACCEPT cycle at index 16. Three fusion tiles contribute 10,800 unrestricted `(g,h)` selectors and 423 emitted normalization, leaf, COPY/glue, and ACCEPT rows. For the lexicographically first bicyclic element

`x=(1-g)h(1+g)`,

exact convolution gives `x^2=0`, so `u=1+x` and `v=(1-x)ACCEPT` satisfy `uv=ACCEPT`. Two exact signed child couplings have identity leaf marginals and product ports `u,v`; their outer-product root has ACCEPT product. The verifier exhausts all 243 and 2,187 coefficient assignments in `{-1,0,1}` on the two frozen sparse supports and finds each coupling uniquely feasible. All rows vanish. The three selector blocks contain 17 negative coefficients, giving cost `10800+8*17=10936` at `a=1`. A matched honest control with leaves `(e,e,e,ACCEPT)` attains the universal anchor lower bound 10,800.

Thus `32*10936 < 33*10800`; residual scale `b` is irrelevant, and all 144 pairs `1<=a,b<=12` fail. The anchor block proves shell coefficients lie in `[-5,6]` and eliminates recession. This explicit primal attack makes the potential LP unnecessary. No exact NO optimum or general nonabelian impossibility theorem is claimed.

Verified by `python3 experiments/verify_a5_bicyclic_fusion_attack.py`.

## Goal-directed Generation 3 finite family rejection

Only Pro proposals survived cross-review. Repaired proposal 5 was selected because it alone specified a finite `D4` triality experiment after repair. Its mechanism was a symmetric off-block coupling among three 24-cell triality ports; the expected move was an empty equal-legal-radius shell supporting the `65/64` tile gate. Any interior DROP/malformed point was the preregistered falsifier.

The verifier freezes scaled triality classes `8_v,8_s,8_c` in `2D4*`, antipodal Boolean labels, every permutation of classes across two inputs/output, all oriented labels, all eight off-block sign patterns, and every distinct `t=p/q` with `|p|<=16`, `1<=q<=16`. Exact Sylvester tests retain 952 positive-definite Gram parameters. Cross-dot compression covers all 3,072 labelings and 2,924,544 candidates.

The family has a center-independent obstruction. COPY legal points `000` and `111` are antipodes, so their midpoint zero lies in the coefficient lattice. If both have squared radius `R^2`, the midpoint identity places zero at `R^2-||p000-p111||_Q^2/4<R^2`. For NAND, legal `011` and `101` have midpoint `(0,0,output-1)`, also in the lattice and not in the codebook, with the same strict inequality. The minimum exact inward deficits over the complete family are `3/4` for COPY and `17/4` for NAND.

Thus every candidate either lacks an equal-radius center or has a malformed lattice point inside its legal shell. The required outside-shell certificate cannot exist, so factor construction and depth-two tables are not authorized. This is finite evidence for the frozen family only.

Verified by `python3 experiments/verify_d4_triality_midpoint_obstruction.py`.

## Goal-directed Generation 4 finite family rejection

Both cross-reviews authorized only the non-antipodal continuation of the `D4` triality gate. Fable proposal 1 was selected. Its mechanism was removal of the Generation-3 midpoint by using ordered distinct non-antipodal truth pairs; its expected move was an exact empty legal NAND/COPY sphere followed by unrestricted `65/64` transfer growth. A false port on or inside the legal sphere was the falsifier.

The verifier enumerates all six assignments of the three triality classes to ports and all `48^3` ordered non-antipodal pair choices, then combines them with the 952 exact positive-definite Grams. A machine-checked reduction groups 663,552 labelings into 43 interaction signatures, so 40,936 exact tests cover 631,701,504 candidates.

For any center, squared distance on the port cube is a quadratic pseudo-Boolean function with pair terms `A,B,C`. If legal NAND words `001,011,101,110` have common squared radius, the false-word excesses for `000,010,100,111` are

`-A+B+C, -A+B, -A+C, A`.

The verifier proves their minimum is never positive over the complete family. A false Boolean lattice point is strictly inside in 528,417,792 candidates and tied in 103,283,712; the best possible minimum excess is exactly zero. Candidates without a common center already fail completeness, while candidates with one fail soundness. Therefore no Fincke–Pohst or depth-two table is needed. This is finite evidence only.

Verified by `python3 experiments/verify_nonantipodal_d4_nand_obstruction.py`.

## Goal-directed Generation 5 finite family rejection

Both cross-reviews selected only the independent-coupling `D4` mutation. Its causal mechanism was independent control of the three Boolean pair interactions; the expected move was a strictly separated NAND cube followed by an exact empty-shell certificate and then depth-two growth. A malformed point on or inside the shell was the falsifier.

The verifier reuses a machine-checked 43-signature compression of all 663,552 non-antipodal labelings and checks all `15^3=3375` positive-definite Grams, covering 2,239,488,000 candidates. Exactly 24,344,064 candidates have all four false Boolean excesses positive; the best minimum excess is 3, so independent coupling genuinely escapes Generation 4's Boolean identity.

Global emptiness still fails. The legal NAND words `001` and `011` differ only between a non-antipodal pair `b0,b1`, which differs in at least two coordinates. Swap one changed coordinate to form hybrids `h,h'`. Both are malformed points of `2D4*`, and coordinate separability of `K tensor I4` gives, for every center,

`E(a0,h,c1)+E(a0,h',c1)=E(a0,b0,c1)+E(a0,b1,c1)=2R^2`.

Thus at least one hybrid is no farther than the legal radius. The verifier checks all 144 oriented class/pair certificates. No complete CVP enumeration, COPY tile, or transfer table is authorized after this exact intruder. This is finite evidence only.

Verified by `python3 experiments/verify_independent_d4_recombination_obstruction.py`.

## Goal-directed Generation 6 finite family rejection

Only Fable proposals survived cross-review. Repaired proposal 3 was selected because opponent review authorized only its explicit `E6` Gosset-cell NAND classification. The mechanism was an irreducible, already-empty Delaunay shell; the expected move was a bounded integral port map sending every shell vertex to one of four legal NAND words and hitting all four. Any malformed image or nonsurjective classification was the falsifier.

The verifier freezes the `E6` Cartan matrix, generates the 27-weight minuscule Weyl orbit, translates one vertex to zero, and obtains center `(2,1,0,-1,-2,0)/3` and radius squared `4/3`. The exact dual-coordinate bound using `max diag(A^-1)=6` confines every point through the radius to `[-3,3]^6`. Exhaustion of all 117,649 points finds exactly the 27 vertices, all on the shell and none inside.

For port classification, all per-port truth relabelings and legal-base translations give 32 NAND target relations containing zero. A necessary condition for a `3x6` map is that every row take values only in `{0,1}` or `{0,-1}` on all 27 vertices. Complete enumeration of all 729 rows finds only the zero row. Since each NAND port bit varies, no triple of rows is surjective. This rowwise argument covers all `3^18=387,420,489` maps without an unproved symmetry reduction.

Thus the local Delaunay certificate succeeds but the complete port-map gate fails. No COPY, gluing, or transfer-growth claim follows. Verified by `python3 experiments/verify_e6_gosset_port_map_obstruction.py`.

## Goal-directed Generation 7 complete affine classification

Both cross-reviews selected only coefficient-unbounded affine classification of the fixed `E6` shell. The causal mechanism was finite interpolation: seven affinely independent vertices determine every rational affine row. The expected move was either a genuine NAND row triple or a complete no-go for affine ports; a surviving nonconstant triple was the falsifier.

The verifier confirms augmented affine rank seven and deterministically selects basis indices `[0,1,2,3,4,5,10]`. For every one of 128 binary assignments on that basis, it solves the rational `7x7` system and evaluates the row on all 27 vertices. Exactly 126 assignments have an explicit first nonbinary value; their rejection certificates are hashed. The only binary-valued rows are constants 0 and 1.

All eight triples of retained rows have singleton image. None matches any of the 32 translated, signed, and per-port-relabelled NAND relations. Therefore no rational affine port projection of this certified shell realizes NAND, regardless of coefficient size. COPY and transfer remain untested. This exact finite-shell no-go does not cover nonlinear or redundant port encodings.

Verified by `python3 experiments/verify_e6_unbounded_affine_port_no_go.py`.

## Goal-directed Generation 8 exact DROP rejection

Only Fable proposals survived, and opponent review authorized only repaired proposal 3. The mechanism was a `D=8` free rational extended Gram with four canonical legal NAND selectors, four zero-port auxiliaries, entry bound 64, diagonal-dominance margin 1, and legal squared energy 64. The expected move was exact `65/64` separation plus a global tail bound. Any unrestricted false/DROP point below 65 was the falsifier.

The zero coefficient vector is unavoidable. Its linear emitted port is `000`, which is false for NAND, and its energy under `H=[[Q,-h],[-h^T,s]]` is exactly `s`. The family bound gives `s<=64`, whereas `65/64` soundness at legal energy 64 gives `s>=65`. Adding these inequalities yields the exact infeasibility certificate `0>=1`; positive definiteness cannot help.

No Gram, COPY tile, or transfer table is therefore authorized. This is a finite symbolic rejection of the prescribed normalization only, not a theorem against a larger target entry or rescaling.

Verified by `python3 experiments/verify_augmented_gram_drop_obstruction.py`.

## Goal-directed Generation 11 finite grade-zero counterexample

Only Pro proposals survived, and Fable's review authorized only the repaired skew-Rees gate test. The canonical template has eight selectors indexed by Boolean triples over `F_289=F_17[u]/(u^2-3)`, with emitted normalization, three port rows, four forbidden-label rows, and a NAND product-table row. The hoped-for mechanism was adverse associated-graded injectivity; any false-boundary grade-zero affine class was the falsifier.

The four legal NAND columns `001,011,101,110` form a unimodular affine simplex. Exact field elimination and the saturated integer submatrix give a unique integral pseudosection for every false boundary. For example, false `111` is represented by `-001+011+101`; it preserves normalization, every port row, all forbidden rows, and the product row. The false boundaries `010,100,111` each have anchor energy 16 and zero residual.

All coefficients are in the base field `F_17`, so Frobenius fixes the witnesses and a skew grade-one copy does not move them out of grade zero. The minimum trace energy of a nonzero element in the quaternion prime above 17 is at least `2*17=34`, while the witness costs 16. Thus the canonical module fails at depth one. This is finite evidence only.

Verified by `python3 experiments/verify_f289_nand_affine_grade_zero_attack.py`.

## Goal-directed Generation 12 finite local survivor

Both cross-reviews authorized only the redundant binary-signature gate. The causal mechanism was to distribute the four legal NAND codewords across repeated coordinate signatures so their mandatory integral affine false representatives acquire large anchor norm. The required bounded move was exact false-fiber energy at least the independently certified prime trace threshold and normalized ratio above `17/16`; any cheaper signed or DROP point was the falsifier.

The verifier exhausts all 490,314 signature multisets at `N=8`. It machine-checks that binary support saturation is equivalent to containing a unimodular four-signature minor; 403,973 multisets are saturated and 13,457 pass both local inequalities. The best multiset is indexed by `(1,2,6,6,6,6,6,9)`, i.e. `0001,0010`, five copies of `0110`, and `1001`.

For this code, four emitted affine-span rows plus normalization and three port rows form a determinant-one `8x8` matrix. Hence every unrestricted integer boundary fiber is a singleton. Legal codewords have energy 8; false `000,010,100,111` have exact energies `160,64,56,56`.

The threshold is not hardcoded. In the definite algebra `(-3,-17)`, the displayed maximal-order basis is multiplication-closed and has trace discriminant 289. Right multiplication by `j` gives a two-sided prime ideal of index 289. A dual coefficient bound reduces its trace shell to `[-1,1]^4`; exact enumeration gives minimum 34. Therefore the candidate passes `56>=34` and `56/8>17/16`. This finite pass authorizes only COPY/depth-two testing.

Verified by `python3 experiments/verify_redundant_signature_nand_survivor.py`.

## Current Generation 1 synthesis

The selected cross-review survivor is the mutated finite adverse transducer. Its proposed cause is finite-state valuation transfer certified by a potential; its falsifier is any adverse state with zero leading defect or any signed zero-gain seam.

`experiments/verify_redundant_nand_grade_zero_seed.py` reconstructs the natural emitted `8x8` NAND map (determinant one), searches 334,592 signed vectors through squared energy 64, and finds exact zero-residual false fibers `010`, `100`, `111` at energies 64, 56, 56. `experiments/verify_quaternion_copy_diagonal_splice.py` checks all 378 saturated binary-signature COPY multisets of ranks 2–8 and both orientations; each admits the repeated false-`111` selector through legal COPY `11` with zero affine/glue residual and total energy 114–120. These are finite kills of the frozen affine defect/glue only.

`lean/Verify_transducer_potential.lean` compiles a universal finite-walk potential telescope, its bounded-potential corollary, and the fact that gain at least one valuation per four binary levels beats binary scaling for prime 17. No current tile supplies the theorem's certificate or even a nonzero initial defect.

## Current Generation 3 synthesis

The only cross-review survivor after correction is the generic quaternion-product tag. Its local cause is genuine bilinearity rather than another affine checksum: a rectangle has transfer `(a0-a1)*(b0-b1)`. The required move against Q1 is simultaneous separation after pair selectors enlarge the integral kernel; a zero-transfer signed sum is the falsifier.

`experiments/verify_product_tag_enlarged_kernel.py` freezes the smallest `4x2` seam. Its labels detect all six old transportation rectangles and false `111` in both COPY orientations, but exhaustive search of 6,561 signed vectors finds one enlarged-kernel move up to sign with zero row/column margins and exact zero tag over `Z[u]/(u^2-3)`. It has `l1=8`, squared coefficient weight 8, and no proper conformal zero-tag submove.

`experiments/verify_product_tag_rectangle_kernel.py` uses distinct asymmetric labels on an `8x8` table. Exact dependency search finds a two-rectangle movement with centered coefficients `(2,-1)`, zero integer margins, zero transfer modulo 17, squared weight 12, and support 6. Neither coefficient weight is asserted to be Euclidean CVP energy, and the complete tile's extra equations are not present.

`lean/Verify_product_tag_rectangle.lean` proves affine-tag annihilation, noncommutative product factorization, division-ring nonvanishing, and the skew-automorphism variant. `lean/Verify_three_transfer_kernel.lean` proves that any three `F_289` leading symbols, represented in `F_17^2`, have a nonzero linear dependency. The local mechanism is correct, but one coordinate cannot certify an enlarged seam by checking primitives separately.

## Current Generation 4 synthesis

The sole cross-review survivor is the fixed-witness full-matrix lift-or-kill audit. Its cause is linear: if the known pair movement survives all added rows, its zero product transfer persists; the candidate survives this discriminator only if those rows obstruct every extension or force energy at least `17E`.

Because no actual maximal-order product-tagged tile was supplied, `experiments/verify_product_tag_full_lift_attack.py` hash-locks the smallest canonical margin-only completion. It has 18 variables, two `22x18` emitted matrices, and sixteen `40x18` factor/target instances. Legal energy is `E=18`. Exhaustion of 6,561 pair movements per orientation finds the known witness and its negative; shell search of 25,856 selectors through pair energy 32 proves a malformed exact-residual-zero vector of total squared distance 42 in every legal fiber. The witness is conformally primitive and `42<306=17E`.

`experiments/verify_product_tag_full_seam_lift.py` independently serializes a related `36x18` decoded-margin factor and obtains the same 16 energy-42 lifts. These are finite kills of the serialized margin-only completions only; neither script represents an absent maximal-order `O/P^2` fusion tile with additional pair-dependent rows.

`lean/Verify_single_transfer_lift_obstruction.lean` proves that if three integrally independent seam directions survive all non-transfer integer rows, one nonzero integer combination also survives, has zero leading `F_17^2` transfer, coefficients bounded by 8 in magnitude, and squared coefficient weight at most 192. The theorem is universal and compiled, but conditional on the three directions surviving; it supplies no full-tile CVP threshold.

## Current Generation 5 synthesis

The selected mutation is a direct sum of product-transfer channels. On the fixed pair seam its cause is exact dimension: two `F_289` channels have four `F_17` coordinates and can inject the three-dimensional transportation kernel.

`experiments/verify_multichannel_product_shell.py` exhausts 81 one-channel label arrays and finds the first rank-three two-channel pair after 97 ordered candidates. The old witness syndrome changes from `(0,0)` to `(1,0,16,16)`. Across both orientations and all legal cells, the verifier checks 7,152 same-margin selectors below `17E=306`: the old channel has 80 zero-syndrome malformed states with minimum energy 42, while the synthesized two-channel map has none. This is only a finite restricted pair-shell pass.

`experiments/verify_multichannel_physical_flip_attack.py` performs the missing unrestricted low-weight audit on channel prefixes `r=1..4`. The tag rows depend only on the pair block. Holding that block fixed and flipping one of ten physical NAND/COPY selectors leaves every transfer component zero. Across 64 legal fibers and 640 Hamming-one candidates, every fiber has a malformed attack of squared distance 20, with non-transfer residual square 2, below `17E=306`. This finitely kills the four unscaled serialized channel-prefix factors.

`lean/Verify_multichannel_transfer.lean` proves that nonzero componentwise division-ring transport preserves zero/nonzero vector syndromes, an injective syndrome detects nonzero defects, `r` channels have exact `F_17` finrank `2r`, and defect dimension above `2r` forces a nonzero kernel. These are universal conditional facts, not Q1 or a tile construction.

## Current Generation 6 synthesis

The campaign frontier is now L1, structural recognition of a complete full-brick compiler as a marked higher-Lawrence family. The only cross-review survivor is a width-four oblivious Beneš network with formula dependence confined to targets and with physical/anchor columns marked.

`experiments/verify_benes_switch_toric_exchange.py` freezes the smallest standard pair-linearized brick (`54x76`). Exact search over 6,560 nonzero local vectors in `{-1,0,1}^8` finds two signs of one support-eight primitive and no proper conformal summand. The movement preserves every normalization, marginal, routing, glue, and DROP row and satisfies the exact affine identity `h000-h011-h100+h111`. Every one of 384 route/input fibers has a malformed zero-residual representative at energy 92 or 108, versus legal energy 76. This is the breaker result for that serialization.

`experiments/verify_marked_benes_local_audit.py` freezes a larger target-only `136x142` matrix with physical `0/1/DROP`, pair transitions, two NANDs, and transfer auxiliaries. All 384 legal vectors have energy 142; 5,832 physical Hamming-one/two movements are nonkernel. Its residual scale 5 nevertheless fails DROP: the zero vector has exact distance 692, below `17*142=2414`. This is a separate finite kill of that scale and serialization.

`lean/Verify_integral_euclidean_isometry.lean` proves that every square integer matrix with Gram identity is a signed permutation matrix. Therefore arbitrary unimodular equivalence cannot silently preserve Euclidean norms or selector marking. The result is universal but does not establish a Beneš compiler, marked L1, or primitive soundness.

## Current Generation 7 synthesis

The selected quadratic-character orbit genuinely detects the Generation-6 mixed rectangle: its mixed derivative is `(0,0,0,-2)`, all four honest words have squared norm 4, and swapping wires permutes the two linear-character coordinates.

`experiments/verify_quadratic_character_ghost.py` shows why this is insufficient. Among 81 signed selectors, 12 malformed selectors are normalized, and three support-three selectors map to non-honest words on the same sphere. The representative `(-1,1,1,0)` maps to `(1,-1,-1,1)`, with mark norm 4 and anchor energy 12. For every tested mark scale 0–64, the normalization scale is chosen minimally so zero/DROP reaches at least `17E`; the ghost remains below `17E`. This is the breaker result for the local objective.

`experiments/verify_quadratic_character_copy_cycle.py` freezes a `74x44` brick with a straight/swap/swap three-COPY cycle, physical and pair selectors, all four transported characters, NAND, output, transfer, normalization, glue, and DROP rows. Complete `3^12` search finds one synchronized support-12 primitive up to sign and no proper conformal kernel summand. Its malformed energy is exactly the legal value 885 in every honest fiber, while DROP is 120,000 and the adverse threshold 15,045. Thus this fuller finite realization also fails.

`lean/Verify_quadratic_character_switch.lean` proves common radius, exact mixed derivative, integer linear independence of the honest words, and marked wire swap. These universal local facts coexist with the finite ghosts because the ghosts have nonzero images of equal norm rather than zero linear image.

## Current Generation 8 synthesis

The frontier is U0, a structural exclusion from fixed-block `n`-fold, generalized `n`-fold, tree-fold, and two-stage forms. The selected finite mechanism uses marked support separators and graph minors; it makes no soundness or gap claim.

`experiments/verify_gen8_affine_detector_separator.py` freezes square 3-regular bipartite detector matrices from three affine matchings. For `S=8,16,32`, independent HiGHS and CBC MILPs certify exact top-level `2/3`-balanced separator optima `4,6,9`. Each is at least `S/4`, and one-subdivision equality expansions contract back exactly. Sparse signed search checks 654,384 vectors modulo global sign and records image energy at least support. This is finite evidence for a surrogate layer, not the actual U1 serializer or a hereditary recursive profile.

`experiments/verify_gen8_separator_kernel_degeneracy.py` tests a different synthetic cumulative family. Its displayed support contains `K_{4,4}`, `K_{8,8}`, and `K_{16,16}`, yet each matrix has a support-two kernel move, adjacent support-three moves, and a unimodular row rebasing to tree incidence. This does not refute the affine surrogate, but it demonstrates that support witnesses alone do not certify signed soundness and may depend strongly on equation basis.

`lean/Verify_support_minor_channel.lean` proves that the support of `C` is induced inside and is a minor of the support of `[I|-C]`, identity columns are leaves, and an equality expansion with onto collapse, connected fibers, and edge lifts gives an explicit minor model. No growing treewidth or fixed-class closure theorem is proved.


## Current Generation 9 U0 invariant counterexamples and reroute

`experiments/verify_gen8_neighborhood_diversity_nfold_counterexample.py`
freezes the literal standard n-fold matrix from the fixed blocks `A=B=[1]`.
For `n=8,16,32`, its color-aware twin-class counts are `17,33,65`; after
systematic identity augmentation `[I|-C]` they are `26,50,98`.  Both support
graphs are certified trees with exact treewidth one.  The augmentation has an
exact size-one `2/3`-balanced separator, and its one-subdivision contracts
faithfully.  Thus growing ordinary marked neighborhood diversity is not a
fixed n-fold exclusion invariant.

`lean/Verify_two_stage_neighborhood_counterexample.lean` proves for all `n`
that the fixed two-stage matrix with one common column and one private column
per scenario (`A=B=[1]`) has pairwise distinct open neighborhoods for all
scenario rows.  This is the universal version of the class-side failure.

`experiments/verify_u0_fixed_nfold_support_counterexample.py` verifies a
basis-dependence counterexample at `n=8,16,32`.  Premultiplying the same
literal fixed n-fold matrix by the lower-cumulative unimodular matrix gives
complete-bipartite displayed supports `K_{9,8}`, `K_{17,16}`, `K_{33,32}`
with exact balanced separators `6,11,22`.  The explicit bidiagonal difference
matrix is a two-sided inverse and returns the fixed n-fold presentation.

The universal systematic-form statement is in
`lean/Verify_row_rebasing_support_failure.lean`: cumulative `[I|-C_n]`
contains an explicit `K_{m,m}` for `n=2m`, but integral first differences turn
it into `[B|-I]` with `B` lower bidiagonal and every row supported on at most
three columns; prefix sums invert the operation.  The semantic step is
formalized independently by `lean/Verify_row_rebasing_kernel.lean`, which
proves exact equality of integer kernels under any integral left rebase with
an integral left inverse.

These facts do not refute a future precisely stated nonmembership theorem for
an actual universal-circuit factor.  They do refute the former U0's suggested
raw invariants as sufficient general criteria and show that its claimed
direct-algorithm exclusion ignored row preprocessing.  The roadmap therefore
retires former U0 and moves the frontier to U0a: emit the actual factor,
marks, uniform class quantifiers, and equality grammar.  U0b must subsequently
use a row-basis-invariant column-matroid profile and prove a separate bound for
each of the four named classes.


## Current Generation 10 finite serializer, affine ghost, and right-basis obstruction

The finite serializer `experiments/verify_u0a_universal_topology_serializer.py`
emits canonical sparse COO matrices at widths 8, 16 and 32.  Its schema is
`u0a-butterfly-nand-copy-factor-v1`.  Source selectors support FREE/FIX0/FIX1;
gate selectors support COPY_A/COPY_B/NAND/ZERO/ONE.  Fixed butterfly offsets
supply fanout and two-step diamonds.  Rows include normalization, program,
edge consistency, redundant dyadic edge sums, outputs, and one physical
identity coordinate for every selector.  Complete artifacts live under
`experiments/artifacts/u0a_universal_topology_w*.json` and reserialize byte for
byte under the three hashes recorded in STATUS.  Honest program checks use
the actual `C,D`, not a constraint surrogate. `experiments/verify_u0a_frozen_depth_obstruction.py` separately checks that each DAG edge advances exactly one stage and that chains one gate longer than `8,10,12` admit zero stage injections. Thus these factors are not yet universal at their frozen sizes.

`experiments/verify_u0a_serialized_gate_kernel_cheat.py` audits the local
COPY_A rectangle on those artifacts.  The movement `(+1,-1,-1,+1)` is zero on
every nonphysical row.  The identity block maps it to itself, so zero-cost
kernel cheating is contained.  On an honest program, cancellation of one base
selector leaves coefficients `[1,0,-1,1]` and raises squared energy by exactly
two.  The finite energy table is `(72,74),(176,178),(416,418)`.  Later
detectors might charge this localized defect, so no soundness kill is claimed.

`U0_GRAMMARS.md` fixes version-1 numerical and semantic conventions.  Class
templates and finite colors are chosen before `S,F`; IDs are not colors;
auxiliary equality gadgets need integer forward/inverse maps and exact
objective preservation.  The displayed y-objective makes both left equation
rebasing and right lattice-basis changes semantically free.

`lean/Verify_column_matroid_grammar.lean` proves integral dependency and
support-minimal circuit invariance under left row rebasing and column
permutations.  `lean/Verify_right_unimodular_lattice_image.lean` proves the
stronger semantic fact for right basis changes: if `QP=I`, `C` and `CQ` have
identical integer images, pointwise attainability, and attainable values for
any output-only cost.  Exact verifier
`verify_right_unimodular_column_matroid_failure.py` shows that their systematic
column matroids can nonetheless be nonisomorphic already in dimension two.
`verify_u0b_right_basis_circuit_failure.py` supplies growing same-lattice
fundamental circuits at the frozen control sizes.  Hence the U0b invariant
must be intrinsic to the embedded lattice and ambient objective, not to a
chosen basis.


## Current Generation 11 parameterized depth, routing, and formula compilation

`verify_u0a_parameterized_depth_chain.py` imports the actual generator with an
explicit depth argument.  For each audited `(w,d)`, it checks the physical
selector identity submatrix, formulas `k=4w+20wd` and
`m=30wd+9w-2d`, exact `D` dimensions, a FREE-input repeated-NAND program with
fixed all-one output target, and the opposite input's output residual.
`Verify_u0a_serializer_dimensions.lean` proves the count formulas and
quadratic bounds for all natural parameters and isolates the exact chain depth
condition.

The default offset schedule is not by itself a universal router.  Exhaustive
small-width DP proves the width-8 default reaches 18,688 permutations.  A
ninth stage reaches all 40,320, and two full cycles also realize every
permutation at widths 4 and 8.  All 25 two-lane mode pairs were checked; an
overall coordinate permutation can only use local identity/swap pairs.

`verify_u0a_butterfly_formula_compiler.py` is the first formula-level audit.
For each formula it deterministically allocates one source per variable,
duplicates repeated leaves, routes tokens by hypercube-edge swaps, evaluates
postorder NAND gates, pads to the width-dependent budget, and cleans every
unused output to ZERO.  Targets therefore depend on the formula/program but
not on the chosen assignment.  Across the finite family, satisfying witnesses
have only physical selector energy; a false root adds exactly one output
residual.  This establishes finite completeness/evaluation, while unrestricted
integer soundness, the universal compiler proof, and a gap remain open.


## Current Generation 12 semantic compiler and canonical manifest

`Verify_nand_formula_compiler.lean` gives the first universal correctness
result about formula compilation itself.  Its stack theorem is strengthened
to arbitrary preexisting stacks, making NAND induction compositional.  The
fixed assertion structure stores only formula code and the desired root bit.
The compile-length theorem establishes linear semantic code size.  No claim is
made that the Python lane trace implements this code for all formulas.

`verify_u0a_canonical_serialize_manifest.py` specifies ASCII canonical JSON and
a versioned manifest.  Formula bytes, program, target and factor components
are separately hashed.  Re-emission is byte-identical, while assignment
execution does not mutate the manifest.  IDs and target dependency roles are
explicit.  Finite count checks through S=4096 support, but do not prove, the
polynomial contract.

`verify_u0a_butterfly_formula_compiler_exhaustive8.py` quotients variable names
by restricted-growth equality patterns and combines all Bell patterns with all
Catalan ordered shapes through eight leaves.  Its 1,901,166 cases independently
mirror token placement and packed truth semantics; actual code is run on each
worst-stage witness.  The maximum raw stage count at eight leaves is 77 versus
budget 294.

The deep-tree recursion warning is repaired in
`verify_u0a_butterfly_deep_formula_iterative_repair.py`.  Traversal, semantic
evaluation, canonical v1 encoding/decoding, and dry scheduling are iterative.
At recursion limit 50 the verifier fully materializes a 61-leaf width-64
program and dry-schedules the former 1,101-leaf blocker at width 2,048.  The
latter would have about two billion padded mode entries, so its manifest stores
counts and a streaming trace hash but explicitly omits modes, `C,D,target_y`.
Thus actual factor streaming and its universal correctness proof remain open.


## Current Generation 13 iterative repair and fresh-register trace

The repaired front end uses explicit work/result stacks and a strict iterative
canonical parser.  `compile_formula_dry_run` follows the same deterministic
lane/token decisions while storing only live placement, counters and a framed
SHA-256 transcript.  On the old 1,101-leaf witness it records raw stage count
43,485, padding 947,768 and total depth 991,254 at width 2,048.

`Verify_nand_register_compiler.lean` proves an abstract SSA bridge.  Its exact
destination trace is the consecutive register interval; every instruction has
one fresh destination, generated operands are older, outside registers remain
unchanged, and the root register equals formula evaluation.  Fresh COPY and
NAND preserve older operands.  No physical lane map is formalized.

The eager resource verifier distinguishes mathematical size from implementation
space.  Complete S=4 output succeeds.  Under a declared 256 MiB address-space
cap, S=16 dry run succeeds but eager complete output raises `MemoryError`.
This host-observable failure motivates streaming COO/target emission and is not
an asymptotic obstruction.


## Current Generation 14 canonical sparse streaming

The streaming emitter preserves the eager canonical order, rather than merely
representing an extensionally equal matrix.  It emits identity D entries before
negative-C entries in each row and hashes the same JSON component objects.
Small eager equality covers metadata as well as triples and target.

`Verify_sparse_coo_stream.lean` formalizes the semantic reason streaming is
safe: every record contributes `coeff*x[col]` to its selected row, and foldl
updates sum to the same row dot product as dense materialization.  COO duplicate
coordinates are added, not overwritten.

The WAIT trace repair captures physical dimension before appending a stage.
The remaining S=128 failure occurs earlier: `compile_formula` materializes all
width-by-depth mode entries even for `(x0 NAND x1)`.  A sparse program record
must define default COPY_A stages, event overrides, padding count and cleanup
without expanding 3,213,056 cells.


## Current Generation 15 sparse program overrides

A canonical raw override is keyed by physical stage and lane and never stores
COPY_A.  Keys are strictly increasing.  WAIT and padding stages therefore need
no entries.  Cleanup is structurally distinct: its default is ZERO and only
the formula root lane overrides to COPY_A.  This boundary convention is tested
explicitly to avoid an off-by-one target error.

The sparse target iterator emits one-hot SOURCE_PROGRAM and GATE_PROGRAM rows
without row metadata or a dense mode map.  Small eager targets match entry by
entry.  Width-256 hashing demonstrates constant program-grid storage under the
declared cap, but full C/D output at that size is not claimed.

`Verify_sparse_program_overrides.lean` formalizes first-match lookup, dense-list
equivalence, sorted key uniqueness and one-hot row targets.  The Python stream
uses unique sorted keys, so first/last-match ambiguity is excluded by the
verified representation invariant.

## Honest butterfly lane semantics

`Verify_butterfly_lane_semantics.lean` closes the generic physical-stage part of the missing bridge. A gate cell reads A from its own lane and B from an involutive neighbor. The five modes have exactly the manifest truth table. XOR by the stage offset is proved involutive. Under the scheduler's local adjacency conditions, two endpoint COPY_B modes implement SWAP, a destination COPY_B implements DUPLICATE while preserving all other lanes, and NAND at the output plus ZERO at the consumed neighbor implements the gate-and-free operation. All-COPY_A WAIT/padding stages are identity; cleanup preserves the root and zeroes every other lane.

Scheduled physical stages and abstract lane events are defined separately, and a list induction proves exact equality after every finite valid trace. Since equality holds on the whole lane state, it also covers unoccupied physical junk more strongly than a live-token-only invariant would. Still open is the compiler-specific theorem that every event emitted by the iterative sparse Python scheduler satisfies these hypotheses and corresponds to the SSA/token trace. The theorem concerns honest `Bool` semantics only and says nothing about factor energy or unrestricted integer soundness.


## Current Generation 16 butterfly lane and matrix trace bridge

The Lean lane model uses unbounded natural lane names and XOR neighbors;
power-of-two range closure remains a serializer obligation.  Event validity
requires endpoint distinctness and the exact directed neighbor equation.  XOR
involution supplies the reverse endpoint needed for SWAP.  Trace induction is
extensional equality of every Boolean lane, stronger than tracking only live
tokens.

The matrix-trace verifier groups canonical COO records one row at a time.  For
selected z support it computes C moments and checks D's identity and negative-C
entries exactly.  Physical coordinates account for the node-count baseline;
only a false asserted root adds one.  The breaker constructs numerical C rows
independently, preventing common-code agreement from hiding an orientation
bug.


## Current Generation 17 smart events and token certificates

A smart XorEvent stores dimension d and one endpoint.  The opposite endpoint
is defined as lane XOR `2^d`; Lean proves distinctness and involution, so local
validity is constructional.  WAIT and cleanup retain a dimension only to use
the same scheduled-stage interface.

The finite certificate contains canonical leaf/gate tables, initial/final token
maps and one record per raw stage.  The checker validates the tree before
replay, ensuring every nonroot token is consumed once.  Selected-column checks
are derived from the round-tripped certificate, not compiler objects.

Full snapshots are diagnostic but not scalable.  At 1,025 leaves the capped
process fails while 129 leaves succeeds.  A delta record already contains the
information needed to update a verifier-owned map, so before/after snapshots
should be removed or sparsely checkpointed.


## Current Generation 18 snapshot-free delta replay

Certificate v2 keeps initial and final token maps but removes all intermediate
maps.  The checker owns the current state and updates it from WAIT/SWAP/
DUPLICATE/NAND records.  Checkpoints contain only a domain-separated,
length-framed SHA-256 digest of the canonical sorted map.

`Verify_event_delta_replay.lean` models a delta as ordered token assignments;
later writes win, although the Python schema uses unique event-local changes.
The theorem checks local equality at the reached replay state, preventing a
producer from validating deltas against fabricated snapshots.  Final-map and
pointwise token corollaries follow.


## Current Generation 19 concrete event deltas

A v3 Change has a token and optional new lane.  Null deletes; a non-null value
moves an existing token or creates a fresh one.  Event-local token names are
unique, so the canonical NAND delete-left/delete-right/create-output order is
unambiguous.  SWAP lists only occupied endpoints; compiler routing forbids an
empty-empty SWAP even though its Boolean lane action would be identity.

`Verify_concrete_event_deltas.lean` quantifies exact endpoint occupants, not
merely lane nonemptiness.  This supplies the uniqueness facts needed to prove
short updates equal global logical token-map functions.  Trace validity is
checked at the replay state, so no producer snapshot is trusted.


## Current Generation 20 finite-width and live-token invariants

`xor_dimension_lt_width` uses Mathlib's `Nat.xor_lt_two_pow`; making dimension
`Fin k` carries the legal-dimension proof.  The resulting neighbor on
`Fin (2^k)` is involutive and never fixes a lane, so all smart endpoint pairs
are distinct and in range.

OccupancyInjective states that two tokens in one live lane are equal.  Valid
SWAP is a lane permutation; DUPLICATE writes a fresh token into a free lane;
NAND erases two distinct children and writes a fresh output into the freed left
lane.  Lean proves preservation and count changes exactly.

The power-boundary breaker uses explicit v3 deltas and independent lane->token
and token->lane maps.  Its largest child is close to the declared 512 MiB cap,
so the result is deliberately finite and resource-scoped.

## Target

Prove a deterministic polynomial-time many-one reduction from 3SAT to Euclidean GapCVP with approximation factor n^c for an explicit absolute c>0, without PCP and without unproved conjectures.
