#!/usr/bin/env python3
"""Verify explicit huge-scale exact-fiber integer CVP cheats."""
import sys
sys.path.insert(0,'experiments')
from scaled_integer_cvp import run
r=run()
assert [x['cheat_squared']-x['yes_baseline_squared'] for x in r]==[2]*5
assert all(x['scale_M']==10**6 and x['violated_clauses']==1 for x in r)
assert r[-1]['distance_ratio_upper_bound']<1.0005
print('scaled integer CVP finite claims verified by exact residual evaluation')
