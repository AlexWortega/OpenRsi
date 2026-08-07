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

## Current Generation 1: adverse transducer — affine realization killed, conditional lemma proved

Both opponent reviews retain only the mutated finite adverse-transducer route (Pro 2 / Fable 1). Causal mechanism: a complete lift-independent residue transition table plus an integer potential should force average valuation gain. Expected frontier move: turn Q2 into finite transition data followed by formal telescoping. Falsification: a zero leading class, a carry-dependent successor, or a zero-gain signed splice.

Two exact finite falsifiers occur before transition construction. The natural determinant-one NAND residual map has false `010`, `100`, and `111` fibers with exact zero residual at energies 64, 56, and 56. Every saturated binary-signature affine COPY code of ranks 2–8 also permits `false111-COPY11-false111` with zero affine and glue residual, at energy 114–120. This kills only the explicit affine-only realization.

`lean/Verify_transducer_potential.lean` separately proves the universal telescope and bounded-potential implications, plus the exact `17>2^4` threshold. It is a conditional proof tool, not an instantiated Q2 certificate. A next candidate must emit a new quaternionic transfer coordinate nonzero on the displayed `111` selector and survive complete `P^2/P^3`, DROP, carry, and internal-kernel enumeration.

## Current Generation 3: one product tag — enlarged rectangle kernel survives

Both reviews select only the corrected generic product-tag route (Fable 1 / Pro 2). Causal mechanism: on one rectangle, an ordered product tag factors as `(a0-a1)*(b0-b1)` and is nonzero for distinct labels in a division ring. Expected frontier move: separate every primitive of the enlarged pair-selector seam. Falsification: a signed combination that preserves all old margins while canceling the new transfer.

The breaker condition is met. The natural `4x2` specialization gives nonzero tags to every old rectangle and false `111`, but exact search of `{-1,0,1}^8` finds a conformally primitive zero-margin, exact-zero-tag move of coefficient weight 8. A separate asymmetric `8x8` stress test finds a two-rectangle movement with coefficients `(2,-1)`, zero integer margins, zero `F_289` transfer, squared weight 12, and support 6. These results concern finite seam kernels; they do not prove that either movement satisfies every row or lies below a CVP threshold in an unspecified full tile.

Lean proves both sides: `Verify_product_tag_rectangle.lean` certifies local product separation, while `Verify_three_transfer_kernel.lean` proves every three `F_289` symbols have a nontrivial `F_17` dependency. Therefore old-move testing is insufficient and a bare single leading coordinate cannot control three independent surviving rectangle directions. The next discriminator is the fully serialized enlarged NAND/COPY matrix: either its extra rows eliminate these directions, or a lifted low-energy witness kills the single-coordinate candidate.

## Current Generation 4: fixed witness lifts through margin-only completions

Both reviews authorize only Proposal 1, the hash-locked lift-or-kill audit. Causal mechanism: extra emitted rows can rescue a single product tag only if they block the certified zero-tag movement or raise every exact lift to at least `17E`. Expected frontier move: an SNF/left-kernel nonextension certificate or a full-factor counterexample. Falsification: a malformed exact lift below `17E`.

No intended maximal-order candidate was available. The breaker therefore freezes the canonical margin-only completion with 18 variables, `22x18` emitted matrices, and `40x18` factors in both COPY orientations. All 16 legal cell/orientation fibers have `E=18`. The movement `(-1,1,1,-1,1,-1,-1,1)` is conformally primitive in the emitted kernel and gives exact zero residual at squared distance `42<306=17E` in every fiber; exact search covers 25,856 pair selectors through pair energy 32. A separate `36x18` decoded-margin serialization obtains the same attack energy. This kills only these two hash-locked margin-only completions.

`Verify_single_transfer_lift_obstruction.lean` proves the universal conditional dimension obstruction: whenever three independent integral seam directions survive all non-transfer rows, one bounded nonzero integer combination also survives, has zero `F_17^2` transfer, coefficients in `[-8,8]`, and squared coefficient weight at most 192. It does not supply the missing full tile or a CVP-energy bound. Any different candidate must now serialize every maximal-order and pair-dependent row before testing this witness; nonextension clears only the witness, not Q1.

## Current Generation 5: multiple pair channels pass the seam but miss physical flips

The only review survivor is the direct sum of rank-one product transfers (Fable 2 / Pro 1). Causal mechanism: `r` channels provide `2r` residue coordinates, so two channels can inject the frozen three-dimensional zero-margin pair seam. Expected move: remove all zero-syndrome malformed vectors below `17E`. Falsification: any unrestricted subthreshold malformed state with zero vector transfer.

The bounded synthesis succeeds on its declared subproblem. The first rank-three two-channel array occurs after 97 ordered pairs, detects the old weight-8 movement, and has no zero-syndrome malformed state among 7,152 same-margin pair selectors below threshold. This does not survive unrestricted low-weight testing. Since every channel row is supported only on pair selectors, flipping one physical NAND selector leaves all channels unchanged. For every `r=1..4`, orientation, and legal cell, exact Hamming-one search finds such a state at squared distance `20<306=17E`; 640 candidates cover 64 fibers. This is the breaker result and kills the four hash-locked unscaled channel-prefix factors only.

`Verify_multichannel_transfer.lean` proves the correct conditional framework: nonzero componentwise division-ring transport preserves vector-syndrome nonzeroness, injective syndrome detects defects, `r` channels have finrank `2r`, and any larger defect space forces a kernel. It does not certify the tested factors. A replacement must cover physical selectors or scale their residuals while preserving legal energy, then rerun physical Hamming-one/two and the unrestricted shell before any Graver or carry claim.

## Current Generation 6: marked Beneš bricks — toric exchange and DROP kills

The new ROADMAP retires pair-supported transfer and moves the frontier to L1, a full-brick higher-Lawrence realization. Both reviews select only marked oblivious Beneš routing. Causal mechanism: formula-specific wiring changes targets on one fixed switch topology, while physical/anchor columns are transported only by color-preserving signed permutations. Expected move: a marked fixed-matrix normal form. Falsification: an honest-affine malformed primitive, unequal energy, setting-dependent matrix, or cheap DROP.

The breaker freezes a `54x76` pair-linearized switch matrix. Exact search finds a support-eight conformally primitive toric exchange with zero residual in every row. It is exactly `h000-h011-h100+h111`, so it lies in the honest affine-difference lattice and cannot be detected by any quotient required to vanish there. All 384 permutation/input fibers admit it at energy 92 or 108 versus legal energy 76. This is the operative finite kill of that brick.

The builder freezes a different `136x142` target-only local matrix. It has common legal energy 142 and passes 5,832 physical Hamming-one/two kernel tests, but the all-zero vector costs 692, below `17*142=2414`; residual scale 5 is killed by DROP. `Verify_integral_euclidean_isometry.lean` separately proves that integral Gram-preserving square transformations are signed permutations, validating the roadmap's marking restriction but not L1. A next full brick must include fanout and COPY cycles and must defeat the honest-affine exchange and DROP before any depth induction.

## Current Generation 7: quadratic characters — equal-radius ghosts and cycle primitive

The only opponent-review survivor is Pro 2's quadratic-character switch orbit. Causal mechanism: `q(a,b)=(1,(-1)^a,(-1)^b,(-1)^(ab))` gives the old rectangle a nonzero quadratic derivative while all honest words retain one norm and wire swap remains marked. Expected move: escape the Generation-6 common-fibre exchange. Falsification: a normalized signed selector or glued cycle movement with malformed energy at most legal energy.

The breaker finds three support-three ghosts in the complete local `{-1,0,1}^4` search. The selector `(-1,1,1,0)` is normalized and maps to the non-honest sign word `(1,-1,-1,1)`, whose squared norm is the honest value 4. Across 65 tested mark scales, normalization is separately raised until DROP clears `17E`; the ghost remains below threshold. This is the operative finite local kill.

A hash-locked `74x44` three-COPY cycle gives a stronger serialized failure. Exhaustion of 531,441 COPY movements finds a conformally primitive synchronized three-rectangle kernel vector. In all four fibers its malformed energy is exactly `885`, equal to legal energy, while DROP costs 120,000 and physical Hamming-one/two changes are nonkernel. `Verify_quadratic_character_switch.lean` proves common radius, nonzero mixed derivative, integer independence, and marked swap, but those local facts do not exclude equal-norm signed ghosts or cycle cancellation. Any repair must charge all three ghosts and the synchronized cycle before L1 depth work.

## Current Generation 8: separator surrogate passes finite gates; support-only inference is unsafe

The ROADMAP now retires full-brick Lawrence as the primary route and moves the frontier to U0, exclusion from four fixed-template optimization classes. Both reviews retain only a support-separator/treewidth mechanism. Causal mechanism: detector support should have growing separators preserved by faithful equality contraction. Expected move: finite authorization for serializer and class-side Lean lemmas. Falsification: bounded decomposition, failed contraction, or failed growth.

The affine-detector surrogate passes the preregistered finite checks. At sizes 8, 16, and 32, independent HiGHS and CBC models certify exact top-level balanced separators 4, 6, and 9. Faithful one-subdivisions contract back, and 654,384 sparse signed defects have image energy at least support in the searched ranges. This is not an actual universal-circuit factor or a hereditary separator profile.

The breaker supplies a synthetic caution rather than a counterexample to that surrogate. Its cumulative controls contain `K_{4,4}`, `K_{8,8}`, and `K_{16,16}` support subgraphs but also support-two/three kernel moves and unimodular row-equivalent tree-incidence presentations. Thus displayed support growth alone says nothing about signed soundness and is not robust under arbitrary equation rebasing. `Verify_support_minor_channel.lean` proves only that `[I|-C]` preserves the original support as an induced minor and that explicitly faithful equality expansions preserve minors. U0 still needs actual serializers, precise admissible transformations, hereditary growth, and four separate class-side bounds.


## Current Generation 9: raw U0 invariants killed; serializer-first reroute

The builder and breaker expose two separate failures in the former U0 edge.
First, ordinary marked neighborhood diversity is not bounded even on the
smallest fixed templates.  The standard fixed n-fold family with
`A1=A2=[1]` and its systematic augmentation `[I|-C]` have every colored
vertex in its own twin class at the tested sizes, while both support graphs
are trees.  Exact counts for `n=8,16,32` are `17,33,65` for `C` and
`26,50,98` for `[I|-C]`; the latter has balanced separator one.  This is
verified by `experiments/verify_gen8_neighborhood_diversity_nfold_counterexample.py`.
The universal Lean file `Verify_two_stage_neighborhood_counterexample.lean`
proves the analogous unbounded row-neighborhood phenomenon for the fixed
two-stage template `A=B=[1]`.

Second, displayed support width depends on the equation basis.  A cumulative
unimodular presentation of the literal fixed n-fold family has complete
bipartite supports and exact separators `6,11,22` at the three tested sizes,
yet first differences return the fixed template.  This is checked by
`experiments/verify_u0_fixed_nfold_support_counterexample.py`.  Universally,
`Verify_row_rebasing_support_failure.lean` proves that cumulative systematic
`[I|-C]` matrices contain arbitrary `K_{m,m}` witnesses but rebase to a
bidiagonal block plus leaves, and `Verify_row_rebasing_kernel.lean` proves
that such invertible integral left rebasing preserves the integer kernel.

This does not decompose the affine-detector surrogate or the absent actual
universal-circuit factor.  It kills the claimed raw-invariant implication and
shows that former U0 was ordered before its object existed.  The route is now:
U0a must hash-freeze the actual serializer and define uniform grammars; only
then may U0b seek a row-basis-invariant column-matroid connectivity or
branch-width obstruction.  Ordinary neighborhood diversity and one-basis
support separators are no longer admissible U0 witnesses.


## Current Generation 10: finite U0a factors; chosen-basis matroid reroute

The builder supplies the first complete numerical factors rather than another
support surrogate.  `verify_u0a_universal_topology_serializer.py` freezes
width-8/16/32 butterfly NAND/COPY topologies, complete sparse `C` and
`D=[I|-C]`, target interfaces, fixed row/column kinds and full JSON artifacts.
Three honest programs per width have energies `72,176,416`.  Physical identity
rows make selector coefficient motion visible in the ROADMAP y-objective.
This is still finite: no all-size `Serialize(S,F)`, formula compiler,
polynomial family theorem, rank theorem, soundness, or class exclusion follows. The depth verifier sharpens the limitation: the artifacts have `8,10,12` stages and cannot embed strict NAND chains of lengths `9,11,13`.

The breaker finds a localized affine rectangle in the actual matrices.  It
annihilates every semantic/program/edge/separator/output row but is seen by the
physical identity block.  Adding it to an honest selector changes exact energy
only `72->74`, `176->178`, `416->418`.  This additive-two pattern is finite
evidence and a mandatory U2/U3 adverse state, not a recurrence or soundness
counterexample.

`U0_GRAMMARS.md` now makes the four class templates uniform, separates IDs
from finite structural colors, and demands objective-preserving auxiliary
bijections.  Its crucial correction is that a CVP basis change `C -> C Q` for
`Q in GL_n(Z)` is as semantically free as a left equation rebase.

That correction kills the first U0b repair.  Lean proves `C` and `CQ` generate
exactly the same lattice image and attainable output-cost values.  Exact
finite enumeration nevertheless gives nonisomorphic column matroids for their
systematic `[I|-C]` presentations, and cumulative bases change a fundamental
circuit from support two to support `9,17,33`.  Thus chosen-basis column
circuits/connectivity/branch-width cannot be the final U0b invariant.  The
frontier remains the all-size U0a compiler; later U0b needs an invariant of the
embedded lattice plus ambient objective.


## Current Generation 11: parameterized compiler passes finite formula audit

The shallow-depth kill is repairable without superpolynomial dimension.  The
factor generator now accepts depth `d`; Lean proves exact dimensions
`k=4w+20wd`, `m=30wd+9w-2d` and explicit quadratic bounds in `w+d`, and proves
chain placement is equivalent to choosing enough stages.  The finite chain
verifier checks depths through 33 on actual matrices.

The routing mechanism has both an exact warning and a repair.  Default width
8 realizes 18,688 rather than all 40,320 permutations, but the ninth scheduled
stage reaches all of them.  Two-cycle exhaustion realizes all permutations at
widths 4 and 8.  Hence frozen default depth is not universal, while repeated
polynomial depth remains viable.

The new compiler treats the topology as a register machine: source variables
are unique FREE selectors, COPY creates repeated occurrences, hypercube swaps
move live tokens, NAND consumes children, and cleanup makes all unused outputs
constant.  It passes every assignment for 100 small NAND trees and an 8-leaf
case on actual `C,D`.  This resolves the earlier witness-dependent-output flaw
for the audited programs.  The surviving frontier is proof, not another local
example: formalize generic evaluation/routing/fanout and polynomial emission in
Lean.  Soundness remains entirely open; an honest false output costs only one.


## Current Generation 12: semantic theorem compiled; recursive emitter killed

Lean now proves the formula-semantic half of U0a universally.  Canonical
postorder code evaluates every NAND tree correctly under one shared variable
assignment, fixed root assertions do not depend on witnesses, and instruction
count is linear in syntax nodes.  The unproved bridge is physical: register
placement, fanout, butterfly routing, cleanup and the numerical factor.

The canonical manifest makes the finite interface byte-strict and
assignment-independent.  An independent exhaustive scheduler checks 1,901,166
shape/equality-pattern cases through eight leaves with no padding failure.
The former 1,101-leaf `RecursionError` is now repaired with explicit traversal,
canonical byte-parser, and scheduler stacks.  A compressed dry manifest avoids
materializing its roughly two-billion padded mode cells.  The next mutation is
not a new gadget: prove correspondence to the Lean postorder compiler and
physical placement trace, then give an actual streaming `C,D,target` emitter;
the dry manifest itself is not the reduction output.


## Current Generation 13: iterative front end repaired; eager emission blocked

The old deep recursion witness now passes explicit-stack traversal, semantic
evaluation, canonical byte parsing and dry scheduling.  Padding is a count and
the unpadded event trace is hashed online.  A width-64 medium witness is still
fully materialized, anchoring dry-run decisions to the real compiler.

Lean supplies the matching abstract register invariant: postorder compilation
allocates consecutive fresh registers, preserves the outside register file,
uses only older operands and computes the formula root; COPY and NAND into a
fresh destination preserve sources.  The missing proof is now specifically
lane placement and row realization, not Boolean semantics or SSA freshness.

The breaker moves the implementation frontier from recursion to emission.  A
256 MiB child process dry-schedules `S=16` but raises `MemoryError` in complete
eager serialization.  Since exact counts remain polynomial, the authorized
repair is a canonical streaming sparse emitter, not a claim of mathematical
impossibility.


## Current Generation 14: sparse factor stream succeeds; dense program remains

Canonical row/column/C/D/target generators now agree item-for-item with eager
serialization on all audited grids.  The S=16 child stays far below the same
memory cap that killed the eager object graph.  Lean independently proves that
folding arbitrary COO records has exactly dense matrix-vector semantics.

The breaker found and closed one metadata discrepancy: WAIT dimensions were
logged after stage increment in the eager trace.  Current eager and dry hashes
now agree.  The cap failure moves cleanly to the dense padded program at S=128.
The next mutation should stream only non-COPY_A stage overrides and cleanup,
then derive GATE_PROGRAM targets directly from that stream; rebuilding factor
streaming is no longer justified.


## Current Generation 15: padded program becomes a sparse override stream

The program grid no longer needs a dictionary entry per stage/lane.  Raw
routing events store only COPY_B/NAND/ZERO deviations from COPY_A; padding is a
count; final cleanup switches the default to ZERO and records the root COPY_A.
Targets are streamed directly from lookup.  Exact comparisons and a width-256
resource child find no representation error.

Lean proves the generic default/override and one-hot-target semantics.  The
frontier is no longer Python storage but proof integration and output volume:
connect the sparse event list to the fresh-register compiler and butterfly
lane invariant, and prove every emitted row consumes the intended mode/value.


## Current Generation 16: event semantics and every numerical row align

Lean now proves that each sparse event pattern has its advertised lane effect
and that valid event traces compose.  Finite numerical verification goes all
the way from selected local-state columns through every C/D row, rather than
stopping at the formula output.  Independent mutation tests reject all
nonsymmetric orientation errors.

The surviving proof gap is exactly the antecedent of the Lean trace theorem:
show the generic sparse compiler always emits valid adjacent events and
maintains its token map, then show the token-selected columns realize the
streamed row equations universally.  This is the last honest-completeness
bridge before soundness becomes the primary frontier.


## Current Generation 17: smart XOR traces verified; snapshots are too large

Lean smart constructors make nonadjacent or self-loop SWAP/DUPLICATE/NAND
events unrepresentable, so the full physical/logical trace theorem is now
unconditional for generated XOR events.  A JSON event certificate independently
replays the Python token map and binds it to selected numerical columns and C
rows on the finite audit.

The next blocker is certificate representation rather than computation:
storing full token maps before and after every event fails the 1,025-leaf cap.
Store only the event delta and enough canonical checkpoints for independent
replay; prove the delta stream elaborates to Lean XorEvents.


## Current Generation 18: delta certificates replace snapshots

A v2 certificate carries only event deltas plus initial/final maps.  Independent
replay and framed checkpoint hashes retain mutation detection while a 4,097-leaf
comb fits the cap.  Lean proves the generic fold principle: state-dependent
local delta equality composes to the claimed final map.

The remaining bridge is concrete rather than representational.  Identify each
JSON event with a Lean smart XorEvent and prove its token delta is exactly that
event's logical token-map update; then connect final token placement to the
already verified selected numerical columns.


## Current Generation 19: explicit deltas match the Lean data model

V3 no longer leaves SWAP changes implicit.  Occupied endpoint tokens move
explicitly; duplicate and NAND use canonical short create/delete lists.  Lean
proves these exact lists implement logical token transitions, and the breaker
rejects missing, reordered or colliding changes.

The remaining gap is generation rather than local semantics: prove the formula
scheduler always meets concrete occupancy/freshness/finite-lane preconditions
and emits the canonical v3 list.  That induction can then feed the existing
trace and row theorems.


## Current Generation 20: finite lanes and occupancy are no longer missing lemmas

Lean packages XOR routing on `Fin (2^k)` and proves closure, involution and
nontrivial pairing.  The concrete delta model now preserves exclusive token
ownership and exact live-token counts.  Large boundary tests find no out-of-
range event across 8,192 lanes.

The only honest-completeness induction still absent is the scheduler algorithm
itself: connect postorder demands, least-free-lane choice and hypercube paths to
these typed finite events and invariants.  All local semantic, delta, finite
lane and count lemmas needed by that induction now exist.
