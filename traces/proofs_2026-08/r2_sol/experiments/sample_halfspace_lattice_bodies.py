#!/usr/bin/env python3
# Question: which high-volume centroid-zero lattice-free 3-polytopes arise from integer-normal facet inequalities, beyond vertex-random sampling?
import argparse,itertools,json,numpy as np
from scipy.spatial import HalfspaceIntersection,ConvexHull
ap=argparse.ArgumentParser();ap.add_argument('--samples',type=int,default=100000);ap.add_argument('--normals',type=int,default=8);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/halfspace_lattice.json');args=ap.parse_args();rng=np.random.default_rng(args.seed)
Z=np.array([z for z in itertools.product(range(-8,9),repeat=3) if z!=(0,0,0)],float);N=np.array([u for u in itertools.product(range(-2,3),repeat=3) if u!=(0,0,0) and np.gcd.reduce(np.abs(u))==1],float)
def centroid(p):
 h=ConvexHull(p);q=p.mean(0);V=0.;M=np.zeros(3)
 for tri in h.simplices:
  a,b,c=p[tri];v=abs(np.linalg.det(np.stack([a-q,b-q,c-q],1)))/6;V+=v;M+=v*(q+a+b+c)/4
 return M/V,V
def ev():
 ids=rng.choice(len(N),args.normals,replace=False);norm=N[ids];offs=rng.uniform(.5,3,args.normals);H=np.c_[norm,-offs]
 # bounding box guarantees boundedness
 H=np.vstack([H,[[1,0,0,-4],[-1,0,0,-4],[0,1,0,-4],[0,-1,0,-4],[0,0,1,-4],[0,0,-1,-4]]])
 try:p=HalfspaceIntersection(H,np.zeros(3)).intersections;c,V=centroid(p);p-=c;h=ConvexHull(p);off=-h.equations[:,3]
 except Exception:return None
 if off.min()<=1e-8:return None
 gauge=(Z@h.equations[:,:3].T/off).max(1);lam=gauge[gauge>1e-10].min();return V*lam**3,(p*lam).tolist(),len(h.vertices)
best=[]
for _ in range(args.samples):
 r=ev()
 if r and (len(best)<100 or r[0]>best[-1]['volume']):best.append({'volume':r[0],'vertices':r[1],'hull_vertices':r[2]});best.sort(key=lambda x:-x['volume']);best=best[:100]
json.dump({'samples':args.samples,'best':best},open(args.out,'w'),indent=2);print(json.dumps({'best_volume':best[0]['volume'],'hull_vertices':best[0]['hull_vertices'],'out':args.out}),flush=True)
