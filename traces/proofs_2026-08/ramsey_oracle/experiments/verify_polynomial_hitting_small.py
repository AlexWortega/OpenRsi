#!/usr/bin/env python3
"""Exhaustive finite verification of low-degree polynomial avoiders."""
from itertools import product

def symmetric_sumfree_sets(p):
 out=[]
 for mask in range(1,1<<(p-1)):
  S={x for x in range(1,p) if mask>>(x-1)&1}
  if S!={(-x)%p for x in S}:continue
  if all((a+b)%p not in S for a in S for b in S):out.append(S)
 return out

def min_avoider_degree(p,S,limit=3):
 for d in range(1,limit+1):
  for cs in product(range(p),repeat=d):
   if cs[-1]==0:continue
   values={sum(c*pow(x,i+1,p) for i,c in enumerate(cs))%p for x in range(p)}
   if values.isdisjoint(S):return d
 return None
expected={5:(2,{2:2}),7:(2,{2:3}),11:(4,{3:5}),13:(4,{2:6,3:3})}
for p,(size,hist_expected) in expected.items():
 sets=symmetric_sumfree_sets(p);mx=max(map(len,sets));hist={}
 for S in sets:
  if len(S)==mx:
   d=min_avoider_degree(p,S);hist[d]=hist.get(d,0)+1
 assert (mx,hist)==(size,hist_expected),(p,mx,hist)
 print('p',p,'maximum_size',mx,'degree_histogram',hist)
print('PASS: every maximum-cardinality symmetric sum-free set at p=5,7,11,13 has a degree<=3 zero-constant polynomial avoider')
