#!/usr/bin/env python3
# Question: can exact rational centered pyramids violate the suspected 1/2 symmetric-core ratio?
# Enumerate small integer planar bases, construct the uniquely centered apex, and compute core ratio numerically.
import argparse,itertools,json,numpy as np
from scipy.spatial import ConvexHull,HalfspaceIntersection
ap=argparse.ArgumentParser();ap.add_argument('--box',type=int,default=2);ap.add_argument('--out',default='experiments/pyramid_enum.json');args=ap.parse_args();pts=list(itertools.product(range(-args.box,args.box+1),repeat=2));best=[]
def cen(P):
 h=ConvexHull(P);Q=P[h.vertices];A=0.;M=np.zeros(2)
 for a,b in zip(Q,np.roll(Q,-1,axis=0)):z=a[0]*b[1]-a[1]*b[0];A+=z;M+=z*(a+b)
 return M/(3*A),Q
for m in [4,5]:
 for S in itertools.combinations(pts,m):
  try:c,Q=cen(np.array(S,float))
  except:continue
  if len(Q)<m:continue
  V=np.vstack([np.c_[Q,-np.ones(m)],[-3*c[0],-3*c[1],3]])
  try:h=ConvexHull(V);E=h.equations;C=ConvexHull(HalfspaceIntersection(np.vstack([E,np.c_[-E[:,:3],E[:,3]]]),np.zeros(3)).intersections).volume;r=C/h.volume
  except:continue
  best.append((r,S))
best.sort(key=lambda x:x[0]);out={'box':args.box,'tested':len(best),'min_ratio':best[0][0],'min_base':best[0][1]};json.dump(out,open(args.out,'w'),indent=2);print(json.dumps(out))
