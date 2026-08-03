# Status

**Outcome:** PARTIAL CONSTRUCTION DIAGNOSTICS ONLY; no progress on goal ladder (a)–(c).

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

No background experiment remained to harvest. Exact dollar attribution could not certify the 40% construction floor, so quarantine was conservatively treated as binding: all subsequent work was construction/implementation/exact attack, with no further oracle call.

`verify_cyclic_ideal_superbudget.py` exhausts 116 small binary cyclic ideals. All 94 nontrivial `ell>d>1` cases compress below `d²`; examples with `(ell,d,d')=(31,11,11)` compress 121 to 11. Directly applying cyclic closure to 3DM fails: `verify_cyclic_closure_3dm.py` checks 400 exact assemblies and every YES/NO transformed code has moving and folded distance one.

The tested mutation keeps the instance code intact and uses a separate cyclic ideal as a catalyst. A length-15, dimension-3 catalyst has odd distance five before and after correlation folding. For any pointed outer code of moving distance `d`, the folded catalyst construction has exact mixed-word distance `5d²`; this follows by tensor reassociation and pointed multiplicativity. `verify_cyclic_catalyst.py` checks 100 random small outer codes. On fixed 3DM instances, `verify_cyclic_ideal_3dm.py` gives YES `15→45`, NO `25→125`, so the ratio squares exactly.

A general parameter identity now closes pure tensor catalysts as gap amplifiers: output length `Ln²` and common distance multiplier `a` give new standard rank exponent `2log(b/d)/(2log n+log L)`, never above the base exponent. `verify_catalyst_exponent_bound.py` checks 17,151,060 tuples; the identity is proved in `proof_cvp.md`. The required tested-next mutation is asymmetric YES/NO multiplication or submultiplicative coordinate growth, not merely a better growing cyclic catalyst.

As a finite end-to-end transfer check, `verify_reduced_fold_cvp.py` converts the level-1 folded YES/NO codes into explicit rank-192 integer lattice bases in systematic Construction-A form. Exact affine enumeration and determinant/index checks give squared Euclidean distances 27 and 75, hence Euclidean ratio exactly `5/3`. This is a finite construction check, not asymptotic hardness.

The protocol-required asymmetric mutation was also tested. `verify_asymmetric_hash_fold.py` checks 866 valid formula-oblivious 1-/2-sparse folds on ten YES and ten NO reduced 3DM squares. Best uniform exponent is 0.0962, below the unfurled finite exponent 0.2447; cancellation usually collapses soundness. Code-dependent algebraic folds remain outside this test.

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

All listed new verifiers exit zero; deterministic logs are in `experiments/*.log`.

## Honest assessment

A final hostile referee pass was incorporated; it corrected pointedness hypotheses, residual-theorem scope, biset-model quantifiers, exponent terminology, and 3DM parity accounting. No deterministic polynomial-gap NCP instance and no GapCVP reduction have been obtained. The relative-quotient candidate suffered a concrete affine-closure failure. Two one-step mixed-word lemmas, a complete finite two-level assembly, and an exact cyclic-catalyst product lemma are obtained. Structured cyclic ideals compress tensor squares, but direct formula coupling dies and every pure tensor catalyst with a common YES/NO multiplier cannot improve the standard rank exponent; the tested asymmetric sparse-hash mutation also loses soundness. No polynomial-gap reduction results. The exact syndrome-to-CVP identity remains only a conditional transfer tool.
