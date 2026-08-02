#!/usr/bin/env python3
"""Test scalar statistics of relative permutations as product-free color classes."""
import itertools,argparse

def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 z=[0]*len(p)
 for i,x in enumerate(p):z[x]=i
 return tuple(z)
def stat(p,m):
 n=len(p)
 if m=='inversions':return sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
 if m=='invmodn':return sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%n
 if m=='support':return sum(p[i]!=i for i in range(n))
 if m=='cycles':
  seen=set();z=0
  for i in range(n):
   if i not in seen:
    z+=1;j=i
    while j not in seen:seen.add(j);j=p[j]
  return n-z
 if m=='maxdisp':return max(abs(i-p[i]) for i in range(n))
 if m=='sumdisp':return sum(abs(i-p[i]) for i in range(n))//2
 if m=='lis':
  D=[]
  for x in p:
   import bisect;j=bisect.bisect_left(D,x)
   if j==len(D):D.append(x)
   else:D[j]=x
  return n-len(D)
 if m=='rankgf2':
  rows=[(1<<i)^(1<<p[i]) for i in range(n)];rank=0
  for b in range(n):
   z=next((x for x in range(rank,n) if rows[x]>>b&1),None)
   if z is not None:
    rows[rank],rows[z]=rows[z],rows[rank]
    for x in range(n):
     if x!=rank and rows[x]>>b&1:rows[x]^=rows[rank]
    rank+=1
  return rank
def test(n,m):
 P=list(itertools.permutations(range(n)));e=tuple(range(n));D={}
 for p in P:
  if p!=e:D.setdefault(stat(p,m),[]).append(p)
 for c,S in D.items():
  T=set(S)
  for x in S:
   for y in S:
    z=comp(x,y)
    if z in T:return False,len(D),(c,x,y,z)
 return True,len(D),None
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--max-n',type=int,default=8);z=a.parse_args()
 for m in ['inversions','invmodn','support','cycles','maxdisp','sumdisp','lis','rankgf2']:
  print('MODE',m)
  for n in range(3,z.max_n+1):
   r=test(n,m);print(n,r,flush=True)
   if not r[0]:break
