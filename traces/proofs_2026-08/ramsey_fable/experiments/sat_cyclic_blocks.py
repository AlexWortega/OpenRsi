#!/usr/bin/env python3
"""SAT for symmetric sum-free k-partition of Z_n \\ {0} with FEW COLOR BLOCKS.

Record-type partitions (Fredricksen–Sweet) are unions of few intervals of orbit
reps. Restricting the number of boundaries (o where color(o) != color(o+1))
to <= B massively prunes; if such a structured solution exists, CaDiCaL finds it.

Usage: sat_cyclic_blocks.py n k B [conflict_budget]
"""
import sys, json, time
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

n, k, B = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
half = n // 2
def orb(x):
    x %= n
    return min(x, n - x)

pool = IDPool()
def var(o, c): return pool.id(("x", o, c))

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
    print(f"n={n}: structurally impossible", flush=True)
    sys.exit(0)

clauses = []
for o in range(1, half + 1):
    vs = [var(o, c) for c in range(k)]
    clauses.append(vs)
    for i in range(k):
        for j in range(i + 1, k):
            clauses.append([-vs[i], -vs[j]])
for t in cons:
    for c in range(k):
        clauses.append([-var(o, c) for o in t])

# boundary vars
bnd = []
for o in range(1, half):
    b = pool.id(("b", o))
    bnd.append(b)
    for c in range(k):
        # color(o)=c and color(o+1)!=c -> b ; i.e. (x[o][c] and -x[o+1][c]) -> b
        clauses.append([-var(o, c), var(o + 1, c), b])
cnf = CardEnc.atmost(bnd, bound=B, vpool=pool, encoding=EncType.seqcounter)
clauses.extend(cnf.clauses)
# symmetry: orbit 1 color 0
clauses.append([var(1, 0)])

print(f"n={n} k={k} B={B} orbits={half} cons={len(cons)} clauses={len(clauses)}", flush=True)
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
    for a in range(1, n):
        for b2 in range(a, n):
            z = (a + b2) % n
            if z and color[a] == color[b2] == color[z]:
                raise AssertionError((a, b2, z))
    classes = [[x for x in range(1, n) if color[x] == c] for c in range(k)]
    fn = f"experiments/cyclicblocks_{n}_{k}_B{B}.json"
    with open(fn, "w") as f:
        json.dump({"n": n, "k": k, "classes": classes}, f)
    print(f"SAT verified base={n**(1/k):.5f} written {fn}", flush=True)
