#!/usr/bin/env python3
"""Test sign-of-first-nonzero-coordinate product-free classes in torsion-free nilpotent groups."""
# Heisenberg over bounded integer boxes: color by index and sign of first nonzero Malcev coordinate.
import itertools

def mul(x,y):a,b,c=x;d,e,f=y;return(a+d,b+e,c+f+a*e)
def inv(x):a,b,c=x;return(-a,-b,-c+a*b)
def col(x,order):
 z=[x[i]for i in order];j=next(j for j,a in enumerate(z)if a);return(j,z[j]>0)
for order in itertools.permutations(range(3)):
 bad=None
 G=list(itertools.product(range(-4,5),repeat=3));e=(0,0,0)
 for x in G:
  if x==e:continue
  for y in G:
   if y==e:continue
   z=mul(x,y)
   if z!=e and max(map(abs,z))<=20 and col(x,order)==col(y,order)==col(z,order):bad=(x,y,z,col(x,order));break
  if bad:break
 print(order,'OK bounded'if bad is None else('FAIL',bad))
