#!/usr/bin/env python3
"""A CRT-global integer CVP encoding and its exact-fiber false-clause cheat.

This deliberately hostile prototype asks whether one global CRT integer can make
local Boolean extrapolations expensive.  It cannot: the usual clause slack
repair remains exact and costs only 8 in squared distance, independently of all
constraint scales.  Charging the global CRT integer also creates a huge YES
baseline.
"""
from __future__ import annotations

from math import prod, sqrt
import numpy as np


def first_odd_primes(n: int) -> list[int]:
    out: list[int] = []
    x = 5
    while len(out) < n:
        if all(x % p for p in range(2, int(sqrt(x)) + 1)):
            out.append(x)
        x += 2
    return out


def crt(bits: list[int], primes: list[int]) -> int:
    """Unique x in [0,P) with x == bits[i] mod primes[i]."""
    P = prod(primes)
    x = 0
    for b, p in zip(bits, primes):
        Pi = P // p
        x = (x + b * Pi * pow(Pi, -1, p)) % P
    return x


def all_eight_core() -> list[tuple[int, int, int]]:
    """Clauses indexed by their unique falsifying 3-bit assignment.

    Literal +(i+1) means x_i; -(i+1) means not x_i.
    """
    clauses = []
    for u in range(8):
        bits = [(u >> i) & 1 for i in range(3)]
        clauses.append(tuple((i + 1) if bits[i] == 0 else -(i + 1) for i in range(3)))
    return clauses


def instance(D: int) -> tuple[int, list[tuple[int, int, int]], list[int]]:
    clauses = all_eight_core()
    bits = [0, 0, 0]
    for j in range(D):
        base = 3 + 3 * j
        clauses.append((base + 1, base + 2, base + 3))
        bits.extend([1, 1, 1])
    return len(bits), clauses, bits


def literal_sum(clause: tuple[int, int, int], bits: list[int]) -> int:
    return sum(bits[lit - 1] if lit > 0 else 1 - bits[-lit - 1] for lit in clause)


def build(D: int, M: int = 10**6):
    """Return integer basis B, target t, explicit cheating coefficients z.

    Coefficients are z=(x,q_1..q_n,b_1..b_n,s_1,t_1,...,s_m,t_m).
    Rows are scaled CRT equations, scaled clause equations, centered identity
    rows for b/slacks, and one global row 2x centered at P.
    """
    n, clauses, bits = instance(D)
    m = len(clauses)
    primes = first_odd_primes(n)
    P = prod(primes)
    x = crt(bits, primes)
    q = [(x - b) // p for b, p in zip(bits, primes)]

    N = 1 + n + n + 2 * m
    ix = 0
    iq = 1
    ib = 1 + n
    isl = 1 + 2 * n
    rows: list[list[int]] = []
    target: list[int] = []

    def add(coeffs: dict[int, int], rhs: int):
        row = [0] * N
        for j, a in coeffs.items():
            row[j] = a
        rows.append(row)
        target.append(rhs)

    # x-p_i q_i-b_i=0.
    for i, p in enumerate(primes):
        add({ix: M, iq + i: -M * p, ib + i: -M}, 0)

    # true-literal count + s + 2t = 4.
    for j, clause in enumerate(clauses):
        c: dict[int, int] = {isl + 2 * j: M, isl + 2 * j + 1: 2 * M}
        const = 0
        for lit in clause:
            if lit > 0:
                c[ib + lit - 1] = c.get(ib + lit - 1, 0) + M
            else:
                const += 1
                c[ib - lit - 1] = c.get(ib - lit - 1, 0) - M
        add(c, M * (4 - const))

    # Center every Boolean/slack coefficient at 1/2 after multiplying by 2.
    for i in range(n):
        add({ib + i: 2}, 1)
    for j in range(2 * m):
        add({isl + j: 2}, 1)

    # This row is needed for injectivity: otherwise x -> x+P and the induced
    # q shifts give a nonzero coefficient-kernel direction.
    add({ix: 2}, P)

    z = [0] * N
    z[ix] = x
    z[iq:iq + n] = q
    z[ib:ib + n] = bits
    violated = []
    for j, clause in enumerate(clauses):
        h = literal_sum(clause, bits)
        if h == 0:
            s, tt = 0, 2                 # exact forbidden repair
            violated.append(j)
        else:
            s, tt = {1: (1, 1), 2: (0, 1), 3: (1, 0)}[h]
        z[isl + 2 * j] = s
        z[isl + 2 * j + 1] = tt

    return np.asarray(rows, dtype=object), np.asarray(target, dtype=object), np.asarray(z, dtype=object), {
        'D': D, 'n': n, 'm': m, 'M': M, 'P': P, 'x': x,
        'violated': violated, 'yes_uniform_upper_squared': P * P + n + 2 * m,
    }


def run(D_values=(0, 1, 4, 10), M=10**6):
    records = []
    for D in D_values:
        B, t, z, info = build(D, M)
        residual = B @ z - t
        sq = sum(int(v) ** 2 for v in residual)
        baseline = info['yes_uniform_upper_squared']
        assert info['violated'] == [0]
        assert sq == (2 * info['x'] - info['P']) ** 2 + info['n'] + 2 * info['m'] + 8
        records.append({
            **info, 'shape': B.shape, 'structural_full_column_rank': True,
            'cheat_squared': sq, 'additive_false_clause_cost': 8,
            'ratio_to_uniform_yes_radius_upper': sqrt((baseline + 8) / baseline),
        })
    print(records)
    return records


if __name__ == '__main__':
    run()
