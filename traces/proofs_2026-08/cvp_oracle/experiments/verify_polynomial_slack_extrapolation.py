#!/usr/bin/env python3
"""Verify finite-difference extrapolation for degree-d slack interfaces on count values."""
from __future__ import annotations
import math,random,numpy as np

def coeffs(d):
 # Lagrange coefficients expressing p(0) from p(1),...,p(d+1).
 return [(-1)**(c+1)*math.comb(d+1,c) for c in range(1,d+2)]
def run(seed=181):
 rng=random.Random(seed);checks=0
 for d in range(1,8):
  lam=coeffs(d);assert sum(lam)==1
  for _ in range(100):
   # Random module-valued polynomial p(c) of degree <=d.
   A=np.array([[rng.randrange(-9,10) for _ in range(d+1)] for _ in range(5)],dtype=object)
   def p(c):return A.dot(np.array([c**j for j in range(d+1)],dtype=object))
   rhs=sum((l*p(c) for c,l in enumerate([0]+lam) if c),np.zeros(5,dtype=object))
   assert np.all(rhs==p(0))
   for mod in (2,3,5,6,11):assert np.all(np.asarray(rhs-p(0),dtype=int)%mod==0)
   checks+=1
 print({'degrees':'1..7','checks':checks,'largest_l1_coefficient_sum':sum(abs(x) for x in coeffs(7)),
        'formula':'p(0)=sum_{c=1}^{d+1} (-1)^(c+1) binom(d+1,c) p(c)'})
if __name__=='__main__':run()
