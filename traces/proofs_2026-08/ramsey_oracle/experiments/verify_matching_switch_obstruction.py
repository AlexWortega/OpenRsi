#!/usr/bin/env python3
"""Finite local check underlying the symmetric matching hypergraph obstruction."""
from itertools import combinations
V=range(4)
pairings=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
def partner(M):
 p=[None]*4
 for a,b in M:p[a]=b;p[b]=a
 return p
P=list(map(partner,pairings));triples=set(combinations(V,3))
# For each pair of pairings, candidate separating triples are exactly all four triples.
for x,y in combinations(P,2):
 cand={tuple(sorted((i,x[i],y[i]))) for i in V}
 assert cand==triples,(x,y,cand)
# If all four triples are edges, each vertex link contains the triangle on the other 3.
for i in V:
 link={tuple(sorted(set(t)-{i})) for t in triples if i in t}
 assert link==set(combinations([x for x in V if x!=i],2))
print('PASS: four-vertex matching switches force a hyperedge, while all four hyperedges force a link triangle')
