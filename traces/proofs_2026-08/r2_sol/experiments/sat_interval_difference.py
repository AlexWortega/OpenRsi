#!/usr/bin/env python3
# Question: exactly, does [N] admit a k-color translation difference rule with no monochromatic a,b,b-a?
import argparse,itertools,json,time
from pysat.formula import CNF
from pysat.solvers import Solver
ap=argparse.ArgumentParser();ap.add_argument('-N',type=int,default=128);ap.add_argument('-k',type=int,default=5);ap.add_argument('--solver',default='cadical195');ap.add_argument('--out',default='experiments/interval_sat.json');args=ap.parse_args();N,k=args.N,args.k
def v(d,c):return (d-1)*k+c+1
cnf=CNF()
for d in range(1,N):
 cnf.append([v(d,c) for c in range(k)])
 for a,b in itertools.combinations(range(k),2):cnf.append([-v(d,a),-v(d,b)])
for a in range(1,N):
 for b in range(a+1,N):
  for c in range(k):cnf.append([-v(a,c),-v(b,c),-v(b-a,c)])
cnf.append([v(1,0)])
t=time.time()
with Solver(name=args.solver,bootstrap_with=cnf.clauses) as s:
 ok=s.solve();print(json.dumps({'sat':ok,'N':N,'k':k,'seconds':time.time()-t,'clauses':len(cnf.clauses)}),flush=True)
 if ok:
  M={x for x in s.get_model() if x>0};colors=[0]+[next(c for c in range(k) if v(d,c) in M) for d in range(1,N)];json.dump({'N':N,'k':k,'colors':colors},open(args.out,'w'));print('wrote',args.out)
