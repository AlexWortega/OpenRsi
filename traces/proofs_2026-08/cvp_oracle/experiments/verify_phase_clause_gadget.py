#!/usr/bin/env python3
"""Verify finite phase-lift gadget searches."""
import sys,itertools
sys.path.insert(0,'experiments')
from phase_clause_gadget import run,evaluate,VIEWS
r2=run(2,200,47); r3=run(3,100,47); r4=run(4,30,47)
assert r2['outcome_histogram']=={(3,0):117,(3,4):81,(3,6):2}
assert r3['outcome_histogram']=={(3,0):89,(3,21):4,(3,18):7}
assert r4['outcome_histogram']=={(3,48):3,None:27}
# Exhaust all separable phase signatures alpha_j(a)=beta_j(a_j).
for q,expected in ((2,{(3,6):64}),(3,{(3,24):729})):
 hist={}
 for vals in itertools.product(range(q),repeat=6):
  beta=[[vals[2*j+b] for b in (0,1)] for j in range(3)]
  alpha={a:tuple(beta[j][a[j]] for j in range(3)) for a in VIEWS}
  e=evaluate(alpha,q);key=(e['minimum_trade'],e['infeasible_targets']);hist[key]=hist.get(key,0)+1
 assert hist==expected
print('phase-gadget finite claims verified by exact GF(2) dynamic programming')
