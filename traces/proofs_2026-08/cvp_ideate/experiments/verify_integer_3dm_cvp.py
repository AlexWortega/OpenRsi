#!/usr/bin/env python3
"""Exact construction/attack: direct integer 3DM incidence CVP.

Basis B=[I_m; M A], target=[0; M 1].  For sufficiently large M the relevant
points satisfy Az=1 over Z and squared distance is ||z||_2^2.  We exhaustively
find the exact integer-fiber minimum on tiny YES/NO 3DM instances, including
signed coefficients, and verify the advertised lattice residuals.  A tested
mutation appends global pair-projection equations to A (targets are allowed to
vary over the finite family realized by perfect matchings; this is only a
finite construction diagnostic, not yet a many-one reduction).
"""
from __future__ import annotations
import itertools
import verify_feature_shell_3dm as b


def ivec(q,u):
    v=[0]*(3*q);v[u[0]]=1;v[q+u[1]]=1;v[2*q+u[2]]=1;return v

def exact_integer_min(q,T,C=2,extra=None,target_extra=None):
    cols=[ivec(q,u) for u in T]; target=[1]*(3*q)
    if extra:
        for j in range(len(T)):cols[j]+= [row[j] for row in extra]
        target += list(target_extra)
    best=None;arg=None;count=0
    # Meet in the middle exact dictionary keyed by row sum.
    h=len(T)//2
    left={}
    vals=range(-C,C+1)
    for z in itertools.product(vals,repeat=h):
        s=tuple(sum(z[j]*cols[j][i] for j in range(h)) for i in range(len(target)))
        norm=sum(a*a for a in z)
        if s not in left or norm<left[s][0]:left[s]=(norm,z)
    for w in itertools.product(vals,repeat=len(T)-h):
        s=tuple(sum(w[j-h]*cols[j][i] for j in range(h,len(T))) for i in range(len(target)))
        need=tuple(target[i]-s[i] for i in range(len(target)))
        if need in left:
            norm=left[need][0]+sum(a*a for a in w);count+=1
            if best is None or norm<best:best=norm;arg=left[need][1]+w
    return best,arg,count

def pair_rows(q,T):
    rows=[]
    for kind in range(3):
      for a in range(q):
       for c in range(q):
        rows.append([int((((u[0],u[1]),(u[0],u[2]),(u[1],u[2]))[kind])==(a,c)) for u in T])
    return rows

def pair_target(rows,x):return [sum(row[j] for j in range(len(row)) if (x>>j)&1) for row in rows]

def pair_fiber_norms(q,T):
    """All pair-projection targets attained by signed {-1,0,1} incidence covers."""
    R=pair_rows(q,T); out={}
    for z in itertools.product((-1,0,1),repeat=len(T)):
        if all(sum(z[j]*ivec(q,T[j])[i] for j in range(len(T)))==1 for i in range(3*q)):
            tar=tuple(sum(R[i][j]*z[j] for j in range(len(T))) for i in range(len(R)))
            norm=sum(a*a for a in z)
            if tar not in out or norm<out[tar]:out[tar]=norm
    return out


def lattice_check(q,T,z,M=1000):
    A=[ivec(q,u) for u in T]; target=[1]*(3*q)
    bottom=[sum(z[j]*A[j][i] for j in range(len(T)))*M for i in range(3*q)]
    residual=sum((bottom[i]-M*target[i])**2 for i in range(3*q))
    top=sum(a*a for a in z)
    return top+residual,residual

def main():
    q,m=3,8;Y,N=b.families(q,m,40)
    yr=[];nr=[];witnesses=[]
    for label,fam,out in [('YES',Y,yr),('NO',N,nr)]:
      for T,M,F in fam:
        val,z,c=exact_integer_min(q,T,2)
        assert val is not None
        out.append(val)
        d,res=lattice_check(q,T,z);assert res==0 and d==val
        witnesses.append((label,T,val,z))
    print({'YES_integer_norm2_distribution':{v:yr.count(v) for v in sorted(set(yr))},
           'NO_integer_norm2_distribution':{v:nr.count(v) for v in sorted(set(nr))},
           'worst_YES':max(yr),'best_NO':min(nr)})
    # Positive finite fact: allowing arbitrary signed integer coefficients does
    # not erase the 3-vs-5 squared-norm gap on this family.
    assert max(yr)==3 and min(nr)==5
    light=next(w for w in witnesses if w[0]=='NO' and w[2]==5)
    print({'lightest_signed_NO':light})

    # Mutation test: append pair-projection target of each perfect matching and
    # ask whether some target shell separates signed repairs.  Use a bounded
    # deterministic subfamily (four YES/four NO, all q!^2 universal targets)
    # so this verifier remains a fast exact finite certificate.
    # Projection target has three q-by-q permutation matrices.  Enumerate the
    # q!^2 consistent choices directly instead of enumerating 2^(q^3) subsets.
    targets=[]
    for p in itertools.permutations(range(q)):
      for r in itertools.permutations(range(q)):
       v=[]
       for kind in range(3):
        for a in range(q):
         for c in range(q):
          if kind==0:v.append(int(c==p[a]))
          elif kind==1:v.append(int(c==r[a]))
          else:
           # BC permutation is r composed with inverse p.
           aa=p.index(a);v.append(int(c==r[aa]))
       targets.append(tuple(v))
    targets=sorted(set(targets));assert len(targets)==36
    mutY=[];mutN=[]
    for T,M,F in Y[:4]:
      R=pair_rows(q,T); norms=pair_fiber_norms(q,T)
      vals=[norms[tuple(pair_target(R,x))] for x in M]
      mutY.append(min(vals)) # existential matching/target branch
    for T,M,F in N[:4]:
      norms=pair_fiber_norms(q,T)
      vals=[norms[tar] for tar in targets if tar in norms]
      mutN.append(min(vals) if vals else 10**9)
    print({'pair_target_mutation_worstYES':max(mutY),'bestNO':min(mutN),
           'YES_dist':{v:mutY.count(v) for v in sorted(set(mutY))},
           'NO_dist':{v:mutN.count(v) for v in sorted(set(mutN))}})
    # Record the exact result without prejudging it: this mutation is only a
    # finite diagnostic because choosing/disjoining projection targets is not
    # yet encoded as one many-one CVP target.
    assert max(mutY)==3
    assert min(mutN)>=3
    print('direct integer 3DM CVP construction and mutation attacked exactly')

if __name__=='__main__':main()
