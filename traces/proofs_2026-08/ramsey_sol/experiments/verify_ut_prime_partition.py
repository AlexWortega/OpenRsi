#!/usr/bin/env python3
import json,sys,itertools
p=sys.argv[1]if len(sys.argv)>1 else'experiments/ut3p5_k6.json';r=json.load(open(p));n=r['n'];q=r['p'];pos=[(i,j)for i in range(n)for j in range(i+1,n)];ix={z:t for t,z in enumerate(pos)};G=list(itertools.product(range(q),repeat=len(pos)));e=(0,)*len(pos)
def mul(x,y):
 z=[(x[t]+y[t])%q for t in range(len(pos))]
 for i in range(n):
  for j in range(i+1,n):
   for h in range(i+1,j):z[ix[i,j]]=(z[ix[i,j]]+x[ix[i,h]]*y[ix[h,j]])%q
 return tuple(z)
def inv(x):return next(y for y in G if mul(x,y)==mul(y,x)==e)
O=[[tuple(x)for x in o]for o in r['orbits']];flat=[x for o in O for x in o];assert set(flat)==set(G)-{e}and len(flat)==len(set(flat));C=[{x for i,o in enumerate(O)if r['colors'][i]==c for x in o}for c in range(r['k'])]
for c,S in enumerate(C):
 assert all(inv(x)in S for x in S)
 for x in S:
  for y in S:
   z=mul(x,y);assert z==e or z not in S,(c,x,y,z)
print(f'verified UT({n},{q}), order {len(G)}, {r["k"]} colors, sizes {[len(s)for s in C]}')
