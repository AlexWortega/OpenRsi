#!/usr/bin/env python3
"""Verify controlled-permutation-cycle NCP finite attacks."""
import sys
sys.path.insert(0,'experiments')
from controlled_permutation_cycle import run,build,min_weight
import numpy as np
for q,trials,seed in ((3,20,223),(4,10,223),(5,10,227)):
 r=run(q,3,trials,seed)
 assert r['reported_optima']==[9]*trials
 assert r['canonical_fixed-branch_weight']==1+6*q
# Validate one explicit weight-9 cheating support exactly.
P=[((2,0,1),(2,0,1)),((1,0,2),(1,2,0)),((1,0,2),(1,2,0))]
H,t,meta=build(P)
chosen=[('x',0),(('s',0),2),(('s',1),1),(('s',2),2),
 (('f',0),(0,2)),(('f',1),(0,0)),(('f',1),(1,0)),(('f',1),(1,1)),(('f',2),(0,2))]
index={m:i for i,m in enumerate(meta)};x=np.zeros(len(meta),dtype=int)
for m in chosen:x[index[m]]=1
assert x.sum()==9 and np.array_equal(H.dot(x)%2,t)
print('controlled permutation cycle claims reproduced; explicit weight-9 cheat checked exactly')
