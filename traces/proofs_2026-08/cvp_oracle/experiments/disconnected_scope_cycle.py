#!/usr/bin/env python3
"""Test disconnected-scope GF(2) marginals on an inconsistent 3-color cycle CSP."""
from __future__ import annotations
import argparse,itertools,random
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import coo_matrix,hstack

def legal_colorings(n,scope):
    V,E=scope;V=tuple(sorted(V));pos={v:i for i,v in enumerate(V)};out=[]
    for a in itertools.product(range(3),repeat=len(V)):
        ok=True
        for e in E:
            u=e;v=(e+1)%n;shift=1 if e==n-1 else 0
            if (a[pos[v]]-a[pos[u]])%3!=shift:ok=False;break
        if ok:out.append(a)
    return V,out

def closure_scopes(n,base_edge_sets):
    # Scope is (vertex frozenset, constrained-edge frozenset). Pair intersections included.
    scopes=set()
    for E in base_edge_sets:
        V=set()
        for e in E:V.update((e,(e+1)%n))
        scopes.add((frozenset(V),frozenset(E)))
    changed=True
    while changed:
        changed=False;old=list(scopes)
        for V1,E1 in old:
            for V2,E2 in old:
                V=V1&V2
                if not V:continue
                E=frozenset(e for e in E1&E2 if e in V and (e+1)%n in V)
                s=(frozenset(V),E)
                if s not in scopes:scopes.add(s);changed=True
    return sorted(scopes,key=lambda s:(len(s[0]),len(s[1]),tuple(s[0]),tuple(s[1])))

def build(n,scopes):
    info=[];cols=[];idx={}
    for si,s in enumerate(scopes):
        V,A=legal_colorings(n,s);info.append((V,A))
        for a in A:idx[si,a]=len(cols);cols.append((si,a))
    rr=[];cc=[];dd=[];t=[]
    for si,(V,A) in enumerate(info):
        r=len(t);t.append(1)
        for a in A:rr.append(r);cc.append(idx[si,a]);dd.append(1)
    # All strict scope inclusions in closure.
    for big,(VB,AB) in enumerate(info):
        setVB=set(VB);pB={v:i for i,v in enumerate(VB)}
        for small,(VS,AS) in enumerate(info):
            if small==big or not set(VS)<setVB:continue
            # Require small constraints subset of big constraints.
            if not scopes[small][1] <= scopes[big][1]:continue
            poses=tuple(pB[v] for v in VS)
            for b in AS:
                r=len(t);t.append(0);rr.append(r);cc.append(idx[small,b]);dd.append(1)
                for a in AB:
                    if tuple(a[p] for p in poses)==b:rr.append(r);cc.append(idx[big,a]);dd.append(1)
    return coo_matrix((dd,(rr,cc)),shape=(len(t),len(cols)),dtype=np.int8),np.array(t),info

def solve(H,t,limit=120):
 H=H.tocsr().astype(float);r,p=H.shape;A=hstack([H,-2*coo_matrix(np.eye(r))],format='csr')
 res=milp(np.r_[np.ones(p),np.zeros(r)],integrality=np.ones(p+r),
  bounds=Bounds(np.zeros(p+r),np.r_[np.ones(p),np.asarray(H.sum(axis=1)).ravel()//2+1]),
  constraints=LinearConstraint(A,t,t),options={'time_limit':limit})
 return res

def run(n=6,d=3,count=8,seed=131):
 rng=random.Random(seed);base=[]
 for _ in range(count):base.append(frozenset(rng.sample(range(n),d)))
 # Ensure every edge appears and include singleton edges.
 base += [frozenset((e,)) for e in range(n)]
 scopes=closure_scopes(n,base);H,t,info=build(n,scopes);res=solve(H,t)
 K=len(scopes);result={'n':n,'d':d,'base_scopes':count,'closure_scopes_K':K,'shape':H.shape,
  'status':res.status,'reported_optimum':None if res.fun is None else round(res.fun),
  'ratio':None if res.fun is None else res.fun/K,'component_proxy_max_colorings':max(len(A) for V,A in info)}
 print(result);return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=6);ap.add_argument('--d',type=int,default=3);ap.add_argument('--count',type=int,default=8);ap.add_argument('--seed',type=int,default=131)
 a=ap.parse_args();run(a.n,a.d,a.count,a.seed)
