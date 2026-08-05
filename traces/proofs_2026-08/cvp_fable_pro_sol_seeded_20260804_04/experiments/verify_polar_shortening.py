#!/usr/bin/env python3
"""Exact finite attack on Pro proposal 2: polarized affine-coset shortening.

For each naturally eight-coordinate 3DM dictionary, sort triples
lexicographically, form the 64 moving coordinates in ordered-pair order, and
right-multiply row vectors by

    P = [[1,0],[1,1]]^{tensor 6}.

Delete exactly the transformed coordinates that vanish on the full star-zero
subcode.  Reconstruct the resulting binary syndrome fiber and enumerate every
mixed image word.  Tests cover ten YES, 200 NO, twenty affine-closure, the
complete all-eight dictionary, and an eight-coordinate twisted three-matching
holonomy dictionary.  Finite findings are not asymptotic claims.
"""
from __future__ import annotations

import itertools
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prior" / "experiments"))
import verify_asymmetric_hash_fold as base  # type: ignore

MOVING = 64


def polar_transform(word: int) -> int:
    """Row-vector multiplication by [[1,0],[1,1]]^tensor6."""
    value = word & ((1 << MOVING) - 1)
    for bit in range(6):
        stride = 1 << bit
        block = stride << 1
        for start in range(0, MOVING, block):
            for offset in range(stride):
                low, high = start + offset, start + offset + stride
                if (value >> high) & 1:
                    value ^= 1 << low
    return value


POLAR_BASIS = tuple(polar_transform(1 << i) for i in range(MOVING))
assert len(set(POLAR_BASIS)) == MOVING
assert all(polar_transform(POLAR_BASIS[i]) == (1 << i) for i in range(MOVING))


def incidence_fiber(q: int, triples: list[tuple[int,int,int]]):
    triples=sorted(triples); cols=[base.syn(q,t) for t in triples]; target=(1<<(3*q))-1; out=[]
    for x in range(1<<len(triples)):
        s=0
        for j,c in enumerate(cols):
            if (x>>j)&1:s^=c
        if s==target:out.append(x)
    return out


def pointed_code(q,triples):
    triples=sorted(triples); cols=[base.syn(q,t) for t in triples]; target=(1<<(3*q))-1; K=[];F=[]
    for x in range(1<<len(triples)):
        s=0
        for j,c in enumerate(cols):
            if (x>>j)&1:s^=c
        if s==0:K.append(x)
        if s==target:F.append(x)
    if not F:return None
    p=min(F,key=lambda x:(x.bit_count(),x))
    return base.basis([x<<1 for x in K]+[1|(p<<1)]),F


def rref(rows,n):
    rows=[x&((1<<n)-1) for x in rows if x]; piv=[];rank=0
    for col in range(n):
        p=next((i for i in range(rank,len(rows)) if (rows[i]>>col)&1),None)
        if p is None:continue
        rows[rank],rows[p]=rows[p],rows[rank]
        for i in range(len(rows)):
            if i!=rank and ((rows[i]>>col)&1):rows[i]^=rows[rank]
        piv.append(col);rank+=1
        if rank==len(rows):break
    return rows[:rank],piv


def nullspace(rows,n):
    E,piv=rref(rows,n);ans=[]
    for free in (j for j in range(n) if j not in piv):
        x=1<<free
        for row,p in zip(E,piv):
            if (row&x).bit_count()&1:x|=1<<p
        ans.append(x)
    assert all(not ((h&r).bit_count()&1) for h in ans for r in rows)
    return ans


def explicit_fiber(image,moving):
    p=next(r for r in image if r&1); K=[]
    for r in image:
        z=r^(p if r&1 else 0)
        if z:K.append(z>>1)
    K=base.basis(K);H=nullspace(K,moving)
    t=sum((((h&(p>>1)).bit_count()&1)<<i) for i,h in enumerate(H))
    assert len(K)+len(H)==moving
    for r in image:
        s=sum((((h&(r>>1)).bit_count()&1)<<i) for i,h in enumerate(H))
        assert s==(t if r&1 else 0)
    return H,t,len(K)


def gray_minimum(rows):
    """Enumerate all 2^k mixed words with one XOR per Gray-code step."""
    rows=base.basis(rows); current=0; minimum=None; minimum_word=None
    total=1<<len(rows)
    for step in range(total):
        if current&1:
            weight=(current>>1).bit_count()
            if minimum is None or weight<minimum:
                minimum,minimum_word=weight,current
        if step+1<total:
            toggle=((step+1)&-(step+1)).bit_length()-1
            current^=rows[toggle]
    assert minimum is not None
    return minimum,minimum_word,total


def project(word,retained):
    out=0
    for new,old in enumerate(retained):out|=((word>>old)&1)<<new
    return out


def polar_report(q,triples):
    triples=sorted(triples); assert len(triples)==8
    data=pointed_code(q,triples);assert data is not None
    base_rows,fiber=data; square=base.reduced(base_rows,8)
    p=next(r for r in square if r&1); K=[]
    for r in square:
        z=r^(p if r&1 else 0)
        if z:K.append(z>>1)
    K=base.basis(K); transformed_K=base.basis([polar_transform(x) for x in K])
    retained=[j for j in range(MOVING) if any((x>>j)&1 for x in transformed_K)]
    deleted=[j for j in range(MOVING) if j not in retained]

    image=[]
    for r in square:
        y=project(polar_transform(r>>1),retained)
        image.append((r&1)|(y<<1))
    image=base.basis(image)
    minimum,minimum_word,total=gray_minimum(image)
    H,target,kdim=explicit_fiber(image,len(retained))

    legal=[];illegal=[]
    for x in fiber:
        matrix=0
        for i in range(8):
            if not ((x>>i)&1):continue
            for j in range(8):
                if (x>>j)&1:matrix|=1<<(8*i+j)
        cost=project(polar_transform(matrix),retained).bit_count()
        (legal if x.bit_count()==q else illegal).append(cost)
    d=min(x.bit_count() for x in fiber)
    return {"base_distance":d,"unfurled_square_distance":d*d,"source_square_dimension":len(square),"star_zero_dimension":len(K),"fiber_size":len(fiber),"retained_coordinates":len(retained),"deleted_coordinates":len(deleted),"retained_indices":tuple(retained),"image_dimension":len(image),"exact_transfer_rank":len(retained),"parity_check_rank":len(H),"target":target,"folded_distance":minimum,"minimum_output_word":minimum_word,"pointed_kernel":minimum==0,"legal_pure_square_range":None if not legal else [min(legal),max(legal)],"cheapest_semantic_illegal_pure_square":min(illegal,default=None),"mixed_words_enumerated":total}


def families(no_count=200):
    yes=[base.planted(3,8,s) for s in range(10)];no=[]
    for s in range(10000,100000):
        T=base.randomT(3,8,s);F=incidence_fiber(3,T)
        if F and min(x.bit_count() for x in F)>3:
            assert min(x.bit_count() for x in F)==5;no.append(T)
            if len(no)==no_count:break
    assert len(no)==no_count;return yes,no


def span_contains(rows,x):
    for r in sorted(base.basis(rows),key=int.bit_length,reverse=True):
        if x.bit_length()==r.bit_length():x^=r
    return x==0


def closure_witnesses(count=20):
    out=[]
    for seed in range(100000):
        T=base.randomT(3,8,seed);F=incidence_fiber(3,T);M=[x for x in F if x.bit_count()==3]
        if not M:continue
        ref=M[0];D=[x^ref for x in M[1:]];bad=[x for x in F if x.bit_count()!=3 and span_contains(D,x^ref)]
        if bad:
            out.append((seed,T,bad))
            if len(out)==count:break
    assert len(out)==count;return out


def all_eight():return 2,list(itertools.product(range(2),repeat=3))

def holonomy8():
    q=3
    matchings=[[(0,0,0),(1,1,1),(2,2,2)],[(0,0,0),(1,1,2),(2,2,1)],[(0,0,1),(1,2,0),(2,1,2)]]
    T=sorted(set().union(*[set(m) for m in matchings]));assert len(T)==8
    F=incidence_fiber(q,T);bad=set(matchings[0])^set(matchings[1])^set(matchings[2])
    mask=sum(1<<T.index(t) for t in bad);assert mask in F and mask.bit_count()==7
    return q,T


def check_relabel(q,T,exhaustive):
    canonical=sorted(T);perms=itertools.permutations(range(8)) if exhaustive else [tuple(reversed(range(8)))];n=0
    for p in perms:assert sorted(T[i] for i in p)==canonical;n+=1
    # Sorting is the first operation in polar_report, so every such permutation
    # constructs byte-for-byte the same code and transform.
    return n


def compact(r):
    return {k:r[k] for k in ("base_distance","unfurled_square_distance","source_square_dimension","star_zero_dimension","fiber_size","retained_coordinates","deleted_coordinates","image_dimension","exact_transfer_rank","parity_check_rank","folded_distance","pointed_kernel","legal_pure_square_range","cheapest_semantic_illegal_pure_square","mixed_words_enumerated")}


def main():
    yes,no=families();closure=closure_witnesses();q8,eight=all_eight();qh,hol=holonomy8()
    yr=[polar_report(3,T) for T in yes];nr=[polar_report(3,T) for T in no]
    cr=[(s,polar_report(3,T),bad) for s,T,bad in closure];er=polar_report(q8,eight);hr=polar_report(qh,hol)
    worst=max(r["folded_distance"] for r in yr);best=min(r["folded_distance"] for r in nr);maxrank=max(r["exact_transfer_rank"] for r in yr+nr)
    ratio=best/worst if worst else 0.0; exponent=math.log(ratio)/math.log(maxrank) if ratio>1 and maxrank>1 else 0.0;baseline=math.log(25/9)/math.log(65)
    hostile=[r["cheapest_semantic_illegal_pure_square"] for _,r,_ in cr]+[er["cheapest_semantic_illegal_pure_square"],hr["cheapest_semantic_illegal_pure_square"]]
    hostile_baselines=[r["legal_pure_square_range"][1] for _,r,_ in cr]+[er["legal_pure_square_range"][1],hr["legal_pure_square_range"][1]]
    assert all(x is not None for x in hostile)

    relabel=0
    for T in yes+no[:10]+[x[1] for x in closure]+[eight,hol]:relabel+=check_relabel(2 if T is eight else 3,T,True)
    for T in no[10:]:relabel+=check_relabel(3,T,False)
    assert relabel==42*math.factorial(8)+190

    reports=yr+nr+[er,hr]+[r for _,r,_ in cr]
    success=(not any(r["pointed_kernel"] for r in reports) and best>worst and exponent>baseline and all(c>b for c,b in zip(hostile,hostile_baselines)))
    summary={"mechanism":"canonical Arikan/Mobius transform P=[[1,0],[1,1]]^tensor6 followed by exact star-zero shortening","expected_move":"matching fibers polarize to sparse retained channels while odd-cover fibers retain many active channels","falsification":"pointed kernel, NO not above worst YES, hostile illegal cost not above legal baseline, or exponent not above baseline","instances":{"YES_q3_m8":10,"NO_q3_m8":200,"affine_closure_q3_m8":20,"all_eight_q2_m8":1,"holonomy_q3_m8":1},"unfurled":{"worst_YES":9,"best_NO":25,"exact_transfer_rank":64,"rank_exponent":baseline},"folded":{"worst_YES":worst,"best_NO":best,"uniform_ratio":ratio,"max_exact_transfer_rank":maxrank,"rank_exponent":exponent,"YES_distance_range":[min(r["folded_distance"] for r in yr),worst],"NO_distance_range":[best,max(r["folded_distance"] for r in nr)],"YES_pointed_kernels":sum(r["pointed_kernel"] for r in yr),"NO_pointed_kernels":sum(r["pointed_kernel"] for r in nr),"retained_range":[min(r["retained_coordinates"] for r in yr+nr),max(r["retained_coordinates"] for r in yr+nr)]},"all_eight":compact(er),"holonomy":compact(hr),"affine_closure":{"seeds":[s for s,_,_ in cr],"distance_range":[min(r["folded_distance"] for _,r,_ in cr),max(r["folded_distance"] for _,r,_ in cr)],"semantic_illegal_cost_range":[min(r["cheapest_semantic_illegal_pure_square"] for _,r,_ in cr),max(r["cheapest_semantic_illegal_pure_square"] for _,r,_ in cr)],"legal_baseline_range":[min(r["legal_pure_square_range"][1] for _,r,_ in cr),max(r["legal_pure_square_range"][1] for _,r,_ in cr)],"pointed_kernels":sum(r["pointed_kernel"] for _,r,_ in cr)},"mixed_words_enumerated":sum(r["mixed_words_enumerated"] for r in reports),"coordinate_relabelings_checked":relabel,"primary_success":success}
    print(json.dumps(summary,indent=2,sort_keys=True))
    # Freeze the exact failure of the precommitted 64-coordinate transform.
    assert (worst,best,maxrank)==(13,0,63)
    assert [min(r["folded_distance"] for r in yr),worst]==[0,13]
    assert [best,max(r["folded_distance"] for r in nr)]==[0,21]
    assert sum(r["pointed_kernel"] for r in yr)==3
    assert sum(r["pointed_kernel"] for r in nr)==38
    assert (er["retained_coordinates"],er["folded_distance"],er["cheapest_semantic_illegal_pure_square"])==(40,0,0)
    assert sum(r["pointed_kernel"] for _,r,_ in cr)==5
    assert not success
    print("POLAR_SHORTENING_PASS")

if __name__=="__main__":main()
