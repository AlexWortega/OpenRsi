#!/usr/bin/env python3
"""Verify all-pair clause hierarchy on scalable XOR/Tseitin CNFs."""
import itertools,sys
sys.path.insert(0,'experiments')
from connected_views import inconsistent_xor_cycle
from tseitin_graph_cnf import formula
from random_scope_3sat import build
from search_pseudoviews import gf2_solve
rows=[]
for length in (3,5,7,10,15):
 C=inconsistent_xor_cycle(length);S=[frozenset((j,)) for j in range(len(C))]+[frozenset(p) for p in itertools.combinations(range(len(C)),2)]
 H,t,_=build(C,S);x=gf2_solve(H,t);assert x is None;rows.append(('xor',length,len(C),H.shape))
for n in (4,6,8):
 C,E=formula(n,313+n);S=[frozenset((j,)) for j in range(len(C))]+[frozenset(p) for p in itertools.combinations(range(len(C)),2)]
 H,t,_=build(C,S);x=gf2_solve(H,t);assert x is None;rows.append(('tseitin',n,len(C),H.shape))
print({'exact_infeasible_instances':len(rows),'rows':rows})
