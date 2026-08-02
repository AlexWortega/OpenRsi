#!/usr/bin/env python3
"""SAT: can F_2^d \ {0} be partitioned into k sum-free sets?
<=> triangle-free XOR k-coloring of K_{2^d}  <=> R_k(3) > 2^d.

Symmetry breaking (sound): some class has size >= (2^d-1)/k > 2^{d-2}-1 vertices
when k <= 4... more simply: the largest class has size >= ceil((2^d-1)/k).
Any set of that size spans dimension >= ceil(log2(size+1)). If that dim >= r,
a linear automorphism maps r independent members to e_1..e_r; so we may fix
colors of e_1..e_r (=1,2,4,...,2^{r-1}) to color 0.
For (d,k): size >= ceil((2^d-1)/k); dim >= smallest r with 2^r-1 >= size.
Also break color permutations: first vertex (in index order) not colored 0
gets color 1; first not in {0,1} gets color 2; etc. via sequential constraints
(simple version: vertex 3's color <= 1+..., we use the standard scheme below).

Usage: sat_f2d.py d k [timeout_hint]
"""
import sys, json, time
from pysat.solvers import Cadical195
from pysat.formula import CNF

d = int(sys.argv[1]); k = int(sys.argv[2])
n = 2**d - 1
def var(v, c): return (v - 1) * k + c + 1

cnf = CNF()
for v in range(1, n + 1):
    cnf.append([var(v, c) for c in range(k)])
    for c1 in range(k):
        for c2 in range(c1 + 1, k):
            cnf.append([-var(v, c1), -var(v, c2)])

nlines = 0
for u in range(1, n + 1):
    for v in range(u + 1, n + 1):
        w = u ^ v
        if w > v:
            nlines += 1
            for c in range(k):
                cnf.append([-var(u, c), -var(v, c), -var(w, c)])
print(f"d={d} k={k} n={n} lines={nlines} vars={n*k} clauses={len(cnf.clauses)}", flush=True)

# symmetry: largest class size s0 >= ceil(n/k); its span dim r: 2^r - 1 >= s0.
import math
s0 = -(-n // k)
r = 1
while 2**r - 1 < s0:
    r += 1
r = min(r, d)
for i in range(r):
    cnf.append([var(2**i, 0)])
print(f"fixed e_1..e_{r} to color 0", flush=True)
# color-permutation breaking on remaining colors: vertex v may use color c>=1
# only if some earlier vertex uses color c-1. Cheap version: order vertices,
# introduce prefix vars p[v][c] = "color c used among vertices 1..v".
top = n * k
def pv(v, c): return top + (v - 1) * k + c + 1
for v in range(1, n + 1):
    for c in range(k):
        # p[v][c] <-> p[v-1][c] or x[v][c]
        if v == 1:
            cnf.append([-pv(v, c), var(v, c)])
            cnf.append([pv(v, c), -var(v, c)])
        else:
            cnf.append([-pv(v, c), pv(v - 1, c), var(v, c)])
            cnf.append([pv(v, c), -pv(v - 1, c)])
            cnf.append([pv(v, c), -var(v, c)])
    for c in range(2, k):
        # x[v][c] -> p[v-1][c-1]
        if v == 1:
            cnf.append([-var(v, c)])
        else:
            cnf.append([-var(v, c), pv(v - 1, c - 1)])

t0 = time.time()
s = Cadical195(bootstrap_with=cnf)
res = s.solve()
print(("SAT" if res else "UNSAT") + f"  ({time.time()-t0:.0f}s)", flush=True)
if res:
    m = s.get_model()
    col = {}
    for v in range(1, n + 1):
        for c in range(k):
            if m[var(v, c) - 1] > 0:
                col[v] = c
    classes = [[v for v in range(1, n + 1) if col[v] == c] for c in range(k)]
    # verify inline
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            w = u ^ v
            if w > v:
                assert not (col[u] == col[v] == col[w])
    print("inline verify OK; sizes", [len(c) for c in classes], flush=True)
    fn = f"experiments/f2_{d}_{k}.json"
    with open(fn, "w") as f:
        json.dump({"d": d, "k": k, "classes": classes}, f)
    print("written", fn, flush=True)
