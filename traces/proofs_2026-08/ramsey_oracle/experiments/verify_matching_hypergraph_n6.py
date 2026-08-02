#!/usr/bin/env python3
"""Verify finite symmetric perfect-matching code at n=6."""
import json
from itertools import combinations
D=json.load(open('experiments/matching_hypergraph_n6.json'));n=D['n'];T={tuple(t) for t in D['triples']}
def matchings(xs):
 xs=tuple(xs)
 if not xs:yield ();return
 a=xs[0]
 for j in range(1,len(xs)):
  b=xs[j]
  for z in matchings(xs[1:j]+xs[j+1:]):yield ((a,b),)+z
def p(M):
 a=[None]*n
 for x,y in M:a[x]=y;a[y]=x
 return a
W=[p(M) for M in matchings(range(n))]
for i in range(n):
 E={tuple(sorted((a,b))) for a,b in combinations([z for z in range(n) if z!=i],2) if tuple(sorted((i,a,b))) in T}
 for a,b,c in combinations(range(n),3):assert not all(tuple(sorted(e)) in E for e in [(a,b),(a,c),(b,c)])
for x,y in combinations(W,2):assert any(tuple(sorted((i,x[i],y[i]))) in T for i in range(n) if x[i]!=y[i])
print('PASS: 8-triple 3-graph gives 15-word perfect-matching code in 6 triangle-free links')
