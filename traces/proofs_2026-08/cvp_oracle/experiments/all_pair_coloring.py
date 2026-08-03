#!/usr/bin/env python3
"""All-pairs full-overlap GF(2) hierarchy for graph q-coloring CSP."""
from __future__ import annotations
import argparse,itertools,sys
import numpy as np
from scipy.sparse import coo_matrix
sys.path.insert(0,'experiments')
from search_pseudoviews import gf2_solve

def graphs(name,n=None):
 if name=='K4':return 4,list(itertools.combinations(range(4),2))
 if name=='K5':return 5,list(itertools.combinations(range(5),2))
 if name=='wheel':
  n=n or 5 # odd rim + hub, not 3-colorable
  return n+1,[(i,(i+1)%n) for i in range(n)]+[(i,n) for i in range(n)]
 raise ValueError(name)
def scope_views(edges,Q,q):
 V=tuple(sorted({v for j in Q for v in edges[j]}));pos={v:i for i,v in enumerate(V)};A=[]
 for a in itertools.product(range(q),repeat=len(V)):
  if all(a[pos[edges[j][0]]]!=a[pos[edges[j][1]]] for j in Q):A.append(a)
 return V,A
def build(edges,q):
 m=len(edges);S=[frozenset((j,)) for j in range(m)]+[frozenset(p) for p in itertools.combinations(range(m),2)]
 info=[];idx={};meta=[]
 for si,Q in enumerate(S):
  V,A=scope_views(edges,Q,q);info.append((V,A))
  for a in A:idx[si,a]=len(meta);meta.append((si,a))
 rr=[];cc=[];dd=[];t=[]
 def row(es,b):
  r=len(t);t.append(b)
  for c in es:rr.append(r);cc.append(c);dd.append(1)
 for si,(V,A) in enumerate(info):row([idx[si,a] for a in A],1)
 for i in range(len(S)):
  Vi,Ai=info[i];pi={v:k for k,v in enumerate(Vi)}
  for j in range(i):
   Vj,Aj=info[j];pj={v:k for k,v in enumerate(Vj)};W=tuple(sorted(set(Vi)&set(Vj)))
   if not W:continue
   for b in itertools.product(range(q),repeat=len(W)):
    row([idx[i,a] for a in Ai if tuple(a[pi[v]] for v in W)==b]+
        [idx[j,a] for a in Aj if tuple(a[pj[v]] for v in W)==b],0)
 return coo_matrix((dd,(rr,cc)),shape=(len(t),len(meta)),dtype=np.int8),np.array(t),S,info

def run(cases=(('K4',None,3),('K5',None,4),('wheel',5,3),('wheel',7,3))):
 out=[]
 for name,n,q in cases:
  nv,E=graphs(name,n);H,t,S,info=build(E,q);x=gf2_solve(H,t)
  out.append({'graph':name,'nparam':n,'vertices':nv,'edges':len(E),'colors':q,
   'groups':len(S),'shape':H.shape,'exact_feasible':x is not None,
   'one_solution_weight':None if x is None else x.bit_count(),'max_views':max(len(A) for V,A in info)})
 print(out);return out
if __name__=='__main__':run()
