#!/usr/bin/env python3
"""Independent verifier for UT(n,2) symmetric product-free partitions."""
import json,sys,itertools
path=sys.argv[1] if len(sys.argv)>1 else 'experiments/ut5_k10.json';r=json.load(open(path));n=r['n'];k=r['k'];N=1<<(n*(n-1)//2);O=r['orbits'];colors=r['colors']
pos=[(i,j) for i in range(n) for j in range(i+1,n)];ix={p:t for t,p in enumerate(pos)}
def mul(x,y):
 z=x^y
 for i in range(n):
  for j in range(i+1,n):
   v=0
   for h in range(i+1,j):v^=((x>>ix[i,h])&1)&((y>>ix[h,j])&1)
   z^=v<<ix[i,j]
 return z
def inv(x):
 # independent brute recurrence solving x*y=identity by increasing diagonal gap
 y=0
 for gap in range(1,n):
  for i in range(n-gap):
   j=i+gap;v=(x>>ix[i,j])&1
   for h in range(i+1,j):v^=((x>>ix[i,h])&1)&((y>>ix[h,j])&1)
   y|=v<<ix[i,j]
 assert mul(x,y)==mul(y,x)==0
 return y
flat=[x for o in O for x in o];assert len(flat)==len(set(flat))==N-1 and set(flat)==set(range(1,N));assert len(colors)==len(O) and all(0<=c<k for c in colors)
owner={x:i for i,o in enumerate(O) for x in o}
for o in O:assert set(o)=={o[0],inv(o[0])}
C=[{x for i,o in enumerate(O) if colors[i]==c for x in o} for c in range(k)]
for c,S in enumerate(C):
 assert all(inv(x) in S for x in S)
 for x in S:
  for y in S:
   z=mul(x,y);assert z==0 or z not in S,(c,x,y,z)
# Direct triangle checking is cubic and too large for order 1024; product-freeness
# is the exact algebraic check for all translated triangles.
print(f'verified UT({n},2), order {N}, {k} colors, class sizes {[len(s) for s in C]}, all within-class products checked')
