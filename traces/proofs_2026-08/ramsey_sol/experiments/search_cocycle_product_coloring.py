#!/usr/bin/env python3
"""Search color reuse in a two-level extension with cocycle cross-edge rules.
Outer K_m and inner K_n seeds; colors of cross edges may depend on both outer endpoints and inner difference class.
Tiny SAT directly colors product vertices with symmetry constraints omitted; asks if mn vertices use max(r,s)+delta colors.
"""
import argparse,itertools,json
from pysat.solvers import Solver
p=argparse.ArgumentParser();p.add_argument('--m',type=int,default=5);p.add_argument('--n',type=int,default=5);p.add_argument('-k',type=int,default=4);p.add_argument('--out');a=p.parse_args();N=a.m*a.n;edges=list(itertools.combinations(range(N),2));ix={e:i for i,e in enumerate(edges)}
def v(e,c):return ix[tuple(sorted(e))]*a.k+c+1
cl=[]
for e in edges:
 cl.append([v(e,c)for c in range(a.k)])
 for c in range(a.k):
  for d in range(c):cl.append([-v(e,c),-v(e,d)])
for x,y,z in itertools.combinations(range(N),3):
 for c in range(a.k):cl.append([-v((x,y),c),-v((x,z),c),-v((y,z),c)])
# enforce translation under simultaneous inner cyclic shift and outer cyclic shift, a structured Z_m x Z_n rule
for e in edges:
 x,y=e;X=(x//a.n,(x%a.n));Y=(y//a.n,y%a.n)
 for shiftout,shiftin in [(0,1),(1,0)]:
  xx=((X[0]+shiftout)%a.m)*a.n+(X[1]+shiftin)%a.n;yy=((Y[0]+shiftout)%a.m)*a.n+(Y[1]+shiftin)%a.n
  if xx!=yy:
   for c in range(a.k):cl += [[-v(e,c),v((xx,yy),c)],[v(e,c),-v((xx,yy),c)]]
with Solver(name='cadical195',bootstrap_with=cl)as s:
 ok=s.solve();print({'N':N,'k':a.k,'vars':len(edges)*a.k},'SAT'if ok else'UNSAT')
 if ok:
  M=set(s.get_model());colors=[next(c for c in range(a.k)if v(e,c)in M)for e in edges];json.dump({'m':a.m,'n':a.n,'k':a.k,'colors':colors},open(a.out or'experiments/cocycle.json','w'))
