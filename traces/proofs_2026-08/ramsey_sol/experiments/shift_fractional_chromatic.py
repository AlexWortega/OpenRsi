#!/usr/bin/env python3
"""Exact-by-enumeration LP diagnostic for fractional chromatic numbers of shift graphs.
Numerical output is heuristic evidence until converted to a rational certificate.
"""
import argparse,itertools,numpy as np
from scipy.optimize import linprog

def solve(n):
 V=[(a,b) for a in range(n) for b in range(a+1,n)]; idx={e:i for i,e in enumerate(V)}; sets=set()
 # An independent set has no label used both as a head and as a tail; enumerate
 # assignments: 0 unused, 1 tail side, 2 head side.
 for z in itertools.product(range(3),repeat=n):
  S=tuple(idx[(a,b)] for a,b in V if z[a]==1 and z[b]==2)
  if S: sets.add(S)
 sets=sorted(sets); A=np.zeros((len(V),len(sets)))
 for j,S in enumerate(sets): A[list(S),j]=1
 res=linprog(np.ones(len(sets)),A_ub=-A,b_ub=-np.ones(len(V)),bounds=(0,None),method='highs')
 assert res.success
 # Dual vertex weights y satisfy sum_{v in I}y_v<=1; objective sum y.
 dual=-res.ineqlin.marginals
 return len(V),len(sets),res.fun,dual
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--max-n',type=int,default=10);a=p.parse_args()
 for n in range(3,a.max_n+1):
  v,s,x,y=solve(n); print(n,v,s,repr(x),'dual-range',float(y.min()),float(y.max()),flush=True)
