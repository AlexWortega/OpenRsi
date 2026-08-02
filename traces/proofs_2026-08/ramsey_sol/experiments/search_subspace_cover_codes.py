#!/usr/bin/env python3
"""Search linear maps L_i so every nonzero message maps into a fixed sum-free affine hyperplane.
This exact algebraic ansatz asks: for all u!=0, some coordinate has first bit 1 and remaining map arbitrary.
It reduces to covering F2^D\0 by m affine hyperplanes L_i(u)=1; tested for hidden impossibility.
"""
import itertools
for D in range(2,9):
 # Any linear functional has kernel; union of m complements covers iff intersection kernels={0}, requiring m>=D.
 # brute verify threshold.
 funcs=list(range(1,1<<D))
 for m in range(1,D+1):
  ok=False
  for F in itertools.combinations(funcs,m):
   if all(any((f&u).bit_count()%2 for f in F)for u in range(1,1<<D)):ok=True;break
  if ok:break
 print(D,'minimum coordinates',m,'base 2^(D/m)',2**(D/m))
