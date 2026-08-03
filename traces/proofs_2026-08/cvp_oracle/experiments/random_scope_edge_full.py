#!/usr/bin/env python3
"""Exact full-overlap random-scope hierarchy on long 3-color holonomy cycles."""
from __future__ import annotations
import argparse,itertools,random,sys
import numpy as np
from scipy.sparse import coo_matrix
sys.path.insert(0,'experiments')
from search_pseudoviews import gf2_solve

def scope_views(n,E):
 V=tuple(sorted({v for e in E for v in (e,(e+1)%n)}));pos={v:i for i,v in enumerate(V)};A=[]
 for a in itertools.product(range(3),repeat=len(V)):
  if all((a[pos[(e+1)%n]]-a[pos[e]])%3==(1 if e==n-1 else 0) for e in E):A.append(a)
 return V,A
def scopes(n,d,count,rng):
 S={frozenset((e,)) for e in range(n)}
 while len(S)<n+count:S.add(frozenset(rng.sample(range(n),d)))
 return sorted(S,key=lambda x:(len(x),tuple(x)))
def build(n,S):
 info=[];idx={};meta=[]
 for si,E in enumerate(S):
  V,A=scope_views(n,E);info.append((V,A))
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
   for b in itertools.product(range(3),repeat=len(W)):
    row([idx[i,a] for a in Ai if tuple(a[pi[v]] for v in W)==b]+
        [idx[j,a] for a in Aj if tuple(a[pj[v]] for v in W)==b],0)
 return coo_matrix((dd,(rr,cc)),shape=(len(t),len(meta)),dtype=np.int8),np.array(t,dtype=np.int8),info

def run(ns=(8,12,16,20,24,30),d=3,mult=2,trials=5,seed=293):
 rng=random.Random(seed);out=[]
 for n in ns:
  vals=[];sizes=[]
  for _ in range(trials):
   S=scopes(n,d,mult*n,rng);H,t,info=build(n,S);x=gf2_solve(H,t)
   vals.append(x is not None);sizes.append((H.shape,len(S),max(len(A) for V,A in info)))
  out.append({'n':n,'d':d,'count':mult*n,'trials':trials,'feasible':sum(vals),'infeasible':trials-sum(vals),
   'max_rows':max(x[0][0] for x in sizes),'max_cols':max(x[0][1] for x in sizes),'groups':max(x[1] for x in sizes),'max_views':max(x[2] for x in sizes)})
 print(out);return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--d',type=int,default=3);ap.add_argument('--mult',type=int,default=2);ap.add_argument('--trials',type=int,default=5);a=ap.parse_args();run(d=a.d,mult=a.mult,trials=a.trials)
