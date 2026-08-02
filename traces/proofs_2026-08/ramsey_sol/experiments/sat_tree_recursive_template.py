#!/usr/bin/env python3
"""SAT template: node color depends on remaining-set size, child pair, and simple prefix state.
Tests scalable local relabelings without enumerating n! vertices.
"""
import argparse,itertools,json
from pysat.solvers import Solver
# state at node is remaining set R and child pair a,b; exact tree constraints can be generated
# recursively: any triangle diverges at a node; two edges there use states (R,a,b),(R,a,c),
# third edge is in subtree prefix+a or prefix+b with remaining R\{a}, etc.
# Prefix identity matters only via remaining set for this template.
def build(n):
 states=[]
 for mask in range(1<<n):
  R=[i for i in range(n) if mask>>i&1]
  if len(R)>=2:
   for a,b in itertools.combinations(R,2):states.append((mask,a,b))
 ix={s:i for i,s in enumerate(states)};C=set()
 # Triangle permutations have first symbols pattern all distinct, or two equal.
 # all distinct: three edge states at same node
 for mask in range(1<<n):
  R=[i for i in range(n) if mask>>i&1]
  for a,b,c in itertools.combinations(R,3):C.add(tuple(sorted((ix[mask,a,b],ix[mask,a,c],ix[mask,b,c]))))
 # two share a, third b: two outer states (R,a,b), inner edge may be ANY state deeper
 # in subtree a with remaining R-a. Add constraints against every possible inner state recursively.
 for mask in range(1<<n):
  R=[i for i in range(n) if mask>>i&1]
  for a,b in itertools.combinations(R,2):
   outer=ix[mask,a,b]
   for root in (a,b):
    rem=mask^(1<<root)
    S=[i for i,s in enumerate(states) if s[0]&~rem==0 and s[0].bit_count()<=rem.bit_count() and s[0].bit_count()>=2]
    # reachable deeper remaining sets are subsets of rem
    for z in S:C.add(tuple(sorted((outer,z))))
 return states,sorted(C)
def run(n,k,out):
 S,C=build(n);print({'n':n,'states':len(S),'constraints':len(C)},flush=True)
 def v(i,c):return i*k+c+1
 cl=[]
 for i in range(len(S)):
  cl.append([v(i,c) for c in range(k)])
  for c in range(k):
   for d in range(c):cl.append([-v(i,c),-v(i,d)])
 for h in C:
  for c in range(k):cl.append([-v(i,c) for i in h])
 with Solver(name='cadical195',bootstrap_with=cl) as so:
  ok=so.solve();print('SAT' if ok else'UNSAT',flush=True)
  if ok:
   M=set(so.get_model());col=[next(c for c in range(k) if v(i,c) in M) for i in range(len(S))];json.dump({'n':n,'k':k,'states':S,'colors':col},open(out,'w'))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=6);p.add_argument('--k',type=int,default=10);p.add_argument('--out',default='experiments/tree_template.json');a=p.parse_args();run(a.n,a.k,a.out)
