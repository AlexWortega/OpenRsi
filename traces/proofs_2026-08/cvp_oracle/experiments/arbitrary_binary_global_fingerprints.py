#!/usr/bin/env python3
"""Matroid obstruction for arbitrary binary global fingerprints.

With q complete assignments and m feature bits, augmented vectors w(x)=(1,f(x))
lie in F2^(m+1). If q>m+1 they are dependent. Any dependence expresses one
assignment's full fingerprint as a subset sum of the others, giving an exact
all-assignments-forbidden NCP witness of weight at most q+m.
"""
from __future__ import annotations
import random
import numpy as np

def dependency(W):
    """Return nonzero GF2 kernel mask of columns, by exact elimination."""
    rows,cols=W.shape;basis={};comb={}
    for j in range(cols):
        v=sum((int(W[i,j])&1)<<i for i in range(rows));c=1<<j
        while v:
            p=v.bit_length()-1
            if p in basis:v^=basis[p];c^=comb[p]
            else:basis[p]=v;comb[p]=c;break
        if not v:
            assert c
            return c
    return None

def build(F):
    q=len(F);m=len(F[0]);meta=[(u,x)for u in range(q)for x in range(q)if x!=u];idx={v:i for i,v in enumerate(meta)}
    rows=[];target=[]
    def add(entries,rhs):
        r=[0]*len(meta)
        for j in entries:r[j]^=1
        rows.append(r);target.append(rhs)
    for u in range(q):add([idx[u,x]for x in range(q)if x!=u],1)
    for k in range(m):
        for u in range(1,q):
            add([idx[u,x]for x in range(q)if x!=u and F[x][k]]+[idx[0,x]for x in range(1,q)if F[x][k]],0)
    return np.array(rows,dtype=np.uint8),np.array(target,dtype=np.uint8),meta

def witness(F):
    q=len(F);W=np.array([[1]*q]+[[F[x][k]for x in range(q)]for k in range(len(F[0]))],dtype=np.uint8)
    dep=dependency(W);assert dep is not None
    supp=[x for x in range(q)if dep>>x&1];a=supp[0]
    A,t,meta=build(F);idx={v:i for i,v in enumerate(meta)};z=np.zeros(len(meta),dtype=np.uint8)
    for u in range(q):
        if u!=a:z[idx[u,a]]=1
        else:
            for x in supp[1:]:z[idx[a,x]]=1
    return A,t,z,dep,a

def run(q=16,trials=30,seed=2081):
    rng=random.Random(seed);records=[]
    for m in (0,1,3,7,14):
        for _ in range(trials):
            F=[[rng.randrange(2)for _ in range(m)]for _ in range(q)]
            A,t,z,dep,a=witness(F);assert np.array_equal(A@z%2,t)
            records.append({'m':m,'relation_support':dep.bit_count(),'weight':int(z.sum()),'anchor':a})
    result={'q':q,'trials_per_m':trials,'m_values':[0,1,3,7,14],'records':len(records),
            'max_weight_by_m':{m:max(x['weight']for x in records if x['m']==m)for m in (0,1,3,7,14)}}
    print(result);return result
if __name__=='__main__':run()
