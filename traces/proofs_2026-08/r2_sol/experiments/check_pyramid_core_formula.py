#!/usr/bin/env python3
# Question: for centered pyramids, how does the symmetric-core ratio depend on overlap of translated homothetic base sections?
# Monte Carlo diagnostic for regular and random planar bases; not a proof.
import numpy as np
from scipy.spatial import ConvexHull,HalfspaceIntersection
for m in range(3,11):
 a=np.arange(m)*2*np.pi/m;B=np.c_[np.cos(a),np.sin(a),-np.ones(m)];V=np.vstack([B,[0,0,3]]);h=ConvexHull(V);E=h.equations;C=ConvexHull(HalfspaceIntersection(np.vstack([E,np.c_[-E[:,:3],E[:,3]]]),np.zeros(3)).intersections).volume
 print(m,C/h.volume)
