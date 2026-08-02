#!/usr/bin/env python3
# Question: how small can vol(K intersect -K)/vol(K) be for numerically volume-centered 3-polytopes, especially after scaling to lattice contact?
import argparse,itertools,json,numpy as np
from scipy.spatial import ConvexHull,HalfspaceIntersection
ap=argparse.ArgumentParser();ap.add_argument('--samples',type=int,default=10000);ap.add_argument('--vertices',type=int,default=8);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/core_ratio.json');args=ap.parse_args();rng=np.random.default_rng(args.seed)
def center(p):
 h=ConvexHull(p);q=p.mean(0);V=0.;M=np.zeros(3)
 for tri in h.simplices:
  a,b,c=p[tri];v=abs(np.linalg.det(np.stack([a-q,b-q,c-q],1)))/6;V+=v;M+=v*(q+a+b+c)/4
 return p-M/V,V
def evaluate(raw):
 try:p,V=center(raw);h=ConvexHull(p);H=h.equations;hs=np.vstack([H,np.c_[-H[:,:3],H[:,3]]]);P=HalfspaceIntersection(hs,np.zeros(3)).intersections;C=ConvexHull(P).volume
 except Exception:return None
 return C/V,V,C,p.tolist()
best=[]
sharp=np.array([[-1,-1,-1],[3,-1,-1],[-1,3,-1],[-1,-1,3]],float);r=evaluate(sharp);best.append({'kind':'sharp','ratio':r[0],'volume':r[1],'core':r[2]})
for _ in range(args.samples):
 d=rng.normal(size=(args.vertices,3));d/=np.linalg.norm(d,axis=1)[:,None];p=d*np.exp(rng.normal(0,1.5,args.vertices))[:,None];r=evaluate(p)
 if r:best.append({'kind':'random','ratio':r[0],'volume':r[1],'core':r[2],'vertices':r[3]})
best.sort(key=lambda x:x['ratio']);json.dump({'samples':args.samples,'smallest':best[:100]},open(args.out,'w'),indent=2);print(json.dumps({'evaluated':len(best),'min':best[0],'sharp':next(x for x in best if x['kind']=='sharp'),'out':args.out},default=str),flush=True)
