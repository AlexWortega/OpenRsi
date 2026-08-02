#!/usr/bin/env python3
# Question: can numerical optimization drive vol(K intersect -K)/vol(K) below 1/2 for a genuinely centroid-zero 3-polytope?
import argparse,json,numpy as np
from scipy.spatial import ConvexHull,HalfspaceIntersection
ap=argparse.ArgumentParser();ap.add_argument('--vertices',type=int,default=6);ap.add_argument('--steps',type=int,default=200000);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/core_opt.json');args=ap.parse_args();rng=np.random.default_rng(args.seed)
def centered(q):
 h=ConvexHull(q);r=q.mean(0);V=0.;M=np.zeros(3)
 for tri in h.simplices:
  a,b,c=q[tri];v=abs(np.linalg.det(np.stack([a-r,b-r,c-r],1)))/6;V+=v;M+=v*(r+a+b+c)/4
 return q-M/V,V
def ev(q):
 try:p,V=centered(q);h=ConvexHull(p);E=h.equations;B=np.vstack([E,np.c_[-E[:,:3],E[:,3]]]);C=ConvexHull(HalfspaceIntersection(B,np.zeros(3)).intersections).volume
 except Exception:return None
 return C/V,p,V,C
# Start from simplex plus near-interior extra points.
base=np.array([[-1,-1,-1],[3,-1,-1],[-1,3,-1],[-1,-1,3]],float);q=np.vstack([base,rng.normal(0,.1,(args.vertices-4,3))]);r=ev(q);best=r[0];bestp=r[1];temp=.3
for it in range(args.steps):
 z=q.copy();i=rng.integers(len(z));z[i]+=rng.normal(0,temp,3);rr=ev(z)
 if rr and (rr[0]<r[0] or rng.random()<np.exp((r[0]-rr[0])/max(temp,.005))*.01):q=z;r=rr
 if rr and rr[0]<best:best,bestp=rr[0],rr[1]
 temp=max(.002,temp*.99995)
 if (it+1)%10000==0:print(it+1,best,flush=True)
out={'ratio':float(best),'vertices':bestp.tolist(),'steps':args.steps,'seed':args.seed};json.dump(out,open(args.out,'w'),indent=2);print(json.dumps({'ratio':best,'out':args.out}),flush=True)
