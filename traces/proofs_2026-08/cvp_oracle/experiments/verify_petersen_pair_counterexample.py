#!/usr/bin/env python3
"""Verify explicit Petersen all-pairs counterexample exactly."""
import sys
sys.path.insert(0,'experiments')
from petersen_pair_counterexample import run
r=run()
assert r=={'vertices':10,'edges':15,'groups':55,'shape':(23680,2925),'all_ones_weight':2925,
 'group_count_histogram':{9:10,27:15,81:30},'elimination_solution_weight':367,'unsat_rhs_sum_mod3':1}
print('Petersen all-pairs counterexample verified exactly')
