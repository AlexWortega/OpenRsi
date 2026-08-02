#!/usr/bin/env python3
"""Test O(n) color rules on GL(n,2) via first moved vector/subspace; exhaustive tiny n."""
import itertools

def rank(cols,n):
 B=[0]*n;r=0
 for x in cols:
  y=x
  while y:
   b=y.bit_length()-1
   if B[b]:y^=B[b]
   else:B[b]=y;r+=1;break
 return r
def mats(n):
 return [x for x in itertools.product(range(1,1<<n),repeat=n)if rank(x,n)==n]
def app(A,x):
 z=0
 for i,a in enumerate(A):
  if x>>i&1:z^=a
 return z
def mul(A,B):return tuple(app(A,b)for b in B)
def lab(A,n,m):
 if m=='basisfirst':
  i=next(i for i,a in enumerate(A)if a!=1<<i);return(i,A[i])
 if m=='basisindex':return next(i for i,a in enumerate(A)if a!=1<<i)
 if m=='vectorfirst':
  x=next(x for x in range(1,1<<n)if app(A,x)!=x);return(x,app(A,x))
 if m=='weight':
  i=next(i for i,a in enumerate(A)if a!=1<<i);return(i,A[i].bit_count())
def test(n,m):
 G=mats(n);e=tuple(1<<i for i in range(n));D={}
 for A in G:
  if A!=e:D.setdefault(lab(A,n,m),[]).append(A)
 for c,S in D.items():
  T=set(S)
  for x in S:
   for y in S:
    z=mul(x,y)
    if z in T:return False,len(D),(c,x,y,z)
 return True,len(D),None
for n in [2,3]:
 for m in ['basisfirst','basisindex','vectorfirst','weight']:print(n,m,test(n,m),flush=True)
