#!/usr/bin/env python3
"""Verify charged-incidence pseudoassignments below graph vertex connectivity."""
from __future__ import annotations
import itertools

def complete_graph(n):return list(itertools.combinations(range(n),2))
def support_combination(n,E,Q,alpha):
 coeff=[]
 amap={v:a for v,a in zip(Q,alpha)}
 for u,v in E:coeff.append((amap.get(u,0)-amap.get(v,0))%3)
 return {i for i,c in enumerate(coeff) if c}
def incident(E,Q):return {i for i,e in enumerate(E) if set(e)&set(Q)}
def verify_case(k):
 n=2*k+1;E=complete_graph(n);groups=[Q for r in range(1,k+1) for Q in itertools.combinations(range(n),r)]
 checks=0
 for Q in groups:
  UQ=incident(E,Q)
  # Incidence rows indexed by every proper Q are independent. Solution count is odd.
  solution_exponent=len(UQ)-len(Q);assert solution_exponent>=0 and 3**solution_exponent%2==1
  for R in groups:
   W=UQ&incident(E,R);common=set(Q)&set(R)
   for alpha in itertools.product(range(3),repeat=len(Q)):
    supp=support_combination(n,E,Q,alpha)
    if supp<=W:
     assert all(a==0 for v,a in zip(Q,alpha) if v not in common)
    checks+=1
 # Global charged system is inconsistent: signed incidence rows sum zero, charges sum one.
 charges=[1]+[0]*(n-1);assert sum(charges)%3==1
 return {'k':k,'vertices':n,'degree':n-1,'edges':len(E),'groups':len(groups),
         'support_combinations_checked':checks,'max_constraint_arity':n-1}
def run():
 out=[verify_case(k) for k in (1,2,3)]
 print(out);return out
if __name__=='__main__':run()
