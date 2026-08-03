#!/usr/bin/env python3
"""Verify all-pair/all-triple scope hierarchy on holonomy cycles."""
import sys
sys.path.insert(0,'experiments')
from all_d_scope_edge import run
r=run()
assert len(r)==11 and all(x['exact_feasible'] is False for x in r)
assert [(x['n'],x['d'],x['groups']) for x in r[-6:]]==[(12,2,78),(16,2,136),(20,2,210),(24,2,300),(30,2,465),(40,2,820)]
print('all-d-scope cycle claims verified by exact GF(2) elimination')
