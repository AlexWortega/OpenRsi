#!/usr/bin/env python3
"""Independent verifier for locally-4 triangle-free colorings stored as JSON
(files experiments/local4_g5_N*.json produced by SAT/min-conflicts searches).

Checks, from scratch:
  1. every pair of vertices has exactly one color in 0..4;
  2. no monochromatic triangle;
  3. every vertex is incident to at most 4 distinct colors (locally-4);
  4. reports N and the implied claim L_4 >= N.

Usage: verify_local4.py file.json [file2.json ...]   (exit 0 iff all pass)
"""
import sys, json, itertools

def check(fn):
    with open(fn) as f:
        data = json.load(f)
    N = data["N"]
    col = {}
    for key, c in data["edges"].items():
        u, v = (int(x) for x in key.split(","))
        assert 0 <= u < v < N, (fn, key)
        assert isinstance(c, int) and 0 <= c <= 4, (fn, key, c)
        assert (u, v) not in col
        col[(u, v)] = c
    # completeness
    assert len(col) == N * (N - 1) // 2, (fn, "missing edges")
    # triangles
    ntri = 0
    for u, v, w in itertools.combinations(range(N), 3):
        a, b, c = col[(u, v)], col[(u, w)], col[(v, w)]
        assert not (a == b == c), (fn, "mono triangle", u, v, w, a)
        ntri += 1
    # local palettes
    pal = [set() for _ in range(N)]
    for (u, v), c in col.items():
        pal[u].add(c)
        pal[v].add(c)
    maxloc = max(len(p) for p in pal)
    assert maxloc <= 4, (fn, "local palette too big", maxloc)
    g = len(set(col.values()))
    print(f"{fn}: N={N} global_colors={g} max_local={maxloc} triangles_checked={ntri} => L_4 >= {N}")
    return N

if __name__ == "__main__":
    files = sys.argv[1:]
    if not files:
        print("usage: verify_local4.py file.json ...")
        sys.exit(2)
    best = 0
    for fn in files:
        best = max(best, check(fn))
    print(f"ALL OK; best verified locally-4 order: {best}")
    sys.exit(0)
