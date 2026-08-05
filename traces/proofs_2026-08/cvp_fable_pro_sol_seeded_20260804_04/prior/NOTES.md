# Attack log

## Milestone 1 — inherited map

Read all required prior status/proof/brief/notes. The inherited campaign obtained no ladder item (a)–(c). Its positive reusable lemma is the exact binary-syndrome to Euclidean-CVP squared-distance identity. Its obstruction map excludes bounded local signatures, marginal/tableau consistency, proper-scope holonomy hierarchies, local phase lifts, affine integer exact fibers, complete-assignment fingerprints, and explicit/code-oblivious tensor compression under their stated hypotheses.

Created `ORACLE_BRIEF.md`, `IDEAS.md`, and `STATUS.md` with explicit fine print rather than treating prior diagnostics as universal no-go theorems.

## Milestone 2 — two scouts

Ran two pre-2024 literature scouts, costing about $2.69 total. One scout reported that it discarded an off-limits search hit unread; no prohibited material was used. Distilled `LITERATURE.md`.

Main new invariant: if the syndrome fiber is `x0+C` and all legal witnesses are `x0+B`, then relative distance `d(C/B)` can charge illegal classes while allowing short legal differences. Exact-cover incidence gives a polynomial sparse global dictionary; CSS/homological code distance supplies classical quotient metrics. No classical theorem supplies the necessary SAT/exact-cover-to-quotient classifier. Product codes still uniquely handle all mixed words but have explicit length blowup. Rank condensers protect nonzero/rank, not Hamming support.

## Milestone 3 — first ideation and triage

The first IDEATE call supplied seven mechanisms. Top two were:

1. BMT exact-cover incidence + exchange quotient + sector-asymmetric distance balancing.
2. Odd-cyclic pointed tensor orbit fold / balanced product.

Other sketches (filling area, Lagrange evaluation, Sidon shielding, Pfaffian canonicalization, quotient expander bundling) all depended on the same legal-versus-illegal classifier or visibly failed on clean odd covers.

## Construction experiment A — exact-cover quotient

Implemented `experiments/verify_exchange_quotient.py`.

For each tiny 3DM dictionary it exactly enumerates every binary triple selection, verifies the BMT counting lemma, enumerates perfect matchings and odd covers, constructs all 2↔2/3↔3 packing exchanges, and computes quotient classes. It also computes the minimal span of *all* legal matching differences, independent of a chosen local exchange presentation.

Results (`experiments/exchange_quotient.log`):

* 120 exact instances checked, including 20 NO instances with nonempty odd-cover fibers.
* In 66 YES instances, an illegal odd cover shared a matching's class modulo bounded packing exchanges.
* In 32 instances, an illegal odd cover lay in the affine span of all perfect matchings themselves. Lightest such covers often had weight 5 versus matching weight 3.

This wounds the proposed quotient interface at an information-theoretic level. Any linear quotient that identifies all perfect matchings identifies every odd affine combination of them. Such an affine combination need not be a matching. A later high-relative-distance shell cannot distinguish an illegal vector already in the cheap legal class.

The broad route is not yet killed because a transformation might make completeness witnesses affine-closed, unique/canonical, or separately protected. No deterministic such transformation is known here.

## Construction experiment B — cyclic tensor fold

Implemented `experiments/verify_cyclic_tensor_fold.py`.

The script handles two families:

* a base pointed code replicated across an odd cyclic phase action, then tensor coordinates folded by diagonal-orbit XOR;
* naturally invariant small quasi-cyclic pointed codes, without phase-separated replication.

It constructs the folded generator and enumerates **every mixed folded word** exactly.

Results (`experiments/cyclic_tensor_fold.log`):

* 120 exact `ell=3` folds checked (20 replicated hostile/random codes, 100 natural invariant codes).
* No example violated the sharper `delta_fold >= 1+ceil((delta^2-1)/3)`.
* No pure minimum square violated the same orbit-count scale.
* 37/100 natural invariant codes lost distance relative to the full tensor value `delta^2`; many attained only the orbit-count scale.
* The phase-replicated family retained `delta_fold=delta^2`, but its replication expands length before folding and therefore gives no free asymptotic compression.

After the finite run, the mixed-word inequality was proved. For an odd group of order `ell` acting freely off the distinguished coordinate, symmetrize any pointed tensor word over the group. The distinguished bit remains one; on each free orbit the symmetrized value equals the fold parity, so `|S|=1+ell(|F(W)|-1)`. Full tensor pointed distance gives `|S|>=delta^2`, hence

`delta_fold >= 1+ceil((delta^2-1)/ell)`.

An invariant pointed minimum word attains equality. This upgrades mixed-word soundness from evidence to a rigorous lemma in `proof_cvp.md`, but it is **not** a hardness result. Missing:

1. a symmetry-replenishing recurrence where the free group order is comparable to current block length without paying that factor in padding;
2. an invariant sparse YES minimum word at every level;
3. exact iteration accounting. For reduced moving weights, amplifying weak base `q` versus `q+1` needs exponent `2^k = Omega(q log N)` (parity gives `q+2`, changing constants), hence `k=Theta(log q + log log N)` ideal squarings.

## Milestone 4 — converge on fold parameter wall

Used one CONVERGE call on the sole promising fold candidate, after the one-step lemma was proved. It returned and proved a no-go for **residual-lineage** iteration. Under the explicit assumption that quotient coordinates represented by fixed-fixed or fixed-moving pairs remain fixed under the next inherited action, propagated supported fixed weight satisfies `s_1>=3`, `s_{i+1}>=s_i^2`. Hence `N_k>=3^(2^(k-1))`, while the fold-certified ratio for base `Q` versus `Q+1` is at most `N_k^(3/(Q ln 3))`. The exponent vanishes as the base witness grows.

I checked the exact recurrences and rounding inequalities on 14,773 transitions in `experiments/verify_residual_fold_parameters.py`, then added a self-contained proof to `proof_cvp.md`. This wounds the natural residual balanced/orbit-product mutation but does not cover a genuinely new symmetry that remobilizes inherited cross sectors.

## Milestone 5 — scout and construct fresh-biset symmetry

Following the residual-lineage theorem, ran the protocol-required classical scout on symmetry renewal. It identified biset composition/balanced and lifted products as genuinely outside residual lineage: spend one group in `U×_G V` while a fresh commuting right group survives.

Immediately implemented the coordinate construction in `experiments/verify_pointed_biset_cross.py`. Across 54 exact cyclic products, the fresh action is free on all quotient coordinates except `[u,*]`. If the first pointed factor has `R_U` moving regular orbits, there are exactly `1+R_U` fixed quotient classes under every nonidentity fresh action. So the mechanism renews symmetry globally on moving-moving sectors but does not erase the distinguished cross sector.

I then tested the direct sector deletion instead of assuming it unsafe. Define reduced pointed tensoring by keeping only the corner bit and moving-moving tensor block. A contraction/slicing proof gives exact mixed-word distance `1+(delta-1)^2`; with an odd free group, orbit folding gives `1+ceil((delta-1)^2/ell)`. `experiments/verify_reduced_orbit_fold.py` checks 100 arbitrary and 100 invariant folded codes exactly. This is a second rigorous positive coding lemma and removes the cross-sector driver of the residual-lineage theorem. The new gap is assembly: realize repeated reduced products with fresh bimodule actions, invariant sparse YES words, and polynomial length.

## Milestone 6 — ideation round 2 and two more constructions

After scout + construction, ran the second IDEATE call. It proved useful functorial formulas for reduced folds and identified a conserved-exponent wall for invariant YES ladders, plus a non-invariant 'super-budget' completeness crack.

Implemented top experiment 1 end to end in `verify_reduced_fold_3dm.py`. A small 3DM YES instance has exact moving distance 3; a NO odd-cover instance has 5. After one-time `Z3` installation and two reduced residual folds, exhaustive mixed-word minima are:

* YES: `9,27,243` moving weights at levels 0,1,2;
* NO: `15,75,1875`;
* exact ratios: `5/3`, `25/9`, `625/81`;
* lengths: `25,193,12289`.

This validates the full assembly and exact ratio squaring, while confirming severe length growth.

Implemented top experiment 2 in three increasingly instance-relevant scripts. `verify_noninvariant_superbudget.py` exhausts cyclic orbit-span codes through `ell=11`; `verify_noninvariant_random_codes.py` adds unpointed cyclic generators; `verify_superbudget_3dm.py` gives each cyclic sheet an independent pointed 3DM witness so completeness does not pay group order. In the 3DM tests (`ell=3,5,7,11`), YES distance 3 folded to 9 and NO distance 5 folded to 25 in every case—the full square, with no orbit compression, even when proved floors were 1 and 3. The broader searches found no nontrivial `ell>d>1` floor-attaining case. This wounds but does not prove impossible the non-invariant completeness crack.

## Milestone 7 — final hostile referee and corrections

A final CONVERGE referee accepted the two main one-step lemmas but found missing hypotheses and scope errors. Corrected all of them in `proof_cvp.md` and scripts:

* added nonzero star-functional/pointedness assumptions;
* added the fixed-set extension of the orbit-fold lemma used in residual recurrence;
* required nonempty initial moving support (`Q>=4`) in the residual theorem;
* narrowed its title/scope to OF-only `Q` versus `Q+1` propagation;
* recorded the parity-sharper 3DM base `q` versus at least `q+2`;
* restricted the biset fixed-class count to the exact independent product-biset model tested;
* made functorial induction and absence of corner-only words explicit;
* rephrased conserved exponent as overhead-normalized, with exact divisibility and both minima invariant;
* corrected reduced moving-weight notation from `(q+2)/(q+1)` to `(q+1)/q` (parity changes constants);
* added exact assertions for the deterministic counts/outcomes claimed by scripts.

All nine new verifiers pass after these corrections.

## Milestone 8 — harvest, quarantine check, and cyclic catalyst construction

Harvested first: no experiment PID or unfinished log exists; only the run's trace tailer is active. Oracle spend remained `$13.80965`. Since total spend was `$23.94`, non-oracle spend was only `$10.13`; exact dollar attribution within that amount was unavailable, so I conservatively treated the 40% quarantine as binding. Every subsequent action in this milestone was a construction attempt, implementation, or exact soundness attack; no oracle call was made.

Implemented four new construction scripts:

1. `verify_cyclic_ideal_superbudget.py`: 116 exact binary cyclic ideals through odd length 31. All 94 nontrivial `ell>d>1` cases compress correlation distance below `d^2`; best recorded `(31,11,11)` compresses 121 to 11. No floor hit.
2. `verify_cyclic_closure_3dm.py`: direct cyclic closure of 3DM. Exact soundness attack on 400 assemblies kills it: every YES and NO transformed code has moving/folded distance 1.
3. Mutation `verify_cyclic_ideal_3dm.py`: retain 3DM and tensor with a separate length-15 cyclic catalyst. Exact mixed minima YES `15→45`, NO `25→125`; ratio squares.
4. `verify_cyclic_catalyst.py`: 100 arbitrary small outer codes verify exact catalyst distance `5d²` for all mixed words. This admits a clean product-code proof now added to `proof_cvp.md`.

Parameter attack began with `verify_catalyst_parameters.py` and was then generalized. For any pure tensor catalyst of output length `L` applying one common distance multiplier `a`, standard rank exponent changes to `2log(b/d)/(2log n+log L)` and cannot increase. `verify_catalyst_exponent_bound.py` checks 17,151,060 tuples; the algebraic identity is the proof. This kills pure tensor catalysts as gap amplifiers, including growing families. Per protocol, `IDEAS.md` records the required mutation: asymmetric YES/NO catalyst factors or submultiplicative coordinate growth.

Also implemented `verify_reduced_fold_cvp.py`, taking the level-1 folded finite codes all the way to explicit rank-192 integer lattice bases. Exact checks give squared distances 27 and 75 and Euclidean ratio `5/3`; each basis has systematic determinant/index `2^187`. This validates the conditional transfer on the actual constructed matrices without claiming asymptotic hardness.

Per the catalyst autopsy, immediately tested the required asymmetric mutation rather than burying it. `verify_asymmetric_hash_fold.py` exactly evaluates 866 valid formula-oblivious sparse hash folds on ten YES and ten NO reduced 3DM squares. Best uniform exponent is 0.0962 versus unfurled 0.2447; most folds collapse the ratio. The exact tested family is wounded/killed with autopsy and the next code-dependent mutation recorded in `IDEAS.md`.

## Milestone 9 — code-dependent folds and exact parity-check simplification

Implemented the previously recorded next mutation rather than extrapolating
from formula-oblivious hashes.  `verify_code_dependent_type_fold.py` groups
moving coordinates by basis-invariant generator-column type and punctures each
class according to a deterministic budget.  It checks all mixed words, the
exact rounding bound, and relabeling invariance on ten YES and ten NO reduced
3DM squares.  The best tested standard rank exponent is the unpunctured one;
at budget two the uniform distance ratio already drops from `25/9` to at most
`13/9`.

Per protocol, ran a targeted pre-2024 scout before any further ideation.  It
found exact syndrome-side matroid simplification: merge repeated nonzero
parity-check columns and delete zero columns, preserving every target's minimum
weight exactly.  I immediately implemented this in
`verify_parity_type_tensor.py`, including reduced tensor, affine parity-check
conversion, simplification, and re-homogenization.  Both tiny 3DM fibers retain
all `8 -> 64 -> 4096` formal coordinates; distances amplify exactly but length
does too.

This finite outcome has a short general autopsy.  A parity-check matrix has a
zero/repeated column only if its kernel has a word of weight one/two.  The BMT
moving span has distance at least three, and its reduced star-zero tensor code
has distance at least nine by product distance.  Therefore parallel
simplification removes nothing at every iteration of this family.  Recorded
the proof in `proof_cvp.md`, the classical digest in `LITERATURE.md`, and both
mutations/autopsies in `IDEAS.md`.

## Milestone 10 — harvest and construction-only round

Harvested background processes first.  No process in this run was active; one
long `ehrhart3_adv.py` process belonged to the separate
`runs/proofs_code_fable` working directory and was left untouched.  No local
PID/log was unfinished.

The user-supplied current accounting was `$4.37/$30`, oracle `$1.50`; exact
construction-dollar attribution was unavailable, so quarantine was treated as
binding.  The next actions were two explicit constructions and exact attacks,
with no oracle call.

1. `verify_feature_shell_3dm.py` implements augmented syndrome matrices with
   cost `|x|+R|Fx|`, using global pair projections, deterministic sparse
   hashes, and hybrids.  Exhaustive search over every odd cover in 40 YES and
   40 NO instances, 45 feature choices, gives best uniform ratio `7/6`, below
   the base `5/3`.  It checks an explicit augmented-matrix cheating witness.
2. `verify_integer_3dm_cvp.py` implements direct integer incidence CVP and
   meet-in-the-middle signed search.  It confirms YES norm squared 3 and NO
   minima at least 5 across 80 instances, including a coefficient `-1` cheat
   at norm 5.  The general proof is `sum z_j^2>=sum z_j=q`, equality only for
   Boolean `z`, with even positive excess in NO cases.
3. The tested mutation appends all pair-projection equations and branches over
   the 36 consistent targets at `q=3`.  Exact `{-1,0,1}` search on four YES and
   four NO instances finds YES norm 3 and no NO exact-fiber point.  This finite
   classifier initially left an exponential `(q!)^2` target menu; item 4 tests
   and resolves the disjunction encoding, but not its additive-gap wall.
4. Immediately tested the required polynomial disjunction mutation in
   `verify_variable_pair_projection_cvp.py`: make all three projection tables
   lattice variables constrained to equal the projections of `z`.  This gives
   one fixed polynomial-size target and is sound against signed vectors, but
   exact minima are only 12 versus 14.  The mutation's autopsy is the table
   norm baseline: each row-sum-one integer table costs at least `q`, so three
   projection tables add `3q` to every YES witness.  Block-weight variants
   change constants but remain additive.

## Milestone 11 — scout then immediate determinant construction

After the construction-only milestone, ran one protocol-required pre-2024
scout on zero-baseline permutation unions and multiplicative integer tensor
soundness.  It found no direct solution; the main constructive lead was the
global determinant/common-basis polynomial, with Haviv--Regev's all-sublattice
criterion as the relevant mixed-tensor invariant.

Acted immediately with `verify_determinant_permutation_dictionary.py`.  It
exhausts signed determinant-monomial dictionaries at q=3 and all support-three
trades at q=4, including aggregate tables and every exterior compound state.
Global states yield finite constant separation but retain short virtual
permutations and require q! monomial columns.  The required mutation from top
determinant to all compounds was tested before recording the autopsy.

## Milestone 12 — homogeneous integer tensor construction

Acted on the scout's Haviv--Regev lead with
`verify_homogeneous_integer_tensor.py`.  It constructs homogeneous integer
exact-cover lattices and exhausts bounded arbitrary mixed tensor coefficients,
not only pure products.  Four rank-two YES/NO examples show exact
multiplicativity of the pointed squared norm.  This remains finite evidence;
higher kernel rank and an all-sublattices determinant theorem are unresolved,
as is the tensor rank wall.  The next hostile mutation is recorded in
`IDEAS.md` rather than promoting the signal to a claim.

## Milestone 13 — harvest and higher-rank tensor mutation

Harvested first.  No local job was initially active; the only old process
belonged to another run.  User accounting (`$10.63`, oracle `$2.89`) did not
permit exact construction attribution, so the next action was the recorded
higher-rank construction mutation, not an obstruction call.

`verify_highrank_integer_tensor.py` now uses Smith decomposition for saturated
integer kernels and exhausts six YES/six NO rank-three tensor codes over all
`3^9` mixed coefficient matrices.  Multiplicativity survives exactly.
`verify_tensor_subdeterminants.py` then attacks the proposed all-sublattices
proof on twelve+ twelve cases and finds the precise failure: unrestricted NO
`s=0` directions match YES minimum norm, rank-two determinant, and support.
The required homogenizing-functional/quotient mutation is recorded before
burying the naive lemma.

A coefficient-`[-2,2]` background search over selected rank-three tensors was
launched after the foreground verifier.

## Milestone 14 — harvest and pointed-sublattice mutation

Harvested the local background search: it completed with `HIGHRANK_C2_PASS`,
checking `5^9` mixed matrices for each of three YES/three NO lattices.  Added
`verify_highrank_tensor_C2.py` so the finite claim is independently
reproducible and asserted.

Then implemented the required mutation to the failed unrestricted sublattice
lemma.  `verify_pointed_sublattice_diagnostics.py` restricts to sublattices on
which the homogenizing functional is primitive.  Exact enumeration over
20+20 rank-three lattices restores rank-one and rank-two norm,
determinant, and support gaps.  This is now the sole promising mathematical
invariant, with arbitrary-rank proof and rank compression still missing.
`verify_pointed_rank3_coeff_bound.py` then widens coefficients through absolute
value three; 145 primitive directions and at least 7,480 rank-two pairs per
instance retain exactly the same finite gaps.  The next rank mutation,
`verify_pointed_rank4_diagnostics.py`, tests 20+20 rank-four lattices and
sparse mixed tensors; it also retains the same pointed determinant/support and
16/36 tensor gaps.

## Milestone 15 — focused proof resolution

Used one CONVERGE call on the sole promising pointed-sublattice lemma.  It
proved the exact rank-two determinant/support bounds and a general odd-minor
bound, but also supplied a decisive arbitrary-partner counterexample.  The
correct surviving mechanism is simpler: coordinate parity reduces the integer
lattice tensor to the already-proved binary pointed tensor theorem, certifying
all mixed integer tensors.  Added a self-contained proof to `proof_cvp.md` and
`verify_pointed_tensor_theorems.py` for every finite arithmetic/count quoted.
The remaining wall is rank compression, not mixed-word soundness.

## Milestone 16 — weighted Euclidean tensor compression

Harvested first: no active process belonged to this run.  User accounting was
`$21.17` total and `$5.73` oracle; exact construction attribution was
unavailable, so quarantine was treated as binding and no oracle was called.

Implemented an exact construction exploiting Euclidean weights rather than
unweighted binary puncturing.  Pure-power tensor coordinates depend only on
their underlying set of base indices.  Integer orbit multiplicities are
represented as sums of scaled square rows, giving an explicit Construction-A
CVP basis whose squared distance equals full tensor Hamming distance.

Three verifiers cover multiset orbits, set-support compression, explicit
integer bases, tiny 3DM end-to-end distances, and the required mutation merging
identical product functions.  The resulting output is independent of tensor
order, but finite function-type counts grow rapidly with base code dimension;
the remaining parameter gap was then attacked rather than left conjectural.
`verify_pure_power_dimension.py` checks the exact formula
`dim P_r(D)=sum_{j<=min(k,r)} C(k,j)`.  The proof in `proof_cvp.md` shows that
all squarefree message monomials occur.  Hence every exact weighted/function
compression has exponential rank once tensor order reaches code dimension;
function-type merging is the tested mutation and cannot evade this wall.

The next construction, `verify_weight_class_compressor.py`, shows that distance
powering itself admits only `m+2` weighted coordinates if exact attainable
fiber weights are supplied.  Exact low-weight search validates it, then the
computability attack identifies its hidden NP-hard step: deciding whether to
include class `q`.  The tested parity/counting relaxation includes that class
in NO and collapses the gap.

Finally tested the dimension-wall mutation that discards rather than exactly
represents most pure-power functions.  A canonical sampled fold initially
found ratio 7 on ten+ten instances.  Before believing it, froze the parameters
and expanded to 50+50 instances at five dictionary sizes and permuted
presentations.  The gap collapses to at most 4/3 and then one, so the apparent
signal is recorded as overfitting with an exact generalization verifier.

With the remaining budget, tested the only small-dimension parameter mutation
rather than calling another oracle.  `verify_exact_power_polynomial_base.py`
confirms large finite gaps when BMT code dimension is at most six.  The
asymptotic autopsy is rigorous: logarithmic dimension permits exhaustive
polynomial decoding, while larger dimension makes exact compressed rank
superpolynomial.  This closes the finite toy without changing ladder status.

## Budget quarantine

Oracle log now records eight calls totaling `$15.31318`, including the final
targeted classical scout.  No further ideation/no-go consultation followed it:
its sole surviving mechanism was immediately implemented, tested, proved
vacuous for the current family, and mutated against the already implemented
generator-type fold.  Construction work includes nineteen exact verifier
scripts and the finite explicit CVP transfer.  No claim is made that dollar
attribution can be reconstructed exactly, but the post-checkpoint research
sequence remained entirely construction/implementation/attack except for the
single protocol-required scout.
