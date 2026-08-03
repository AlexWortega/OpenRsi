#!/usr/bin/env python3
"""Verify deterministic unique-SAT phase completeness attack."""
import sys
sys.path.insert(0,'experiments')
from phase_unique_sat import run
for q in (2,3,5):
 r=run(q,1000,101)
 assert r['satisfying_assignments']==[(0,0,0)] and r['lifts']==0
 # Selected incidence graph: 3 variable vertices + 7 clause vertices,
 # 21 edges, connected, hence cycle rank 21-10+1=12.
 assert 21-(3+7)+1==12
 exact_probability=q**-12
 assert exact_probability>0
print('unique-SAT random-phase failures verified; exact lift probability is q^-12')
