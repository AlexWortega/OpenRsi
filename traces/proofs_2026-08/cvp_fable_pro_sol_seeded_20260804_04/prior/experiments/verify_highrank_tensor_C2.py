#!/usr/bin/env python3
"""Exact wider-box mixed tensor verification for selected rank-3 lattices.

Exhausts coefficient matrices in [-2,2]^9 (1,953,125 mixed tensors per
instance) on three deterministic YES and three NO homogeneous 3DM lattices.
This promotes the harvested background finite output to a reproducible
verify_*.py claim.
"""
from __future__ import annotations
import numpy as np
import verify_highrank_integer_tensor as v


def fast_tensor_min(B,C=2,chunk=200000):
 """Exact vectorized enumeration of [-C,C]^(r^2) via the tensor Gram matrix."""
 A=np.array(B,dtype=np.int64); Q=A@A.T; r=len(B)
 G=np.kron(Q,Q); star=A[:,-1]; functional=np.kron(star,star)
 total=(2*C+1)**(r*r);best=None
 powers=(2*C+1)**np.arange(r*r,dtype=np.int64)
 for lo in range(0,total,chunk):
  nums=np.arange(lo,min(total,lo+chunk),dtype=np.int64)[:,None]
  X=((nums//powers[None,:])%(2*C+1)-C).astype(np.int64)
  ok=(X@functional)==1
  if np.any(ok):
   Y=X[ok]; norms=np.sum((Y@G)*Y,axis=1); z=int(norms.min())
   best=z if best is None else min(best,z)
 return best,r*r,total


def main():
 rec=[]
 for yes in [True,False]:
  fam=v.sample(3,9,3,yes,3);assert len(fam)==3
  for T,B in fam:
   d,a=v.pointed_min(B,3)
   dt,r,states=fast_tensor_min(B,2)
   row=('Y' if yes else 'N',d,dt,r,states,T)
   print(row);rec.append(row)
 assert all(x[4]==1953125 and x[3]==9 for x in rec)
 assert all(x[2]==x[1]*x[1] for x in rec)
 assert [x[2] for x in rec if x[0]=='Y']==[16]*3
 assert [x[2] for x in rec if x[0]=='N']==[36]*3
 print('HIGHRANK_C2_PASS')
if __name__=='__main__':main()
