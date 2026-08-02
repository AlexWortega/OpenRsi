#!/usr/bin/env python3
"""Partition the layer of permutations moving the last point into symmetric product-free sets."""
import itertools,argparse,json,time
from pysat.solvers import Solver

def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 z=[0]*len(p)
 for i,x in enumerate(p):z[x]=i
 return tuple(z)
def run(n,k,out):
 t=time.time();P=[p for p in itertools.permutations(range(n)) if p[-1]!=n-1];idx={p:i for i,p in enumerate(P)};oid={};O=[]
 for p in P:
  if p not in oid:
   o=sorted(set((p,inv(p))));i=len(O);O.append(o)
   for x in o:oid[x]=i
 C=set();one=[]
 for x in P:
  for y in P:
   z=comp(x,y)
   if z in idx:
    h=tuple(sorted(set((oid[x],oid[y],oid[z]))));C.add(h)
    if len(h)==1:one.append((x,y,z))
 print({'n':n,'layer':len(P),'orbits':len(O),'constraints':len(C),'one':len(one),'build':time.time()-t},flush=True)
 if one:return
 def v(i,c):return i*k+c+1
 cl=[]
 for i in range(len(O)):
  cl.append([v(i,c) for c in range(k)])
  for c in range(k):
   for d in range(c):cl.append([-v(i,c),-v(i,d)])
 for h in C:
  for c in range(k):cl.append([-v(i,c) for i in h])
 cl.append([v(0,0)])
 with Solver(name='cadical195',bootstrap_with=cl) as s:
  ok=s.solve();print('SAT' if ok else'UNSAT','elapsed',time.time()-t,flush=True)
  if ok:
   M=set(s.get_model());colors=[next(c for c in range(k) if v(i,c) in M) for i in range(len(O))];json.dump({'n':n,'k':k,'orbits':[[list(x) for x in o] for o in O],'colors':colors},open(out,'w'))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=5);p.add_argument('--k',type=int,default=3);p.add_argument('--out',default='experiments/sn_layer.json');a=p.parse_args();run(a.n,a.k,a.out)
