#!/usr/bin/env python3
# Question: can F_2^6\{0} be partitioned into four sum-free classes?
import argparse, json, time
from itertools import combinations
from pysat.formula import CNF
from pysat.solvers import Solver

N,K=64,4
def var(x,c): return (x-1)*K+c+1
cnf=CNF()
for x in range(1,N):
    cnf.append([var(x,c) for c in range(K)])
    for a,b in combinations(range(K),2): cnf.append([-var(x,a),-var(x,b)])
# Each F_2 projective line {x,y,x+y} is nonmonochromatic.
lines=[]
for x in range(1,N):
  for y in range(x+1,N):
    z=x^y
    if y<z:
      lines.append((x,y,z))
      for c in range(K): cnf.append([-var(x,c),-var(y,c),-var(z,c)])
ap=argparse.ArgumentParser(); ap.add_argument('--solver',default='cadical195'); ap.add_argument('--out',default='experiments/f2_6_solution.json'); ap.add_argument('--strong-symmetry',action='store_true'); ap.add_argument('--sixth-color',type=int,choices=range(K)); args=ap.parse_args()
# Color permutation and GL(6,2) permit vector 1 to have color zero.  Strong mode is
# also sound: a largest class has >=16 vectors, hence rank >=5 (a 4-space has only
# 15 nonzero vectors), so five independent members can be mapped to e_1,...,e_5.
cnf.append([var(1,0)])
if args.strong_symmetry:
    for x in (2,4,8,16): cnf.append([var(x,0)])
if args.sixth_color is not None:
    cnf.append([var(32,args.sixth_color)])
t=time.time()
with Solver(name=args.solver,bootstrap_with=cnf.clauses) as s:
    ok=s.solve()
    print(json.dumps({'sat':ok,'seconds':time.time()-t,'variables':N*K-K,'clauses':len(cnf.clauses),'lines':len(lines)}),flush=True)
    if ok:
      m=set(v for v in s.get_model() if v>0)
      classes=[[x for x in range(1,N) if var(x,c) in m] for c in range(K)]
      with open(args.out,'w') as f: json.dump(classes,f,indent=2)
      print('sizes',list(map(len,classes)),'wrote',args.out,flush=True)
