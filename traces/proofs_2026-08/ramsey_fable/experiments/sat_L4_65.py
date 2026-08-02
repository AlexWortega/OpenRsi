#!/usr/bin/env python3
"""Decisive SAT for L_4 = 65 vs L_4 <= 64.

Justified structure of any hypothetical locally-4 triangle-free K_65
(65 = 1 + 4*L_3, so extremal; round1 equality lemma + this run's rigidity
theorem, both proved/verified):
  - fix a vertex v0; the other 64 split into 4 classes of 16 by the color of
    their edge to v0; WLOG class i's edge color is i (i=0..3);
  - class i induces an extremal locally-3 triangle-free K_16, which by the
    rigidity theorem uses EXACTLY 3 colors globally, all != i;
  - hence at most 4 + 4*3 = 16 colors occur anywhere; WLOG universe = 0..15;
  - the whole coloring is triangle-free and every vertex sees <= 4 colors.

Encoding (faithful; no relaxation, no strengthening beyond proved facts):
  vertices 0..63 (class i = 16i..16i+15); v0 implicit.
  vars e[u][v][c] for c in 0..15, minus domain restriction c != i for
  within-class-i edges. Exactly-one per edge. Constraints:
  (1) no monochromatic triangle among 0..63 (v0-triangles auto-safe);
  (2) class i internal edges use <= 3 distinct colors (aux u[i][c], card <= 3);
  (3) every vertex sees <= 4 distinct colors incl. its v0-edge color i
      (aux y[v][c], y[v][i] forced, card <= 4);
  (4) color symmetry: colors 4..15 used in increasing order (precedence).

UNSAT => L_4 <= 64.  SAT => explicit locally-4 K_65 witness => L_4 = 65.
"""
import sys, json, time, itertools
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

NC = 16  # color universe
pool = IDPool()

def cls(v): return v // 16

def xe(u, v, c):
    if u > v: u, v = v, u
    return pool.id(("e", u, v, c))

def dom(u, v):
    if cls(u) == cls(v):
        return [c for c in range(NC) if c != cls(u)]
    return list(range(NC))

clauses = []
edges = list(itertools.combinations(range(64), 2))
for u, v in edges:
    vs = [xe(u, v, c) for c in dom(u, v)]
    clauses.append(vs)
    for p, q in itertools.combinations(vs, 2):
        clauses.append([-p, -q])

# (1) triangles
for u, v, w in itertools.combinations(range(64), 3):
    common = set(dom(u, v)) & set(dom(u, w)) & set(dom(v, w))
    for c in common:
        clauses.append([-xe(u, v, c), -xe(u, w, c), -xe(v, w, c)])

# (2) class palettes <= 3
for i in range(4):
    us = []
    for c in range(NC):
        if c == i:
            continue
        uic = pool.id(("u", i, c))
        us.append(uic)
        # e -> u
        for a, b in itertools.combinations(range(16 * i, 16 * i + 16), 2):
            clauses.append([-xe(a, b, c), uic])
    cnf = CardEnc.atmost(us, bound=3, vpool=pool, encoding=EncType.seqcounter)
    clauses.extend(cnf.clauses)

# (3) vertex palettes <= 4 (v0-edge color i counts as one)
for v in range(64):
    ys = []
    i = cls(v)
    for c in range(NC):
        yvc = pool.id(("y", v, c))
        ys.append(yvc)
        for u in range(64):
            if u == v:
                continue
            if c in dom(u, v):
                clauses.append([-xe(u, v, c), yvc])
    clauses.append([pool.id(("y", v, i))])  # sees color i on the v0 edge
    cnf = CardEnc.atmost(ys, bound=4, vpool=pool, encoding=EncType.seqcounter)
    clauses.extend(cnf.clauses)

# (4) color precedence for 4..15: global "color c used" gvar; g_c -> g_{c-1}
gv = {}
for c in range(4, NC):
    g = pool.id(("g", c))
    gv[c] = g
    for u, v in edges:
        if c in dom(u, v):
            clauses.append([-xe(u, v, c), g])
for c in range(5, NC):
    clauses.append([-gv[c], gv[c - 1]])

print(f"vars={pool.top} clauses={len(clauses)}", flush=True)
t0 = time.time()
s = Cadical195(bootstrap_with=clauses)
res = s.solve()
print(("SAT" if res else "UNSAT") + f" ({time.time()-t0:.0f}s)", flush=True)
if res:
    m = set(l for l in s.get_model() if l > 0)
    col = {}
    for u, v in edges:
        for c in dom(u, v):
            if xe(u, v, c) in m:
                col[f"{u+1},{v+1}"] = c  # shift: v0 = vertex 0 in final K_65
    # add v0 edges
    for v in range(64):
        col[f"0,{v+1}"] = cls(v)
    fn = "experiments/L4_65_witness.json"
    with open(fn, "w") as f:
        json.dump({"N": 65, "edges": col}, f)
    print("written", fn, flush=True)
else:
    print("L_4 <= 64 (conditional only on the proved equality lemma and rigidity theorem)", flush=True)
