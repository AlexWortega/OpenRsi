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

## Goal-directed Generation 12: redundant-signature NAND code — finite local survivor

Both reviews selected only proposal 1: replace the canonical selector module by redundant binary codewords. The experiment exhausts the smallest authorized rank `N=8`; causal mechanism: signature multiplicities can raise every unavoidable affine false representative while preserving binary legal energy. Expected move: a saturated decoder with all exact false minima at least the independently derived prime threshold 34 and ratio above `17/16`. Falsification: any DROP or signed false fiber below either gate.

`experiments/verify_redundant_signature_nand_survivor.py` checks all 490,314 length-eight signature multisets; 403,973 are saturated and 13,457 pass the local thresholds. The best code uses signatures `0001,0010,0110` five times, and `1001`. Its complete emitted `8x8` matrix has determinant one, legal energy 8, and exact false energies `(160,64,56,56)`. Separately, the verifier constructs a maximal order in `(-3,-17)`, its two-sided prime of index 289, and certifies minimum nonzero trace energy 34. Thus `56>=34` and `56/8>17/16`. This is only a finite depth-one NAND survivor; COPY and recursive filtration remain open.

## Goal-directed Generation 11: canonical F289 NAND module — finite grade-zero kill

Only Pro proposal 1 survived cross-review. The repaired experiment froze a canonical eight-selector NAND module over `F_289`, with complete normalization, port, forbidden-label, and product-table rows. Causal mechanism: associated-graded exactness at the quaternion prime might force every false boundary into positive filtration. Expected move: eliminate every grade-zero false affine class before lifting to the maximal order. Falsification: any false-boundary class with zero defect and subthreshold energy.

`experiments/verify_f289_nand_affine_grade_zero_attack.py` exhausts all four false boundaries. The legal NAND columns form a unimodular affine simplex, so each false word has a unique integral signed pseudosection using only legal selectors. Three witnesses have anchor energy 16, zero residual, and one negative coefficient. Their coefficients lie in `F_17`, hence are Frobenius-fixed and remain grade zero in the skew grade-one copy. Since a nonzero element of the prime above 17 has trace energy at least 34, `16<34` kills adverse graded injectivity at depth one. No maximal-order lift or depth-two table is authorized. This kills only the canonical template.

## Goal-directed Generation 8: bounded augmented Gram — exact DROP rejection

Only repaired Fable proposal 3 survived. Its causal mechanism was joint synthesis of a free extended Gram for canonical one-hot NAND/COPY selectors, with strict diagonal dominance providing a global tail bound. The frozen normalization required legal squared energy 64, every extended-Gram entry bounded by 64, and adverse ratio at least `65/64`. Falsification included any unrestricted DROP at or below legal cost.

`experiments/verify_augmented_gram_drop_obstruction.py` observes that the unrestricted coefficient vector zero has emitted port `000`, false for NAND, and exact energy equal to the bottom-right Gram entry `s`. The entry bound gives `s<=64`, while soundness requires `s>=65`; the exact certificate is `0>=1`. Thus the Gram search is empty before enumeration, and COPY/transfer tests are not authorized. This rejects only the frozen scale/bound combination, not rescaled augmented tiles.

## Goal-directed Generation 7: coefficient-unbounded E6 affine ports — complete finite-shell no-go

Both populations survived only through proposal 1: remove the coefficient bound from affine port maps on the certified `E6` shell. Causal mechanism: seven affine-basis values determine every rational affine row, making unbounded classification finite. Expected move: find a nonconstant binary row triple realizing NAND, or close the entire affine-port branch. Falsification of the no-go was any surviving NAND triple.

`experiments/verify_e6_unbounded_affine_port_no_go.py` certifies affine rank six, chooses seven independent vertices, and exactly solves all `2^7=128` binary assignments. Of these, 126 rows take a nonbinary value on another shell vertex; the only survivors are constants zero and one. Their eight triples have singleton images and match none of the 32 translated/relabelled NAND relations. Thus no rational affine projection of this fixed shell realizes NAND. This is a complete statement for a finite shell, not a general Voronoi or hardness theorem; nonlinear/redundant ports remain open.

## Goal-directed Generation 6: E6 Gosset-cell port map — finite family rejection

Only Fable proposals survived; repaired proposal 3 was the sole authorized bounded test. Causal mechanism: start from the irreducible 27-vertex `E6` Gosset Delaunay cell, whose empty sphere avoids product-coordinate hybrids, and project every shell vertex to a legal NAND word. Expected move: an exact empty shell plus a complete four-word port classification. Falsification: any malformed shell image or failure to realize all legal words.

`experiments/verify_e6_gosset_port_map_obstruction.py` constructs the minuscule Weyl orbit in an explicit `E6` root basis and proves that its 27 vertices are exactly all lattice points at distance squared at most `4/3` from the rational center. It then covers all `3^18=387,420,489` integral `3x6` maps with entries in `{-1,0,1}` by exhaustive enumeration of their 729 possible rows. Any legal map row must take only `{0,1}` or `{0,-1}` on the shell; the zero row is the sole such row, so no map reaches all four NAND words. COPY and transfer tables are not authorized. This rejects only the prescribed map family.

## Goal-directed Generation 5: independent-coupling D4 grid — finite family rejection

Both reviews selected only proposal 1 from each population: replace the common coupling by `Q=K(x,y,z) tensor I4`, with independent `x,y,z in {-7/16,...,7/16}`. Causal mechanism: independent Boolean pair interactions can make all four false NAND excesses positive. Expected move: retain a strict Boolean candidate, then certify an empty all-lattice shell before COPY and `65/64` transfers. Falsification: any malformed lattice point on or inside a surviving shell.

`experiments/verify_independent_d4_recombination_obstruction.py` checks 2,239,488,000 candidates through 145,125 exact signature/Gram tests. It finds 24,344,064 strict Boolean survivors, with best minimum false excess 3. All still fail: `K tensor I4` makes energy coordinate-separable. Recombining one changed coordinate between legal `001` and `011` produces two malformed `2D4*` labels whose energies sum to `2R^2`; at least one is on or inside the legal radius. The verifier checks this for all 144 class/pair certificates. COPY and transfer tables are not authorized. This kills only the frozen independent grid.

## Goal-directed Generation 4: non-antipodal D4 completion — finite family rejection

Both populations survived only through the same non-antipodal `D4` mutation; Fable proposal 1 was selected because both reviews prescribed it exactly. Causal mechanism: replacing antipodal truth labels by ordered distinct non-antipodal pairs might remove integral midpoints and permit an empty NAND/COPY Delaunay shell. Expected move: pass exact common-sphere/outside-point certification before depth-two `65/64` transfer testing. Falsification: any false Boolean or malformed lattice point on or inside the legal shell.

`experiments/verify_nonantipodal_d4_nand_obstruction.py` covers all six class assignments, 48 ordered non-antipodal pairs per port, and the same 952 positive-definite Grams: 631,701,504 candidates, compressed exactly to 40,936 signature/Gram tests. Restricting squared distance to the Boolean cube gives pair interactions `A,B,C`; equal legal NAND costs force false-port excesses `-A+B+C,-A+B,-A+C,A`. Every candidate has a nonpositive excess. In 528,417,792 cases a false point is strictly inside; in 103,283,712 it ties. COPY and transfer construction are therefore not authorized. This rejects only the prescribed grid.

## Goal-directed Generation 3: D4 triality tile — finite family rejection

Only Pro proposals survived; repaired Pro proposal 5 was the sole conditional survivor. Causal mechanism: assign NAND/COPY ports to the three `D4` 24-cell triality classes and use a symmetric nonorthogonal Gram `Q=I+tS` to separate false transfers by Voronoi geometry. Expected move: an equal-legal-radius empty shell with exact outside-state coercivity and eventual `65/64` growth. Falsification: DROP, parity, malformed ports, control mismatch, or an uncertifiable outside state.

`experiments/verify_d4_triality_midpoint_obstruction.py` exactly audits 2,924,544 retained positive-definite candidates: all class assignments, antipodal truth labels, eight symmetric sign orbits, and reduced `t=p/q` with `|p|<=16`, `q<=16`. Every COPY legal pair is antipodal, so zero is an allowed malformed midpoint strictly inside any common shell. Likewise, the midpoint of legal NAND states `011` and `101` is `(0,0,output-1)` and lies strictly inside. Minimum exact inward deficits are `3/4` and `17/4`. No factor or transfer table is authorized. This rejects only the declared triality family.

## Goal-directed Generation 2: A5 convolution tile — finite counterexample

Only Fable proposals survived cross-review; proposal 3 was the sole authorized bounded construction. Causal mechanism: complete nonabelian multiplication ports and group-algebra energy might make a virtual ACCEPT product grow by at least `33/32`. Expected move: strict depth-two adverse growth for some `C=[aI;bA]`, `1<=a,b<=12`. Falsification: a legal-boundary unrestricted integral fusion below that ratio, a control mismatch, or an isometry.

`experiments/verify_a5_bicyclic_fusion_attack.py` emits three 3,600-selector `A5` tiles with all normalizations, leaf ports, product-to-parent COPY rows, and the G19 ACCEPT product. A bicyclic zero divisor `x` with `x^2=0` gives units `u=1+x` and `v=(1-x)ACCEPT`. Exact signed couplings fuse four identity leaves to ACCEPT with zero residual, squared cost `10936a^2`, versus exact honest-control radius `10800a^2`. Since `32*10936 < 33*10800`, all 144 tested factors fail before a potential LP can certify growth. This kills only this frozen tile.

## Goal-directed Generation 1: ordered-pair Barrington lift — finite counterexample

Only Fable/Pro survivors were eligible; Fable proposal 1 was selected because both reviews made the hash-locked G19 splice the mandatory first audit. Causal mechanism: a signed flow may close under layerwise moments; expected frontier move: find a zero-residual integral `k=2` accepting flow below `(4/3)^2 R_2^2`, or identify the first coherence row that blocks it. Falsification of the amplification claim is any such vector.

`experiments/verify_k2_barrington_tensor_splice.py` emits rank 224,282 pair-flow, unary-marginal, complete query, source/conservation/ACCEPT, and strong diagonal rows. The pure tensor fails 14 diagonal rows, but the linear diagonal embedding of the exact two-negative G19 flow satisfies all 348,451 rows. Its squared cost is 224,330 versus exact control radius squared 224,282, below both `4R_2^2/3` and the actual frontier threshold `16R_2^2/9`. This is a finite counterexample to this explicit lift, not an exact `k=2` optimum or a general impossibility theorem.

## Generation 38: 3-clause splitter bags — finite B+64 pass

Only Pro proposals survived cross-review; Proposal 5 was authorized for the sole bounded falsifier. Its mechanism uses a minimum 12-bag separating family so every clause support of size at most four is isolated somewhere, with selectors only for assignments satisfying all clauses in a bag. Expected move: prevent the G13 affine pseudodistribution from extending through larger overlapping bags. Falsification: control mismatch, exact G13 lift, or any obstruction vector through `B+64`.

`experiments/verify_splitter_clause_bags.py` emits 117 obstruction selectors, 119 control selectors, 12 normalization rows, and 968 complete pairwise marginal rows. The control exact minimum is 119. Eleven obstruction bags contain all four variables. Any nonconstant integer coordinate across those bags contributes at least 10 pairwise residual energy; if all agree, their common legal support is empty and 11 normalizations fail. Hence raw residual square is at least 3, excluding every vector through `117+64=181`. The projected G13 vector costs 6883 and DROP costs 417. This is a finite pass only; no splitter scaling or polynomial gap follows.
