#!/usr/bin/env python3
"""Exact numerical identities used in proof_ehrhart.md."""
from fractions import Fraction
from math import factorial


def A(n):
    return Fraction((n + 1) ** n, factorial(n)) if n else Fraction(1)


for n in range(1, 301):
    assert 2**n <= A(n)
    if n >= 2:
        assert A(n) / A(n - 1) == Fraction((n + 1) ** n, n**n)
        assert 2 * A(n - 1) <= A(n)

for n in range(2, 101):
    for m in range(1, n):
        r = n - m
        assert A(m) * A(r) <= A(n)
        assert 2**r * A(m) <= A(n)

assert A(3) == Fraction(32, 3)
assert A(4) / A(2) ** 2 == Fraction(625, 486)

print("Ehrhart constants checked through dimension 300")
print("all two-block splits checked through dimension 100")
print("A3 =", A(3), "; A4/A2^2 =", A(4) / A(2) ** 2)
