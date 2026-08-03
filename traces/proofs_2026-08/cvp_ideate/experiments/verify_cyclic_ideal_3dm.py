#!/usr/bin/env python3
"""Exact mutation: couple a 3DM pointed code to a cyclic ideal before folding.

Direct cyclic closure destroyed the 3DM gap.  Here the instance code is retained
as one tensor factor, while a small cyclic ideal supplies structured
self-correlation compression and a free Z_15 action.  Reduced orbit folding is
then applied only to the phase coordinate.  Every mixed image word is exactly
enumerated for fixed YES/NO 3DM instances.
"""
from __future__ import annotations

import itertools
import random


def basis(rows):
    piv = {}
    for z in rows:
        while z:
            p = z.bit_length()-1
            if p in piv:
                z ^= piv[p]
            else:
                for q,y in list(piv.items()):
                    if (y>>p)&1:
                        piv[q]=y^z
                piv[p]=z; break
    return [piv[p] for p in sorted(piv)]


def words(rows):
    for mask in range(1<<len(rows)):
        z=0
        for i,r in enumerate(rows):
            if (mask>>i)&1:z^=r
        yield z


def pd(rows):
    return min((z>>1).bit_count() for z in words(rows) if z&1)


def syndrome(q,u):
    return (1<<u[0])|(1<<(q+u[1]))|(1<<(2*q+u[2]))


def instance_code(q,triples):
    cols=[syndrome(q,u) for u in triples]; target=(1<<(3*q))-1
    K=[];F=[]
    for mask in range(1<<len(cols)):
        s=0
        for j,c in enumerate(cols):
            if (mask>>j)&1:s^=c
        if s==0:K.append(mask)
        if s==target:F.append(mask)
    assert F
    point=min(F,key=int.bit_count)
    rows=[z<<1 for z in basis(K)]+[1|(point<<1)]
    rows=basis(rows)
    assert pd(rows)==point.bit_count()
    return rows,pd(rows)


def poly_mul(a,b):
    z=0
    while b:
        lb=b&-b;z^=a<<(lb.bit_length()-1);b^=lb
    return z


def cyclic_ideal():
    # ell=15, generator (x^4+x+1)(x^4+x^3+1)(x^4+x^3+x^2+x+1),
    # a degree-12 divisor of x^15+1.  Dimension 3, odd distance 5.
    ell=15
    g=poly_mul(poly_mul((1<<4)|(1<<1)|1,(1<<4)|(1<<3)|1),
               (1<<4)|(1<<3)|(1<<2)|(1<<1)|1)
    rows=basis([g<<i for i in range(3)])
    odd=[z for z in words(rows) if z.bit_count()&1]
    assert min(map(int.bit_count,odd))==5
    return ell,rows,5


def product_code(inst_rows,m,ideal_rows,ell):
    # Moving code C_inst tensor A; corner/star form is product of star forms.
    out=[]
    for u in inst_rows:
        for a in ideal_rows:
            z=(u&1)&(a.bit_count()&1)
            for j in range(m):
                if (u>>(1+j))&1:
                    for h in range(ell):
                        if (a>>h)&1:z^=1<<(1+j*ell+h)
            out.append(z)
    return basis(out)


def fold(rows,m,ell):
    out=[]
    for a in rows:
        for b in rows:
            z=(a&1)&(b&1)
            for j in range(m):
                for h in range(ell):
                    if not ((a>>(1+j*ell+h))&1):continue
                    for k in range(m):
                        for t in range(ell):
                            if (b>>(1+k*ell+t))&1:
                                z^=1<<(1+(j*m+k)*ell+(t-h)%ell)
            out.append(z)
    return basis(out)


def planted(q,m,seed):
    rng=random.Random(seed);diag=[(i,i,i) for i in range(q)]
    rest=[u for u in itertools.product(range(q),repeat=3) if u not in diag]
    rng.shuffle(rest);return diag+rest[:m-q]


def random_instance(q,m,seed):
    rng=random.Random(seed);a=list(itertools.product(range(q),repeat=3));rng.shuffle(a);return a[:m]


def find_no(q,m):
    for seed in range(100000,110000):
        T=random_instance(q,m,seed)
        try:rows,d=instance_code(q,T)
        except AssertionError:continue
        if d>q:return seed,T,rows,d
    raise RuntimeError


def main():
    q,m=3,5
    Y=planted(q,m,9);Yr,Yd=instance_code(q,Y);assert Yd==3
    seed,N,Nr,Nd=find_no(q,m);assert Nd==5
    ell,A,ad=cyclic_ideal()
    reports=[]
    for label,rows,d in [('YES',Yr,Yd),('NO',Nr,Nd)]:
        P=product_code(rows,m,A,ell)
        base=pd(P);assert base==d*ad
        F=fold(P,m,ell);fp=pd(F)
        # The cyclic ideal is correlation-stable at odd pointed distance 5.
        assert fp==d*d*ad
        reports.append((label,len(rows),len(P),base,len(F),fp))
    print({'NO_seed':seed,'ell':ell,'ideal_dim':len(A),'ideal_odd_distance':ad})
    for r in reports:print(r)
    from fractions import Fraction
    assert Fraction(reports[1][-1],reports[0][-1])==Fraction(5,3)**2
    print('Cyclic-ideal coupling preserves the 3DM ratio square exactly.')

if __name__=='__main__':main()
