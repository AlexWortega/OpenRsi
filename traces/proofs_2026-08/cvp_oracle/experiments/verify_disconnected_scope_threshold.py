#!/usr/bin/env python3
"""Verify deterministic random-scope feasibility table by exact GF(2) elimination."""
import sys
sys.path.insert(0,'experiments')
from disconnected_scope_threshold import run
r=run(trials=5)
summary={(x['n'],x['d'],x['count']):(x['feasible'],x['infeasible']) for x in r}
assert summary=={
(5,2,5):(2,3),(5,2,10):(0,5),(5,3,5):(0,5),(5,3,10):(0,5),
(6,2,6):(4,1),(6,2,12):(0,5),(6,3,6):(0,5),(6,3,12):(0,5),
(7,2,7):(4,1),(7,2,14):(0,5),(7,3,7):(1,4),(7,3,14):(0,5),
(8,2,8):(5,0),(8,2,16):(2,3),(8,3,8):(2,3),(8,3,16):(0,5),
(9,2,9):(5,0),(9,2,18):(2,3),(9,3,9):(1,4),(9,3,18):(0,5),
(10,2,10):(5,0),(10,2,20):(1,4),(10,3,10):(2,3),(10,3,20):(0,5)}
print('random disconnected-scope threshold table verified exactly')
