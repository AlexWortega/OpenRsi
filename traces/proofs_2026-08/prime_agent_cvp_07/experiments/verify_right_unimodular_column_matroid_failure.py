#!/usr/bin/env python3
"""Exact counterexample: right-unimodular rebasing changes [I|-C]'s column matroid.

All arithmetic is over Fraction.  No optimization package or floating point is
used.  The universal fact that C and C Q have the same integer image is proved
separately in lean/Verify_right_unimodular_lattice_image.lean.
"""
from fractions import Fraction
from itertools import combinations


def matmul(a, b):
    assert len(a[0]) == len(b)
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def mulvec(a, x):
    return [sum((a[i][j] * x[j] for j in range(len(x))), Fraction(0))
            for i in range(len(a))]


def rank(a):
    """Exact Gaussian-elimination rank over Q."""
    if not a:
        return 0
    m = [[Fraction(x) for x in row] for row in a]
    rows, cols = len(m), len(m[0])
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if m[i][c]), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        q = m[r][c]
        m[r] = [x / q for x in m[r]]
        for i in range(rows):
            if i != r and m[i][c]:
                q = m[i][c]
                m[i] = [m[i][j] - q * m[r][j] for j in range(cols)]
        r += 1
        if r == rows:
            break
    return r


def take_columns(a, subset):
    return [[row[j] for j in subset] for row in a]


def circuits(a):
    """All inclusion-minimal dependent labeled column supports over Q."""
    n = len(a[0])
    out = []
    for size in range(1, n + 1):
        for s in combinations(range(n), size):
            if rank(take_columns(a, s)) == size:
                continue
            # Check every proper subset directly (not just deletions), so
            # inclusion-minimality itself is exhaustively machine checked.
            proper = (u for k in range(size) for u in combinations(s, k))
            if all(rank(take_columns(a, u)) == len(u) for u in proper):
                out.append(s)
    return tuple(out)


def main():
    Z = Fraction
    C = [[Z(1), Z(0)], [Z(0), Z(1)]]
    Q = [[Z(1), Z(1)], [Z(0), Z(1)]]
    P = [[Z(1), Z(-1)], [Z(0), Z(1)]]
    I = [[Z(1), Z(0)], [Z(0), Z(1)]]
    assert matmul(Q, P) == I and matmul(P, Q) == I

    CQ = matmul(C, Q)
    D = [[I[i][j] for j in range(2)] + [-C[i][j] for j in range(2)]
         for i in range(2)]
    DQ = [[I[i][j] for j in range(2)] + [-CQ[i][j] for j in range(2)]
          for i in range(2)]
    assert D == [[1, 0, -1, 0], [0, 1, 0, -1]]
    assert DQ == [[1, 0, -1, -1], [0, 1, 0, -1]]

    old_circuits = circuits(D)
    new_circuits = circuits(DQ)
    assert old_circuits == ((0, 2), (1, 3))
    assert new_circuits == ((0, 2), (0, 1, 3), (1, 2, 3))
    # Hence not even an unlabeled matroid isomorphism can relate them: their
    # multisets of circuit cardinalities differ.
    assert sorted(map(len, old_circuits)) == [2, 2]
    assert sorted(map(len, new_circuits)) == [2, 3, 3]

    # Concrete old circuit vector on support {y_2,z_2}; the same labeled
    # coefficient vector ceases even to be a dependency after rebasing.
    x = [Z(0), Z(1), Z(0), Z(1)]
    assert mulvec(D, x) == [0, 0]
    assert mulvec(DQ, x) == [-1, 0]

    print("PASS: exact right-unimodular column-matroid counterexample")
    print("old circuits:", old_circuits)
    print("new circuits:", new_circuits)


if __name__ == "__main__":
    main()
