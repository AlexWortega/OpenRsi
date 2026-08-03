#!/usr/bin/env python3
"""Verify long-cycle full-overlap random-scope finite table."""
import sys
sys.path.insert(0,'experiments')
from random_scope_edge_full import run
r=run(d=3,mult=2,trials=3,seed=293)
assert [(x['n'],x['feasible'],x['infeasible']) for x in r]==[
 (8,0,3),(12,0,3),(16,1,2),(20,0,3),(24,3,0),(30,3,0)]
assert all(x['max_views']==27 for x in r)
print('long-cycle random-scope claims verified by exact GF(2) elimination')
