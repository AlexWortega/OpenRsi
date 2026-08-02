#!/usr/bin/env python3
"""Find an equitable legal q=2 GQ-Tanner configuration (finite diagnostic)."""
from itertools import combinations,permutations
from pysat.formula import CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
V=range(6); points=list(combinations(V,2)); pidx={p:i for i,p in enumerate(points)}
def matchings(xs):
 xs=tuple(xs)
 if not xs: yield (); return
 a=xs[0]
 for j in range(1,len(xs)):
  b=xs[j]
  for rest in matchings(xs[1:j]+xs[j+1:]): yield tuple(sorted(((min(a,b),max(a,b)),)+rest))
lines=sorted(set(matchings(tuple(V))))
edges=[(i,15+j) for i,p in enumerate(points) for j,L in enumerate(lines) if p in L]
inc=[[] for _ in range(30)]
for e,(u,v) in enumerate(edges):inc[u].append(e);inc[v].append(e)
def x(e,p):return 1+15*e+p
cnf=CNF();top=675
for e in range(45):
 xs=[x(e,p) for p in range(15)];cnf.append(xs)
 for a,b in combinations(xs,2):cnf.append([-a,-b])
# Tuple selector per check; exactly one, implies three labels. Reverse implication unnecessary.
for es in inc:
 sels=[]
 for L in lines:
  ids=[pidx[p] for p in L]
  for vals in permutations(ids):
   top+=1;sels.append(top)
   for i in range(3):cnf.append([-top,x(es[i],vals[i])])
 cnf.append(sels)
 for a,b in combinations(sels,2):cnf.append([-a,-b])
for p in range(15):
 eq=CardEnc.equals([x(e,p) for e in range(45)],3,top_id=top,encoding=EncType.seqcounter)
 top=eq.nv;cnf.extend(eq.clauses)
# Geometry is flag-transitive; fix the first ordered star to one ordered line.
base=tuple(pidx[p] for p in lines[0])
for i,e in enumerate(inc[0]): cnf.append([x(e,base[i])])
print('instance',top,len(cnf.clauses),flush=True)
with Solver(name='cadical195',bootstrap_with=cnf.clauses) as s:
 ok=s.solve();print('sat',ok,flush=True)
 if ok:
  model={z for z in s.get_model() if z>0}
  labels=[next(p for p in range(15) if x(e,p) in model) for e in range(45)]
  open('experiments/gq_tanner_q2_config.txt','w').write(' '.join(map(str,labels))+'\n')
  raise AssertionError('unexpected equitable configuration')
print('PASS: q=2 equitable GQ-Tanner configuration CSP is UNSAT')
