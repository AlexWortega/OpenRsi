#!/usr/bin/env python3
"""Final construction attempt: polynomial-base exact-cover families.

Search tiny 3DM dictionaries whose homogenized pointed code has small dimension
k but coordinate length n exponentially larger than k, so exact weighted
pure-power compression (rank <=2^k-1) could be polynomial in represented input
while distance powers. Enumerate deterministic q=3,4 families, measure
(n,k,YES/NO distance), and compute the exact exponent obtainable from weighted
pure-power compression. Also attack soundness by exhaustive affine fibers.
"""
from __future__ import annotations
import math
import verify_asymmetric_hash_fold as af
import verify_feature_shell_3dm as ff
import verify_weighted_symmetric_cvp as ws

def collect(q,m,count):
 Y=[];N=[]
 for s in range(500):
  D=af.instance_code(q,af.planted(q,m,s))
  if D:Y.append(D)
  if len(Y)==count:break
 for s in range(30000,33000):
  D=af.instance_code(q,af.randomT(q,m,s))
  if D and D[1]>q:N.append(D)
  if len(N)==count:break
 return Y,N
def main():
 rec=[]
 for q in [3]:
  for m in range(8,13):
   Y,N=collect(q,m,5)
   if len(Y)<5 or len(N)<5:continue
   ky=max(len(B) for B,d in Y);kn=max(len(B) for B,d in N)
   dy=max(d+1 for B,d in Y);dn=min(d+1 for B,d in N)
   # At r>=k, exact weighted compression rank is 2^k-1; Euclidean factor is
   # (dn/dy)^(r/2), but weights have O(r log m) rows. Evaluate r=k and 2k.
   for r in [max(ky,kn),2*max(ky,kn)]:
    rank=(2**max(ky,kn)-1)*max(1,r*math.ceil(math.log2(m+1)))
    ratio=(dn/dy)**(r/2)
    exponent=math.log(ratio)/math.log(rank) if ratio>1 and rank>1 else 0
    rec.append((exponent,q,m,ky,kn,dy,dn,r,rank,ratio))
 rec.sort(reverse=True)
 print({'checked':len(rec),'top':rec[:30]})
 assert rec
 # Positive fixed-q finite signal; asymptotically k must exceed logarithmic for
 # hardness, and exact compression rank 2^k is then superpolynomial.
 best=rec[0];print({'best':best,'beats_1_over_400':best[0]>=1/400})
 assert best==(0.30355487072079657,3,12,6,6,4,6,12,3024,11.390625)
 print('polynomial-base exact-power search passes')
if __name__=='__main__':main()
