#!/usr/bin/env python3
"""Verify explicit translation-invariant cyclic triangle-free colorings."""
import json,itertools
for p,k,path in [(127,5,'experiments/cyclic_127_5.json'),(251,6,'experiments/cyclic_251_6.json'),(509,7,'experiments/cyclic_509_7.json'),(1021,8,'experiments/cyclic_1021_8.json'),(2039,9,'experiments/cyclic_2039_9.json')]:
 C=[set(x) for x in json.load(open(path))]
 assert len(C)==k and set().union(*C)==set(range(1,p)) and sum(map(len,C))==p-1
 assert all(all((-x)%p in S for x in S) for S in C)
 assert all(all((x+y)%p not in S for x in S for y in S) for S in C)
 col={x:i for i,S in enumerate(C) for x in S}
 # Translation reduces every vertex triangle to nonzero differences a,b,b-a.
 # Check all ordered difference pairs in O(p^2), rather than O(p^3) vertices.
 for a in range(1,p):
  for b in range(1,p):
   if a!=b: assert len({col[a],col[b],col[(b-a)%p]})>1
 count=p*(p-1)*(p-2)//6
 print('verified cyclic K_%d with %d colors:'%(p,k),count,'triangles via all difference pairs; sizes',list(map(len,C)))
