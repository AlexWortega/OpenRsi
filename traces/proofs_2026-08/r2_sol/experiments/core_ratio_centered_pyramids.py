#!/usr/bin/env python3
# Question: is vol(K intersect -K)/vol(K)>=1/2 for centered 3D pyramids, a tractable nonsimplicial class toward a 16 volume bound?
import argparse,json,numpy as np
from scipy.spatial import ConvexHull,HalfspaceIntersection
ap=argparse.ArgumentParser();ap.add_argument('--samples',type=int,default=100000);ap.add_argument('--base-vertices',type=int,default=8);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/core_pyramids.json');args=ap.parse_args();rng=np.random.default_rng(args.seed)
def polygon_centroid(P):
 h=ConvexHull(P);Q=P[h.vertices];A=0.;M=np.zeros(2)
 for a,b in zip(Q,np.roll(Q,-1,axis=0)):
  z=a[0]*b[1]-a[1]*b[0];A+=z;M+=z*(a+b)
 return M/(3*A),abs(A)/2,Q
def ev():
 a=np.sort(rng.uniform(0,2*np.pi,args.base_vertices));rad=np.exp(rng.normal(0,.8,args.base_vertices));P=np.c_[rad*np.cos(a),rad*np.sin(a)]
 try:c,A,Q=polygon_centroid(P)
 except Exception:return None
 # Base centroid c at z=-1; choose apex (-3c,3), making pyramid centroid zero.
 V=np.vstack([np.c_[Q,np.full(len(Q),-1.)],[-3*c[0],-3*c[1],3.]])
 try:h=ConvexHull(V);E=h.equations;C=ConvexHull(HalfspaceIntersection(np.vstack([E,np.c_[-E[:,:3],E[:,3]]]),np.zeros(3)).intersections).volume
 except Exception as exc:
  return None
 return C/h.volume,len(Q),V.tolist()
vals=[]
for _ in range(args.samples):
 r=ev()
 if r: vals.append({'ratio':r[0],'base_vertices':r[1],'vertices':r[2]})
best=sorted(vals,key=lambda x:x['ratio'])[:100]
json.dump({'samples':args.samples,'best':best},open(args.out,'w'),indent=2);print(json.dumps({'min':best[0]['ratio'],'base_vertices':best[0]['base_vertices'],'out':args.out}),flush=True)
