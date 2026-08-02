# Question: find a triangle-free locally-4-colored K_N with global palette g (>4) for N up to 65.
# Min-conflicts local search: state = edge coloring; conflicts = mono triangles + local palette overflow.
import sys, random, itertools, json

N = int(sys.argv[1]); G = int(sys.argv[2]); S = int(sys.argv[3]) if len(sys.argv)>3 else 4
SEED = int(sys.argv[4]) if len(sys.argv)>4 else 1
random.seed(SEED)

edges = list(itertools.combinations(range(N),2))
eidx = {e:i for i,e in enumerate(edges)}
def E(u,v): return eidx[(u,v) if u<v else (v,u)]

# vertex palettes: assign each vertex a random S-subset of [G]; edge colors restricted to
# palette intersection (guarantees local-S). If intersection empty -> resample palettes so
# that all pairs intersect: use palettes containing a common structure? Simpler: intersecting
# family via "all palettes contain color 0"? That wastes. Instead: sunflower-free random retry.
def gen_palettes():
    while True:
        P = [frozenset(random.sample(range(G), S)) for _ in range(N)]
        ok = all(P[u] & P[v] for u,v in edges)
        if ok: return P

P = gen_palettes()
col = [0]*len(edges)
for (u,v) in edges:
    col[E(u,v)] = random.choice(sorted(P[u]&P[v]))

tris = list(itertools.combinations(range(N),3))
# incident triangles per edge
tri_of_edge = [[] for _ in edges]
for t,(u,v,w) in enumerate(tris):
    for e in ((u,v),(u,w),(v,w)):
        tri_of_edge[E(*e)].append(t)

def tri_mono(t):
    u,v,w = tris[t]
    return col[E(u,v)]==col[E(u,w)]==col[E(v,w)]

def n_conflicts():
    return sum(1 for t in range(len(tris)) if tri_mono(t))

best_conf = None
for restart in range(50):
    if restart:
        P = gen_palettes()
        for (u,v) in edges:
            col[E(u,v)] = random.choice(sorted(P[u]&P[v]))
    conf = set(t for t in range(len(tris)) if tri_mono(t))
    for step in range(400000):
        if not conf:
            break
        t = random.choice(list(conf))
        u,v,w = tris[t]
        e = E(*random.choice([(u,v),(u,w),(v,w)]))
        a,b = edges[e]
        choices = sorted(P[a]&P[b])
        # pick color minimizing new conflicts among incident triangles
        bestc, bestn = None, None
        random.shuffle(choices)
        for c in choices:
            old = col[e]; col[e] = c
            n = sum(1 for tt in tri_of_edge[e] if tri_mono(tt))
            col[e] = old
            if bestn is None or n < bestn:
                bestn, bestc = n, c
        old = col[e]
        col[e] = bestc if random.random() > 0.05 else random.choice(choices)
        for tt in tri_of_edge[e]:
            if tri_mono(tt): conf.add(tt)
            else: conf.discard(tt)
    nc = len(conf)
    if best_conf is None or nc < best_conf:
        best_conf = nc
        print(f"restart {restart}: conflicts {nc}", flush=True)
    if nc == 0:
        pal = [set() for _ in range(N)]
        for (u,v) in edges:
            pal[u].add(col[E(u,v)]); pal[v].add(col[E(u,v)])
        smax = max(len(p) for p in pal)
        g_used = len(set(col))
        print(f"SUCCESS N={N} local<= {smax} global={g_used}", flush=True)
        json.dump({"N":N,"col":{f"{u},{v}":col[E(u,v)] for u,v in edges}}, open(f"/tmp/mc_local{S}_N{N}_G{G}_seed{SEED}.json","w"))
        break
print(f"DONE best_conflicts={best_conf}")
