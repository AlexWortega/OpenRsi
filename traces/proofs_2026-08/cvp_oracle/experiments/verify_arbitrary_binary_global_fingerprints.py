#!/usr/bin/env python3
"""Exact finite checks for arbitrary binary global-fingerprint dependence."""
import sys
sys.path.insert(0,'experiments')
from arbitrary_binary_global_fingerprints import run,witness
import numpy as np
r=run();assert r['records']==150
for m,w in r['max_weight_by_m'].items():assert w<=15+(m+1)
# Dense GF2 row processing preserves one attack.
F=[[(i*(j+3)+j*j+1)&1 for j in range(14)]for i in range(16)]
A,t,z,dep,a=witness(F);rng=np.random.default_rng(2083);L=rng.integers(0,2,size=(37,A.shape[0]),dtype=np.uint8)
assert np.array_equal((L@A@z)%2,(L@t)%2)
print('arbitrary binary global-fingerprint obstruction verified exactly')
