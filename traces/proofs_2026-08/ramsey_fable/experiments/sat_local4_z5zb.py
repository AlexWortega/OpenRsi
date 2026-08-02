#!/usr/bin/env python3
"""Structured SAT for a locally-4 triangle-free coloring of K_{5b} with 5 global colors.

Ansatz: vertices = Z_5 x Z_b. Vertex (i,x) has missing color i (palette = Z_5\{i}).
- within group i: edge (i,x)(i,y) colored c_i(x-y), c_i: Z_b\{0} -> Z_5\{i}, symmetric
  (c_i(d)=c_i(-d)).
- cross groups i<j: edge (i,x)(j,y) colored X_ij(x-y mod b), X_ij: Z_b -> Z_5\{i,j}.

Triangle-freeness constraints:
 T1 (one group): no d,e,d+e all !=0 with c_i equal on them (sum-free classes).
 T2 (two in i, one in j, i<j): no a, d!=0, e with c_i(d)=X_ij(e)=X_ij(e-d)=a.
 T2'(two in j, one in i, i<j): no a, d!=0, f with c_j(d)=X_ij(f)=X_ij(f+d)=a.
 T3 (i<j<k): no a, d1, d2 with X_ij(d1)=X_ik(d2)=X_jk(d2-d1)=a.

If SAT: locally-4 triangle-free K_{5b}; b>=13 gives N>=65 => L_4 = 65 (max possible).
b=13 => N=65. Usage: sat_local4_z5zb.py b
"""
import sys, json, time, itertools
from pysat.solvers import Cadical195
from pysat.formula import IDPool

b = int(sys.argv[1]) if len(sys.argv) > 1 else 13
pool = IDPool()

def cw(i, d, a):  # within-group i, difference d (canonical min(d,b-d)), color a != i
    d = min(d % b, (-d) % b)
    assert d != 0
    return pool.id(("c", i, d, a))

def cx(i, j, d, a):  # cross i<j, difference d in Z_b, color a not in {i,j}
    assert i < j
    return pool.id(("x", i, j, d % b, a))

clauses = []
# domains: exactly-one color per cell
for i in range(5):
    dom = [a for a in range(5) if a != i]
    for d in range(1, b // 2 + 1):
        vs = [cw(i, d, a) for a in dom]
        clauses.append(vs)
        for p, q in itertools.combinations(vs, 2):
            clauses.append([-p, -q])
for i, j in itertools.combinations(range(5), 2):
    dom = [a for a in range(5) if a not in (i, j)]
    for d in range(b):
        vs = [cx(i, j, d, a) for a in dom]
        clauses.append(vs)
        for p, q in itertools.combinations(vs, 2):
            clauses.append([-p, -q])

# T1: sum-free within each group
for i in range(5):
    dom = [a for a in range(5) if a != i]
    seen = set()
    for d in range(1, b):
        for e in range(d, b):
            f = (d + e) % b
            if f == 0:
                continue
            key = tuple(sorted({min(d, b - d), min(e, b - e), min(f, b - f)}))
            if key in seen:
                continue
            seen.add(key)
            for a in dom:
                lits = sorted({cw(i, d, a), cw(i, e, a), cw(i, f, a)})
                clauses.append([-l for l in lits])

# T2 and T2'
for i, j in itertools.combinations(range(5), 2):
    xd = [a for a in range(5) if a not in (i, j)]
    for a in xd:
        for d in range(1, b):
            for e in range(b):
                # two in i: c_i(d)=X_ij(e)=X_ij(e-d)=a
                lits = {cw(i, d, a), cx(i, j, e, a), cx(i, j, e - d, a)}
                clauses.append([-l for l in lits])
                # two in j: c_j(d)=X_ij(f)=X_ij(f+d)=a  (f=e)
                lits = {cw(j, d, a), cx(i, j, e, a), cx(i, j, e + d, a)}
                clauses.append([-l for l in lits])

# T3
for i, j, k in itertools.combinations(range(5), 3):
    dom = [a for a in range(5) if a not in (i, j, k)]
    for a in dom:
        for d1 in range(b):
            for d2 in range(b):
                lits = {cx(i, j, d1, a), cx(i, k, d2, a), cx(j, k, d2 - d1, a)}
                clauses.append([-l for l in lits])

print(f"b={b} N={5*b} vars={pool.top} clauses={len(clauses)}", flush=True)
t0 = time.time()
s = Cadical195(bootstrap_with=clauses)
res = s.solve()
print(("SAT" if res else "UNSAT") + f" ({time.time()-t0:.1f}s)", flush=True)
if res:
    m = set(l for l in s.get_model() if l > 0)
    within = {}
    cross = {}
    for i in range(5):
        for d in range(1, b // 2 + 1):
            for a in range(5):
                if a != i and cw(i, d, a) in m:
                    within[(i, d)] = a
    for i, j in itertools.combinations(range(5), 2):
        for d in range(b):
            for a in range(5):
                if a not in (i, j) and cx(i, j, d, a) in m:
                    cross[(i, j, d)] = a
    out = {"b": b,
           "within": {f"{i},{d}": a for (i, d), a in within.items()},
           "cross": {f"{i},{j},{d}": a for (i, j, d), a in cross.items()}}
    fn = f"experiments/local4_z5z{b}.json"
    with open(fn, "w") as f:
        json.dump(out, f)
    print("written", fn, flush=True)
