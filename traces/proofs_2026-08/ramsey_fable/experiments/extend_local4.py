#!/usr/bin/env python3
"""Extend a verified locally-4 coloring by one vertex at a time via SAT.
Freeze the existing K_N coloring; add vertex N with a chosen missing color
(try each group); solve for its N edge colors. Iterate greedily with
backtracking over which group the new vertex joins.

Usage: extend_local4.py start.json target_N
"""
import sys, json, itertools, time
from pysat.solvers import Cadical195
from pysat.formula import IDPool

fn, target = sys.argv[1], int(sys.argv[2])
with open(fn) as f:
    data = json.load(f)
N = data["N"]
col = {}
for key, c in data["edges"].items():
    u, v = (int(x) for x in key.split(","))
    col[(u, v)] = c
group = data.get("group")
if group is None:
    # infer missing color per vertex
    group = []
    for v in range(N):
        pal = set()
        for u in range(N):
            if u == v:
                continue
            e = (min(u, v), max(u, v))
            pal.add(col[e])
        miss = [c for c in range(5) if c not in pal]
        group.append(miss[0] if miss else -1)

def try_extend(col, group, N, newgroup):
    """new vertex N in group newgroup; edges to v get color != newgroup, != group[v];
    also must keep locally-4: old vertices keep palette within their 4;
    constraint: no mono triangle with two old vertices."""
    pool = IDPool()
    def xe(v, c): return pool.id((v, c))
    clauses = []
    for v in range(N):
        dom = [c for c in range(5) if c != newgroup and c != group[v]]
        vs = [xe(v, c) for c in dom]
        clauses.append(vs)
        for p, q in itertools.combinations(vs, 2):
            clauses.append([-p, -q])
    for u, v in itertools.combinations(range(N), 2):
        c = col[(u, v)]
        if c != newgroup and c != group[u] and c != group[v]:
            clauses.append([-xe(u, c), -xe(v, c)])
    s = Cadical195(bootstrap_with=clauses)
    if not s.solve():
        return None
    m = set(l for l in s.get_model() if l > 0)
    newcols = {}
    for v in range(N):
        for c in range(5):
            if c != newgroup and c != group[v] and xe(v, c) in m:
                newcols[v] = c
    return newcols

while N < target:
    done = False
    for ng in range(5):
        r = try_extend(col, group, N, ng)
        if r is not None:
            for v, c in r.items():
                col[(v, N)] = c
            group.append(ng)
            N += 1
            print(f"extended to N={N} (group {ng})", flush=True)
            done = True
            break
    if not done:
        print(f"STUCK at N={N}: no single-vertex extension in any group", flush=True)
        break

out = {"N": N, "group": group,
       "edges": {f"{u},{v}": c for (u, v), c in col.items()}}
fn2 = f"experiments/local4_ext_N{N}.json"
with open(fn2, "w") as f:
    json.dump(out, f)
print("written", fn2, flush=True)
