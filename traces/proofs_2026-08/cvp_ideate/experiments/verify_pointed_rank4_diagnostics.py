#!/usr/bin/env python3
"""Rank-4 hostile test of the primitive-functional sublattice signal.

Select homogeneous 3DM lattices of rank four (m=10), enumerate primitive
coefficient vectors in {-1,0,1}^4 and all primitive-functional rank-two pairs,
and search sparse mixed tensor coefficient matrices of support <=3 with signs.
This attacks extension of the rank-three signal before theorem-building.
"""
from __future__ import annotations
import itertools,math
import verify_highrank_integer_tensor as ht
import verify_tensor_subdeterminants as sd


def analyze(B):
 C=sd.coeff_vectors(4);V={c:sd.vec(B,c) for c in C};r1=[];r2=[]
 for c in C:
  u=V[c]
  if u[-1]!=0:r1.append((sd.dot(u,u),sd.support([u]),abs(u[-1]),c))
 for i,c in enumerate(C):
  u=V[c]
  for d in C[i+1:]:
   if not sd.rank2(c,d):continue
   v=V[d]
   if math.gcd(abs(u[-1]),abs(v[-1]))==1:
    r2.append((sd.det2(u,v),sd.support([u,v]),abs(u[-1]),abs(v[-1]),c,d))
 return min(r1),min(r2),len(C),len(r2)
def sparse_tensor(B,maxsupp=3):
 G=ht.tensor_basis(B);r=len(G);n=len(G[0]);best=None;arg=None;checked=0
 star=[g[-1] for g in G]
 for k in range(1,maxsupp+1):
  for S in itertools.combinations(range(r),k):
   for signs in itertools.product((-1,1),repeat=k):
    if sum(signs[a]*star[S[a]] for a in range(k))!=1:continue
    checked+=1
    v=tuple(sum(signs[a]*G[S[a]][j] for a in range(k)) for j in range(n))
    z=sd.dot(v,v)
    if best is None or z<best:best,arg=z,(S,signs,v)
 return best,arg,checked
def main():
 rec=[]
 for yes in [True,False]:
  fam=ht.sample(3,10,4,yes,20);assert len(fam)==20
  for T,B in fam:
   d,a=ht.pointed_min(B,2); diag=analyze(B);dt,at,c=sparse_tensor(B,3)
   rec.append(('Y' if yes else 'N',d,diag,dt,c,T,at));print(rec[-1][:-2])
 Y=[x for x in rec if x[0]=='Y'];N=[x for x in rec if x[0]=='N']
 summary={'Y_d':min(x[1] for x in Y),'N_d':min(x[1] for x in N),
  'Y_r1':min(x[2][0][0] for x in Y),'N_r1':min(x[2][0][0] for x in N),
  'Y_r2det':min(x[2][1][0] for x in Y),'N_r2det':min(x[2][1][0] for x in N),
  'Y_r2support':min(x[2][1][1] for x in Y),'N_r2support':min(x[2][1][1] for x in N),
  'Y_sparse_tensor':min(x[3] for x in Y),'N_sparse_tensor':min(x[3] for x in N),
  'min_sparse_checked':min(x[4] for x in rec),'coeff_vectors':Y[0][2][2]}
 print(summary)
 assert summary=={'Y_d':4,'N_d':6,'Y_r1':4,'N_r1':6,
  'Y_r2det':12,'N_r2det':20,'Y_r2support':6,'N_r2support':8,
  'Y_sparse_tensor':16,'N_sparse_tensor':36,'min_sparse_checked':451,
  'coeff_vectors':40}
 print('pointed rank4 diagnostics pass')
if __name__=='__main__':main()
