#!/usr/bin/env python3
"""Verify diagonal odd-orbit cheat for arbitrary disconnected scopes with unary marginals."""
from __future__ import annotations
import itertools,random

def scope_assignment(n,edges):
    """Find one coloring for a proper subset of inconsistent translation-cycle edges."""
    adj=[[] for _ in range(n)]
    for e in edges:
        u,v=e,(e+1)%n;shift=1 if e==n-1 else 0
        adj[u].append((v,shift));adj[v].append((u,-shift))
    color={}
    for root in range(n):
        if root in color:continue
        color[root]=0;stack=[root]
        while stack:
            u=stack.pop()
            for v,s in adj[u]:
                want=(color[u]+s)%3
                if v in color:assert color[v]==want
                else:color[v]=want;stack.append(v)
    return tuple(color[i] for i in range(n))

def verify(n=11,trials=500,seed=151):
    rng=random.Random(seed);checks=0
    for _ in range(trials):
        size=rng.randrange(1,n)
        E=frozenset(rng.sample(range(n),size))
        a=scope_assignment(n,E)
        orbit=[tuple((x+r)%3 for x in a) for r in range(3)]
        # Every orbit member satisfies every selected translation edge.
        for b in orbit:
            for e in E:
                assert (b[(e+1)%n]-b[e])%3==(1 if e==n-1 else 0)
        # At each variable, its unary marginal is exactly all three colors once.
        for v in range(n):assert sorted(b[v] for b in orbit)==[0,1,2]
        checks+=1
    print({'cycle_vertices':n,'arbitrary_proper_scopes_checked':checks,
           'support_per_scope':3,'global_unary_support':3})
if __name__=='__main__':verify()
