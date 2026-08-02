# GQ-Tanner q=2 falsification and one possible repair

The proposal was implemented at its prescribed smallest test, and the exact failure is now recorded in ORACLE_BRIEF.md.

Using the doily as duads/synthemes of K6, an involutory polarity was found and all 720 doily collineations were exhausted. Exactly 30 collineations outside `Aut(Q,pi)` move every point to a nonneighbor in the polarity graph. Hence for any legal equitable configuration f, `g=sigma f` is a legal equitable coordinatewise-bad mate not removed by the proposed polarity-centralizer quotient. Passing verifier: `experiments/test_gq_tanner_q2.py`.

Separately, the exact q=2 equitable CSP on the Tutte-Coxeter graph (7155 variables, 140613 clauses after one-star symmetry fixing) is solver-UNSAT. No certificate was retained, so this is diagnostic only.

There is one nontrivial potential repair: quotient by the **full collineation group** of the GQ, since Tanner line constraints and equitability are invariant under it. Although the polarity graph is not invariant under this larger group, choosing one canonical representative per full orbit is still logically allowed if every bad pair is in a common full orbit. At q=2 this absorbs the 30 discovered maps. However abundance remains completely unproved, and the Bethe count may be invalid because a configuration is a locally-injective homomorphism from the cubic Tanner graph into the line-intersection geometry.

Analyze only this repair. Either:
1. give a rigorous asymptotic abundance lower bound and a credible full-collineation rigidity lemma/proof; or
2. derive a structural/spectral obstruction showing equitable configurations are absent or too few; or
3. provide a concrete q=2 or q=8 finite bad pair not related by a full collineation, with an implementable search reduction.

Do not switch to a new family or merely repeat the unproved program. The forbidden recent work remains off-limits.