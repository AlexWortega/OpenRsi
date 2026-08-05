# PCP-free polynomial-factor CVP hardness

No hardness theorem or asymptotic lemma has been established.

## Finite obstruction: residual spreading misses slack cheats

Consider the unsatisfiable conjunction of all eight sign patterns of a 3-literal clause on `x,y,z`. For clause literal sum `L_i`, the tested affine residual is

`r_i = L_i - 1 - a_i - b_i`,

with integer slack coordinates. The RS block evaluates `R(T)=sum_i r_i T^i` for `T=1,...,64`; every coordinate also pays scaled half-integral anchor squared cost `(2z-1)^2`. The Boolean baseline for 19 coordinates is therefore 19.

Any nonzero `r` gives RS squared energy at least 57 because a nonzero degree-at-most-7 polynomial has at most seven roots. Nevertheless, a Boolean assignment falsifies exactly one of the eight clauses, and choosing slack `(-1,0)` there (ordinary Boolean slack elsewhere) makes every `r_i=0`. The exact squared objective is then 27, only 8 above baseline, for distance ratio `sqrt(27/19)`.

`experiments/verify_rs_slack_cheat.py` deterministically certifies this finite optimum. Thus spreading affine residuals alone cannot supply the claimed move for this gadget: soundness must also prevent or amplify non-Boolean slack. This is not a general impossibility theorem for RS-based reductions.

## Finite affine-isolation observation

For one falsified OR clause, let the seven satisfying local patterns be columns of `P`. A signed selector `y` is harmful when `sum(y)=1` and `P^T y=0`, since it mimics global marginals `(0,0,0)`. The elementary example is `001 + 010 - 011`.

`experiments/verify_affine_isolation_core.py` tests all degree-one left-regular binary measurement matrices with seven selector and five auxiliary columns and one to three rows. Exact bounded search finds short cheats for every one- and two-row matrix. For three rows, 18 of 531,441 matrices have no harmful point in the tested coefficient box `[-3,3]`; one representative places selector columns on rows `[0,0,1,0,1,1,2]` and all auxiliaries on row 0.

### Exact unbounded certification

Generation 3 removes the coefficient-box caveat for the 18 survivors. For each matrix and each legal one-hot reference, write the harmful affine system as `A z=b`. The new verifier supplies an integral left-kernel vector `w` satisfying

`w^T A = 0` and `w^T b != 0`.

Therefore each system is inconsistent over `Q`, and a fortiori over `Z`. For the representative selector-row assignment `[0,0,1,0,1,1,2]` with all auxiliaries on row 0, one certificate (up to sign) is `[1,-1,-1,-1,0,1,2]`; its seven right-hand-side pairings are `1,1,2,1,2,2,3`. `experiments/verify_affine_isolation_unbounded.py` checks corresponding certificates and independent rational elimination for all `18*7=126` systems.

This is only a finite local isolation fact.

### Overlap counterexample

Generation 5 tests whether private copies of these syndrome rows compose when clauses share one or two variable marginals. They do not. Once unshared marginals are free, every tested composed matrix has a nonzero integer kernel move of squared norm at most 4. For the representative and a first-variable overlap, one move on clause-one selectors is

`[-1, 0, 1, 1, -1, 0, 0]`.

It preserves selector normalization, all three private measurement rows, and the shared first marginal; all auxiliaries and the second clause remain unchanged. `experiments/verify_overlap_composition.py` checks exact row preservation for all 5,832 ordered survivor-pair/overlap/polarity systems and 95,256 compatible references.

Therefore the fixed-marginal local isolation certificate cannot be used as the claimed private-row composition gadget. This is a finite mechanism kill, not a general theorem about affine encodings. No uniform matrix family, CVP basis/target, completeness radius, soundness threshold, or dimension-gap scaling law follows.

## Finite global-quotient audit (invalidated as CVP evidence)

For the all-eight-clause core, introduce all 64 clause/local-pattern selectors, including each clause's false `000` label. The eight complete Boolean selector vectors generate seven difference relations `H`. Generation 6 tests the quotient

`Z^64 / H`.

Normalization and variable consistency are affine equations defining harmful selectors, not quotient generators: quotienting by their entire preserving kernel would make every consistent harmful move zero tautologically. The emitted manifest lists all 64 coordinates, eight normalization and 21 consistency checks, seven quotient relations, 48 face-circuit attacks, and the absence of slack/auxiliary coordinates.

Smith normal form has seven unit invariants, so this finite quotient is torsion-free of rank 57; independent rational elimination gives relation rank 7. For each Boolean reference, exact low-weight search enumerates every integral deviation with squared norm at most 12 that removes all false labels while preserving normalization and common global marginals. There are 156,880 such reference/deviation pairs. None has zero quotient syndrome, and none has zero syndrome modulo 2. The minimum harmful squared norm is 4 and the minimum binary syndrome weight is 4.

The verifier also emits a 178-dimensional full-rank triangular basis `[[S,0],[ES,2I]]` and target `[h,Eh]`, where `E` repeats the 57 binary quotient checks and `S` scales the eight false selectors by 2. Its determinant is `2^122`; the minimum tested harmful squared distance is 12. This is a finite Construction-A carry audit only. Listing all complete assignments is exponential for general formulas, and no polynomial-size relation generator, completeness/soundness scaling law, or hardness reduction has been proved.

Verified by `experiments/verify_global_selector_quotient.py` and its checked manifest `experiments/gen6_global_selector_manifest.json`. The Generation-6 gate nevertheless invalidated this as soundness evidence: the affine checks were external filters, the distance audit changed references, and the nine-clause instance supplies an unrestricted mod-2 bypass.

## Finite counterexample: cyclic radix residuals have an exact kernel

Generation 7 implements only the surviving Pro Proposal 5 on the nine-clause four-variable edge-cover formula. For 72 integral truth-table selectors `z`, the emitted rank-72 lattice and one fixed target realize

`||2z-1||^2 + ||Az-b||^2 + ||R(Az-b)||^2`.

The 41 rows of `A` are nine selector normalizations, nine forbidden-`000` legality checks, and 23 occurrence-consistency checks. `R` contains every cyclic ordering of these residuals with base 33. The ambient dimension is 154. There are no slack, carry, or externally filtered variables. The manifest emits every basis column and target coordinate; the verifier reconstructs them and checks a canonical column-HNF hash.

The nine falsification edges cover all 16 Boolean assignments. Hence squared distance 72 would force all selectors to be Boolean and every residual to vanish, which would give a satisfying assignment, impossible for this finite formula. The exact signed attack at global marginals `0000` uses honest one-hot blocks except in clause 0, where

`000` is replaced by `011 + 100 - 111`.

This block has coefficient sum one and all three literal marginals zero. It therefore preserves normalization and every shared marginal while setting the illegal selector to zero. Thus `Az=b`, every radix residual is exactly zero, and only one coefficient `-1` raises anchor energy by 8. The squared distance is 80.

This is also the exact unrestricted minimum. Every integral anchor contributes at least one, and each excess is a nonnegative multiple of 8. Below 80 all selectors would therefore be Boolean. For Boolean selectors every raw residual digit has absolute value at most 7; since `7(33^40-1)/32 < 33^40`, a nonzero residual has a nonzero leading digit in every cyclic radix row, giving squared cost greater than 80. Zero residual is excluded by the 16-assignment coverage. The signed witness attains 80.

`experiments/verify_multiorder_radix_barrier.py` deterministically checks these finite claims and `experiments/gen7_multiorder_radix_manifest.json`. The ratio `sqrt(80/72)` is not a polynomial-gap theorem; the exact kernel kills only this tested linear radix mutation.

## Finite global PSD-metric audit

Generation 9 tests the only cross-review survivor: a predeclared incidence-equivariant quadratic metric with two shared scales. For each formula, `A` contains clause normalization and legality plus all pairwise consistency rows for global singleton and pair moments. The emitted rational Euclidean factor and fixed target realize

`||2z-1||^2 + 25||Az-b||^2`,

with Gram matrix `Q=4I+25A^T A`. Thus `Q` is positive definite with certified minimum eigenvalue at least 4. The manifest records the exact factor, target, Gram matrix, rational center, and orthogonal target energy for both instances.

A fixed satisfiable overlapping nine-clause control has an honest vector attaining the universal anchor lower bound 72, so its exact unrestricted squared minimum is 72. The nine-clause obstruction covers all 16 assignments. Its old three-term replacement `011+100-111` has nonzero pair-moment residual and squared distance 305.

Exact low-weight search does not stop there. Any vector through squared radius 96 has derived coefficients in `{-2,-1,0,1,2,3}` from its anchor energy. After normalization and legality, there are exactly 959 local signed states through anchor excess 24. Dynamic programming joins all shared degree-one/two moments without a coefficient filter. The minimum zero-residual extra is 24, attained by replacing one forbidden label with the seven legal labels using the cube-parity signs. A nonzero integral residual costs at least 25, hence total squared distance at least 97. Therefore the displayed parity vector proves the exact unrestricted obstruction minimum is 96.

The finite ratio is `sqrt(96/72)=sqrt(4/3)>1.1`. This is not a hardness lemma: the nearest vector is precisely a constant-cost low-degree parity kernel, and no uniform synthesis, composition law, or dimension-dependent gap has been proved. `experiments/verify_global_psd_metric.py` checks the manifest and every stated finite calculation.

## Finite counterexample: available cubic moments leave an isolated triple

Generation 11 adds every all-pairs consistency row for squarefree global moments through degree three to the Generation-9 fixed-target construction. The checked manifest emits the complete factor and target for

`||2z-1||^2 + 25||A_{<=3}z-b||^2`,

so `Q=4I+25 A_{<=3}^T A_{<=3}` is positive definite and coefficients are unrestricted integers. The satisfiable control still has exact squared minimum 72 by an honest witness and the coordinatewise anchor lower bound.

The new cubic rows detect the inherited seven-term parity in clause 3: its raw residual squared norm becomes 1 and its squared distance 121. They do not raise the obstruction optimum. Clause 1 is the only occurrence containing global triple `(0,2,3)`, so all-pairs consistency emits no row for that triple. Moving the same seven-term cube-parity block to clause 1 changes only this unshared top moment, preserves every emitted row, and has anchor excess 24.

Exact DP enumerates all 959 normalized/legal signed local states through anchor excess 24 and joins all shared degree-zero-through-three moments. It proves minimum zero-residual excess 24. Any nonzero integral residual costs at least 25 on top of the universal anchor cost 72, hence at least 97, while the displayed zero-residual selector attains 96. Thus the exact obstruction minimum remains 96 and the finite ratio remains `sqrt(4/3)`. This falsifies only the fixed cubic mutation; it is not an asymptotic limitation on other constructions.

`experiments/verify_degree3_global_psd_metric.py` checks these claims and `experiments/gen11_degree3_global_psd_metric_manifest.json`.

## Finite counterexample: a spherical parity tag exposes clause dropping

Generation 12 tests an explicit bounded survivor from the dissociated spherical-fingerprint proposal. For local pattern `a`, assign the top Walsh tag

`chi(a)=(-1)^(1+|a|)`,

and give each clause its own tag coordinate. Every one-hot local label contributes tag squared norm one, independent of signs, so every honest nine-clause encoding has fingerprint squared radius `H=9`. The rational fixed-target factor emits

`||2z-1||^2 + 25||A_{<=3}z-b||^2 + ||Fz||^2`,

with `Q=4I+25 A_{<=3}^T A_{<=3}+F^T F >=4I` and unrestricted integral coefficients. The completeness squared radius is 81. A seven-term cube parity has tag magnitude seven in its changed clause, so the inherited attack rises to squared distance 153.

This does not meet the prescribed strict threshold `(4/3)81=108`. Set every selector in clause 0 to zero and choose compatible legal one-hot labels in the other eight clauses. The anchor contribution remains 72, the missing normalization contributes 25, all moment comparisons and other residuals vanish, and eight remaining tags contribute 8. The squared distance is 105.

The verifier exactly enumerates every integral selector vector through squared distance 108. The coordinate range `[-2,3]` follows from the anchor lower bound. A DP retains exact running sums and sums of squares for each shared moment, thereby charging every pair residual without an external consistency filter. It proves exact obstruction and control minima 105 and 81, respectively. The finite squared ratio is `35/27<4/3`.

`experiments/verify_spherical_parity_fingerprint.py` checks the emitted factor, target, Gram data, shell search, and `experiments/gen12_spherical_parity_fingerprint_manifest.json`. This is a counterexample only to this explicit dimension-9 Walsh candidate, not to all spherical fingerprints or global PSD metrics.

## Finite obstruction: honest-compatible raw-selector codes miss an affine parity

Generation 13 performs the compatibility audit required before the surviving Construction-A/expander syndrome proposals may emit carries or scale syndromes. Let `h_0,...,h_15` be the 16 globally consistent one-hot encodings in the 72 selector coordinates. Any linear hash assigning all of them one common target must annihilate

`D_p = span_{F_p}{h_i-h_0}`.

For each `p` in `{2,3,5,127}`, exact modular elimination gives `rank(D_p)=14`; the verifier constructs the full 58-dimensional orthogonal complement, so it tests the maximal possible compatible linear syndrome rather than a selected code.

The Generation-11 unique-triple parity selector `z*` has anchor excess 24 and satisfies the exact integer identity

`z* = sum_i c_i h_i`,

where, in lexicographic assignment order,

`c = [1,-1,-1,1,0,0,0,0,-1,1,1,-1,1,0,0,0]`

and `sum_i c_i=1`. Therefore any linear hash with `Hh_i=t` obeys `Hz*=sum_i c_i t=t`. This holds over the integers and modulo every prime. In particular, the maximal compatible syndrome of `z*-h_0` is zero for all four audited primes. Construction-A carries, code distance, or syndrome scaling cannot charge this exact collision.

The same verifier audits the supplied G5 representative embeddings, G7 three-term attack, G9 parity, and all 144 simple clause drops; those have nonzero maximal syndromes, but one collision suffices to falsify the bounded raw-selector coding mutation. `experiments/verify_selector_code_compatibility.py` checks the exact affine identity, modular bases, and `experiments/gen13_selector_code_compatibility_manifest.json`. This is a finite obstruction for linear hashes of the current 72 selectors, not a theorem about nonlinear or enlarged encodings.

## Finite pair-bag shell audit

Generation 14 implements the sole Fable survivor. For every pair of the nine clauses, introduce one integral selector for each assignment to the union of their variables. Seven bags have 8 selectors and 29 have 16, so the common obstruction/control baseline is `B=520`. The emitted rows are one normalization per bag, both forbidden-label marginals per bag, and canonical-star equality of every full eight-label clause marginal across its eight incident bags. The exact fixed-target objective is

`||2z-1||^2 + 25||Az-b||^2`,

with 612 residual rows and unrestricted integral coefficients.

No obstruction vector exists through squared radius `B+32=552`. Each non-Boolean integral bag contributes at least 8 anchor excess, so at most four bags are non-Boolean in this shell. The complete pair mesh gives every clause eight incident bags; hence every clause retains a Boolean incident bag. At zero residual that bag is a legal one-hot assignment, and full-marginal equality propagates its legal one-hot clause label to all incident bags. Joint endpoint marginals force every pair of clause labels to agree on shared variables. Exact backtracking over legal labels finds no globally compatible tuple, equivalently no satisfying assignment.

A nonzero integral residual costs at least 25, leaving anchor excess at most 7 and forcing every coefficient Boolean. Squared residual at most one would then mean exactly one bad row. A bad normalization necessarily changes a full-marginal total; one forbidden one-hot label propagates to all eight bags incident to its clause; and two distinct one-hot marginals differ in two label rows. Thus none can be the sole residual.

The control has an honest vector at 520, equal to the coordinatewise integral anchor lower bound, so its exact unrestricted minimum is 520. The Generation-11 affine collision does extend to pair bags, but the 29 four-variable bags each retain its signed measure and the total anchor excess is 928, giving squared distance 1448. The G7 attack fails overlap compatibility on seven incident bags. Direct evaluation puts every single-bag and single-clause control drop above 552.

`experiments/verify_pair_bag_lift.py` checks the emitted matrix/target hash, shell proof, reconstructed attacks, drops, and `experiments/gen14_pair_bag_lift_manifest.json`. This finite pass does not establish fixed-level composition, a uniform soundness lemma, or a dimension-dependent gap.

## Finite counterexample: a weighted laminar hierarchy admits the affine lift

Generation 15 preregisters the sole surviving hierarchy direction before testing. The deterministic adjacent-pair laminar tree has nine clause leaves and eight internal assignment nodes of sizes 2, 4, 8, and 9 clauses. Because the fixed formula has four variables, leaves have eight selectors and internal nodes have sixteen, for 200 unrestricted integral coefficients. The emitted 210 rows are all node normalizations, leaf legality equations, and parent-child full-marginal equations.

The unscaled anchor weights are `1` on leaves and `1/16` internally; residual weight is `16`; and `delta=1/2`. After multiplying squared distance by 256, the exact integral factor uses `(32z-16)^2` on leaf coordinates, `(2z-1)^2` internally, and `256^2(Az-b)^2` on residuals. The completeness baseline is

`B = 72*256 + 128 = 18560`,

and the preregistered threshold is

`T = B + 256*9^(3/2) = 25472`.

The G13 affine coefficients sum to one. Applying them to the 16 globally consistent hierarchy encodings commutes with every marginal map. At the leaves the result is exactly the legal G11 unique-triple parity selector; at every internal four-variable node it is the same signed global measure. Consequently every emitted residual is zero. The leaf parity adds scaled anchor excess `24*256=6144`, while each of eight internal nodes adds 32, for total excess 6400 and squared distance

`18560 + 6400 = 24960 < 25472`.

Thus high residual weights do not help this mutation: the affine pseudodistribution threads the full hierarchy. The satisfiable control has exact minimum 18560 by an honest vector and the coordinatewise anchor lower bound. Single-leaf drops are heavily charged, confirming that deletion weighting alone misses the zero-residual attack.

`experiments/verify_weighted_laminar_hierarchy.py` checks the emitted rows and factor/target hash, the affine lift, threshold comparison, control minimum, and `experiments/gen15_weighted_laminar_hierarchy_manifest.json`. This is a finite kill of the frozen hierarchy/weight rule only, not an asymptotic theorem about all sparse hierarchies.

## Finite counterexample: signed flow splices a Barrington ACCEPT path

Generation 19 implements the sole surviving Fable proposal. A deterministic balanced AND/OR tree for the nine clauses is compiled by the width-5 commutator construction. Lexicographically fixed 5-cycles and commutator pairs produce 3,250 layers, of which 1,300 query a variable and 1,950 apply a constant permutation. Direct evaluation on all 16 assignments verifies that the obstruction always returns the identity state and the matched control accepts exactly its satisfying assignments.

The lattice uses one coefficient per transition edge—five at a constant layer and ten at a queried layer—plus four shared query totals, for rank 22,754. Its 17,555 rows emit the source unit flow, ACCEPT sink, every interlayer conservation equation, and one branch-one-total equality for every repeated query. The exact objective is

`||2z-1||^2 + 25||Az-b||^2`.

An exact dynamic program keeps the five-component integral flow and four shared query totals. Its cost unit is `z(z-1)/2`, exactly one eighth of anchor excess. It enumerates every transition choice in the objective-derived coefficient range. No exact accepting flow exists through one cost unit, but at two units it reconstructs one with two edge coefficients `-1`, 3,252 coefficients `1`, and all remaining coefficients zero. Every emitted residual vanishes, and the anchor excess is 16.

The universal integral anchor lower bound is 22,754. A nonzero integral residual adds at least 25, whereas the signed ACCEPT flow attains 22,770. Hence 22,770 is the exact unrestricted obstruction minimum. The satisfiable control has an honest Boolean accepting path at the baseline, so its exact minimum is 22,754. The resulting ratio is only finite and tends to one under naive length growth.

`experiments/verify_barrington_signed_flow.py` checks the compiler, full sparse row manifest, factor/target hash, exact shell DP, reconstructed witness, and `experiments/gen19_barrington_signed_flow_manifest.json`. This kills only this emitted branching-program flow encoding; it is not a theorem about every nonlinear computation encoding.

## Finite failure: a frozen reduced pair-tile has no favorable min-plus growth

Generation 28 implements the sole authorized Pro survivor as a literal finite recursion rule. A tile contains two same-variable G14 pair bags. Each bag has eight unrestricted integral assignment coefficients, normalization, and two endpoint-legality rows; eight full-assignment rows glue the bags. Two tiles are composed using the singleton allowed seam permutation, the identity. The fixed-target objective is

`||2z-1||^2 + 25||Az-b||^2`.

The depth-two obstruction uses the eight clause signs that forbid all assignments of three variables. Its matched control replaces forbidden assignment seven by a duplicate of zero. Both factors have rank 32 because their anchor block is `2I`, and `Q=4I+25A^T A>=4I`. An explicit one-hot obstruction vector has squared cost 57, so every possible minimizer lies in that radius. The other 31 odd anchor squares then force every coefficient into `[-2,3]`.

The verifier exhausts every depth-one state of cost at most 41 and composes every seam fiber of total cost at most 57. Each of the three depth-one tables has 20 entries. The complete obstruction table has eight entries, all ILLEGAL and cost 57. The complete control table has one LEGAL entry of cost 32 and six ILLEGAL entries of cost 57. These minima also have short exact proofs: zero obstruction residual would equate all four ports, its eight legality rows would set every port coordinate to zero, and normalization would require their sum to be one; the control has an honest assignment at the universal anchor baseline.

The minimum depth-one adverse and legal costs are 32 and 16. Hence the tested raw growth factors are

`lambda = 57/32 < mu = 32/16 = 2`.

The serialized priority partition is exhaustive over integral states and explicitly names LEGAL, ILLEGAL, DROP, G13, G19, and MALFORMED. Diagonal DROP, G13 parity, and exact two-negative G19 seeds have squared costs 132, 303, and 221. `experiments/verify_frozen_minplus_pair_tile.py` checks the complete tables and `experiments/gen28_frozen_minplus_pair_tile_manifest.json`.

This is a finite falsification of this reduced recursion rule's growth inequality, not a statement about arbitrary tiles and not an asymptotic hardness result.

## Finite tensor obstruction: the frozen depth-one seed pair is isometric

Generation 30 tests the sole authorized Fable survivor. For each G28 depth-one right tile, let `C=[2I;5A]` and `y=[1;5b]`; the literal two-copy proposal uses `C tensor C`, `y tensor y`, and an unrestricted integral `16x16` coefficient matrix. The seed rank and ambient dimension are 16 and 30, while the product rank and ambient dimension are 256 and 900.

The alleged NO tile has endpoint-forbidden sets `((4,5),(6,7))`; the matched control has `((4,5),(6,0))`. Let `P` swap assignment coordinates zero and seven in both bags. An emitted ambient row permutation `Q` satisfies exactly

`C_YES P = Q C_NO` and `y_YES = Q y_NO`.

Consequently `P tensor P` maps every unrestricted integer product coefficient matrix bijectively and preserves its objective. This proves equality of the two product CVP distances without restricting to rank-one tensors. Both seed minima are 16, so the tested ratios are `R_1=1` and `R_2=1`; the required strict improvement fails. The common two-copy minimum is not claimed exactly: product anchor rows give the lower bound 256, and a rank-one honest witness gives the upper bound 1,888.

The first audited radius containing a representative of each named attack class is 31,285. The product singular value is at least 4 and `||y tensor y||=66`, so a coefficient of magnitude at least 61 would force distance at least `4*61-66=178`, whose square is 31,684. Thus the complete shell lies in `[-60,60]^256`, and the tensor permutation pairs all of it. Exact attack costs are 4,356 for DROP, 31,285 for the best diagonal G13 state, 11,749 for the best exact two-negative G19 state, and 4,420 for the tested rank-two malformed sum. The verifier also exhausts all 131,585 integer matrices of `l1` norm at most two; zero is best in that low-weight class at 4,356 for both seeds.

`experiments/verify_literal_tensor_seed_isometry.py` checks the factors, targets, product hashes, permutations, shell bound, attacks, and `experiments/gen30_literal_tensor_seed_manifest.json`. This is a finite falsification of this serialized seed pair, not an impossibility theorem for tensor lattices.

## Finite strict-four-thirds pass: an equal-radius Walsh Gram

Generation 31 implements the sole authorized Pro survivor. Let `A` be the emitted normalization, legality, and all-pairs squarefree moment matrix through degree three. Let `F` contain nine block-diagonal copies of the integral Walsh matrix `H_8`. The fixed-target objective is

`||2z-1||^2 + ||Fz||^2 + 100||Az-b||^2`.

Since `F^T F=8I`, its Gram matrix is `Q=12I+100A^T A`, with exact integral factor and rational center. Every globally consistent one-hot selector has anchor-plus-Walsh squared energy `72+72=144`, although its Walsh vector need not equal that of another assignment. A satisfying control selector has zero formula residual and attains 144. Conversely, a vector below 144 would have zero residual because a nonzero integral residual costs 100 above universal base 72. Zero residual makes every clause block normalized and legal; its integer base energy is at least 16, proving the exact control minimum `9*16=144`.

The obstruction shell is exhausted through 192. The coordinate energy is `12z^2-4z+1`, yielding the global coefficient interval `[-3,3]`. Since base energy is at least 72, only raw residual square zero or one can occur in the shell.

For residual zero, each block is normalized/legal. The other eight blocks cost at least 16, so one block costs at most 64 and has coefficients in `[-2,2]`. There are exactly 364 such signed local states, with cost histogram `{16:7,40:105,64:252}`. Exact DP joins their complete degree-one-through-three moment vectors. Its layer counts are

`[364,4030,4103,979,153,56,13,3,0]`,

so no zero-residual obstruction state survives through 192.

For residual square one, base energy is at most 92, only 20 above the all-zero base. Coordinate extras show that every possible vector is zero, has one `1`, one `-1`, or two `1` coordinates. Exhausting all 2,701 vectors finds minimum raw residual square 7, so this branch is also empty. Therefore the obstruction squared minimum is at least 193. A zero-residual G11/G13 parity vector has cost 216, while the repaired clause-drop vector costs 236. Hence only the finite interval

`193 <= d_NO^2 <= 216`

is certified, against exact control `d_YES^2=144`; in particular the finite squared ratio is at least `193/144>4/3`.

`experiments/verify_equal_radius_walsh_gram.py` checks the full factor, target, rational center, shell searches, and `experiments/gen31_equal_radius_walsh_gram_manifest.json`. This is not a scalable construction or an asymptotic hardness result.

## Finite composition failure: cross-copy moments remain additive

Generation 32 selects Pro Proposal 1 from the two cross-review survivors because it directly tests the missing composition law for the Generation-31 Gram. Two nine-clause copies share global variables 0 and 1; original variables 2 and 3 in the second copy are renamed 4 and 5. The rank-144 fixed-target objective retains 18 Walsh blocks and residual scale 10, while all-pairs squarefree moment rows through degree three are rebuilt over all six variables. This emits 433 checks, including 125 cross-copy moment rows.

Before composition, the verifier determines the exact one-copy obstruction value. A malformed local block has base at least 8 and one local residual costing 100; with eight other blocks of minimum 16, it would cost at least 236. Hence every vector through 216 is locally normalized/legal. Exactly 959 signed local states have possible costs `{16,40,64,88}`. Exact DP accumulates every all-pairs moment residual and has layer counts

`[959,2396,891,192,63,26,15,7,1]`.

Its unique terminal cost is 216, proving `d_1^2=216`.

A compatible satisfying assignment gives the two-copy control cost 288. This is exact by complete residual-branch accounting below 288. Residual zero forces 18 normalized/legal blocks and base at least `18*16=288`. With residual square one, a sole moment error gives at least `288+100=388`; a sole local error gives at least `17*16+8+100=380`. Residual square at least two gives at least `144+200=344`.

For soundness, use assignment values `x_0=x_1=1` in both copies and place the zero-residual G11/G13 parity block in clause 1 of each copy (global clause indices 1 and 10). The altered top moments use disjoint triples `(0,2,3)` and `(0,4,5)`, while every shared proper moment is unchanged. Thus all 125 cross-copy rows also vanish. The emitted unrestricted vector has

`d_2^2 <= 432 = 2*216 = 2d_1^2`.

It lies in the derived threshold coefficient interval `[-4,5]`. Therefore the preregistered strict-superadditivity condition fails exactly at the additive boundary. `experiments/verify_crosscopy_walsh_composition.py` checks the full factors, targets, one-copy DP, control proof, parity vector, and `experiments/gen32_crosscopy_walsh_composition_manifest.json`.

This is a finite counterexample to this cross-copy coupling rule, not a theorem about every noncommuting or nonorthogonal composition.

## Finite completeness obstruction for a shared exterior block

Generation 33 implements the sole selectable Fable survivor only through its preregistered completeness gate. For label `t in {0,...,7}`, define

`v(t)=(1,t,t^2,t^3)`

and use the six Plücker coordinates of `v(t) wedge v(t+1)`, ordered as `(01,02,03,12,13,23)`. These are distinct integral decomposable bivectors; each exactly satisfies

`p01*p23 - p02*p13 + p03*p12 = 0`.

For a clause-sign vector `s in {-1,+1}^9`, a global assignment selects one tag per clause and produces the shared exterior point

`p(a)=sum_c s_c tag(label_c(a)) in Z^6`.

The experiment checks all 512 sign rules in fixed lexicographic order. Equal completeness with an arbitrary rational center `c` would require the 16 points to be cospherical. Relative to point zero, this is the exact linear system

`2(p_i-p_0).c = ||p_i||^2-||p_0||^2`,  `i=1,...,15`.

For every sign rule on the matched satisfiable control, the coefficient matrix has rank 4 and the augmented matrix rank 5. The same `(4,5)` result holds for all 512 obstruction rules. Therefore no rational—or real—center and common radius exists in this frozen Euclidean exterior factor. Representative integral left-kernel certificates are emitted; for the all-negative control rule, the first three equations combine with coefficients `(1,1,-1)` to give nonzero right pairing `1985168`.

The best zero-centered control sign rule still has squared-norm spread 9,340,400 among honest encodings. The candidate therefore fails before a CVP target, matched completeness radius, coefficient shell, or one/two-copy soundness ratio can be defined. `experiments/verify_exterior_bivector_completeness.py` checks the exhaustive sign audit and `experiments/gen33_exterior_bivector_completeness_manifest.json`.

This is a finite rejection of this exact Vandermonde-bivector/sign family, not a general obstruction to exterior-algebra Grams.

## Exact infeasibility of the positive-definite exterior-metric repair

Generation 34 implements the sole authorized Fable survivor as a completeness-only feasibility problem. It retains the eight Generation-33 bivectors and all 512 clause-incidence sign rules. The proposed repair asks for one rational symmetric `6x6` metric `G`, shared by the control and obstruction, with separate centers/radii and

`trace(G)=1`,  `G-(1/100)I >= 0`.

For one formula, let `p_0,...,p_15 in Z^6` be its honest exterior fingerprints. Equal squared radius under `G` means

`p_i^T G p_i - 2 p_i^T h + rho = 0`

for some `h=Gc` and scalar `rho`. Thus the quadratic-value vector must lie in the column space of the 16-by-7 matrix with rows `[1,p_i]`. If `alpha` is any exact affine dependency, `sum_i alpha_i=0` and `sum_i alpha_i p_i=0`, then every feasible metric satisfies

`sum_i alpha_i p_i^T G p_i = 0`.

These are homogeneous rational equations in the 21 upper-triangular Gram entries. For each sign rule, the verifier forms 11 dependency rows from the control and 11 from the obstruction. The combined row space has rank 10. Exhaustion of all 512 rules yields one identical RREF, with pivot columns

`[6,7,9,10,11,13,14,18,19,20]`.

In upper-triangle order, column 6 is diagonal coordinate `(1,1)`, and the RREF contains its unit row. Hence every metric satisfying both equal-sphere systems obeys exactly

`G[1,1]=0`.

But `G-(1/100)I` positive semidefinite implies every diagonal entry of `G` is at least `1/100`. This contradiction is an exact algebraic/facial-reduction certificate; trace normalization cannot repair it. No numerical SDP tolerance is involved.

`experiments/verify_exterior_metric_repair_infeasible.py` checks every sign rule and `experiments/gen34_exterior_metric_repair_manifest.json`. Since completeness is infeasible, no rational factor, CVP target, or soundness shell is emitted. This is a finite rejection of this repaired tag family, not a theorem about arbitrary equal-radius Grams.

## Exact two-level parity cut for an incidence-orbit metric family

Generation 37 implements the sole authorized Pro survivor as a bounded exact cutting-plane test. The frozen feature family contains the G31 anchor and Walsh rows in orthogonal copy-local blocks and every G32 within/cross-copy degree-at-most-three residual row. Assign nonnegative squared weights `alpha,beta` to anchor and Walsh blocks, require

`72(alpha+beta)=1`,

and retain residual squared weight 100. Thus every satisfying control has squared radius 1 for one copy and 2 for two copies. The selector Gram has base eigenvalue

`4alpha+8beta >= 1/18`,

and the emitted two-copy row norms give the uniform upper bound `Q<=275416 I`.

Use the fixed one-copy G11/G13 parity witness from the exact Generation-32 search. Its feature components are

`anchor=96`, `Walsh=120`, `residual^2=0`,

so its cost throughout the family is

`W_1=96alpha+120beta`.

Place compatible copies of this parity in the two overlapping instances. Every shared proper moment is preserved, so all 125 cross-copy residual rows vanish. Its components are exactly

`anchor=192`, `Walsh=240`, `residual^2=0`,

and hence

`W_2=192alpha+240beta=2W_1`.

Therefore a proposed soundness margin requiring all two-copy NO vectors to have cost at least `2W_1+delta` has the exact valid cutting plane

`delta <= W_2-2W_1 = 0`.

No numerical optimization or incomplete attack list can overcome this explicit unrestricted integer vector within the frozen composition rule. For a fully emitted rational representative, choose `alpha=beta=1/144`. The factor is `(1/12)[2I;F]` together with residual factor `10A`. Exact control minima are 1 and 2; the one-copy obstruction minimum is `3/2`, and the compatible two-copy vector costs 3. Coefficient intervals through those thresholds are `[-3,3]` and `[-4,5]`.

`experiments/verify_twolevel_metric_parity_cut.py` checks the component identities, exact rational factors/targets, eigenvalue bounds, and `experiments/gen37_twolevel_metric_parity_cut_manifest.json`. This finitely kills the normalized orthogonal incidence-orbit family only; it is not a certificate for unrestricted PSD metric synthesis.

## Finite splitter-bag shell pass

Generation 38 implements the sole authorized Pro survivor. Among all 3/4-subsets of the nine clauses, the separating requirement is: for every nonempty support `S` of size at most four and every `i in S`, some bag intersects `S` exactly in `{i}`. A deterministic set-cover MILP checks 210 candidates and 837 requirements and returns minimum cardinality 12. The emitted family is the fixed lexically refined collection

`012, 034, 056, 078, 135, 147, 168, 238, 246, 257, 367, 458`.

For each bag, introduce one unrestricted integral selector for every assignment to its variable union satisfying every clause in the bag. Emit one normalization row per bag and, for every pair of bags, every complete marginal equality on their shared variables. The fixed-target objective is

`||2z-1||^2 + 25||Az-b||^2`.

The obstruction has 117 selectors and the control 119; both have 980 checks. A satisfying control assignment gives one legal selector per bag and zero residual, attaining the universal odd-anchor lower bound 119.

For the obstruction, 11 of 12 bags contain all four variables. Between each pair of these bags, the emitted marginal rows are the 16 coordinatewise global-assignment equalities. For any fixed assignment, if its 11 integral coefficients are not all equal, their all-pairs squared difference is at least 10. Consequently raw residual square at most two forces all 11 full bag distributions to coincide.

The legal supports of the 11 full bags have empty intersection: collectively their clauses cover every global assignment. Their common distribution must therefore be zero. But each of the 11 normalization rows then has residual `-1`, contradicting raw residual square at most two. Thus every vector that could approach the declared shell has raw residual square at least three. Since

`25*3 = 75 > 64`,

there is no unrestricted obstruction vector through `B+64=181`. The anchor shell gives coefficient interval `[-3,4]`. The projected Generation-13 affine vector has breakdown `(anchor,residual^2,total)=(333,262,6883)`, and all-zero DROP costs 417.

`experiments/verify_splitter_clause_bags.py` checks the family, full factor/target manifest, control, attacks, and `experiments/gen38_splitter_clause_bags_manifest.json`. This is a finite shell pass only; no polynomial-size splitter construction, relative-gap recurrence, or hardness theorem follows.

## Target

Prove a deterministic polynomial-time many-one reduction from 3SAT to Euclidean GapCVP with approximation factor n^c for an explicit absolute c>0, without PCP and without unproved conjectures.
