#!/usr/bin/env python3
"""Dilation-invariant symmetric sum-free k-partitions of Z_p \\ {0}, p prime.

Fix subgroup H <= Z_p^* of order m (need m even so -1 in H), index t=(p-1)/m.
Color classes = unions of cosets g^i H. Constraints (dilation-reduced):
for each coset rep x=g^i (i<t), each y != 0, -x: triple (cls(x),cls(y),cls(x+y))
must not be monochromatic; also 2x vs x (a=b case) is included since y=x allowed.
SAT over t*k variables => triangle-free difference k-coloring of K_p:
R_k(3) > p, per-color base p^{1/k}. Beat 3.19963 needs p>=1076 (k=6), p>=3434 (k=7).

Usage: coset_zp.py k pmin pmax [tmax]
"""
import sys, json, time
from sympy import isprime, primitive_root
from pysat.solvers import Cadical195

k = int(sys.argv[1]); pmin = int(sys.argv[2]); pmax = int(sys.argv[3])
tmax = int(sys.argv[4]) if len(sys.argv) > 4 else 120

def try_pt(p, t):
    g = primitive_root(p)
    m = (p - 1) // t
    if m % 2:
        return None  # -1 not in H, classes not symmetric
    # coset index of x: dlog(x) mod t. build dlog table
    dlog = [0] * p
    val = 1
    for i in range(p - 1):
        dlog[val] = i
        val = val * g % p
    cls = [0] * p  # coset index (only nonzero meaningful)
    for x in range(1, p):
        cls[x] = dlog[x] % t
    # constraints
    cons = set()
    selfbad = False
    # reps x = g^i, i < t
    reps = []
    val = 1
    for i in range(t):
        reps.append(val)
        val = val * g % p
    for i, x in enumerate(reps):
        for y in range(1, p):
            z = (x + y) % p
            if z == 0:
                continue
            tri = frozenset({i, cls[y], cls[z]})
            if len(tri) == 1:
                selfbad = True
                break
            cons.add(tri)
        if selfbad:
            break
    if selfbad:
        return None
    def var(i, c): return i * k + c + 1
    clauses = []
    for i in range(t):
        clauses.append([var(i, c) for c in range(k)])
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                clauses.append([-var(i, c1), -var(i, c2)])
    for tri in cons:
        for c in range(k):
            clauses.append([-var(i, c) for i in tri])
    s = Cadical195(bootstrap_with=clauses)
    if not s.solve():
        return False
    mdl = set(l for l in s.get_model() if l > 0)
    assign = [next(c for c in range(k) if var(i, c) in mdl) for i in range(t)]
    # full inline verify: all pairs a<b in classes, a+b check; symmetric check
    color = [ -1 ] * p
    for x in range(1, p):
        color[x] = assign[cls[x]]
    for x in range(1, p):
        assert color[x] == color[p - x]
    for a in range(1, p):
        ca = color[a]
        for b in range(a, p):
            if color[b] != ca:
                continue
            z = (a + b) % p
            if z and color[z] == ca:
                raise AssertionError((p, t, a, b, z))
    return assign, color

for p in range(pmin, pmax + 1):
    if not isprime(p):
        continue
    divs = sorted(d for d in range(2, tmax + 1) if (p - 1) % d == 0)
    for t in divs:
        t0 = time.time()
        r = try_pt(p, t)
        if r is None:
            continue
        if r is False:
            print(f"p={p} t={t}: UNSAT ({time.time()-t0:.1f}s)", flush=True)
            continue
        assign, color = r
        base = p ** (1 / k)
        print(f"p={p} t={t}: SAT!!! base={base:.5f} assign={assign}", flush=True)
        classes = [[x for x in range(1, p) if color[x] == c] for c in range(k)]
        fn = f"experiments/cosetzp_{p}_{k}_{t}.json"
        with open(fn, "w") as f:
            json.dump({"p": p, "k": k, "t": t, "assign": assign,
                       "classes": classes}, f)
        print("written", fn, flush=True)
