#!/usr/bin/env python3
"""SAT compression of full (first-difference position, symbol-pair) labels on S_n."""
import argparse,itertools,json,time
from pysat.solvers import Solver

def edge(a,b):
 i=next(i for i in range(len(a)) if a[i]!=b[i]);return (i,min(a[i],b[i]),max(a[i],b[i]))
def build(n):
 V=list(itertools.permutations(range(n))); labels=sorted({edge(a,b) for i,a in enumerate(V) for b in V[:i]});ix={x:i for i,x in enumerate(labels)};C=set();one=[]
 E=[[None]*len(V) for _ in V]
 for i,a in enumerate(V):
  for j,b in enumerate(V[:i]):E[i][j]=E[j][i]=ix[edge(a,b)]
 for i in range(len(V)):
  for j in range(i):
   for h in range(j):
    z=tuple(sorted(set((E[i][j],E[i][h],E[j][h]))));C.add(z)
    if len(z)==1:one.append((i,j,h,z[0]))
 return V,labels,sorted(C),one
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=4);p.add_argument('--k',type=int,default=4);p.add_argument('--out');a=p.parse_args();t=time.time();V,L,C,one=build(a.n);print({'n':a.n,'vertices':len(V),'states':len(L),'constraints':len(C),'one':len(one),'build_s':time.time()-t},flush=True)
 if one:raise SystemExit('one-state obstruction')
 def v(i,c):return i*a.k+c+1
 clauses=[]
 for i in range(len(L)):
  clauses.append([v(i,c) for c in range(a.k)])
  for c in range(a.k):
   for d in range(c):clauses.append([-v(i,c),-v(i,d)])
 for h in C:
  for c in range(a.k):clauses.append([-v(i,c) for i in h])
 clauses.append([v(0,0)])
 # first-use color symmetry
 for i in range(1,len(L)):
  for c in range(1,a.k):clauses.append([-v(i,c)]+[v(j,c-1) for j in range(i)])
 with Solver(name='cadical195',bootstrap_with=clauses) as s:
  ok=s.solve();print('SAT' if ok else 'UNSAT','solve_s',time.time()-t,flush=True)
  if ok:
   M=set(s.get_model());colors=[next(c for c in range(a.k) if v(i,c) in M) for i in range(len(L))];json.dump({'n':a.n,'k':a.k,'labels':L,'colors':colors},open(a.out or f'experiments/permstate_n{a.n}_k{a.k}.json','w'))
