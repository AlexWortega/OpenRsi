#!/usr/bin/env python3
"""Finite arithmetic checks for the tensor-catalyst exponent monotonicity lemma.

If a catalyst output code has length L and pointed moving distance a<=L, one
step maps outer rank proxy n to n^2 L and both YES/NO distances to a times their
squares.  The standard rank exponent log(b/d)/log n cannot increase.
"""
from fractions import Fraction
import math


def exponent(n,d,b):
    return math.log(Fraction(b,d))/math.log(n)

def main():
    checked=0
    for n in range(2,101):
      for d in range(1,n+1):
       for b in range(d+1,min(n, d+8)+1):
        e=exponent(n,d,b)
        for L in range(1,31):
         for a in range(1,L+1):
          ep=exponent(n*n*L,a*d*d,a*b*b)
          assert ep<=e+1e-15
          checked+=1
    print(f'checked {checked} exact-parameter catalyst exponent inequalities')
    assert checked>1_000_000
if __name__=='__main__':main()
