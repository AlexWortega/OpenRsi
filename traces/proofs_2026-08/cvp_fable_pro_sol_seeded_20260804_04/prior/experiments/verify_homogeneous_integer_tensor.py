#!/usr/bin/env python3
"""Exact mixed-word test for homogenized integer 3DM lattices.

L(T)={(z,s) in Z^m x Z : A z = s*1}.  Primitive vectors with s=1 are
exact-cover witnesses; tensor products are homogeneous lattices.  We enumerate
small coefficient boxes, build Kronecker generators for L(T)⊗L(T), and perform
exact bounded mixed-coefficient search.  This probes the Haviv--Regev-style
all-mixed tensor issue before any claim of multiplicative integer soundness.
"""
from __future__ import annotations
import itertools
import verify_feature_shell_3dm as f
import verify_integer_3dm_cvp as ic


def rref_null_integer(q,T):
    """Simple spanning generators: kernel relations from exact bounded set plus one pointed vector."""
    # Enumerate [-2,2] homogeneous solutions; greedily take Q-linearly
    # independent vectors via Fraction elimination.  Tiny exact experiment.
    sols=[]
    for z in itertools.product(range(-2,3),repeat=len(T)):
      for s in range(-2,3):
       if all(sum(z[j] for j,u in enumerate(T) if u[k]==a)==s for k in range(3) for a in range(q)):
        if any(z) or s:sols.append(tuple(z)+(s,))
    sols.sort(key=lambda v:(sum(a*a for a in v),v))
    from fractions import Fraction
    basis=[];piv=[]
    for v in sols:
      x=[Fraction(a) for a in v]
      for p,b in zip(piv,basis):
       if x[p]:
        c=x[p];x=[x[i]-c*b[i] for i in range(len(x))]
      if any(x):
       p=next(i for i,a in enumerate(x) if a);c=x[p];x=[a/c for a in x]
       # eliminate new pivot from old rows
       for h,b in enumerate(basis):
        if b[p]:
         c=b[p];basis[h]=[b[i]-c*x[i] for i in range(len(x))]
       # preserve sorted pivots
       at=sum(pp<p for pp in piv);piv.insert(at,p);basis.insert(at,x)
    # Return original short integer vectors independently spanning same rank.
    out=[];rank=0
    for v in sols:
      cand=out+[v]
      # rational rank quick
      B=[];P=[]
      for w in cand:
       x=[Fraction(a) for a in w]
       for p,b in zip(P,B):
        if x[p]:c=x[p];x=[x[i]-c*b[i] for i in range(len(x))]
       if any(x):
        p=next(i for i,a in enumerate(x) if a);c=x[p];x=[a/c for a in x];P.append(p);B.append(x)
      if len(B)>rank:out.append(v);rank+=1
      if rank==len(basis):break
    assert rank==len(basis)
    return out

def pointed_min(vectors,C=2):
    best=None;arg=None
    for coef in itertools.product(range(-C,C+1),repeat=len(vectors)):
      x=tuple(sum(coef[i]*vectors[i][j] for i in range(len(vectors))) for j in range(len(vectors[0])))
      if x[-1]==1:
       w=sum(a*a for a in x)
       if best is None or w<best:best,arg=w,(coef,x)
    return best,arg

def tensor_generators(B):
    n=len(B[0]);out=[]
    for u in B:
     for v in B:out.append(tuple(u[i]*v[j] for i in range(n) for j in range(n)))
    return out

def bounded_tensor_min(B,C=1):
    G=tensor_generators(B);n=len(B[0]);best=None;arg=None
    # Dimension is tiny (typically 4 generators after tensor for m=8 sparse T).
    assert len(G)<=16
    for coef in itertools.product(range(-C,C+1),repeat=len(G)):
      x=tuple(sum(coef[i]*G[i][j] for i in range(len(G))) for j in range(n*n))
      if x[-1]==1:
       w=sum(a*a for a in x)
       if best is None or w<best:best,arg=w,(coef,x)
    return best,arg,len(G)

def main():
 q,m=3,8;Y,N=f.families(q,m,4)
 rec=[]
 for label,fam in [('Y',Y),('N',N)]:
  for idx,(T,M,F) in enumerate(fam):
   B=rref_null_integer(q,T)
   d,a=pointed_min(B,2);dt,at,g=bounded_tensor_min(B,1)
   rec.append((label,idx,len(B),d,dt,g,dt/(d*d),T,a,at))
 for x in rec:print(x[:8])
 yd=[x for x in rec if x[0]=='Y'];nd=[x for x in rec if x[0]=='N']
 assert all(x[3]==4 for x in yd) # includes homogenizing coordinate s^2
 assert all(x[3]>=6 for x in nd)
 # Bounded exact mixed search result: record whether pure-square distance holds.
 pure=all(x[4]==x[3]*x[3] for x in rec)
 print({'all_bounded_tensor_minima_multiplicative':pure,
        'YES_tensor':[x[4] for x in yd],'NO_tensor':[x[4] for x in nd]})
 assert all(x[4] is not None for x in rec)
 print('homogeneous integer tensor bounded mixed search passes')

if __name__=='__main__':main()
