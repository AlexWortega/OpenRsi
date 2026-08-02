#!/usr/bin/env python3
"""Finite checks for tensor fitting-rank obstruction and bilinear certificate."""
from itertools import product

def rank_mod(A,p):
 A=[row[:] for row in A];m=len(A);n=len(A[0]) if m else 0;r=0
 for c in range(n):
  z=next((i for i in range(r,m) if A[i][c]%p),None)
  if z is None:continue
  A[r],A[z]=A[z],A[r];iv=pow(A[r][c]%p,-1,p)
  A[r]=[(x*iv)%p for x in A[r]]
  for i in range(m):
   if i!=r and A[i][c]%p:
    a=A[i][c]%p;A[i]=[(x-a*y)%p for x,y in zip(A[i],A[r])]
  r+=1
 return r
# H=K2, fitting matrix identity. All binary words are separated, tensor bound tight.
for m in range(1,7):
 X=list(product(range(2),repeat=m));B=[[int(i==j) for j in range(2)] for i in range(2)]
 M=[[1]*len(X) for _ in X]
 for a,x in enumerate(X):
  for b,y in enumerate(X):
   for i in range(m):M[a][b]*=B[x[i]][y[i]]
 assert rank_mod(M,2)==len(X)==2**m
# Binary alternating bilinear predicate on F2^4: R(u,v)=u1v2+u2v1+u3v4+u4v3.
V=list(product(range(2),repeat=4))
def R(u,v):return (u[0]*v[1]+u[1]*v[0]+u[2]*v[3]+u[3]*v[2])%2
BM=[[1^R(u,v) for v in V] for u in V]
assert all(R(v,v)==0 for v in V)
assert rank_mod(BM,2)<=5
assert all(BM[i][j]==0 for i,u in enumerate(V) for j,v in enumerate(V) if R(u,v))
print('PASS: tensor bound tight for K2 through m=6; F2^4 bilinear fitting rank',rank_mod(BM,2),'<=5')
