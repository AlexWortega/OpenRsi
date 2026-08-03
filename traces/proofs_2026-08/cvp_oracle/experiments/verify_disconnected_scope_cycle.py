#!/usr/bin/env python3
"""Verify finite disconnected-scope cycle experiments."""
import sys
sys.path.insert(0,'experiments')
from disconnected_scope_cycle import run,closure_scopes,build
from search_pseudoviews import gf2_solve
r1=run(5,2,5,131);r2=run(6,3,8,131);r3=run(7,3,10,137)
def exact_feasible(n,d,count,seed):
 import random
 rng=random.Random(seed);base=[frozenset(rng.sample(range(n),d)) for _ in range(count)]
 base += [frozenset((e,)) for e in range(n)]
 H,t,_=build(n,closure_scopes(n,base))
 return gf2_solve(H,t) is not None
assert exact_feasible(5,2,5,131)
assert not exact_feasible(6,3,8,131)
assert not exact_feasible(7,3,10,137)
assert r1=={'n':5,'d':2,'base_scopes':5,'closure_scopes_K':24,'shape':(480,162),
 'status':0,'reported_optimum':72,'ratio':3.0,'component_proxy_max_colorings':27}
assert r2['status']==2 and r2['reported_optimum'] is None and r2['closure_scopes_K']==58
assert r3['status']==2 and r3['reported_optimum'] is None and r3['closure_scopes_K']==84
print('disconnected-scope feasibility claims verified by exact GF(2) elimination; optimum 72 remains MILP evidence')
