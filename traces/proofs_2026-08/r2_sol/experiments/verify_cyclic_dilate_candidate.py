#!/usr/bin/env python3
# Question: does a cyclic dilate-cover candidate actually give a triangle-free m-coloring of K_p?
import json
D=json.load(open('experiments/cyclic_dilate_codes.json'))
for r in D:
 p=r['p'];S=set(r['S']);A=r['multipliers']
 assert 0 not in S and all((-x)%p in S for x in S)
 assert all((x+y)%p not in S for x in S for y in S)
 cover=set().union(*({a*x%p for x in S} for a in A))
 assert cover==set(range(1,p))
 # Color each nonzero difference by its first covering multiplier.
 col={d:next(i for i,a in enumerate(A) if d*pow(a,-1,p)%p in S) for d in range(1,p)}
 assert all(col[d]==col[-d%p] for d in range(1,p))
 for x in range(p):
  for y in range(x+1,p):
   for z in range(y+1,p):
    assert len({col[(y-x)%p],col[(z-x)%p],col[(z-y)%p]})>1
 print('verified',p,'vertices',len(A),'colors','base',p**(1/len(A)))
