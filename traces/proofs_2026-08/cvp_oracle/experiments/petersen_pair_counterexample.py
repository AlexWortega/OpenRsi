#!/usr/bin/env python3
"""Explicit Petersen GF(3) counterexample to all-pairs GF(2) hierarchy exactness."""
from __future__ import annotations
import itertools,sys
import numpy as np
from scipy.sparse import coo_matrix
sys.path.insert(0,'experiments')
from search_pseudoviews import gf2_solve
E=[(0,1),(1,2),(2,3),(3,4),(0,4),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(6,9),(6,8),(5,8)]
inc={v:[] for v in range(10)}
for ei,(u,v) in enumerate(E):inc[u].append((ei,1));inc[v].append((ei,-1))
b=[1]+[0]*9

def group_views(Q):
 U=tuple(sorted({ei for v in Q for ei,s in inc[v]}));pos={e:i for i,e in enumerate(U)};A=[]
 for a in itertools.product(range(3),repeat=len(U)):
  if all(sum(s*a[pos[e]] for e,s in inc[v])%3==b[v] for v in Q):A.append(a)
 return U,A

def build():
 S=[(v,) for v in range(10)]+list(itertools.combinations(range(10),2));info=[];idx={};meta=[]
 for si,Q in enumerate(S):
  U,A=group_views(Q);info.append((U,A))
  for a in A:idx[si,a]=len(meta);meta.append((si,a))
 rr=[];cc=[];dd=[];t=[]
 def row(es,z):
  r=len(t);t.append(z)
  for c in es:rr.append(r);cc.append(c);dd.append(1)
 for si,(U,A) in enumerate(info):row([idx[si,a] for a in A],1)
 for i in range(len(S)):
  Ui,Ai=info[i];pi={e:k for k,e in enumerate(Ui)}
  for j in range(i):
   Uj,Aj=info[j];pj={e:k for k,e in enumerate(Uj)};W=tuple(sorted(set(Ui)&set(Uj)))
   if not W:continue
   for z in itertools.product(range(3),repeat=len(W)):
    row([idx[i,a] for a in Ai if tuple(a[pi[e]] for e in W)==z]+
        [idx[j,a] for a in Aj if tuple(a[pj[e]] for e in W)==z],0)
 H=coo_matrix((dd,(rr,cc)),shape=(len(t),len(meta)),dtype=np.int8)
 return H,np.array(t,dtype=np.int8),S,info,meta

def run():
 H,t,S,info,meta=build();x=np.ones(len(meta),dtype=int)
 assert np.array_equal(H.dot(x)%2,t)
 counts=[len(A) for U,A in info];assert counts.count(9)==10 and counts.count(27)==15 and counts.count(81)==30
 assert sum(counts)==2925
 # Exact UNSAT certificate: sum all ten vertex RHS =1 while incidence LHS cancels.
 assert sum(b)%3==1
 coeff=[0]*len(E)
 for v in range(10):
  for e,s in inc[v]:coeff[e]+=s
 assert all(c==0 for c in coeff)
 # Confirm generic elimination also finds a fiber.
 sol=gf2_solve(H,t);assert sol is not None
 result={'vertices':10,'edges':15,'groups':55,'shape':H.shape,'all_ones_weight':len(meta),
  'group_count_histogram':{9:10,27:15,81:30},'elimination_solution_weight':sol.bit_count(),
  'unsat_rhs_sum_mod3':sum(b)%3}
 print(result);return result
if __name__=='__main__':run()
