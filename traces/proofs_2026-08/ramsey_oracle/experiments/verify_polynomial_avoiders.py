#!/usr/bin/env python3
"""Independent verification of explicit polynomial-hitting counterexamples."""
cases=[
 # p, S, coefficients c1,c2,... for f(x)=sum c_i x^i
 (5,{2,3},(0,1)),
 (7,{3,4},(1,1)),
 (11,{4,5,6,7},(1,0,1)),
 (13,{5,6,7,8},(0,1)),
]
for p,S,cs in cases:
 assert S=={(-x)%p for x in S}
 assert all((a+b)%p not in S for a in S for b in S)
 vals=[sum(c*pow(x,i+1,p) for i,c in enumerate(cs))%p for x in range(p)]
 assert not (set(vals)&S)
 print(p,cs,vals)
print('PASS: explicit nonzero degree<=3 polynomials avoid the stated symmetric sum-free sets')
