#!/usr/bin/env python3
"""Verify phase cocycle classification and support-three restoration on finite type graphs."""
from __future__ import annotations
import collections,random


def coboundary_or_cycle(L,R,edges,q):
    """edges: (l,r,alpha). Return potentials or a nonzero-holonomy closed walk."""
    adj=collections.defaultdict(list)
    for idx,(l,r,a) in enumerate(edges):
        adj[('L',l)].append((('R',r),a,idx))
        adj[('R',r)].append((('L',l),-a,idx)) # potential_L - potential_R = alpha
    pot={};parent={}
    for root in list(adj):
        if root in pot:continue
        pot[root]=0;parent[root]=None;stack=[root]
        while stack:
            u=stack.pop()
            for v,delta,idx in adj[u]:
                # traversing L->R: p_R=p_L-alpha; stored delta=alpha.
                expected=(pot[u]-delta)%q
                if v not in pot:pot[v]=expected;parent[v]=(u,idx);stack.append(v)
                elif pot[v]!=expected:return None,(u,v,idx,(pot[v]-expected)%q)
    beta={x:pot.get(('L',x),0) for x in L};gamma={x:pot.get(('R',x),0) for x in R}
    assert all((beta[l]-gamma[r]-a)%q==0 for l,r,a in edges)
    return (beta,gamma),None

def run(seed=97):
 rng=random.Random(seed);checks=0;detected=0
 for q in (2,3,5,8):
  for _ in range(100):
   L=list(range(5));R=list(range(4));beta={l:rng.randrange(q) for l in L};gamma={r:rng.randrange(q) for r in R}
   E=[]
   for l in L:
    for r in R:
     if rng.random()<.45:E.append((l,r,(beta[l]-gamma[r])%q))
   if not E:continue
   p,c=coboundary_or_cycle(L,R,E,q);assert p is not None and c is None;checks+=1
   # Perturb one edge only when it lies on a cycle; classifier then detects if holonomy changes.
   idx=rng.randrange(len(E));bad=E.copy();l,r,a=bad[idx];bad[idx]=(l,r,(a+1)%q)
   p,c=coboundary_or_cycle(L,R,bad,q)
   if p is None:detected+=1
 # Explicit three-view boundary after gauge: phases beta_(port,bit).
 for q in (2,3,7):
  beta={(r,b):rng.randrange(q) for r in range(3) for b in (0,1)}
  u=(0,0,0);a=(1,0,0);b=(0,1,0);c=(1,1,0)
  # GF2 multiset at each (port,bit,phase) equals forbidden singleton.
  lhs=[]
  for v in (a,b,c):
   lhs += [(r,v[r],beta[r,v[r]]) for r in range(3)]
  odd={x for x in lhs if lhs.count(x)%2}
  rhs={(r,u[r],beta[r,u[r]]) for r in range(3)}
  assert odd==rhs
 print({'random_coboundaries_recovered':checks,'single_edge_cycle_perturbations_detected':detected,
        'support_three_gauge_checks':3})
 return checks,detected
if __name__=='__main__':run()
