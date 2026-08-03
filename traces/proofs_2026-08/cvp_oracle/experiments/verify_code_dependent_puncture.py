#!/usr/bin/env python3
"""Verify exact finite code-dependent puncturing search."""
import sys
sys.path.insert(0,'experiments')
from code_dependent_puncture import run
r=run()
assert r['canonical_full_len']==9 and r['canonical_min_sample']==9
assert r['canonical_preserving_samples']==[(0,1,2,3,4,5,6,7,8)]
assert r['random_(base_delta,min_sample)_histogram']=={
    (1,1):7,(2,4):13,(3,16):6,(2,8):6,(3,9):5,(2,9):3}
print('code-dependent puncture claims verified by exhaustive subset/codeword enumeration')
