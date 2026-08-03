#!/usr/bin/env python3
"""Finite end-to-end reduced-fold syndrome -> explicit integer CVP basis.

Build the level-1 YES and NO pointed codes from verify_reduced_fold_3dm.py,
extract an explicit parity-check matrix H and target syndrome, and construct the
full-rank integer basis of Lambda={z in Z^N:Hz=0 mod 2}.  Exact enumeration of
the low-dimensional affine fiber gives squared Euclidean distances 27 and 75.
The basis is verified columnwise and its determinant/index is certified by its
systematic block form.
"""
from __future__ import annotations

from verify_reduced_fold_3dm import (
    basis, words, planted, random_instance, replicated_pointed_code, folded,
)


def rref_rows(rows: list[int]) -> tuple[list[int], list[int]]:
    """True GF(2) reduced row echelon form with ascending pivot columns."""
    A = [z for z in rows if z]
    pivots=[]; r=0
    maxcol=max((z.bit_length() for z in A),default=0)
    for c in range(maxcol):
        p=next((i for i in range(r,len(A)) if (A[i]>>c)&1),None)
        if p is None:continue
        A[r],A[p]=A[p],A[r]
        for i in range(len(A)):
            if i!=r and ((A[i]>>c)&1):A[i]^=A[r]
        pivots.append(c);r+=1
        if r==len(A):break
    A=A[:r]
    assert all(((A[i]>>p)&1)==(i==j) for j,p in enumerate(pivots) for i in range(r))
    return A,pivots


def affine_parts(pointed_rows: list[int], N: int):
    allw = list(words(pointed_rows))
    zero = basis([z >> 1 for z in allw if not (z & 1)])
    point = next(z >> 1 for z in allw if z & 1)
    assert all(z < (1 << N) for z in zero+[point])
    return zero, point


def parity_check(kernel_rows: list[int], N: int):
    R, pivots = rref_rows(kernel_rows)
    pivot_set = set(pivots)
    free = [j for j in range(N) if j not in pivot_set]
    # For every free f, h_f=e_f+sum_{row pivot p with row[f]=1}e_p.
    H = []
    for f in free:
        h = 1 << f
        for row, p in zip(R, pivots):
            if (row >> f) & 1:
                h ^= 1 << p
        H.append(h)
    for h in H:
        assert all((h & z).bit_count() % 2 == 0 for z in R)
    assert len(H) + len(R) == N
    return H, free, pivots


def syndrome(H: list[int], x: int) -> int:
    return sum((((h & x).bit_count() & 1) << i) for i,h in enumerate(H))


def lattice_basis_systematic(H: list[int], free: list[int], kpiv: list[int], N: int):
    """Return N integer columns in original coordinate order.

    Ordering columns of H as free|kpiv gives [I_r|A].  Lattice columns in that
    coordinate ordering are (2e_i,0) and (-A_col,e_j).
    """
    r = len(free); assert len(kpiv) == N-r
    cols = []
    for i, coord in enumerate(free):
        col = [0]*N; col[coord] = 2; cols.append(col)
    for j, coord in enumerate(kpiv):
        col = [0]*N; col[coord] = 1
        for i,h in enumerate(H):
            if (h >> coord) & 1:
                col[free[i]] = -1
        cols.append(col)
    # Every integer basis column has zero binary syndrome.
    for col in cols:
        residue = sum(((v & 1) << i) for i,v in enumerate(col))
        assert syndrome(H,residue) == 0
    # In free|kpiv row/column order this matrix is [[2I,-A],[0,I]], so
    # determinant is exactly 2^r; record rather than invoke floating algebra.
    det_abs = 1 << r
    return cols, det_abs


def run(label: str, q: int, triples):
    rows, blocks, base_d = replicated_pointed_code(q, triples, 3)
    rows, blocks = folded(rows, blocks, 3)
    N = 3*blocks
    K, point = affine_parts(rows, N)
    H, free, kpiv = parity_check(K,N)
    t = syndrome(H,point)
    # Hx=t is exactly point+span(K), checked over all generated affine words;
    # dimensions match, so inclusion is equality.
    affine = [z >> 1 for z in words(rows) if z&1]
    assert all(syndrome(H,z)==t for z in affine)
    assert len(affine)==1<<len(K)
    min_weight = min(map(int.bit_count,affine))
    cols,det_abs = lattice_basis_systematic(H,free,kpiv,N)
    assert det_abs == 1 << len(H)
    return {"case":label,"rank":N,"code_dim":len(K),"check_rank":len(H),
            "target_syndrome_bits":t.bit_count(),"squared_CVP_distance":min_weight,
            "basis_columns":len(cols),"determinant_bit_length":det_abs.bit_length()}


def main():
    q,m=3,8
    yes=run('YES',q,planted(q,m,17))
    no=run('NO',q,random_instance(q,m,10003))
    print(yes);print(no)
    assert yes['rank']==no['rank']==192
    assert yes['squared_CVP_distance']==27
    assert no['squared_CVP_distance']==75
    # Euclidean NO/YES distance ratio = sqrt(75/27)=5/3 exactly.
    assert 75*9==27*25
    print('Explicit rank-192 integer CVP bases have exact distance ratio 5/3.')

if __name__=='__main__':main()
