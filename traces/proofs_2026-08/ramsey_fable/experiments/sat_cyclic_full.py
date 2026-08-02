#!/usr/bin/env python3
"""Full SAT for symmetric sum-free k-partition of Z_n \\ {0} (orbit variables).
SAT => triangle-free difference k-coloring of K_n => R_k(3) > n.
Usage: sat_cyclic_full.py n k
"""
import sys, json, time
from pysat.solvers import Cadical195

n, k = int(sys.argv[1]), int(sys.argv[2])
half = n // 2
def orb(x):
    x %= n
    return min(x, n - x)
def var(o, c): return (o - 1) * k + c + 1

cons = set()
selfbad = set()
for a in range(1, n):
    for b in range(a, n):
        c = (a + b) % n
        if c == 0:
            continue
        t = frozenset({orb(a), orb(b), orb(c)})
        if len(t) == 1:
            selfbad.add(orb(a))
        else:
            cons.add(t)
if selfbad:
    print(f"n={n}: structurally impossible ({len(selfbad)} self-bad orbits)", flush=True)
    sys.exit(0)
clauses = []
for o in range(1, half + 1):
    clauses.append([var(o, c) for c in range(k)])
    for c1 in range(k):
        for c2 in range(c1 + 1, k):
            clauses.append([-var(o, c1), -var(o, c2)])
for t in cons:
    for c in range(k):
        clauses.append([-var(o, c) for o in t])
print(f"n={n} k={k} orbits={half} cons={len(cons)} clauses={len(clauses)}", flush=True)
t0 = time.time()
s = Cadical195(bootstrap_with=clauses)
res = s.solve()
print(("SAT" if res else "UNSAT") + f" ({time.time()-t0:.0f}s)", flush=True)
if res:
    m = set(l for l in s.get_model() if l > 0)
    color = [-1] * n
    for o in range(1, half + 1):
        c = next(c for c in range(k) if var(o, c) in m)
        color[o] = c
        color[n - o] = c
    # inline full verify
    for a in range(1, n):
        for b in range(a, n):
            z = (a + b) % n
            if z and color[a] == color[b] == color[z]:
                raise AssertionError((a, b, z))
    classes = [[x for x in range(1, n) if color[x] == c] for c in range(k)]
    fn = f"experiments/cyclicfull_{n}_{k}.json"
    with open(fn, "w") as f:
        json.dump({"n": n, "k": k, "classes": classes}, f)
    print(f"SAT verified, base={n**(1/k):.5f}, written {fn}", flush=True)
