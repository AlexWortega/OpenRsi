#!/usr/bin/env python3
"""Integer all-pairs hierarchy counterexample on a mixed 2/3-flow Petersen CSP.

Take the disjoint union of a charged F2 flow system and a charged F3 flow
system, with a global branch selecting one.  Each local affine solution family
has size a power of 2 or 3.  Signed Bezout-weighted all-solution tables have
integer mass one and matching full-intersection marginals, although both global
branches are inconsistent.
"""
from __future__ import annotations
import itertools
import numpy as np

E=[(0,1),(1,2),(2,3),(3,4),(0,4),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(6,9),(6,8),(5,8)]
inc={v:[] for v in range(10)}
for ei,(u,v) in enumerate(E):inc[u].append((ei,1));inc[v].append((ei,-1))
b=[1]+[0]*9
GROUPS=[(v,) for v in range(10)]+list(itertools.combinations(range(10),2))

def eg(a,b):
    if b==0:return 1,0,a
    x,y,g=eg(b,a%b);return y,x-(a//b)*y,g

def branch_views(Q,p):
    U=tuple(sorted({e for v in Q for e,s in inc[v]}));pos={e:i for i,e in enumerate(U)};out=[]
    for a in itertools.product(range(p),repeat=len(U)):
        if all(sum(s*a[pos[e]] for e,s in inc[v])%p==b[v]%p for v in Q):out.append(a)
    return U,out

def build():
    info=[];meta=[];idx={}
    for gi,Q in enumerate(GROUPS):
        U,A2=branch_views(Q,2);U3,A3=branch_views(Q,3);assert U==U3
        # Give the two branches fixed global signed masses m2=-80,m3=81.
        # Every local solution count divides its branch mass: c2 in {4,8,16},
        # c3 in {9,27,81}. Uniform probability tables scaled by fixed branch
        # masses therefore have integral coefficients and consistent marginals.
        m2,m3=-80,81
        assert m2+m3==1 and m2%len(A2)==0 and m3%len(A3)==0
        table=[((2,)+a,m2//len(A2)) for a in A2]+[((3,)+a,m3//len(A3)) for a in A3]
        info.append((U,table))
        for a,w in table:idx[gi,a]=len(meta);meta.append((gi,a,w))
    rows=[];target=[]
    def add(entries,rhs):
        r=[0]*len(meta)
        for j,c in entries:r[j]+=c
        rows.append(r);target.append(rhs)
    for gi,(U,table) in enumerate(info):add([(idx[gi,a],1) for a,w in table],1)
    for i in range(len(GROUPS)):
        Ui,Ti=info[i];pi={e:k for k,e in enumerate(Ui)}
        for j in range(i):
            Uj,Tj=info[j];pj={e:k for k,e in enumerate(Uj)};W=tuple(sorted(set(Ui)&set(Uj)))
            if not W:continue
            for p in (2,3):
                for z in itertools.product(range(p),repeat=len(W)):
                    entries=[(idx[i,a],1) for a,w in Ti if a[0]==p and tuple(a[1+pi[e]] for e in W)==z]
                    entries += [(idx[j,a],-1) for a,w in Tj if a[0]==p and tuple(a[1+pj[e]] for e in W)==z]
                    add(entries,0)
    z=np.array([w for gi,a,w in meta],dtype=object)
    return np.array(rows,dtype=object),np.array(target,dtype=object),z,info,meta

def run():
    H,t,z,info,meta=build();counts=[]
    for U,table in info:
        c2=sum(a[0]==2 for a,w in table);c3=sum(a[0]==3 for a,w in table)
        counts.append((c2,c3))
    result={'groups':len(GROUPS),'shape':H.shape,'columns':len(meta),'support':int(np.count_nonzero(z)),
            'squared_norm':int(sum(int(x)**2 for x in z)),'max_coeff':max(abs(int(x)) for x in z),
            'count_histogram':{x:counts.count(x) for x in sorted(set(counts))},'exact':bool(np.all(H@z==t)),
            'rhs_sum_mod2':sum(b)%2,'rhs_sum_mod3':sum(b)%3}
    print(result);return result
if __name__=='__main__':run()
