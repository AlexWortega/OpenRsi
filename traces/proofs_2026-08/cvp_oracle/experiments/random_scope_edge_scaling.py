#!/usr/bin/env python3
"""Coverage/output scaling for random d-edge scopes on cycles."""
from __future__ import annotations
import math

def requirements(n,d,fail=None):
 if fail is None:fail=1/n
 p=d*(d-1)/(n*(n-1))
 # Union bound n*(1-p)^m <= fail.
 m=math.ceil(math.log(n/fail)/(-math.log1p(-p))) if p else math.inf
 # A forest d-edge scope has at most 2d vertices and <=3^(d+components) colorings; upper use 3^(2d).
 views_upper=3**(2*d)
 return m,views_upper,m*views_upper

def run():
 out=[]
 for n in (64,256,1024,4096):
  for d in (3,math.ceil(math.log2(n)),math.ceil(math.sqrt(n))):
   m,v,total=requirements(n,d);out.append({'n':n,'d':d,'required_scopes_union_bound':m,
    'views_upper_per_scope':v,'column_upper':m*v,'log_n_column_upper':math.log(m*v,n)})
 print(out);return out
if __name__=='__main__':run()
