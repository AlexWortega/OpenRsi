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

## Finite counterexample: diagonal signed flow survives a complete ordered-pair lift

The goal-directed Generation-1 experiment freezes a linear `k=2` realization of Strategy 1 on the hash-verified Generation-19 width-5 program. Its coordinates are every ordered pair of same-layer transitions, both unary transition marginals, all four branch-pair totals per queried variable, and both unary branch distributions. It emits pair and unary source, conservation, and ACCEPT rows; complete transition/query marginal rows; and the strong same-path equations setting off-diagonal transition pairs to zero and each diagonal pair equal to its unary marginal. Odd anchors give the universal integral lower bound `R_2^2=n=224282`.

Let `s` be the exact Generation-19 accepting signed flow with two coefficients `-1`. The literal product `s tensor s` satisfies the flow and marginal rows but violates 14 strong diagonal rows. This does not rescue soundness: set each diagonal pair coordinate to `s_e`, every off-diagonal pair coordinate to zero, and both unary marginals to `s`. Put the corresponding binary query totals on their diagonal patterns. This `diag(s)` vector is integral, reaches `(ACCEPT,ACCEPT)`, and satisfies all 348,451 emitted equations exactly. It has six negative coordinates across the pair and unary levels, hence anchor excess 48 and squared cost

`E_2 = 224282 + 48 = 224330`.

A matched satisfying control has an honest diagonal path at the anchor lower bound, so its exact squared radius is `R_2^2=224282`. Exact integer comparisons give

`3E_2 < 4R_2^2` and `9E_2 < 16R_2^2`.

Therefore this finite lift fails both the weaker `4/3` squared test and the displayed `k=2` FRONTIER requirement `(4/3)^2=16/9`. `experiments/verify_k2_barrington_tensor_splice.py` reruns the unrestricted G19 low-weight seed search, hashes every emitted row, and checks both witnesses. No exact `k=2` optimum or general impossibility theorem is claimed.

## Finite counterexample: a bicyclic unit defeats the A5 fusion tile

Generation 2 freezes the sole authorized Fable survivor. A fusion tile has 3,600 unrestricted integral selectors `z[g,h]`, `g,h in A5`. Two child tiles have all four leaf marginals fixed; their product marginals are equated by emitted rows to the root left/right marginals, and the root product is equated to the hash-locked G19 ACCEPT 5-cycle. Three normalizations and all 420 port equations are emitted. For `C=[aI;bA]`, the objective is

`a^2||2z-1||^2+b^2||Az-rhs||^2`.

In `Z[A5]`, choose the verifier's lexicographically first involution `g` and element `h` for which

`x=(1-g)h(1+g)`

has four distinct terms. Associativity gives `x^2=0`. Hence `u=1+x` and `v=(1-x)ACCEPT` obey `uv=ACCEPT`. Exact sparse child couplings realize product ports `u` and `v` while both marginals of each child remain `delta_e`. Their outer-product root coupling has left/right marginals `u,v` and product `delta_ACCEPT`. This is an unrestricted integral vector satisfying every emitted NO row.

The two children have 2 and 3 negative coefficients, and the root has 12, so the zero-residual depth-two cost is

`E_NO <= (10800+8*17)a^2 = 10936a^2`.

The matched control uses honest leaves `(e,e,e,ACCEPT)` and three one-hot tiles, attaining the universal anchor lower bound `R^2=10800a^2`. Therefore

`32 E_NO <= 32*10936a^2 < 33*10800a^2 = 33 R^2`.

The residual scale `b` cannot charge this vector. The verifier checks all 144 pairs `1<=a,b<=12`, exact group convolution, all 423 rows, the matched control, the absence of a Boolean zero-residual NO vector, and the coefficient shell `[-5,6]`. Thus the frozen tile cannot meet the `33/32` gate. No exact NO minimum or theorem about arbitrary group-algebra gadgets is claimed.

## Finite obstruction: D4 triality legal shells contain malformed midpoints

Generation 3 implements the sole repaired Pro survivor through its mandatory geometry gate. Scale the three `D4` 24-cell triality classes to integral subsets of `2D4*`: vector vertices `+-2e_i` and the even/odd half-spinor classes represented by sign vectors in `{-1,1}^4`. Each Boolean value is an antipodal pair. Assign the three classes to the two inputs and output, and use

`Q=I+tS`,

where the three symmetric off-block `4x4` blocks are signed scalar identities and `t=p/q`, `|p|<=16`, `1<=q<=16`. Exact Sylvester inequalities retain only positive-definite `Q`.

For any positive-definite quadratic form and center `c`,

`||(x+y)/2-c||_Q^2 = (||x-c||_Q^2+||y-c||_Q^2)/2 - ||x-y||_Q^2/4`.

The legal COPY representatives `p000` and `p111=-p000` are distinct antipodes. If they have common squared radius `R^2`, their midpoint zero is a coefficient-lattice point of strictly smaller cost. It is malformed rather than a Boolean port. For NAND, legal representatives `p011` and `p101` have midpoint `(0,0,output-1)`: antipodality cancels both input blocks, while the common output block remains. This point also lies in `(2D4*)^3`, is outside the Boolean codebook, and has cost strictly below the common legal radius.

`experiments/verify_d4_triality_midpoint_obstruction.py` enumerates all 3,072 class/orientation labelings and 952 retained Gram parameters, compressed exactly into eight cross-dot signatures, for 2,924,544 candidates. Exact minimum inward deficits are `3/4` for COPY and `17/4` for NAND. Consequently no candidate can have the required empty legal Delaunay shell or outside-codebook certificate; depth-two `65/64` transfer testing is not authorized. This is not a theorem about other Voronoi geometries.

## Finite obstruction: non-antipodal D4 NAND shells contain a false port

Generation 4 performs the sole bounded mutation authorized by both reviews. Each of the three scaled `D4` triality classes supplies an ordered distinct non-antipodal truth pair. All class assignments and the frozen symmetric Gram family `Q=I+tS` are retained exactly when `Q` is positive definite.

Write a Boolean port representative as

`p(a,b,c)=p000+a*da+b*db+c*dc`.

For any center, its squared `Q`-distance is a quadratic pseudo-Boolean function

`q(a,b,c)=k+la*a+lb*b+lc*c+A*ab+B*ac+C*bc`,

where `A=2<da,db>_Q`, `B=2<da,dc>_Q`, and `C=2<db,dc>_Q`. If the four legal NAND words `001,011,101,110` all have squared cost `R^2`, eliminating the linear terms gives exact false-port excesses

`q000-R^2=-A+B+C`,
`q010-R^2=-A+B`,
`q100-R^2=-A+C`,
`q111-R^2=A`.

`experiments/verify_nonantipodal_d4_nand_obstruction.py` enumerates all 663,552 labelings and groups them, with a checked hash, into 43 sufficient interaction signatures. Combining these with 952 positive-definite Gram parameters covers 631,701,504 candidates through 40,936 exact rational tests. In every test the minimum of the four displayed excesses is nonpositive. It is negative for 528,417,792 candidates and zero for 103,283,712; the maximum achievable minimum is exactly zero.

Thus any candidate with equal legal radius has a false Boolean lattice point on or inside that radius. A candidate lacking such a center fails completeness already. No member of this grid reaches the empty-shell prerequisite, so COPY, gluing, and depth-two `65/64` tests are not authorized. This is not a no-go theorem for other codebooks or Gram families.

## Finite obstruction: coordinate recombination defeats independent D4 couplings

Generation 5 tests the sole cross-review survivor. Replace the common triality coupling by

`Q=K(x,y,z) tensor I4`,

with unit diagonal and independent `x,y,z in {-7/16,...,7/16}`. All 3,375 matrices in this box are positive definite. Exact Boolean-signature enumeration finds 24,344,064 label/Gram candidates whose four false NAND ports are strictly farther than the equal legal Boolean radius; the best minimum false excess is 3. Thus the independent mutation genuinely escapes the Generation-4 Boolean obstruction.

It cannot produce an empty lattice shell. Consider legal points `p001=(a0,b0,c1)` and `p011=(a0,b1,c1)`. A non-antipodal pair `b0,b1` in any triality class differs in at least two coordinate positions. Pick one changed position and define `h` by replacing that coordinate of `b0` with its value in `b1`; define `h'` by the complementary replacement in `b1`. Both are in `2D4*`, distinct from both Boolean labels.

Because `Q` has no cross-coordinate terms, at every coordinate the unordered pair of local triples for `(a0,h,c1),(a0,h',c1)` equals that for `(a0,b0,c1),(a0,b1,c1)`. Hence for every center

`E(a0,h,c1)+E(a0,h',c1)=E(p001)+E(p011)`.

If the two legal points have common squared radius `R^2`, the right side is `2R^2`, so at least one malformed hybrid has cost at most `R^2`. Strict inequality gives an interior point; equality gives an extra shell point. Either defeats the required exact legal shell.

`experiments/verify_independent_d4_recombination_obstruction.py` covers 2,239,488,000 candidates via 145,125 exact signature/Gram tests and checks the recombination certificate for every one of the 144 oriented class pairs. This rejects the frozen grid, not nonseparable Grams or arbitrary Voronoi tiles.

## Finite obstruction: the E6 Gosset shell has no bounded NAND port map

Generation 6 tests the sole authorized Fable survivor. In a simple-root basis, the `E6` lattice has Cartan Gram determinant 3. The Weyl orbit of a minuscule fundamental weight has 27 points. Translating one orbit point to zero gives integral vertices, rational center

`c=(2,1,0,-1,-2,0)/3`,

and common squared radius `4/3`.

This shell is certified globally. If `v=z-c` has `v^T A v<=4/3`, dual Cauchy–Schwarz gives

`v_i^2 <= (4/3)(A^-1)_{ii} <= 8`.

Since every center coordinate has magnitude at most `2/3`, integer `z` lies in `[-3,3]^6`. Exact enumeration of all `7^6=117649` points finds precisely the 27 Gosset vertices, all at radius and none inside.

Now let an affine port map have linear part `M in {-1,0,1}^{3x6}`. Translate the target relation so the zero vertex maps to one legal word. Across all per-port relabelings and legal-base choices there are 32 translated NAND relations. Every coordinate of each relation takes exactly two values, `{0,1}` or `{0,-1}`. Therefore every row of `M` must take values in one of those pairs on all 27 vertices.

The verifier exhausts all `3^6=729` rows. The zero row is the only admissible one, and it takes only one value. Hence no three-row map can hit all four legal words; this covers all `3^18=387420489` maps exactly. The Delaunay geometry passes, but complete legal port classification fails before COPY or transfer closure. This finite result says nothing about larger map entries or other irreducible Delaunay cells.

## Exact finite-shell no-go: every rational affine E6 binary row is constant

Generation 7 removes the coefficient bound from the certified 27-vertex `E6` shell. The translated vertices affinely span `Q^6`; equivalently, their augmented vectors `(v,1)` have rank seven. Hence any rational affine row

`f(v)=r dot v+b`

is uniquely determined by its values on seven affinely independent vertices.

The verifier chooses a deterministic affine basis and enumerates all 128 assignments of values in `{0,1}`. It solves every interpolation system exactly over `Q` and evaluates the result on all 27 shell vertices. For 126 assignments, an explicit vertex has value outside `{0,1}`. The remaining assignments are all-zero and all-one, producing only the two constant affine rows.

Any affine three-port map whose image lies in a four-word NAND relation must have each component binary-valued after independent sign/translation relabeling. Constants remain constants under those operations. Exhausting all eight triples of surviving rows yields singleton images, while each of the 32 translated/relabelled NAND relations has four words and both values in every coordinate. Therefore no rational affine projection of this shell realizes NAND.

`experiments/verify_e6_unbounded_affine_port_no_go.py` checks rank, all exact systems, hashed rejection certificates, and all row triples. This is a complete no-go for rational affine ports on one finite Delaunay shell, not a statement about nonlinear ports, other cells, recursion, or GapCVP hardness.

## Exact finite obstruction: the bounded extended Gram cannot charge DROP

Generation 8 implements the only repaired Fable survivor at its first soundness gate. The frozen rank-eight tile has four canonical one-hot columns with NAND ports `001,011,101,110` and four auxiliary columns with port zero. Its affine quadratic energy is represented by

`H=[[Q,-h],[-h^T,s]]`,

with every entry of `H` bounded in absolute value by 64. Every legal one-hot selector is required to have squared energy 64.

For the unrestricted coefficient vector `z=0`, all `Q` and `h` terms vanish and

`E(0)=[0;1]^T H [0;1]=s`.

The emitted linear port is `000`, a false NAND word, so the `65/64` gate requires `E(0)>=65`. The entry bound instead gives `s<=64`. The two constraints sum to the exact contradiction `0>=1`. Strict diagonal dominance or positive semidefiniteness only lower-bound `s` and cannot alter this obstruction.

`experiments/verify_augmented_gram_drop_obstruction.py` checks the port map and exact rational inequalities. No candidate Gram exists in this normalized family, so COPY, closure, and depth-two growth are not reached. Rescaling or changing the target-entry bound defines a different family and remains open.

## Finite counterexample: a grade-zero affine class defeats the canonical F289 gate

Generation 11 tests the sole repaired Pro survivor. Let the eight selector columns be indexed by Boolean triples. Emit normalization, the three complete port marginals, one zero row for each false NAND label, and the linearized product value `ab+c-1`. Work over

`F_289=F_17[u]/(u^2-3)`.

The legal columns are `001,011,101,110`. Their augmented `4x4` normalization/port matrix has determinant one. Therefore every Boolean boundary has a unique integral affine representation using legal columns, and adjoining the four forbidden unit rows makes the full integer system saturated. In particular,

`111 = -001 + 011 + 101`

with coefficient sum one. This selector has one coefficient `-1`, every emitted residual zero, and anchor energy 16 for the eight coordinates. Analogous energy-16 witnesses exist for false `010` and `100`; false `000` costs 32.

The witnesses use only base-field coefficients, so the `F_289/F_17` Frobenius fixes them. They remain degree-zero classes under the proposed skew grade-one recurrence. A nonzero element of the maximal-order prime above 17 has reduced norm at least 17 and trace energy at least 34. Hence the zero-defect false witness of energy 16 violates the intended depth-one adverse-filtration dichotomy.

`experiments/verify_f289_nand_affine_grade_zero_attack.py` checks field arithmetic, all emitted rows, exact field rank, all four unique integer witnesses, Frobenius invariance, and the energy comparison. This kills only the canonical selector template, not arbitrary quaternion modules or the general ramified frontier.

## Finite depth-one survivor: a redundant eight-coordinate NAND code

Generation 12 tests the sole surviving proposal at the smallest authorized rank. Let four legal NAND configurations be binary codewords in `Z^8`; each coordinate is one of 16 four-bit signatures. Exhaustive multiplicity search, with exact maximal-minor saturation, finds a best code with rows

`0001, 0010, 0110, 0110, 0110, 0110, 0110, 1001`.

Choose the four distinct signature rows as an active unimodular minor. Emit four equations defining duplicate coordinates from the active coordinates, followed by normalization and the three Boolean port equations. The resulting integral `8x8` matrix has determinant one. Thus each boundary fiber contains exactly one unrestricted integer vector. Honest codewords are binary and have anchor energy 8. The exact false-boundary energies for `000,010,100,111` are

`160, 64, 56, 56`.

The arithmetic threshold is independently realized. In the definite quaternion algebra with `i^2=-3`, `j^2=-17`, use the order basis

`1, (1+i)/2, (j+ij)/2, (i+ij)/3`.

The verifier checks multiplication closure and trace Gram determinant `17^2`, hence maximality. The left and right ideals generated by `j` coincide; right multiplication has determinant `17^2`. The induced prime-ideal trace Gram has a dual bound confining vectors of energy at most 34 to `[-1,1]^4`; exact enumeration finds minimum nonzero energy 34.

Therefore the finite candidate satisfies `min_false=56>=34` and `56/8>17/16`. `experiments/verify_redundant_signature_nand_survivor.py` also exhausts all 490,314 rank-eight multisets and records 13,457 local survivors. This is not a COPY construction, composition theorem, adverse-filtration lemma, or asymptotic hardness result.

## Current finite transducer obstruction and formal conditional lemma

The cross-review-surviving mutation seeks a complete residue transducer with integer edge gains and a potential `phi` satisfying a local inequality. The needed seed condition is a nonzero leading `P`-class for every adverse fiber.

For the only emitted redundant NAND map, that condition fails. Exact inversion of its determinant-one `8x8` matrix gives zero emitted residual for false boundaries `010`, `100`, and `111`, with selector energies 64, 56, and 56. The false-`111` selector is

`(0,1,2,2,2,2,2,-1)`.

For every saturated binary-signature affine COPY multiset of ranks 2–8, the legal `11` selector can be placed between two copies of this adverse selector. Both glue orientations have zero affine, boundary, and seam residual; total squared energy is `112+N`, hence 114–120. `experiments/verify_redundant_nand_grade_zero_seed.py` and `experiments/verify_quaternion_copy_diagonal_splice.py` certify these finite statements. They reject the frozen affine defect and glue, not every quaternionic lift.

The universal proof-side implication is available. `lean/Verify_transducer_potential.lean` proves that if every allowed transition satisfies

`p <= q*weight(x,y) + phi(y) - phi(x)`,

then the inequalities telescope on every finite walk. If `lo <= phi <= hi`, the formal cross-multiplied bound is `p*length-(hi-lo) <= q*totalGain` (and gives the usual lower bound when `q>0`). It also proves `2^depth < 17^gain` whenever `gain>0` and `depth<=4*gain`. These theorems do not provide a transition system, lumpability, or a certificate for the current tile.

## Product-tag rectangle lemma and enlarged-kernel obstruction

For pair selectors `z[j,k]`, row- and column-only affine tags annihilate the alternating rectangle. An ordered product tag instead gives

`a0*b0 + a1*b1 - a0*b1 - a1*b0 = (a0-a1)*(b0-b1)`.

`lean/Verify_product_tag_rectangle.lean` proves this identity without commutative multiplication and proves that, in a division ring, its value is nonzero exactly when both label pairs differ. The criterion remains true after applying a fixed ring automorphism to the right labels. This formally validates local separation of one rectangle.

Local separation is not closure under signed sums. In the frozen `4x2` specialization with labels `a=(0,1,u,1+u)`, `b=(0,1)`, all six old rectangles and the false-`111` coefficient vector have nonzero leading tags. Nevertheless, exact enumeration of `{-1,0,1}^8` finds

`(-1,1, 1,-1, 1,-1, -1,1)`,

whose four row margins, two column margins, and both product-tag coordinates vanish exactly over `Z[u]/(u^2-3)`. Its squared coefficient weight is 8, and its only conformal zero-tag submoves are zero and itself. `experiments/verify_product_tag_enlarged_kernel.py` certifies this finite kernel statement.

There is also a structural residue-dimension obstruction. Since `F_289` is two-dimensional over `F_17`, any three proposed leading symbols have a nonzero `F_17` linear dependency. `lean/Verify_three_transfer_kernel.lean` proves this by a finrank/kernel argument. For a concrete distinct asymmetric `8x8` labeling, `experiments/verify_product_tag_rectangle_kernel.py` lifts such a relation to two independent rectangle directions with centered coefficients `(2,-1)`. The resulting integer table has zero row and column sums and zero leading product transfer modulo 17; its squared coefficient weight is 12 and support is 6.

These statements do not show that the movements satisfy extra equations of an unspecified full NAND/COPY tile, nor that their coefficient weights equal Euclidean CVP energies. They do prove that checking each old primitive separately is unsound and that bare all-pairs margins plus one `F_289` leading coordinate cannot separate all combinations of three surviving independent rectangle directions. Q1 still requires a fully emitted matrix, complete enlarged Graver audit, exact legal energy, DROP and malformed fibers, and lift/carry checks.

## Finite full-factor attack on the margin-only product seam

Generation 4 asks whether the certified pair movement survives a serialized candidate and remains below the local threshold. No maximal-order `O/P^2` fusion tile was supplied, so the implemented candidates are explicitly limited to the smallest completions determined by the current NAND, COPY, pair-margin, and product-tag data.

The breaker serialization has 18 unrestricted integer variables: eight NAND selectors, two COPY selectors, and eight `4x2` pair selectors. Its non-anchor matrix emits the determinant-one NAND and COPY modules, all physical row/column margin equations, and both integer coordinates of the product tag. For each COPY orientation the matrix is `22x18`; adjoining `2I` anchors gives a `40x18` CVP factor. Every legal pair cell is binary and has squared energy

`E=18`.

The pair movement

`g=(-1,1,1,-1,1,-1,-1,1)`

has zero image under every non-anchor row in both orientations. Exhaustion of all `{-1,0,1}^8` pair movements finds only `g` and `-g` as nonzero kernel moves in that box, and a support-submove audit shows `g` is conformally primitive. For each of the 16 legal cell/orientation fibers, one sign produces a malformed pair selector with unchanged residual and total squared distance

`42 < 306 = 17E`.

Exact shell enumeration covers all 25,856 pair selectors of pair anchor energy at most 32. `experiments/verify_product_tag_full_lift_attack.py` checks the matrices, factor/target hashes, shell, residuals, energies, and primitivity. `experiments/verify_product_tag_full_seam_lift.py` uses a related decoded-state margin serialization with a `36x18` factor and independently obtains the same energy 42 in every legal fiber. These are finite counterexamples to those margin-only completions, not to an unspecified tile with additional pair-dependent rows.

The accompanying universal statement is formal. `lean/Verify_single_transfer_lift_obstruction.lean` considers three integrally independent integer seam directions annihilated by every non-transfer row. Since one leading symbol lies in `F_17^2`, a residue dependency exists. Balanced representatives give integer coefficients in `[-8,8]`, squared coefficient weight at most `3*64=192`, and a nonzero combined movement annihilated by every non-transfer row and by the leading transfer modulo 17. The theorem does not assert that the required directions survive any omitted full-tile equations or that coefficient weight controls the full CVP energy.

## Multi-channel transfer capacity and physical-selector counterexample

A direct sum of product channels repairs the Generation-4 pair-only dimension defect on the frozen seam. Let each channel contribute two `F_17` coordinates through one `F_289` product table. Exhaustive synthesis over left labels in `{0,1,u}` finds two channels whose transfer has rank three on the three-dimensional `4x2` zero-margin transportation space. The old movement

`(-1,1,1,-1,1,-1,-1,1)`

has new syndrome `(1,0,16,16)`. Exact same-margin enumeration checks 7,152 pair selectors below `17E=306`; no malformed selector has zero two-channel syndrome. `experiments/verify_multichannel_product_shell.py` certifies this finite restricted pass.

The full serialized factors still fail at lower weight. Every appended transfer row is supported only on the eight pair selectors. Keep the pair table fixed and flip one physical NAND/COPY selector of a legal vector. Its anchor contribution remains unchanged because both 0 and 1 have odd-anchor energy one. The physical consistency residual has squared norm 2, while every transfer residual remains zero. Therefore the total squared distance is

`18 + 2 = 20 < 306 = 17E`.

`experiments/verify_multichannel_physical_flip_attack.py` checks all channel prefixes `r=1,2,3,4`, both COPY orientations, eight legal cells, and ten physical Hamming-one flips: 640 exact candidates in 64 fibers. Every fiber has such a malformed zero-vector-transfer attack. This is a finite counterexample to the four unscaled 18-variable channel-prefix factors, not to a candidate with different physical rows, scaling, or a supplied maximal-order construction.

The algebraic capacity statement is formalized in `lean/Verify_multichannel_transfer.lean`. For a division ring, componentwise transport `x_i -> u_i*x_i*v_i` with nonzero `u_i,v_i` preserves and reflects whether the entire syndrome is zero. Hence an injective additive syndrome detects every nonzero defect after transport. For residue channels represented as `Fin r -> Fin 2 -> ZMod 17`, the exact finrank is `2r`; injectivity requires defect finrank at most `2r`, while a larger defect space forces a nonzero syndrome-kernel element. These theorems are conditional and do not establish rank-one label realizability, Q1 energy, or Q2 carry stability.

## Marked Beneš switch obstruction and integral-isometry lemma

The retired transfer frontier is replaced by a proposed fixed-brick higher-Lawrence compiler. Generation 6 tests the only surviving local mechanism: use a width-four Beneš network so every permutation is realized by one fixed matrix, with switch settings encoded in targets and with physical/anchor columns marked.

In the breaker's pair-linearized switch, the coordinates for each of two ports form a `2x2` table indexed by switch setting and bit. Add the same alternating rectangle

`(1,-1,-1,1)`

to both tables. Every table normalization and marginal is unchanged, and the two product changes cancel in the COPY/SWAP output equations. Hence the combined support-eight movement

`g=(1,-1,-1,1,1,-1,-1,1)`

has exact zero image under the full `54x76` emitted matrix. Exhaustion of all 6,560 nonzero local vectors in `{-1,0,1}^8` proves minimum kernel support eight and leaves only `g` and `-g`; support-submove enumeration proves conformal primitivity.

More strongly, the movement is an honest affine collision:

`g = h(0,0,0) - h(0,1,1) - h(1,0,0) + h(1,1,1)`.

The coefficients sum to zero. Therefore any linear detector required to vanish on all honest affine differences also vanishes on `g`. For all 24 routed permutations and 16 input words, one sign gives a malformed zero-residual vector. Legal energy is 76 and attack energy is 92 or 108. `experiments/verify_benes_switch_toric_exchange.py` certifies these finite statements. They kill only this frozen pair-linearized brick.

The builder's distinct local serialization has 142 columns and 136 rows, including physical `0/1/DROP` states, six switches, two NAND gates, outputs, and transfer auxiliaries. All 384 legal encodings have energy 142. Exact local search finds six weight-eight switch primitives, and 5,832 physical Hamming-one/two movements are nonkernel. At residual squared scale 25, however, the zero vector has energy

`142 + 25*22 = 692 < 17*142 = 2414`.

Thus explicit DROP kills this scale before any depth-2/3 structural inference. `experiments/verify_marked_benes_local_audit.py` checks the serialization and hash.

The marking correction is formal. `lean/Verify_integral_euclidean_isometry.lean` proves first that an integer vector of squared norm one has exactly one nonzero coordinate, equal to `+1` or `-1`. It then proves that a square integer matrix with orthonormal columns—or equivalently Gram matrix identity—is a signed permutation matrix. Consequently arbitrary unimodular column equivalence cannot preserve selector support and Euclidean energy; L1 must use signed color-preserving permutations on semantic columns and explicitly transport any residual Gram. This theorem does not provide the missing compiler induction.

## Quadratic-character switch lemma and equal-radius counterexamples

For Boolean switch state `(a,b)`, define

`q(a,b)=(1,(-1)^a,(-1)^b,(-1)^(ab))`.

This local mutation correctly escapes the zero mixed derivative of affine marks. `lean/Verify_quadratic_character_switch.lean` proves

`q(0,0)-q(0,1)-q(1,0)+q(1,1)=(0,0,0,-2)`,

proves every honest word has squared norm 4, proves the four words are integrally linearly independent, and proves that wire swap is the marked coordinate transposition of the two linear characters.

The breaker finds a different signed-affine failure. The normalized selector

`z=(-1,1,1,0)`

has coefficient sum one and image

`-q(0,0)+q(0,1)+q(1,0)=(1,-1,-1,1)`.

This is not one of the four honest codewords, but its squared mark norm is again 4. Its binary-anchor energy is 12, compared with 4 for a one-hot selector. Exhausting `{-1,0,1}^4` finds 12 normalized malformed selectors, minimum support three, and exactly three equal-radius ghosts. For each integer mark scale `m=0,...,64`, `experiments/verify_quadratic_character_ghost.py` chooses the least normalization scale making the zero selector cost at least `17E`. The ghost remains exactly normalized and has energy `12+4m^2`, still below `17(4+4m^2)` in every tested case. This is finite evidence for those 65 scales, not a universal scale theorem or a full-brick result.

The three-COPY serialization shows a compositional failure at one fixed scale. It has 44 columns and 74 rows, with three COPY selectors, physical `0/1/DROP` selectors, straight/swap/swap orientations, transport of all four characters, one NAND, output and transfer selectors, normalization, glue, and DROP auxiliaries. Complete search of `{-1,0,1}^{12}` finds only the two signs of the minimum support-12 movement

`(1,-1,-1,1)` repeated at all three cycle vertices.

A proper-support audit proves conformal primitivity in the full frozen matrix. Character changes cancel around the cycle. For each honest state, one sign reflects the quadratic coordinate at every node without changing its magnitude. Consequently malformed and legal squared energies are both 885. The zero/DROP vector costs 120,000, which is above `17*885=15,045`, and 882 physical Hamming-one/two changes are nonkernel. `experiments/verify_quadratic_character_copy_cycle.py` certifies these finite statements.

Thus nonzero mixed derivative, local integer independence, common honest radius, and marked routing do not imply signed-selector soundness or cycle closure. Any L1 candidate using this orbit must explicitly charge all three local ghosts and the synchronized cycle movement while retaining equal legal energy.

## Support-minor plumbing, finite separator evidence, and a degeneracy control

The current frontier U0 concerns structural nonmembership in four known fixed-template convex integer-optimization classes. Generation 8 tests only a support-graph mechanism; it does not establish Euclidean soundness.

For a matrix `C`, let `G(C)` be its bipartite row/column support graph and let `D=[I|-C]`. `lean/Verify_support_minor_channel.lean` formalizes these graphs and proves three universal facts:

1. the row vertices and original `C` columns induce exactly `G(C)` inside `G(D)`;
2. each identity-column vertex is a leaf attached to its row;
3. an equality expansion with a surjective collapse, internally connected collapse fibers, and an edge lift for every old edge yields an explicit branch-set minor model of the old graph.

Thus identity augmentation and any expansion carrying this exact certificate cannot erase a minor-monotone obstruction already present in `G(C)`. The file does not formalize treewidth or any target matrix class.

The builder freezes a finite surrogate. For `S` in `{8,16,32}`, `C_S` is the union of matchings

`j=i`, `j=3i+1 mod S`, and `j=5i+2 mod S`.

Its support graph is 3-regular bipartite. Independent exact MILP formulations using HiGHS and CBC give minimum top-level `2/3`-balanced vertex-separator sizes

`4, 6, 9`.

The values grow strictly and meet the preregistered finite bound `separator >= S/4`. Subdividing every edge once and contracting each auxiliary to its right endpoint reconstructs the original graph. An independent exact signed audit searches 654,384 defects modulo global sign, through support six for `S=8,16` and support four for `S=32`; every recorded detector image energy is at least its support. `experiments/verify_gen8_affine_detector_separator.py` certifies these finite facts. It does not compute the hereditary recursive separator profile and does not serialize U1.

The breaker tests a distinct control family to expose what support growth cannot prove. Let `C_n` be lower-triangular cumulative ones. Then `D_n=[I|-C_n]` contains a support `K_{n/2,n/2}`. Nevertheless, `z=e_{n-1}` gives a total support-two kernel vector, adjacent differences give `n-1` support-three kernel vectors, and multiplying rows by the unimodular difference matrix changes the presentation to `[U|-I]`, whose incidence graph is a tree. `experiments/verify_gen8_separator_kernel_degeneracy.py` verifies this at `n=8,16,32` and exhausts `z` of support at most two with coefficients `+/-1`.

The control does not refute the affine surrogate and does not show that its row rebasing is allowed by U0. It does show that a large support subgraph alone neither controls signed kernel vectors nor yields an equation-basis-invariant obstruction. U0 still requires a frozen actual serializer, precise transformation grammar, hereditary lower bound, and a proved template-dependent upper bound for each target class.


## Failure of raw U0 invariants and the serializer-first repair

The former U0 proposed ordinary marked neighborhood diversity or a displayed
support separator as a certificate that `[I|-C]` cannot have a fixed-template
n-fold, generalized n-fold, tree-fold, or two-stage presentation.  Neither
raw quantity supplies that inference.

For the fixed one-by-one n-fold template `A_1=A_2=[1]`, let `C_n` have one
all-ones global row and an `n x n` identity local block.  This is literally a
standard fixed-template n-fold matrix.  Its bipartite support is a subdivided
star, hence a tree.  Adding one identity leaf at each row to form `[I|-C_n]`
still gives a tree.  Nevertheless standard color-aware twin classes do not
identify the repeated bricks: at `n=8,16,32`, exact neighborhood-diversity
counts are `17,33,65` for `C_n` and `26,50,98` for `[I|-C_n]`.  The latter
has exact `2/3`-balanced separator one and a width-one leaf elimination.
`experiments/verify_gen8_neighborhood_diversity_nfold_counterexample.py`
checks the matrices, all twin classes, the tree certificates, separator
certificate, and faithful edge subdivisions.  Therefore ordinary marked
neighborhood diversity is not bounded by a fixed n-fold template.

This is not merely a finite accident of n-fold notation.  In
`lean/Verify_two_stage_neighborhood_counterexample.lean`, the canonical fixed
two-stage matrix `A=B=[1]` has one common first-stage column and one private
second-stage column per scenario.  The theorem
`same_row_neighborhood_iff` proves for every `n` that two scenario rows have
the same open neighborhood exactly when their indices agree.  Thus at least
`n` distinct row-neighborhood types occur in one fixed two-stage template.

A displayed support separator is better behaved under permutations and the
connected-fiber equality expansions already formalized, but not under an
invertible change of equality basis.  This matters because left row rebasing
does not change coefficient feasibility or the Euclidean coefficient
objective.  `lean/Verify_row_rebasing_kernel.lean` proves exactly that if
integer matrices `U,V` satisfy `VU=I`, then

`ker_Z(U D) = ker_Z(D)`.

The support failure is universal and systematic.  Let
`C_n(i,j)=1[j<=i]`.  Before rebasing, `[I|-C_n]` contains the complete
biclique between the lower `m` rows and first `m` C-columns when `n=2m`.
`lean/Verify_row_rebasing_support_failure.lean` proves that integral first
differences and prefix sums are mutual inverses, and that first differences
send

`[I|-C_n]` to `[B_n|-I]`,

where `B_n` is lower bidiagonal.  Every rebased row has support at most three,
every right column is a leaf, and every left column meets at most its matching
row and successor.  Thus arbitrarily large raw biclique witnesses can be
artifacts of the displayed equation basis.

The complementary finite verifier
`experiments/verify_u0_fixed_nfold_support_counterexample.py` begins with the
literal fixed n-fold matrix above.  Cumulative unimodular row presentations at
`n=8,16,32` have complete-bipartite supports `K_{9,8}`, `K_{17,16}` and
`K_{33,32}`, with exact `2/3`-balanced separators `6,11,22`.  Multiplication
by the explicit first-difference inverse returns the fixed n-fold matrix.
This does not say that the eventual systematic universal-circuit factor has
such a rebase; it shows why an alleged tractability exclusion must quantify
over semantic row preprocessing.

Consequently former U0 is retired as a roadmap edge.  It mentioned an
“actual” factor that had not been serialized and did not define marks,
uniform fixed-template quantifiers, equality gadgets, or the four separate
class grammars.  The replacement is ordered correctly: U0a first emits and
hash-freezes the actual factor and precise transformation grammar; after U1
exists, U0b must use a row-basis-invariant marked column-matroid connectivity
or branch-width profile and prove one class bound at a time.  No nonmembership
of the Generation-8 affine surrogate or a future actual factor is asserted
here.


## A finite universal-topology factor and the right-basis obstruction

The U0a reroute now has a genuine finite factor family at three frozen widths.
The serializer uses `L=2 log_2 W+2` repeated butterfly stages.  Every source
node has selectors for FREE/FIX0/FIX1 values; every later node has complete
truth selectors for COPY_A, COPY_B, NAND, ZERO and ONE.  Program rows select a
mode through target bits, while numerical matrix entries remain fixed.  Edge
rows compare both child inputs to the prescribed butterfly parents.  Dyadic
separator rows are materialized exact sums of edge rows.  Normalization rows
charge DROP, and an identity row for every selector places coefficient energy
inside the ambient y-objective.

`experiments/verify_u0a_universal_topology_serializer.py` emits all row and
column metadata and every nonzero entry of `C` and `D=[I|-C]`.  At widths
8,16,32, the C shapes are `1976x1312`, `4924x3264`, `11784x7808`; D shapes are
`1976x3288`, `4924x8188`, `11784x19592`.  Three explicit programs at each
width satisfy all nonphysical coordinates, and `D(Cz,z)=0` exactly.  Since the
physical target is zero and one selector is chosen per node, common squared
energies are `72,176,416`.  Canonical JSON files are hash-frozen in
`experiments/artifacts`.  These finite checks prove neither universality nor a
compiler for arbitrary formulas. Indeed, `verify_u0a_frozen_depth_obstruction.py` proves the explicit failure: gate depth is only `8,10,12`, while dependency chains with `9,11,13` NAND gates require more distinct stages.

The local affine obstruction persists in controlled form.  Four COPY_A states
at one node satisfy the rectangle relation on normalization, program, input,
output, edge, separator and acceptance features.  The physical identity rows
alone see the movement.  Adding it to the matching honest state produces
`[1,0,-1,1]`; exact energies become `74,178,418`, only two above the respective
honest values.  `verify_u0a_serialized_gate_kernel_cheat.py` checks the actual
matrices and all 256 affine/constant rectangles at width eight.  This is a
localized defect for U2/U3, not by itself a NO-instance counterexample.

The semantic grammar also needs right-basis closure.  If `Q` is unimodular,
then `C` and `CQ` generate the same embedded lattice.  This is formalized in
`lean/Verify_right_unimodular_lattice_image.lean`, including equality of the
attainable values of every objective that depends only on the ambient lattice
vector.  Thus a tractability exclusion cannot freeze the supplied coefficient
basis.

This invalidates the initially proposed column-matroid repair.  With
`C=I_2` and `Q=[[1,1],[0,1]]`, exact rational enumeration gives circuits
`{(0,2),(1,3)}` for `[I|-C]` but
`{(0,2),(0,1,3),(1,2,3)}` for `[I|-CQ]`; the circuit-cardinality multisets
differ, so the matroids are not isomorphic.  Larger cumulative bases keep the
lattice `Z^n` while changing one fundamental circuit from support two to
support `n+1`.  The finite verifiers certify both statements.
`lean/Verify_column_matroid_grammar.lean` correctly proves invariance only
under left rebasing and column permutation, so it remains a grammar lemma but
cannot establish U0b.

The active mathematical object for any future exclusion is therefore the
embedded lattice `C Z^n` together with its ambient Euclidean objective.  A
basis-independent decomposition width and four fixed-class bounds remain
open.  Before that, U0a must turn the finite topology into a total canonical
`Serialize(S,F)` and prove formula compilation and polynomial bounds.


## Parameterized butterfly formula compilation

The finite universal-topology factor can be repeated to arbitrary declared
depth.  With width `w` and depth `d`, four source selector states per lane and
twenty gate states per location give

`k=4w+20wd`.

Counting normalization, program, edge, dyadic separator, output and physical
rows gives

`m=30wd+9w-2d`.

`lean/Verify_u0a_serializer_dimensions.lean` proves these identities and the
bounds `k<=24(w+d+1)^2`, `m<=39(w+d+1)^2`, and
`m+k<=63(w+d+1)^2`.  It also proves that canonical strict-chain placement
exists exactly when the chosen depth is sufficient.  Thus polynomially many
repeated stages remove the earlier finite chain blocker.

The offset schedule alternates each hypercube dimension twice.  Exact switch
DP shows that default width eight is one useful routing layer short: only
18,688 of 40,320 permutations occur.  Adding the ninth scheduled stage gives
all permutations.  Two full cycles are exhaustively rearrangeable for widths
four and eight, and reversal programs satisfy the actual factor.  These are
finite facts, not a general Beneš theorem.

The deterministic formula compiler maintains a register assignment to lanes.
To create repeated variable occurrences it copies one FREE source along a
hypercube edge.  To combine two live tokens it swaps along a shortest
hypercube path until they are adjacent, applies NAND to one output, and zeros
the consumed register.  After postorder evaluation it pads to
`4w(log_2 w)^2+2log_2 w` stages and applies a final cleanup: only the root lane
is copied and every other output is ZERO.  Consequently all assignments to a
given formula use one fixed target with root bit one and other output bits
zero.

`experiments/verify_u0a_butterfly_formula_compiler.py` verifies this against
complete serialized matrices for all 100 ordered two-variable formula trees
with two through four leaves and all 400 assignments, plus one branching
8-leaf formula at width eight.  Repeated-variable witness
`((x0 NAND x1) NAND (x0 NAND x1))` is explicitly included.  Every evaluation
matches the recursive Boolean semantics; satisfying assignments meet every
nonphysical target, false assignments differ only in the root output row;
`D(Cz,z)=0` and exact energies are checked.

This is the right finite mechanism for U0a, but campaign discipline forbids
promoting the generic Python implementation to a universal theorem.  The next
proof obligation is a Lean induction covering token-map invariants, COPY
fanout, swap routing, NAND evaluation, cleanup targets, and polynomial
emission.  Moreover completeness alone gives no hardness: false honest
assignments cost only one above the physical baseline, and unrestricted signed
selectors remain unaudited.


## Universal postorder semantics and the recursive-emitter obstruction

Let a NAND formula be either a variable or an ordered pair of formulas.  The
semantic compiler emits one `read x` instruction for a variable and concatenates
left code, right code and one `nand` instruction at an internal node.  The
executor is a total Boolean stack machine.  In
`lean/Verify_nand_formula_compiler.lean`, the append law for execution enables
structural induction proving

`run (compile F) assignment stack = eval(F,assignment) :: stack`

for every formula, assignment and initial stack.  Since all `read x`
instructions use one assignment function, repeated occurrences are consistent.
A compiled assertion contains only code and a desired root bit; execution hits
that fixed target exactly when recursive evaluation does.  Compilation has
exactly one instruction per syntax node.

This theorem establishes semantic compilation but not physical butterfly
realization.  The finite canonical manifest supplies the current bridge at
S=4.  It encodes variables as `["V",i]`, NAND as `["N",a,b]`, and rejects any
noncanonical byte string.  Fixed S determines all padding and numerical factor
data before F.  Complete reconstruction checks the systematic matrix, and
formula/assignment audits prove only declared target rows vary.

The physical scheduler has been exhaustively tested on every ordered shape and
variable-equality partition through eight leaves.  Packed truth tables avoid
assignment enumeration in the 1,901,166-case core.  No token collision,
semantic error or padding overflow occurs.  This cannot replace induction.

The former recursive implementation was not total on a legal 1,101-leaf
right-deep formula.  Generation 13 repairs traversal, evaluation, canonical
encoding and scheduling with explicit stacks.  The historical verifier retains
the old recursive walk only as a regression; the current dry-run path succeeds.
Full emitted factors remain a separate streaming obligation.

## Abstract fresh-register trace

The stack semantics can be refined without choosing a routing network.  In
`lean/Verify_nand_register_compiler.lean`, an abstract register instruction is
one of `load(dst,x)`, `copy(dst,src)`, or `nand(dst,left,right)`.  A canonical
postorder SSA compiler allocates one consecutive register to every syntax
node, putting the parent after both children.  For a formula `F` compiled at
`base`, Lean proves the exact destination-list identity

`map dst (compileRegsAt F base) = map (base+·) (range F.nodes)`.

Thus the trace has `F.nodes` operations, every destination is fresh, and its
write footprint is precisely contained in `[base,base+F.nodes)`.  Execution
from an arbitrary initial register file preserves every register outside that
interval and stores `eval(F,assignment)` in `base+F.nodes-1`.  Every operand of
every emitted instruction is at least `base` and strictly older than its
destination.  Standalone theorems additionally show that a LOAD reads the
global assignment and that a COPY or NAND appended at a fresh register
preserves its older sources.

This is a machine-independent SSA invariant, not yet the physical compiler.
The canonical formula trace uses LOAD and NAND; COPY is provided as the
verified fanout primitive but is not yet inserted or routed by this compiler.
No theorem here maps these abstract operations to butterfly stages, serialized
factor rows, Euclidean energy, or unrestricted signed soundness.


## Iterative dry-run repair and eager-emission boundary

The repaired compiler maintains the same stable postorder token IDs with an
explicit work stack.  A dry-run scheduler performs all swaps, duplications and
NAND placement but does not allocate the padded stage-by-lane mode grid.  It
frames and hashes every unpadded event and represents padding by its exact
count.  The old 1,101-leaf witness now schedules in a fraction of a second and
reports the same deterministic trace hash on rerun.

The abstract physical bridge is strengthened by
`lean/Verify_nand_register_compiler.lean`.  Its SSA compiler assigns syntax
nodes to consecutive fresh natural-number registers.  Lean proves exact
destination order, freshness, write confinement, preservation outside the
allocated interval, older operands and correct root evaluation.  Verified
COPY/NAND extension lemmas model fanout and gate computation before choosing
butterfly lanes.

Complete numerical emission is still eager.  At S=16 the count model already
has 493,440 ambient rows and 330,304 selector columns.  The resource verifier
places only its child under a 256 MiB virtual-memory cap: dry scheduling passes,
whereas complete `serialize` raises `MemoryError`.  The construction remains
polynomial and could stream its sparse triples; the counterexample concerns
this Python object graph, not CVP reducibility.  A valid total implementation
must stream canonical program modes, C triples, D identity/negative-C triples
and target coordinates while hashing them, then prove the stream matches the
SSA/lane trace.


## Canonical sparse factor emission

A sparse factor need not exist as a Python list.  The canonical emitter walks
row families in the same order as the eager serializer and sends each COO
triple directly to a hash/count sink.  Systematic D is emitted in one pass:
for each row output its identity triple, followed by the sign-negated C triples
with the coefficient-column offset.  Row and column metadata and target values
are streamed analogously.

At S=4 every emitted object equals the eager object entry by entry.  At S=16
the stream contains 4,457,168 C records and 4,950,608 D records but retains no
matrix triple.  A 256 MiB child completes with low measured RSS.  This repairs
the earlier eager-factor MemoryError for the audited instance.

The universal algebraic kernel is
`lean/Verify_sparse_coo_stream.lean`.  Dense materialization sums all records
at a coordinate.  Lean proves an invariant for online fold accumulation at
each row, then derives equality with ordinary matrix multiplication.  Hence
chunking or permuting records preserves the represented linear map.

Program data remains eager.  Even a two-leaf formula at S=128 creates over
three million `(stage,lane)->mode` dictionary entries, causing the certified
256 MiB failure.  The construction's natural sparse description is much
smaller: most stages are COPY_A, padding is a count, and only swap/duplicate/
NAND/cleanup events override defaults.  Completing U0a requires a canonical
stream for these overrides and a proof that target program rows read exactly
the implied mode at every stage/lane.


## Sparse program and target emission

Most cells of the formula-oblivious padded program are COPY_A.  The sparse
encoding stores a default and only stage/lane deviations created by swaps,
duplications and NAND events.  A padding interval inherits COPY_A without any
records.  The final cleanup stage instead has default ZERO and a single COPY_A
at the root.  Source lanes default FIX0 with FREE overrides; output bits default
zero with the asserted root override.

Streaming lookup reconstructs the full logical mode grid in stage-major order
and emits five one-hot GATE_PROGRAM target rows per cell.  Exact finite tests
compare this reconstruction to the former eager program, its canonical hash
and every target coordinate.  At width 256, more than sixteen million logical
cells are hashed under 256 MiB without retaining the grid.

The universal representation theorem is
`lean/Verify_sparse_program_overrides.lean`.  It proves eager dense lists and
sparse lookup agree pointwise.  Under strict key ordering, overrides are unique
and select their recorded modes; absent keys select the default.  Summing
one-hot target rows gives one per cell and the total number of cells globally.

This still falls short of a reduction theorem.  The sparse event generator's
lane-token invariant is implemented but not formalized, and the complete
large factor stream is not practically consumed in the width-256 audit.  A
Lean bridge must show each SSA LOAD/COPY/NAND operation is realized by the
emitted sequence of sparse overrides and corresponding edge/program/output
rows.

## Honest lane semantics for butterfly events

The physical stage semantics is now formalized in `lean/Verify_butterfly_lane_semantics.lean`. Each lane uses its own previous bit as port A and the bit at its current XOR neighbor as port B. XOR neighbors are involutions. The exact sparse event mode patterns are proved to realize their abstract effects: SWAP exchanges adjacent endpoints; DUPLICATE copies a source into an adjacent free destination and preserves all other lanes; NAND+ZERO writes the NAND at the first endpoint and clears the consumed second endpoint; WAIT and padding are identity; final cleanup retains only the root lane. A universal induction theorem equates execution of any locally valid scheduled physical trace with execution of its abstract lane events.

This is a semantic bridge, not the full compiler theorem. In particular it assumes event-by-event adjacency and neighbor involution rather than deriving them from the Python scheduler, and it is limited to honest Boolean gate evaluation. It proves no statement about the serialized Euclidean factor, selector integrality, adverse vectors, CVP soundness, or approximation gap.


## Honest sparse events realize butterfly lanes and streamed rows

For a fixed physical stage, lane i has A-parent i and B-parent its XOR
neighbor.  `lean/Verify_butterfly_lane_semantics.lean` assigns the exact
serializer truth table to COPY_A, COPY_B, NAND, ZERO and ONE.  Under the local
adjacency conditions, it proves:

- all COPY_A is identity;
- COPY_B at both endpoints swaps their values;
- COPY_B only at a destination duplicates the adjacent source;
- NAND at the output and ZERO at the consumed lane performs the compiler gate;
- cleanup retains the root and zeros every other lane.

An induction then equates physical and logical lane states for every valid
scheduled event trace.

The finite numerical bridge instantiates this semantics inside actual factors.
For each assignment it derives the selected source/gate state and its exact
column index.  Streaming row by row, normalization and selected program modes
are one; edge and separator syndromes vanish; output rows equal cleanup values;
physical rows equal selector coefficients.  The paired vector `(Cz,z)` has
zero moment in every streamed systematic D row.  Honest energy is the node
count plus one only when the asserted root is false.

An independent verifier regenerates C coefficients from the local truth table
and scheduled XOR offsets.  Exhaustion through five leaves and deliberate
mutations shows that shifting the stage dimension, replacing XOR by modular
addition, making COPY_B read A, or dropping the fanout override is detected.
The result is finite, while the lane-event theorem is conditional universal.
The next proof must show the compiler-generated event trace satisfies that
condition and that its token-to-column map realizes these row identities for
all formulas.


## Valid-by-construction XOR events and independent token certificates

The conditional physical-trace theorem can be specialized to the actual
butterfly grammar.  A smart event records dimension d and one endpoint; the
other endpoint is generated by XOR with `2^d`.  Lean proves XOR neighbor is an
involution without fixed points.  Hence every generated SWAP, duplicate and
NAND+ZERO event has distinct adjacent endpoints, and every generated trace
satisfies the physical/logical equivalence theorem without an external
validity hypothesis.

The Python certificate creates a separate producer/checker boundary.  It is
serialized to JSON and parsed back before validation.  The checker reconstructs
the formula's postorder demands, replays every WAIT/SWAP/DUPLICATE/NAND token
transition, and verifies the flattened nondefault overrides.  From the
certificate and an assignment it selects actual local truth-state columns and
projects the canonical C stream.  Thus normalization, program, edge, separator,
output and physical equations are checked without reusing the compiler state.

This is finite evidence of the Python-to-Lean correspondence.  Moreover the
certificate's complete token-map snapshots are too expensive: a 1,025-leaf
comb exceeds 256 MiB.  Since replay naturally maintains its own map, a delta
certificate can preserve independent verification with much smaller storage.
The universal theorem still must connect the concrete emitted delta sequence
to Lean XorEvents and then to streamed row equations.


## Snapshot-free event delta certificates

Full before/after token maps are unnecessary.  Certificate v2 records formula
tables, one initial map, each event's physical stage/dimension/endpoints/modes
and semantic tokens, and one final map.  An independent verifier reconstructs
the current map.  SWAP exchanges every token at its endpoints; DUPLICATE adds
the declared new token in a free adjacent lane; NAND deletes its children and
adds its output.  Event order and flattened mode overrides must match the
program stream exactly.

The 4,097-leaf resource test demonstrates the representation repair: more than
84,000 events fit below 256 MiB, where v1 full snapshots already failed at
1,025 leaves.  Mutation tests show that missing/reordered events, map
collisions, omitted overrides, wrong tokens and substituted checkpoint states
are rejected.

`lean/Verify_event_delta_replay.lean` abstracts this checker.  Applying an
ordered sparse delta is a fold of function updates.  If the next delta equals
the advertised logical transition at the state produced so far, induction
proves the entire replay equals logical execution.  A certificate needs only
initial state, event deltas and claimed final state.  This theorem must still
be instantiated with the concrete XorEvent token-map semantics and then linked
to numerical selected columns.


## Concrete explicit token deltas

Certificate v2 allowed the checker to derive token changes from event semantics;
v3 emits the same changes explicitly in the generic Lean representation.  A
one-sided SWAP writes one token's new lane, a two-sided SWAP writes both;
DUPLICATE writes the new token; NAND erases its two operands and writes its
fresh output.  Applying an event delta removes changed old tokens first, then
checks all destination lanes are free before inserting non-null values.

The independent v3 checker derives the expected list from its current map and
requires exact ordered equality.  This catches changes that preserve mode rows
but corrupt token ownership, including a consistently inserted empty-empty
physical SWAP.  Resource behavior remains linear enough for the 4,097-leaf
capped audit.

`lean/Verify_concrete_event_deltas.lean` gives a matching universal theorem.
Its validity predicate states exact lane occupants, destination freeness,
token freshness and distinctness.  Under these premises, each canonical list
is extensionally equal to the logical global-map transition.  Induction gives
snapshot-free final-map correctness.  The next theorem must show the concrete
formula scheduler establishes these premises and finite-width bounds at every
step.


## Finite-width butterfly and token-occupancy invariants

A stage dimension below k flips one of the low k bits.  Mathlib's XOR bound
shows this maps every lane below `2^k` back below `2^k`.  In
`lean/Verify_butterfly_finite_width.lean`, the map is therefore defined on
`Fin (2^k)` itself.  It is involutive and fixed-point-free.  Smart finite events
synthesize their partner endpoint with this map, making out-of-range and
nonadjacent pairs unrepresentable.

The token delta theory now proves exclusive occupancy is stable.  WAIT does
nothing; SWAP applies an injective lane involution; DUPLICATE uses a free lane
and fresh token; NAND consumes two distinct tokens before reusing one freed
lane for a fresh output.  These facts compose over every valid concrete trace.
For finite token types, active-count theorems give 0,0,+1,-1 changes for
WAIT,SWAP,DUPLICATE,NAND respectively.

A boundary audit tests the concrete serializer on formula sizes immediately
below, at and above a power of two.  Every lane and delta remains inside its
chosen width.  Mutations setting a lane or dimension to its exclusive bound,
forging width, breaking XOR adjacency or reintroducing snapshots are rejected.
The missing theorem is no longer local routing arithmetic; it is structural
correctness of the Python scheduler's sequence of swaps, duplicate allocations
and postorder NAND consumption.

## Target

Prove a deterministic polynomial-time many-one reduction from 3SAT to Euclidean GapCVP with approximation factor n^c for an explicit absolute c>0, without PCP and without unproved conjectures.
