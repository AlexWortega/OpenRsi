#!/usr/bin/env python3
"""Exact construction/attack: linear feature-cost shells for BMT 3DM.

Given Ax=1, append variables z=Fx and charge their Hamming weight (optionally
R replicated copies).  The resulting binary syndrome system is explicit:
rows are Ax=1 and z^(s)+Fx=0 for each copy s.  Its optimum is
|x|+R|Fx|.  We test genuinely global pair-projection features and deterministic
sparse expander/hash features.  Completeness uses the worst perfect matching
in each YES instance; soundness is the exact minimum over every odd cover.
No nearest witness is used to construct F.
"""
from __future__ import annotations
import itertools, random
from collections import defaultdict


def triples(q): return list(itertools.product(range(q), repeat=3))
def col(q,u): return (1<<u[0])|(1<<(q+u[1]))|(1<<(2*q+u[2]))
def xor_cols(q,T,x):
    z=0
    for j,u in enumerate(T):
        if (x>>j)&1:z^=col(q,u)
    return z

def fiber(q,T):
    t=(1<<(3*q))-1
    return [x for x in range(1<<len(T)) if xor_cols(q,T,x)==t]
def matchings(q,T): return [x for x in fiber(q,T) if x.bit_count()==q]

def feature_pair(q,T):
    """Rows for all AB, AC, BC pair projections."""
    rows=[]
    for kind in range(3):
        for a in range(q):
            for b in range(q):
                r=0
                for j,u in enumerate(T):
                    pair=((u[0],u[1]),(u[0],u[2]),(u[1],u[2]))[kind]
                    if pair==(a,b):r|=1<<j
                rows.append(r)
    return rows

def feature_hash(T,B,D,seed):
    """Deterministic D-left-regular triple-to-bucket adjacency matrix."""
    rows=[0]*B
    for j,u in enumerate(T):
        # Stable arithmetic hash of the actual triple, not its input position.
        code=1+u[0]+17*u[1]+289*u[2]
        rng=random.Random(seed+1000003*code)
        for r in rng.sample(range(B),D): rows[r]|=1<<j
    return rows

def feature_hybrid(q,T,B,D,seed): return feature_pair(q,T)+feature_hash(T,B,D,seed)
def fweight(rows,x): return sum((r&x).bit_count()&1 for r in rows)
def cost(rows,x,R): return x.bit_count()+R*fweight(rows,x)

def planted(q,m,seed):
    rng=random.Random(seed); diag=[(i,i,i) for i in range(q)]
    rest=[u for u in triples(q) if u not in diag];rng.shuffle(rest)
    return sorted(diag+rest[:m-q])
def random_instance(q,m,seed):
    a=triples(q);random.Random(seed).shuffle(a);return sorted(a[:m])

def families(q=3,m=8,count=40):
    Y=[];N=[]
    for s in range(10000):
        T=planted(q,m,s); M=matchings(q,T)
        if M:Y.append((T,M,fiber(q,T)))
        if len(Y)==count:break
    for s in range(20000,100000):
        T=random_instance(q,m,s); F=fiber(q,T);M=[x for x in F if x.bit_count()==q]
        if F and not M:N.append((T,M,F))
        if len(N)==count:break
    assert len(Y)==len(N)==count
    assert all(min(x.bit_count() for x in F)==5 for T,M,F in N)
    return Y,N

def explicit_matrix_check(q,T,rows,R,x):
    """Check the advertised augmented syndrome witness exactly."""
    m=len(T); p=len(rows); n=m+R*p
    H=[]; rhs=[]
    # Incidence equations on x.
    for e in range(3*q):
        H.append(sum(((col(q,u)>>e)&1)<<j for j,u in enumerate(T)));rhs.append(1)
    # z_(s,r) + F_r x = 0.
    zbits=0
    for s in range(R):
        for r,fr in enumerate(rows):
            row=fr | (1<<(m+s*p+r));H.append(row);rhs.append(0)
            if (fr&x).bit_count()&1:zbits|=1<<(m+s*p+r)
    w=x|zbits
    assert all(((h&w).bit_count()&1)==b for h,b in zip(H,rhs))
    assert w.bit_count()==cost(rows,x,R)
    return len(H),n

def main():
    q,m=3,8;Y,N=families(q,m);specs=[]
    specs.append(('pair',lambda T:feature_pair(q,T)))
    for B,D in [(8,2),(12,2),(16,3),(24,3)]:
        specs.append((f'hash-{B}-{D}',lambda T,B=B,D=D:feature_hash(T,B,D,911)))
        specs.append((f'hybrid-{B}-{D}',lambda T,B=B,D=D:feature_hybrid(q,T,B,D,911)))
    reports=[];cheats=[]
    for name,mk in specs:
        for R in [1,2,4,8,16]:
            yes=[];no=[]
            for T,M,F in Y:
                rows=mk(T)
                # Uniform completeness threshold for this instance: every
                # matching is accepted, so use the maximum matching cost.
                yes.append(max(cost(rows,x,R) for x in M))
            for T,M,F in N:
                rows=mk(T); opt=min(cost(rows,x,R) for x in F);no.append(opt)
                if opt<=max(yes):
                    x=min(F,key=lambda z:cost(rows,z,R))
                    cheats.append((name,R,T,x,x.bit_count(),fweight(rows,x),opt))
            CY=max(yes);SN=min(no); reports.append((SN/CY,name,R,CY,SN,min(yes),max(no)))
    reports.sort(reverse=True)
    print('ratio,name,R,worstYES,bestNO,bestYES,worstNO')
    for z in reports:print(z)
    best=reports[0]
    # Compare to the exact unshelled 5/3 gap on these instances.
    assert best[0] <= 5/3 + 1e-12
    assert cheats
    name,R,T,x,wx,fx,opt=cheats[0]
    rows=dict(specs)[name](T)
    dims=explicit_matrix_check(q,T,rows,R,x)
    print({'first_exact_cheat':(name,R,T,x,wx,fx,opt),'augmented_rows_cols':dims})
    print({'tested_instances_each':len(Y),'feature_shells':len(reports),
           'best':best})
    print('linear feature shell construction attacked exactly')

if __name__=='__main__':main()
