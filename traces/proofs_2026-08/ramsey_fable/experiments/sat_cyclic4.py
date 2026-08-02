#!/usr/bin/env python3
"""SAT scan: largest n with Z_n \ {0} partitioned into 4 symmetric sum-free classes.
Class S: S=-S, and no a,b in S (equal allowed) with a+b in S (all mod n).
Gives triangle-free difference 4-coloring of K_n. Usage: sat_cyclic4.py nmin nmax [k]
"""
import sys, json, time
from pysat.solvers import Cadical195

nmin, nmax = int(sys.argv[1]), int(sys.argv[2])
K = int(sys.argv[3]) if len(sys.argv) > 3 else 4

def run(n, k):
    half = n // 2
    def orb(x):
        x %= n
        return min(x, n - x)
    # orbit reps 1..half (if n even, orbit n/2 valid: 2*(n/2)=0 not constraint? a+b=c with a=b=n/2 -> c=0 skip)
    def var(o, c): return (o - 1) * k + c + 1
    clauses = []
    for o in range(1, half + 1):
        clauses.append([var(o, c) for c in range(k)])
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                clauses.append([-var(o, c1), -var(o, c2)])
    bad = set()
    cons = set()
    for a in range(1, n):
        for b in range(a, n):
            c = (a + b) % n
            if c == 0:
                continue
            t = frozenset({orb(a), orb(b), orb(c)})
            if len(t) == 1:
                bad.add(orb(a))
            else:
                cons.add(t)
    for o in bad:
        return None  # structurally impossible (orbit forms self-triple)
    for t in cons:
        for c in range(k):
            clauses.append([-var(o, c) for o in t])
    s = Cadical195(bootstrap_with=clauses)
    if not s.solve():
        return False
    m = set(l for l in s.get_model() if l > 0)
    classes = [[] for _ in range(k)]
    for o in range(1, half + 1):
        for c in range(k):
            if var(o, c) in m:
                classes[c].append(o)
                if o != n - o and n - o != o:
                    classes[c].append(n - o)
    for cl in classes:
        cl.sort()
    return classes

for n in range(nmin, nmax + 1):
    t0 = time.time()
    r = run(n, K)
    if r is None:
        print(f"n={n}: structurally impossible", flush=True)
    elif r is False:
        print(f"n={n}: UNSAT ({time.time()-t0:.1f}s)", flush=True)
    else:
        print(f"n={n}: SAT sizes={[len(c) for c in r]} ({time.time()-t0:.1f}s)", flush=True)
        with open(f"experiments/cyclic4_{n}.json", "w") as f:
            json.dump({"n": n, "k": K, "classes": r}, f)
