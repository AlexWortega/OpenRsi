#!/usr/bin/env python3
"""Exact verification of mixed 2/3-orbit integer hierarchy obstruction."""
import sys
sys.path.insert(0,'experiments')
from integer_mixed_orbit_cycle import run,witness,DOMAIN,perm
import numpy as np

records=run()
assert all(r['exact'] and r['support']==5*r['groups_K'] and r['squared_norm']==5*r['groups_K'] for r in records)
# Global UNSAT: branch is preserved; final permutation has no fixed point.
assert all(perm(True,x)!=x for x in DOMAIN)
# Arbitrary dense integer row processing retains exactness.
H,t,z,_,_,_=witness(7,3)
rng=np.random.default_rng(1827)
L=rng.integers(-9,10,size=(43,H.shape[0]),dtype=np.int64).astype(object)
assert np.all(L@(H@z-t)==0)
print('mixed 2/3-orbit integer hierarchy obstruction verified exactly')
