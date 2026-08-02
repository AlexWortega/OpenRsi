#!/usr/bin/env python3
"""Falsify n-color diagonal compressions of permutation first-difference labels."""
import itertools,argparse

def check(n,mode,A=1,B=1):
 V=list(itertools.permutations(range(n)))
 def c(x,y):
  i=next(i for i in range(n) if x[i]!=y[i]);a,b=x[i],y[i]
  if mode=='sum':return (A*i+B*(a+b))%n
  if mode=='prod':return (A*i+B*a*b)%n
  if mode=='diff':return (A*i+B*min((a-b)%n,(b-a)%n))%n
  if mode=='xor':return i^(a^b)
 for i,x in enumerate(V):
  for j,y in enumerate(V[:i]):
   zc=c(x,y)
   for z in V[:j]:
    if zc==c(x,z)==c(y,z):return False,(x,y,z,zc)
 return True,None
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--max-n',type=int,default=7);a=p.parse_args()
 for n in range(3,a.max_n+1):
  for mode in ['sum','prod','diff','xor']:
   for A in range(n):
    for B in range(1,n):
     ok,w=check(n,mode,A,B)
     if ok:print('SUCCESS',n,mode,A,B,flush=True);break
    if ok:break
   if not ok:print('fail',n,mode,'last witness',w,flush=True)
