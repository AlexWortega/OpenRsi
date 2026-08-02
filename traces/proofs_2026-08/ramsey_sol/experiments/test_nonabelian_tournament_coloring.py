#!/usr/bin/env python3
"""Test orientation-based coloring on S_n using a tournament color of relative permutation."""
import itertools,argparse

def comp(p,q):return tuple(p[q[i]]for i in range(len(p)))
def inv(p):
 z=[0]*len(p)
 for i,x in enumerate(p):z[x]=i
 return tuple(z)
def test(n,mode):
 V=list(itertools.permutations(range(n)))
 def c(x,y):
  if y<x:x,y=y,x
  p=comp(inv(x),y);i=next(i for i in range(n)if p[i]!=i);a=p[i]
  if mode=='edgecolor':return (i+a)% (n if n%2 else n-1)
  if mode=='cycdiff':return min((a-i)%n,(i-a)%n)
  if mode=='orient':return ((a-i)%n)<=n//2
  if mode=='hash':return (2*i+a)%n
 for i,x in enumerate(V):
  for j,y in enumerate(V[:i]):
   z=c(x,y)
   for w in V[:j]:
    if z==c(x,w)==c(y,w):return False,(x,y,w,z)
 return True,len({c(x,y)for i,x in enumerate(V)for y in V[:i]})
if __name__=='__main__':
 for n in range(3,8):
  for m in ['edgecolor','cycdiff','orient','hash']:
   print(n,m,test(n,m),flush=True)
