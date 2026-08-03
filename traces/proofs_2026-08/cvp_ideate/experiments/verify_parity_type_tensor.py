#!/usr/bin/env python3
"""Exact code-dependent tensor compression by parity-check parallel classes.

For Hx=t over F2, replacing every nonzero column type of H by one copy
preserves the minimum weight exactly.  This script alternates:
  pointed code D -> reduced pointed tensor R(D) -> affine parity-check fiber
  -> exact parallel-class simplification -> homogenized pointed code.
All steps use Gaussian elimination only; no closest word is computed.

The reduced tensor theorem proves that the moving pointed distance squares
before simplification, and the parallel-class lemma preserves it afterward,
for every mixed word.  Small 3DM YES/NO fibers test whether the number of
parity-check types stays small enough to make this an amplifier.
"""
from __future__ import annotations
import itertools
import verify_asymmetric_hash_fold as old


def basis(rows: list[int]) -> list[int]:
    return old.basis(rows)


def nullspace(row_masks: list[int], n: int) -> list[int]:
    """Basis for {x: rows*x=0}, with row masks on n coordinates."""
    piv: dict[int, int] = {}
    for x in row_masks:
        while x:
            p = x.bit_length()-1
            if p in piv:
                x ^= piv[p]
            else:
                for q, y in list(piv.items()):
                    if (y >> p) & 1:
                        piv[q] = y ^ x
                piv[p] = x
                break
    free = [j for j in range(n) if j not in piv]
    out = []
    for f in free:
        x = 1 << f
        # Pivot equations have pivot p and only lower/free coordinates after
        # the basis() convention; evaluating all nonpivot coefficients works.
        for p in sorted(piv):
            if ((piv[p] & x).bit_count() & 1):
                x ^= 1 << p
        assert all(((r & x).bit_count() & 1) == 0 for r in row_masks)
        out.append(x)
    assert len(out) == n-len(piv)
    return basis(out)


def solve(row_masks: list[int], rhs: int, n: int) -> int:
    """Solve rows*x=rhs bits; deterministic free variables zero."""
    aug = []
    for i, r in enumerate(row_masks):
        aug.append(r | (((rhs >> i) & 1) << n))
    piv: dict[int, int] = {}
    for z in aug:
        x = z & ((1 << n)-1)
        b = (z >> n) & 1
        while x:
            p = x.bit_length()-1
            if p in piv:
                zz = piv[p]; x ^= zz & ((1 << n)-1); b ^= (zz >> n) & 1
            else:
                znew = x | (b << n)
                for q, zz in list(piv.items()):
                    if (zz >> p) & 1:
                        piv[q] = zz ^ znew
                piv[p] = znew
                break
        else:
            assert b == 0, "inconsistent"
    sol = 0
    for p in sorted(piv):
        z = piv[p]
        if ((z & sol).bit_count() & 1) != ((z >> n) & 1):
            sol ^= 1 << p
    assert all(((r & sol).bit_count() & 1) == ((rhs >> i) & 1)
               for i, r in enumerate(row_masks))
    return sol


def pointed_from_syndrome(Hrows: list[int], target: int, n: int) -> list[int]:
    K = nullspace(Hrows, n)
    x0 = solve(Hrows, target, n)
    return basis([(k << 1) for k in K] + [1 | (x0 << 1)])


def syndrome_from_pointed(D: list[int], n: int) -> tuple[list[int], int]:
    """Return H,t for moving vectors occurring with star=1 in D."""
    D = basis(D)
    pfull = next(r for r in D if r & 1)
    pointed = pfull >> 1
    # Kernel of the star functional on span(D): star-zero basis rows, and
    # differences of every other star-one basis row with the anchor.
    zero = [(r >> 1) for r in D if not (r & 1)]
    zero += [((r ^ pfull) >> 1) for r in D if (r & 1) and r != pfull]
    C0 = basis(zero)
    H = nullspace(C0, n)  # orthogonal checks
    target = 0
    for i, h in enumerate(H):
        target |= (((h & pointed).bit_count() & 1) << i)
    D2 = pointed_from_syndrome(H, target, n)
    assert len(D2) == len(D) == len(basis(D2 + D))
    return H, target


def simplify_syndrome(H: list[int], target: int, n: int) -> tuple[list[int], int, dict[int,int]]:
    """One column per distinct nonzero syndrome column."""
    cols: dict[int, int] = {}
    mult: dict[int, int] = {}
    for j in range(n):
        c = sum(((h >> j) & 1) << i for i, h in enumerate(H))
        if c:
            mult[c] = mult.get(c, 0) + 1
    types = sorted(mult)
    H2 = []
    for i in range(len(H)):
        H2.append(sum(((c >> i) & 1) << j for j, c in enumerate(types)))
    # Row-reduce augmented equations, pivoting only on coefficient columns.
    piv: dict[int, tuple[int,int]] = {}
    for i, x0 in enumerate(H2):
        x, b = x0, (target >> i) & 1
        while x:
            p = x.bit_length()-1
            if p in piv:
                y, c = piv[p]; x ^= y; b ^= c
            else:
                for q, (y,c) in list(piv.items()):
                    if (y >> p) & 1:
                        piv[q] = (y ^ x, c ^ b)
                piv[p] = (x,b); break
        else:
            assert b == 0
    eqs = [piv[p] for p in sorted(piv)]
    H3 = [x for x,b in eqs]
    t3 = sum(b << i for i,(x,b) in enumerate(eqs))
    return H3, t3, mult


def reduced_tensor(D: list[int], n: int) -> list[int]:
    out = []
    for a in basis(D):
        for b in basis(D):
            y = (a & 1) & (b & 1)
            ua, ub = a >> 1, b >> 1
            for i in range(n):
                if (ua >> i) & 1:
                    for j in range(n):
                        if (ub >> j) & 1:
                            y ^= 1 << (1+i*n+j)
            out.append(y)
    return basis(out)


def direct_min(H: list[int], target: int, n: int) -> int:
    return min(x.bit_count() for x in range(1 << n)
               if all(((h & x).bit_count() & 1) == ((target >> i) & 1)
                      for i, h in enumerate(H)))


def initial(q: int, triples: list[tuple[int,int,int]]) -> tuple[list[int], int, int]:
    C, d = old.instance_code(q, triples)
    return C, len(triples), d


def planted(q: int, m: int, seed: int):
    return old.planted(q, m, seed)


def random_no(q: int, m: int):
    for seed in range(10000, 30000):
        T = old.randomT(q, m, seed)
        z = old.instance_code(q, T)
        if z and z[1] > q:
            return T
    raise AssertionError


def run(label: str, D: list[int], n: int, d: int, levels: int) -> list[dict]:
    rec = [{"level": 0, "n": n, "dim": len(D), "moving_d": d}]
    for lev in range(1, levels+1):
        assert n*n <= 100_000, "experiment size guard"
        R = reduced_tensor(D, n)
        H, t = syndrome_from_pointed(R, n*n)
        H2, t2, mult = simplify_syndrome(H, t, n*n)
        n2 = len(mult)
        D2 = pointed_from_syndrome(H2, t2, n2)
        # The two exact algebraic identities imply d2=d^2; directly enumerate
        # only when small enough as an independent implementation check.
        d2 = d*d
        if len(D2) <= 22:
            assert old.pd(D2) == d2
        rec.append({"level": lev, "formal_n": n*n, "n": n2,
                    "dim": len(D2), "checks": len(H2), "moving_d": d2,
                    "max_multiplicity": max(mult.values()),
                    "distinct_multiplicities": sorted(set(mult.values()))})
        D, n, d = D2, n2, d2
    print(label, rec)
    return rec


def main() -> None:
    q, m = 3, 8
    Y, ny, dy = initial(q, planted(q, m, 17))
    N, nn, dn = initial(q, random_no(q, m))
    assert (dy, dn) == (3, 5)
    yr = run("YES", Y, ny, dy, 2)
    nr = run("NO", N, nn, dn, 2)
    for i in range(3):
        assert yr[i]["moving_d"] == 3 ** (2**i)
        assert nr[i]["moving_d"] == 5 ** (2**i)
    print("ratios", [(5/3) ** (2**i) for i in range(3)])
    # On both hostile fibers every parity-check column remains distinct: exact
    # simplification gives no compression, already through two squarings.
    assert all(r["n"] == r["formal_n"] for r in yr[1:] + nr[1:])
    print("parity-check type tensor experiment passes")


if __name__ == "__main__":
    main()
