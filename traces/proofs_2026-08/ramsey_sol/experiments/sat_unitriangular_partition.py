#!/usr/bin/env python3
"""Exact SAT for inverse-orbit product-free chromatic number of UT(n,2)."""
import argparse,json
from pysat.solvers import Solver
from pysat.card import CardEnc,EncType
from unitriangular_partition import build
p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=4);p.add_argument('--k',type=int,default=4);p.add_argument('--out');a=p.parse_args()
N,O,C,one,pos=build(a.n);print({'order':N,'orbits':len(O),'constraints':len(C),'one':len(one)},flush=True)
if one:raise SystemExit('one-state obstruction')
def v(i,c):return i*a.k+c+1
cla=[]
for i in range(len(O)):
 cla.append([v(i,c) for c in range(a.k)])
 for c in range(a.k):
  for d in range(c):cla.append([-v(i,c),-v(i,d)])
for h in C:
 for c in range(a.k):cla.append([-v(i,c) for i in h])
# color symmetry: orbit 0 gets color 0, first use order
cla.append([v(0,0)])
for i in range(1,len(O)):
 for c in range(1,a.k):cla.append([-v(i,c)]+[v(j,c-1) for j in range(i)])
with Solver(name='cadical195',bootstrap_with=cla) as s:
 ok=s.solve();print('SAT' if ok else 'UNSAT',flush=True)
 if ok:
  M=set(s.get_model());colors=[next(c for c in range(a.k) if v(i,c) in M) for i in range(len(O))]
  r={'n':a.n,'k':a.k,'order':N,'orbits':O,'colors':colors,'best':0}
  json.dump(r,open(a.out or f'experiments/ut{a.n}_k{a.k}_sat.json','w'))
