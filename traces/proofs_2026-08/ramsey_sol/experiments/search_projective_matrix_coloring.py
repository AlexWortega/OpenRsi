#!/usr/bin/env python3
"""Test determinant/rank color rules on matrix vertex spaces over F_q."""
import itertools

def det2(A,B,q):return(A[0]*B[1]-A[1]*B[0])%q
def test(q,mode):
 V=list(itertools.product(range(q),repeat=2))
 def c(x,y):
  d=((x[0]-y[0])%q,(x[1]-y[1])%q)
  if mode=='slope':return d[1]*pow(d[0],-1,q)%q if d[0]else q
  if mode=='quad':return(d[0]*d[0]+d[1]*d[1])%q
  if mode=='prod':return d[0]*d[1]%q
  if mode=='support':return(d[0]!=0,d[1]!=0)
 for i,x in enumerate(V):
  for j,y in enumerate(V[:i]):
   z=c(x,y)
   for w in V[:j]:
    if z==c(x,w)==c(y,w):return False,(x,y,w,z)
 return True,len({c(x,y)for i,x in enumerate(V)for y in V[:i]})
for q in [3,5,7,11,13,17,19]:
 for m in ['slope','quad','prod','support']:print(q,m,test(q,m),flush=True)
