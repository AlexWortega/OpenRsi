#!/usr/bin/env python3
# Question: among genuinely nonsimplicial centered 3-polytopes, can the symmetric-core ratio approach or cross 1/2?
import argparse,json,numpy as np
from scipy.spatial import ConvexHull,HalfspaceIntersection
ap=argparse.ArgumentParser();ap.add_argument('--samples',type=int,default=100000);ap.add_argument('--vertices',type=int,default=8);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/core_nonsimplex.json');args=ap.parse_args();rng=np.random.default_rng(args.seed)
def ev(q):
 try:
  h=ConvexHull(q)
  if len(h.vertices)<5:return None
  r=q.mean(0);V=0.;M=np.zeros(3)
  for tri in h.simplices:
   a,b,c=q[tri];v=abs(np.linalg.det(np.stack([a-r,b-r,c-r],1)))/6;V+=v;M+=v*(r+a+b+c)/4
  p=q-M/V;h=ConvexHull(p);E=h.equations;B=np.vstack([E,np.c_[-E[:,:3],E[:,3]]]);C=ConvexHull(HalfspaceIntersection(B,np.zeros(3)).intersections).volume
  return C/V,p,len(h.vertices)
 except Exception:return None
best=[]
for _ in range(args.samples):
 d=rng.normal(size=(args.vertices,3));d/=np.linalg.norm(d,axis=1)[:,None];q=d*np.exp(rng.normal(0,.7,args.vertices))[:,None];r=ev(q)
 if r and (len(best)<100 or r[0]<best[-1]['ratio']):best.append({'ratio':r[0],'vertices':r[1].tolist(),'hull_vertices':r[2]});best.sort(key=lambda x:x['ratio']);best=best[:100]
json.dump({'samples':args.samples,'best':best},open(args.out,'w'),indent=2);print(json.dumps({'min':best[0]['ratio'],'hull_vertices':best[0]['hull_vertices'],'out':args.out}),flush=True)
