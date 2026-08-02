#!/usr/bin/env python3
# Question: does a verified cyclic k-coloring contain a large induced subcoloring in which every selected vertex misses one color?
import argparse,json,time
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc,EncType
from pysat.solvers import Solver
ap=argparse.ArgumentParser();ap.add_argument('-p',type=int,default=127);ap.add_argument('-k',type=int,default=5);ap.add_argument('-N',type=int,required=True);ap.add_argument('--solver',default='cadical195');ap.add_argument('--out',default='experiments/local_subset.json');args=ap.parse_args();p,k=args.p,args.k
C=json.load(open(f'experiments/cyclic_{p}_{k}.json'));col={x:i for i,S in enumerate(C) for x in S};pool=IDPool();X=[pool.id(('x',v)) for v in range(p)];M=[[pool.id(('m',v,c)) for c in range(k)] for v in range(p)];cnf=CNF()
for v in range(p):
 cnf.append([-X[v],*M[v]])
 for c in range(k):
  cnf.append([-M[v][c],X[v]])
  for w in range(p):
   if w!=v and col[(w-v)%p]==c:cnf.append([-M[v][c],-X[w]])
cnf.extend(CardEnc.atleast(X,bound=args.N,vpool=pool,encoding=EncType.totalizer).clauses)
t=time.time()
with Solver(name=args.solver,bootstrap_with=cnf.clauses) as s:
 ok=s.solve();print(json.dumps({'sat':ok,'p':p,'k':k,'target':args.N,'seconds':time.time()-t,'vars':pool.top,'clauses':len(cnf.clauses)}),flush=True)
 if ok:
  mod={x for x in s.get_model() if x>0};V=[v for v in range(p) if X[v] in mod][:args.N];json.dump({'p':p,'k':k,'vertices':V,'classes':C},open(args.out,'w'),indent=2);print('wrote',len(V),args.out,flush=True)
