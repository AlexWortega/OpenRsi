#!/usr/bin/env python3
# Question: can adding/moving vertices near the sharp simplex improve centered first-lattice-contact volume?
import argparse,json,numpy as np
from scipy.spatial import ConvexHull
from itertools import product

ap=argparse.ArgumentParser(); ap.add_argument('--vertices',type=int,default=6); ap.add_argument('--steps',type=int,default=100000); ap.add_argument('--seed',type=int,default=1); ap.add_argument('--box',type=int,default=12); ap.add_argument('--out',default='experiments/hill_poly.json'); args=ap.parse_args()
rng=np.random.default_rng(args.seed)
Z=np.array([z for z in product(range(-args.box,args.box+1),repeat=3) if z!=(0,0,0)],float)
base=np.array([[-1,-1,-1],[3,-1,-1],[-1,3,-1],[-1,-1,3]],float)
# Duplicate randomly perturbed simplex vertices; hull may initially still be simplex.
p=np.vstack([base,base[rng.integers(4,size=args.vertices-4)]+rng.normal(0,.03,(args.vertices-4,3))])

def centered(q):
 h=ConvexHull(q); ref=q.mean(0); V=0.; M=np.zeros(3)
 for tri in h.simplices:
  a,b,c=q[tri]; v=abs(np.linalg.det(np.stack([a-ref,b-ref,c-ref],1)))/6
  V+=v;M+=v*(ref+a+b+c)/4
 return q-M/V,V

def eval(q):
 try:q,V=centered(q);h=ConvexHull(q)
 except Exception:return None
 off=-h.equations[:,3]
 if off.min()<1e-8:return None
 gauge=(Z@h.equations[:,:3].T/off).max(1)
 lam=gauge[gauge>1e-12].min()
 return V*lam**3,q*lam,lam
r=eval(p); best=r[0]; bestp=r[1]; temp=.25
for it in range(args.steps):
 cand=p.copy(); i=rng.integers(len(p)); cand[i]+=rng.normal(0,temp,3)
 rr=eval(cand)
 if rr and (rr[0]>=best or rng.random()<np.exp((rr[0]-best)/max(.02,temp))*.002):
  p=cand
  if rr[0]>best:best,bestp=rr[0],rr[1]
 temp=max(.005,temp*.99995)
 if (it+1)%10000==0:print(it+1,best,flush=True)
data={'volume':float(best),'target':32/3,'vertices':bestp.tolist(),'box':args.box,'steps':args.steps,'seed':args.seed}
with open(args.out,'w') as f:json.dump(data,f,indent=2)
print(json.dumps(data),flush=True)
