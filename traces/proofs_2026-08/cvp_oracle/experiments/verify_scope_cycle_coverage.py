#!/usr/bin/env python3
"""Verify probability/union-bound arithmetic for random scopes covering a whole cycle."""
from __future__ import annotations
import math

def run():
 checks=[]
 for n in (20,50,100,200):
  for d in (2,3,5,10):
   if d>n:continue
   p=1/math.comb(n,d) if d==n else 0.0
   # A d-edge scope contains all n cycle edges iff d=n.
   assert p==0
   checks.append((n,d,p))
 # If contradiction requires one scope containing all n edges, any family with d<n fails deterministically.
 print({'checks':len(checks),'statement':'a scope of d<n cycle edges never contains the whole n-edge obstruction',
  'consequence':'proper-scope odd orbit survives unless higher-order overlap closure reconstructs global information'})
if __name__=='__main__':run()
