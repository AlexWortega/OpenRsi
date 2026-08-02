#!/usr/bin/env python3
"""Verify the n=6 matching-partner correlated code."""
import json
from itertools import combinations
D=json.load(open('experiments/matching_partner_n6.json'));n=D['n']
H=[{tuple(e) for e in G} for G in D['graphs']]
def matchings(xs):
 xs=tuple(xs)
 if not xs:yield ();return
 a=xs[0]
 for j in range(1,len(xs)):
  b=xs[j]
  for t in matchings(xs[1:j]+xs[j+1:]):yield ((a,b),)+t
MS=list(matchings(range(n)))
def P(M):
 p=[None]*n
 for a,b in M:p[a]=b;p[b]=a
 return p
W=list(map(P,MS))
for i in range(n):
 for a,b,c in combinations(range(n),3):
  assert not all(tuple(sorted(e)) in H[i] for e in [(a,b),(a,c),(b,c)])
for x,y in combinations(W,2):
 assert any(tuple(sorted((x[i],y[i]))) in H[i] for i in range(n) if x[i]!=y[i])
print('PASS: all 15 perfect matchings of K6 form a 6-coordinate separated code; every coordinate graph is triangle-free; base',len(W)**(1/n))
