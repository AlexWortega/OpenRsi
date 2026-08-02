#!/usr/bin/env python3
"""Exact rational checks for the triangular scaled-intersection formula."""
from fractions import Fraction
# For u=(3-z)/4, barycentric clipping gives r=u^2-3(u-1/2)^2.
def r(z):
    u=(Fraction(3)-z)/4
    clipped=u*u-3*(u-Fraction(1,2))**2
    assert clipped==(Fraction(3)-z*z)/8
    return clipped
assert r(Fraction(0))==Fraction(3,8)
assert r(Fraction(1))==r(Fraction(-1))==Fraction(1,4)
# Integral from -1 to 1: (1/8)(6-2/3)=2/3. Pyramid volume / area(B)=4/3.
core=Fraction(2,3);pyramid=Fraction(4,3)
assert core/pyramid==Fraction(1,2)
print('triangle section ratio r(z)=(3-z^2)/8; centered tetrahedron core ratio',core/pyramid)
