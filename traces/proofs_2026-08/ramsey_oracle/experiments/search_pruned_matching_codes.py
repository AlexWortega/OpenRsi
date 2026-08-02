#!/usr/bin/env python3
"""Search switch-free factorial matching subfamilies with triangle-free coordinate separators."""
import sys,random,json
from itertools import combinations
from pysat.formula import CNF
from pysat.solvers import Solver
n=int(sys.argv[1]) if len(sys.argv)>1 else 8
runs=int(sys.argv[2]) if len(sys.argv)>2 else 200
def matchings(xs):
 xs=tuple(xs)
 if not xs:yield ();return
 a=xs[0]
 for j in range(1,len(xs)):
  b=xs[j]
  for z in matchings(xs[1:j]+xs[j+1:]):yield ((a,b),)+z
def partner(M):
 p=[None]*n
 for a,b in M:p[a]=b;p[b]=a
 return tuple(p)
W=list(map(partner,matchings(range(n))))
def switch(x,y):return sum(x[i]!=y[i] for i in range(n))==4
best=[]
for _ in range(runs):
 random.shuffle(W);C=[]
 for x in W:
  if all(not switch(x,y) for y in C):C.append(x)
 if len(C)>len(best):best=C[:]
print('n',n,'matchings',len(W),'switch_free',len(best),flush=True)
pairs=list(combinations(range(n),2));pid={e:j for j,e in enumerate(pairs)}
def v(i,a,b):return 1+i*len(pairs)+pid[tuple(sorted((a,b)))]
cnf=CNF()
for i in range(n):
 for a,b,c in combinations([x for x in range(n) if x!=i],3):cnf.append([-v(i,a,b),-v(i,a,c),-v(i,b,c)])
for x,y in combinations(best,2):cnf.append([v(i,x[i],y[i]) for i in range(n) if x[i]!=y[i]])
with Solver(name='cadical195',bootstrap_with=cnf.clauses) as s:
 ok=s.solve();print('SAT',ok,'base',len(best)**(1/n),flush=True)
 if ok:
  model={z for z in s.get_model() if z>0};G=[]
  for i in range(n):G.append([list(e) for e in pairs if i not in e and v(i,*e) in model])
  json.dump({'n':n,'words':best,'graphs':G},open(f'experiments/pruned_matching_n{n}.json','w'))
