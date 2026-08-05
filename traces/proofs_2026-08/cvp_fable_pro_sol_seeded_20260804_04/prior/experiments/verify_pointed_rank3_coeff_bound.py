#!/usr/bin/env python3
"""Wider coefficient test of the primitive-functional rank-2 invariant.

For selected rank-3 homogeneous 3DM lattices, enumerate primitive coefficient
vectors in [-B,B]^3 modulo sign (B=3), and all independent pairs whose star
values have gcd one.  Compute minimum Gram determinant/support.  This attacks
whether the promising {-1,0,1} pointed-sublattice gap was a coefficient-box
artifact.
"""
from __future__ import annotations
import itertools,math
import verify_highrank_integer_tensor as ht
import verify_tensor_subdeterminants as sd


def coeffs(B):
 return sorted({sd.canon_sign(c) for c in itertools.product(range(-B,B+1),repeat=3) if any(c)})
def analyze(Basis,B):
 C=coeffs(B);V={c:sd.vec(Basis,c) for c in C};best1=None;best2=None;checked=0
 for c in C:
  u=V[c]
  if u[-1]!=0:
   z=(sd.dot(u,u),sd.support([u]),abs(u[-1]),c)
   best1=z if best1 is None or z<best1 else best1
 for i,c in enumerate(C):
  u=V[c]
  for d in C[i+1:]:
   if not sd.rank2(c,d):continue
   v=V[d]
   if math.gcd(abs(u[-1]),abs(v[-1]))!=1:continue
   checked+=1;z=(sd.det2(u,v),sd.support([u,v]),abs(u[-1]),abs(v[-1]),c,d)
   best2=z if best2 is None or z<best2 else best2
 return best1,best2,len(C),checked
def main():
 box=3;rec=[]
 for yes in [True,False]:
  fam=ht.sample(3,9,3,yes,10);assert len(fam)==10
  for T,B in fam:
   a=analyze(B,box);rec.append(('Y' if yes else 'N',a,T));print(rec[-1][:-1])
 Y=[x[1] for x in rec if x[0]=='Y'];N=[x[1] for x in rec if x[0]=='N']
 summary={'box':box,'coeff_vectors':Y[0][2],
  'min_pairs_checked':min(x[3] for x in Y+N),
  'Y_r1':min(x[0][0] for x in Y),'N_r1':min(x[0][0] for x in N),
  'Y_r2det':min(x[1][0] for x in Y),'N_r2det':min(x[1][0] for x in N),
  'Y_r2support':min(x[1][1] for x in Y),'N_r2support':min(x[1][1] for x in N)}
 print(summary)
 assert summary=={'box':3,'coeff_vectors':145,'min_pairs_checked':7480,
  'Y_r1':4,'N_r1':6,'Y_r2det':12,'N_r2det':20,
  'Y_r2support':6,'N_r2support':8}
 print('pointed rank3 coefficient-bound diagnostics pass')
if __name__=='__main__':main()
