#!/usr/bin/env python3
"""Exact low-weight kernel attack on a single F_289 product tag.

The surviving Fable-1 / Pro-2 mechanism appends all-pairs selectors with one
leading product value a_j b_k in O/P = F_289.  This verifier freezes the
smallest current all-pairs regime with the N=8 selector count and uses a
maximally distinct deterministic labeling.  It searches the 49 independent
2x2 rectangle directions of an 8x8 pair table.

Every rectangle preserves both pair-table marginals.  Its product transfer is
(a_0-a_j)(b_0-b_k) in F_289, a two-dimensional F_17 vector.  Exact search finds
a nonzero combination of at most three rectangle directions whose integer row
and column sums and F_289 leading transfer all vanish.  The companion Lean file
proves that such a coefficient relation exists for every three proposed
F_289 leading symbols; the Python output supplies one concrete low-weight
movement for an asymmetric, distinct-label stress instance.

Scope: this attacks a seam containing independent all-pairs selectors and only
one F_289 leading-symbol coordinate.  It does not prove reachability of the
movement in an unspecified enlarged Euclidean tile, and it does not address a
multi-coordinate or higher-graded replacement.
"""

from __future__ import annotations

from itertools import combinations
import hashlib
import json

P = 17
NONSQUARE = 3
N = 8


def add(x, y):
    return ((x[0] + y[0]) % P, (x[1] + y[1]) % P)


def neg(x):
    return ((-x[0]) % P, (-x[1]) % P)


def sub(x, y):
    return add(x, neg(y))


def mul(x, y):
    return (
        (x[0] * y[0] + NONSQUARE * x[1] * y[1]) % P,
        (x[0] * y[1] + x[1] * y[0]) % P,
    )


def power(x, exponent):
    result = (1, 0)
    while exponent:
        if exponent & 1:
            result = mul(result, x)
        x = mul(x, x)
        exponent >>= 1
    return result


def primitive_element():
    # F_289^* has order 288 = 2^5 * 3^2.  These two tests exclude every
    # proper subgroup whose order divides 288.
    for a in range(P):
        for b in range(P):
            value = (a, b)
            if value != (0, 0) and power(value, 288) == (1, 0):
                if power(value, 144) != (1, 0) and power(value, 96) != (1, 0):
                    return value
    raise AssertionError("no primitive element")


def centered(value):
    value %= P
    return value if value <= P // 2 else value - P


def det(x, y):
    return (x[0] * y[1] - x[1] * y[0]) % P


def rectangle(j, k):
    matrix = [[0] * N for _ in range(N)]
    matrix[0][0] += 1
    matrix[0][k] -= 1
    matrix[j][0] -= 1
    matrix[j][k] += 1
    return matrix


def combine_rectangles(directions, coefficients):
    result = [[0] * N for _ in range(N)]
    for (j, k), coefficient in zip(directions, coefficients):
        block = rectangle(j, k)
        for row in range(N):
            for column in range(N):
                result[row][column] += coefficient * block[row][column]
    return result


def transfer(matrix, left, right):
    result = (0, 0)
    for j in range(N):
        for k in range(N):
            scalar = matrix[j][k] % P
            result = add(result, mul((scalar, 0), mul(left[j], right[k])))
    return result


def dependency(vectors):
    """Return a nonzero F_17 dependency on one, two, or three 2-vectors."""
    assert 1 <= len(vectors) <= 3
    if len(vectors) == 1:
        return (1,) if vectors[0] == (0, 0) else None
    if len(vectors) == 2:
        x, y = vectors
        if det(x, y):
            return None
        if x == (0, 0):
            return (1, 0)
        if y == (0, 0):
            return (0, 1)
        coordinate = 0 if x[0] else 1
        return (y[coordinate] % P, (-x[coordinate]) % P)
    x, y, z = vectors
    candidate = (det(y, z), det(z, x), det(x, y))
    if candidate != (0, 0, 0):
        return candidate
    # Rank at most one: a dependency already exists on a pair.
    for first, second in combinations(range(3), 2):
        pair = dependency((vectors[first], vectors[second]))
        if pair is not None:
            result = [0, 0, 0]
            result[first], result[second] = pair
            return tuple(result)
    raise AssertionError("three vectors in F_17^2 must be dependent")


def score(matrix):
    flat = [entry for row in matrix for entry in row]
    return (sum(entry * entry for entry in flat), sum(abs(entry) for entry in flat), sum(entry != 0 for entry in flat))


# The first eight powers are distinct.  The right labels use a coprime exponent
# permutation and offset, avoiding the easy symmetric a_j=b_j degeneracy.
generator = primitive_element()
left_labels = tuple(power(generator, index) for index in range(N))
right_labels = tuple(power(generator, 5 * index + 7) for index in range(N))
assert len(set(left_labels)) == N
assert len(set(right_labels)) == N
assert left_labels != right_labels

basis = tuple((j, k) for j in range(1, N) for k in range(1, N))
symbols = {
    direction: mul(
        sub(left_labels[0], left_labels[direction[0]]),
        sub(right_labels[0], right_labels[direction[1]]),
    )
    for direction in basis
}

best = None
# Search exact dependencies in increasing support.  Support <=3 is guaranteed
# because the leading-symbol space has F_17 dimension two.
for support_size in (1, 2, 3):
    for directions in combinations(basis, support_size):
        residue_coefficients = dependency(tuple(symbols[d] for d in directions))
        if residue_coefficients is None:
            continue
        coefficients = tuple(centered(value) for value in residue_coefficients)
        if not any(coefficients):
            continue
        matrix = combine_rectangles(directions, coefficients)
        assert any(entry for row in matrix for entry in row)
        assert all(sum(row) == 0 for row in matrix)
        assert all(sum(matrix[row][column] for row in range(N)) == 0 for column in range(N))
        assert transfer(matrix, left_labels, right_labels) == (0, 0)
        record = (score(matrix), directions, coefficients, matrix)
        if best is None or record[:3] < best[:3]:
            best = record
    if best is not None:
        break

assert best is not None
movement_score, directions, coefficients, movement = best
certificate = {
    "left_labels": left_labels,
    "right_labels": right_labels,
    "directions": directions,
    "coefficients": coefficients,
    "movement": movement,
}
certificate_hash = hashlib.sha256(repr(certificate).encode("ascii")).hexdigest()


def main():
    print(json.dumps({
        "selected_proposals": [
            "Fable 1: generic skew-product avoidance (corrected enlarged-kernel gate)",
            "Pro 2: generic quaternion-product specialization",
        ],
        "causal_mechanism_tested": (
            "one F_289 product-leading coordinate is intended to separate every "
            "non-honest all-pairs movement"
        ),
        "expected_frontier_move": (
            "Q1 would advance only if the enlarged pair-selector seam had no "
            "short row/column-neutral movement with zero initial transfer"
        ),
        "falsification_condition": (
            "a nonzero integer combination of independent rectangle directions "
            "preserves both marginals and has zero F_289 product transfer"
        ),
        "field": "F_289 = F_17[u]/(u^2-3)",
        "primitive_element": list(generator),
        "selector_table_shape": [N, N],
        "independent_rectangle_directions": len(basis),
        "left_labels": [list(value) for value in left_labels],
        "right_labels": [list(value) for value in right_labels],
        "labels_distinct_on_each_side": True,
        "asymmetric_label_stress": True,
        "kernel_rectangle_directions": [list(value) for value in directions],
        "centered_integer_coefficients": list(coefficients),
        "kernel_movement": movement,
        "integer_row_sums": [sum(row) for row in movement],
        "integer_column_sums": [sum(movement[row][column] for row in range(N)) for column in range(N)],
        "product_transfer_mod_P": list(transfer(movement, left_labels, right_labels)),
        "movement_squared_frobenius_weight": movement_score[0],
        "movement_l1_weight": movement_score[1],
        "movement_support": movement_score[2],
        "certificate_sha256": certificate_hash,
        "finding": (
            "the asymmetric distinct-label all-pairs stress instance has an exact "
            "short internal zero-boundary movement with zero product initial symbol"
        ),
        "lean_companion": (
            "Verify_three_transfer_kernel proves that any three F_289 leading "
            "symbols, viewed in F_17^2, have a nonzero F_17 dependency"
        ),
        "scope": (
            "rules out separation of all independent rectangle directions by a "
            "single F_289 leading coordinate; reachability in an unspecified full "
            "tile and multi-coordinate/higher-grade repairs are not tested"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
