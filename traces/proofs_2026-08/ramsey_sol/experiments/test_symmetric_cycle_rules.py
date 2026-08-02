#!/usr/bin/env python3
"""Test O(n)-ish product-free labels in symmetric groups based on cycle structure."""
import itertools,argparse

def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def cyc(p,i):
 C=[i];x=p[i]
 while x!=i:C.append(x);x=p[x]
 return C
def label(p,m):
 n=len(p);i=next(i for i in range(n) if p[i]!=i);C=cyc(p,i);L=len(C)
 if m=='length':return L
 if m=='lengthpar':return(L,i%2)
 if m=='lenorient':return(L,p[i]>i)
 if m=='leni':return(i,L)
 if m=='maxcycle':return(max(C),L)
 if m=='interval':return(min(C),max(C),L)
 if m=='cycleminlen':
  cs=[];seen=set()
  for a in range(n):
   if a not in seen:
    z=cyc(p,a);seen|=set(z)
    if len(z)>1:cs.append((min(z),len(z)))
  return min(cs)
def test(n,m):
 P=list(itertools.permutations(range(n)));e=tuple(range(n));D={}
 for p in P:
  if p!=e:D.setdefault(label(p,m),[]).append(p)
 for c,S in D.items():
  T=set(S)
  for x in S:
   for y in S:
    z=comp(x,y)
    if z in T:return False,len(D),(c,x,y,z)
 return True,len(D),None
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--max-n',type=int,default=8);z=a.parse_args()
 for m in ['length','lengthpar','lenorient','leni','maxcycle','interval','cycleminlen']:
  print('MODE',m)
  for n in range(3,z.max_n+1):
   r=test(n,m);print(n,r,flush=True)
   if not r[0] and n>=5:break
