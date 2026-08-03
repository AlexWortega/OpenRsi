#!/usr/bin/env python3
"""Exact all-d-subset scope hierarchy on inconsistent 3-color cycles."""
from __future__ import annotations
import argparse,itertools,sys
sys.path.insert(0,'experiments')
from random_scope_edge_full import build
from search_pseudoviews import gf2_solve

def run(cases=((6,2),(6,3),(8,2),(8,3),(10,2),(12,2),(16,2),(20,2),(24,2),(30,2),(40,2)),max_rows=2_000_000):
 out=[]
 for n,d in cases:
  S={frozenset((e,)) for e in range(n)}
  S.update(frozenset(E) for E in itertools.combinations(range(n),d))
  S=sorted(S,key=lambda x:(len(x),tuple(x)))
  H,t,info=build(n,S)
  if H.shape[0]>max_rows:x='skipped'
  else:x=gf2_solve(H,t)
  out.append({'n':n,'d':d,'groups':len(S),'shape':H.shape,
   'exact_feasible':None if x=='skipped' else x is not None,
   'one_solution_weight':None if x=='skipped' or x is None else x.bit_count(),
   'max_views':max(len(A) for V,A in info)})
 print(out);return out
if __name__=='__main__':run()
