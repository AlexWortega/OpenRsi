#!/usr/bin/env python3
"""Verify exact random-scope results on scalable padded cycle CNFs."""
import sys
sys.path.insert(0,'experiments')
from random_scope_padded_cycle import run
r=run()
assert [(x['n'],x['scope_clauses_d'],x['random_scope_multiplier'],x['exact_feasible']) for x in r]==[
 (3,2,1,True),(3,3,1,False),(4,2,1,True),(4,3,1,True),(4,3,2,False),(4,4,1,False),(5,3,1,True)]
assert [x['one_solution_weight'] for x in r if x['exact_feasible']]==[352,418,894,962]
print('padded-cycle random-scope claims verified by exact GF(2) elimination')
