#!/usr/bin/env python3
"""Exact checks for integer mixed-characteristic Petersen all-pairs cheat."""
import sys
sys.path.insert(0,'experiments')
from integer_petersen_pair_counterexample import run,build,E,inc,b
import numpy as np
r=run()
assert r['groups']==55 and r['exact']
assert r['rhs_sum_mod2']==r['rhs_sum_mod3']==1
# Both branches are globally UNSAT: summing signed incidence rows cancels LHS.
coeff=[0]*len(E)
for v in range(10):
 for e,s in inc[v]:coeff[e]+=s
assert coeff==[0]*len(E) and sum(b)==1
H,t,z,_,_=build();rng=np.random.default_rng(1901)
L=rng.integers(-5,6,size=(53,H.shape[0]),dtype=np.int64).astype(object)
assert np.all(L@(H@z-t)==0)
print('integer mixed-characteristic Petersen all-pairs counterexample verified exactly')
