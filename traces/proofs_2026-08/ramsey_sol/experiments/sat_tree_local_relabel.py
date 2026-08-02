#!/usr/bin/env python3
"""SAT color lookup by (common prefix, unordered next symbols) on S_n.
Unlike a global quotient, each permutation-tree node may relabel its child edges.
"""
import argparse,itertools,json,time
from pysat.solvers import Solver

def state(a,b):
 i=next(i for i in range(len(a)) if a[i]!=b[i]);return (a[:i],min(a[i],b[i]),max(a[i],b[i]))
def build(n):
 V=list(itertools.permutations(range(n)));sts=sorted({state(a,b) for i,a in enumerate(V) for b in V[:i]});ix={s:i for i,s in enumerate(sts)};E=[[0]*len(V) for _ in V]
 for i,a in enumerate(V):
  for j,b in enumerate(V[:i]):E[i][j]=E[j][i]=ix[state(a,b)]
 C=set()
 for i in range(len(V)):
  for j in range(i):
   for h in range(j):C.add(tuple(sorted(set((E[i][j],E[i][h],E[j][h])))))
 return V,sts,sorted(C)
def run(n,k,out):
 t=time.time();V,S,C=build(n);one=[h for h in C if len(h)==1];print({'n':n,'V':len(V),'states':len(S),'constraints':len(C),'one':len(one),'build':time.time()-t},flush=True)
 if one:return
 def v(i,c):return i*k+c+1
 cl=[]
 for i in range(len(S)):
  cl.append([v(i,c) for c in range(k)])
  for c in range(k):
   for d in range(c):cl.append([-v(i,c),-v(i,d)])
 for h in C:
  for c in range(k):cl.append([-v(i,c) for i in h])
 cl.append([v(0,0)])
 with Solver(name='cadical195',bootstrap_with=cl) as sol:
  ok=sol.solve();print('SAT' if ok else 'UNSAT','elapsed',time.time()-t,flush=True)
  if ok:
   M=set(sol.get_model());col=[next(c for c in range(k) if v(i,c) in M) for i in range(len(S))];json.dump({'n':n,'k':k,'states':[[list(p),a,b] for p,a,b in S],'colors':col},open(out,'w'))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=5);p.add_argument('--k',type=int,default=5);p.add_argument('--out',default='experiments/tree_relabel.json');a=p.parse_args();run(a.n,a.k,a.out)
