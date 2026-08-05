#!/usr/bin/env python3
"""Finite adversarial audit for the Generation-8 separator/treewidth proposal.

This is a synthetic control family, not the campaign's (currently unspecified) C_S.
For n in {8,16,32}, it checks exactly that:
  * D = [I | -C] has a certified K_{n/2,n/2} support subgraph;
  * D has support-2 and internal support-3 integral kernel moves;
  * a unimodular row rebasing turns D into [U | -I], whose incidence
    support graph is a tree.
It also exhausts z with support at most two and coefficients in {-1,+1}.
"""

from itertools import combinations, product

SIZES = (8, 16, 32)


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def matmul(a, b):
    assert len(a[0]) == len(b)
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def hstack(a, b):
    return [ra + rb for ra, rb in zip(a, b)]


def matvec(a, x):
    return [sum(v * w for v, w in zip(row, x)) for row in a]


def support(x):
    return sum(v != 0 for v in x)


def cumulative_matrix(n):
    # C[i,j] = 1 exactly when i >= j.
    return [[int(i >= j) for j in range(n)] for i in range(n)]


def difference_matrix(n):
    # U = C^{-1}: diagonal 1 and subdiagonal -1.
    u = eye(n)
    for i in range(1, n):
        u[i][i - 1] = -1
    return u


def incidence_is_tree(a):
    """Check the bipartite support graph exactly."""
    nr, nc = len(a), len(a[0])
    adj = [set() for _ in range(nr + nc)]
    edges = 0
    for i, row in enumerate(a):
        for j, value in enumerate(row):
            if value:
                adj[i].add(nr + j)
                adj[nr + j].add(i)
                edges += 1
    seen = set()
    stack = [0]
    while stack:
        v = stack.pop()
        if v in seen:
            continue
        seen.add(v)
        stack.extend(adj[v] - seen)
    return len(seen) == nr + nc and edges == nr + nc - 1


def bounded_low_weight_search(c):
    """Exhaust z of support 1 or 2 with nonzeros +/-1; return minima."""
    n = len(c)
    best = None
    witnesses = []
    by_z_support = {}
    for z_support in (1, 2):
        local_best = None
        for places in combinations(range(n), z_support):
            for signs in product((-1, 1), repeat=z_support):
                z = [0] * n
                for place, sign in zip(places, signs):
                    z[place] = sign
                y = matvec(c, z)
                x = y + z
                weight = support(x)
                if local_best is None or weight < local_best:
                    local_best = weight
                if best is None or weight < best:
                    best = weight
                    witnesses = [(y, z)]
                elif weight == best:
                    witnesses.append((y, z))
        by_z_support[z_support] = local_best
    return best, witnesses, by_z_support


def audit(n):
    i_n = eye(n)
    c = cumulative_matrix(n)
    u = difference_matrix(n)
    d = hstack(i_n, [[-v for v in row] for row in c])
    rebased = matmul(u, d)
    expected_rebased = hstack(u, [[-v for v in row] for row in i_n])

    assert matmul(u, c) == i_n
    assert rebased == expected_rebased
    assert incidence_is_tree(rebased)

    # Explicit finite K_{k,k} witness in the support graph of D: selected
    # rows are adjacent to every selected z-column.
    k = n // 2
    rows = list(range(n - k, n))
    z_columns = list(range(k))
    assert all(d[i][n + j] != 0 for i in rows for j in z_columns)

    # Boundary support-2 kernel move: z=e_(n-1), y=Cz=e_(n-1).
    z_boundary = [0] * n
    z_boundary[-1] = 1
    y_boundary = matvec(c, z_boundary)
    x_boundary = y_boundary + z_boundary
    assert matvec(d, x_boundary) == [0] * n
    assert support(x_boundary) == 2

    # Internal adjacent-difference moves have support 3.
    internal = []
    for j in range(n - 1):
        z = [0] * n
        z[j], z[j + 1] = 1, -1
        y = matvec(c, z)
        x = y + z
        assert matvec(d, x) == [0] * n
        assert support(x) == 3
        internal.append((j, x))

    best, witnesses, by_z_support = bounded_low_weight_search(c)
    assert best == 2
    assert by_z_support == {1: 2, 2: 3}
    assert any(z == z_boundary for _, z in witnesses)

    return {
        "n": n,
        "certified_complete_bipartite_order": k,
        "rebased_incidence_is_tree": True,
        "bounded_search": "z support <= 2, nonzeros in {-1,+1}",
        "minimum_total_kernel_support": best,
        "minimum_for_z_support_2": by_z_support[2],
        "internal_support_3_moves": len(internal),
    }


def main():
    results = [audit(n) for n in SIZES]
    print("Generation-8 separator/kernel degeneracy audit: PASS")
    for result in results:
        print(result)
    print(
        "FINITE FINDING: on this synthetic n=8,16,32 control family, "
        "increasing complete-bipartite support witnesses coexist with "
        "support-2/3 kernel moves and a row-equivalent tree presentation."
    )


if __name__ == "__main__":
    main()
