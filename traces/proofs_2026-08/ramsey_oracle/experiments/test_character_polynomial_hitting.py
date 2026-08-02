#!/usr/bin/env python3
"""Search multiplicative-character sum-free Cayley sets and polynomial avoiders."""
from itertools import product,combinations

def caps(p):
 vals=range(1,p);out=[]
 for mask in range(1,1<<(p-1)):
  S={x for x in vals if mask>>(x-1)&1}
  if S!={(-x)%p for x in S}:continue
  if all((a+b)%p not in S for a in S for b in S):out.append(S)
 return out
def avoider(p,S,maxd=4):
 for d in range(1,maxd+1):
  for cs in product(range(p),repeat=d):
   if cs[-1]==0:continue
   vals=[]
   for x in range(p):
    y=0
    for c in reversed(cs):y=(y*x+c)%p
    vals.append(y*x%p)
   if not set(vals)&S:return d,cs,vals
 return None
for p in [5,7,11,13]:
 C=caps(p);best=max(map(len,C),default=0)
 hist={}
 for S in C:
  if len(S)==best:
   a=avoider(p,S);hist[a[0] if a else None]=hist.get(a[0] if a else None,0)+1
 print('p',p,'symmetric_caps',len(C),'max',best,'avoider_degree_hist',hist)
