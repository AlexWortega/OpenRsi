#!/usr/bin/env python3
# Question: what symmetric-core ratios occur for centered prisms and bipyramids?
import numpy as np
from scipy.spatial import ConvexHull,HalfspaceIntersection
for typ in ['prism','bipyramid']:
 for m in range(3,13):
  a=np.arange(m)*2*np.pi/m;P=np.c_[np.cos(a),np.sin(a)]
  V=np.vstack([np.c_[P,-np.ones(m)],np.c_[P,np.ones(m)]]) if typ=='prism' else np.vstack([np.c_[P,np.zeros(m)],[0,0,-1],[0,0,1]])
  h=ConvexHull(V);E=h.equations;C=ConvexHull(HalfspaceIntersection(np.vstack([E,np.c_[-E[:,:3],E[:,3]]]),np.zeros(3)).intersections).volume
  print(typ,m,C/h.volume)
