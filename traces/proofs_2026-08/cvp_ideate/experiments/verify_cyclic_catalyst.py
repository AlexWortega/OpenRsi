#!/usr/bin/env python3
"""Exact verifier for the cyclic correlation catalyst construction.

A fixed cyclic pointed code A of length 15 has odd distance a=5, and its
correlation image B has odd distance a'=5.  For an arbitrary small pointed code
C of moving distance d, form C tensor A, then reduced-tensor and fold only the
cyclic phase.  Algebra predicts the folded moving code C tensor C tensor B and
pointed moving distance d^2 a'.  We enumerate every mixed word exactly.
"""
from __future__ import annotations
import random


def basis(rows):
 p={}
 for z in rows:
  while z:
   q=z.bit_length()-1
   if q in p:z^=p[q]
   else:
    for r,y in list(p.items()):
     if (y>>q)&1:p[r]=y^z
    p[q]=z;break
 return [p[q] for q in sorted(p)]
def words(rows):
 for s in range(1<<len(rows)):
  z=0
  for i,r in enumerate(rows):
   if (s>>i)&1:z^=r
  yield z
def pd(rows):return min((z>>1).bit_count() for z in words(rows) if z&1)
def pmul(a,b):
 z=0
 while b:
  lb=b&-b;z^=a<<(lb.bit_length()-1);b^=lb
 return z

def catalyst():
 ell=15
 g=pmul(pmul((1<<4)|(1<<1)|1,(1<<4)|(1<<3)|1),
        (1<<4)|(1<<3)|(1<<2)|(1<<1)|1)
 A=basis([g<<i for i in range(3)])
 # Star form on A is parity. Build the correlation image B with its product
 # star bit; B is another pointed code on ell moving coordinates.
 B=[]
 for a in A:
  for b in A:
   z=(a.bit_count()&1)&(b.bit_count()&1)
   for h in range(ell):
    bit=0
    for i in range(ell):bit^=((a>>i)&1)&((b>>((i+h)%ell))&1)
    z|=bit<<(1+h)
   B.append(z)
 B=basis(B)
 assert pd(B)==5
 return ell,A,B

def triple_product(C,n,B,ell):
 # Pointed tensor of C,C,B, retaining one star and n*n*ell moving coords.
 out=[]
 for u in C:
  for v in C:
   for b in B:
    z=(u&1)&(v&1)&(b&1)
    for i in range(n):
     if not ((u>>(1+i))&1):continue
     for j in range(n):
      if not ((v>>(1+j))&1):continue
      for h in range(ell):
       if (b>>(1+h))&1:z^=1<<(1+(i*n+j)*ell+h)
    out.append(z)
 return basis(out)
def main():
 ell,A,B=catalyst();rng=random.Random(8675309);reports=[]
 while len(reports)<100:
  n=rng.choice([2,3,4,5]);k=rng.choice([1,2,3])
  rows=basis([rng.randrange(1<<(n+1)) for _ in range(k)])
  if not rows or len(rows)>3 or not any(z&1 for z in words(rows)):continue
  d=pd(rows)
  if d==0:continue
  T=triple_product(rows,n,B,ell)
  if len(T)>18:continue
  got=pd(T);assert got==d*d*5
  reports.append((n,len(rows),d,len(T),got,1+n*n*ell))
 print(f'checked {len(reports)} exact arbitrary-code catalyst assemblies')
 print({'ell':ell,'A_dim':len(A),'B_dim':len(B),'A_odd_d':5,'B_odd_d':5})
 for r in reports[:20]:print(r)
if __name__=='__main__':main()
