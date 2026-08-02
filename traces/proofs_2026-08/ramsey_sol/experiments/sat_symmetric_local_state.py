#!/usr/bin/env python3
"""SAT quotient of S_n by state (least moved i, p(i), p^{-1}(i)), symmetrized."""
import argparse,itertools,json,time
from pysat.solvers import Solver

def comp(p,q):return tuple(p[q[i]]for i in range(len(p)))
def inv(p):
 z=[0]*len(p)
 for i,x in enumerate(p):z[x]=i
 return tuple(z)
def state(p):
 ip=inv(p);i=next(i for i in range(len(p))if p[i]!=i);a,b=sorted((p[i],ip[i]));return(i,a,b)
def run(n,k,out):
 t=time.time();P=list(itertools.permutations(range(n)));e=tuple(range(n));S=sorted({state(p)for p in P if p!=e});ix={s:i for i,s in enumerate(S)};C=set();one=[]
 for x in P:
  if x==e:continue
  for y in P:
   if y==e:continue
   z=comp(x,y)
   if z!=e:
    h=tuple(sorted(set((ix[state(x)],ix[state(y)],ix[state(z)]))));C.add(h)
    if len(h)==1:one.append((x,y,z))
 print({'n':n,'states':len(S),'constraints':len(C),'one':len(one),'build':time.time()-t},flush=True)
 if one:print('ONE',one[0]);return
 def v(i,c):return i*k+c+1
 cl=[]
 for i in range(len(S)):
  cl.append([v(i,c)for c in range(k)])
  for c in range(k):
   for d in range(c):cl.append([-v(i,c),-v(i,d)])
 for h in C:
  for c in range(k):cl.append([-v(i,c)for i in h])
 with Solver(name='cadical195',bootstrap_with=cl)as sol:
  ok=sol.solve();print('SAT'if ok else'UNSAT','elapsed',time.time()-t,flush=True)
  if ok:
   M=set(sol.get_model());colors=[next(c for c in range(k)if v(i,c)in M)for i in range(len(S))];json.dump({'n':n,'k':k,'states':S,'colors':colors},open(out,'w'))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('-n',type=int,default=5);p.add_argument('-k',type=int,default=7);p.add_argument('--out',default='experiments/symstate.json');a=p.parse_args();run(a.n,a.k,a.out)
