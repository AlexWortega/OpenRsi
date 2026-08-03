#!/usr/bin/env python3
"""Verify elementary output-size tradeoff for explicit full-view columns."""
from __future__ import annotations
import math

def run():
 rows=[]
 for N in (16,32,64,128,256,1024):
  for c in (1,2,4,8):
   r=math.ceil(c*math.log2(N))
   cols=2**r
   rows.append((N,c,r,cols,cols<=N**(c+1)))
   assert cols>=N**c
 # To get per-scope support penalty 2^r=N^c one needs r>=c log2 N,
 # and explicit columns for all views already cost at least N^c per scope.
 print({'checks':len(rows),'identity':'2^ceil(c log2 N) >= N^c',
  'consequence':'logarithmic full-view arity is polynomial-size but spends the same exponent in output size',
  'sample':rows[:6]})
if __name__=='__main__':run()
