#!/usr/bin/env python3
"""Exact checks for integer full-truth-table unary-marginal faults."""
import sys
sys.path.insert(0,'experiments')
from truth_table_marginal_integer import run, explicit_witness
import numpy as np

records=run()
assert len(records)==8
assert all(r['shape']==(59,62) and r['support']==13 and r['l1']==13 and r['squared_norm']==13 and r['exact'] for r in records)
# Dense linear row maps and all tested modular reductions retain exactness.
rng=np.random.default_rng(613)
for assignment in [(0,0,0),(0,0,1),(1,1,1)]:
 A,t,z,_=explicit_witness(assignment)
 L=rng.integers(-7,8,size=(31,A.shape[0]),dtype=np.int64).astype(object)
 assert np.all(L@(A@z-t)==0)
 for modulus in (2,3,5,6,10): assert np.all((A@z-t)%modulus==0)
print('integer full-truth-table marginal faults verified exactly')
