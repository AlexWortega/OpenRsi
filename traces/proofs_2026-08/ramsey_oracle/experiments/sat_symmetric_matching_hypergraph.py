#!/usr/bin/env python3
"""SAT for a 3-graph whose triangle-free links separate all perfect matchings."""
import sys,json
from itertools import combinations
from pysat.formula import CNF
from pysat.solvers import Solver
n=int(sys.argv[1]) if len(sys.argv)>1 else 8
trip=list(combinations(range(n),3));tid={t:i+1 for i,t in enumerate(trip)}
def v(a,b,c):return tid[tuple(sorted((a,b,c)))]
def matchings(xs):
 xs=tuple(xs)
 if not xs:yield ();return
 a=xs[0]
 for j in range(1,len(xs)):
  b=xs[j]
  for t in matchings(xs[1:j]+xs[j+1:]):yield ((a,b),)+t
MS=list(matchings(range(n)))
def partner(M):
 p=[None]*n
 for a,b in M:p[a]=b;p[b]=a
 return p
P=list(map(partner,MS));cnf=CNF()
# Link at i triangle-free: forbid iab,iac,ibc.
for i in range(n):
 for a,b,c in combinations([z for z in range(n) if z!=i],3):cnf.append([-v(i,a,b),-v(i,a,c),-v(i,b,c)])
for x,y in combinations(range(len(P)),2):
 clause=set()
 for i in range(n):
  if P[x][i]!=P[y][i]:clause.add(v(i,P[x][i],P[y][i]))
 cnf.append(list(clause))
print('n',n,'matchings',len(P),'vars',len(trip),'clauses',len(cnf.clauses),flush=True)
with Solver(name='cadical195',bootstrap_with=cnf.clauses) as s:
 ok=s.solve();print('SAT',ok)
 if ok:
  model={z for z in s.get_model() if z>0};T=[list(t) for t in trip if tid[t] in model]
  json.dump({'n':n,'triples':T},open(f'experiments/matching_hypergraph_n{n}.json','w'))
