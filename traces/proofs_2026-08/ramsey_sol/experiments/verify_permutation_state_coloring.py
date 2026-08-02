#!/usr/bin/env python3
"""Independent verifier for a quotient of permutation first-difference labels."""
import itertools,json,sys
p=sys.argv[1] if len(sys.argv)>1 else 'experiments/permstate_n5_k7.json';r=json.load(open(p));n=r['n'];k=r['k'];labels=[tuple(x) for x in r['labels']];colors=r['colors'];assert len(labels)==len(colors) and all(0<=x<k for x in colors);mp=dict(zip(labels,colors));V=list(itertools.permutations(range(n)))
def c(a,b):
 i=next(i for i in range(n) if a[i]!=b[i]);return mp[i,min(a[i],b[i]),max(a[i],b[i])]
tri=0
for i,a in enumerate(V):
 for j,b in enumerate(V[:i]):
  ab=c(a,b)
  for h in range(j):
   tri+=1;d=V[h];assert not(ab==c(a,d)==c(b,d)),(a,b,d,ab)
print(f'verified {k}-coloring of K_{len(V)} on S_{n}; {tri} triangles; base {len(V)**(1/k):.9f}')
