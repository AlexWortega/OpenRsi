#!/usr/bin/env python3
# Question: what is the exact central-core volume ratio for the centered simplex in dimensions 1..12?
from fractions import Fraction
from math import comb,factorial
# In barycentric coordinates lambda_i>=0, sum lambda_i=1. Reflection about the
# centroid sends lambda_i to 2/(n+1)-lambda_i. Thus K cap -K is the simplex
# distribution clipped by lambda_i<=2/(n+1). Inclusion-exclusion gives ratio.
for n in range(1,13):
 m=n+1;ratio=sum(Fraction((-1)**j*comb(m,j)*(m-2*j)**n,m**n) for j in range(m//2+1))
 print(n,ratio,float(ratio))
