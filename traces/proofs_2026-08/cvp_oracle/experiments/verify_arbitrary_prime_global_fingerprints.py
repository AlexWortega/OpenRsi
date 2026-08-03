#!/usr/bin/env python3
"""Exact finite checks for arbitrary prime-field global fingerprints."""
import sys
sys.path.insert(0,'experiments')
from arbitrary_prime_global_fingerprints import run,witness
import numpy as np
r=run();assert r['q']==12 and r['m']==10 and r['max_support']<=22
p=5;F=[[(i*i+3*i*j+2*j+1)%p for j in range(10)]for i in range(12)];A,t,z,rel,a=witness(F,p)
rng=np.random.default_rng(2113);L=rng.integers(0,p,size=(29,A.shape[0]),dtype=np.int64).astype(object)
assert np.all((L@(A@z-t))%p==0)
print('arbitrary prime-field global-fingerprint obstruction verified exactly')
