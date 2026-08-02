#!/usr/bin/env python3
"""SAT test: separate all perfect matchings by coordinate triangle-free graphs."""
import sys,json
from itertools import combinations
from pysat.formula import CNF
from pysat.solvers import Solver

def matchings(xs):
 xs=tuple(xs)
 if not xs:yield ();return
 a=xs[0]
 for j in range(1,len(xs)):
  b=xs[j]
  for tail in matchings(xs[1:j]+xs[j+1:]):yield ((a,b),)+tail
n=int(sys.argv[1]) if len(sys.argv)>1 else 6
MS=list(matchings(range(n)));pairs=list(combinations(range(n),2));pid={p:i for i,p in enumerate(pairs)}
def var(i,u,v):
 if u>v:u,v=v,u
 return 1+i*len(pairs)+pid[(u,v)]
def partner(M):
 p=[None]*n
 for a,b in M:p[a]=b;p[b]=a
 return p
P=[partner(M) for M in MS];cnf=CNF()
# H_i triangle-free; edges involving symbol i are irrelevant but harmless and excluded.
for i in range(n):
 for a,b,c in combinations([x for x in range(n) if x!=i],3):
  cnf.append([-var(i,a,b),-var(i,a,c),-var(i,b,c)])
for x,y in combinations(range(len(MS)),2):
 clause=[]
 for i in range(n):
  if P[x][i]!=P[y][i]:clause.append(var(i,P[x][i],P[y][i]))
 cnf.append(clause)
print('n',n,'matchings',len(MS),'vars',n*len(pairs),'clauses',len(cnf.clauses),flush=True)
with Solver(name='cadical195',bootstrap_with=cnf.clauses) as s:
 ok=s.solve();print('SAT',ok,flush=True)
 if ok:
  model={z for z in s.get_model() if z>0};out=[]
  for i in range(n):out.append([[a,b] for a,b in pairs if i not in (a,b) and var(i,a,b) in model])
  json.dump({'n':n,'graphs':out},open(f'experiments/matching_partner_n{n}.json','w'))
