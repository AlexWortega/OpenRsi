#!/usr/bin/env python3
"""SAT for locally-4 triangle-free K_N with g global colors (g<=7 so all
4-subsets pairwise intersect). Vertices are assigned fixed 4-subset palettes
in balanced round-robin over all C(g,4) types (or over types containing a
common structure). Edge (u,v) colored from P_u cap P_v; no mono triangle.

Usage: sat_local4_g.py N g
"""
import sys, json, time, itertools
from pysat.solvers import Cadical195
from pysat.formula import IDPool

N = int(sys.argv[1]); g = int(sys.argv[2])
assert g <= 7
types = list(itertools.combinations(range(g), 4))
pal = [set(types[i % len(types)]) for i in range(N)]

pool = IDPool()
def xe(u, v, c):
    if u > v: u, v = v, u
    return pool.id(("e", u, v, c))

def dom(u, v):
    return sorted(pal[u] & pal[v])

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

print(f"N={N} g={g} types={len(types)} vars={pool.top} clauses={len(clauses)}", flush=True)
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
    fn = f"experiments/local4_g{g}_N{N}.json"
    with open(fn, "w") as f:
        json.dump({"N": N, "g": g, "edges": coloring}, f)
    print("written", fn, flush=True)
