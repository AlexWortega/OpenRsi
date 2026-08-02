#!/usr/bin/env python3
"""Test O(q)-color product-free rules on affine groups AGL(1,q), q prime."""
import argparse
# (a,b): x -> a*x+b, a!=0; multiply (a,b)(c,d)=(ac,ad+b)
def mul(x,y,q):a,b=x;c,d=y;return(a*c%q,(a*d+b)%q)
def inv(x,q):a,b=x;ai=pow(a,-1,q);return(ai,-ai*b%q)
def label(x,q,m):
 a,b=x
 if m=='a':return a
 if m=='b':return b
 if m=='fixed':return b*pow((1-a)%q,-1,q)%q if a!=1 else q
 if m=='disc':return (a,b==0)
 if m=='ratio':return b*pow(a-1,-1,q)%q if a!=1 else q
 if m=='orbitpair':return min(b,(-b*pow(a,-1,q))%q)
def test(q,m):
 G=[(a,b)for a in range(1,q)for b in range(q)];e=(1,0);D={}
 try:
  for x in G:
   if x!=e:D.setdefault(label(x,q,m),[]).append(x)
 except ValueError:return False,0,('undefined',)
 for c,S in D.items():
  T=set(S)
  for x in S:
   for y in S:
    z=mul(x,y,q)
    if z in T:return False,len(D),(c,x,y,z)
 return True,len(D),None
if __name__=='__main__':
 for q in [3,5,7,11,13,17,19,23,29,31]:
  for m in ['a','b','fixed','disc','ratio','orbitpair']:
   print(q,m,test(q,m),flush=True)
