#!/usr/bin/env python3
# Question: does replacing K by the convex hull of its lattice points preserve enough volume in centered 3D samples to reduce toward lattice polytopes?
import argparse,itertools,json,numpy as np
from scipy.spatial import ConvexHull
ap=argparse.ArgumentParser();ap.add_argument('--samples',type=int,default=5000);ap.add_argument('--vertices',type=int,default=8);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/integer_hull.json');args=ap.parse_args();rng=np.random.default_rng(args.seed)
def center(p):
 h=ConvexHull(p);q=p.mean(0);V=0.;M=np.zeros(3)
 for tri in h.simplices:
  a,b,c=p[tri];v=abs(np.linalg.det(np.stack([a-q,b-q,c-q],1)))/6;V+=v;M+=v*(q+a+b+c)/4
 return p-M/V,V
def inside(h,z):return np.max(h.equations[:,:3]@z+h.equations[:,3])<=1e-9
rec=[]
for _ in range(args.samples):
 d=rng.normal(size=(args.vertices,3));d/=np.linalg.norm(d,axis=1)[:,None];p=d*np.exp(rng.normal(0,.8,args.vertices))[:,None]
 try:p,V=center(p);h=ConvexHull(p);off=-h.equations[:,3]
 except Exception:continue
 Z=np.array([z for z in itertools.product(range(-6,7),repeat=3) if z!=(0,0,0)],float);g=(Z@h.equations[:,:3].T/off).max(1);lam=g[g>1e-10].min();p*=lam;h=ConvexHull(p);V*=lam**3
 pts=[np.array(z,float) for z in itertools.product(*(range(int(np.floor(p[:,i].min())),int(np.ceil(p[:,i].max()))+1) for i in range(3))) if inside(h,np.array(z,float))]
 try:IH=ConvexHull(np.array(pts));ratio=IH.volume/V
 except Exception:ratio=0
 rec.append({'volume':V,'integer_hull_ratio':ratio,'lattice_points':len(pts)})
rec.sort(key=lambda x:-x['volume']);json.dump({'samples':args.samples,'top':rec[:200]},open(args.out,'w'),indent=2);print(json.dumps({'best':rec[0],'min_ratio_top100':min(x['integer_hull_ratio'] for x in rec[:100])}),flush=True)
