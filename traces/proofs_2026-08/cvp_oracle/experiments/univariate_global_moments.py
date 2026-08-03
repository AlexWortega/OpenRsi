#!/usr/bin/env python3
"""Global univariate moment rows on the all-assignments-forbidden core.

Assignments are indexed 0..q-1. Equality of moments x^k for k=1..d across
all q groups admits a finite-difference virtual delta of support d+2 in the
exceptional group whenever d<=q-2. Full degree q-1 is exact but uses q moments.
"""
from __future__ import annotations
from math import comb
import numpy as np

def build(q,d):
    meta=[(u,x) for u in range(q) for x in range(q) if x!=u];idx={m:i for i,m in enumerate(meta)}
    rows=[];target=[]
    def add(entries,rhs):
        r=[0]*len(meta)
        for j,v in entries:r[j]+=v
        rows.append(r);target.append(rhs)
    for u in range(q):add([(idx[u,x],1) for x in range(q) if x!=u],1)
    for k in range(1,d+1):
        for u in range(1,q):
            add([(idx[u,x],x**k) for x in range(q) if x!=u]+[(idx[0,x],-x**k) for x in range(1,q)],0)
    return np.array(rows,dtype=object),np.array(target,dtype=object),meta

def witness(q,d,a=0):
    assert a==0 and d<=q-2
    A,t,meta=build(q,d);idx={m:i for i,m in enumerate(meta)};z=np.zeros(len(meta),dtype=object)
    for u in range(1,q):z[idx[u,0]]=1
    # delta_0 on degree <=d equals sum_{j=1}^{d+1} (-1)^(j+1) C(d+1,j) delta_j.
    for j in range(1,d+2):z[idx[0,j]]=(-1)**(j+1)*comb(d+1,j)
    return A,t,z

def rank_mod(A,p=1000003):
    """Exact rank over F_p; here matching full column rank suffices over Q."""
    M=[[int(x)%p for x in row] for row in A.tolist()];m=len(M);n=len(M[0]);r=0
    for c in range(n):
        pivot=next((i for i in range(r,m) if M[i][c]),None)
        if pivot is None:continue
        M[r],M[pivot]=M[pivot],M[r];iv=pow(M[r][c],-1,p)
        M[r]=[(x*iv)%p for x in M[r]]
        for i in range(m):
            if i!=r and M[i][c]:
                a=M[i][c];M[i]=[(x-a*y)%p for x,y in zip(M[i],M[r])]
        r+=1
        if r==m:return r
    return r
def run(q=8):
    rec=[]
    for d in range(q-1):
        A,t,z=witness(q,d);assert np.all(A@z==t)
        rec.append({'degree':d,'shape':A.shape,'support':int(np.count_nonzero(z)),
                    'l1':int(sum(abs(int(x)) for x in z)),'squared_norm':int(sum(int(x)**2 for x in z)),
                    'max_coeff':max(abs(int(x)) for x in z)})
    Af,tf,_=build(q,q-1);r=rank_mod(Af);ra=rank_mod(np.c_[Af,tf])
    result={'q':q,'columns':q*(q-1),'records':rec,'full_degree_shape':Af.shape,'full_rank':r,'augmented_rank':ra,'full_infeasible':ra>r}
    print(result);return result
if __name__=='__main__':run()
