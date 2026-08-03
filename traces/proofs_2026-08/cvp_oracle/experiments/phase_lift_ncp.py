#!/usr/bin/env python3
"""End-to-end phase-lifted one-hot NCP candidate and completeness attack."""
from __future__ import annotations
import argparse,itertools,random,sys
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import coo_matrix,hstack
sys.path.insert(0,'experiments')
from connected_views import satisfies,all_eight_clauses


def clause_views(clause):
 scope=tuple(abs(x) for x in clause)
 out=[]
 for a in itertools.product((0,1),repeat=3):
  if satisfies(clause,dict(zip(scope,a))):out.append(a)
 return out

def random_alpha(clauses,q,rng):
 return [{a:tuple(rng.randrange(q) for _ in range(3)) for a in clause_views(c)} for c in clauses]

def build(clauses,n,q,alpha):
 rows=[];cols=[];data=[];target=[];meta=[]
 def add(r,c):rows.append(r);cols.append(c);data.append(1)
 # Preallocate row IDs.
 V=[]
 for i in range(n):V.append(len(target));target.append(1)
 Q=[]
 for j in range(len(clauses)):Q.append(len(target));target.append(1)
 R={}
 for j,c in enumerate(clauses):
  for r in range(3):
   for b in (0,1):
    for p in range(q):R[j,r,b,p]=len(target);target.append(0)
 # Variable columns X(i,b,y), phase y copied to every occurrence.
 for i in range(1,n+1):
  occ=[(j,r) for j,c in enumerate(clauses) for r,lit in enumerate(c) if abs(lit)==i]
  for b in (0,1):
   for y in range(q):
    ci=len(meta);meta.append(('X',i,b,y));add(V[i-1],ci)
    for j,r in occ:add(R[j,r,b,y],ci)
 # Legal clause-view columns Y(j,a,z).
 for j,c in enumerate(clauses):
  for a in clause_views(c):
   for z in range(q):
    ci=len(meta);meta.append(('Y',j,a,z));add(Q[j],ci)
    for r,b in enumerate(a):add(R[j,r,b,(z+alpha[j][a][r])%q],ci)
 H=coo_matrix((data,(rows,cols)),shape=(len(target),len(meta)),dtype=np.int8)
 return H,np.array(target,dtype=np.int8),meta

def min_weight(H,t,limit=60):
 H=H.tocsr().astype(float);r,p=H.shape
 A=hstack([H,-2*coo_matrix(np.eye(r))],format='csr')
 c=np.r_[np.ones(p),np.zeros(r)];mx=np.asarray(H.sum(axis=1)).ravel()//2+1
 res=milp(c,integrality=np.ones(p+r),bounds=Bounds(np.zeros(p+r),np.r_[np.ones(p),mx]),
          constraints=LinearConstraint(A,t,t),options={'time_limit':limit})
 return res

def sat_assignments(clauses,n):
 return [bits for bits in itertools.product((0,1),repeat=n)
         if all(satisfies(c,dict(enumerate(bits,1))) for c in clauses)]
def assignment_lifts(bits,clauses,q,alpha):
 # Brute force variable phases y; each clause requires three y-alpha values equal.
 for ys in itertools.product(range(q),repeat=len(bits)):
  ok=True
  for j,c in enumerate(clauses):
   a=tuple(bits[abs(l)-1] for l in c)
   vals=[(ys[abs(c[r])-1]-alpha[j][a][r])%q for r in range(3)]
   if len(set(vals))!=1:ok=False;break
  if ok:return ys
 return None

def sat_pair(): return [(1,2,3),(1,-2,3)]
def run(q=2,trials=30,seed=71):
 rng=random.Random(seed); complete=0;examples=[]
 C=sat_pair(); sats=sat_assignments(C,3)
 for _ in range(trials):
  a=random_alpha(C,q,rng)
  lifts=[b for b in sats if assignment_lifts(b,C,q,a) is not None]
  complete += bool(lifts)
  if not lifts and len(examples)<1:examples.append(a)
 # UNSAT all8 NCP optima.
 U=all_eight_clauses();opts=[]
 for _ in range(min(trials,10)):
  a=random_alpha(U,q,rng);H,t,_=build(U,3,q,a);res=min_weight(H,t,30)
  opts.append(None if res.fun is None else round(res.fun))
 result={'q':q,'trials':trials,'sat_formula_boolean_assignments':len(sats),
         'random_lifts_preserving_some_assignment':complete,'completeness_failures':trials-complete,
         'unsat_all8_K':11,'unsat_reported_optima':opts,'example_completeness_failure':examples}
 print(result);return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--q',type=int,default=2);ap.add_argument('--trials',type=int,default=30);ap.add_argument('--seed',type=int,default=71)
 a=ap.parse_args();run(a.q,a.trials,a.seed)
