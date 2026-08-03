#!/usr/bin/env python3
"""Verify the universal two-nearby-lattice-points extrapolation inequality."""
from __future__ import annotations
import random,numpy as np

def run(seed=211,trials=2000):
 rng=random.Random(seed);checks=0;max_ratio=0
 for dim in (1,2,5,10):
  for _ in range(trials//4):
   B=np.array([[rng.randrange(-5,6) for _ in range(dim)] for _ in range(dim)],dtype=float)
   a=np.array([rng.randrange(-4,5) for _ in range(dim)],dtype=float)
   b=np.array([rng.randrange(-4,5) for _ in range(dim)],dtype=float)
   t=np.array([rng.uniform(-8,8) for _ in range(dim)])
   p0=B.dot(a);p1=B.dot(b);p2=2*p0-p1
   # p2=B(2a-b) remains a lattice point.
   assert np.allclose(p2,B.dot(2*a-b))
   lhs=np.linalg.norm(p2-t);rhs=2*np.linalg.norm(p0-t)+np.linalg.norm(p1-t)
   assert lhs<=rhs+1e-9
   denom=max(np.linalg.norm(p0-t),np.linalg.norm(p1-t))
   if denom:max_ratio=max(max_ratio,lhs/denom)
   checks+=1
 print({'integer_lattice_extrapolations':checks,'dimension_set':[1,2,5,10],
        'maximum_observed_ratio_to_larger_branch_radius':max_ratio,'proved_upper_bound':3})
if __name__=='__main__':run()
