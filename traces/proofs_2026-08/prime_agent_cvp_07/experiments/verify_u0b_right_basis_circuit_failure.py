#!/usr/bin/env python3
"""Finite right-basis counterexample to a basis-column-circuit U0b invariant.

I_n and the unimodular cumulative Q_n generate the same lattice Z^n.  The
systematic matrices [I|-I] and [I|-Q] nevertheless have different explicit
minimal column dependencies: the z_0 fundamental circuit has support 2 in the
first presentation and n+1 in the second.  Thus integral column circuits of D
are invariant under equality-row changes and column permutations, but not
under semantically free right-unimodular lattice-basis changes C -> C Q.
"""
from itertools import chain
SIZES=(8,16,32)
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def cumulative(n):return [[int(j<=i) for j in range(n)] for i in range(n)]
def difference(n):return [[int(i==j)-int(i==j+1) for j in range(n)] for i in range(n)]
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def mv(a,x):return [sum(v*w for v,w in zip(row,x)) for row in a]
def aug(c):
 n=len(c);return [eye(n)[i]+[-v for v in c[i]] for i in range(n)]
def supp(x):return sum(v!=0 for v in x)
records=[]
for n in SIZES:
 I=eye(n);Q=cumulative(n);V=difference(n)
 assert mm(Q,V)==I and mm(V,Q)==I
 # Exact image equality witnesses: Q(Vx)=x and V(Qx)=x for every coordinate,
 # certified here as the two matrix identities above.
 DI,DQ=aug(I),aug(Q)
 z=[1]+[0]*(n-1)
 xI=mv(I,z)+z;xQ=mv(Q,z)+z
 assert mv(DI,xI)==[0]*n and mv(DQ,xQ)==[0]*n
 assert supp(xI)==2 and supp(xQ)==n+1
 # Minimality certificate for xQ: its selected y columns are the entire
 # identity basis and z0 is -ones.  If any selected y_i is omitted, row i
 # forces the z0 coefficient to zero, after which every y coefficient is zero.
 assert [Q[i][0] for i in range(n)]==[1]*n
 for omitted in range(n):
  # Machine-check the forcing row has no other selected nonidentity column.
  assert DQ[omitted][n]==-1
  assert all(DQ[omitted][j]==int(omitted==j) for j in range(n))
 # Omitting z0 leaves an identity-column subset, also independent.
 records.append({'n':n,'same_lattice_inverse_verified':True,
   'identity_fundamental_circuit_support':supp(xI),
   'cumulative_fundamental_circuit_support':supp(xQ),
   'cumulative_circuit_minimality_forcing_rows':n})
print('right-basis column-circuit counterexample: PASS')
for r in records:print(r)
print('scope: kills chosen-basis circuit support as a lattice-intrinsic U0b invariant; no fixed-class membership claim')
