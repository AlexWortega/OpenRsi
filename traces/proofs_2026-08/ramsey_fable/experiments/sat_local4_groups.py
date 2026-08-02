#!/usr/bin/env python3
"""SAT for locally-4 triangle-free K_N with g=5 global colors, via missing-color groups.

Structure: partition vertices into 5 groups; group i's vertices never see color i
(palette subset of the other 4). Edge (u,v) with u in group i, v in group j may use
any color not in {i,j}. Constraint: no monochromatic triangle. This automatically
gives a locally-4 coloring. N=62 would prove L_4 >= 62 > R_4(3)-1 (<=61).

Usage: sat_local4_groups.py N [sizes-comma-separated] [timeout: none]
"""
import sys, json, time, itertools
from pysat.solvers import Cadical195
from pysat.formula import IDPool

N = int(sys.argv[1])
if len(sys.argv) > 2 and "," in sys.argv[2]:
    sizes = [int(x) for x in sys.argv[2].split(",")]
    assert sum(sizes) == N and len(sizes) == 5
else:
    q, r = divmod(N, 5)
    sizes = [q + 1] * r + [q] * (5 - r)

group = []
for i, s in enumerate(sizes):
    group += [i] * s
print(f"N={N} sizes={sizes}", flush=True)

pool = IDPool()
def xe(u, v, c):
    if u > v: u, v = v, u
    return pool.id(("e", u, v, c))

def dom(u, v):
    return [c for c in range(5) if c != group[u] and c != group[v]]

clauses = []
for u, v in itertools.combinations(range(N), 2):
    vs = [xe(u, v, c) for c in dom(u, v)]
    clauses.append(vs)
    for p, q2 in itertools.combinations(vs, 2):
        clauses.append([-p, -q2])
for u, v, w in itertools.combinations(range(N), 3):
    common = set(dom(u, v)) & set(dom(u, w)) & set(dom(v, w))
    for c in common:
        clauses.append([-xe(u, v, c), -xe(u, w, c), -xe(v, w, c)])

print(f"vars={pool.top} clauses={len(clauses)}", flush=True)
t0 = time.time()
s = Cadical195(bootstrap_with=clauses)
res = s.solve()
print(("SAT" if res else "UNSAT") + f" ({time.time()-t0:.1f}s)", flush=True)
if res:
    m = set(l for l in s.get_model() if l > 0)
    coloring = {}
    for u, v in itertools.combinations(range(N), 2):
        for c in dom(u, v):
            if xe(u, v, c) in m:
                coloring[f"{u},{v}"] = c
    fn = f"experiments/local4_g5_N{N}.json"
    with open(fn, "w") as f:
        json.dump({"N": N, "sizes": sizes, "group": group, "edges": coloring}, f)
    print("written", fn, flush=True)
