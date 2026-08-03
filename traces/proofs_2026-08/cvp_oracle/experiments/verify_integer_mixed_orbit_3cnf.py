#!/usr/bin/env python3
"""Finite exact-3CNF checks for the integer mixed-orbit obstruction."""
import sys
sys.path.insert(0,'experiments')
from integer_mixed_orbit_3cnf import run,make_formula,perm,COLORS

records=run(((3,1),(4,2)))
assert all(r['exact'] and r['d']<r['n'] for r in records)
for r in records:
 clauses,attach,nv,aux=make_formula(r['n'])
 assert len(clauses)==r['clauses']==43*r['n'] and nv==r['vars']==27*r['n']
 assert r['squared_norm'] <= 25*r['groups']
 assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in clauses)
 occ={i:0 for i in range(1,nv+1)}
 for c in clauses:
  for lit in c:occ[abs(lit)]+=1
 assert max(occ.values())==17
# The one-hot/equivalence semantics force an impossible fixed point globally.
assert all(perm(True,x)!=x for x in COLORS)
print('exact-3CNF mixed-orbit integer obstruction finite instances verified')
