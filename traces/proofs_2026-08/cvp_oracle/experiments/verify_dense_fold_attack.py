#!/usr/bin/env python3
"""Verify deterministic finite claims from dense_fold_attack.py."""
import sys
sys.path.insert(0, 'experiments')
from dense_fold_attack import run
r = run()
assert r['base_delta'] == 2
assert r['full_tensor_delta'] == 4
assert r['orbit_outputs'] == 6
assert r['orbit_fold_delta'] == 2
assert r['orbit_pure_weights'] == [2, 2]
assert r['random_dense_delta_histogram'] == {2: 118, 1: 52, 3: 28, 4: 2}
assert r['arbitrary_below_pure_examples'] == [(2, 3, 4), (1, 3, 4), (2, 3, 4)]
print('dense-fold finite claims verified exactly by GF(2) enumeration')
