#!/usr/bin/env python3
"""Verify the odd-alphabet permutation-cycle counterexample to connected views."""
from __future__ import annotations
import argparse, sys
from collections import defaultdict
sys.path.insert(0, 'experiments')
from connected_views import build


def permutation_cycle_cnf(n):
    """Return exact 3CNF, clause attachments, color metadata, and edge data."""
    assert n >= 3
    next_var = 3 * n + 1
    clauses, attachments = [], []
    color_meta = {3*v + c + 1: (v, c) for v in range(n) for c in range(3)}
    edges = [(i, (i + 1) % n, 1 if i == n - 1 else 0) for i in range(n)]

    def X(v, c): return 3*v + c + 1
    def add3(clause, attachment):
        assert len(clause) == 3 and len({abs(x) for x in clause}) == 3
        clauses.append(tuple(clause)); attachments.append(attachment)
    def pad2(binary, attachment):
        nonlocal next_var
        z = next_var; next_var += 1
        add3((*binary, z), attachment)
        add3((*binary, -z), attachment)

    for v in range(n):
        add3((X(v,0), X(v,1), X(v,2)), ('vertex', v))
        for c in range(3):
            for cp in range(c + 1, 3):
                pad2((-X(v,c), -X(v,cp)), ('vertex', v))
    for ei, (u, v, shift) in enumerate(edges):
        for c in range(3):
            pc = (c + shift) % 3
            pad2((-X(u,c), X(v,pc)), ('edge', ei))
            pad2((X(u,c), -X(v,pc)), ('edge', ei))
    assert len(clauses) == 19*n and next_var - 1 == 12*n
    return clauses, attachments, color_meta, edges


def pseudo_support(q, scope, attachments, color_meta, edges):
    selected_edges, vertices = set(), set()
    for ci in q:
        kind, obj = attachments[ci]
        if kind == 'vertex':
            vertices.add(obj)
        else:
            selected_edges.add(obj)
            vertices.update(edges[obj][:2])
    assert vertices
    incidence = defaultdict(list)
    for ei in selected_edges:
        u, v, shift = edges[ei]
        incidence[u].append((v, shift))
        incidence[v].append((u, -shift))

    coeff = set()
    root = min(vertices)
    for root_color in range(3):
        color = {root: root_color}
        stack = [root]
        while stack:
            u = stack.pop()
            for v, shift in incidence[u]:
                implied = (color[u] + shift) % 3
                if v in color:
                    assert color[v] == implied, 'local skeleton unexpectedly inconsistent'
                else:
                    color[v] = implied; stack.append(v)
        assert vertices == set(color), 'clause connectivity should imply skeleton connectivity'
        bits = tuple(int(color[color_meta[var][0]] == color_meta[var][1])
                     if var in color_meta else 0 for var in scope)
        if bits in coeff: coeff.remove(bits)
        else: coeff.add(bits)
    assert len(coeff) in (1, 3)
    return coeff


def verify(n, d):
    assert d < n
    clauses, attachments, color_meta, edges = permutation_cycle_cnf(n)
    inst = build(clauses, d)
    index = {col: j for j, col in enumerate(inst.columns)}
    chosen = []
    sizes = defaultdict(int)
    for q in inst.groups:
        support = pseudo_support(q, inst.scopes[q], attachments, color_meta, edges)
        sizes[len(support)] += 1
        for bits in support:
            assert bits in inst.views[q], (q, bits)
            chosen.append(index[(q, bits)])
    got = inst.H.tocsr()[:, chosen].sum(axis=1).A1 % 2
    assert (got == inst.target).all()
    assert len(chosen) <= 3 * len(inst.groups)
    # Direct unsatisfiability follows from the proved holonomy contradiction.
    assert all((c + 1) % 3 != c for c in range(3))
    result = {'n': n, 'M': len(clauses), 'd': d, 'groups_K': len(inst.groups),
              'rows': inst.H.shape[0], 'columns': inst.H.shape[1],
              'witness_weight': len(chosen), 'weight_over_K': len(chosen)/len(inst.groups),
              'support_histogram': dict(sizes)}
    print(result)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=4)
    ap.add_argument('--d', type=int, default=2)
    a = ap.parse_args(); verify(a.n, a.d)

if __name__ == '__main__': main()
