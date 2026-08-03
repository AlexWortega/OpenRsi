#!/usr/bin/env python3
"""Global Walsh-moment NCP/integer systems on the all-assignments-forbidden core."""
from __future__ import annotations
from itertools import product,combinations
import numpy as np

def subsets(n):return [s for k in range(1,n+1) for s in combinations(range(n),k)]
def omega(n):return list(product((0,1),repeat=n))
def chi(T,x):return -1 if sum(x[i] for i in T)%2 else 1
def parity(T,x):return sum(x[i] for i in T)%2

def build(n,P,field='Z'):
    O=omega(n);anchor=O[0];meta=[];idx={}
    for u in O:
        for x in O:
            if x!=u:idx[u,x]=len(meta);meta.append((u,x))
    rows=[];target=[]
    def add(entries,rhs):
        r=[0]*len(meta)
        for j,v in entries:r[j]+=v
        rows.append(r);target.append(rhs)
    for u in O:add([(idx[u,x],1) for x in O if x!=u],1)
    f=chi if field=='Z' else parity
    for T in P:
        for u in O[1:]:
            add([(idx[u,x],f(T,x)) for x in O if x!=u]+[(idx[anchor,x],-f(T,x)) for x in O if x!=anchor],0)
    return np.array(rows,dtype=object),np.array(target,dtype=object),meta

def integer_witness(n,P,T0,a):
    A,t,meta=build(n,P,'Z');idx={m:i for i,m in enumerate(meta)};O=omega(n);z=np.zeros(len(meta),dtype=object)
    for u in O:
        if u!=a:z[idx[u,a]]=1
        else:
            for x in O:
                if x!=a:z[idx[a,x]]=-chi(T0,x)//chi(T0,a)
    return A,t,z

def binary_witness(n,P,a):
    A,t,meta=build(n,P,'F2');idx={m:i for i,m in enumerate(meta)};O=omega(n);z=np.zeros(len(meta),dtype=object)
    for u in O:
        if u!=a:z[idx[u,a]]=1
        else:
            for x in O:
                if x!=a:z[idx[a,x]]=1
    return A,t,z

def rank_fraction_free(A):
    """Exact rational rank via sympy, tiny n=3 only."""
    import sympy as sp
    return sp.Matrix(A.tolist()).rank()

def run(n=3):
    O=omega(n);S=subsets(n);int_checks=bin_checks=0
    for omitted in S:
        P=[T for T in S if T!=omitted]
        for a in O:
            A,t,z=integer_witness(n,P,omitted,a);assert np.all(A@z==t);int_checks+=1
    # Binary even with all parity moments.
    for a in O:
        A2,t2,e=binary_witness(n,S,a);assert np.all((A2@e-t2)%2==0);bin_checks+=1
    # Full integer Walsh closure is inconsistent: rank augments by one.
    Af,tf,_=build(n,S,'Z');r=rank_fraction_free(Af);ra=rank_fraction_free(np.c_[Af,tf])
    result={'n':n,'q':len(O),'columns':len(O)*(len(O)-1),'proper_integer_checks':int_checks,
            'binary_full_checks':bin_checks,'witness_cost':2*len(O)-2,
            'full_integer_shape':Af.shape,'full_rank':r,'augmented_rank':ra,'full_integer_infeasible':ra>r}
    print(result);return result
if __name__=='__main__':run()
