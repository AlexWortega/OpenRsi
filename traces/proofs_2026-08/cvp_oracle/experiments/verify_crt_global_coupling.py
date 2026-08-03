#!/usr/bin/env python3
"""Exact checks for the CRT-global coupling failure."""
import sys
sys.path.insert(0, 'experiments')
from crt_global_coupling import build, run

records = run((0, 1, 4, 10), 10**6)
for rec in records:
    B, t, z, info = build(rec['D'], rec['M'])
    # Full column rank is structural: identity rows pivot every b/slack column,
    # the final row pivots x, and each CRT row then pivots its private q_i.
    assert rec['structural_full_column_rank'] and B.shape[0] >= B.shape[1]
    assert all(int(v) == 0 for v in (B @ z - t)[:info['n'] + info['m']])
    assert rec['additive_false_clause_cost'] == 8
    assert rec['ratio_to_uniform_yes_radius_upper'] < 1.18
# The global CRT coefficient is intrinsically huge in this explicit family.
assert records[-1]['P'] > 10**30
print('CRT global-coupling failure verified exactly')
