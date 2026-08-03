#!/usr/bin/env python3
"""Mutation: coarsen binary pure tensor coordinates by underlying set support.

For binary x, a tensor coordinate x_{i1}...x_{ir} depends only on the set of
distinct indices in the tuple.  Thus P_r(D) compresses exactly to subsets
S with 1<=|S|<=r.  Coordinate S has integer weight equal to the number of
length-r words with alphabet exactly S: |S|! S(r,|S|).  Weighted Hamming
therefore equals full tensor Hamming for every mixed pure-power word.

Tests random pointed codes and tiny 3DM YES/NO codes, and realizes small cases
as explicit integer CVP bases via four-square Euclidean weight embeddings.
"""
from __future__ import annotations
import itertools,math,random
import verify_weighted_symmetric_cvp as ws
import verify_asymmetric_hash_fold as af
import verify_reduced_orbit_fold as ro


def subsets(n,r):
 return [S for k in range(1,min(n,r)+1) for S in itertools.combinations(range(n),k)]
def surjections(r,k):
 return sum((-1)**j*math.comb(k,j)*(k-j)**r for j in range(k+1))
def compressed_code(D,n,r):
 SS=subsets(n,r);rows=[]
 for x in ws.words(D):
  y=0
  for j,S in enumerate(SS):
   if all((x>>i)&1 for i in S):y|=1<<j
  rows.append(y)
 return ws.basis(rows),SS,[surjections(r,len(S)) for S in SS]
def pointed_weight(C,SS,w):
 star=SS.index((0,))
 return min(sum(w[j] for j in range(len(w)) if (x>>j)&1)
            for x in ws.words(C) if (x>>star)&1)
def permute_star(C,SS):
 """Move subset {0} coordinate to bit zero for explicit pointed CVP helper."""
 star=SS.index((0,));order=[star]+[j for j in range(len(SS)) if j!=star];out=[]
 for x in C:
  y=0
  for k,j in enumerate(order):
   if (x>>j)&1:y|=1<<k
  out.append(y)
 return ws.basis(out),order
def instance(q,T):
 C,d=af.instance_code(q,T);return C,len(T),d
def main():
 rng=random.Random(2029);reports=[]
 for n in [3,4,5,6]:
  for r in [2,3,4,6,8]:
   for z in range(5):
    D=ws.basis([1|(rng.randrange(1<<(n-1))<<1) for _ in range(2)])
    d=ro.pdist(D);C,SS,w=compressed_code(D,n,r);got=pointed_weight(C,SS,w)
    assert got==d**r and sum(w)==n**r
    multiset=math.comb(n+r-1,r);setcount=sum(math.comb(n,k) for k in range(1,min(n,r)+1))
    assert len(SS)==setcount<=multiset
    if n<=4 and r<=4:
     Q,order=permute_star(C,SS);ww=[w[j] for j in order]
     cvpd,rank,ambient,maxscale,EB,t=ws.explicit_distance(Q,1,ww)
     assert cvpd==got and rank==len(SS)
    reports.append((n,r,d,n**r,multiset,setcount,got,max(w)))
 # End-to-end tiny 3DM distances, including every mixed pure-power word.
 q,m=3,8;Y=af.planted(q,m,17);N=af.randomT(q,m,10003)
 CY,n,dy=instance(q,Y);CN,_,dn=instance(q,N);assert (dy,dn)==(3,5)
 dm=[]
 for r in [2,3,4,8,12]:
  row=[]
  for label,D,d in [('Y',CY,dy),('N',CN,dn)]:
   C,SS,w=compressed_code(D,n,r);got=pointed_weight(C,SS,w)
   assert got==d**r
   row.append((label,len(C),len(SS),got,max(w)))
  dm.append((r,row))
 print({'random_checks':len(reports),'sample':reports[:15],
        '3DM':dm})
 assert len(reports)==100
 print('set-support weighted pure-power CVP compression passes')
if __name__=='__main__':main()
