#!/usr/bin/env python3
# Question: does polar duality expose a tractable statistic separating the sharp simplex from random centered lattice-free bodies?
import argparse,json,numpy as np,itertools
from scipy.spatial import ConvexHull,HalfspaceIntersection
ap=argparse.ArgumentParser();ap.add_argument('--samples',type=int,default=20000);ap.add_argument('--vertices',type=int,default=8);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/polar_stats.json');args=ap.parse_args();rng=np.random.default_rng(args.seed);Z=np.array([z for z in itertools.product(range(-7,8),repeat=3) if z!=(0,0,0)],float)
def center(p):
 h=ConvexHull(p);q=p.mean(0);V=0.;M=np.zeros(3)
 for tri in h.simplices:
  a,b,c=p[tri];v=abs(np.linalg.det(np.stack([a-q,b-q,c-q],1)))/6;V+=v;M+=v*(q+a+b+c)/4
 return p-M/V,V
def ev(p):
 try:p,V=center(p);h=ConvexHull(p);off=-h.equations[:,3];g=(Z@h.equations[:,:3].T/off).max(1);lam=g[g>1e-10].min();p*=lam;V*=lam**3;h=ConvexHull(p);polar=h.equations[:,:3]/(-h.equations[:,3,None]);PV=ConvexHull(polar).volume
 except:return None
 return V,PV,V*PV,len(h.vertices),len(polar)
rec=[]
for _ in range(args.samples):
 d=rng.normal(size=(args.vertices,3));d/=np.linalg.norm(d,axis=1)[:,None];r=ev(d*np.exp(rng.normal(0,.8,args.vertices))[:,None]);
 if r:rec.append(r)
rec.sort(reverse=True);json.dump({'top':[list(x) for x in rec[:200]]},open(args.out,'w'));print('best',rec[0],'min product top100',min(x[2] for x in rec[:100]))
