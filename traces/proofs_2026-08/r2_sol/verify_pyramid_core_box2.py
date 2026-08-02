#!/usr/bin/env python3
"""Independently reproduce the finite centered-pyramid core-ratio box-2 minimum."""
# Numerical finite benchmark only: robust margin above 1/2 is ~0.0076.
import itertools,numpy as np
from scipy.spatial import ConvexHull,HalfspaceIntersection
pts=list(itertools.product(range(-2,3),repeat=2));best=2.;count=0
for m in [4,5]:
 for S in itertools.combinations(pts,m):
  P=np.array(S,float)
  try:h=ConvexHull(P);Q=P[h.vertices]
  except:continue
  if len(Q)<m:continue
  A=0.;M=np.zeros(2)
  for a,b in zip(Q,np.roll(Q,-1,axis=0)):z=a[0]*b[1]-a[1]*b[0];A+=z;M+=z*(a+b)
  c=M/(3*A);V=np.vstack([np.c_[Q,-np.ones(m)],[-3*c[0],-3*c[1],3]])
  try:h=ConvexHull(V);E=h.equations;core=ConvexHull(HalfspaceIntersection(np.vstack([E,np.c_[-E[:,:3],E[:,3]]]),np.zeros(3)).intersections).volume
  except:continue
  best=min(best,core/h.volume);count+=1
assert count==19026 and abs(best-0.5076734000688732)<1e-10 and best>.507
print('verified numerical pyramid box-2 benchmark:',count,'minimum ratio',best)
