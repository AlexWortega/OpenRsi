#!/usr/bin/env python3
"""Min-conflicts + restarts for sum-free partitions of F_2^d \\ {0} into k classes.

Constraint: no projective line {u,v,u^v} monochromatic.
SAT => R_k(3) > 2^d, and by superadditivity of d(k) this feeds the family base.

Usage: mc_f2d.py d k [seed] [max_sec]
"""
import sys, json, time, random
import numpy as np

d, k = int(sys.argv[1]), int(sys.argv[2])
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
max_sec = float(sys.argv[4]) if len(sys.argv) > 4 else 1e18

n = 2**d - 1
lines = []
for u in range(1, n + 1):
    for v in range(u + 1, n + 1):
        w = u ^ v
        if w > v:
            lines.append((u, v, w))
L = np.array(lines, dtype=np.int32)
m = len(L)
adj = [[] for _ in range(n + 1)]
for i, (u, v, w) in enumerate(L):
    adj[u].append(i); adj[v].append(i); adj[w].append(i)
adj = [np.array(x, dtype=np.int32) for x in adj]
print(f"d={d} k={k} n={n} lines={m}", flush=True)

prng = random.Random(seed)
rng = np.random.default_rng(seed)
t0 = time.time()
global_best = m
restart = 0
while time.time() - t0 < max_sec:
    restart += 1
    color = rng.integers(0, k, n + 1).astype(np.int8)
    ca, cb, cc = color[L[:, 0]], color[L[:, 1]], color[L[:, 2]]
    conflicts = set(np.nonzero((ca == cb) & (cb == cc))[0].tolist())
    best = len(conflicts)
    stall = 0
    step = 0
    while conflicts and time.time() - t0 < max_sec:
        step += 1
        i = prng.choice(tuple(conflicts)) if len(conflicts) < 30 else None
        if i is None:
            while True:
                i = prng.randrange(m)
                if i in conflicts:
                    break
        tri = L[i]
        v = int(tri[prng.randrange(3)])
        old = int(color[v])
        rows_idx = adj[v]
        rows = L[rows_idx]
        if prng.random() < 0.07:
            c_new = prng.randrange(k - 1)
            if c_new >= old:
                c_new += 1
        else:
            bestc, bestv = old, None
            for c in range(k):
                if c == old:
                    continue
                color[v] = c
                x, y, z = color[rows[:, 0]], color[rows[:, 1]], color[rows[:, 2]]
                cnt = int(((x == y) & (y == z)).sum())
                if bestv is None or cnt < bestv or (cnt == bestv and prng.random() < 0.5):
                    bestv, bestc = cnt, c
            color[v] = old
            c_new = bestc
        x, y, z = color[rows[:, 0]], color[rows[:, 1]], color[rows[:, 2]]
        was = (x == y) & (y == z)
        color[v] = c_new
        x, y, z = color[rows[:, 0]], color[rows[:, 1]], color[rows[:, 2]]
        now = (x == y) & (y == z)
        for j in rows_idx[was & ~now]:
            conflicts.discard(int(j))
        for j in rows_idx[now & ~was]:
            conflicts.add(int(j))
        if len(conflicts) < best:
            best = len(conflicts)
            stall = 0
        else:
            stall += 1
        if stall > 400_000:
            break  # restart
        if step % 3_000_000 == 0:
            print(f"r{restart} step={step} conf={len(conflicts)} best={best} gbest={global_best} {time.time()-t0:.0f}s", flush=True)
    global_best = min(global_best, best)
    if not conflicts:
        print(f"SOLVED d={d} k={k} restart={restart} {time.time()-t0:.0f}s", flush=True)
        classes = [[v for v in range(1, n + 1) if color[v] == c] for c in range(k)]
        fn = f"experiments/f2_{d}_{k}_mc.json"
        with open(fn, "w") as f:
            json.dump({"d": d, "k": k, "classes": classes}, f)
        print("written", fn, flush=True)
        sys.exit(0)
    print(f"restart {restart}: best={best} gbest={global_best}", flush=True)
print(f"TIMEOUT gbest={global_best}", flush=True)
