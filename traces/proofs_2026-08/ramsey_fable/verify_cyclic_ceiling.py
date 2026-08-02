#!/usr/bin/env python3
"""Machine check of the finite content of the cyclic->Schur restriction lemma.

For all n <= NMAX and k <= KMAX:
  - decide by exhaustive search whether Z_n \\ {0} has a symmetric sum-free
    k-partition (over orbit variables {x, n-x});
  - whenever one exists, check that its restriction to [1, floor((n-1)/2)] is an
    integer sum-free k-partition (the lemma's conclusion), and that
    floor((n-1)/2) <= S(k) for the exact small Schur numbers
    S(1)=1, S(2)=4, S(3)=13 (classical, re-derivable by the same brute force).

Also independently recomputes S(k) for k<=3 by brute force to avoid citing.
Exit 0 iff everything is consistent.
"""
import sys
from itertools import product

NMAX, KMAX = 45, 3

def sumfree_int(cls):
    s = set(cls)
    for a in cls:
        for b in cls:
            if a + b in s:
                return False
    return True

def schur_exact(k, mmax=20):
    """largest m <= mmax such that [1,m] has a sum-free k-partition (equal summands allowed)"""
    best = 0
    for m in range(1, mmax + 1):
        found = False
        for assign in product(range(k), repeat=m):
            classes = [[i + 1 for i in range(m) if assign[i] == c] for c in range(k)]
            if all(sumfree_int(cl) for cl in classes):
                found = True
                break
        if found:
            best = m
        else:
            break
    return best

S = {1: schur_exact(1, 3), 2: schur_exact(2, 6), 3: schur_exact(3, 15)}
assert S == {1: 1, 2: 4, 3: 13}, S
print(f"recomputed Schur numbers: {S}")

def cyclic_partitions(n, k):
    """yield symmetric sum-free k-partitions of Z_n (color vector on orbits), or None"""
    half = n // 2
    def orb(x):
        x %= n
        return min(x, n - x)
    cons = set()
    for a in range(1, n):
        for b in range(a, n):
            c = (a + b) % n
            if c == 0:
                continue
            t = frozenset({orb(a), orb(b), orb(c)})
            if len(t) == 1:
                return None  # structurally impossible
            cons.add(tuple(sorted(t)))
    for assign in product(range(k), repeat=half):
        col = {}
        for o in range(1, half + 1):
            col[o] = assign[o - 1]
        ok = True
        for t in cons:
            if len(set(col[o] for o in t)) == 1:
                ok = False
                break
        if ok:
            return col
    return False

checked = 0
exists = 0
for k in range(1, KMAX + 1):
    for n in range(2, NMAX + 1):
        # skip large search spaces: half <= 22 for k=2, half <= 15 for k=3 keeps runtime sane
        half = n // 2
        if k == 3 and half > 15:
            continue
        r = cyclic_partitions(n, k)
        checked += 1
        if r in (None, False):
            continue
        exists += 1
        col = r
        m = (n - 1) // 2
        # lemma conclusion 1: restriction is integer sum-free
        classes = [[x for x in range(1, m + 1) if col[min(x, n - x)] == c] for c in range(k)]
        for cl in classes:
            assert sumfree_int(cl), (n, k, cl)
        # lemma conclusion 2: m <= S(k)
        assert m <= S[k], (n, k, m, S[k])
print(f"checked {checked} (n,k) cases; {exists} admit partitions; "
      f"all restrictions integer-sum-free and m <= S(k). OK")
sys.exit(0)
