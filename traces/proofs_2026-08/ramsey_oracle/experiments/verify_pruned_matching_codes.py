#!/usr/bin/env python3
"""Verify saved pruned perfect-matching partner codes."""
import json
from itertools import combinations
for n in [8,10,12]:
 D=json.load(open(f'experiments/pruned_matching_n{n}.json'));W=D['words'];G=[{tuple(e) for e in H} for H in D['graphs']]
 assert all(len(set(w))==n and all(w[w[i]]==i and w[i]!=i for i in range(n)) for w in W)
 for i in range(n):
  for a,b,c in combinations(range(n),3):assert not all(tuple(sorted(e)) in G[i] for e in [(a,b),(a,c),(b,c)])
 for x,y in combinations(W,2):assert any(tuple(sorted((x[i],y[i]))) in G[i] for i in range(n) if x[i]!=y[i])
 print('n',n,'N',len(W),'base',len(W)**(1/n))
print('PASS: saved pruned matching partner codes are separated by triangle-free coordinate graphs')
