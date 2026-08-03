#!/usr/bin/env python3
"""Run selected finite sanity checks for the discarded candidate encodings."""
import sys
sys.path.insert(0, 'experiments')
from connected_views import all_eight_clauses, build, exact_min_weight
from search_pseudoviews import gf2_solve

COUNTEREXAMPLE = [
 (2,-1,-4),(2,1,-4),(3,2,-1),(-3,-2,-4),(-1,4,-2),(-2,3,1),
 (3,-1,-2),(2,3,4),(4,2,1),(4,-3,1),(4,2,-1),(4,2,3),
 (2,3,-4),(1,3,4)]

def check_solution(inst, mask):
    assert mask is not None
    chosen = [j for j in range(inst.H.shape[1]) if (mask >> j) & 1]
    got = inst.H.tocsr()[:, chosen].sum(axis=1).A1 % 2
    assert (got == inst.target).all()

# All eight clauses: d=1 permits one legal view per clause; d=2 has no exact fiber.
i1 = build(all_eight_clauses(), 1)
r1, _ = exact_min_weight(i1, 30)
assert r1.status == 0 and round(r1.fun) == 8
i2 = build(all_eight_clauses(), 2)
assert gf2_solve(i2.H, i2.target) is None

# Fixed UNSAT formula found at seed 1. Exhaustively verify UNSAT over its four variables.
from connected_views import satisfies
import itertools
assert not any(all(satisfies(c, dict(enumerate(bits, 1))) for c in COUNTEREXAMPLE)
               for bits in itertools.product((0,1), repeat=4))
ic = build(COUNTEREXAMPLE, 2)
mask = gf2_solve(ic.H, ic.target)
check_solution(ic, mask)
assert len(ic.groups) == 105 and mask.bit_count() == 243
# HiGHS proves this support is minimum, not merely one elimination output.
rc, _ = exact_min_weight(ic, 300)
assert rc.status == 0 and round(rc.fun) == 243
# Adding connected triples kills the exact fiber for this particular formula.
i3 = build(COUNTEREXAMPLE, 3)
assert gf2_solve(i3.H, i3.target) is None
from verify_odd_cycle_counterexample import verify
verify(3, 1)
verify(4, 2)
from ternary_exact_one import matrix, min_weight_mod3, all8, construction_a_basis
Ht, tt, Nt, _ = matrix(all8(), 3)
assert Nt == 51 and Ht.shape == (83, 102)
rt, xt = min_weight_mod3(Ht, tt, 300)
assert rt.status == 0 and round(rt.fun) == Nt + 1
assert (Ht.dot(xt) % 3 == tt).all()
Bt = construction_a_basis(Ht)
assert Bt.shape == (102, 102) and (Ht.toarray().dot(Bt) % 3 == 0).all()
# det(B)=3^rank(H), so nonzero diagonal determinant follows from its block construction.
assert all(Bt[:, j].any() for j in range(Bt.shape[1]))
print('selected finite sanity checks passed (MILP statuses are not proof certificates)')
