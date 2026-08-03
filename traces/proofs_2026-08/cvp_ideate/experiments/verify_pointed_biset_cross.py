#!/usr/bin/env python3
"""Exact pointed-biset test: fresh symmetry versus the unavoidable star cross.

U = {*} disjoint (Ru copies of the regular right G-set).
V = {*} disjoint (Rv copies of the regular (G,H)-biset GxH).
The balanced product U x_G V spends G and retains a fresh independent right
H-action.  In this specific product bitorsor, right H cannot be compensated by
left G on [*,v].  We enumerate quotient classes, verify that H is free off the
classes [u,*], and count the fixed cross sector.  No count is claimed for
arbitrary bitorsors where left/right actions may overlap.  This is the smallest concrete test of the
symmetry-renewal mechanism suggested by the classical biset literature.
"""
from __future__ import annotations


def add(x, a, n):
    return (x + a) % n


def elements_U(g: int, ru: int):
    return [("s",)] + [("u", copy, x) for copy in range(ru) for x in range(g)]


def elements_V(g: int, h: int, rv: int):
    return [("s",)] + [
        ("v", copy, x, y)
        for copy in range(rv) for x in range(g) for y in range(h)
    ]


def right_G_U(u, a, g):
    return u if u[0] == "s" else ("u", u[1], add(u[2], a, g))


def left_G_V(v, a, g):
    return v if v[0] == "s" else ("v", v[1], add(v[2], a, g), v[3])


def right_H_V(v, b, h):
    return v if v[0] == "s" else ("v", v[1], v[2], add(v[3], b, h))


def quotient(g: int, h: int, ru: int, rv: int):
    U, V = elements_U(g, ru), elements_V(g, h, rv)
    pairs = [(u, v) for u in U for v in V]
    unseen = set(pairs)
    orbits = []
    owner = {}
    while unseen:
        p = next(iter(unseen))
        u, v = p
        orb = {
            (right_G_U(u, a, g), left_G_V(v, -a, g))
            for a in range(g)
        }
        idx = len(orbits)
        for z in orb:
            owner[z] = idx
        unseen -= orb
        orbits.append(orb)
    return U, V, orbits, owner


def run(g: int, h: int, ru: int, rv: int):
    U, V, O, owner = quotient(g, h, ru, rv)
    # Induced fresh H action on quotient classes.
    perms = []
    for b in range(h):
        p = []
        for orb in O:
            u, v = next(iter(orb))
            p.append(owner[(u, right_H_V(v, b, h))])
        assert sorted(p) == list(range(len(O)))
        perms.append(p)

    fixed_nonidentity = {
        b: [i for i, j in enumerate(perms[b]) if i == j]
        for b in range(1, h)
    }
    # Precisely the quotient classes represented by (u, star_V) are fixed.
    expected = {owner[(u, ("s",))] for u in U}
    # Moving regular U elements collapse to ru G-orbits, plus the star.
    assert len(expected) == 1 + ru
    assert all(set(v) == expected for v in fixed_nonidentity.values())

    # Every nonfixed coordinate lies in a free H-orbit for prime h (we test
    # primes below), so fresh symmetry really is renewed away from the cross.
    moved = set(range(len(O))) - expected
    for i in moved:
        assert len({perms[b][i] for b in range(h)}) == h

    # Burnside/size accounting.  There is one singleton (*,*), ru classes in
    # U_moving x {*}, rv*h classes in {*} x V_moving, and ru*rv*g*h classes in
    # moving x moving.
    predicted = 1 + ru + rv * h + ru * rv * g * h
    assert len(O) == predicted
    return {
        "G": g, "H": h, "Ru": ru, "Rv": rv,
        "raw_pairs": len(U) * len(V), "quotient": len(O),
        "fresh_H_fixed": len(expected), "fresh_H_moving": len(moved),
    }


def main():
    reports = []
    for g in [3, 5, 7]:
        for h in [3, 5, 7]:
            for ru in [1, 2, 3]:
                for rv in [1, 2]:
                    reports.append(run(g, h, ru, rv))
    print(f"checked {len(reports)} pointed biset products exactly")
    for r in reports[:12]:
        print(r)
    print("Fresh symmetry is free off the unavoidable U x {star_V} cross sector.")


if __name__ == "__main__":
    main()
