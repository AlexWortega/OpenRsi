#!/usr/bin/env python3
"""SAT quotient of least-moved-point pair classes in S_n.
States are pairs i<j. A state triple is constrained if represented by x,y,xy.
"""
import argparse,itertools,json
from pysat.solvers import Solver

def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def lab(p):
 i=next(i for i in range(len(p)) if p[i]!=i);return (i,p[i])
def main(n,k,out):
 P=list(itertools.permutations(range(n)));e=tuple(range(n));states=list(itertools.combinations(range(n),2));ix={x:i for i,x in enumerate(states)};bucket={s:[] for s in states}
 for p in P:
  if p!=e:bucket[lab(p)].append(p)
 C=set();one=[]
 for a,A in bucket.items():
  for b,B in bucket.items():
   for x in A:
    for y in B:
     z=comp(x,y)
     if z!=e:
      h=tuple(sorted(set((ix[a],ix[b],ix[lab(z)]))));C.add(h)
      if len(h)==1:one.append((x,y,z,a))
 print({'n':n,'states':len(states),'constraints':len(C),'one':len(one)},flush=True)
 if one:print('ONE',one[0]);return
 def v(i,c):return i*k+c+1
 clauses=[]
 for i in range(len(states)):
  clauses.append([v(i,c) for c in range(k)])
  for c in range(k):
   for d in range(c):clauses.append([-v(i,c),-v(i,d)])
 for h in C:
  for c in range(k):clauses.append([-v(i,c) for i in h])
 clauses.append([v(0,0)])
 with Solver(name='cadical195',bootstrap_with=clauses) as s:
  ok=s.solve();print('SAT' if ok else 'UNSAT',flush=True)
  if ok:
   M=set(s.get_model());colors=[next(c for c in range(k) if v(i,c) in M) for i in range(len(states))];json.dump({'n':n,'k':k,'states':states,'colors':colors},open(out,'w'))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=5);p.add_argument('--k',type=int,default=5);p.add_argument('--out',default='experiments/sn_compress.json');a=p.parse_args();main(a.n,a.k,a.out)
