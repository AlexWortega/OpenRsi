#!/usr/bin/env python3
"""Mutation: merge set-support coordinates with identical codeword functions.

Parameterize a binary code D by k message bits. Each base coordinate is a
linear Boolean form. A set-support tensor coordinate is the product of its
forms, represented exactly by a 2^k-bit truth table. Merge equal truth tables
and sum their integer tuple multiplicities. Weighted distance is unchanged for
every mixed pure-power word. Test random codes and 3DM pointed codes, tracking
formal subsets versus distinct nonzero function types.
"""
from __future__ import annotations
import itertools,math,random
import verify_set_support_weighted_cvp as ss
import verify_weighted_symmetric_cvp as ws
import verify_asymmetric_hash_fold as af
import verify_reduced_orbit_fold as ro


def coord_forms(B,n):
 # k-bit coefficient vector for each coordinate.
 return [sum(((row>>j)&1)<<i for i,row in enumerate(B)) for j in range(n)]
def truth_product(forms,k):
 t=0
 for msg in range(1<<k):
  if all((msg&f).bit_count()%2 for f in forms):t|=1<<msg
 return t
def types(B,n,r):
 B=ws.basis(B);forms=coord_forms(B,n);W={}
 for S,w in zip(ss.subsets(n,r),[ss.surjections(r,len(S)) for S in ss.subsets(n,r)]):
  t=truth_product([forms[i] for i in S],len(B))
  if t:W[t]=W.get(t,0)+w
 return W
def image_code(k,typekeys):
 rows=[]
 for bit in range(k):
  msg=1<<bit;y=0
  for j,t in enumerate(typekeys):
   if (t>>msg)&1:y|=1<<j
  rows.append(y)
 return ws.basis(rows)
def pointed_distance(B,n,r):
 W=types(B,n,r);keys=sorted(W);C=image_code(len(B),keys)
 # Star functional is message/code coordinate 0, not necessarily compressed bit.
 best=None
 for msg in range(1<<len(B)):
  x=0
  for i,row in enumerate(B):
   if (msg>>i)&1:x^=row
  if not (x&1):continue
  y=0
  for j,t in enumerate(keys):
   if (t>>msg)&1:y|=1<<j
  z=sum(W[t] for j,t in enumerate(keys) if (y>>j)&1)
  best=z if best is None else min(best,z)
 return best,len(W),sum(W.values()),max(W.values()),len(B)
def main():
 rng=random.Random(7001);reports=[]
 for n in range(3,9):
  for k0 in range(1,min(5,n)+1):
   for seed in range(3):
    B=ws.basis([rng.randrange(1<<n)|1 for _ in range(k0)])
    if not B:continue
    d=ro.pdist(B)
    for r in [2,3,4,8,12]:
     got,nt,total,mx,k=pointed_distance(B,n,r)
     assert got==d**r
     reports.append((n,k,r,d,nt,sum(math.comb(n,j) for j in range(1,min(n,r)+1)),total,mx))
 # Tiny 3DM with varying m/kernel dimensions.
 dm=[]
 for q,m in [(3,8),(3,9),(3,10),(3,11),(3,12)]:
  Y=af.planted(q,m,17);D,d=af.instance_code(q,Y)
  for r in [4,8,12,24]:
   got,nt,total,mx,k=pointed_distance(D,m+1,r) # homogenized code has star+moving
   assert got==(d+1)**r
   dm.append((q,m,k,r,nt,2**(m+1)-1,got,mx))
 print({'random_checks':len(reports),'random_sample':reports[:20],'3DM':dm})
 # Exact finite count.
 assert len(reports)==405 and len(dm)==20
 print('function-type weighted pure-power compression passes')
if __name__=='__main__':main()
