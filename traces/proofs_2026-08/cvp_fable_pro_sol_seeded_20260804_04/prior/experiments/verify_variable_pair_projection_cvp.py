#!/usr/bin/env python3
"""Polynomial-size mutation: make pair-projection targets lattice variables.

Variables are integer triple coefficients z and their three pair projections
p=Pi(z).  Constraints enforce p-Pi(z)=0 and every row/column sum of p is one
(redundant but explicit).  The CVP identity block charges ||z||^2+||p||^2.
No permutation target is chosen by the reduction: a YES matching determines
it existentially.  Exact signed search attacks tiny YES/NO instances.
"""
from __future__ import annotations
import itertools
import verify_feature_shell_3dm as f
import verify_integer_3dm_cvp as ic


def projection(q,T,z):
    out=[]
    for kind in range(3):
      for a in range(q):
       for b in range(q):
        out.append(sum(z[j] for j,u in enumerate(T)
          if ((u[0],u[1]),(u[0],u[2]),(u[1],u[2]))[kind]==(a,b)))
    return tuple(out)

def norm_aug(q,T,z,weights=(1,1,1,1)):
    p=projection(q,T,z); q2=q*q
    return weights[0]*sum(a*a for a in z)+sum(weights[k+1]*sum(a*a for a in p[k*q2:(k+1)*q2]) for k in range(3))
def incidence_ok(q,T,z):
    return all(sum(z[j] for j,u in enumerate(T) if u[k]==a)==1
               for k in range(3) for a in range(q))
def exact(q,T,C=2,weights=(1,1,1,1)):
    best=None;arg=None
    for z in itertools.product(range(-C,C+1),repeat=len(T)):
      if incidence_ok(q,T,z):
       v=norm_aug(q,T,z,weights)
       if best is None or v<best:best,arg=v,z
    return best,arg

def explicit_basis_residual(q,T,z,M=1000):
    """Check B=[I;M E], target [0;Mb] for variables (z,p)."""
    m=len(T); q2=q*q; p=projection(q,T,z); coeff=tuple(z)+p;n=len(coeff)
    rows=[];target=[]
    # Incidence rows Az=1.
    for k in range(3):
      for a in range(q):
       rows.append(tuple(int(j<m and T[j][k]==a) for j in range(n)));target.append(1)
    # p - pair projection(z)=0.
    for kind in range(3):
      for a in range(q):
       for b in range(q):
        pi=(kind*q2+a*q+b); row=[]
        for j in range(n):
         if j<m:
          pair=((T[j][0],T[j][1]),(T[j][0],T[j][2]),(T[j][1],T[j][2]))[kind]
          row.append(-int(pair==(a,b)))
         else:row.append(int(j==m+pi))
        rows.append(tuple(row));target.append(0)
    assert all(sum(row[j]*coeff[j] for j in range(n))==b for row,b in zip(rows,target))
    top=sum(a*a for a in coeff)
    residual=sum((M*(sum(row[j]*coeff[j] for j in range(n))-b))**2 for row,b in zip(rows,target))
    assert residual==0
    # Identity block makes columns linearly independent: rank n, determinant
    # of Gram not needed for an explicit rank-n integer lattice basis.
    return n,len(rows),top

def main():
    q,m=3,8;Y,N=f.families(q,m,40)
    for weights in [(1,1,1,1),(2,1,1,1),(4,1,1,1),(8,1,1,1),
                    (1,2,2,2),(1,4,4,4)]:
      yd=[];nd=[];args=[]
      for label,fam,out in [('Y',Y,yd),('N',N,nd)]:
       for T,M,F in fam:
        v,z=exact(q,T,2,weights);out.append(v);args.append((label,T,v,z))
      ratio=min(nd)/max(yd)
      print({'weights':weights,'YES':{v:yd.count(v) for v in sorted(set(yd))},
             'NO':{v:nd.count(v) for v in sorted(set(nd))},
             'worstYES':max(yd),'bestNO':min(nd),'ratio':ratio})
      assert max(yd)==q*sum(weights)
      # General integrality proof predicts at least baseline+2*min(weight).
      assert min(nd)>=q*sum(weights)+2*min(weights)
      if weights==(1,1,1,1):
       light=next(a for a in args if a[0]=='N' and a[2]==min(nd))
       dims=explicit_basis_residual(q,light[1],light[3])
       print({'lightest_NO':light,'basis_rank_rows_norm':dims})
    print('variable pair-projection CVP passes exact signed search')

if __name__=='__main__':main()
