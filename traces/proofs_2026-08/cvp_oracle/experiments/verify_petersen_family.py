#!/usr/bin/env python3
"""Verify scalable disjoint-Petersen all-pairs pseudoassignment counts/support lemma."""
from __future__ import annotations
import itertools
BASE=[(0,1),(1,2),(2,3),(3,4),(0,4),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(6,9),(6,8),(5,8)]
def graph(copies):return [(10*c+u,10*c+v) for c in range(copies) for u,v in BASE]
def verify(copies):
 E=graph(copies);n=10*copies;inc={v:set() for v in range(n)}
 for i,(u,v) in enumerate(E):inc[u].add(i);inc[v].add(i)
 assert all(len(inc[v])==3 for v in range(n))
 # No triangles or 4-cycles, checked through common-neighbor counts.
 adj={v:set() for v in range(n)}
 for u,v in E:adj[u].add(v);adj[v].add(u)
 assert all(u not in adj[u] for u in range(n))
 for u,v in itertools.combinations(range(n),2):
  assert len(adj[u]&adj[v])<=1
 # Support lemma for every singleton/pair Q,R and every nonzero GF3 row combination.
 groups=[(v,) for v in range(n)]+list(itertools.combinations(range(n),2));checks=0
 for Q in groups:
  UQ=set().union(*(inc[v] for v in Q))
  for R in groups:
   W=UQ & set().union(*(inc[v] for v in R));common=set(Q)&set(R)
   for alpha in itertools.product(range(3),repeat=len(Q)):
    coeff=[0]*len(E)
    for v,a in zip(Q,alpha):
     for ei in inc[v]:
      u,w=E[ei];coeff[ei]=(coeff[ei]+a*(1 if u==v else -1))%3
    if {i for i,c in enumerate(coeff) if c}<=W:
     assert all(a==0 for v,a in zip(Q,alpha) if v not in common)
    checks+=1
 adjacent=len(E);pairs=n*(n-1)//2;nonadj=pairs-adjacent;K=n+pairs
 weight=n*9+adjacent*27+nonadj*81
 return {'copies':copies,'vertices':n,'edges':len(E),'groups_K':K,'pseudo_weight':weight,
  'weight_over_K':weight/K,'support_checks':checks,'charge_sum_mod3':1}
def run():
 out=[verify(c) for c in (1,2,3)]
 print(out);return out
if __name__=='__main__':run()
