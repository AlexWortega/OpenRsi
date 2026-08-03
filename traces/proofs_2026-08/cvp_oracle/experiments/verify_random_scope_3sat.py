#!/usr/bin/env python3
"""Verify random nonlocal-scope 3SAT exact-feasibility table."""
import sys
sys.path.insert(0,'experiments')
from random_scope_3sat import run
r1=run('all8',3,8,20,271);r2=run('xor5',3,10,20,271);r3=run('k4',2,12,10,271)
assert (r1['exact_feasible'],r1['exact_infeasible'])==(0,20)
assert (r2['exact_feasible'],r2['exact_infeasible'])==(0,20)
assert (r3['exact_feasible'],r3['exact_infeasible'])==(0,10)
print('random-scope 3SAT finite table verified by exact GF(2) elimination')
