#!/usr/bin/env python3
"""Test non-inverse-closed relative-permutation rules using canonical lex edge orientation."""
import itertools

def comp(p,q):return tuple(p[q[i]]for i in range(len(p)))
def inv(p):
 z=[0]*len(p)
 for i,x in enumerate(p):z[x]=i
 return tuple(z)
def rel(x,y):return comp(inv(x),y)
def c(x,y,m):
 if y<x:x,y=y,x
 p=rel(x,y);n=len(p);i=next(i for i in range(n)if p[i]!=i);a=p[i]
 if m=='i':return i
 if m=='iaorder':return(i,a>i)
 if m=='diff':return(i,(a-i)%n)
 if m=='sum':return(i,(a+i)%n)
 if m=='a':return a
 if m=='cyclelen':
  L=1;z=p[i]
  while z!=i:L+=1;z=p[z]
  return(i,L)
def test(n,m):
 V=list(itertools.permutations(range(n)))
 for i,x in enumerate(V):
  for j,y in enumerate(V[:i]):
   z=c(x,y,m)
   for w in V[:j]:
    if z==c(x,w,m)==c(y,w,m):return False,(x,y,w,z)
 return True,len({c(x,y,m)for i,x in enumerate(V)for y in V[:i]})
for m in ['i','iaorder','diff','sum','a','cyclelen']:
 print('MODE',m)
 for n in range(3,8):
  r=test(n,m);print(n,r,flush=True)
  if not r[0]and n>=5:break
