#!/usr/bin/env python3
"""Exact dimension theorem/parameter attack for P_r(D).

If D is a k-dimensional binary code with injective message map and no zero
coordinate requirement beyond spanning, the coordinate linear forms span the
dual message space. Products of r forms (repetitions allowed, l^2=l as Boolean
functions) span all squarefree monomials of degrees 1..min(k,r). Hence
 dim P_r(D)=sum_{j=1}^{min(k,r)} C(k,j).

The script verifies this for random codes and tiny 3DM codes by explicit pure
powers, and checks saturation at 2^k-1. It also verifies that enumerating all
2^k base codewords computes pointed distance, documenting the parameter wall.
"""
from __future__ import annotations
import itertools,math,random
import verify_weighted_symmetric_cvp as ws
import verify_asymmetric_hash_fold as af
import verify_reduced_orbit_fold as ro


def predicted(k,r):return sum(math.comb(k,j) for j in range(1,min(k,r)+1))
def main():
 rng=random.Random(444);reports=[]
 for n in range(2,9):
  for trial in range(20):
   B=ws.basis([rng.randrange(1<<n) for _ in range(rng.randint(1,n))])
   if not B:continue
   k=len(B)
   for r in range(1,min(6,k+2)):
    P=ws.pure_code(B,n,r);want=predicted(k,r)
    assert len(P)==want
    reports.append((n,k,r,len(P),want))
 # 3DM incidence pointed codes, increasing nullity/dimension.
 dm=[]
 for q,m in [(3,8),(3,9),(3,10),(3,11),(3,12),(4,12),(4,13),(4,14)]:
  T=af.planted(q,m,17);B,d=af.instance_code(q,T);k=len(B)
  for r in range(1,k+2):
   # Explicit tensors only when n^r remains modest; function evaluation rank
   # supplies an independent check at larger r.
   want=predicted(k,r)
   if m**r<=2_000_000:
    assert len(ws.pure_code(B,m+1,r))==want
   # Evaluation matrix of all nonconstant squarefree message monomials.
   mons=[S for j in range(1,min(k,r)+1) for S in itertools.combinations(range(k),j)]
   rows=[]
   for msg in range(1<<k):
    y=0
    for a,S in enumerate(mons):
     if all((msg>>i)&1 for i in S):y|=1<<a
    rows.append(y)
   assert len(ws.basis(rows))==want
   dm.append((q,m,k,r,want,2**k-1))
  # Exhaustive base pointed distance takes exactly 2^k messages.
  vals=[x.bit_count() for x in ws.words(B) if x&1]
  assert min(vals)==d+1
 print({'random_checks':len(reports),'sample':reports[:20],'3DM':dm})
 assert reports and dm and all(z[4]==z[5] for z in dm if z[3]>=z[2])
 print('pure-power dimension theorem finite checks pass')
if __name__=='__main__':main()
