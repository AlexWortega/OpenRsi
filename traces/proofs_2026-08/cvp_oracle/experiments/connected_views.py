#!/usr/bin/env python3
"""Build and exactly attack the connected-view GF(2) syndrome candidate.

Clauses are tuples of signed integers. Positive i means x_i; negative -i means not x_i.
This is finite experimental evidence only, not a proof of asymptotic soundness.
"""
from __future__ import annotations

import argparse
import itertools
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix, hstack

Clause = Tuple[int, ...]
Scope = Tuple[int, ...]
Assignment = Tuple[int, ...]


def satisfies(clause: Clause, values: Dict[int, int]) -> bool:
    return any(values[abs(lit)] == (1 if lit > 0 else 0) for lit in clause)


def all_satisfying_views(clauses: Sequence[Clause], q: Tuple[int, ...]):
    scope = tuple(sorted({abs(lit) for j in q for lit in clauses[j]}))
    views = []
    for bits in itertools.product((0, 1), repeat=len(scope)):
        val = dict(zip(scope, bits))
        if all(satisfies(clauses[j], val) for j in q):
            views.append(bits)
    return scope, tuple(views)


def intersection_graph(clauses: Sequence[Clause]) -> List[set[int]]:
    scopes = [{abs(x) for x in c} for c in clauses]
    adj = [set() for _ in clauses]
    for i in range(len(clauses)):
        for j in range(i):
            if scopes[i] & scopes[j]:
                adj[i].add(j)
                adj[j].add(i)
    return adj


def connected_subsets(clauses: Sequence[Clause], d: int) -> List[Tuple[int, ...]]:
    """Enumerate connected nonempty clause subsets, canonically (tiny instances)."""
    adj = intersection_graph(clauses)
    out = []
    m = len(clauses)
    for size in range(1, min(d, m) + 1):
        for q in itertools.combinations(range(m), size):
            allowed = set(q)
            seen = {q[0]}
            frontier = [q[0]]
            while frontier:
                v = frontier.pop()
                for w in adj[v] & allowed:
                    if w not in seen:
                        seen.add(w); frontier.append(w)
            if seen == allowed:
                out.append(q)
    return out


@dataclass
class Instance:
    H: coo_matrix
    target: np.ndarray
    columns: List[Tuple[Tuple[int, ...], Assignment]]
    scopes: Dict[Tuple[int, ...], Scope]
    views: Dict[Tuple[int, ...], Tuple[Assignment, ...]]
    groups: List[Tuple[int, ...]]


def build(clauses: Sequence[Clause], d: int) -> Instance:
    groups = connected_subsets(clauses, d)
    scopes, views = {}, {}
    columns = []
    col_index = {}
    for q in groups:
        scopes[q], views[q] = all_satisfying_views(clauses, q)
        for a in views[q]:
            col_index[(q, a)] = len(columns)
            columns.append((q, a))

    rows, cols, data, target = [], [], [], []
    # Odd group coverage. Empty A_Q intentionally produces an all-zero row target 1.
    for q in groups:
        r = len(target); target.append(1)
        for a in views[q]:
            rows.append(r); cols.append(col_index[(q, a)]); data.append(1)

    group_set = set(groups)
    # One-clause-deletion connected inclusions and every satisfying child view.
    for q in groups:
        if len(q) < 2:
            continue
        for deleted in q:
            child = tuple(x for x in q if x != deleted)
            if child not in group_set:
                continue
            child_pos = {v: i for i, v in enumerate(scopes[child])}
            parent_positions = tuple(scopes[q].index(v) for v in scopes[child])
            for b in views[child]:
                r = len(target); target.append(0)
                rows.append(r); cols.append(col_index[(child, b)]); data.append(1)
                for a in views[q]:
                    if tuple(a[i] for i in parent_positions) == b:
                        rows.append(r); cols.append(col_index[(q, a)]); data.append(1)

    H = coo_matrix((data, (rows, cols)), shape=(len(target), len(columns)), dtype=np.int8)
    return Instance(H, np.asarray(target, dtype=np.int8), columns, scopes, views, groups)


def exact_min_weight(inst: Instance, time_limit: float = 60.0):
    """Solve min |x| subject to Hx=t mod 2 via scipy/HiGHS MILP."""
    H = inst.H.tocsr().astype(float)
    r, p = H.shape
    # Hx - 2z = t. z is nonnegative because Hx >= 0.
    A = hstack([H, -2.0 * coo_matrix(np.eye(r))], format="csr")
    c = np.r_[np.ones(p), np.zeros(r)]
    max_row = np.asarray(H.sum(axis=1)).ravel() // 2 + 1
    lb = np.zeros(p + r)
    ub = np.r_[np.ones(p), max_row]
    result = milp(c, integrality=np.ones(p + r), bounds=Bounds(lb, ub),
                  constraints=LinearConstraint(A, inst.target, inst.target),
                  options={"time_limit": time_limit})
    chosen = None
    if result.x is not None:
        chosen = np.flatnonzero(result.x[:p] > .5).tolist()
    return result, chosen


def all_eight_clauses() -> List[Clause]:
    # Clause uniquely falsified by each assignment u: literal is x when u=0, not x when u=1.
    return [tuple((i + 1) if bit == 0 else -(i + 1) for i, bit in enumerate(u))
            for u in itertools.product((0, 1), repeat=3)]


def inconsistent_xor_cycle(length: int) -> List[Clause]:
    """An odd-parity cycle of 2-XOR constraints, encoded by two clauses each."""
    assert length >= 3
    clauses: List[Clause] = []
    for i in range(length):
        x, y = i + 1, (i + 1) % length + 1
        unequal = i == length - 1
        if unequal:  # x xor y = 1
            clauses.extend([(x, y), (-x, -y)])
        else:        # x xor y = 0
            clauses.extend([(x, -y), (-x, y)])
    return clauses


def xor3_clauses(vars_: Tuple[int, int, int], parity: int) -> List[Clause]:
    """Four 3-clauses encoding xor(vars_) = parity."""
    ans = []
    for u in itertools.product((0, 1), repeat=3):
        if sum(u) % 2 != parity:
            ans.append(tuple(v if bit == 0 else -v for v, bit in zip(vars_, u)))
    return ans


def k4_tseitin() -> List[Clause]:
    """Inconsistent Tseitin system on K4, with one odd vertex charge."""
    edges = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    edge_var = {e: k + 1 for k, e in enumerate(edges)}
    clauses: List[Clause] = []
    for v in range(4):
        incident = tuple(edge_var[e] for e in edges if v in e)
        clauses.extend(xor3_clauses(incident, 1 if v == 0 else 0))
    return clauses


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", choices=["all8", "xorcycle", "k4tseitin"], default="all8")
    ap.add_argument("--length", type=int, default=5)
    ap.add_argument("--d", type=int, default=2)
    ap.add_argument("--time", type=float, default=60)
    args = ap.parse_args()
    if args.family == "all8":
        clauses = all_eight_clauses()
    elif args.family == "xorcycle":
        clauses = inconsistent_xor_cycle(args.length)
    else:
        clauses = k4_tseitin()
    inst = build(clauses, args.d)
    res, chosen = exact_min_weight(inst, args.time)
    print({"clauses": len(clauses), "d": args.d, "groups": len(inst.groups),
           "rows": inst.H.shape[0], "columns": inst.H.shape[1],
           "status": res.status, "message": res.message,
           "optimum": None if res.fun is None else round(res.fun),
           "exact_feasible": chosen is not None})
    if chosen is not None:
        assert np.array_equal(np.asarray(inst.H.tocsr()[:, chosen].sum(axis=1)).ravel() % 2,
                              inst.target)


if __name__ == "__main__":
    main()
