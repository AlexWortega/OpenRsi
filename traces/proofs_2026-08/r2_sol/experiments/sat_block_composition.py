#!/usr/bin/env python3
# Question: can two translation partitions be block-composed using fewer than the sum of their colors?
import argparse,json,time
from itertools import combinations
from pysat.formula import CNF
from pysat.solvers import Solver
ap=argparse.ArgumentParser();ap.add_argument('--seed',default='experiments/f2_7_5.json');ap.add_argument('-q',type=int,default=9);ap.add_argument('--solver',default='cadical195');ap.add_argument('--out',default='experiments/block_composition.json');args=ap.parse_args()
classes=json.load(open(args.seed));k=len(classes);d=(max(max(C) for C in classes)).bit_length(); col=[-1]*(1<<d)
for i,C in enumerate(classes):
 for x in C:col[x]=i
# State 0 denotes zero; states 1..k denote a seed color. Record all realizable addition triples of states.
def st(x):return 0 if x==0 else col[x]+1
R=set()
for x in range(1<<d):
 for y in range(x,1<<d):R.add(tuple(sorted((st(x),st(y),st(x^y)))))
states=[(a,b) for a in range(k+1) for b in range(k+1) if (a,b)!=(0,0)];idx={s:i for i,s in enumerate(states)}
# Product-state triples realizable coordinatewise; ignore repetitions corresponding to equal group vectors.
T=set()
for r1 in R:
 for r2 in R:
  # all alignments matter because sorted coordinate triples lose pairing.
  import itertools
  for p in set(itertools.permutations(r2)):
   ss=tuple(sorted((idx[(r1[j],p[j])] for j in range(3)))) if all((r1[j],p[j])!=(0,0) for j in range(3)) else None
   if ss is not None:T.add(ss)
def v(s,c):return s*args.q+c+1
cnf=CNF()
for s in range(len(states)):
 cnf.append([v(s,c) for c in range(args.q)])
 for a,b in combinations(range(args.q),2):cnf.append([-v(s,a),-v(s,b)])
for tri in T:
 for c in range(args.q):cnf.append([-v(tri[0],c),-v(tri[1],c),-v(tri[2],c)])
cnf.append([v(0,0)])
t=time.time()
with Solver(name=args.solver,bootstrap_with=cnf.clauses) as sol:
 ok=sol.solve();print(json.dumps({'sat':ok,'seed_colors':k,'dimension':d,'output_colors':args.q,'states':len(states),'state_triples':len(T),'seconds':time.time()-t}),flush=True)
 if ok:
  m={x for x in sol.get_model() if x>0};mapping={f'{a},{b}':next(c for c in range(args.q) if v(idx[(a,b)],c) in m) for a,b in states}
  json.dump({'seed':args.seed,'q':args.q,'mapping':mapping},open(args.out,'w'),indent=2);print('wrote',args.out,flush=True)
