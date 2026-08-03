#!/usr/bin/env python3
"""Exact checks for the global Walsh-moment no-go."""
import sys
sys.path.insert(0,'experiments')
from walsh_global_moments import run,subsets,omega,integer_witness,binary_witness
import numpy as np
r=run(3)
assert r=={'n':3,'q':8,'columns':56,'proper_integer_checks':56,'binary_full_checks':8,
 'witness_cost':14,'full_integer_shape':(57,56),'full_rank':56,'augmented_rank':57,'full_integer_infeasible':True}
# Dense maps preserve selected exact witnesses.
S=subsets(3);a=omega(3)[5];T0=S[-1];P=S[:-1]
A,t,z=integer_witness(3,P,T0,a);rng=np.random.default_rng(2011)
L=rng.integers(-7,8,size=(39,A.shape[0]),dtype=np.int64).astype(object)
assert np.all(L@(A@z-t)==0) and np.count_nonzero(z)==14 and sum(int(x)**2 for x in z)==14
A,t,e=binary_witness(3,S,a);L=rng.integers(0,2,size=(41,A.shape[0]),dtype=np.int8).astype(object)
assert np.all((L@(A@e-t))%2==0) and np.count_nonzero(e)==14
print('global Walsh-moment obstruction verified exactly')
