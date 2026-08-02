#!/usr/bin/env python3
"""Does a triangle-free LOCALLY-3 coloring of K_16 exist that uses >= 4 colors globally?

If UNSAT, every extremal locally-3 coloring on 16 vertices is an ordinary
3-coloring (hence one of the R(3,3,3)=17 critical colorings), which massively
constrains any hypothetical extremal L_4 = 65 example.

Encoding: g global colors (try g=4,5,6 with all colors forced used); edge vars;
per-vertex incidence y[v][c]; sum_c y[v][c] <= 3; every color used somewhere.
"""
import sys, itertools, time
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

N = 16
g = int(sys.argv[1]) if len(sys.argv) > 1 else 4

pool = IDPool()
def xe(u, v, c):
    if u > v: u, v = v, u
    return pool.id(("e", u, v, c))
def yv(v, c): return pool.id(("y", v, c))

clauses = []
edges = list(itertools.combinations(range(N), 2))
for u, v in edges:
    vs = [xe(u, v, c) for c in range(g)]
    clauses.append(vs)
    for p, q in itertools.combinations(vs, 2):
        clauses.append([-p, -q])
for u, v, w in itertools.combinations(range(N), 3):
    for c in range(g):
        clauses.append([-xe(u, v, c), -xe(u, w, c), -xe(v, w, c)])
for u, v in edges:
    for c in range(g):
        clauses.append([-xe(u, v, c), yv(u, c)])
        clauses.append([-xe(u, v, c), yv(v, c)])
for v in range(N):
    cnf = CardEnc.atmost([yv(v, c) for c in range(g)], bound=3, vpool=pool,
                         encoding=EncType.seqcounter)
    clauses.extend(cnf.clauses)
# every color used
for c in range(g):
    clauses.append([xe(u, v, c) for (u, v) in edges])
# symmetry: vertex 0 palette = {0,1,2}; edge (0,1) color 0
for c in range(3, g):
    clauses.append([-yv(0, c)])
clauses.append([xe(0, 1, 0)])

print(f"N={N} g={g} vars={pool.top} clauses={len(clauses)}", flush=True)
t0 = time.time()
s = Cadical195(bootstrap_with=clauses)
res = s.solve()
print(("SAT" if res else "UNSAT") + f" ({time.time()-t0:.1f}s)", flush=True)
if res:
    m = set(l for l in s.get_model() if l > 0)
    import json
    col = {}
    for u, v in edges:
        for c in range(g):
            if xe(u, v, c) in m:
                col[f"{u},{v}"] = c
    fn = f"experiments/local3_16_g{g}.json"
    with open(fn, "w") as f:
        json.dump({"N": N, "g": g, "edges": col}, f)
    print("written", fn, flush=True)
