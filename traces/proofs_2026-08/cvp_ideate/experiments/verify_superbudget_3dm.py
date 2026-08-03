#!/usr/bin/env python3
"""Exact super-budget reduced folds on cyclic families of 3DM witnesses.

Each cyclic sheet has its own pointed 3DM witness; the shared star makes the
minimum pointed word live on ONE sheet and hence non-invariant.  This avoids
paying the group order in YES weight.  We test whether diagonal orbit folding
nevertheless compresses the true pointed distance toward ceil(d^2/ell).
"""
from __future__ import annotations
import itertools, random


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
def pd(rows):return min((x>>1).bit_count() for x in words(rows) if x&1)
def syn(q,u):return (1<<u[0])|(1<<(q+u[1]))|(1<<(2*q+u[2]))
def data(q,T):
 c=[syn(q,u) for u in T];tar=(1<<(3*q))-1
 def ev(x):
  z=0
  for j,a in enumerate(c):
   if (x>>j)&1:z^=a
  return z
 K=[x for x in range(1<<len(T)) if ev(x)==0]
 F=[x for x in range(1<<len(T)) if ev(x)==tar]
 if not F:return None
 return basis(K),min(F,key=int.bit_count),min(map(int.bit_count,F))
def randT(q,m,seed):
 r=random.Random(seed);a=list(itertools.product(range(q),repeat=3));r.shuffle(a);return a[:m]
def planted(q,m,seed):
 r=random.Random(seed);d=[(i,i,i) for i in range(q)];a=[u for u in itertools.product(range(q),repeat=3) if u not in d];r.shuffle(a);return d+a[:m-q]
def cyclic_code(q,T,l):
 K,p,d=data(q,T);m=len(T);rows=[]
 for h in range(l):
  for z in K:
   y=0
   for j in range(m):
    if (z>>j)&1:y^=1<<(1+j*l+h)
   rows.append(y)
  y=1
  for j in range(m):
   if (p>>j)&1:y^=1<<(1+j*l+h)
  rows.append(y)
 rows=basis(rows);assert pd(rows)==d
 return rows,d
def fold(rows,m,l):
 out=[]
 for a in rows:
  for b in rows:
   y=(a&1)&(b&1)
   for j in range(m):
    for h in range(l):
     if not ((a>>(1+j*l+h))&1):continue
     for k in range(m):
      for z in range(l):
       if (b>>(1+k*l+z))&1:
        y^=1<<(1+(j*m+k)*l+(z-h)%l)
   out.append(y)
 return basis(out)
def find_no(q,m):
 for s in range(100000,110000):
  T=randT(q,m,s);D=data(q,T)
  if D and D[2]>q:return T,s,D[2]
 raise RuntimeError
def main():
 q=3;m=5;Y=planted(q,m,9);N,seed,nd=find_no(q,m)
 print('NO seed',seed,'single distance',nd)
 for l in [3,5,7,11]:
  for label,T in [('YES',Y),('NO',N)]:
   rows,d=cyclic_code(q,T,l);fr=fold(rows,m,l);dp=pd(fr);lo=(d*d+l-1)//l
   assert dp>=lo
   assert dp==d*d  # exact deterministic outcome claimed in STATUS/proof
   print({'ell':l,'case':label,'base_dim':len(rows),'d':d,
          'fold_dim':len(fr),'dprime':dp,'lower':lo,'ratio_to_square':f'{dp}/{d*d}'})
 print('All super-budget 3DM folds enumerated exactly.')
if __name__=='__main__':main()
