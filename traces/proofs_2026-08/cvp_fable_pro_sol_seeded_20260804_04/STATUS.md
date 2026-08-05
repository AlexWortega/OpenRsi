# Status

**Outcome:** PARTIAL CONSTRUCTION DIAGNOSTICS ONLY; no progress on goal ladder (a)–(c).

## Generation 16 update

Only Fable proposal 5 survived as a bounded experiment. `experiments/verify_adversarial_matroid_fold.py` solves the canonical all-functional integer row-selection ILP on every dimension-four reduced code, covering nine YES and 195 NO dictionaries. Every optimum has rank 64 and distance 16, so the uniform ratio is one. Larger hostile codes expose the construction wall directly: all-eight dimension 25 requires 33,554,431 candidate rows and 16,777,216 pointed constraints. The exact ILP route is killed as a scalable construction; this is finite evidence and explicit size accounting only.

## Generation 13 update

Only Fable proposal 2 survived as a bounded experiment. `experiments/verify_a4_convolution_fold.py` implements the frozen four-probe `A_4` ordered-pair convolution map. Across ten YES, 200 NO, twenty affine-closure, all-eight, and holonomy dictionaries, worst YES is 20 and best NO is 10 at exact-transfer rank 48. Canonical all-eight has a pointed kernel, as do 28,800 of 40,320 adversarial label assignments. The frozen quasirandom fold is killed; this is finite evidence only.

## Generation 8 update

Only Pro proposal 2 survived as a bounded experiment. `experiments/verify_polar_shortening.py` applies the frozen 64-coordinate Arikan/Möbius transform and exact star-zero shortening. Across ten YES, 200 NO, twenty affine-closure, all-eight, and eight-coordinate holonomy instances, worst YES is 13 and best NO is zero; 3 YES, 38 NO, 5 affine-closure, and all-eight images have pointed kernels. The frozen polar rule is killed. This is finite evidence only.

## Generation 6 update

The strongest surviving bounded experiment was proposal 2's frozen two-sided `F_8` rank-condenser fold. `experiments/verify_f8_two_sided_condenser.py` exactly attacks ten YES, 200 NO, twenty affine-closure, all-eight, and holonomy dictionaries. It finds no pointed kernels, but worst YES is 31 and best NO is 6 at exact-transfer rank at most 48, so the ratio is `6/31` and the rank exponent is zero. The five-block family is killed by support flattening; this is finite evidence only.

## Generation 5 update

The strongest surviving bounded experiment was Pro proposal 2's fully specified rank-one `M_3(F_4)` ordered-pair fold. `experiments/verify_f4_ordered_pair_fold.py` exactly attacks ten YES, 200 NO, twenty affine-closure, all-eight, and holonomy dictionaries and constructs each binary syndrome image. The frozen rule fails: worst YES 3, best NO 0, maximum exact-transfer rank 4, and rank exponent zero. There are 112 NO pointed kernels, 18 affine-closure kernels, and a holonomy pointed kernel. The tested canonical noncommutative family is killed; no general asymptotic claim is made.

## Generation 4 update

Only Pro proposal 3 survived opponent review as a defined bounded experiment. `experiments/verify_nonsemisimple_multiplication_fold.py` implements the frozen `F_2[u]/(u^16)` multiplication map and exactly attacks every mixed image word on ten YES, 200 NO, all-eight, and twisted-holonomy dictionaries. The result is negative: worst YES distance 4, best NO distance 2, uniform ratio `1/2`, and zero rank exponent versus the unfurled `0.2447428`. All-eight contains a pointed kernel word of moving weight zero. The tested rule is killed; this is finite evidence only.

## Generation 2 update

Only Pro proposal 7 survived opponent review. `experiments/verify_nonbacktracking_schur_walks.py` implements its explicit partial Schur lift and exhausts every mixed image word. On ten YES and 200 deterministic exact NO `q=3,m=8` dictionaries, the precommitted length-4 map has worst YES 3, best NO 33, ratio 11, maximum nominal pointed length 1277, and finite exponent `0.3352636`, above the base `0.2324868`. The script enumerates 103,136 mixed words and checks relabeling covariance on 846,721 permutations/tests.

This is **FINITE** progress only. All-eight and twisted-holonomy diagnostics contain illegal affine mixed words of costs 6 and 9 whose walk features cancel completely. No bounded-incompatibility-degree reduction or polynomial walk-count theorem is known for logarithmic length, and no asymptotic soundness lemma follows.

## Generation 1 update

Only Pro proposal 2 survived opponent review. The smallest frozen modular-Kronecker fold experiment is implemented in `experiments/verify_sparse_pit_tensor_fold.py`. It exactly enumerates 24,084 mixed image words across 35 precommitted rules and ten YES/ten NO `q=3,m=8` codes, while checking all 806,400 coordinate relabelings. The unfurled finite ratio is `25/9`; no folded rule preserves a uniform ratio above one, and none beats the unfurled rank exponent. The precommitted five-modulus rule has worst YES 17 versus best NO 5. The tested family is falsified; this is not a theorem about arbitrary code-dependent folds.

## Completed phases

1. Read all required prior obstruction artifacts and distilled `ORACLE_BRIEF.md`.
2. Seeded `IDEAS.md` with inherited autopsies, exact fine-print assumptions, and tested mutations.
3. Ran two classical-literature scouts and distilled `LITERATURE.md`. No prohibited material was used; one off-limits hit was reported discarded unread by a scout.
4. Ran the first IDEATE consultation with map + literature + idea population attached.
5. Implemented and exactly attacked the top two construction sketches.

## Construction A — exact-cover + relative quotient: wounded

`experiments/verify_exchange_quotient.py` exhaustively enumerates small 3DM incidence fibers, perfect matchings, bounded packing exchanges, and quotient classes.

Verified outcomes over 120 instances (20 NO instances with nonempty odd-cover fibers):

* 66 YES instances contain an illegal odd cover in a matching's class modulo 2↔2/3↔3 packing exchanges.
* 32 contain an illegal odd cover in the **minimal affine span of all perfect matchings themselves**.
* Lightest examples have weight 5 versus matching weight 3.

Thus any linear quotient identifying all legal witnesses also identifies all their odd affine combinations, some illegal. A relative-distance shell cannot charge an illegal point already in the legal class. The broad route survives only with a new mutation: affine-closed/canonical legal witnesses or separately protected legal sectors.

## Construction B — odd-cyclic tensor fold: promising finite signal, major gaps

`experiments/verify_cyclic_tensor_fold.py` explicitly builds the diagonal-orbit XOR fold and exhaustively enumerates **all mixed image words**.

Across 120 deterministic `ell=3` folds:

* no violation of the sharper `delta_fold ≥ 1+ceil((delta^2-1)/3)` was found;
* 37/100 natural invariant codes lost distance relative to full tensor distance `delta^2`, often down to the orbit-count scale;
* phase-replicated cases retained `delta^2`, but replication spends the compression factor and gives no free asymptotic gain.

The mixed-word lower bound is now proved generally for any odd group acting freely off the distinguished coordinate: symmetrization converts orbit parity into an invariant full tensor word, giving `delta_fold ≥ 1+ceil((delta^2-1)/ell)`. An invariant pointed minimum word attains equality. This is a genuine coding lemma, but not a reduction. A further theorem in `proof_cvp.md` treats natural **residual-lineage OF-only propagation** from a `Q` versus `Q+1` certificate, assuming nonempty invariant moving support: if fixed/cross sectors remain fixed under the next inherited action, then `N_k≥3^(2^(k-1))` while the propagated certified ratio is at most `N_k^(3/(Q ln 3))`. Its exponent vanishes as `Q→∞`; this is not a no-go for stronger base soundness. `experiments/verify_residual_fold_parameters.py` checks 14,773 exact recurrence transitions.

A follow-up classical scout found fresh symmetry through biset/bimodule composition, which lies outside residual lineage. The coordinate-level construction was implemented in `verify_pointed_biset_cross.py`: over 54 exact products, the new action is free except on `[u,*]` classes, exactly `1+R_U` of them.

A direct reduced-product mutation removes both star-cross sectors while retaining the corner and moving-moving block. This now has a proof: if `d=delta_*(D)-1`, reduced pointed tensor distance is exactly `1+d^2` for all mixed words; an odd free-orbit fold has distance at least `1+ceil(d^2/ell)`. `verify_reduced_orbit_fold.py` checks 100 deterministic randomly generated reduced codes and 100 invariant folded codes. This bypasses the cross-sector recurrence. An explicit two-level residual assembly is now implemented in `verify_reduced_fold_3dm.py`: exact YES/NO moving distances evolve `9/15 → 27/75 → 243/1875`, so the ratio squares exactly, but lengths grow `25 → 193 → 12289`. This validates the mechanism while exposing the output exponent wall.

A non-invariant 'super-budget' mutation avoids multiplying the YES weight by the group order. Exact 3DM tests for `ell=3,5,7,11` retain the full squared distances 9 (YES) and 25 (NO), not the much smaller orbit floors. Two broader cyclic searches also found no nontrivial `ell>d>1` floor-attaining example. This is finite negative evidence, not a theorem.

## Construction C — cyclic correlation catalyst: positive finite mechanism, insufficient parameters

No background experiment remained to harvest. Exact dollar attribution could not certify the 40% construction floor, so quarantine was conservatively treated as binding. The next eight research actions were construction/implementation/exact attacks; afterward one protocol-required targeted classical scout was run and its sole exact mechanism was immediately implemented and attacked in Construction D.

`verify_cyclic_ideal_superbudget.py` exhausts 116 small binary cyclic ideals. All 94 nontrivial `ell>d>1` cases compress below `d²`; examples with `(ell,d,d')=(31,11,11)` compress 121 to 11. Directly applying cyclic closure to 3DM fails: `verify_cyclic_closure_3dm.py` checks 400 exact assemblies and every YES/NO transformed code has moving and folded distance one.

The tested mutation keeps the instance code intact and uses a separate cyclic ideal as a catalyst. A length-15, dimension-3 catalyst has odd distance five before and after correlation folding. For any pointed outer code of moving distance `d`, the folded catalyst construction has exact mixed-word distance `5d²`; this follows by tensor reassociation and pointed multiplicativity. `verify_cyclic_catalyst.py` checks 100 random small outer codes. On fixed 3DM instances, `verify_cyclic_ideal_3dm.py` gives YES `15→45`, NO `25→125`, so the ratio squares exactly.

A general parameter identity now closes pure tensor catalysts as gap amplifiers: output length `Ln²` and common distance multiplier `a` give new standard rank exponent `2log(b/d)/(2log n+log L)`, never above the base exponent. `verify_catalyst_exponent_bound.py` checks 17,151,060 tuples; the identity is proved in `proof_cvp.md`. The required tested-next mutation is asymmetric YES/NO multiplication or submultiplicative coordinate growth, not merely a better growing cyclic catalyst.

As a finite end-to-end transfer check, `verify_reduced_fold_cvp.py` converts the level-1 folded YES/NO codes into explicit rank-192 integer lattice bases in systematic Construction-A form. Exact affine enumeration and determinant/index checks give squared Euclidean distances 27 and 75, hence Euclidean ratio exactly `5/3`. This is a finite construction check, not asymptotic hardness.

The protocol-required asymmetric mutation was also tested. `verify_asymmetric_hash_fold.py` checks 866 valid formula-oblivious 1-/2-sparse folds on ten YES and ten NO reduced 3DM squares. Best uniform exponent is 0.0962, below the unfurled finite exponent 0.2447; cancellation usually collapses soundness. Code-dependent algebraic folds remain outside this test.

## Construction D — code-dependent column-type compression: tested and closed for the current ladder

`verify_code_dependent_type_fold.py` tests a deterministic, basis-invariant
generator-column-type puncture selected from the code alone.  It checks every
mixed word and coordinate-relabeling invariance on ten YES and ten NO reduced
3DM squares.  Budget two lowers the uniform finite gap from `25/9` to at most
`13/9`; no tested budget improves the standard rank exponent.

A fresh targeted classical scout then isolated exact parity-check parallel
simplification: one representative of each distinct nonzero syndrome column
preserves every affine coset minimum exactly.  This was immediately assembled
end to end in `verify_parity_type_tensor.py`.  It gives no compression:
YES and NO type counts both grow `8 -> 64 -> 4096`, while distances grow
`3 -> 9 -> 81` and `5 -> 25 -> 625`.

The failure is rigorous for this family, not just finite evidence.  A binary
parity-check matrix with kernel distance at least three has no zero or repeated
columns.  The BMT moving span has distance at least three, and reduced tensor
star-zero codes inherit distance at least nine by product distance.  Hence
every stage remains parity-check-simple.  Both generator-side approximate type
compression and parity-check-side exact type compression are now autopsied and
mutated as required.

## Construction E — feature shells and direct integer exact cover

Background harvest found no active process belonging to this run.  Because
construction-spend attribution was unavailable, quarantine was treated as
binding and this milestone used no oracle.

`verify_feature_shell_3dm.py` constructs explicit augmented syndrome systems
with objective `|x|+R|Fx|`.  It exhaustively attacks global pair projections,
deterministic sparse hashes, and hybrids over every odd cover in 40 YES and 40
NO tiny instances.  Across 45 choices the best uniform ratio is only `7/6`,
below the base `5/3`; the required hybrid mutation was tested and is worse.

`verify_integer_3dm_cvp.py` tests the explicit integer basis
`B=[I;MA]`, target `[0;M1]`, against signed coefficients.  Across 40 YES and
40 NO instances, squared minima are YES 3 and NO 5, 7, 9, or 13.  Generally,
`Az=1` implies `sum z_j=q`, so `||z||²-q=sum(z_j²-z_j)` is nonnegative and
even, with equality exactly for a Boolean perfect matching.  This proves only
an additive `q` versus `q+2` gap.

A fixed pair-projection target separates the tested fibers, but has `(q!)²`
possible values.  The required mutation is now implemented in
`verify_variable_pair_projection_cvp.py`: make the three projection tables
lattice variables constrained to equal the projections of `z`.  This is one
polynomial-size fixed-target basis and existentially includes every matching.
Exact signed search on 40 YES/40 NO instances gives squared norm 12 versus 14.
The construction is valid but still additive: every integer row-sum-one table
has norm at least `q`, so the three tables add a `3q` YES baseline.  Tested
block weights change constants only, reaching at best 49/33 for weight eight.

## Construction G — homogenized integer tensor, bounded mixed search

Following the scout's all-sublattices lead,
`verify_homogeneous_integer_tensor.py` builds
`L={(z,s):Az=s1}` for four tiny YES/four NO 3DM instances.  Exact bounded
search gives base squared norms 4 versus 6 or 8 and mixed tensor minima exactly
16 versus 36 or 64.

The required higher-rank mutation is now tested.
`verify_highrank_integer_tensor.py` constructs saturated Smith-form Z-bases
for six YES/six NO rank-three lattices and exhausts all `3^9` mixed
coefficient matrices: 4 versus 6 becomes exactly 16 versus 36.  However,
`verify_tensor_subdeterminants.py` kills the naive unrestricted
all-sublattices lemma.  Across twelve YES/twelve NO instances, both have
minimum short-direction norm 4, rank-two Gram determinant 12, and support 6,
because NO lattices contain short `s=0` kernel directions.  The pointed mutation is now exactly tested.
`verify_pointed_sublattice_diagnostics.py` restricts to sublattices where the
homogenizing functional is primitive.  On 20 YES/20 NO examples, rank-one
norm/support separate 4/4 versus 6/6 and rank-two Gram determinant/support
separate 12/6 versus 20/8.  A harvested wider search, reproduced by
`verify_highrank_tensor_C2.py`, exhausts `5^9` mixed matrices on three YES/three
NO lattices and again gives 16 versus 36.  `verify_pointed_rank3_coeff_bound.py` widens the search to 145 primitive
coefficient directions and at least 7,480 rank-two pairs per instance; the
same gaps persist on ten YES/ten NO lattices.
`verify_pointed_rank4_diagnostics.py` then checks 20 YES/20 NO rank-four
lattices, including 702 primitive-functional pairs and sparse mixed tensors;
the same 4/6, 12/20, 6/8, and 16/36 minima persist.  A focused CONVERGE pass then proved the rank-two theorem universally:
`det_Gr(K)>=4(q+2)` and support at least `q+5` for every primitive-functional
NO sublattice.  A general odd-minor bound is
`ceil((q+3)4^(r-1)/r!)`.  However, arbitrary-Euclidean pointed
multiplicativity is false by an explicit norm-4 tensor versus base squared
minimum 5.  Mod-2 coordinate distance does multiply exactly and certifies
`(q+1)^k` versus `(q+3)^k` squared norms for all mixed integer tensors, but no
submultiplicative rank compression is proved.

## Construction F — global determinant permutation dictionary

One targeted classical scout was followed immediately by construction.  The
determinant/common-basis polynomial has exactly permutation monomials and is a
genuinely global selector.  `verify_determinant_permutation_dictionary.py`
exhausts signed coefficient dictionaries at q=3 and every support-three trade
at q=4.  Coefficient-plus-table costs are legal/virtual 4/8 and 5/7; top
determinant state gives 2/4; all exterior compound states give 8/22 and 16/34.
The required all-compounds mutation was tested.

This does not yield a reduction.  An explicit linear determinant-monomial
dictionary has q! columns.  Succinct bounded-fan-in determinant evaluation
re-enters the proved tableau faults, while top/compound global states retain
short affine virtual permutations and growing completeness baselines.

## Construction H — exact weighted set-support tensor compression

The quarantine was treated as binding, so the next action was a construction.
For binary pure-power tensors, tuple coordinates with the same underlying set
are identical for every mixed word.  Keeping one subset coordinate with weight
`|S|! {r brace |S|}` preserves the full tensor Hamming distance exactly.
Binary expansion writes every weight as `O(log w)` integer squares, yielding
an explicit ordinary Euclidean CVP basis with polynomial-bit entries.

`verify_weighted_symmetric_cvp.py` checks 72 multiset-orbit cases and explicit
integer bases.  `verify_set_support_weighted_cvp.py` checks 100 stronger
set-support cases and tiny 3DM: length saturates at 255 while distances remain
`3^r` versus `5^r`.  `verify_function_type_weighted_cvp.py` tests the required
mutation merging equal Boolean product functions.  At 3DM code dimensions
2--6, tested type counts are 6, 20, 59, 251, 1158.

This is a genuine exact compression, including every mixed pure-power word,
and output is independent of tensor order after saturation.  But a rigorous
dimension wall closes it for general BMT instances:
`dim P_r(D)=sum_{j<=min(k,r)} binom(k,j)`, reaching `2^k-1` at `r>=k`.
`verify_pure_power_dimension.py` checks 448 random and increasing 3DM cases.
Any exact realization preserving all pure-power mixed words has at least this
rank.  If BMT dimension were logarithmic enough to make it polynomial, its
base fiber could itself be exhaustively decoded in polynomial time.  The
function-type mutation therefore cannot yield the target reduction.

## Construction I — compact weight-class compressor and computability attack

`verify_weight_class_compressor.py` constructs a weighted class coordinate for
each attainable fiber weight.  It exactly powers distance with only `m+2`
coordinates; on tiny BMT, `r=16` yields a ratio above 3500.  But producing the
class-`q` generator is equivalent to deciding whether a perfect matching
exists.  The tested polynomial counting/parity relaxation inserts class `q`
in NO as well and collapses the gap.  The compact nonlinear mechanism therefore
hides the NP-hard step and is killed after its required mutation.

## Construction J — sampled pure-power fold, initial signal and failed generalization

A deterministic code-dependent sampler discards most pure-power functions and
merges duplicates with Euclidean multiplicity weights.
`verify_sampled_pure_power_fold.py` found a finite ratio 7 on ten YES/ten NO
instances.  The required mutation froze that setting and expanded the family:
`verify_sampled_fold_generalization.py` checks 50+50 instances for each
`m=8,...,12` and coordinate permutations.  The ratio drops to at most 4/3 and
then to one or below.  The initial signal was overfitting; the sampled fold is
killed in this form after exact mixed-word search.

## Construction K — low-dimensional exact-power toy search

`verify_exact_power_polynomial_base.py` combines weighted exact powering with
small-dimensional BMT codes.  Finite q=3 toys show large exponents (best tested
rank proxy 3024, ratio 11.390625), confirming the construction arithmetic.
This cannot become an NP-hard asymptotic family: logarithmic code dimension
makes the affine fiber polynomially enumerable, while superlogarithmic
dimension makes exact compressed rank `2^k` superpolynomial.  The function
merge and sampled mutations were already tested, so this closes the toy signal
without a hardness claim.

## Files

* `ORACLE_BRIEF.md` — obstruction map and surviving openings.
* `LITERATURE.md` — classical machinery digest.
* `IDEAS.md` — current idea population with autopsies/mutations.
* `NOTES.md` — detailed attack log and budget accounting.
* `proof_cvp.md` — honest mathematical write-up.
* `experiments/verify_exchange_quotient.py`
* `experiments/verify_cyclic_tensor_fold.py`
* `experiments/verify_residual_fold_parameters.py`
* `experiments/verify_pointed_biset_cross.py`
* `experiments/verify_reduced_orbit_fold.py`
* `experiments/verify_reduced_fold_3dm.py`
* `experiments/verify_noninvariant_superbudget.py`
* `experiments/verify_noninvariant_random_codes.py`
* `experiments/verify_superbudget_3dm.py`
* `experiments/verify_cyclic_ideal_superbudget.py`
* `experiments/verify_cyclic_closure_3dm.py`
* `experiments/verify_cyclic_ideal_3dm.py`
* `experiments/verify_cyclic_catalyst.py`
* `experiments/verify_catalyst_parameters.py`
* `experiments/verify_catalyst_exponent_bound.py`
* `experiments/verify_reduced_fold_cvp.py`
* `experiments/verify_asymmetric_hash_fold.py`
* `experiments/verify_code_dependent_type_fold.py`
* `experiments/verify_parity_type_tensor.py`
* `experiments/verify_feature_shell_3dm.py`
* `experiments/verify_integer_3dm_cvp.py`
* `experiments/verify_variable_pair_projection_cvp.py`
* `experiments/verify_determinant_permutation_dictionary.py`
* `experiments/verify_homogeneous_integer_tensor.py`
* `experiments/verify_highrank_integer_tensor.py`
* `experiments/verify_tensor_subdeterminants.py`
* `experiments/verify_pointed_sublattice_diagnostics.py`
* `experiments/verify_highrank_tensor_C2.py`
* `experiments/verify_pointed_rank3_coeff_bound.py`
* `experiments/verify_pointed_rank4_diagnostics.py`
* `experiments/verify_pointed_tensor_theorems.py`
* `experiments/verify_weighted_symmetric_cvp.py`
* `experiments/verify_set_support_weighted_cvp.py`
* `experiments/verify_function_type_weighted_cvp.py`
* `experiments/verify_pure_power_dimension.py`
* `experiments/verify_weight_class_compressor.py`
* `experiments/verify_sampled_pure_power_fold.py`
* `experiments/verify_sampled_fold_generalization.py`
* `experiments/verify_exact_power_polynomial_base.py`

All listed new verifiers exit zero; deterministic logs are in `experiments/*.log`. The weighted-compression/dimension suite passes (`WEIGHTED_DIMENSION_SUITE_PASS`), the compact weight-class construction passes (`WEIGHT_CLASS_PASS`), the sampled-fold/generalization pair passes (`SAMPLED_FOLD_SUITE_PASS`), and the final low-dimensional toy check passes (`FINAL_TOY_PASS`).

## Honest assessment

A final hostile referee pass was incorporated; it corrected pointedness hypotheses, residual-theorem scope, biset-model quantifiers, exponent terminology, and 3DM parity accounting. No deterministic polynomial-gap NCP instance and no GapCVP reduction have been obtained. The relative-quotient candidate suffered a concrete affine-closure failure. Two one-step mixed-word lemmas, a complete finite two-level assembly, and an exact cyclic-catalyst product lemma are obtained. Structured cyclic ideals compress tensor squares, but direct formula coupling dies and every pure tensor catalyst with a common YES/NO multiplier cannot improve the standard rank exponent. Formula-oblivious sparse hashes, linear feature shells, and code-dependent generator-type punctures lose soundness; exact parity-check type simplification is rigorously vacuous on the BMT reduced tensor ladder. Direct integer exact cover gives a clean additive squared-distance gap. Fixed pair-projection targets separate the tested fibers; a polynomial variable-target encoding now realizes their disjunction, but necessarily introduces another linear YES norm baseline and retains only an additive gap. The explicit global determinant dictionary and its all-compounds mutation retain short virtual permutations and exponential representation size. Homogenized integer exact-cover tensors are multiplicative in bounded rank-two and rank-three searches. Unrestricted NO sublattices have short witnesses, but restricting to sublattices carrying a primitive homogenizing functional restores finite rank-one/rank-two determinant and support gaps. A universal rank-two pointed determinant theorem and a weaker general odd-minor bound are proved; they are quantitatively insufficient for arbitrary-Euclidean partners. The parity tensor certificate is rigorous. Weighted set-support compression preserves exact pure-power tensor distance, but the proved pure-power dimension formula makes its rank exponential in the regime needed for BMT amplification; its maximal function-type mutation cannot repair this. A compact weight-class powering construction exists, but computing its generators decides the source problem; its polynomial parity relaxation collapses soundness. Deterministic sampled product folds can show large tiny-family gaps but fail frozen-parameter generalization as dimension grows. Low-dimensional exact-power toys have large finite gaps, but their dimension regime is incompatible with asymptotic NP-hardness. No polynomial-size polynomial-time reduction is obtained. No polynomial-gap reduction results. The exact syndrome-to-CVP identity remains only a conditional transfer tool.
