#!/usr/bin/env python3
"""Verify the universal GF(2) 2x2 marginal swap kernel."""
from __future__ import annotations
import itertools,random,numpy as np

def marginal_matrix(a,b):
 # rows: coverage, A values, B values; columns: pairs.
 pairs=list(itertools.product(range(a),range(b)));M=[]
 M.append([1]*len(pairs))
 for i in range(a):M.append([int(x==i) for x,y in pairs])
 for j in range(b):M.append([int(y==j) for x,y in pairs])
 return np.array(M,dtype=int),pairs

def run():
 checks=0
 for a in range(2,8):
  for b in range(2,8):
   M,pairs=marginal_matrix(a,b);idx={p:i for i,p in enumerate(pairs)}
   for i0,i1 in itertools.combinations(range(a),2):
    for j0,j1 in itertools.combinations(range(b),2):
     x=np.zeros(len(pairs),dtype=int)
     for p in ((i0,j0),(i0,j1),(i1,j0),(i1,j1)):x[idx[p]]=1
     # Even coverage and zero marginals: a 4-cycle kernel vector.
     assert np.all(M.dot(x)%2==0);checks+=1
 # Adding a kernel rectangle to any feasible odd table preserves all unary marginals.
 M,pairs=marginal_matrix(3,3);base=np.zeros(9,dtype=int);base[pairs.index((0,0))]=1
 rect=np.zeros(9,dtype=int)
 for p in ((0,0),(0,1),(1,0),(1,1)):rect[pairs.index(p)]=1
 assert np.array_equal(M.dot(base)%2,M.dot(base^rect)%2)
 print({'alphabet_sizes':'2..7 x 2..7','rectangle_kernel_checks':checks,
        'explicit_odd_table_supports':[int(base.sum()),int((base^rect).sum())],
        'consequence':'unary GF2 marginals never identify a joint table'})
if __name__=='__main__':run()
