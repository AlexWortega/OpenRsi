#!/usr/bin/env python3
"""Exact small test: zero-constant polynomials avoiding a symmetric sum-free interval."""
from itertools import product

def interval_S(p):
 # centered middle third: integers with p/3 < representative < 2p/3
 return {x for x in range(p) if p/3 < x < 2*p/3}
def sumfree(S,p):return all((a+b)%p not in S for a in S for b in S)
def first_avoider(p):
 S=interval_S(p);assert S=={(-x)%p for x in S} and sumfree(S,p)
 # coefficient tuple c1..cd, constant zero
 for d in range(1,p):
  tested=0
  for cs in product(range(p),repeat=d):
   if cs[-1]==0:continue
   tested+=1
   vals=[]
   for x in range(p):
    y=0
    for c in reversed(cs):y=(y*x+c)%p
    # above evaluates c1 + c2*x... then multiply x for zero constant
    y=y*x%p;vals.append(y)
   if all(y not in S for y in vals):return S,d,cs,vals,tested
 return S,None,None,None,None
for p in [5,7,11,13]:
 S,d,cs,vals,n=first_avoider(p)
 print('p',p,'S',sorted(S),'first_avoiding_degree',d,'coeffs',cs,'values',vals,'last_layer_tested',n)
