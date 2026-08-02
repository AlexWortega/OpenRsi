#!/usr/bin/env python3
"""Decide: does a triangle-free locally-3 coloring of K_16 with exactly 4 global
colors exist?

Justified reduction (round1 equality lemma, rederived in NOTES.md): any locally-3
triangle-free K_16 has, at EVERY vertex, exactly 3 incident colors (since
16 = 1 + 3*L_2 forces equality throughout the neighborhood recursion). With 4
global colors each vertex therefore misses exactly one color; the missing-color
map splits the 16 vertices into groups of sizes m_0..m_3 with sum 16. Each color
class is 5-regular on its support of size 16 - m_c (equality lemma), so
16 - m_c is even and >= 10: m_c even, m_c <= 6.

For each size profile we run a SAT instance: edge (u,v) colored from
{0..3} \ {miss(u), miss(v)}; no mono triangle; PLUS 5-regularity of each color
at each supporting vertex (equality lemma). If all profiles UNSAT, every
extremal locally-3 K_16 is globally 3-colored.

Exit prints per-profile SAT/UNSAT.
"""
import sys, json, time, itertools
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

N = 16
profiles = [(6,6,4,0), (6,6,2,2), (6,4,4,2), (4,4,4,4)]
STRICT = len(sys.argv) > 1 and sys.argv[1] == "strict"

for prof in profiles:
    group = []
    for c, m in enumerate(prof):
        group += [c] * m
    pool = IDPool()
    def xe(u, v, c):
        if u > v: u, v = v, u
        return pool.id(("e", u, v, c))
    clauses = []
    edges = list(itertools.combinations(range(N), 2))
    def dom(u, v):
        return [c for c in range(4) if c != group[u] and c != group[v]]
    for u, v in edges:
        vs = [xe(u, v, c) for c in dom(u, v)]
        clauses.append(vs)
        for p, q in itertools.combinations(vs, 2):
            clauses.append([-p, -q])
    for u, v, w in itertools.combinations(range(N), 3):
        for c in set(dom(u, v)) & set(dom(u, w)) & set(dom(v, w)):
            clauses.append([-xe(u, v, c), -xe(u, w, c), -xe(v, w, c)])
    # equality-lemma regularity: every vertex sees each non-missing color on exactly 5 edges
    for v in range(N):
        for c in range(4):
            if c == group[v]:
                continue
            lits = [xe(u, v, c) for u in range(N) if u != v and group[u] != c]
            eq = CardEnc.equals(lits, bound=5, vpool=pool, encoding=EncType.seqcounter)
            clauses.extend(eq.clauses)
    t0 = time.time()
    s = Cadical195(bootstrap_with=clauses)
    res = s.solve()
    print(f"profile {prof}: {'SAT' if res else 'UNSAT'} ({time.time()-t0:.1f}s)", flush=True)
    if res:
        m = set(l for l in s.get_model() if l > 0)
        col = {}
        for u, v in edges:
            for c in dom(u, v):
                if xe(u, v, c) in m:
                    col[f"{u},{v}"] = c
        fn = f"experiments/local3_16_g4_{'_'.join(map(str,prof))}.json"
        with open(fn, "w") as f:
            json.dump({"N": N, "profile": prof, "group": group, "edges": col}, f)
        print("written", fn, flush=True)
