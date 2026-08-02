#!/usr/bin/env python3
"""Compute binary-pattern independent sets giving fractional covers of generalized shift graphs."""
import argparse,numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import coo_matrix

def calc(r):
 N=1<<r;mask=(1<<(r-1))-1;E=[]
 for x in range(N):
  for bit in (0,1):
   y=((x&mask)<<1)|bit
   if x!=y:E.append(tuple(sorted((x,y))))
 E=sorted(set(E));rows=[];cols=[]
 for i,(x,y) in enumerate(E):rows += [i,i];cols += [x,y]
 A=coo_matrix((np.ones(len(rows)),(rows,cols)),shape=(len(E),N)).tocsr()
 res=milp(-np.ones(N),integrality=np.ones(N),bounds=Bounds(0,1),constraints=LinearConstraint(A,0,1),options={'time_limit':60})
 alpha=round(-res.fun) if res.fun is not None else None
 return N,len(E),alpha,N/alpha if alpha else None,res.message
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--max-r',type=int,default=12);a=p.parse_args()
 for r in range(2,a.max_r+1):print(r,calc(r),flush=True)
