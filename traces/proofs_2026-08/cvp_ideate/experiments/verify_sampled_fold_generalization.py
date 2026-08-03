#!/usr/bin/env python3
"""Generalization attack on the best sampled pure-power fold.

Fix public parameters (r=8,M=256,salt=19, weighted duplicate multiplicities)
and apply the same deterministic code-dependent algorithm to larger families,
input relabelings, and m=8..12 BMT instances. Selection uses only row-reduced
code bits. Exhaustively enumerate all messages, recording worst YES/best NO.
"""
from __future__ import annotations
import random
import verify_sampled_pure_power_fold as sf
import verify_asymmetric_hash_fold as af
import verify_weighted_symmetric_cvp as ws


def permute(B,n,perm):
 out=[]
 for x in B:
  y=0
  for i,j in enumerate(perm):
   if (x>>i)&1:y|=1<<j
  out.append(y)
 return ws.basis(out)
def families(q,m,count):
 Y=[];N=[]
 for s in range(10000):
  D=af.instance_code(q,af.planted(q,m,s))
  if D:Y.append(D[0])
  if len(Y)==count:break
 for s in range(20000,200000):
  D=af.instance_code(q,af.randomT(q,m,s))
  if D and D[1]>q:N.append(D[0])
  if len(N)==count:break
 return Y,N
def evaluate(Y,N,n,r=8,M=256,salt=19):
 yd=[sf.sampled(B,n,r,M,salt,True)[0] for B in Y]
 nd=[sf.sampled(B,n,r,M,salt,True)[0] for B in N]
 return max(yd),min(nd),min(yd),max(nd),min(nd)/max(yd)
def main():
 reports=[]
 for m in range(8,13):
  Y,N=families(3,m,50);assert len(Y)==len(N)==50
  reports.append(('base',m,evaluate(Y,N,m+1)))
  # Relabel moving triple coordinates but keep star fixed. Canonical row bits
  # change the sampler seed, so soundness must survive arbitrary presentation.
  Yp=[];Np=[]
  for tag,F,out in [('Y',Y,Yp),('N',N,Np)]:
   for j,B in enumerate(F):
    rng=random.Random(900000+m*1000+j+(tag=='N')*500)
    mov=list(range(1,m+1));rng.shuffle(mov);p=[0]+mov
    out.append(permute(B,m+1,p))
  reports.append(('permuted',m,evaluate(Yp,Np,m+1)))
 print({'reports':reports})
 # The original 7x sample does not generalize: exact deterministic outcome.
 assert reports[0][2][4] == 4/3
 assert max(z[2][4] for z in reports) < 2
 print('sampled fold generalization attack passes')
if __name__=='__main__':main()
