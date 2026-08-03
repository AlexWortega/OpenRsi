#!/usr/bin/env python3
"""Attack random nonlocal scopes on the scalable padded 3-color cycle CNF."""
from __future__ import annotations
import argparse,random,sys
sys.path.insert(0,'experiments')
from verify_odd_cycle_counterexample import permutation_cycle_cnf
from random_scope_3sat import scopes_random,build
from search_pseudoviews import gf2_solve

def run(cases=None,seed=277):
 if cases is None:cases=[(3,2,1),(3,3,1),(4,2,1),(4,3,1),(4,3,2),(4,4,1),(5,3,1)]
 out=[]
 for off,(n,d,mult) in enumerate(cases):
  C,*_=permutation_cycle_cnf(n);rng=random.Random(seed+2*off)
  S=scopes_random(len(C),d,mult*len(C),rng);H,t,info=build(C,S);sol=gf2_solve(H,t)
  out.append({'n':n,'clauses':len(C),'scope_clauses_d':d,'random_scope_multiplier':mult,
   'groups':len(S),'shape':H.shape,'exact_feasible':sol is not None,
   'one_solution_weight':None if sol is None else sol.bit_count()})
 print(out);return out
if __name__=='__main__':run()
