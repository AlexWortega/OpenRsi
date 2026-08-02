#!/usr/bin/env python3
"""Verify degree of the four-switch conflict graph for small even n."""
from itertools import combinations
def matchings(xs):
 xs=tuple(xs)
 if not xs:yield ();return
 a=xs[0]
 for j in range(1,len(xs)):
  b=xs[j]
  for z in matchings(xs[1:j]+xs[j+1:]):yield ((a,b),)+z
def p(M,n):
 z=[None]*n
 for a,b in M:z[a]=b;z[b]=a
 return z
for n in [4,6,8,10]:
 W=[p(M,n) for M in matchings(range(n))];deg=[]
 for x in W:deg.append(sum(sum(a!=b for a,b in zip(x,y))==4 for y in W))
 expected=2*((n//2)*(n//2-1)//2)
 assert set(deg)=={expected}
 print(n,len(W),expected)
print('PASS: four-switch conflict degree is 2*binom(n/2,2) through n=10')
