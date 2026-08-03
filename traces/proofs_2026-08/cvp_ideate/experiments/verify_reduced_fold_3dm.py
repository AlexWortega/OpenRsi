#!/usr/bin/env python3
"""End-to-end exact 3DM -> pointed code -> two reduced Z3 folds.

This is the concrete self-renewing assembly from IDEATE round 2.  A 3DM
syndrome instance is repeated on three cyclic sheets with one shared star bit.
Reduced pointed tensoring deletes star-cross sectors; diagonal Z3 orbit parity
folds the moving square.  The residual phase-difference action is again free,
so the operation is iterated.  Every pointed image word is enumerated exactly.
"""
from __future__ import annotations

import itertools
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


def syndrome(q, triple):
    return (1 << triple[0]) | (1 << (q + triple[1])) | (1 << (2 * q + triple[2]))


def xor_cols(cols, x):
    y = 0
    for j, c in enumerate(cols):
        if (x >> j) & 1:
            y ^= c
    return y


def planted(q, m, seed):
    rng = random.Random(seed)
    diag = [(i, i, i) for i in range(q)]
    rest = [u for u in itertools.product(range(q), repeat=3) if u not in diag]
    rng.shuffle(rest)
    return diag + rest[:m-q]


def random_instance(q, m, seed):
    rng = random.Random(seed)
    all_t = list(itertools.product(range(q), repeat=3))
    rng.shuffle(all_t)
    return all_t[:m]


def single_fiber_data(q, triples):
    cols = [syndrome(q, u) for u in triples]
    target = (1 << (3*q)) - 1
    ker = [x for x in range(1 << len(cols)) if xor_cols(cols, x) == 0]
    fib = [x for x in range(1 << len(cols)) if xor_cols(cols, x) == target]
    assert fib
    kb = basis(ker)
    d = min(x.bit_count() for x in fib)
    return kb, min(fib, key=int.bit_count), d


def replicated_pointed_code(q, triples, g=3):
    kb, point, d = single_fiber_data(q, triples)
    m = len(triples)
    rows = []
    # Moving coordinate index = triple block j, phase h; bit 0 is star.
    for h in range(g):
        for z in kb:
            y = 0
            for j in range(m):
                if (z >> j) & 1:
                    y ^= 1 << (1 + j*g + h)
            rows.append(y)
    y = 1
    for h in range(g):
        for j in range(m):
            if (point >> j) & 1:
                y ^= 1 << (1 + j*g + h)
    rows.append(y)
    rows = basis(rows)
    assert pdist(rows) == 1 + g*d
    return rows, m, d


def shift(x, blocks, g):
    y = x & 1
    for b in range(blocks):
        for h in range(g):
            i = 1 + b*g + h
            if (x >> i) & 1:
                y ^= 1 << (1 + b*g + (h+1) % g)
    return y


def folded(rows, blocks, g=3):
    """Reduced diagonal fold; output blocks=(old blocks)^2 and phase=hj-hi."""
    length = 1 + blocks*g
    out = []
    for a in rows:
        sa = [i for i in range(1, length) if (a >> i) & 1]
        for b in rows:
            sb = [j for j in range(1, length) if (b >> j) & 1]
            y = (a & 1) & (b & 1)
            for i in sa:
                bi, hi = divmod(i-1, g)
                for j in sb:
                    bj, hj = divmod(j-1, g)
                    block = bi*blocks + bj
                    phase = (hj-hi) % g
                    y ^= 1 << (1 + block*g + phase)
            out.append(y)
    return basis(out), blocks*blocks


def run(label, q, triples, levels=2):
    rows, blocks, single_d = replicated_pointed_code(q, triples)
    records = [{"level": 0, "length": 1+3*blocks, "dim": len(rows),
                "moving_d": pdist(rows)-1}]
    expected = 3*single_d
    assert records[0]["moving_d"] == expected
    for level in range(1, levels+1):
        # Verify the residual cyclic action preserves the whole code.
        assert basis(rows + [shift(x, blocks, 3) for x in rows]) == basis(rows)
        rows, blocks = folded(rows, blocks)
        got = pdist(rows)-1
        expected = expected*expected//3
        assert got == expected  # invariant minimum word attains lower bound
        records.append({"level": level, "length": 1+3*blocks,
                        "dim": len(rows), "moving_d": got})
    return label, single_d, records


def main():
    q, m = 3, 8
    yes = planted(q, m, 17)
    no = random_instance(q, m, 10003)
    # The deterministic NO seed has an odd-cover fiber but no weight-q matching.
    assert single_fiber_data(q, no)[2] == 5
    assert single_fiber_data(q, yes)[2] == 3
    reports = [run("YES", q, yes), run("NO", q, no)]
    for r in reports:
        print(r)
    yr, nr = reports[0][2], reports[1][2]
    from fractions import Fraction
    for i in range(3):
        ratio = Fraction(nr[i]["moving_d"], yr[i]["moving_d"])
        assert ratio == Fraction(5, 3) ** (2**i)
        print({"level": i, "exact_NO/YES": str(ratio),
               "rank_proxy_length": yr[i]["length"]})
    print("End-to-end two-level reduced Z3 assembly passes exact enumeration.")


if __name__ == "__main__":
    main()
