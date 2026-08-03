#!/usr/bin/env python3
"""Verify all-pair coloring hierarchy finite attacks."""
import sys
sys.path.insert(0,'experiments')
from all_pair_coloring import run
r=run()
assert all(not x['exact_feasible'] for x in r)
assert [(x['graph'],x['nparam'],x['groups']) for x in r]==[('K4',None,21),('K5',None,55),('wheel',5,55),('wheel',7,105)]
print('all-pair coloring claims verified by exact GF(2) elimination')
