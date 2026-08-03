#!/usr/bin/env python3
"""Explicit exact-fiber cheat for a hugely scaled direct integer CVP encoding."""
from __future__ import annotations
import itertools,math

def all8():
 return [tuple((i+1) if bit==0 else -(i+1) for i,bit in enumerate(u))
         for u in itertools.product((0,1),repeat=3)]

def padded_formula(D):
 C=all8();n=3
 for _ in range(D):
  C.append((n+1,n+2,n+3));n+=3
 return C,n

def literal_true(lit,bits):return bits[abs(lit)-1]==(1 if lit>0 else 0)

def witness(D,M=10**6):
 C,n=padded_formula(D)
 # Core assignment 000 violates exactly clause 000; pad clauses set first variable true.
 bits=[0]*3
 for j in range(D):bits += [1,0,0]
 x=[]
 for b in bits:x += [1-b,b]
 slack=[];viol=0
 for c in C:
  sat=sum(literal_true(l,bits) for l in c)
  if sat==0:
   slack += [0,2];viol+=1 # exact: 0+0+2*2=4
  elif sat==1:slack += [1,1]
  elif sat==2:slack += [0,1]
  else:slack += [1,0]
 # Compute residuals in the proposed lattice coordinates.
 var_res=[M*(x[2*i]+x[2*i+1]-1) for i in range(n)]
 clause_res=[]
 for j,c in enumerate(C):
  sat=sum(x[2*(abs(l)-1)+(1 if l>0 else 0)] for l in c)
  clause_res.append(M*(sat+slack[2*j]+2*slack[2*j+1]-4))
 ident=[z-.5 for z in x+slack]
 sq=sum(r*r for r in var_res+clause_res+ident)
 baseline=(2*n+2*len(C))*.25
 assert max(map(abs,var_res+clause_res))==0 and viol==1
 assert sq==baseline+2
 return {'D':D,'nvars':n,'clauses':len(C),'scale_M':M,'yes_baseline_squared':baseline,
         'cheat_squared':sq,'distance_ratio_upper_bound':math.sqrt(sq/baseline),'violated_clauses':viol}

def run():
 out=[witness(D) for D in (0,1,10,100,1000)]
 print(out);return out
if __name__=='__main__':run()
