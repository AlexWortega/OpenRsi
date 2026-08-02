# Question: is there a triangle-free, locally-4-colored complete graph K_N with N > 50
# (i.e., beating the best known globally-4-colored R_4(3)-1 >= 50 lower bound) using g > 4 global colors?
# SAT encoding: edge vars x[e][c]; exactly-one color per edge; no mono triangle;
# vertex-color incidence indicator y[v][c] with cardinality <= s per vertex.
import sys, itertools
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
G = int(sys.argv[2]) if len(sys.argv) > 2 else 6
S = int(sys.argv[3]) if len(sys.argv) > 3 else 4

pool = IDPool()
def xe(u, v, c):
    if u > v: u, v = v, u
    return pool.id(("x", u, v, c))
def yv(v, c): return pool.id(("y", v, c))

clauses = []
edges = list(itertools.combinations(range(N), 2))
for (u,v) in edges:
    clauses.append([xe(u,v,c) for c in range(G)])
    for c1 in range(G):
        for c2 in range(c1+1, G):
            clauses.append([-xe(u,v,c1), -xe(u,v,c2)])
# triangle constraints
for (u,v,w) in itertools.combinations(range(N), 3):
    for c in range(G):
        clauses.append([-xe(u,v,c), -xe(u,w,c), -xe(v,w,c)])
# incidence: x[u][v][c] -> y[u][c] and y[v][c]
for (u,v) in edges:
    for c in range(G):
        clauses.append([-xe(u,v,c), yv(u,c)])
        clauses.append([-xe(u,v,c), yv(v,c)])
# cardinality: sum_c y[v][c] <= S
for v in range(N):
    cnf = CardEnc.atmost([yv(v,c) for c in range(G)], bound=S, vpool=pool, encoding=EncType.seqcounter)
    clauses.extend(cnf.clauses)
# symmetry breaking: edge (0,1) color 0; vertex 0's palette = first S colors
clauses.append([xe(0,1,0)])
for c in range(S, G):
    clauses.append([-yv(0,c)])

s = Cadical195(bootstrap_with=clauses)
print(f"N={N} G={G} S={S} vars={pool.top} clauses={len(clauses)}", flush=True)
res = s.solve()
print("SAT" if res else "UNSAT", flush=True)
if res:
    m = set(l for l in s.get_model() if l > 0)
    col = {}
    for (u,v) in edges:
        for c in range(G):
            if xe(u,v,c) in m: col[(u,v)] = c
    # verify
    for (u,v,w) in itertools.combinations(range(N),3):
        assert not (col[(u,v)]==col[(u,w)]==col[(v,w)])
    for v in range(N):
        pal = set(col[tuple(sorted((v,u)))] for u in range(N) if u!=v)
        assert len(pal) <= S, (v, pal)
    print("verified locally-%d triangle-free on K_%d with %d global colors" % (S, N, len(set(col.values()))))
    import json
    json.dump({f"{u},{v}": c for (u,v),c in col.items()}, open(f"/tmp/local{S}_N{N}_G{G}.json","w"))
    print("saved")
