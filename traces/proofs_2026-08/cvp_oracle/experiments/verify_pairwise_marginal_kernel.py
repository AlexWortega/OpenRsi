#!/usr/bin/env python3
"""Verify parity-cube kernels survive all marginals below full arity."""
from __future__ import annotations
import itertools,numpy as np

def marginal_matrix(k,d):
 V=list(itertools.product((0,1),repeat=k));rows=[]
 for r in range(d+1):
  for S in itertools.combinations(range(k),r):
   for vals in itertools.product((0,1),repeat=r):
    rows.append([int(tuple(x[i] for i in S)==vals) for x in V])
 return np.array(rows,dtype=int),V

def run():
 table={};checks=0
 for k in range(2,9):
  parity=np.ones(2**k,dtype=int) # all vertices; signs collapse mod 2
  for d in range(k):
   M,V=marginal_matrix(k,d)
   assert np.all(M.dot(parity)%2==0)
   table[k,d]=(M.shape[0],M.shape[1]);checks+=1
  M,V=marginal_matrix(k,k)
  assert np.any(M.dot(parity)%2)
 print({'arity_range':[2,8],'proper_marginal_kernel_checks':checks,
        'statement':'all 2^k cube vertices vanish under every GF2 marginal of arity < k',
        'matrix_shapes':table})
if __name__=='__main__':run()
