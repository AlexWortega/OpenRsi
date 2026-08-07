#!/usr/bin/env python3
"""Exact finite breaker for a target-programmed linear 2x2 switch serializer.

This does NOT claim that every future serializer has these columns.  It certifies
the mandatory collision that occurs if one numerical linear factor contains the
four unit-input words of both straight and crossed modes, while the mode is only
metadata/a target bit.
"""
from itertools import product
from math import gcd
from functools import reduce
import hashlib, json

# Port order is (input0,input1,output0,output1).
straight0 = (1,0,1,0)
straight1 = (0,1,0,1)
crossed0  = (1,0,0,1)
crossed1  = (0,1,1,0)
cols = (straight0, straight1, crossed0, crossed1)
C = tuple(tuple(cols[j][i] for j in range(4)) for i in range(4))

def mv(A, x):
    return tuple(sum(a*b for a,b in zip(row,x)) for row in A)

def sub(x,y): return tuple(a-b for a,b in zip(x,y))
def add(x,y): return tuple(a+b for a,b in zip(x,y))
def supp(x): return sum(a != 0 for a in x)
def dot(x,y): return sum(a*b for a,b in zip(x,y))

# Both modes obey the only common port conservation equation.
conservation = (-1,-1,1,1)
assert all(dot(conservation,c) == 0 for c in cols)

# Honest-affine collision: the two straight unit words and the two crossed
# unit words have exactly the same sum.
assert add(straight0,straight1) == (1,1,1,1)
assert add(crossed0,crossed1) == (1,1,1,1)
q = (1,1,-1,-1)
assert mv(C,q) == (0,0,0,0)
assert reduce(gcd,(abs(a) for a in q),0) == 1
assert supp(q) == 4

# Exact bounded enumeration: this is the unique relation up to sign among
# coefficient vectors in {-1,0,1}^4, and no support <= 3 relation exists.
rels = []
for z in product((-1,0,1), repeat=4):
    if z != (0,0,0,0) and mv(C,z) == (0,0,0,0): rels.append(z)
assert rels == [(-1,-1,1,1),(1,1,-1,-1)]
assert min(map(supp, rels)) == 4

# Subtracting one honest mode response from the other produces a two-port
# signed flow with zero inputs and nonzero opposite outputs.
ghost = sub(straight0,crossed0)
assert ghost == (0,0,1,-1)
assert ghost[:2] == (0,0) and ghost[2:] != (0,0)
assert dot(conservation,ghost) == 0
assert sum(a*a for a in ghost) == 2

# Changing only target/mark metadata cannot alter the numerical matrix or its
# signed relation.  Canonical numerical hashes are identical for two programs.
def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
straight_instance = {'C':C, 'target_program':0, 'column_marks':['S0','S1','X0','X1']}
crossed_instance  = {'C':C, 'target_program':1, 'column_marks':['S0','S1','X0','X1']}
assert digest(straight_instance['C']) == digest(crossed_instance['C'])
assert mv(straight_instance['C'],q) == mv(crossed_instance['C'],q) == (0,0,0,0)

print('verified target-only 2x2-switch span cheat')
print('C_sha256',digest(C))
print('primitive coefficient kernel',q,'support',supp(q))
print('zero-input signed port ghost',ghost,'squared_norm',sum(a*a for a in ghost))
print('scope: applies when the common numerical factor contains all four mode words')
