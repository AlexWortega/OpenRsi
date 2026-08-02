#!/usr/bin/env python3
"""Dilation-invariant sum-free partitions of F_{2^d}^* .

Let g generate F_{2^d}^* (order n=2^d-1). Fix t | n and let H = subgroup of
order n/t (index t). Look for a partition of the t cosets g^i H (i mod t) into
k classes such that each class (union of cosets) is sum-free in F_{2^d}.

Constraint: for x=g^a, y=g^b distinct nonzero, z=x+y (z!=0 since char 2, x!=y),
z=g^c: the coset triple (a%t, b%t, c%t) must not be monochromatic.
SAT over t*k vars. SAT => triangle-free k-coloring of K_{2^d}: R_k(3) > 2^d.

Usage: coset_f2d.py d t k
"""
import sys, json, time
from pysat.solvers import Cadical195

d, t, k = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
n = 2**d - 1
assert n % t == 0

# GF(2^d) via primitive polynomial (conway-ish minimal weight primitive polys)
PRIM = {2:0b111, 3:0b1011, 4:0b10011, 5:0b100101, 6:0b1000011, 7:0b10000011,
        8:0b100011101, 9:0b1000010001, 10:0b10000001001, 11:0b100000000101,
        12:0b1000001010011, 13:0b10000000011011, 14:0b100010001000011,
        15:0b1000000000000011, 16:0b10001000000001011}
poly = PRIM[d]

def gmul2(a):  # multiply by x
    a <<= 1
    if a >> d:
        a ^= poly
    return a

# build discrete log table: g = x (must be primitive for chosen poly)
log = {}
val = 1
for i in range(n):
    assert val not in log, f"x not primitive for d={d}"
    log[val] = i
    val = gmul2(val)
assert val == 1

exp = [0] * n
for v, i in log.items():
    exp[i] = v

# constraint triples over Z_t
cons = set()
selfbad = set()
for a in range(n):
    x = exp[a]
    for b in range(a + 1, n):
        y = exp[b]
        z = x ^ y
        c = log[z]
        tri = frozenset({a % t, b % t, c % t})
        if len(tri) == 1:
            selfbad.add(a % t)
        else:
            cons.add(tri)

print(f"d={d} n={n} t={t} k={k} cosets_selfbad={len(selfbad)} cons={len(cons)}", flush=True)
if len(selfbad) == t:
    print("ALL cosets self-bad: impossible at this t", flush=True)
    sys.exit(0)

def var(i, c): return i * k + c + 1
clauses = []
for i in range(t):
    clauses.append([var(i, c) for c in range(k)])
    for c1 in range(k):
        for c2 in range(c1 + 1, k):
            clauses.append([-var(i, c1), -var(i, c2)])
if selfbad:
    print(f"self-bad cosets {sorted(selfbad)}: impossible (they can get no color)", flush=True)
    sys.exit(0)
for tri in cons:
    for c in range(k):
        clauses.append([-var(i, c) for i in tri])

t0 = time.time()
s = Cadical195(bootstrap_with=clauses)
res = s.solve()
print(("SAT" if res else "UNSAT") + f" ({time.time()-t0:.1f}s)", flush=True)
if res:
    m = set(l for l in s.get_model() if l > 0)
    assign = []
    for i in range(t):
        for c in range(k):
            if var(i, c) in m:
                assign.append(c)
    # inline full verify over all pairs
    for a in range(n):
        x = exp[a]
        ca = assign[a % t]
        for b in range(a + 1, n):
            if assign[b % t] != ca:
                continue
            c = log[x ^ exp[b]]
            assert assign[c % t] != ca, (a, b, c)
    print("inline full verify OK; coset assignment:", assign, flush=True)
    fn = f"experiments/coset_{d}_{t}_{k}.json"
    with open(fn, "w") as f:
        json.dump({"d": d, "t": t, "k": k, "poly": poly, "assign": assign}, f)
    print("written", fn, flush=True)
