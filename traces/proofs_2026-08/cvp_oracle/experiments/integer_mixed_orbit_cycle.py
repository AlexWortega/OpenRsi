#!/usr/bin/env python3
"""Mixed 2/3-orbit obstruction to integer connected-view hierarchies.

Domain A has two colors and domain B three colors.  Cycle edges preserve the
branch; all are identities except the last, which is fixed-point-free in both
branches.  The CSP is UNSAT.  Every proper connected edge scope is a path with
2 A-colorings and 3 B-colorings.  Weight -1 on all A-colorings and +1 on all
B-colorings gives integer mass 3-2=1 and perfectly consistent marginals.
"""
from __future__ import annotations
from itertools import product
import numpy as np

A = (0,1)
B = (2,3,4)
DOMAIN = A+B


def perm(last: bool, x: int) -> int:
    if not last: return x
    if x in A: return A[(A.index(x)+1)%2]
    return B[(B.index(x)+1)%3]


def connected_scopes(n: int, d: int):
    """All nonempty cyclic intervals of edges of length <=d<n."""
    assert 1 <= d < n
    return [tuple((start+j)%n for j in range(length)) for length in range(1,d+1) for start in range(n)]


def scope_vertices(n, scope):
    return tuple(sorted(set(scope)|{(e+1)%n for e in scope}))


def views(n, scope):
    verts=scope_vertices(n,scope); pos={v:i for i,v in enumerate(verts)};out=[]
    for vals in product(DOMAIN,repeat=len(verts)):
        ok=True
        for e in scope:
            if vals[pos[(e+1)%n]] != perm(e==n-1,vals[pos[e]]):ok=False;break
        if ok:out.append(vals)
    return verts,out


def build(n=5,d=2):
    scopes=connected_scopes(n,d); tables={q:views(n,q) for q in scopes}
    meta=[];idx={}
    for q in scopes:
        for a in tables[q][1]:idx[q,a]=len(meta);meta.append((q,a))
    rows=[];target=[]
    def add(entries,rhs):
        r=[0]*len(meta)
        for j,v in entries:r[j]+=v
        rows.append(r);target.append(rhs)
    for q in scopes:add([(idx[q,a],1) for a in tables[q][1]],1)
    # Every connected subinterval deletion relation represented in the family.
    scope_set=set(scopes)
    for q in scopes:
        if len(q)==1:continue
        for q2 in (q[1:],q[:-1]):
            assert q2 in scope_set
            v1,tab1=tables[q];v2,tab2=tables[q2];p=[v1.index(v) for v in v2]
            for b in tab2:
                entries=[(idx[q2,b],1)]
                entries += [(idx[q,a],-1) for a in tab1 if tuple(a[j] for j in p)==b]
                add(entries,0)
    return np.asarray(rows,dtype=object),np.asarray(target,dtype=object),meta,scopes,tables


def witness(n=5,d=2):
    H,t,meta,scopes,tables=build(n,d);idx={m:i for i,m in enumerate(meta)}
    z=np.zeros(len(meta),dtype=object)
    for q in scopes:
        for a in tables[q][1]:
            branches={x in B for x in a}
            assert len(branches)==1
            z[idx[q,a]]=1 if next(iter(branches)) else -1
    return H,t,z,meta,scopes,tables


def run(cases=((4,1),(5,2),(6,3),(8,4))):
    rec=[]
    for n,d in cases:
        H,t,z,meta,scopes,tables=witness(n,d)
        # each proper connected path has exactly 2+3 legal views
        assert all(len(tables[q][1])==5 for q in scopes)
        rec.append({'n':n,'d':d,'groups_K':len(scopes),'shape':H.shape,
                    'support':int(np.count_nonzero(z)),'squared_norm':int(sum(int(x)**2 for x in z)),
                    'mass_per_group':1,'exact':bool(np.all(H@z==t))})
    print(rec);return rec

if __name__=='__main__':run()
