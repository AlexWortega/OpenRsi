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

The mixed-word lower bound is now proved generally for any odd group acting freely off the distinguished coordinate: symmetrization converts orbit parity into an invariant full tensor word, giving `delta_fold ≥ 1+ceil((delta^2-1)/ell)`. An invariant pointed minimum word attains equality. This is a genuine coding lemma, but not a reduction. A further theorem in `proof_cvp.md` rules out the natural **residual-lineage** iteration: if fixed/cross sectors remain fixed under the next inherited action, then `N_k≥3^(2^(k-1))` while the certified ratio from base `Q` versus `Q+1` is at most `N_k^(3/(Q ln 3))`. Thus its exponent vanishes. `experiments/verify_residual_fold_parameters.py` checks 14,773 exact recurrence transitions.

A follow-up classical scout found fresh symmetry through biset/bimodule composition, which lies outside residual lineage. The coordinate-level construction was implemented in `verify_pointed_biset_cross.py`: over 54 exact products, the new action is free except on `[u,*]` classes, exactly `1+R_U` of them.

A direct reduced-product mutation removes both star-cross sectors while retaining the corner and moving-moving block. This now has a proof: if `d=delta_*(D)-1`, reduced pointed tensor distance is exactly `1+d^2` for all mixed words; an odd free-orbit fold has distance at least `1+ceil(d^2/ell)`. `verify_reduced_orbit_fold.py` checks 100 arbitrary reduced codes and 100 invariant folded codes. This bypasses the cross-sector recurrence. An explicit two-level residual assembly is now implemented in `verify_reduced_fold_3dm.py`: exact YES/NO moving distances evolve `9/15 → 27/75 → 243/1875`, so the ratio squares exactly, but lengths grow `25 → 193 → 12289`. This validates the mechanism while exposing the output exponent wall.

A non-invariant 'super-budget' mutation avoids multiplying the YES weight by the group order. Exact 3DM tests for `ell=3,5,7,11` retain the full squared distances 9 (YES) and 25 (NO), not the much smaller orbit floors. Two broader cyclic searches also found no nontrivial `ell>d>1` floor-attaining example. This is finite negative evidence, not a theorem.

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

Both verifiers exit zero and logs are in `experiments/*.log`.

## Honest assessment

No deterministic polynomial-gap NCP instance and no GapCVP reduction have been obtained. The relative-quotient candidate suffered a concrete affine-closure failure. Two one-step mixed-word lemmas and a complete finite two-level assembly are obtained. The invariant ladder has vanishing exponent/output blowup; tested non-invariant ladders fail to compress YES distance. No polynomial-gap reduction results. The exact syndrome-to-CVP identity remains only a conditional transfer tool.
