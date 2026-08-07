#!/usr/bin/env python3
"""Finite counterexample to neighborhood diversity as a U0 class exclusion.

For n in {8,16,32}, freeze the standard fixed-block n-fold matrix

                  [ A A ... A ]
    C_n =          [ B 0 ... 0 ]       with A=B=[1].
                   [ 0 B ... 0 ]
                   [       ...   ]
                   [ 0 0 ... B ]

Thus C_n has one global row and n local rows, and one column per brick.
The same two 1-by-1 blocks are used at every size.  We also form the actual
identity augmentation D_n=[I|-C_n].

The colored support graphs have the most unfavorable possible ordinary
neighborhood-diversity behavior: every vertex is its own twin class, both for
C_n and D_n.  Nevertheless both graphs are trees, have exact treewidth one,
and D_n has an exact 2/3-balanced separator of size one.  Subdividing every
support edge once stays a tree and contracts faithfully.

This is a finite class-side counterexample only.  It proves that a growing
(standard colored) marked-neighborhood-diversity measurement cannot by itself
exclude fixed-block n-fold form.  It does not refute separator/treewidth
invariants, other nonstandard quotient notions, or U0.
"""

from __future__ import annotations

from hashlib import sha256
import json

SIZES = (8, 16, 32)
EXPECTED_HASH = "0a1d64fa0d24a208775310e2a6e7f2616b78355c0c5efeeec7ca50c07ea31696"


def fixed_nfold_matrix(n: int) -> tuple[tuple[int, ...], ...]:
    """Standard n-fold matrix from the fixed blocks A=B=[1]."""
    rows = [[1] * n]
    rows.extend([[int(i == j) for j in range(n)] for i in range(n)])
    return tuple(tuple(row) for row in rows)


def identity_augmented(matrix: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    row_count = len(matrix)
    return tuple(
        tuple(int(i == j) for j in range(row_count))
        + tuple(-value for value in matrix[i])
        for i in range(row_count)
    )


def support_graph(matrix: tuple[tuple[int, ...], ...]):
    nr, nc = len(matrix), len(matrix[0])
    vertices = tuple(range(nr + nc))
    edges = tuple(
        (i, nr + j)
        for i in range(nr)
        for j in range(nc)
        if matrix[i][j] != 0
    )
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    return vertices, edges, adjacency


def is_tree(vertices, edges, adjacency) -> bool:
    if not vertices:
        return False
    seen = set()
    stack = [vertices[0]]
    while stack:
        vertex = stack.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        stack.extend(adjacency[vertex] - seen)
    return len(seen) == len(vertices) and len(edges) == len(vertices) - 1


def colored_twin_classes(vertices, adjacency, colors):
    """Exact standard colored neighborhood-diversity partition.

    The general twin signature deletes the other vertex before comparison, so
    it handles both true and false twins.  The deliberately quadratic routine
    is independent of any special property of the frozen graphs.
    """
    remaining = set(vertices)
    classes = []
    while remaining:
        representative = min(remaining)
        cls = []
        for candidate in sorted(remaining):
            if colors[candidate] != colors[representative]:
                continue
            if (adjacency[candidate] - {representative}
                    == adjacency[representative] - {candidate}):
                cls.append(candidate)
        assert representative in cls
        classes.append(tuple(cls))
        remaining.difference_update(cls)
    return tuple(classes)


def leaf_elimination_certificate(vertices, edges, adjacency):
    """Emit and verify a width-one elimination ordering for a tree."""
    live = set(vertices)
    adj = {v: set(neighbors) for v, neighbors in adjacency.items()}
    ordering = []
    maximum_later_neighbors = 0
    while len(live) > 1:
        leaf = min(v for v in live if len(adj[v] & live) <= 1)
        later = adj[leaf] & live
        maximum_later_neighbors = max(maximum_later_neighbors, len(later))
        ordering.append(leaf)
        live.remove(leaf)
    ordering.extend(sorted(live))
    assert set(ordering) == set(vertices) and len(ordering) == len(vertices)
    assert maximum_later_neighbors <= 1
    assert edges  # an edge gives the matching lower bound treewidth >= 1
    return tuple(ordering), 1


def balanced_separator_one_certificate(vertices, edges, adjacency, separator):
    """Verify an exact size-one 2/3-balanced separator certificate."""
    remaining = set(vertices) - {separator}
    components = []
    unseen = set(remaining)
    while unseen:
        seed = min(unseen)
        component = set()
        stack = [seed]
        while stack:
            v = stack.pop()
            if v in component:
                continue
            component.add(v)
            stack.extend((adjacency[v] & remaining) - component)
        unseen.difference_update(component)
        components.append(component)

    bound = 2 * len(vertices) // 3
    # Exhaust all allocations of components for these star-of-branches trees
    # by a subset-sum DP, yielding a primal two-side partition.
    reachable = {0: ()}
    for index, component in enumerate(components):
        size = len(component)
        updated = dict(reachable)
        for total, selected in reachable.items():
            updated.setdefault(total + size, selected + (index,))
        reachable = updated
    chosen_total = next(
        total for total in sorted(reachable)
        if total <= bound and len(vertices) - 1 - total <= bound
    )
    chosen = set(reachable[chosen_total])
    side_a = set().union(*(components[i] for i in chosen)) if chosen else set()
    side_b = remaining - side_a
    assert len(side_a) <= bound and len(side_b) <= bound
    assert all(not ((u in side_a and v in side_b) or
                    (u in side_b and v in side_a)) for u, v in edges)

    # Exactness: a size-zero separator cannot split a connected graph between
    # two noncrossing sides, and putting the whole connected graph on one side
    # violates bound < |V|.
    assert is_tree(vertices, edges, adjacency)
    assert bound < len(vertices)
    return tuple(sorted(side_a)), tuple(sorted(side_b)), (separator,)


def subdivide_and_contract(vertices, edges):
    """Subdivide every edge once, verify treehood and faithful contraction."""
    old_count = len(vertices)
    expanded_edges = []
    collapse = {v: v for v in vertices}
    for index, (u, v) in enumerate(edges):
        auxiliary = old_count + index
        expanded_edges.extend(((u, auxiliary), (auxiliary, v)))
        collapse[auxiliary] = v
    expanded_vertices = tuple(range(old_count + len(edges)))
    expanded_adj = {v: set() for v in expanded_vertices}
    for u, v in expanded_edges:
        expanded_adj[u].add(v)
        expanded_adj[v].add(u)
    assert is_tree(expanded_vertices, tuple(expanded_edges), expanded_adj)
    contracted = {
        tuple(sorted((collapse[u], collapse[v])))
        for u, v in expanded_edges
        if collapse[u] != collapse[v]
    }
    assert contracted == {tuple(sorted(edge)) for edge in edges}
    return len(expanded_vertices), len(expanded_edges)


def audit(n: int):
    c = fixed_nfold_matrix(n)
    d = identity_augmented(c)
    assert len(c) == n + 1 and len(c[0]) == n
    assert c[0] == (1,) * n
    assert all(sum(c[i + 1]) == 1 and c[i + 1][i] == 1 for i in range(n))

    cv, ce, ca = support_graph(c)
    dv, de, da = support_graph(d)
    assert is_tree(cv, ce, ca)
    assert is_tree(dv, de, da)

    # Marks are a finite refinement of row/column roles; refinement can only
    # split, never merge, ordinary colored twin classes.
    ccolors = {}
    ccolors[0] = "global_row"
    for i in range(1, n + 1):
        ccolors[i] = "local_row"
    for v in range(n + 1, len(cv)):
        ccolors[v] = "brick_column"

    dcolors = {}
    dcolors[0] = "global_row"
    for i in range(1, n + 1):
        dcolors[i] = "local_row"
    first_column_vertex = n + 1
    dcolors[first_column_vertex] = "global_identity_column"
    for v in range(first_column_vertex + 1, first_column_vertex + n + 1):
        dcolors[v] = "local_identity_column"
    for v in range(first_column_vertex + n + 1, len(dv)):
        dcolors[v] = "brick_column"

    cclasses = colored_twin_classes(cv, ca, ccolors)
    dclasses = colored_twin_classes(dv, da, dcolors)
    assert len(cclasses) == len(cv) == 2 * n + 1
    assert len(dclasses) == len(dv) == 3 * n + 2
    assert all(len(cls) == 1 for cls in cclasses + dclasses)

    _, ctw = leaf_elimination_certificate(cv, ce, ca)
    _, dtw = leaf_elimination_certificate(dv, de, da)
    assert ctw == dtw == 1
    sides = balanced_separator_one_certificate(dv, de, da, separator=0)
    expanded_vertices, expanded_edges = subdivide_and_contract(dv, de)

    return {
        "n": n,
        "fixed_blocks": {"A": [[1]], "B": [[1]]},
        "C_shape": [n + 1, n],
        "D_shape": [n + 1, 2 * n + 1],
        "C_support_vertices": len(cv),
        "C_colored_neighborhood_diversity": len(cclasses),
        "D_support_vertices": len(dv),
        "D_colored_neighborhood_diversity": len(dclasses),
        "exact_treewidth_C": ctw,
        "exact_treewidth_D": dtw,
        "exact_D_two_thirds_balanced_separator": 1,
        "balanced_partition_sizes": [len(sides[0]), len(sides[1]), 1],
        "subdivision_vertices_edges": [expanded_vertices, expanded_edges],
    }


SPECIFICATION = {
    "sizes": SIZES,
    "fixed_blocks": {"A": ((1,),), "B": ((1,),)},
    "augmentation": "D=[I|-C]",
    "marks_C": ("global_row", "local_row", "brick_column"),
    "marks_D": ("global_row", "local_row", "global_identity_column",
                "local_identity_column", "brick_column"),
    "twin_relation": "same mark and N(u)\\{v}=N(v)\\{u}",
    "equality_expansion": "subdivide every support edge once",
}
SPECIFICATION_HASH = sha256(json.dumps(
    SPECIFICATION, sort_keys=True, separators=(",", ":")
).encode("ascii")).hexdigest()


def main():
    assert SPECIFICATION_HASH == EXPECTED_HASH, SPECIFICATION_HASH
    records = [audit(n) for n in SIZES]
    assert [r["C_colored_neighborhood_diversity"] for r in records] == [17, 33, 65]
    assert [r["D_colored_neighborhood_diversity"] for r in records] == [26, 50, 98]
    print(json.dumps({
        "specification_sha256": SPECIFICATION_HASH,
        "records": records,
        "finite_finding": (
            "standard colored marked neighborhood diversity grows maximally in "
            "this frozen fixed-block n-fold family although C and [I|-C] are trees"
        ),
        "U0_consequence": (
            "unbounded standard marked neighborhood diversity alone is not a valid "
            "fixed-block n-fold exclusion invariant"
        ),
        "scope": (
            "finite exact class-side counterexample at n=8,16,32; no asymptotic "
            "claim, no counterexample to separator/treewidth, and no resolution of U0"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
