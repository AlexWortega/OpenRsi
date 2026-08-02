#!/usr/bin/env python3
"""SAT test universal color-reuse operation on two triangle-free colorings.
State of an edge in product: outer color a or (same outer vertex, inner color b).
Allow mappings into common k colors; derive abstract triangle constraints.
"""
import argparse,itertools
from pysat.solvers import Solver
p=argparse.ArgumentParser();p.add_argument('--r',type=int,default=3);p.add_argument('--s',type=int,default=3);p.add_argument('-k',type=int,default=4);a=p.parse_args()
# Variables colors for outer labels O_a and inner I_b. Abstract lex product triangles impose:
# outer triangle patterns may be any nonmonochromatic triple; inner likewise.
# Mixed triangle with two in fiber: pattern O_a,O_a,I_b must not become monochromatic.
states=[('o',i)for i in range(a.r)]+[('i',j)for j in range(a.s)];ix={z:i for i,z in enumerate(states)};C=set()
for t in itertools.product(range(a.r),repeat=3):
 if len(set(t))>1:C.add(tuple(sorted(set(ix['o',x]for x in t))))
for t in itertools.product(range(a.s),repeat=3):
 if len(set(t))>1:C.add(tuple(sorted(set(ix['i',x]for x in t))))
for x in range(a.r):
 for y in range(a.s):C.add(tuple(sorted((ix['o',x],ix['i',y]))))
def v(i,c):return i*a.k+c+1
cl=[]
for i in range(len(states)):
 cl.append([v(i,c)for c in range(a.k)])
 for c in range(a.k):
  for d in range(c):cl.append([-v(i,c),-v(i,d)])
for h in C:
 for c in range(a.k):cl.append([-v(i,c)for i in h])
with Solver(name='cadical195',bootstrap_with=cl)as s:print({'r':a.r,'s':a.s,'k':a.k,'constraints':len(C)},'SAT'if s.solve()else'UNSAT')
