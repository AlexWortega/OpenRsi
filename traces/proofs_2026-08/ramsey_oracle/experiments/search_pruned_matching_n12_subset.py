#!/usr/bin/env python3
"""Find a verifiable n=12 matching code by shrinking saved-in-memory greedy family."""
import random,json
from itertools import combinations
from pysat.formula import CNF
from pysat.solvers import Solver
n=12
def matchings(xs):
 xs=tuple(xs)
 if not xs:yield ();return
 a=xs[0]
 for j in range(1,len(xs)):
  b=xs[j]
  for z in matchings(xs[1:j]+xs[j+1:]):yield ((a,b),)+z
def p(M):
 z=[None]*n
 for a,b in M:z[a]=b;z[b]=a
 return tuple(z)
W=list(map(p,matchings(range(n))));random.seed(4);random.shuffle(W);C=[]
for x in W:
 if all(sum(a!=b for a,b in zip(x,y))!=4 for y in C):C.append(x)
print('switchfree',len(C),flush=True)
pairs=list(combinations(range(n),2));pid={e:j for j,e in enumerate(pairs)}
def v(i,a,b):return 1+i*len(pairs)+pid[tuple(sorted((a,b)))]
base=CNF()
for i in range(n):
 for a,b,c in combinations([x for x in range(n) if x!=i],3):base.append([-v(i,a,b),-v(i,a,c),-v(i,b,c)])
for target in [300,200,150,100]:
 S=C[:target];cnf=CNF(from_clauses=base.clauses)
 for x,y in combinations(S,2):cnf.append([v(i,x[i],y[i]) for i in range(n) if x[i]!=y[i]])
 print('try',target,len(cnf.clauses),flush=True)
 with Solver(name='cadical195',bootstrap_with=cnf.clauses) as s:
  if s.solve():
   model={z for z in s.get_model() if z>0};G=[]
   for i in range(n):G.append([list(e) for e in pairs if i not in e and v(i,*e) in model])
   json.dump({'n':n,'words':S,'graphs':G},open('experiments/pruned_matching_n12.json','w'));print('SAT',target,target**(1/n));break
