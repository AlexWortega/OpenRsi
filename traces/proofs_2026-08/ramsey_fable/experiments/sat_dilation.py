#!/usr/bin/env python3
"""Symmetric sum-free k-partition of Z_n \\ {0} invariant under dilation x->g*x.

Variables = orbits of the group <g,-1> (multiplication) acting on Z_n \\ {0}
(g must be a unit mod n). Constraints: for each orbit-rep x and each y,
triple (orb(x),orb(y),orb(x+y)) not monochromatic. If an orbit forms a
self-triple, that g is impossible. Works for composite n (e.g. 1073=29*37).

Usage: sat_dilation.py n k g          (single g)
       sat_dilation.py n k scan gmax  (scan all units g<=gmax with even order incl -1 handling)
"""
import sys, json, time
from math import gcd
from pysat.solvers import Cadical195

n, k = int(sys.argv[1]), int(sys.argv[2])

def build_orbits(g):
    # orbits of <g,-1>
    orbit = [-1] * n
    reps = []
    for x in range(1, n):
        if orbit[x] != -1:
            continue
        # BFS closure under *g and negation
        stack = [x]
        oid = len(reps)
        members = []
        while stack:
            y = stack.pop()
            if orbit[y] != -1:
                continue
            orbit[y] = oid
            members.append(y)
            stack.append((y * g) % n)
            stack.append((n - y) % n)
        reps.append(members)
    return orbit, reps

def solve_g(g, verbose=True):
    if gcd(g, n) != 1:
        return None
    orbit, reps = build_orbits(g)
    t = len(reps)
    cons = set()
    for members in reps:
        x = members[0]
        for y in range(1, n):
            z = (x + y) % n
            if z == 0:
                continue
            tri = frozenset({orbit[x], orbit[y], orbit[z]})
            if len(tri) == 1:
                return ("selfbad", t)
            cons.add(tri)
    def var(i, c): return i * k + c + 1
    clauses = []
    for i in range(t):
        clauses.append([var(i, c) for c in range(k)])
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                clauses.append([-var(i, c1), -var(i, c2)])
    for tri in cons:
        for c in range(k):
            clauses.append([-var(i, c) for i in tri])
    s = Cadical195(bootstrap_with=clauses)
    t0 = time.time()
    if not s.solve():
        return ("unsat", t, time.time() - t0)
    m = set(l for l in s.get_model() if l > 0)
    color = [-1] * n
    for i, members in enumerate(reps):
        c = next(c for c in range(k) if var(i, c) in m)
        for y in members:
            color[y] = c
    # full inline verify
    for a in range(1, n):
        for b in range(a, n):
            z = (a + b) % n
            if z and color[a] == color[b] == color[z]:
                raise AssertionError((a, b, z))
    classes = [[x for x in range(1, n) if color[x] == c] for c in range(k)]
    fn = f"experiments/dilation_{n}_{k}_g{g}.json"
    with open(fn, "w") as f:
        json.dump({"n": n, "k": k, "g": g, "classes": classes}, f)
    return ("SAT", t, fn)

if sys.argv[3] == "scan":
    gmax = int(sys.argv[4]) if len(sys.argv) > 4 else n - 1
    for g in range(2, min(gmax + 1, n)):
        if gcd(g, n) != 1:
            continue
        r = solve_g(g)
        if r is None:
            continue
        if r[0] == "SAT":
            print(f"g={g}: SAT!!! orbits={r[1]} base={n**(1/k):.5f} file={r[2]}", flush=True)
        elif r[0] == "unsat":
            print(f"g={g}: UNSAT orbits={r[1]} ({r[2]:.1f}s)", flush=True)
        # skip printing selfbad
else:
    g = int(sys.argv[3])
    print(solve_g(g), flush=True)
