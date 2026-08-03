#!/usr/bin/env python3
"""Exact rank tests: nonlinear violation row kills local trades but is not unary-separable."""
from __future__ import annotations
import itertools,numpy as np

def rank2(rows):
 basis={}
 for row in rows:
  z=sum(int(b)<<i for i,b in enumerate(row))
  while z:
   p=z.bit_length()-1
   if p not in basis:basis[p]=z;break
   z^=basis[p]
 return len(basis)

def in_span(cols,t):
 # Rank of column family represented as bit-vectors.
 return rank2(cols)==rank2(cols+[t])

def signature(r,d):
 V=list(itertools.product((0,1),repeat=r));mons=[T for k in range(d+1) for T in itertools.combinations(range(r),k)]
 cols=[tuple(np.prod([x[i] for i in T],dtype=int) if T else 1 for T in mons) for x in V]
 return V,cols,mons

def run():
 table={}
 for r in range(3,9):
  V=list(itertools.product((0,1),repeat=r));u=(0,)*r
  legal=[i for i,x in enumerate(V) if any(x[:3])]
  for d in range(0,4):
   _,cols,mons=signature(r,d);table[r,d]=in_span([cols[i] for i in legal],cols[V.index(u)])
 # Cubic violation indicator cannot be a sum of unary functions: mixed third difference is nonzero.
 def viol(x):return (1-x[0])*(1-x[1])*(1-x[2])
 alt=sum(((-1)**sum(x))*viol(x) for x in itertools.product((0,1),repeat=3))
 assert abs(alt)==1
 # Degree <=2 is locally cheatable; degree 3 separates every forbidden extension from legal columns.
 assert all(table[r,d] for r in range(3,9) for d in range(3))
 assert all(not table[r,3] for r in range(3,9))
 result={'r_range':[3,8],'target_in_legal_span_by_degree':table,
         'cubic_mixed_difference':alt,'interpretation':'degree3 separates OR violation; unary interface cannot generate it'}
 print(result)
if __name__=='__main__':run()
