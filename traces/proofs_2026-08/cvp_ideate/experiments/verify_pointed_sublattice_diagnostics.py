#!/usr/bin/env python3
"""Test the mutation: sublattices carrying the homogenizing functional.

For rank-3 homogeneous exact-cover lattices, enumerate primitive coefficient
vectors c in {-1,0,1}^3 and independent pairs.  Keep rank-1 directions with
s(c)!=0, and rank-2 pairs whose s-values have gcd one (the star functional is
primitive on the sublattice).  Compare ambient norm, support, and Gram
determinant on deterministic YES/NO families.
"""
from __future__ import annotations
import itertools,math
import verify_highrank_integer_tensor as ht
import verify_tensor_subdeterminants as sd


def main():
 q=3;rec=[]
 for yes in [True,False]:
  fam=ht.sample(q,9,3,yes,20);assert len(fam)==20
  for T,B in fam:
   C=sd.coeff_vectors(3);V={c:sd.vec(B,c) for c in C}
   r1=[];r2=[]
   for c in C:
    u=V[c]
    if u[-1]!=0:r1.append((sd.dot(u,u),sd.support([u]),abs(u[-1]),c))
   for i,c in enumerate(C):
    for d in C[i+1:]:
     if not sd.rank2(c,d):continue
     u,v=V[c],V[d]
     if math.gcd(abs(u[-1]),abs(v[-1]))==1:
      r2.append((sd.det2(u,v),sd.support([u,v]),abs(u[-1]),abs(v[-1]),c,d))
   assert r1 and r2
   rec.append(('Y' if yes else 'N',min(r1),min(r2),T))
 for x in rec:print(x[:3])
 Y=[x for x in rec if x[0]=='Y'];N=[x for x in rec if x[0]=='N']
 summary={'Y_r1_norm':min(x[1][0] for x in Y),'N_r1_norm':min(x[1][0] for x in N),
  'Y_r1_support':min(x[1][1] for x in Y),'N_r1_support':min(x[1][1] for x in N),
  'Y_r2_det':min(x[2][0] for x in Y),'N_r2_det':min(x[2][0] for x in N),
  'Y_r2_support':min(x[2][1] for x in Y),'N_r2_support':min(x[2][1] for x in N),
  'instances_each':20}
 print(summary)
 # Deterministic finite signal: requiring the homogenizing functional to be
 # primitive restores both rank-one and tested rank-two determinant/support gaps.
 assert summary=={'Y_r1_norm':4,'N_r1_norm':6,'Y_r1_support':4,'N_r1_support':6,
  'Y_r2_det':12,'N_r2_det':20,'Y_r2_support':6,'N_r2_support':8,
  'instances_each':20}
 print('pointed sublattice diagnostics pass')
if __name__=='__main__':main()
