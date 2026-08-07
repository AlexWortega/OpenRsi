#!/usr/bin/env python3
"""Finite counterexamples to two underspecified support invariants proposed for U0.

For n in {8,16,32}, let B_n be the standard n-fold matrix of the fixed
1-by-1 bimatrix A_1=A_2=[1]: its first row is all ones and its remaining
n rows form I_n.  Thus B_n is *literally* a fixed-template n-fold matrix.

Two exact cautions are checked.

(1) The colored incidence graph of B_n (global row / local row / column
colors) has 2n+1 distinct open neighborhoods, and its column-intersection
(primal) graph is K_n.  Hence ordinary (even color-aware) neighborhood
diversity and primal treewidth are unbounded-looking on finite sizes despite
an explicit fixed n-fold presentation.  These cannot be class-exclusion
invariants without a different, formally specified quotient/support graph.

(2) Premultiply B_n by the unimodular lower-cumulative matrix U_n.  The
result T_n=U_n B_n has no zero entries, so its displayed incidence support is
K_{n+1,n} and has a growing exact 2/3-balanced separator.  Nevertheless the
explicit difference matrix V_n=U_n^{-1} sends T_n back to the same fixed
n-fold B_n.  Thus displayed incidence separators are not invariant under
unimodular rebasing of equality constraints.

This does NOT refute an U0 statement whose admissible grammar explicitly
forbids row rebasing and uses the bipartite incidence separator (B_n itself
has separator one).  It does show that such a statement is not, by itself,
a basis-robust tractability exclusion, and that the phrase ``marked
neighborhood diversity'' needs a nonstandard precise definition.
"""

from __future__ import annotations

from hashlib import sha256
import json

SIZES = (8, 16, 32)


def matmul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    assert len(a[0]) == len(b)
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def fixed_nfold(n: int) -> list[list[int]]:
    # The n-fold product of the fixed bimatrix A1=[1], A2=[1].
    return [[1] * n] + [[int(i == j) for j in range(n)] for i in range(n)]


def cumulative(nrows: int) -> list[list[int]]:
    return [[int(j <= i) for j in range(nrows)] for i in range(nrows)]


def difference(nrows: int) -> list[list[int]]:
    return [[int(i == j) - int(i == j + 1) for j in range(nrows)]
            for i in range(nrows)]


def identity(n: int) -> list[list[int]]:
    return [[int(i == j) for j in range(n)] for i in range(n)]


def colored_incidence_neighborhoods(b: list[list[int]]) -> list[tuple[str, tuple[int, ...]]]:
    rows, cols = len(b), len(b[0])
    result: list[tuple[str, tuple[int, ...]]] = []
    for i in range(rows):
        color = "global-row" if i == 0 else "local-row"
        result.append((color, tuple(rows + j for j in range(cols) if b[i][j])))
    for j in range(cols):
        result.append(("column", tuple(i for i in range(rows) if b[i][j])))
    return result


def exact_complete_bipartite_balanced_separator(p: int, q: int) -> tuple[int, tuple[int, ...]]:
    """Exhaust all six part-counts, modulo symmetry inside K_{p,q}."""
    total = p + q
    bound = 2 * total // 3
    best = total + 1
    witness: tuple[int, ...] | None = None
    # aL,bL,xL and aR,bR,xR partition the two bipartition classes.
    for a_l in range(p + 1):
        for b_l in range(p - a_l + 1):
            x_l = p - a_l - b_l
            for a_r in range(q + 1):
                # No edge may cross between side A and side B.
                if a_r and b_l:
                    continue
                for b_r in range(q - a_r + 1):
                    if b_r and a_l:
                        continue
                    x_r = q - a_r - b_r
                    if a_l + a_r > bound or b_l + b_r > bound:
                        continue
                    sep = x_l + x_r
                    if sep < best:
                        best = sep
                        witness = (a_l, b_l, x_l, a_r, b_r, x_r)
    assert witness is not None
    return best, witness


def main() -> None:
    records = []
    for n in SIZES:
        b = fixed_nfold(n)
        assert len(b) == n + 1 and len(b[0]) == n
        assert b[0] == [1] * n
        assert b[1:] == identity(n)

        # Every colored open neighborhood is distinct.  A further color
        # refinement can split these types but cannot merge any of them.
        neighborhoods = colored_incidence_neighborhoods(b)
        assert len(set(neighborhoods)) == 2 * n + 1

        # The primal/column-intersection graph is exactly K_n because the
        # fixed global row contains every column.
        primal_edges = {(i, j) for i in range(n) for j in range(i + 1, n)
                        if any(b[r][i] and b[r][j] for r in range(n + 1))}
        assert len(primal_edges) == n * (n - 1) // 2

        u = cumulative(n + 1)
        v = difference(n + 1)
        assert matmul(u, v) == identity(n + 1)
        assert matmul(v, u) == identity(n + 1)
        t = matmul(u, b)
        assert matmul(v, t) == b
        # Explicitly: column j is 1 through row j and 2 thereafter.
        assert all(t[i][j] == (1 if i <= j else 2)
                   for i in range(n + 1) for j in range(n))
        assert all(value != 0 for row in t for value in row)

        sep, sep_counts = exact_complete_bipartite_balanced_separator(n + 1, n)
        expected_sep = (2 * n + 3) // 3  # ceil((2n+1)/3)
        assert sep == expected_sep

        digest = sha256(json.dumps({"B": b, "U": u, "V": v, "T": t},
                                   separators=(",", ":")).encode()).hexdigest()
        records.append({
            "n": n,
            "fixed_template": {"A1": [[1]], "A2": [[1]], "bricks": n},
            "colored_open_neighborhood_types": len(set(neighborhoods)),
            "primal_graph": f"K_{n}",
            "primal_clique_size": n,
            "rebased_incidence_graph": f"K_{{{n+1},{n}}}",
            "exact_two_thirds_balanced_separator": sep,
            "separator_count_witness": sep_counts,
            "unimodular_inverse_verified": True,
            "row_rebases_back_to_fixed_nfold": True,
            "sha256": digest,
        })

    assert [r["colored_open_neighborhood_types"] for r in records] == [17, 33, 65]
    assert [r["exact_two_thirds_balanced_separator"] for r in records] == [6, 11, 22]
    print(json.dumps({"status": "PASS", "records": records}, indent=2))


if __name__ == "__main__":
    main()
