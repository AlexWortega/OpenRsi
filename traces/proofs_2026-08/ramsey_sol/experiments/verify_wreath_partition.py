#!/usr/bin/env python3
import json,sys
from wreath2_partition import ops
p=sys.argv[1] if len(sys.argv)>1 else'experiments/wreath3_k7.json';r=json.load(open(p));N,mul,inv=ops(r['level']);O=r['orbits'];col=r['colors'];k=r['k'];flat=[x for o in O for x in o];assert N==r['order'] and set(flat)==set(range(1,N))and len(flat)==len(set(flat))
for o in O:assert set(o)=={o[0],inv(o[0])}
C=[{x for i,o in enumerate(O)if col[i]==c for x in o}for c in range(k)]
for c,S in enumerate(C):
 assert all(inv(x)in S for x in S)
 for x in S:
  for y in S:
   z=mul(x,y);assert z==0 or z not in S,(c,x,y,z)
tri=0
for x in range(N):
 for y in range(x):
  a=col[next(i for i,o in enumerate(O)if mul(inv(x),y)in o)]
  for z in range(y):
   tri+=1
   def ec(u,v):
    w=mul(inv(u),v);return col[next(i for i,o in enumerate(O)if w in o)]
   assert not(a==ec(x,z)==ec(y,z))
print(f'verified wreath level {r["level"]}, order {N}, {k} colors, {tri} triangles, sizes {[len(s)for s in C]}')
