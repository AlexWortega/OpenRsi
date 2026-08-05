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

## Target

Prove a deterministic polynomial-time many-one reduction from 3SAT to Euclidean GapCVP with approximation factor n^c for an explicit absolute c>0, without PCP and without unproved conjectures.
