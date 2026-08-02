#!/usr/bin/env python3
"""Test explicit recursive O(level) color rules on iterated C2 wreath groups."""
from wreath2_partition import ops
import argparse

def dec(x,N):return x//(2*N),(x//2)%N,x&1
def label(level,x,mode):
 if level==1:return (0,)
 N,_,_=ops(level-1);a,b,s=dec(x,N)
 if mode=='topbit':
  if s:return(level,'swap')
  if a:return(level,'L',label(level-1,a,mode))
  return(level,'R',label(level-1,b,mode))
 if mode=='depth':
  if s:return(level,'swap')
  la=label(level-1,a,mode) if a else None;lb=label(level-1,b,mode)if b else None
  return max([z for z in (la,lb)if z is not None],default=(0,))
 if mode=='depthtype':
  if s:return(level,1)
  if a and b:return(max(label(level-1,a,mode)[0],label(level-1,b,mode)[0]),2)
  z=a or b;return label(level-1,z,mode)
def test(l,m):
 N,mul,inv=ops(l);D={}
 for x in range(1,N):D.setdefault(label(l,x,m),[]).append(x)
 for c,S in D.items():
  T=set(S)
  for x in S:
   for y in S:
    z=mul(x,y)
    if z in T:return False,len(D),(c,x,y,z)
 return True,len(D),None
if __name__=='__main__':
 for l in range(2,5):
  for m in ['topbit','depth','depthtype']:
   print(l,m,test(l,m),flush=True)
