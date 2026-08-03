#!/usr/bin/env python3
"""Exact tiny tests for systematic nonlinear-feature generators [I | phi(x)]."""
from __future__ import annotations
import itertools,random,numpy as np

def row_basis(G):
 basis={};keep=[]
 for row in G:
  z=sum(int(x)<<i for i,x in enumerate(row))
  while z:
   p=z.bit_length()-1
   if p not in basis:basis[p]=z;keep.append(row.copy());break
   z^=basis[p]
 return np.array(keep,dtype=np.uint8)
def words(G):
 for c in itertools.product((0,1),repeat=len(G)):
  w=np.zeros(G.shape[1],dtype=np.uint8)
  for b,r in zip(c,G):
   if b:w^=r
  yield w

def dist(G,t):return min(int((w^t).sum()) for w in words(row_basis(G)))
def run(seed=241,trials=200):
 rng=random.Random(seed);records=[];cheats=0
 for _ in range(trials):
  k=4;m=8
  P=np.array([[rng.randrange(2) for _ in range(m)] for _ in range(k)],dtype=np.uint8)
  G=np.concatenate([np.eye(k,dtype=np.uint8),P],axis=1)
  # Target uses a random Boolean assignment in systematic part but perturbs one feature.
  a=np.array([rng.randrange(2) for _ in range(k)],dtype=np.uint8)
  t=np.r_[a,a.dot(P)%2];j=k+rng.randrange(m);t[j]^=1
  d=dist(G,t);records.append(d);cheats+=d==1
 assert cheats==trials
 print({'systematic_random_codes':trials,'target_single_feature_corruption_distances':{d:records.count(d) for d in set(records)},
  'diagnosis':'systematic assignment coefficients do not make nonlinear features; target remains one bit from its generating codeword'})
if __name__=='__main__':run()
