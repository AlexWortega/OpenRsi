#!/usr/bin/env python3
# Question: what high-volume centroid-zero lattice-free tetrahedra occur in R^3?
import argparse, json, numpy as np
from scipy.optimize import differential_evolution
from scipy.spatial import ConvexHull
from itertools import product

ap=argparse.ArgumentParser(); ap.add_argument('--seed',type=int,default=1); ap.add_argument('--iters',type=int,default=1000); ap.add_argument('--out',default='experiments/tetra_search.json'); args=ap.parse_args()
# Four vertices with centroid zero; optimize first three, fourth is minus their sum.
def decode(x):
 v=np.asarray(x).reshape(3,3); return np.vstack([v,-v.sum(axis=0)])
def volume(v): return abs(np.linalg.det((v[1:]-v[0]).T))/6
def barycentric(v,p):
 A=np.vstack([v.T,np.ones(4)]); return np.linalg.solve(A,np.r_[p,1.])
def score(x):
 v=decode(x); vol=volume(v)
 if vol<1e-8:return 1e6
 lo=np.floor(v.min(axis=0)).astype(int)-1; hi=np.ceil(v.max(axis=0)).astype(int)+1
 worst=0.; offenders=0
 for p in product(*(range(lo[j],hi[j]+1) for j in range(3))):
  if p==(0,0,0):continue
  lam=barycentric(v,np.array(p,float)); margin=lam.min()
  if margin>0: offenders+=1; worst=max(worst,margin)
 # Smooth-ish penalty strongly rejects actual interior lattice points.
 return -vol+1e4*offenders+1e4*worst
res=differential_evolution(score,[(-5,5)]*9,maxiter=args.iters,popsize=15,seed=args.seed,polish=True,workers=1,updating='immediate')
v=decode(res.x); data={'seed':args.seed,'objective':res.fun,'volume':volume(v),'vertices':v.tolist(),'success':bool(res.success),'message':res.message}
with open(args.out,'w') as f:json.dump(data,f,indent=2)
print(json.dumps(data),flush=True)
