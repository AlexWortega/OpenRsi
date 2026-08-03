#!/usr/bin/env python3
"""Exact finite checks for bounded global-fingerprint subset collisions."""
import sys
sys.path.insert(0,'experiments')
from bounded_global_fingerprint_collision import run,collision,witness
import numpy as np
r=run();assert r['subset_count']>r['sum_bin_upper'] and r['trials']==20
assert all(x['witness_support']<=19+x['relation_support']-1 for x in r['records'])
# Dense mixing preserves a deterministic example.
f=[[(7*i+3*j)%5-2 for j in range(2)]for i in range(16)];lam,*_=collision(f);A,t,z,a=witness(f,lam)
rng=np.random.default_rng(2059);L=rng.integers(-6,7,size=(31,A.shape[0]),dtype=np.int64).astype(object)
assert np.all(L@(A@z-t)==0)
print('bounded global-fingerprint collision obstruction verified exactly')
