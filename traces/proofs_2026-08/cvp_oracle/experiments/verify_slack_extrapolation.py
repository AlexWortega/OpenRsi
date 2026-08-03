#!/usr/bin/env python3
"""Verify affine extrapolation of linear clause-slack witnesses exactly."""
from __future__ import annotations
import random,numpy as np

def run(seed=173,trials=500):
 rng=random.Random(seed);checks=0
 for rows in (1,2,5,9):
  for cols in (1,3,7):
   for _ in range(trials//4):
    A=np.array([[rng.randrange(-7,8) for _ in range(cols)] for _ in range(rows)],dtype=object)
    # Choose arbitrary witnesses for true counts 1 and 2; define corresponding affine RHS.
    w1=np.array([rng.randrange(-5,6) for _ in range(cols)],dtype=object)
    w2=np.array([rng.randrange(-5,6) for _ in range(cols)],dtype=object)
    # The difference between RHS values must equal one copy of a fixed literal contribution h.
    h=A.dot(w1-w2)
    target=h+A.dot(w1) # c*h + A w_c = target at c=1
    assert np.all(h+A.dot(w1)==target)
    assert np.all(2*h+A.dot(w2)==target)
    w0=2*w1-w2
    assert np.all(A.dot(w0)==target)
    assert np.linalg.norm(np.asarray(w0,dtype=float)) <= 2*np.linalg.norm(np.asarray(w1,dtype=float))+np.linalg.norm(np.asarray(w2,dtype=float))+1e-9
    for mod in (2,3,5,6,11):assert np.all(np.asarray(A.dot(w0)-target,dtype=int)%mod==0)
    checks+=1
 print({'integer_linear_slack_extrapolations':checks,'row_sizes':[1,2,5,9],
        'column_sizes':[1,3,7],'identity':'w_false=2*w_count1-w_count2'})
if __name__=='__main__':run()
