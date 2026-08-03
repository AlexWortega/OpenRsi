#!/usr/bin/env python3
"""Exact scout-followup: determinant/permutation global dictionary at q=3,4.

A coefficient lambda_sigma selects determinant monomials (permutations).
Coverage sum lambda=1.  Its aggregate table is X=sum lambda P_sigma.
We charge lambda and optional exterior/compound representation states
S_k=sum lambda wedge^k(P_sigma).  Legal singleton witnesses are global and
avoid local tableaus.  Exhaustive signed search finds the cheapest non-singleton
virtual permutation and measures whether compound states give a multiplicative
penalty.  This is a finite construction diagnostic; q! columns are not a
polynomial reduction.
"""
from __future__ import annotations
import itertools


def perms(q):return list(itertools.permutations(range(q)))
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))&1
def table(p):
 q=len(p);return tuple(int(p[i]==j) for i in range(q) for j in range(q))
def det01(mat):
 n=len(mat)
 if n==0:return 1
 # determinant over integers for 0/1 permutation minors.
 return sum(((-1)**parity(p))*__import__('math').prod(mat[i][p[i]] for i in range(n))
            for p in perms(n))
def compound(p,k):
 q=len(p); subs=list(itertools.combinations(range(q),k));out=[]
 P=table(p)
 for I in subs:
  for J in subs:
   out.append(det01([[P[i*q+j] for j in J] for i in I]))
 return tuple(out)
def add(vs,coef):return tuple(sum(coef[i]*vs[i][j] for i in range(len(coef))) for j in range(len(vs[0])))
def sq(v):return sum(a*a for a in v)

def run(q,C=1):
 ps=perms(q);tabs=[table(p) for p in ps]
 comps={k:[compound(p,k) for p in ps] for k in range(1,q+1)}
 legal={tuple(1 if i==j else 0 for i in range(len(ps))) for j in range(len(ps))}
 best={};arg={}; counts=0
 for lam in itertools.product(range(-C,C+1),repeat=len(ps)):
  if sum(lam)!=1 or lam in legal:continue
  counts+=1;X=add(tabs,lam)
  # Every affine combination has row/column sums one.  Non-singleton includes
  # repeated legal tables only if lambda is not singleton; record all.
  base=sum(a*a for a in lam)
  states={k:add(comps[k],lam) for k in comps}
  costs={
   'lambda':base,
   'lambda+table':base+sq(X),
   'lambda+all_compounds':base+sum(sq(states[k]) for k in states),
   'lambda+top_det':base+sq(states[q]),
   'lambda+middle_compounds':base+sum(sq(states[k]) for k in range(2,q)),
  }
  for name,c in costs.items():
   if name not in best or c<best[name]:best[name]=c;arg[name]=(lam,X,{k:states[k] for k in states})
 # Uniform legal baseline for every singleton.
 legalcost={
  'lambda':1,
  'lambda+table':1+q,
  'lambda+all_compounds':1+sum(len(next(v for v in comps[k])) and sq(comps[k][0]) for k in comps),
  'lambda+top_det':2,
  'lambda+middle_compounds':1+sum(sq(comps[k][0]) for k in range(2,q)),
 }
 report={n:(legalcost[n],best[n],best[n]/legalcost[n]) for n in best}
 print({'q':q,'signed_affine_vectors':counts,'report':report})
 for n in best:
  print(n,{'lambda':arg[n][0],'X':arg[n][1],'legal':legalcost[n],'illegal':best[n]})
 assert best['lambda']==3
 assert best['lambda+table']==legalcost['lambda+table']+4 # q+1 vs q+5
 # Top determinant/sign is only one charged coordinate and cannot exclude a
 # three-monomial affine virtual state by more than a constant.
 assert best['lambda+top_det']<=legalcost['lambda+top_det']+4
 return report

def main():
 r3=run(3,2)
 # q=4 has 24 columns, so exhaustive lambda is infeasible.  Attack all
 # support-three affine combinations e_a+e_b-e_c, the universal first threat.
 q=4;ps=perms(q);tabs=[table(p) for p in ps];comps={k:[compound(p,k) for p in ps] for k in range(1,q+1)}
 best={};arg={}
 for a,b,c in itertools.permutations(range(len(ps)),3):
  lam=[0]*len(ps);lam[a]+=1;lam[b]+=1;lam[c]-=1
  X=add(tabs,lam);states={k:add(comps[k],lam) for k in comps};base=3
  costs={'lambda':3,'lambda+table':3+sq(X),
   'lambda+all_compounds':3+sum(sq(states[k]) for k in states),
   'lambda+top_det':3+sq(states[q]),
   'lambda+middle_compounds':3+sum(sq(states[k]) for k in range(2,q))}
  for n,v in costs.items():
   if n not in best or v<best[n]:best[n]=v;arg[n]=(a,b,c,X)
 legal={'lambda':1,'lambda+table':5,'lambda+all_compounds':1+sum(sq(comps[k][0]) for k in comps),
        'lambda+top_det':2,'lambda+middle_compounds':1+sum(sq(comps[k][0]) for k in range(2,q))}
 print({'q':4,'support3_checked':24*23*22,'report':{n:(legal[n],best[n],best[n]/legal[n]) for n in best},'arg':arg})
 assert best['lambda']==3 and best['lambda+top_det']<=6
 print('determinant/permutation dictionary exact attack passes')

if __name__=='__main__':main()
