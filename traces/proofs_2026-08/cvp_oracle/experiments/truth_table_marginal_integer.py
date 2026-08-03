#!/usr/bin/env python3
"""Full 3-clause truth tables with integer unary marginals: exact 3-column fault.

This is the natural full-degree local escape from the GF(2) cube relation.
Integer coefficients do not make the local table integral: a forbidden singleton
boundary has the signed legal decomposition 000 = 001 + 010 - 011 (translated
as needed), with coverage and every unary marginal preserved.
"""
from __future__ import annotations
from itertools import product
import numpy as np

BITS = list(product((0, 1), repeat=3))


def build():
    meta = []
    idx = {}
    for i in range(3):
        for b in (0, 1):
            idx['v', i, b] = len(meta); meta.append(('v', i, b))
    for forbidden in BITS:
        for a in BITS:
            if a != forbidden:
                idx['c', forbidden, a] = len(meta); meta.append(('c', forbidden, a))
    rows = []
    target = []
    def add(entries, rhs):
        r = [0] * len(meta)
        for j, v in entries:
            r[j] += v
        rows.append(r); target.append(rhs)
    for i in range(3):
        add([(idx['v', i, b], 1) for b in (0, 1)], 1)
    for forbidden in BITS:
        add([(idx['c', forbidden, a], 1) for a in BITS if a != forbidden], 1)
        for i in range(3):
            for b in (0, 1):
                entries = [(idx['v', i, b], 1)]
                entries += [(idx['c', forbidden, a], -1) for a in BITS if a != forbidden and a[i] == b]
                add(entries, 0)
    return np.asarray(rows, dtype=object), np.asarray(target, dtype=object), meta


def explicit_witness(assignment=(0, 0, 1)):
    A, t, meta = build(); idx = {m:i for i,m in enumerate(meta)}
    z = np.zeros(len(meta), dtype=object)
    for i, b in enumerate(assignment): z[idx['v', i, b]] = 1
    for forbidden in BITS:
        if forbidden != assignment:
            z[idx['c', forbidden, assignment]] = 1
        else:
            # Flip coordinates 1 and 2: a+b-c = forbidden.
            a = (assignment[0], 1-assignment[1], assignment[2])
            b = (assignment[0], assignment[1], 1-assignment[2])
            c = (assignment[0], 1-assignment[1], 1-assignment[2])
            assert all(v != forbidden for v in (a,b,c))
            z[idx['c', forbidden, a]] = 1
            z[idx['c', forbidden, b]] = 1
            z[idx['c', forbidden, c]] = -1
    return A, t, z, meta


def run():
    records=[]
    for assignment in BITS:
        A,t,z,meta=explicit_witness(assignment)
        records.append({'assignment':assignment,'shape':A.shape,'support':int(np.count_nonzero(z)),
                        'l1':int(sum(abs(int(x)) for x in z)),'squared_norm':int(sum(int(x)**2 for x in z)),
                        'exact':bool(np.all(A@z==t))})
    print(records)
    return records

if __name__=='__main__':run()
