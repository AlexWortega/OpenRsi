#!/usr/bin/env python3
"""Verify pure-power-subcode and symmetric-representative finite claims."""
import sys
sys.path.insert(0,'experiments')
from pure_power_span import run
r=run()
assert r['canonical']=={
 1:{'rank':2,'delta':2,'expected_full':2,'length':3},
 2:{'rank':3,'delta':4,'expected_full':4,'length':9},
 3:{'rank':3,'delta':8,'expected_full':8,'length':27},
 4:{'rank':3,'delta':16,'expected_full':16,'length':81}}
assert r['canonical_symmetric']=={
 1:{'length':3,'rank':2,'delta':2},2:{'length':6,'rank':3,'delta':3},
 3:{'length':10,'rank':3,'delta':4},4:{'length':15,'rank':3,'delta':5},
 5:{'length':21,'rank':3,'delta':6}}
assert r['random_records']==50 and r['nonmultiplicative_records']==0
assert r['symmetric_lower_bound_failures']==0 and r['first_failures']==[]
print('pure-power finite claims verified by exact GF(2) enumeration')
