#!/usr/bin/env python3
"""Exact construction search: formula-oblivious sparse folds of reduced 3DM squares.

Coordinates are ordered pairs of the m sorted triple columns.  A deterministic
seed defines the same linear hash map for every instance of size m.  We search
partition and two-sparse maps from m^2 moving coordinates to M outputs, then
exactly enumerate every mixed image word.  Uniform finite completeness uses the
maximum YES distance over ten planted instances; soundness uses the minimum NO
distance over ten exact odd-cover/no-matching instances.
"""
from __future__ import annotations
import itertools,random,math


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
def pd(rows):
 v=[(z>>1).bit_count() for z in words(rows) if z&1]
 return min(v) if v else None
def syn(q,u):return (1<<u[0])|(1<<(q+u[1]))|(1<<(2*q+u[2]))
def instance_code(q,T):
 T=sorted(T);c=[syn(q,u) for u in T];tar=(1<<(3*q))-1;K=[];F=[]
 for s in range(1<<len(T)):
  z=0
  for j,a in enumerate(c):
   if (s>>j)&1:z^=a
  if z==0:K.append(s)
  if z==tar:F.append(s)
 if not F:return None
 p=min(F,key=int.bit_count)
 return basis([z<<1 for z in K]+[1|(p<<1)]),p.bit_count()
def reduced(rows,m):
 out=[]
 for a in rows:
  for b in rows:
   z=(a&1)&(b&1)
   for i in range(m):
    if (a>>(1+i))&1:
     for j in range(m):
      if (b>>(1+j))&1:z^=1<<(1+i*m+j)
   out.append(z)
 return basis(out)
def planted(q,m,seed):
 r=random.Random(seed);d=[(i,i,i) for i in range(q)]
 a=[u for u in itertools.product(range(q),repeat=3) if u not in d];r.shuffle(a)
 return d+a[:m-q]
def randomT(q,m,seed):
 r=random.Random(seed);a=list(itertools.product(range(q),repeat=3));r.shuffle(a);return a[:m]
def samples(q,m):
 Y=[]
 for s in range(10):
  T=planted(q,m,s);C,d=instance_code(q,T);assert d==q;Y.append(reduced(C,m))
 N=[]
 for s in range(10000,30000):
  T=randomT(q,m,s);D=instance_code(q,T)
  if D and D[1]>q:
   N.append(reduced(D[0],m))
   if len(N)==10:break
 assert len(N)==10
 return Y,N
def map_rows(rows,m,M,seed,degree):
 r=random.Random(seed);maps=[]
 for _ in range(m*m):
  picks=r.sample(range(M),degree)
  z=0
  for p in picks:z^=1<<p
  maps.append(z)
 out=[]
 for row in rows:
  z=row&1
  for ij,v in enumerate(maps):
   if (row>>(1+ij))&1:z^=v<<1
  out.append(z)
 return basis(out)
def main():
 q,m=3,8;Y,N=samples(q,m);records=[]
 baseY=max(pd(C) for C in Y);baseN=min(pd(C) for C in N)
 assert (baseY,baseN)==(9,25)
 for M in [8,12,16,24,32]:
  for degree in [1,2]:
   for seed in range(100):
    yd=[pd(map_rows(C,m,M,100000*M+1000*degree+seed,degree)) for C in Y]
    nd=[pd(map_rows(C,m,M,100000*M+1000*degree+seed,degree)) for C in N]
    if any(v is None or v==0 for v in yd+nd):continue
    y=max(yd);n=min(nd);ratio=n/y
    exp=math.log(ratio)/math.log(M+1) if ratio>1 else 0
    records.append((exp,ratio,M,degree,seed,y,n,min(yd),max(nd)))
 records.sort(reverse=True)
 print({'base_length':65,'base_Y':baseY,'base_N':baseN,
        'base_ratio':baseN/baseY,'base_rank_exponent':math.log(baseN/baseY)/math.log(65)})
 print(f'checked {len(records)} valid exact hash-fold/sample combinations')
 assert len(records)==866
 for row in records[:30]:print(row)
 best=records[0]
 base_exp=math.log(baseN/baseY)/math.log(65)
 improvement=best[0]>base_exp
 print({'best_improves_base_exponent':improvement,'best_exponent':best[0],
        'base_exponent':base_exp})
 # Deterministic finite outcome used in the autopsy: this tested hash family
 # does NOT improve the sampled standard rank exponent.
 assert not improvement
if __name__=='__main__':main()
