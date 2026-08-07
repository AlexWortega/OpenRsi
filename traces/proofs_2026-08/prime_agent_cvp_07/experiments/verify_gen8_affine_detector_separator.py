#!/usr/bin/env python3
"""Finite audit of a frozen candidate separator layer for the U0 frontier.

The surviving Generation-8 proposal is the incidence-separator/treewidth
mechanism.  This verifier freezes, for S in {8,16,32}, a 0/1 candidate
separator matrix C_S whose support is the union of three affine matchings:

    j = i,  j = 3*i+1 (mod S),  j = 5*i+2 (mod S).

It then forms D_S = [I | -C_S].  Identity columns are private leaves, so the
measured graph is the marked detector subgraph induced by the rows of C_S and
the physical columns of C_S.  Two independent MILP backends compute the exact
minimum 2/3-balanced vertex separator.  Independently checked primal
partitions certify feasibility.  The exact optima also give finite treewidth
lower bounds (separator optimum minus one); faithful edge subdivision has the
original graph as a contraction minor.

As an auxiliary exact low-weight attack, all {-1,0,1} signed physical defects
through support 6 for S=8,16 and support 4 for S=32 are searched, modulo global
sign.  This is only a detector-map test, not a CVP energy or full signed-shell
audit.

This file does NOT serialize a universal circuit, selectors, targets, DROP, or
the four standard fixed-block grammars.  Consequently its strictly growing
finite values neither prove unbounded growth nor prove U0.  They only test the
causal mechanism on the hash-frozen candidate separator layer.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json
from math import comb

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix
import pulp

SIZES = (8, 16, 32)
BALANCE_NUMERATOR = 2
BALANCE_DENOMINATOR = 3
PREDECLARED_SEPARATOR_ALPHA_NUMERATOR = 1
PREDECLARED_SEPARATOR_ALPHA_DENOMINATOR = 4
SIGNED_SUPPORT_LIMIT = {8: 6, 16: 6, 32: 4}
EXPECTED_SEPARATOR_OPTIMA = {8: 4, 16: 6, 32: 9}
EXPECTED_DETERMINANTS = {8: -15, 16: -135, 32: -39015}
EXPECTED_SIGNED_MINIMA = {
    8: {1: 3, 2: 2, 3: 5, 4: 4, 5: 7, 6: 6},
    16: {1: 3, 2: 4, 3: 5, 4: 4, 5: 5, 6: 6},
    32: {1: 3, 2: 4, 3: 5, 4: 6},
}


def affine_neighbors(i: int, size: int) -> tuple[int, int, int]:
    return (i, (3 * i + 1) % size, (5 * i + 2) % size)


def candidate_matrix(size: int) -> tuple[tuple[int, ...], ...]:
    matrix = [[0] * size for _ in range(size)]
    for row in range(size):
        neighbors = affine_neighbors(row, size)
        assert len(set(neighbors)) == 3
        for column in neighbors:
            matrix[row][column] = 1
    result = tuple(tuple(row) for row in matrix)
    assert all(sum(row) == 3 for row in result)
    assert all(sum(result[row][column] for row in range(size)) == 3
               for column in range(size))
    return result


def detector_edges(matrix: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, int], ...]:
    size = len(matrix)
    return tuple(
        (row, size + column)
        for row in range(size)
        for column in range(size)
        if matrix[row][column]
    )


def bareiss_determinant(matrix: tuple[tuple[int, ...], ...]) -> int:
    """Fraction-free exact determinant with deterministic row pivoting."""
    work = [list(row) for row in matrix]
    n = len(work)
    sign = 1
    denominator = 1
    for pivot_index in range(n - 1):
        pivot_row = next(
            (row for row in range(pivot_index, n)
             if work[row][pivot_index] != 0),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = work[pivot_row], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, n):
            for column in range(pivot_index + 1, n):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                assert numerator % denominator == 0
                work[row][column] = numerator // denominator
        for row in range(pivot_index + 1, n):
            work[row][pivot_index] = 0
        denominator = pivot
    return sign * work[-1][-1]


def scipy_balanced_separator(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[int, tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    """Solve the exact integral 2/3-balanced-separator formulation with HiGHS."""
    variable_count = 3 * vertex_count
    objective = np.zeros(variable_count)
    objective[2 * vertex_count:] = 1
    rows: list[dict[int, int]] = []
    lower: list[float] = []
    upper: list[float] = []

    for vertex in range(vertex_count):
        rows.append({vertex: 1, vertex_count + vertex: 1,
                     2 * vertex_count + vertex: 1})
        lower.append(1)
        upper.append(1)
    for left, right in edges:
        rows.append({left: 1, vertex_count + right: 1})
        lower.append(-np.inf)
        upper.append(1)
        rows.append({vertex_count + left: 1, right: 1})
        lower.append(-np.inf)
        upper.append(1)

    balance_bound = BALANCE_NUMERATOR * vertex_count // BALANCE_DENOMINATOR
    rows.append({vertex: 1 for vertex in range(vertex_count)})
    lower.append(-np.inf)
    upper.append(balance_bound)
    rows.append({vertex_count + vertex: 1 for vertex in range(vertex_count)})
    lower.append(-np.inf)
    upper.append(balance_bound)

    constraint_matrix = lil_matrix((len(rows), variable_count), dtype=float)
    for row_index, coefficients in enumerate(rows):
        for variable, coefficient in coefficients.items():
            constraint_matrix[row_index, variable] = coefficient

    result = milp(
        objective,
        integrality=np.ones(variable_count),
        bounds=Bounds(0, 1),
        constraints=LinearConstraint(
            constraint_matrix.tocsr(), np.array(lower), np.array(upper)
        ),
        options={"mip_rel_gap": 0.0, "time_limit": 120},
    )
    assert result.success and result.status == 0, result.message
    assert result.fun is not None and result.x is not None
    optimum = int(round(float(result.fun)))
    assert abs(float(result.fun) - optimum) < 1e-6
    side_a = tuple(i for i in range(vertex_count) if result.x[i] > 0.5)
    side_b = tuple(i for i in range(vertex_count)
                   if result.x[vertex_count + i] > 0.5)
    separator = tuple(i for i in range(vertex_count)
                      if result.x[2 * vertex_count + i] > 0.5)
    return optimum, side_a, side_b, separator


def cbc_balanced_separator(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[int, tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    """Solve the same integer formulation independently with CBC."""
    problem = pulp.LpProblem("balanced_vertex_separator", pulp.LpMinimize)
    side_a_vars = [pulp.LpVariable(f"a_{i}", cat="Binary")
                   for i in range(vertex_count)]
    side_b_vars = [pulp.LpVariable(f"b_{i}", cat="Binary")
                   for i in range(vertex_count)]
    separator_vars = [pulp.LpVariable(f"x_{i}", cat="Binary")
                      for i in range(vertex_count)]
    problem += pulp.lpSum(separator_vars)
    for vertex in range(vertex_count):
        problem += (side_a_vars[vertex] + side_b_vars[vertex]
                    + separator_vars[vertex] == 1)
    for left, right in edges:
        problem += side_a_vars[left] + side_b_vars[right] <= 1
        problem += side_b_vars[left] + side_a_vars[right] <= 1
    balance_bound = BALANCE_NUMERATOR * vertex_count // BALANCE_DENOMINATOR
    problem += pulp.lpSum(side_a_vars) <= balance_bound
    problem += pulp.lpSum(side_b_vars) <= balance_bound
    status = problem.solve(pulp.PULP_CBC_CMD(msg=False, threads=1))
    assert status == pulp.LpStatusOptimal, pulp.LpStatus[status]
    optimum_value = pulp.value(problem.objective)
    assert optimum_value is not None
    optimum = int(round(optimum_value))
    assert abs(optimum_value - optimum) < 1e-6
    side_a = tuple(i for i, variable in enumerate(side_a_vars)
                   if pulp.value(variable) > 0.5)
    side_b = tuple(i for i, variable in enumerate(side_b_vars)
                   if pulp.value(variable) > 0.5)
    separator = tuple(i for i, variable in enumerate(separator_vars)
                      if pulp.value(variable) > 0.5)
    return optimum, side_a, side_b, separator


def verify_separator_partition(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    solution: tuple[int, tuple[int, ...], tuple[int, ...], tuple[int, ...]],
) -> None:
    optimum, side_a_tuple, side_b_tuple, separator_tuple = solution
    side_a = set(side_a_tuple)
    side_b = set(side_b_tuple)
    separator = set(separator_tuple)
    assert side_a.isdisjoint(side_b)
    assert side_a.isdisjoint(separator)
    assert side_b.isdisjoint(separator)
    assert side_a | side_b | separator == set(range(vertex_count))
    assert len(separator) == optimum
    balance_bound = BALANCE_NUMERATOR * vertex_count // BALANCE_DENOMINATOR
    assert len(side_a) <= balance_bound
    assert len(side_b) <= balance_bound
    assert all(not ((left in side_a and right in side_b)
                    or (left in side_b and right in side_a))
               for left, right in edges)


def verify_faithful_subdivision_contraction(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
) -> None:
    """Check the frozen width-one equality expansion contracts to the input graph."""
    expanded_edges: set[tuple[int, int]] = set()
    contraction_target = {vertex: vertex for vertex in range(vertex_count)}
    for edge_index, (left, right) in enumerate(edges):
        auxiliary = vertex_count + edge_index
        expanded_edges.add(tuple(sorted((left, auxiliary))))
        expanded_edges.add(tuple(sorted((auxiliary, right))))
        contraction_target[auxiliary] = right
    contracted_edges = {
        tuple(sorted((contraction_target[u], contraction_target[v])))
        for u, v in expanded_edges
        if contraction_target[u] != contraction_target[v]
    }
    assert contracted_edges == {tuple(sorted(edge)) for edge in edges}


def signed_low_weight_audit(
    matrix: tuple[tuple[int, ...], ...],
    support_limit: int,
) -> tuple[dict[int, int], dict[int, dict[str, object]], int]:
    """Exhaust the signed coefficient box, fixing the first sign to +1."""
    size = len(matrix)
    minima: dict[int, int] = {}
    witnesses: dict[int, dict[str, object]] = {}
    searched = 0
    for support_size in range(1, support_limit + 1):
        best_energy: int | None = None
        best_support: tuple[int, ...] | None = None
        best_coefficients: tuple[int, ...] | None = None
        for support in combinations(range(size), support_size):
            for remaining_signs in product((-1, 1), repeat=support_size - 1):
                coefficients = (1,) + remaining_signs
                searched += 1
                image = tuple(
                    sum(matrix[row][support[index]] * coefficients[index]
                        for index in range(support_size))
                    for row in range(size)
                )
                energy = sum(value * value for value in image)
                if best_energy is None or energy < best_energy:
                    best_energy = energy
                    best_support = support
                    best_coefficients = coefficients
        assert best_energy is not None
        assert best_support is not None and best_coefficients is not None
        minima[support_size] = best_energy
        witnesses[support_size] = {
            "support": best_support,
            "coefficients": best_coefficients,
        }
    expected_count = sum(
        comb(size, support_size) * (2 ** (support_size - 1))
        for support_size in range(1, support_limit + 1)
    )
    assert searched == expected_count
    return minima, witnesses, searched


SPECIFICATION = {
    "sizes": SIZES,
    "affine_matchings": ("i", "3*i+1 mod S", "5*i+2 mod S"),
    "matrices": {size: candidate_matrix(size) for size in SIZES},
    "marks": {
        "rows": "detector_separator",
        "C_columns": "physical",
        "identity_columns": "private_residual_leaf",
    },
    "balance": (BALANCE_NUMERATOR, BALANCE_DENOMINATOR),
    "predeclared_separator_alpha": (
        PREDECLARED_SEPARATOR_ALPHA_NUMERATOR,
        PREDECLARED_SEPARATOR_ALPHA_DENOMINATOR,
    ),
    "equality_expansion": "subdivide each support edge once and contract auxiliary to right endpoint",
    "signed_support_limit": SIGNED_SUPPORT_LIMIT,
}
SPECIFICATION_SHA256 = sha256(json.dumps(
    SPECIFICATION, sort_keys=True, separators=(",", ":")
).encode("ascii")).hexdigest()
EXPECTED_SPECIFICATION_SHA256 = "9e9591bbcba45333c6bcf83f092181f6510d201044070b4d3fb1842643dd0c90"


def main() -> None:
    assert SPECIFICATION_SHA256 == EXPECTED_SPECIFICATION_SHA256, SPECIFICATION_SHA256
    records = []
    previous_optimum = -1
    total_signed_candidates = 0
    for size in SIZES:
        matrix = candidate_matrix(size)
        determinant = bareiss_determinant(matrix)
        assert determinant == EXPECTED_DETERMINANTS[size]
        edges = detector_edges(matrix)
        assert len(edges) == 3 * size
        vertex_count = 2 * size

        highs_solution = scipy_balanced_separator(vertex_count, edges)
        cbc_solution = cbc_balanced_separator(vertex_count, edges)
        verify_separator_partition(vertex_count, edges, highs_solution)
        verify_separator_partition(vertex_count, edges, cbc_solution)
        separator_optimum = highs_solution[0]
        assert cbc_solution[0] == separator_optimum
        assert separator_optimum == EXPECTED_SEPARATOR_OPTIMA[size]
        assert separator_optimum > previous_optimum
        assert (separator_optimum * PREDECLARED_SEPARATOR_ALPHA_DENOMINATOR
                >= PREDECLARED_SEPARATOR_ALPHA_NUMERATOR * size)
        previous_optimum = separator_optimum

        verify_faithful_subdivision_contraction(vertex_count, edges)
        signed_minima, signed_witnesses, signed_candidates = signed_low_weight_audit(
            matrix, SIGNED_SUPPORT_LIMIT[size]
        )
        assert signed_minima == EXPECTED_SIGNED_MINIMA[size]
        assert all(energy >= support for support, energy in signed_minima.items())
        total_signed_candidates += signed_candidates

        records.append({
            "S": size,
            "C_shape": [size, size],
            "D_shape": [size, 2 * size],
            "determinant_C": determinant,
            "detector_vertices": vertex_count,
            "detector_edges": len(edges),
            "exact_balanced_separator": separator_optimum,
            "finite_treewidth_lower_bound": separator_optimum - 1,
            "highs_separator": highs_solution[3],
            "cbc_separator": cbc_solution[3],
            "signed_support_limit": SIGNED_SUPPORT_LIMIT[size],
            "signed_candidates_searched_modulo_global_sign": signed_candidates,
            "signed_minimum_image_energy": signed_minima,
            "signed_minimizers": signed_witnesses,
        })

    print(json.dumps({
        "selected_surviving_proposal": (
            "Fable 2 / Pro 2: incidence separator profile and treewidth minor"
        ),
        "causal_mechanism": (
            "three affine reconvergence matchings create a marked detector graph with "
            "growing balanced separators; faithful equality subdivisions retain that "
            "graph as a contraction minor"
        ),
        "expected_frontier_move": (
            "finite discrimination of a concrete separator invariant before attempting "
            "the four separate fixed-class closure lemmas required by U0"
        ),
        "falsification_condition": (
            "kill this frozen layer if exact separator optima fail strict growth or S/4, "
            "or if a searched signed defect has detector energy below its support"
        ),
        "specification_sha256": SPECIFICATION_SHA256,
        "records": records,
        "independent_exact_milp_backends": ["SciPy/HiGHS", "PuLP/CBC"],
        "total_signed_candidates_searched_modulo_global_sign": total_signed_candidates,
        "finding": (
            "the frozen candidate passes the preregistered finite separator and sparse "
            "detector tests at S=8,16,32"
        ),
        "scope": (
            "finite candidate-layer evidence only: no universal-circuit serializer, DROP "
            "objective, hereditary profile, class-wide closure theorem, U0 lemma, or "
            "asymptotic lower bound is established"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
