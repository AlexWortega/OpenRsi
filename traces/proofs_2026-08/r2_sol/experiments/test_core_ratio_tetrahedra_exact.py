#!/usr/bin/env python3
# Question: is vol(T intersect -T)/vol(T)=1/2 exactly for every centroid-zero tetrahedron, independent of shape?
from fractions import Fraction
# Affine invariance reduces every centered tetrahedron to the sharp coordinate simplex.
# In barycentric coordinates lambda_i>=0,sum lambda=1, reflection sends
# lambda_i -> 1/2-lambda_i. Inclusion-exclusion for lambda_i<=1/2:
r=sum(Fraction((-1)**j,1)*(__import__('math').comb(4,j))*Fraction((4-2*j)**3,4**3) for j in range(3))
assert r==Fraction(1,2)
print('exact centered-tetrahedron core ratio:',r)
