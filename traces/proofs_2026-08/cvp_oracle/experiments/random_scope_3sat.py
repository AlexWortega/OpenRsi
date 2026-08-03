#!/usr/bin/env python3
"""Random nonlocal clause-scope NCP hierarchy for arbitrary small CNFs.

Each scope is a set of clauses. Columns are satisfying assignments to its variable
union. Every group has odd coverage. Every pair of scopes has equal GF(2)
marginals on all shared variables. This is a concrete globally overlapping
candidate; exact elimination attacks its zero-residual fiber.
"""
from __future__ import annotations
import argparse,itertools,random,sys
import numpy as np
from scipy.sparse import coo_matrix
sys.path.insert(0,'experiments')
from connected_views import satisfies,all_eight_clauses,inconsistent_xor_cycle,k4_tseitin
from search_pseudoviews import gf2_solve

def views(clauses,Q):
 V=tuple(sorted({abs(l) for j in Q for l in clauses[j]}));A=[]
 for bits in itertools.product((0,1),repeat=len(V)):
  val=dict(zip(V,bits))
  if all(satisfies(clauses[j],val) for j in Q):A.append(bits)
 return V,A

def scopes_random(m,d,count,rng):
 S={frozenset((j,)) for j in range(m)}
 while len(S)<m+count:S.add(frozenset(rng.sample(range(m),min(d,m))))
 return sorted(S,key=lambda x:(len(x),tuple(x)))
def build(clauses,scopes):
 info=[];idx={};meta=[]
 for si,Q in enumerate(scopes):
  V,A=views(clauses,Q);info.append((V,A))
  for a in A:idx[si,a]=len(meta);meta.append((si,a))
 rr=[];cc=[];dd=[];t=[]
 def row(entries,target):
  r=len(t);t.append(target)
  for c in entries:rr.append(r);cc.append(c);dd.append(1)
 for si,(V,A) in enumerate(info):row([idx[si,a] for a in A],1)
 # Pairwise full overlap marginals (not merely shared-clause marginals).
 for i in range(len(scopes)):
  Vi,Ai=info[i];pi={v:k for k,v in enumerate(Vi)}
  for j in range(i):
   Vj,Aj=info[j];pj={v:k for k,v in enumerate(Vj)};W=tuple(sorted(set(Vi)&set(Vj)))
   if not W:continue
   for b in itertools.product((0,1),repeat=len(W)):
    ei=[idx[i,a] for a in Ai if tuple(a[pi[v]] for v in W)==b]
    ej=[idx[j,a] for a in Aj if tuple(a[pj[v]] for v in W)==b]
    row(ei+ej,0)
 H=coo_matrix((dd,(rr,cc)),shape=(len(t),len(meta)),dtype=np.int8)
 return H,np.array(t,dtype=np.int8),info

def is_sat(clauses):
 n=max(abs(l) for c in clauses for l in c)
 return any(all(satisfies(c,dict(enumerate(bits,1))) for c in clauses)
            for bits in itertools.product((0,1),repeat=n))
def run(family='all8',d=3,count=8,trials=20,seed=271):
 if family=='all8':C=all_eight_clauses()
 elif family=='xor5':C=inconsistent_xor_cycle(5)
 elif family=='k4':C=k4_tseitin()
 else:raise ValueError(family)
 assert not is_sat(C);rng=random.Random(seed);rows=[]
 for _ in range(trials):
  S=scopes_random(len(C),d,count,rng);H,t,info=build(C,S);sol=gf2_solve(H,t)
  rows.append((sol is not None,len(S),H.shape,max(len(A) for V,A in info)))
 result={'family':family,'clauses':len(C),'d':d,'count':count,'trials':trials,
  'exact_feasible':sum(x[0] for x in rows),'exact_infeasible':sum(not x[0] for x in rows),
  'max_groups':max(x[1] for x in rows),'max_rows':max(x[2][0] for x in rows),
  'max_columns':max(x[2][1] for x in rows),'max_group_views':max(x[3] for x in rows)}
 print(result);return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--family',choices=['all8','xor5','k4'],default='all8');ap.add_argument('--d',type=int,default=3);ap.add_argument('--count',type=int,default=8);ap.add_argument('--trials',type=int,default=20);ap.add_argument('--seed',type=int,default=271)
 a=ap.parse_args();run(a.family,a.d,a.count,a.trials,a.seed)
