#!/usr/bin/env python3
"""Arbitrary global fingerprints over fixed prime fields."""
from __future__ import annotations
import random
import numpy as np

def kernel_relation(W,p):
    rows,q=W.shape;M=[[int(W[i,j])%p for i in range(rows)]for j in range(q)]
    basis={};comb={}
    for j in range(q):
        v=M[j][:];c=[0]*q;c[j]=1
        while any(v):
            pivot=max(i for i,x in enumerate(v)if x)
            if pivot not in basis:
                inv=pow(v[pivot],-1,p);v=[x*inv%p for x in v];c=[x*inv%p for x in c]
                basis[pivot]=v;comb[pivot]=c;break
            a=v[pivot];v=[(x-a*y)%p for x,y in zip(v,basis[pivot])];c=[(x-a*y)%p for x,y in zip(c,comb[pivot])]
        if not any(v):return c
    return None

def build(F,p):
    q=len(F);m=len(F[0]);meta=[(u,x)for u in range(q)for x in range(q)if x!=u];idx={v:i for i,v in enumerate(meta)};rows=[];t=[]
    def add(entries,rhs):
        r=[0]*len(meta)
        for j,v in entries:r[j]=(r[j]+v)%p
        rows.append(r);t.append(rhs)
    for u in range(q):add([(idx[u,x],1)for x in range(q)if x!=u],1)
    for k in range(m):
        for u in range(1,q):add([(idx[u,x],F[x][k])for x in range(q)if x!=u]+[(idx[0,x],-F[x][k])for x in range(1,q)],0)
    return np.array(rows,dtype=object),np.array(t,dtype=object),meta

def witness(F,p):
    q=len(F);W=np.array([[1]*q]+[[F[x][k]for x in range(q)]for k in range(len(F[0]))],dtype=object)
    rel=kernel_relation(W,p);supp=[i for i,x in enumerate(rel)if x%p];a=supp[0];inv=pow(rel[a],-1,p)
    A,t,meta=build(F,p);idx={v:i for i,v in enumerate(meta)};z=np.zeros(len(meta),dtype=object)
    for u in range(q):
        if u!=a:z[idx[u,a]]=1
        else:
            for x in supp[1:]:z[idx[a,x]]=(-rel[x]*inv)%p
    return A,t,z,rel,a

def run(q=12,trials=20,seed=2111):
    rng=random.Random(seed);rec=[]
    for p in (2,3,5,7):
        m=q-2
        for _ in range(trials):
            F=[[rng.randrange(p)for _ in range(m)]for _ in range(q)]
            A,t,z,rel,a=witness(F,p);assert np.all((A@z-t)%p==0)
            centered=[min(int(x)%p,p-int(x)%p)for x in z]
            rec.append({'p':p,'support':int(np.count_nonzero(z)),'centered_squared_norm':sum(x*x for x in centered)})
    result={'q':q,'m':q-2,'trials_per_prime':trials,'primes':[2,3,5,7],
            'max_support':max(x['support']for x in rec),'max_centered_squared_by_p':{p:max(x['centered_squared_norm']for x in rec if x['p']==p)for p in (2,3,5,7)}}
    print(result);return result
if __name__=='__main__':run()
