#!/usr/bin/env python3
"""Exhaustive first falsification test for the oracle's stationary automaton.

Enumerates every symmetric Boolean transition matrix A on five states (loops
allowed), with H=C5, and tests q=2..6 by exact integer transfer matrices.
Outputs the best feasible closed-walk code for each q. This is a search, not a
claim of optimality beyond the explicitly enumerated symmetric class.
"""
import itertools, json, os
import numpy as np

N = 5
H = np.zeros((N, N), dtype=np.int64)
for i in range(N):
    H[i, (i + 1) % N] = H[(i + 1) % N, i] = 1
bad_states = [(u, v) for u in range(N) for v in range(N) if not H[u, v]]
entries = [(i, j) for i in range(N) for j in range(i, N)]
QS = range(2, 7)
best = {q: (-1, None, None) for q in QS}
feasible_counts = {q: 0 for q in QS}

def traces(A):
    B = np.zeros((len(bad_states), len(bad_states)), dtype=np.int64)
    for i, (u, v) in enumerate(bad_states):
        for j, (x, y) in enumerate(bad_states):
            B[i, j] = A[u, x] * A[v, y]
    Ap = np.eye(N, dtype=np.int64)
    Bp = np.eye(len(bad_states), dtype=np.int64)
    out = {}
    for q in range(1, max(QS) + 1):
        Ap = Ap @ A
        Bp = Bp @ B
        if q in QS:
            out[q] = (int(np.trace(Ap)), int(np.trace(Bp)))
    return out

for mask in range(1 << len(entries)):
    A = np.zeros((N, N), dtype=np.int64)
    for bit, (i, j) in enumerate(entries):
        if mask >> bit & 1:
            A[i, j] = A[j, i] = 1
    for q, (w, wb) in traces(A).items():
        assert wb >= w
        if wb == w:
            feasible_counts[q] += 1
            if w > best[q][0]:
                best[q] = (w, mask, A.tolist())

os.makedirs("experiments/results", exist_ok=True)
out = {
    "template": "C5",
    "transition_class": "all symmetric Boolean 5x5 matrices, loops allowed",
    "entry_order": entries,
    "feasible_counts": feasible_counts,
    "best": {str(q): {"W": w, "base": w ** (1/q) if w else 0,
                       "mask": mask, "A": A}
             for q, (w, mask, A) in best.items()},
}
with open("experiments/results/stationary_c5_symmetric.json", "w") as f:
    json.dump(out, f, indent=2)
print(json.dumps(out, indent=2))
