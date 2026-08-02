#!/usr/bin/env python3
# Question: can facet-generated centroid-zero 3-polytopes have vol(K intersect -K)/vol(K) below the simplex value 1/2?
import argparse,json,numpy as np
from scipy.spatial import HalfspaceIntersection,ConvexHull
ap=argparse.ArgumentParser();ap.add_argument('--samples',type=int,default=20000);ap.add_argument('--facets',type=int,default=12);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/core_ratio_halfspace.json');args=ap.parse_args();rng=np.random.default_rng(args.seed)
def centroid(p):
 h=ConvexHull(p);q=p.mean(0);V=0.;M=np.zeros(3)
 for tri in h.simplices:
  a,b,c=p[tri];v=abs(np.linalg.det(np.stack([a-q,b-q,c-q],1)))/6;V+=v;M+=v*(q+a+b+c)/4
 return M/V,V
def evalone():
 # Begin with a containing box, then random support halfspaces; origin is initially interior.
 H=[[1,0,0,-1],[-1,0,0,-1],[0,1,0,-1],[0,-1,0,-1],[0,0,1,-1],[0,0,-1,-1]]
 for _ in range(args.facets):
  u=rng.normal(size=3);u/=np.linalg.norm(u);H.append([*u,-np.exp(rng.normal(0,.9))])
 H=np.array(H,float)
 try:p=HalfspaceIntersection(H,np.zeros(3)).intersections;c,V=centroid(p);p=p-c;h=ConvexHull(p);E=h.equations;both=np.vstack([E,np.c_[-E[:,:3],E[:,3]]]);core=ConvexHull(HalfspaceIntersection(both,np.zeros(3)).intersections).volume
 except Exception:return None
 return core/V,p.tolist(),V,core
out=[]
for _ in range(args.samples):
 r=evalone()
 if r and (len(out)<100 or r[0]<out[-1]['ratio']):
  out.append({'ratio':r[0],'vertices':r[1],'volume':r[2],'core':r[3]});out.sort(key=lambda x:x['ratio']);out=out[:100]
json.dump({'samples':args.samples,'facets':args.facets,'smallest':out},open(args.out,'w'),indent=2);print(json.dumps({'min':out[0]['ratio'],'volume':out[0]['volume'],'core':out[0]['core'],'out':args.out}),flush=True)
