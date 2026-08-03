#!/usr/bin/env python3
"""Exact verification of global univariate finite-difference moments."""
import sys
sys.path.insert(0,'experiments')
from univariate_global_moments import run,witness
import numpy as np
r=run(8)
assert r['columns']==56 and r['full_degree_shape']==(57,56)
assert r['full_rank']==56 and r['augmented_rank']==57 and r['full_infeasible']
for x in r['records']:
 d=x['degree'];assert x['support']==7+d+1 and x['l1']==7+(2**(d+1)-1)
# Dense row mixing preserves the highest incomplete-degree witness.
A,t,z=witness(8,6);rng=np.random.default_rng(2029);L=rng.integers(-4,5,size=(37,A.shape[0]),dtype=np.int64).astype(object)
assert np.all(L@(A@z-t)==0)
print('univariate global-moment obstruction verified exactly')
