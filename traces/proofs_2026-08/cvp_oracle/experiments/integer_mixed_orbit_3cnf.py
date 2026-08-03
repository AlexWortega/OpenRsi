#!/usr/bin/env python3
"""Exact-3CNF realization of the mixed 2/3-orbit integer obstruction.

Each 5-valued state is one-hot encoded.  Permutation equivalences and at-most-
one constraints are padded to exact three-literal clauses.  For every connected
clause set of depth d<n (n = cycle length), its attachment skeleton omits a
cycle edge.  On each skeleton component, sum all branch-B colorings and subtract
all branch-A colorings.  Componentwise mass is 3^c-2^c, odd and positive; scale
by Bezout coefficients to obtain mass exactly one while preserving restrictions.
"""
from __future__ import annotations
from itertools import combinations,product
from math import gcd
import numpy as np

A=range(2); B=range(2,5); COLORS=range(5)

def perm(last,x):
    if not last:return x
    return (x+1)%2 if x<2 else 2+(x-2+1)%3

def make_formula(n):
    clauses=[];attach=[];nv=5*n;aux={}
    def pad(binary,att):
        nonlocal nv
        nv+=1;z=nv;aux[z]=('pad',)
        clauses.extend([tuple(binary)+(z,),tuple(binary)+(-z,)])
        attach.extend([att,att])
    for v in range(n):
        # at least one color: convert 5-OR to exact 3CNF with two chain auxiliaries.
        # (a b y1)&(~y1 c y2)&(~y2 d e)
        nv+=1;y1=nv;aux[y1]=('chain',v,1)
        nv+=1;y2=nv;aux[y2]=('chain',v,2)
        xs=[5*v+c+1 for c in COLORS]
        clauses += [(xs[0],xs[1],y1),(-y1,xs[2],y2),(-y2,xs[3],xs[4])]
        attach += [('v',v)]*3
        for c,d in combinations(COLORS,2):pad((-(5*v+c+1),-(5*v+d+1)),('v',v))
    for e in range(n):
        u=e;v=(e+1)%n
        for c in COLORS:
            a=5*u+c+1; bb=5*v+perm(e==n-1,c)+1
            pad((-a,bb),('e',e));pad((a,-bb),('e',e))
    return clauses,attach,nv,aux

def intersection_graph(clauses):
    scopes=[{abs(x) for x in c} for c in clauses];adj=[set() for _ in clauses]
    for i in range(len(clauses)):
        for j in range(i):
            if scopes[i]&scopes[j]:adj[i].add(j);adj[j].add(i)
    return adj

def connected_subsets(clauses,d):
    adj=intersection_graph(clauses);out=[]
    for size in range(1,d+1):
        for q in combinations(range(len(clauses)),size):
            seen={q[0]};st=[q[0]];allowed=set(q)
            while st:
                for w in adj[st.pop()]&allowed:
                    if w not in seen:seen.add(w);st.append(w)
            if seen==allowed:out.append(q)
    return out

def skeleton(n,q,attach):
    vs=set();es=set()
    for j in q:
        kind,k=attach[j]
        if kind=='v':vs.add(k)
        else:es.add(k);vs|={k,(k+1)%n}
    return vs,es

def components(n,vs,es):
    out=[];seen=set()
    for root in sorted(vs):
        if root in seen:continue
        comp={root};st=[root];seen.add(root)
        while st:
            v=st.pop()
            for e,w in (((v-1)%n,(v-1)%n),(v,(v+1)%n)):
                if e in es and w in vs and w not in seen:seen.add(w);comp.add(w);st.append(w)
        out.append(comp)
    return out

def bezout_mass(c):
    a=3**c;b=2**c
    # extended Euclid ua+vb=1
    def eg(x,y):
        if not y:return (1,0,x)
        p,q,g=eg(y,x%y);return q,p-(x//y)*q,g
    u,v,g=eg(a,b);assert g==1
    return u,v

def assignments_for_scope(n,q,clauses,attach,aux):
    vs,es=skeleton(n,q,attach);comps=components(n,vs,es);c=len(comps);u,v=bezout_mass(c)
    # enumerate independent root colors within a fixed branch, propagate on forest
    records=[]
    for branch,coef in ((tuple(B),u),(tuple(A),v)):
        for roots in product(branch,repeat=c):
            colors={}
            for comp,rootcol in zip(comps,roots):
                root=min(comp);colors[root]=rootcol;st=[root]
                while st:
                    x=st.pop()
                    for e,y,forward in ((x,(x+1)%n,True),((x-1)%n,(x-1)%n,False)):
                        if e in es and y in comp and y not in colors:
                            # inverse only matters on last edge
                            if forward:colors[y]=perm(e==n-1,colors[x])
                            else:
                                colors[y]=next(z for z in branch if perm(e==n-1,z)==colors[x])
                            st.append(y)
            # Canonical global Boolean encoding. Padding is zero. Chain bits for
            # one-hot color c are (0,0) for c<2, (1,0) for c=2, (1,1) for c>2.
            # Using one global rule is essential for restriction consistency.
            vals={}
            for x,col in colors.items():
                for k in COLORS:vals[5*x+k+1]=int(k==col)
            scope=sorted({abs(l) for j in q for l in clauses[j]})
            for x in scope:
                if x in vals:continue
                spec=aux[x]
                if spec[0]=='pad':vals[x]=0
                else:
                    _,vertex,which=spec;col=colors[vertex]
                    vals[x]=int(col>=2) if which==1 else int(col>=3)
            found=tuple(vals[x] for x in scope)
            assert all(any(vals[abs(l)]==(l>0) for l in clauses[j]) for j in q)
            records.append((found,coef))
    # combine collisions
    total={}
    for a,w in records:total[a]=total.get(a,0)+w
    return tuple(sorted({abs(l) for j in q for l in clauses[j]})),{a:w for a,w in total.items() if w}

def build(n=4,d=2):
    assert d<n
    clauses,attach,nv,aux=make_formula(n);groups=connected_subsets(clauses,d)
    tables={q:assignments_for_scope(n,q,clauses,attach,aux) for q in groups}
    meta=[];idx={}
    for q in groups:
        for a in tables[q][1]:idx[q,a]=len(meta);meta.append((q,a))
    rows=[];target=[]
    def add(entries,rhs):
        r=[0]*len(meta)
        for j,v in entries:r[j]+=v
        rows.append(r);target.append(rhs)
    for q in groups:add([(idx[q,a],1) for a in tables[q][1]],1)
    gs=set(groups)
    for q in groups:
        if len(q)<2:continue
        for j in q:
            q2=tuple(x for x in q if x!=j)
            if q2 not in gs:continue
            s1,tab1=tables[q];s2,tab2=tables[q2];pos=[s1.index(x) for x in s2]
            keys=set(tab2)|{tuple(a[k] for k in pos) for a in tab1}
            for b in keys:
                entries=[]
                if b in tab2:entries.append((idx[q2,b],1))
                entries += [(idx[q,a],-1) for a in tab1 if tuple(a[k] for k in pos)==b]
                add(entries,0)
    z=np.array([tables[q][1][a] for q,a in meta],dtype=object)
    return np.array(rows,dtype=object),np.array(target,dtype=object),z,{'clauses':len(clauses),'vars':nv,'groups':len(groups),'columns':len(meta)}

def run(cases=((3,1),(4,2))):
    out=[]
    for n,d in cases:
        H,t,z,info=build(n,d);out.append({'n':n,'d':d,**info,'shape':H.shape,'support':int(np.count_nonzero(z)),'squared_norm':int(sum(int(x)**2 for x in z)),'max_coeff':max(abs(int(x)) for x in z),'exact':bool(np.all(H@z==t))})
    print(out);return out
if __name__=='__main__':run()
