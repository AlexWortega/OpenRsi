#!/usr/bin/env python3
"""Sanity check of the structured encoding style at s=3: K_16 = 1 + 3*5.
Classes C_0..C_2 of 5, each globally 2-colored (locally-2 extremal K_5),
palettes P_i = {i} u pal_i, |pal_i| = 2. Degrees: internal 2-regular per pal
color; cross color i exactly 4; cross pal colors exactly 3 each.
g=3 scenario pal_i = {0,1,2}\\{i} MUST be SAT (the K_16 seed realizes it).
"""
import sys, time, itertools
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

pals = [tuple(int(x) for x in a.split(",")) for a in sys.argv[1:4]]
P = [set(p) | {i} for i, p in enumerate(pals)]
pool = IDPool()
def cls(v): return v // 5
def xe(u, v, c):
    if u > v: u, v = v, u
    return pool.id(("e", u, v, c))
def dom(u, v):
    i, j = cls(u), cls(v)
    return sorted(pals[i]) if i == j else sorted(P[i] & P[j])

clauses = []
edges = list(itertools.combinations(range(15), 2))
for u, v in edges:
    d = dom(u, v)
    if not d:
        print("INFEASIBLE cross palette"); sys.exit(0)
    vs = [xe(u, v, c) for c in d]
    clauses.append(vs)
    for p, q in itertools.combinations(vs, 2):
        clauses.append([-p, -q])
for u, v, w in itertools.combinations(range(15), 3):
    for c in set(dom(u, v)) & set(dom(u, w)) & set(dom(v, w)):
        clauses.append([-xe(u, v, c), -xe(u, w, c), -xe(v, w, c)])
for v in range(15):
    i = cls(v)
    ins = [u for u in range(5 * i, 5 * i + 5) if u != v]
    outs = [u for u in range(15) if cls(u) != i]
    for c in pals[i]:
        cnf = CardEnc.equals([xe(u, v, c) for u in ins], bound=2, vpool=pool, encoding=EncType.seqcounter)
        clauses.extend(cnf.clauses)
    lits = [xe(u, v, i) for u in outs if i in dom(u, v)]
    cnf = CardEnc.equals(lits, bound=4, vpool=pool, encoding=EncType.seqcounter)
    clauses.extend(cnf.clauses)
    for c in pals[i]:
        lits = [xe(u, v, c) for u in outs if c in dom(u, v)]
        cnf = CardEnc.equals(lits, bound=3, vpool=pool, encoding=EncType.seqcounter)
        clauses.extend(cnf.clauses)
t0 = time.time()
s = Cadical195(bootstrap_with=clauses)
print(("SAT" if s.solve() else "UNSAT") + f" ({time.time()-t0:.1f}s)", flush=True)
