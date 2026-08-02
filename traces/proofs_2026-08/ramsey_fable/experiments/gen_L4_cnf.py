#!/usr/bin/env python3
"""Write the DIMACS CNF for one structured L_4=65 palette case.
Usage: gen_L4_cnf.py pal0 pal1 pal2 pal3 out.cnf
(Encoding identical to sat_L4_65_struct.py; see NOTES.md derivation.)
"""
import sys, itertools
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

pals = [tuple(int(x) for x in a.split(",")) for a in sys.argv[1:5]]
out = sys.argv[5]
P = [set(p) | {i} for i, p in enumerate(pals)]
pool = IDPool()
def cls(v): return v // 16
def xe(u, v, c):
    if u > v: u, v = v, u
    return pool.id(("e", u, v, c))
def dom(u, v):
    i, j = cls(u), cls(v)
    return sorted(pals[i]) if i == j else sorted(P[i] & P[j])

clauses = []
edges = list(itertools.combinations(range(64), 2))
for u, v in edges:
    d = dom(u, v)
    assert d
    vs = [xe(u, v, c) for c in d]
    clauses.append(vs)
    for p, q in itertools.combinations(vs, 2):
        clauses.append([-p, -q])
for u, v, w in itertools.combinations(range(64), 3):
    for c in set(dom(u, v)) & set(dom(u, w)) & set(dom(v, w)):
        clauses.append([-xe(u, v, c), -xe(u, w, c), -xe(v, w, c)])
for v in range(64):
    i = cls(v)
    ins = [u for u in range(16 * i, 16 * i + 16) if u != v]
    outs = [u for u in range(64) if cls(u) != i]
    for c in pals[i]:
        cnf = CardEnc.equals([xe(u, v, c) for u in ins], bound=5, vpool=pool,
                             encoding=EncType.seqcounter)
        clauses.extend(cnf.clauses)
    lits = [xe(u, v, i) for u in outs if i in dom(u, v)]
    assert len(lits) >= 15
    cnf = CardEnc.equals(lits, bound=15, vpool=pool, encoding=EncType.seqcounter)
    clauses.extend(cnf.clauses)
    for c in pals[i]:
        lits = [xe(u, v, c) for u in outs if c in dom(u, v)]
        assert len(lits) >= 11
        cnf = CardEnc.equals(lits, bound=11, vpool=pool, encoding=EncType.seqcounter)
        clauses.extend(cnf.clauses)

with open(out, "w") as f:
    f.write(f"p cnf {pool.top} {len(clauses)}\n")
    for cl in clauses:
        f.write(" ".join(map(str, cl)) + " 0\n")
print(f"{out}: vars={pool.top} clauses={len(clauses)}")
