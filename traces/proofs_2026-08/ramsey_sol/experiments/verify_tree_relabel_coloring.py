#!/usr/bin/env python3
import itertools,json,sys
p=sys.argv[1] if len(sys.argv)>1 else'experiments/tree_n5_k7.json';r=json.load(open(p));n=r['n'];k=r['k'];S=[(tuple(p),a,b) for p,a,b in r['states']];mp=dict(zip(S,r['colors']));V=list(itertools.permutations(range(n)))
def c(x,y):
 i=next(i for i in range(n) if x[i]!=y[i]);return mp[x[:i],min(x[i],y[i]),max(x[i],y[i])]
t=0
for i,x in enumerate(V):
 for j,y in enumerate(V[:i]):
  xy=c(x,y)
  for z in V[:j]:t+=1;assert not(xy==c(x,z)==c(y,z))
print(f'verified tree-relabel {k}-color K_{len(V)}, {t} triangles, base {len(V)**(1/k):.9f}')
