#!/usr/bin/env python3
# Question: can cyclic seeds contain large induced subsets where every vertex misses at least two colors, enabling stronger missing-color blow-ups?
import argparse,json,time
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc,EncType
from pysat.solvers import Solver
ap=argparse.ArgumentParser();ap.add_argument('-p',type=int);ap.add_argument('-k',type=int);ap.add_argument('-N',type=int);ap.add_argument('-t',type=int,default=2);ap.add_argument('--out',default='experiments/multi_missing.json');args=ap.parse_args();p,k,N,t=args.p,args.k,args.N,args.t
C=json.load(open(f'experiments/cyclic_{p}_{k}.json'));col={x:i for i,S in enumerate(C) for x in S};pool=IDPool();X=[pool.id(('x',v)) for v in range(p)];M=[[pool.id(('m',v,c)) for c in range(k)] for v in range(p)];cnf=CNF()
for v in range(p):
 # Conditional cardinality: if X_v, at least t of the k missing-color flags hold.
 # Equivalently every (k-t+1)-subset contains a true flag.
 import itertools
 for S in itertools.combinations(range(k),k-t+1):cnf.append([-X[v],*[M[v][c] for c in S]])
 for c in range(k):
  cnf.append([-M[v][c],X[v]])
  for w in range(p):
   if w!=v and col[(w-v)%p]==c:cnf.append([-M[v][c],-X[w]])
cnf.extend(CardEnc.atleast(X,bound=N,vpool=pool,encoding=EncType.totalizer).clauses);st=time.time()
with Solver(name='cadical195',bootstrap_with=cnf.clauses) as s:
 ok=s.solve();print(json.dumps({'sat':ok,'p':p,'k':k,'N':N,'t':t,'seconds':time.time()-st}),flush=True)
 if ok:
  A={z for z in s.get_model() if z>0};V=[v for v in range(p) if X[v] in A][:N];json.dump({'p':p,'k':k,'vertices':V,'classes':C,'t':t},open(args.out,'w'),indent=2)
