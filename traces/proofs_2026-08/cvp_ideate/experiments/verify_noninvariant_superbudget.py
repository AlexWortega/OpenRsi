#!/usr/bin/env python3
"""Exhaustive non-invariant YES test for one-orbit reduced group folds.

For every nonempty x subset Z_ell, build D_x = span{(1,gx):g in Z_ell}.
The selected YES word x need not be invariant.  Enumerate the true base pointed
moving distance d and true reduced orbit-fold distance d'.  This attacks the
'super-budget' hope that ell>d can make d' attain ceil(d^2/ell) cheaply.
"""
from __future__ import annotations

from collections import Counter


def rank_basis(rows):
    piv = {}
    for x in rows:
        while x:
            p = x.bit_length()-1
            if p in piv:x ^= piv[p]
            else:
                for q,y in list(piv.items()):
                    if (y>>p)&1:piv[q]=y^x
                piv[p]=x;break
    return [piv[p] for p in sorted(piv)]


def words(rows):
    for s in range(1<<len(rows)):
        x=0
        for i,r in enumerate(rows):
            if (s>>i)&1:x^=r
        yield x


def shift_mask(x,ell):
    low=x&1
    mov=x>>1
    mov=((mov<<1)&((1<<ell)-1)) | (mov>>(ell-1))
    return low | (mov<<1)


def orbit_code(mask,ell):
    x=1|(mask<<1); rows=[]
    for _ in range(ell):
        rows.append(x);x=shift_mask(x,ell)
    return rank_basis(rows)


def pd(rows):
    return min((x>>1).bit_count() for x in words(rows) if x&1)


def fold(rows,ell):
    # One moving orbit: output moving coordinate is phase difference.
    out=[]
    for a in rows:
        for b in rows:
            y=(a&1)&(b&1)
            for i in range(ell):
                if (a>>(1+i))&1:
                    for j in range(ell):
                        if (b>>(1+j))&1:
                            y ^= 1 << (1+(j-i)%ell)
            out.append(y)
    return rank_basis(out)


def canonical(mask,ell):
    vals=[];x=mask
    for _ in range(ell):
        vals.append(x)
        x=((x<<1)&((1<<ell)-1)) | (x>>(ell-1))
    return min(vals)


def main():
    total=0; stats=Counter(); examples=[]
    for ell in [3,5,7,11]:
        seen=set()
        for mask in range(1,1<<ell):
            c=canonical(mask,ell)
            if c in seen:continue
            seen.add(c)
            rows=orbit_code(mask,ell)
            d=pd(rows)
            if d==0:continue  # (1,0) lies in D; not a valid pointed coset.
            fr=fold(rows,ell)
            dp=pd(fr)
            lower=(d*d+ell-1)//ell
            assert dp>=lower
            total+=1
            key=(ell,d,dp,lower,dp==lower)
            stats[key]+=1
            if len(examples)<20 and ell>d and dp==lower:
                examples.append((ell,mask.bit_count(),len(rows),d,dp,lower,bin(mask)))
    print(f"checked {total} cyclic-orbit pointed codes up to ell=11")
    print(f"valid super-budget cases attaining lower bound: {len(examples)} sample count")
    for e in examples:print(e)
    print("distribution (ell,d,dprime,lower,equality): count")
    for k,v in sorted(stats.items()):print(k,v)


if __name__=='__main__':main()
