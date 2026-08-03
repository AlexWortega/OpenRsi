#!/usr/bin/env python3
"""Verify deterministic random-scope coverage statistics."""
import sys
sys.path.insert(0,'experiments')
from random_scope_coverage_stats import run
r=run()
assert r[12]['avg_uncovered_adjacent_pairs']==3.89
assert r[24]['avg_uncovered_adjacent_pairs']==14.26
assert r[30]['avg_uncovered_adjacent_pairs']==19.24
assert r[60]['avg_total_adjacent_pair_hits']==12.65
assert r[100]['avg_uncovered_adjacent_pairs']==88.51
assert all(r[n]['prob_all_adjacent_pairs_covered']==0 for n in (24,30,60,100))
print('random-scope coverage statistics verified')
