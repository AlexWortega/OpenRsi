#!/usr/bin/env python3
"""Exact checks of reduced pointed tensoring and free-orbit folding.

The reduced map keeps only (*,*) and the moving x moving tensor block, deleting
both star-cross sectors.  For any pointed code with affine moving distance d,
its reduced tensor image has pointed distance exactly 1+d^2.  If an odd group
acts freely on moving coordinates, orbit parity gives >=1+ceil(d^2/|G|).
This script enumerates every mixed image word for deterministic small codes.
"""
from __future__ import annotations

import random


def basis(rows):
    piv = {}
    for x in rows:
        while x:
            p = x.bit_length() - 1
            if p in piv:
                x ^= piv[p]
            else:
                for q, y in list(piv.items()):
                    if (y >> p) & 1:
                        piv[q] = y ^ x
                piv[p] = x
                break
    return [piv[p] for p in sorted(piv)]


def words(rows):
    for mask in range(1 << len(rows)):
        x = 0
        for i, r in enumerate(rows):
            if (mask >> i) & 1:
                x ^= r
        yield x


def pdist(rows):
    return min(x.bit_count() for x in words(rows) if x & 1)


def reduced_tensor(rows, length):
    """Generator on corner bit 0 plus ordered moving pairs."""
    out = []
    for a in rows:
        for b in rows:
            y = (a & 1) & (b & 1)
            for i in range(1, length):
                if (a >> i) & 1:
                    for j in range(1, length):
                        if (b >> j) & 1:
                            y ^= 1 << (1 + (i - 1) * (length - 1) + (j - 1))
            out.append(y)
    return basis(out), 1 + (length - 1) ** 2


def shift(x, blocks, g):
    y = x & 1
    for b in range(blocks):
        for h in range(g):
            i = 1 + b * g + h
            if (x >> i) & 1:
                y ^= 1 << (1 + b * g + (h + 1) % g)
    return y


def orbit_key(i, j, g):
    # Moving coordinates only; diagonal shift preserves block pair and phase diff.
    bi, hi = divmod(i - 1, g)
    bj, hj = divmod(j - 1, g)
    return bi, bj, (hj - hi) % g


def reduced_orbit_tensor(rows, length, g):
    assert (length - 1) % g == 0
    blocks = (length - 1) // g
    keys = [(bi, bj, d) for bi in range(blocks) for bj in range(blocks) for d in range(g)]
    idx = {k: 1 + z for z, k in enumerate(keys)}
    out = []
    for a in rows:
        for b in rows:
            y = (a & 1) & (b & 1)
            for i in range(1, length):
                if (a >> i) & 1:
                    for j in range(1, length):
                        if (b >> j) & 1:
                            y ^= 1 << idx[orbit_key(i, j, g)]
            out.append(y)
    return basis(out), 1 + blocks * blocks * g


def invariant_code(g, blocks, seed):
    rng = random.Random(seed)
    length = 1 + g * blocks
    rows = []
    for _ in range(rng.choice([1, 2])):
        x = 1 | (rng.randrange(1 << (length - 1)) << 1)
        for _ in range(g):
            rows.append(x)
            x = shift(x, blocks, g)
    return basis(rows), length


def main():
    rng = random.Random(424242)
    ordinary = []
    while len(ordinary) < 100:
        L = rng.choice([3, 4, 5, 6])
        rows = basis([1 | (rng.randrange(1 << (L - 1)) << 1) for _ in range(2)])
        if len(rows) <= 3:
            ordinary.append((rows, L))
    for rows, L in ordinary:
        d = pdist(rows) - 1
        rr, LL = reduced_tensor(rows, L)
        assert LL == 1 + (L - 1) ** 2
        assert pdist(rr) == 1 + d * d

    folded = []
    for seed in range(100):
        g = 3 if seed < 60 else 5
        blocks = 1 if seed % 3 else 2
        rows, L = invariant_code(g, blocks, 10000 + seed)
        # Check invariance explicitly.
        assert basis(rows + [shift(x, blocks, g) for x in rows]) == basis(rows)
        d = pdist(rows) - 1
        fr, FL = reduced_orbit_tensor(rows, L, g)
        got = pdist(fr)
        bound = 1 + (d * d + g - 1) // g
        assert got >= bound
        folded.append((g, blocks, len(rows), L, d, FL, got, bound))

    print(f"checked {len(ordinary)} exact reduced tensor codes: distance = 1+d^2")
    print(f"checked {len(folded)} exact free-orbit folds: distance >= 1+ceil(d^2/g)")
    for row in folded[:15]:
        print(row)


if __name__ == "__main__":
    main()
