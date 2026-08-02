#!/usr/bin/env python3
"""Test homomorphism/kernel-coset product-free partition mechanism in S_n.
A color class is a fiber of a statistic/homomorphism; catches identity-fiber obstruction.
"""
import itertools
# conceptual finite sanity: any nontrivial subgroup kernel contains x,x^-1 and identity product;
# identity is excluded, but if x has order >2 then x*x may stay same fiber only for quotient element g with g^2=g => g=e.
# Search quotient-fiber labels sign and action on blocks.
def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
for n in range(3,8):
 P=list(itertools.permutations(range(n)));e=tuple(range(n))
 for mode in ['sign','image0','sethalf']:
  def c(p):
   if mode=='sign':return parity(p)
   if mode=='image0':return p[0]
   h=n//2;return tuple(sorted(p[:h]))
  D={}
  for p in P:
   if p!=e:D.setdefault(c(p),[]).append(p)
  bad=next(((a,x,y,comp(x,y)) for a,S in D.items() for x in S for y in S if comp(x,y) in set(S)),None)
  print(n,mode,len(D),'OK' if bad is None else ('FAIL',bad),flush=True)
