#!/usr/bin/env python3
"""Test edge colors on F_q^d using first nonzero difference plus bilinear endpoint data."""
import itertools,argparse

def test(q,d,mode):
 V=list(itertools.product(range(q),repeat=d))
 def c(x,y):
  z=tuple((a-b)%q for a,b in zip(x,y));i=next(i for i,a in enumerate(z) if a)
  if mode=='firstsum':return(i,(x[i]+y[i])%q)
  if mode=='firstprod':return(i,x[i]*y[i]%q)
  if mode=='dot':return(i,sum(a*b for a,b in zip(x,y))%q)
  if mode=='symp' and d%2==0:return(i,sum((x[2*j]*y[2*j+1]+y[2*j]*x[2*j+1]) for j in range(d//2))%q)
  if mode=='quad':return(i,(sum(a*a for a in x)+sum(a*a for a in y))%q)
 for i,x in enumerate(V):
  for j,y in enumerate(V[:i]):
   xy=c(x,y)
   for z in V[:j]:
    if xy==c(x,z)==c(y,z):return False,(x,y,z,xy)
 return True,len({c(x,y) for i,x in enumerate(V) for y in V[:i]})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--max-v',type=int,default=400);a=p.parse_args()
 for q in [2,3,5,7]:
  for d in range(1,7):
   if q**d>a.max_v:continue
   for m in ['firstsum','firstprod','dot','symp','quad']:
    if m=='symp' and d%2:continue
    r=test(q,d,m);print(q,d,m,r,flush=True)
