#!/usr/bin/env python3
# Question: which centered 3D polytopes maximize volume after scaling to first lattice contact?
import argparse, json, numpy as np
from scipy.spatial import ConvexHull
from itertools import product

ap=argparse.ArgumentParser(); ap.add_argument('--samples',type=int,default=20000); ap.add_argument('--vertices',type=int,default=8); ap.add_argument('--seed',type=int,default=1); ap.add_argument('--box',type=int,default=12); ap.add_argument('--out',default='experiments/polytope_search.json'); args=ap.parse_args()
rng=np.random.default_rng(args.seed)
Z=np.array([z for z in product(range(-args.box,args.box+1),repeat=3) if z!=(0,0,0)],float)

def centroid_volume(points,hull):
 # Triangulate oriented boundary facets with an interior reference q; tetra centroids average by volume.
 q=points.mean(axis=0); V=0.; M=np.zeros(3)
 for tri in hull.simplices:
  a,b,c=points[tri]; v=abs(np.linalg.det(np.stack([a-q,b-q,c-q],axis=1)))/6
  V+=v; M+=v*(q+a+b+c)/4
 return M/V,V

def evaluate(points):
 try:h=ConvexHull(points)
 except Exception:return None
 cen,V=centroid_volume(points,h); p=points-cen; h=ConvexHull(p)
 # scipy equations: normal*x+offset <= 0. Gauge max(normal*x/(-offset)).
 off=-h.equations[:,3]
 if off.min()<=1e-9:return None
 gauges=(Z@h.equations[:,:3].T/off).max(axis=1)
 positive=gauges[gauges>1e-10]
 if not len(positive):return None
 scale=positive.min(); return V*scale**3,scale,cen,p,h

best=[]
for it in range(args.samples):
 dirs=rng.normal(size=(args.vertices,3)); dirs/=np.linalg.norm(dirs,axis=1)[:,None]
 radii=np.exp(rng.normal(0,0.9,size=args.vertices)); pts=dirs*radii[:,None]
 r=evaluate(pts)
 if r is None:continue
 vol,scale,cen,p,h=r
 rec={'volume':float(vol),'scale':float(scale),'raw_centroid':cen.tolist(),'vertices':(p*scale).tolist(),'facets':int(len(h.simplices)),'box':args.box}
 if len(best)<20 or vol>best[-1]['volume']:
  best.append(rec);best.sort(key=lambda x:-x['volume']);best=best[:20]
with open(args.out,'w') as f:json.dump(best,f,indent=2)
print(json.dumps({'samples':args.samples,'vertices':args.vertices,'best_volume':best[0]['volume'] if best else None,'target':32/3,'out':args.out}),flush=True)
