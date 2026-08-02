#!/usr/bin/env python3
# Question: does the Grötzsch complement strong cube have an independent code of size at least 12?
import argparse,json,time
from itertools import combinations
import networkx as nx
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc,EncType
from pysat.solvers import Solver

ap=argparse.ArgumentParser();ap.add_argument('--target',type=int,default=12);ap.add_argument('--solver',default='cadical195');ap.add_argument('--out',default='experiments/grotzsch_cube_code.json');args=ap.parse_args()
H=nx.mycielskian(nx.cycle_graph(5)) # triangle-free 11-vertex Grötzsch graph
n=len(H); words=[(i//(n*n),(i//n)%n,i%n) for i in range(n**3)]
edges={tuple(sorted(e)) for e in H.edges()}
def compatible(a,b):return any(tuple(sorted((a[j],b[j]))) in edges for j in range(3))
cnf=CNF(); bad=0
for i,j in combinations(range(len(words)),2):
 if not compatible(words[i],words[j]):cnf.append([-(i+1),-(j+1)]);bad+=1
vpool=IDPool(start_from=len(words)+1)
cnf.extend(CardEnc.atleast(list(range(1,len(words)+1)),bound=args.target,vpool=vpool,encoding=EncType.totalizer).clauses)
t=time.time()
with Solver(name=args.solver,bootstrap_with=cnf.clauses) as s:
 ok=s.solve(); print(json.dumps({'sat':ok,'target':args.target,'seconds':time.time()-t,'words':len(words),'incompatible_pairs':bad,'clauses':len(cnf.clauses)}),flush=True)
 if ok:
  model=set(x for x in s.get_model() if x>0); code=[words[i] for i in range(len(words)) if i+1 in model]
  # Trim because at-least encoding may return more than target.
  code=code[:args.target]
  with open(args.out,'w') as f:json.dump(code,f,indent=2)
  print('code',code,flush=True)
