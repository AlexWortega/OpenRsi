#!/usr/bin/env python3
"""Fast min-conflicts for symmetric sum-free partitions of Z_n \\ {0} into k classes.

Class S: S = -S and no a,b in S (a=b allowed) with a+b in S (mod n).
SAT => triangle-free difference k-coloring of K_n => R_k(3) >= n+1,
per-color base n^{1/k}. Target: beat classical 3.1996 (=1073^{1/6}).

State: color of each orbit {x, n-x}. Conflicts counted over constraint triples
of orbits arising from a+b=c mod n (unique orbit-triples, incl. size-2).

Usage: mc_cyclic.py n k [seed] [max_sec]
"""
import sys, json, time
import numpy as np

n = int(sys.argv[1]); k = int(sys.argv[2])
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
max_sec = float(sys.argv[4]) if len(sys.argv) > 4 else 3600

half = n // 2
def orb(x):
    x %= n
    return min(x, n - x)

cons = set()
selfbad = set()
for a in range(1, half + 1):          # a ranges over orbit reps; but constraints need all a,b
    pass
# generate constraints over all a<=b in 1..n-1 (orbits collapse duplicates)
for a in range(1, n):
    for b in range(a, n):
        c = (a + b) % n
        if c == 0:
            continue
        t = frozenset({orb(a), orb(b), orb(c)})
        if len(t) == 1:
            selfbad.add(orb(a))
        else:
            cons.add(tuple(sorted(t)))
if selfbad:
    print(f"IMPOSSIBLE: self-bad orbits {sorted(selfbad)[:10]}", flush=True)
    sys.exit(0)

cons = sorted(cons)
m = len(cons)
orbs = list(range(1, half + 1))
print(f"n={n} k={k} orbits={half} constraints={m}", flush=True)

# pad triples of size 2 to size 3 by repetition (mono iff all equal still correct)
T = np.array([ (t[0], t[1], t[2] if len(t) == 3 else t[1]) for t in cons ], dtype=np.int32)

adj = [[] for _ in range(half + 1)]
for i, (a, b, c) in enumerate(T):
    for o in {a, b, c}:
        adj[int(o)].append(i)
adj = [np.array(x, dtype=np.int32) for x in adj]

rng = np.random.default_rng(seed)
color = rng.integers(0, k, half + 1).astype(np.int8)

def viol_mask():
    ca, cb, cc = color[T[:, 0]], color[T[:, 1]], color[T[:, 2]]
    return (ca == cb) & (cb == cc)

vm = viol_mask()
conflicts = set(np.nonzero(vm)[0].tolist())
best = len(conflicts)
t0 = time.time()
step = 0
import random
prng = random.Random(seed)
last = 0
while conflicts and time.time() - t0 < max_sec:
    step += 1
    i = prng.choice(tuple(conflicts)) if len(conflicts) < 40 else None
    if i is None:
        while True:
            i = prng.randrange(m)
            if i in conflicts:
                break
    t = T[i]
    o = int(t[prng.randrange(3)])
    old = int(color[o])
    if prng.random() < 0.06:
        c_new = prng.randrange(k)
        if c_new == old:
            c_new = (c_new + 1) % k
    else:
        # evaluate each color by violated count among adj[o]
        rows = T[adj[o]]
        bestc, bestv = old, None
        for c in range(k):
            if c == old:
                continue
            color[o] = c
            ca = color[rows[:, 0]]; cb = color[rows[:, 1]]; cc = color[rows[:, 2]]
            v = int(((ca == cb) & (cb == cc)).sum())
            if bestv is None or v < bestv or (v == bestv and prng.random() < 0.5):
                bestv, bestc = v, c
        color[o] = old
        c_new = bestc
    # apply
    rows_idx = adj[o]
    rows = T[rows_idx]
    ca = color[rows[:, 0]]; cb = color[rows[:, 1]]; cc = color[rows[:, 2]]
    was = (ca == cb) & (cb == cc)
    color[o] = c_new
    ca = color[rows[:, 0]]; cb = color[rows[:, 1]]; cc = color[rows[:, 2]]
    now = (ca == cb) & (cb == cc)
    for j in rows_idx[was & ~now]:
        conflicts.discard(int(j))
    for j in rows_idx[now & ~was]:
        conflicts.add(int(j))
    if len(conflicts) < best:
        best = len(conflicts)
    if step - last >= 200_000:
        last = step
        print(f"step={step} conf={len(conflicts)} best={best} {time.time()-t0:.0f}s", flush=True)

if not conflicts:
    print(f"SOLVED n={n} k={k} step={step} {time.time()-t0:.0f}s", flush=True)
    classes = [[] for _ in range(k)]
    for o in range(1, half + 1):
        classes[int(color[o])].append(o)
        if (n - o) % n != o:
            classes[int(color[o])].append(n - o)
    for cl in classes:
        cl.sort()
    fn = f"experiments/cyclic_{n}_{k}_s{seed}.json"
    with open(fn, "w") as f:
        json.dump({"n": n, "k": k, "classes": classes}, f)
    print("written", fn, flush=True)
else:
    print(f"STALLED n={n} k={k} best={best} steps={step}", flush=True)
