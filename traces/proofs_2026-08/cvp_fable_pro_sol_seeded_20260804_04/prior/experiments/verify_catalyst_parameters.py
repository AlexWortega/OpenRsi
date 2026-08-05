#!/usr/bin/env python3
"""Exact parameter arithmetic for iterating fixed cyclic catalysts.

One catalyst step with phase length ell and correlation odd distance a maps
moving length n -> ell*n^2 and YES/NO distances d,b -> a*d^2,a*b^2.
This verifier checks closed forms, ratio squaring, and the resulting standard
rank exponent on representative growing additive-gap bases.
"""
from fractions import Fraction


def iterate(n,d,b,ell,a,k):
 hist=[]
 for i in range(k+1):
  hist.append((n,d,b,Fraction(b,d)))
  n,d,b=ell*n*n,a*d*d,a*b*b
 return hist

def closed(base,mult,k):
 # x_{i+1}=mult*x_i^2
 return mult**(2**k-1)*base**(2**k)
def main():
 checked=0;maxexp=[]
 for q in [3,5,10,30,100,300,1000]:
  n=q*q+q+1;d=q;b=q+2 # parity-sharp 3DM-style additive gap
  H=iterate(n,d,b,15,5,6)
  for k,(nk,dk,bk,r) in enumerate(H):
   assert nk==closed(n,15,k)
   assert dk==closed(d,5,k)
   assert bk==closed(b,5,k)
   assert r==Fraction(b,d)**(2**k)
   checked+=1
  # Best exponent log(gap)/log(rank) over these six levels.
  import math
  exps=[math.log(float(r))/math.log(nk) for nk,dk,bk,r in H if nk>1]
  maxexp.append((q,max(exps),exps[-1]))
 print(f'checked {checked} exact catalyst recurrence states')
 print('q, best standard rank exponent through level 6, level-6 exponent')
 for row in maxexp:print(row)
 # For growing q and n polynomially above q, the exponent decays.
 assert maxexp[-1][1] < maxexp[0][1]
if __name__=='__main__':main()
