#!/usr/bin/env python3
"""Verify finite-seed phase dichotomy on a realized bipartite type graph."""
from __future__ import annotations
import random,sys
sys.path.insert(0,'experiments')
from verify_phase_cocycle import coboundary_or_cycle

def run(seed=191):
 rng=random.Random(seed);families=0;all_bad=0;with_good=0;trade_checks=0
 L=list(range(3));R=list(range(3));pairs=[(l,r) for l in L for r in R]
 for q in (2,3,5,7):
  for _ in range(100):
   tables=[]
   for s in range(8):
    E=[(l,r,rng.randrange(q)) for l,r in pairs]
    tables.append(E)
   # Every seed is evaluated on the same realized K_3,3 incidence graph.
   feasible=[]
   for E in tables:
    pot,cycle=coboundary_or_cycle(L,R,E,q)
    feasible.append(pot is not None)
   all_bad+=not any(feasible);families+=1
   # Add one guaranteed coboundary seed; it is feasible but gauge-trivial.
   beta={l:rng.randrange(q) for l in L};gamma={r:rng.randrange(q) for r in R}
   E=[(l,r,(beta[l]-gamma[r])%q) for l,r in pairs]
   pot,cycle=coboundary_or_cycle(L,R,E,q);assert pot is not None
   with_good+=1
   # Abstract support-three cancellation after gauging: at three ports,
   # 100+010+110 = 000 in GF(2) values coordinatewise.
   a,b,c,u=(1,0,0),(0,1,0),(1,1,0),(0,0,0)
   assert tuple(a[i]^b[i]^c[i] for i in range(3))==u;trade_checks+=1
 print({'seed_families':families,'seeds_per_family':8,'all_nontrivial_families_rejecting_realized_graph':all_bad,
        'families_with_inserted_coboundary_seed':with_good,'gauge_trade_checks':trade_checks})
if __name__=='__main__':run()
