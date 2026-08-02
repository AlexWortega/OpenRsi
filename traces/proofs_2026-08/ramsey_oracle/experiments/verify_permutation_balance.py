#!/usr/bin/env python3
"""Finite sanity check for the constant-composition permutation blow-up lemma."""
from itertools import product
from collections import Counter, defaultdict

# H=K2, all binary words of length 4 are H-separated: distinct words differ
# somewhere, and 0--1 is the unique edge.
m = 4
words = list(product(range(2), repeat=m))
classes = defaultdict(list)
for w in words:
    classes[tuple(Counter(w)[v] for v in range(2))].append(w)
assert len(classes) == 5  # <= binom(m+q-1,q-1)=5
C = max(classes.values(), key=len)
assert len(C) == 6
r = tuple(Counter(C[0])[v] for v in range(2))
assert r == (2, 2)

def lift(w):
    seen = [0, 0]
    out = []
    for v in w:
        seen[v] += 1
        out.append((v, seen[v]))
    return tuple(out)

F = [lift(w) for w in C]
vertices = {(v, a) for v in range(2) for a in range(1, r[v] + 1)}
for pi in F:
    assert set(pi) == vertices and len(pi) == m
for i, pi in enumerate(F):
    for sigma in F[i+1:]:
        assert any(pi[j][0] != sigma[j][0] for j in range(m))
print("PASS: K2 length-4 constant-composition class lifts to 6 separated permutations")
