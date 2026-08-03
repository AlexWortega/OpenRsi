#!/usr/bin/env python3
"""Exact construction search: cyclic-ideal pointed codes with compressed squares.

For every binary cyclic code C=<g> of odd length ell<=31 whose dimension is at
most 16, use the invariant parity functional as star form:
    D={(sum(u),u): u in C}.
The pointed moving distance d is the minimum odd weight in C.  Reduced diagonal
orbit folding maps u tensor v to cyclic correlation
    corr(u,v)[a] = sum_i u_i v_{i+a}.
We enumerate every mixed word in the span of all correlations and compute its
minimum odd-star moving distance d'.  This is a structured-autocorrelation
mutation of I07, not a no-go theorem.
"""
from __future__ import annotations

import itertools
from sympy import Poly, symbols, factor_list

x = symbols("x")


def bits_from_poly(p: Poly) -> int:
    out = 0
    for (e,), c in p.terms():
        if int(c) & 1:
            out |= 1 << e
    return out


def mul_poly_bits(a: int, b: int) -> int:
    out = 0
    while b:
        lb = b & -b
        out ^= a << (lb.bit_length() - 1)
        b ^= lb
    return out


def basis(rows: list[int]) -> list[int]:
    piv: dict[int, int] = {}
    for z in rows:
        while z:
            p = z.bit_length() - 1
            if p in piv:
                z ^= piv[p]
            else:
                for q, y in list(piv.items()):
                    if (y >> p) & 1:
                        piv[q] = y ^ z
                piv[p] = z
                break
    return [piv[p] for p in sorted(piv)]


def words(rows: list[int]):
    for mask in range(1 << len(rows)):
        z = 0
        for i, r in enumerate(rows):
            if (mask >> i) & 1:
                z ^= r
        yield z


def correlation(a: int, b: int, ell: int) -> int:
    out = 0
    for shift in range(ell):
        bit = 0
        for i in range(ell):
            bit ^= ((a >> i) & 1) & ((b >> ((i + shift) % ell)) & 1)
        out |= bit << shift
    return out


def cyclic_generators(gbits: int, ell: int, degree: int) -> list[int]:
    # Since g divides x^ell+1, shifts x^i g for i<ell-degree are independent
    # without wraparound and generate the ideal.
    return basis([gbits << i for i in range(ell - degree)])


def all_divisor_generators(ell: int):
    poly = Poly(x**ell + 1, x, modulus=2)
    _, factors = factor_list(poly, modulus=2)
    expanded = []
    for f, multiplicity in factors:
        assert multiplicity == 1  # ell odd, so square-free over F2
        expanded.append(Poly(f, x, modulus=2))
    for choose in itertools.product((0, 1), repeat=len(expanded)):
        g = Poly(1, x, modulus=2)
        label = []
        for take, f in zip(choose, expanded):
            if take:
                g *= f
                label.append(str(f.as_expr()))
        yield g, " * ".join(label) if label else "1"


def analyze(ell: int, g: Poly, label: str):
    degree = g.degree()
    dim = ell - degree
    if dim <= 0 or dim > 16:
        return None
    rows = cyclic_generators(bits_from_poly(g), ell, degree)
    assert len(rows) == dim
    odd = [u for u in words(rows) if u.bit_count() & 1]
    if not odd:
        return None
    d = min(u.bit_count() for u in odd)

    # A reduced tensor generator has star bit parity(a)parity(b), and moving
    # block corr(a,b).  Include the star as bit ell.
    folded_rows = basis([
        correlation(a, b, ell) | (((a.bit_count() & 1) & (b.bit_count() & 1)) << ell)
        for a in rows for b in rows
    ])
    if len(folded_rows) > 22:
        return None
    pointed = [z & ((1 << ell) - 1) for z in words(folded_rows) if (z >> ell) & 1]
    assert pointed
    dp = min(v.bit_count() for v in pointed)
    lower = (d*d + ell - 1) // ell
    assert dp >= lower
    return {
        "ell": ell, "generator": label, "dim": dim, "fold_dim": len(folded_rows),
        "d": d, "dprime": dp, "lower": lower,
        "superbudget": ell > d > 1,
        "at_lower": dp == lower,
        "compression": (d*d, dp),
    }


def main() -> None:
    reports = []
    for ell in range(3, 32, 2):
        for g, label in all_divisor_generators(ell):
            r = analyze(ell, g, label)
            if r is not None:
                reports.append(r)
    assert reports
    candidates = [r for r in reports if r["superbudget"]]
    compressed = [r for r in candidates if r["dprime"] < r["d"] ** 2]
    floor_hits = [r for r in candidates if r["at_lower"]]
    print(f"checked {len(reports)} exact cyclic ideal/star-form constructions")
    print(f"nontrivial super-budget ell>d>1: {len(candidates)}")
    print(f"compressed below d^2: {len(compressed)}; attained floor: {len(floor_hits)}")
    print("best candidates:")
    for r in sorted(candidates, key=lambda z: (z["dprime"]/(z["d"]**2), z["ell"]))[:30]:
        print(r)
    # Exact deterministic finite claims used in STATUS/IDEAS.
    assert (len(reports),len(candidates),len(compressed),len(floor_hits)) == (116,94,94,0)


if __name__ == "__main__":
    main()
