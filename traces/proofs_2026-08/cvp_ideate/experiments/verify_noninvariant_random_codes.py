#!/usr/bin/env python3
"""Exact random invariant-code search for super-budget reduced folds.

Unlike orbit spans of one pointed word, each code has independent unpointed
cyclic generators plus one pointed orbit.  Search asks whether ell>d>1 and the
true folded distance reaches the symmetrization floor ceil(d^2/ell).
"""
from __future__ import annotations
import random
from collections import Counter


def basis(rows):
 p={}
 for x in rows:
  while x:
   q=x.bit_length()-1
   if q in p:x^=p[q]
   else:
    for r,y in list(p.items()):
     if (y>>q)&1:p[r]=y^x
    p[q]=x;break
 return [p[q] for q in sorted(p)]

def words(rows):
 for s in range(1<<len(rows)):
  x=0
  for i,r in enumerate(rows):
   if (s>>i)&1:x^=r
  yield x

def sh(x,l):
 m=x>>1;m=((m<<1)&((1<<l)-1))|(m>>(l-1));return (x&1)|(m<<1)
def orb(x,l):
 z=[]
 for _ in range(l):z.append(x);x=sh(x,l)
 return z

def pd(rows):return min((x>>1).bit_count() for x in words(rows) if x&1)
def fold(rows,l):
 out=[]
 for a in rows:
  for b in rows:
   y=(a&1)&(b&1)
   for i in range(l):
    if (a>>(1+i))&1:
     for j in range(l):
      if (b>>(1+j))&1:y^=1<<(1+(j-i)%l)
   out.append(y)
 return basis(out)

def main():
 rng=random.Random(20260803); C=Counter(); hits=[]; checked=0
 for l in [5,7,11]:
  for trial in range(3000):
   pm=rng.randrange(1,1<<l); um=rng.randrange(1,1<<l)
   rows=basis(orb(1|(pm<<1),l)+orb(um<<1,l))
   if len(rows)>12:continue
   d=pd(rows)
   if d==0:continue
   fr=fold(rows,l)
   if len(fr)>16:continue
   dp=pd(fr); lo=(d*d+l-1)//l
   assert dp>=lo
   checked+=1;C[(l,d,dp,lo,dp==lo)]+=1
   if l>d>1 and dp==lo and len(hits)<20:
    hits.append((l,len(rows),len(fr),d,dp,bin(pm),bin(um)))
 print('checked',checked,'hits ell>d>1 at floor',len(hits))
 for x in hits:print(x)
 print('distribution')
 for k,v in sorted(C.items()):print(k,v)
if __name__=='__main__':main()
