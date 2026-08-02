#!/usr/bin/env python3
"""Verify the explicit size-12 Grötzsch strong-cube code without third-party packages."""
import json
from itertools import combinations
EDGES={tuple(sorted(e)) for e in [(0,1),(0,4),(0,6),(0,9),(1,2),(1,5),(1,7),(2,3),(2,6),(2,8),(3,4),(3,7),(3,9),(4,5),(4,8),(5,10),(6,10),(7,10),(8,10),(9,10)]}
with open('experiments/grotzsch_cube_code.json') as f: code=[tuple(x) for x in json.load(f)]
assert len(code)==12==len(set(code))
assert all(len(w)==3 and all(0<=x<11 for x in w) for w in code)
for a,b in combinations(code,2):
    assert any(tuple(sorted((a[i],b[i]))) in EDGES for i in range(3))
# H is triangle-free, equivalently G=complement(H) has independence at most two.
for a,b,c in combinations(range(11),3):
    assert not all(tuple(sorted(e)) in EDGES for e in ((a,b),(a,c),(b,c)))
print('verified: triangle-free Grötzsch graph and 12-word strong-cube independent code')
