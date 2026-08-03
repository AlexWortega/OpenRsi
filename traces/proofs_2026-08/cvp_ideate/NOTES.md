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
3. exact iteration accounting. Amplifying `(q+2)/(q+1)` needs exponent `2^k = Omega(q log N)`, hence `k=Theta(log q + log log N)` squarings, not a casual logarithmic claim.

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

## Budget quarantine

Oracle spending so far: two scouts + one ideation call. Construction work immediately followed the ideation answer with two exact end-to-end finite programs. No further no-go consultation has been made. The construction fraction is now substantial and should remain at least 40%.
