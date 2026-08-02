#!/usr/bin/env python3
"""Structured decisive SAT for L_4 = 65 (see NOTES.md for the proved derivation).

Structure (conditional ONLY on the proved equality lemma + rigidity theorem):
  classes C_0..C_3 of 16 vertices, |P_i| = 4 with i in P_i, pal_i = P_i \\ {i};
  internal edges of C_i from pal_i with per-vertex 5-regularity in each color;
  cross edges C_i-C_j from P_i cap P_j;
  per-vertex cross-degree: vertex in C_i has exactly 15 cross edges of color i
  and exactly 11 cross edges of each c in pal_i;
  no monochromatic triangle anywhere (v0 triangles are automatically safe:
  v0-u-w mono needs u,w in same class with internal color i, excluded).

Palette choice is an input: pal_0..pal_3 given on the command line as e.g.
  "1,2,3 0,2,3 0,1,3 0,1,2"  (the g=4 scenario)
Colors are integers; class colors are 0,1,2,3; extra colors 4+.
Exit: SAT writes witness JSON (=> L_4 = 65); UNSAT rules out this palette
combination.
"""
import sys, json, time, itertools
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

pals = [tuple(int(x) for x in a.split(",")) for a in sys.argv[1:5]]
assert len(pals) == 4 and all(len(p) == 3 for p in pals)
for i, p in enumerate(pals):
    assert i not in p
P = [set(p) | {i} for i, p in enumerate(pals)]
tag = "_".join("".join(map(str, p)) for p in pals)

pool = IDPool()
def cls(v): return v // 16
def xe(u, v, c):
    if u > v: u, v = v, u
    return pool.id(("e", u, v, c))
def dom(u, v):
    i, j = cls(u), cls(v)
    if i == j:
        return sorted(pals[i])
    return sorted(P[i] & P[j])

clauses = []
edges = list(itertools.combinations(range(64), 2))
feasible = True
for u, v in edges:
    d = dom(u, v)
    if not d:
        feasible = False
        break
    vs = [xe(u, v, c) for c in d]
    clauses.append(vs)
    for p, q in itertools.combinations(vs, 2):
        clauses.append([-p, -q])
if not feasible:
    print(f"pals={pals}: INFEASIBLE (empty cross palette)", flush=True)
    sys.exit(0)

for u, v, w in itertools.combinations(range(64), 3):
    for c in set(dom(u, v)) & set(dom(u, w)) & set(dom(v, w)):
        clauses.append([-xe(u, v, c), -xe(u, w, c), -xe(v, w, c)])

# exact degree constraints
for v in range(64):
    i = cls(v)
    ins = [u for u in range(16 * i, 16 * i + 16) if u != v]
    outs = [u for u in range(64) if cls(u) != i]
    # internal: 5-regular in each pal_i color
    for c in pals[i]:
        lits = [xe(u, v, c) for u in ins]
        cnf = CardEnc.equals(lits, bound=5, vpool=pool, encoding=EncType.seqcounter)
        clauses.extend(cnf.clauses)
    # cross color i: exactly 15
    lits = [xe(u, v, i) for u in outs if i in dom(u, v)]
    if len(lits) < 15:
        print(f"pals={pals}: INFEASIBLE (color {i} cross capacity {len(lits)} < 15 at class {i})", flush=True)
        sys.exit(0)
    cnf = CardEnc.equals(lits, bound=15, vpool=pool, encoding=EncType.seqcounter)
    clauses.extend(cnf.clauses)
    # cross each c in pal_i: exactly 11
    for c in pals[i]:
        lits = [xe(u, v, c) for u in outs if c in dom(u, v)]
        if len(lits) < 11:
            print(f"pals={pals}: INFEASIBLE (color {c} cross capacity < 11)", flush=True)
            sys.exit(0)
        cnf = CardEnc.equals(lits, bound=11, vpool=pool, encoding=EncType.seqcounter)
        clauses.extend(cnf.clauses)

print(f"pals={pals} vars={pool.top} clauses={len(clauses)}", flush=True)
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
                col[f"{u+1},{v+1}"] = c
    for v in range(64):
        col[f"0,{v+1}"] = cls(v)
    fn = f"experiments/L4_65_witness_{tag}.json"
    with open(fn, "w") as f:
        json.dump({"N": 65, "edges": col}, f)
    print("WITNESS written", fn, "=> L_4 = 65 (verify with verify_local4.py after palette check)", flush=True)
