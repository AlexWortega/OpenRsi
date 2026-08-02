#!/usr/bin/env python3
# Question: for centroid-zero planar B, is area(aB intersect -bB)/area(B) minimized by a triangle for every a,b, which would prove the 3D centered-pyramid core bound?
import argparse,json,numpy as np
from scipy.spatial import ConvexHull,HalfspaceIntersection
ap=argparse.ArgumentParser();ap.add_argument('--samples',type=int,default=50000);ap.add_argument('--vertices',type=int,default=8);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/scaled_planar_intersection.json');args=ap.parse_args();rng=np.random.default_rng(args.seed)
def center(P):
 h=ConvexHull(P);Q=P[h.vertices];A=0.;M=np.zeros(2)
 for x,y in zip(Q,np.roll(Q,-1,axis=0)):z=x[0]*y[1]-x[1]*y[0];A+=z;M+=z*(x+y)
 return Q-M/(3*A),abs(A)/2
zs=np.linspace(-1,1,17);mins={str(float(z)):10. for z in zs};arg={}
for _ in range(args.samples):
 a=np.sort(rng.uniform(0,2*np.pi,args.vertices));rad=np.exp(rng.normal(0,1,args.vertices));P=np.c_[rad*np.cos(a),rad*np.sin(a)]
 try:P,A=center(P)
 except:continue
 for z in zs:
  u=(3-z)/4;v=(3+z)/4;H1=ConvexHull(u*P).equations;H2=ConvexHull(-v*P).equations
  try:r=ConvexHull(HalfspaceIntersection(np.vstack([H1,H2]),np.zeros(2)).intersections).volume/A
  except:continue
  if r<mins[str(float(z))]:mins[str(float(z))]=r;arg[str(float(z))]=len(P)
json.dump({'samples':args.samples,'minimum_ratios':mins,'hull_vertices':arg},open(args.out,'w'),indent=2);print(json.dumps({'mins':mins,'arg':arg}))
