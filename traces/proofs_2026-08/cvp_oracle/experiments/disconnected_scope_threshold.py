#!/usr/bin/env python3
"""Exact GF(2) feasibility threshold for random disconnected scopes on odd holonomy cycles."""
from __future__ import annotations
import argparse,random,sys,time
sys.path.insert(0,'experiments')
from disconnected_scope_cycle import closure_scopes,build
from search_pseudoviews import gf2_solve

def instance(n,d,count,rng):
 base=[frozenset(rng.sample(range(n),d)) for _ in range(count)]
 base += [frozenset((e,)) for e in range(n)]
 scopes=closure_scopes(n,base);H,t,_=build(n,scopes)
 return gf2_solve(H,t) is not None,len(scopes),H.shape

def run(ns=(5,6,7,8,9,10),ds=(2,3),mults=(1,2),trials=10,seed=251):
 rng=random.Random(seed);rows=[]
 for n in ns:
  for d in ds:
   if d>=n:continue
   for mult in mults:
    vals=[];sizes=[]
    for _ in range(trials):
     feasible,K,shape=instance(n,d,mult*n,rng);vals.append(feasible);sizes.append((K,shape))
    rows.append({'n':n,'d':d,'count':mult*n,'trials':trials,'feasible':sum(vals),
      'infeasible':trials-sum(vals),'max_K':max(x[0] for x in sizes),
      'max_rows':max(x[1][0] for x in sizes),'max_cols':max(x[1][1] for x in sizes)})
 print(rows);return rows
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--trials',type=int,default=10);a=ap.parse_args();run(trials=a.trials)
