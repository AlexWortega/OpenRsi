#!/usr/bin/env python3
"""Subset-sum collisions for arbitrary bounded global integer fingerprints.

For q complete assignments with m bounded integer features, two subsets have the
same augmented (coverage, feature-sum) vector once 2^q exceeds the number of
possible sums. Their difference is a {-1,0,1} relation, yielding an exact
virtual assignment in the all-assignments-forbidden hierarchy.
"""
from __future__ import annotations
import random
import numpy as np

def collision(features):
    q=len(features);m=len(features[0]);seen={};
    for mask in range(1<<q):
        s=[mask.bit_count()]+[0]*m
        for x in range(q):
            if mask>>x&1:
                for j in range(m):s[j+1]+=features[x][j]
        key=tuple(s)
        if key in seen and seen[key]!=mask:
            other=seen[key];lam=[((mask>>x)&1)-((other>>x)&1) for x in range(q)]
            assert any(lam) and all(v in (-1,0,1) for v in lam)
            return lam,mask,other
        seen[key]=mask
    return None

def build(features):
    q=len(features);m=len(features[0]);meta=[(u,x)for u in range(q)for x in range(q)if x!=u];idx={v:i for i,v in enumerate(meta)}
    rows=[];target=[]
    def add(entries,rhs):
        r=[0]*len(meta)
        for j,v in entries:r[j]+=v
        rows.append(r);target.append(rhs)
    for u in range(q):add([(idx[u,x],1)for x in range(q)if x!=u],1)
    for j in range(m):
        for u in range(1,q):
            add([(idx[u,x],features[x][j])for x in range(q)if x!=u]+[(idx[0,x],-features[x][j])for x in range(1,q)],0)
    return np.array(rows,dtype=object),np.array(target,dtype=object),meta

def witness(features,lam):
    q=len(features);a=next(i for i,v in enumerate(lam)if v);sgn=lam[a]
    A,t,meta=build(features);idx={v:i for i,v in enumerate(meta)};z=np.zeros(len(meta),dtype=object)
    for u in range(q):
        if u!=a:z[idx[u,a]]=1
        else:
            for x in range(q):
                if x!=a and lam[x]:z[idx[a,x]]=-lam[x]*sgn
    return A,t,z,a

def run(q=20,m=2,H=2,trials=20,seed=2053):
    rng=random.Random(seed);records=[]
    bins=(q+1)*(2*q*H+1)**m
    assert 2**q>bins
    for _ in range(trials):
        f=[[rng.randint(-H,H)for _ in range(m)]for _ in range(q)]
        got=collision(f);assert got is not None
        lam,_,_=got;A,t,z,a=witness(f,lam);assert np.all(A@z==t)
        records.append({'relation_support':sum(v!=0 for v in lam),'witness_support':int(np.count_nonzero(z)),
                        'squared_norm':int(sum(int(x)**2 for x in z)),'anchor':a})
    result={'q':q,'m':m,'H':H,'trials':trials,'subset_count':2**q,'sum_bin_upper':bins,
            'max_relation_support':max(r['relation_support']for r in records),
            'max_witness_support':max(r['witness_support']for r in records),'records':records}
    print(result);return result
if __name__=='__main__':run()
