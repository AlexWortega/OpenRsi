#!/usr/bin/env python3
"""Min-conflicts for locally-4 triangle-free K_N with 5 global colors,
5-group missing-color structure (group i never uses color i).

Usage: mc_local4_groups.py N [seed] [max_steps]
"""
import sys, json, random, time, itertools

N = int(sys.argv[1])
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 1
MAX_STEPS = int(sys.argv[3]) if len(sys.argv) > 3 else 200_000_000
rng = random.Random(SEED)

q, r = divmod(N, 5)
sizes = [q + 1] * r + [q] * (5 - r)
group = []
for i, s in enumerate(sizes):
    group += [i] * s

edges = list(itertools.combinations(range(N), 2))
eidx = {}
for i, e in enumerate(edges):
    eidx[e] = i

def dom(u, v):
    return [c for c in range(5) if c != group[u] and c != group[v]]

domains = [dom(u, v) for (u, v) in edges]
col = [rng.choice(domains[i]) for i in range(len(edges))]

# triangles: store as edge-index triples
tris = []
for u, v, w in itertools.combinations(range(N), 3):
    tris.append((eidx[(u, v)], eidx[(u, w)], eidx[(v, w)]))
tri_of_edge = [[] for _ in edges]
for t_i, (a, b, c) in enumerate(tris):
    tri_of_edge[a].append(t_i)
    tri_of_edge[b].append(t_i)
    tri_of_edge[c].append(t_i)

def mono(t_i):
    a, b, c = tris[t_i]
    return col[a] == col[b] == col[c]

conflicts = set(t for t in range(len(tris)) if mono(t))
best = len(conflicts)
t0 = time.time()
print(f"N={N} seed={SEED} edges={len(edges)} tris={len(tris)} init_conflicts={best}", flush=True)

step = 0
last_report = 0
while conflicts and step < MAX_STEPS:
    step += 1
    t_i = next(iter(conflicts)) if len(conflicts) == 1 else rng.choice(tuple(conflicts))
    e = tris[t_i][rng.randrange(3)]
    d = domains[e]
    if rng.random() < 0.05:
        c_new = rng.choice(d)
    else:
        # greedy: minimize resulting monochromatic incident triangles
        best_c, best_v = None, None
        old = col[e]
        for c in d:
            if c == old:
                continue
            col[e] = c
            v = sum(1 for tj in tri_of_edge[e] if mono(tj))
            col[e] = old
            if best_v is None or v < best_v or (v == best_v and rng.random() < 0.5):
                best_v, best_c = v, c
        c_new = best_c
    old = col[e]
    if c_new == old:
        continue
    for tj in tri_of_edge[e]:
        if mono(tj):
            conflicts.discard(tj)
    col[e] = c_new
    for tj in tri_of_edge[e]:
        if mono(tj):
            conflicts.add(tj)
    if len(conflicts) < best:
        best = len(conflicts)
    if step - last_report >= 2_000_000:
        last_report = step
        print(f"step={step} conf={len(conflicts)} best={best} {time.time()-t0:.0f}s", flush=True)

if not conflicts:
    print(f"SOLVED N={N} in {step} steps {time.time()-t0:.0f}s", flush=True)
    out = {"N": N, "sizes": sizes, "group": group,
           "edges": {f"{u},{v}": col[eidx[(u, v)]] for (u, v) in edges}}
    fn = f"experiments/local4_g5_N{N}_s{SEED}.json"
    with open(fn, "w") as f:
        json.dump(out, f)
    print("written", fn, flush=True)
else:
    print(f"STALLED N={N}: best={best} after {step} steps", flush=True)
