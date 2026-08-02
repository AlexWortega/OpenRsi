#!/usr/bin/env python3
# Question: do locally-(g-1) seeds decompose recursively by the unique missing color, suggesting a general construction?
import json,collections,itertools,networkx as nx
for N,g,s in [(26,5,4),(57,6,5)]:
 D=json.load(open(f'experiments/local_{N}_g{g}_s{s}.json'));P=[set(x) for x in D['palettes']];E={tuple(map(int,k.split(','))):v for k,v in D['edge_colors'].items()};miss=[next(iter(set(range(g))-x)) for x in P]
 print('\nN,g,s',N,g,s,'missing groups',collections.Counter(miss))
 for a in range(g):
  V=[i for i,x in enumerate(miss) if x==a]; used={E[tuple(sorted((u,v)))] for u,v in itertools.combinations(V,2)}
  print(' group',a,'size',len(V),'internal colors',sorted(used),'missing internal',sorted(set(range(g))-used))
 # Quotient majority color between each group pair and purity.
 for a,b in itertools.combinations(range(g),2):
  vals=[E[tuple(sorted((u,v)))] for u in range(N) if miss[u]==a for v in range(N) if miss[v]==b];c,n=collections.Counter(vals).most_common(1)[0]
  print(' pair',a,b,'majority',c,'purity',n/len(vals))
