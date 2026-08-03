#!/usr/bin/env python3
"""Exact NCP experiments for controlled permutation branching-cycle marginals."""
from __future__ import annotations
import argparse,random
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import coo_matrix,hstack

def compose(p,q):return tuple(p[q[i]] for i in range(len(p))) # p after q
def product(seq,q):
 p=tuple(range(q))
 for x in seq:p=compose(x,p)
 return p
def cycles(p):
 seen=set();out=[]
 for i in range(len(p)):
  if i not in seen:
   c=[];j=i
   while j not in seen:seen.add(j);c.append(j);j=p[j]
   out.append(c)
 return out

def random_perm(q,rng):
 a=list(range(q));rng.shuffle(a);return tuple(a)
def build(perms):
 # perms[j][b] maps state j to state j+1 cyclically. One global Boolean variable.
 L=len(perms);q=len(perms[0][0]);meta=[];idx={}
 def col(g,key):idx[g,key]=len(meta);meta.append((g,key));return len(meta)-1
 for b in (0,1):col('x',b)
 for j in range(L):
  for s in range(q):col(('s',j),s)
 for j in range(L):
  for b in (0,1):
   for s in range(q):col(('f',j),(b,s))
 rr=[];cc=[];dd=[];t=[]
 def row(entries,target):
  r=len(t);t.append(target)
  for c in entries:rr.append(r);cc.append(c);dd.append(1)
 # Odd group coverage.
 row([idx['x',b] for b in (0,1)],1)
 for j in range(L):row([idx[('s',j),s] for s in range(q)],1)
 for j in range(L):row([idx[('f',j),(b,s)] for b in (0,1) for s in range(q)],1)
 # Factor-to-global-x marginals.
 for j in range(L):
  for b in (0,1):row([idx['x',b]]+[idx[('f',j),(b,s)] for s in range(q)],0)
 # Incoming and outgoing state marginals.
 for j in range(L):
  for s in range(q):row([idx[('s',j),s]]+[idx[('f',j),(b,s)] for b in (0,1)],0)
  nxt=(j+1)%L
  for u in range(q):
   entries=[idx[('s',nxt),u]]
   entries += [idx[('f',j),(b,s)] for b in (0,1) for s in range(q) if perms[j][b][s]==u]
   row(entries,0)
 H=coo_matrix((dd,(rr,cc)),shape=(len(t),len(meta)),dtype=np.int8)
 return H,np.array(t),meta

def min_weight(H,t,limit=120):
 H=H.tocsr().astype(float);r,p=H.shape;A=hstack([H,-2*coo_matrix(np.eye(r))],format='csr')
 res=milp(np.r_[np.ones(p),np.zeros(r)],integrality=np.ones(p+r),
  bounds=Bounds(np.zeros(p+r),np.r_[np.ones(p),np.asarray(H.sum(axis=1)).ravel()//2+1]),
  constraints=LinearConstraint(A,t,t),options={'time_limit':limit})
 return res

def sample_unsat(q,L,rng):
 while True:
  P=[(random_perm(q,rng),random_perm(q,rng)) for _ in range(L)]
  hol=[product([P[j][b] for j in range(L)],q) for b in (0,1)]
  if all(len(cycles(h))==1 for h in hol):return P,hol

def run(q=3,L=3,trials=20,seed=223):
 rng=random.Random(seed);vals=[];examples=[]
 for _ in range(trials):
  P,hol=sample_unsat(q,L,rng);H,t,meta=build(P);res=min_weight(H,t,60)
  val=None if res.fun is None else round(res.fun);vals.append(val)
  canonical=1+2*L*q
  if val is not None and val<canonical and len(examples)<2:examples.append({'opt':val,'canonical':canonical,'perms':P})
 result={'q':q,'L':L,'trials':trials,'canonical_fixed-branch_weight':1+2*L*q,
  'reported_optima':vals,'histogram':{v:vals.count(v) for v in sorted(set(vals),key=lambda x:(x is None,x))},
  'cheating_examples':examples}
 print(result);return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--q',type=int,default=3);ap.add_argument('--L',type=int,default=3);ap.add_argument('--trials',type=int,default=20);ap.add_argument('--seed',type=int,default=223)
 a=ap.parse_args();run(a.q,a.L,a.trials,a.seed)
