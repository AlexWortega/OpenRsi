#!/usr/bin/env python3
"""Finite fixed-witness lift audit for the smallest serialized product-tag seam.

The Generation-4 cross-reviews retain only the hash-locked lift-or-kill test.
No complete maximal-order NAND/COPY candidate was supplied, so this verifier
serializes the smallest completion determined by the frozen data already in the
campaign: the N=8 redundant NAND module, the determinant-one rank-2 COPY
module, a 4x2 all-pairs table, every row/column marginal equation, and the two
integer coordinates of the current product tag in Z[u]/(u^2-3).  Anchor rows
are 2I with target 1.  All consistency, normalization, port, glue, and tag rows
are included in one exact integer factor.  Both COPY orientations are tested.

For every legal NAND/COPY pair, the target is the image of its binary selector
under the non-anchor rows.  Thus every legal fiber has squared energy E=18.
Exact search of all {-1,0,1}^8 pair-table movements finds the known movement
and its negative.  They leave every non-anchor row unchanged in both COPY
orientations.  Translating each legal selector by the cheaper sign gives a
malformed signed pair table of squared energy 42, below 17E=306.

This is a finite kill only of this newly explicit smallest completion.  It is
not the absent maximal-order O/P^2 candidate, a complete fusion tile, Q1, Q2,
or an all-size claim.  Its purpose is to show that margin-only completion of
the supplied partial data does not rescue the certified movement.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import hashlib
import json

NAND_LEGAL = ((0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0))
NAND_SIGNATURE_INDICES = (1, 2, 6, 6, 6, 6, 6, 9)
NAND_CODE = tuple(
    tuple(int(bit) for bit in f"{index:04b}")
    for index in NAND_SIGNATURE_INDICES
)
COPY_CODE = ((0, 1), (1, 0))
ACTIVE_NAND = (0, 1, 2, 7)
A_LABELS = ((0, 0), (1, 0), (0, 1), (1, 1))
B_LABELS = ((0, 0), (1, 0))
NONSQUARE = 3

N_NAND = 8
N_COPY = 2
N_PAIR = 8
N_VARIABLES = N_NAND + N_COPY + N_PAIR
PAIR_OFFSET = N_NAND + N_COPY


def determinant(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    answer = Fraction(1)
    sign = 1
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        value = work[column][column]
        answer *= value
        work[column] = [entry / value for entry in work[column]]
        for row in range(column + 1, len(work)):
            scale = work[row][column]
            work[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(work[row], work[column])
            ]
    return sign * answer


def inverse(matrix):
    size = len(matrix)
    work = [
        [Fraction(value) for value in matrix[row]]
        + [Fraction(int(row == column)) for column in range(size)]
        for row in range(size)
    ]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [entry / scale for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(work[row], work[column])
            ]
    return tuple(tuple(row[size:]) for row in work)


def row_matrix(row, matrix):
    return tuple(
        sum(row[index] * matrix[index][column] for index in range(len(row)))
        for column in range(len(matrix[0]))
    )


def matrix_vector(matrix, vector):
    return tuple(
        sum(row[column] * vector[column] for column in range(len(vector)))
        for row in matrix
    )


def affine_module(code_rows, boundary_rows):
    rank = len(code_rows[0])
    active = next(
        positions
        for positions in combinations(range(len(code_rows)), rank)
        if abs(determinant(tuple(code_rows[position] for position in positions))) == 1
    )
    active_matrix = tuple(code_rows[position] for position in active)
    active_inverse = inverse(active_matrix)
    rows = []
    for position in range(len(code_rows)):
        if position in active:
            continue
        coefficients = row_matrix(code_rows[position], active_inverse)
        row = [Fraction(0)] * len(code_rows)
        row[position] = 1
        for active_position, coefficient in zip(active, coefficients):
            row[active_position] -= coefficient
        rows.append(tuple(row))
    for boundary_row in boundary_rows:
        coefficients = row_matrix(boundary_row, active_inverse)
        row = [Fraction(0)] * len(code_rows)
        for active_position, coefficient in zip(active, coefficients):
            row[active_position] += coefficient
        rows.append(tuple(row))
    assert len(rows) == len(code_rows)
    assert abs(determinant(rows)) == 1
    assert all(value.denominator == 1 for row in rows for value in row)
    return tuple(tuple(int(value) for value in row) for row in rows)


def decoder(code_rows, active):
    active_matrix = tuple(code_rows[position] for position in active)
    active_inverse = inverse(active_matrix)
    result = []
    for state in range(len(active_inverse)):
        row = [Fraction(0)] * len(code_rows)
        for coordinate, active_position in enumerate(active):
            row[active_position] = active_inverse[state][coordinate]
        result.append(tuple(row))
    assert all(value.denominator == 1 for row in result for value in row)
    return tuple(tuple(int(value) for value in row) for row in result)


def qmul(left, right):
    return (
        left[0] * right[0] + NONSQUARE * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def embed_row(block, offset):
    row = [0] * N_VARIABLES
    row[offset : offset + len(block)] = block
    return tuple(row)


def pair_index(nand_state, copy_state):
    return PAIR_OFFSET + 2 * nand_state + copy_state


NAND_BOUNDARY_ROWS = ((1, 1, 1, 1),) + tuple(
    tuple(word[coordinate] for word in NAND_LEGAL)
    for coordinate in range(3)
)
NAND_MODULE = affine_module(NAND_CODE, NAND_BOUNDARY_ROWS)
COPY_MODULE = affine_module(COPY_CODE, ((1, 1), (0, 1)))
NAND_DECODER = decoder(NAND_CODE, ACTIVE_NAND)
COPY_DECODER = decoder(COPY_CODE, (0, 1))
assert determinant(COPY_CODE) == -1

TAG_TABLE = tuple(
    tuple(qmul(A_LABELS[row], B_LABELS[column]) for column in range(2))
    for row in range(4)
)


def build_factor(orientation):
    assert orientation in ("forward", "reversed")
    rows = []
    names = []

    # Exact anchor factor: ||2z-1||^2.
    for coordinate in range(N_VARIABLES):
        row = [0] * N_VARIABLES
        row[coordinate] = 2
        rows.append(tuple(row))
        names.append(f"anchor_{coordinate}")

    for index, module_row in enumerate(NAND_MODULE):
        rows.append(embed_row(module_row, 0))
        names.append(f"nand_consistency_or_port_{index}")
    for index, module_row in enumerate(COPY_MODULE):
        rows.append(embed_row(module_row, N_NAND))
        names.append(f"copy_normalization_or_port_{index}")

    # Pair rows equal decoded NAND-state coefficients.
    for nand_state in range(4):
        row = [0] * N_VARIABLES
        for copy_state in range(2):
            row[pair_index(nand_state, copy_state)] += 1
        for coordinate, value in enumerate(NAND_DECODER[nand_state]):
            row[coordinate] -= value
        rows.append(tuple(row))
        names.append(f"pair_nand_margin_{nand_state}")

    # Pair columns equal decoded COPY-state coefficients.  Reversing COPY swaps
    # which decoded endpoint is attached to each table column.
    for copy_state in range(2):
        decoded_state = copy_state if orientation == "forward" else 1 - copy_state
        row = [0] * N_VARIABLES
        for nand_state in range(4):
            row[pair_index(nand_state, copy_state)] += 1
        for coordinate, value in enumerate(COPY_DECODER[decoded_state]):
            row[N_NAND + coordinate] -= value
        rows.append(tuple(row))
        names.append(f"pair_copy_margin_{copy_state}")

    # The current product transfer has two integer coordinates in Z[u].
    for tag_coordinate in range(2):
        row = [0] * N_VARIABLES
        for nand_state in range(4):
            for copy_state in range(2):
                row[pair_index(nand_state, copy_state)] = TAG_TABLE[nand_state][copy_state][tag_coordinate]
        rows.append(tuple(row))
        names.append(f"product_tag_{tag_coordinate}")

    assert len(rows) == 36
    return tuple(rows), tuple(names)


def legal_vector(nand_state, copy_state, orientation):
    logical_copy_state = copy_state if orientation == "forward" else 1 - copy_state
    nand = tuple(row[nand_state] for row in NAND_CODE)
    copy = tuple(row[logical_copy_state] for row in COPY_CODE)
    pair = tuple(
        int(row == nand_state and column == copy_state)
        for row in range(4)
        for column in range(2)
    )
    return nand + copy + pair


def squared_distance(factor, target, vector):
    image = matrix_vector(factor, vector)
    return sum((value - expected) ** 2 for value, expected in zip(image, target))


FACTORS = {}
TARGETS = {}
ROW_NAMES = {}
for orientation in ("forward", "reversed"):
    factor, row_names = build_factor(orientation)
    FACTORS[orientation] = factor
    ROW_NAMES[orientation] = row_names
    targets = {}
    for nand_state in range(4):
        for copy_state in range(2):
            vector = legal_vector(nand_state, copy_state, orientation)
            nonanchor_image = matrix_vector(factor[N_VARIABLES:], vector)
            target = (1,) * N_VARIABLES + nonanchor_image
            assert squared_distance(factor, target, vector) == N_VARIABLES
            targets[(nand_state, copy_state)] = target
    TARGETS[orientation] = targets

LEGAL_ENERGY = N_VARIABLES
THRESHOLD = 17 * LEGAL_ENERGY
assert LEGAL_ENERGY == 18
assert THRESHOLD == 306

# Search the exact low-weight pair-only box against every emitted non-anchor
# row, rather than checking margins and transfer in separate toy matrices.
kernel_moves = {}
searched = 0
for pair_move in product((-1, 0, 1), repeat=N_PAIR):
    searched += 1
    if not any(pair_move):
        continue
    full_move = (0,) * (N_NAND + N_COPY) + pair_move
    surviving = tuple(
        orientation
        for orientation in ("forward", "reversed")
        if matrix_vector(FACTORS[orientation][N_VARIABLES:], full_move)
        == (0,) * (len(FACTORS[orientation]) - N_VARIABLES)
    )
    if surviving:
        kernel_moves[pair_move] = surviving

assert searched == 3**8
assert len(kernel_moves) == 2
WITNESS = min(kernel_moves)
assert kernel_moves[WITNESS] == ("forward", "reversed")
assert tuple(-value for value in WITNESS) in kernel_moves
assert sum(value * value for value in WITNESS) == 8

records = []
for orientation in ("forward", "reversed"):
    factor = FACTORS[orientation]
    for nand_state in range(4):
        for copy_state in range(2):
            legal = legal_vector(nand_state, copy_state, orientation)
            target = TARGETS[orientation][(nand_state, copy_state)]
            candidates = []
            for pair_move in kernel_moves:
                full_move = (0,) * (N_NAND + N_COPY) + pair_move
                malformed = tuple(value + delta for value, delta in zip(legal, full_move))
                candidates.append((squared_distance(factor, target, malformed), pair_move, malformed))
            energy, pair_move, malformed = min(candidates)
            assert matrix_vector(factor[N_VARIABLES:], malformed) == matrix_vector(
                factor[N_VARIABLES:], legal
            )
            assert energy == 42
            assert energy < THRESHOLD
            records.append({
                "orientation": orientation,
                "nand_state": nand_state,
                "copy_state": copy_state,
                "energy": energy,
                "pair_move": list(pair_move),
                "malformed_pair": list(malformed[PAIR_OFFSET:]),
            })

payload = {
    "nand_signature_indices": NAND_SIGNATURE_INDICES,
    "copy_code": COPY_CODE,
    "a_labels": A_LABELS,
    "b_labels": B_LABELS,
    "factors": FACTORS,
    "targets": {
        orientation: {
            f"{nand_state},{copy_state}": target
            for (nand_state, copy_state), target in targets.items()
        }
        for orientation, targets in TARGETS.items()
    },
    "row_names": ROW_NAMES,
}
serialization_sha256 = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("ascii")
).hexdigest()
EXPECTED_SERIALIZATION_SHA256 = "ee19d247d0143f03228a77c40efd3ca106c18740f08be8304c1fd3004f36d711"
assert serialization_sha256 == EXPECTED_SERIALIZATION_SHA256


def main():
    print(json.dumps({
        "selected_surviving_proposal": "hash-locked fixed-witness lift-or-kill audit",
        "causal_mechanism": (
            "the certified zero-tag pair movement kills a product-tag candidate "
            "only when it lifts through every emitted NAND, COPY, marginal, and tag row"
        ),
        "expected_frontier_move": (
            "either block the fixed movement in a fully serialized seam or exhibit "
            "an exact malformed lift below 17 times the common legal energy"
        ),
        "falsification_condition": (
            "failure to serialize the intended maximal-order candidate, or a lifted "
            "malformed signed selector of squared energy below 17E"
        ),
        "candidate_scope": "smallest explicit margin-only completion of the supplied partial data",
        "maximal_order_candidate_supplied": False,
        "serialization_sha256": serialization_sha256,
        "factor_shape_each_orientation": [len(FACTORS["forward"]), N_VARIABLES],
        "row_groups": {
            "anchors": N_VARIABLES,
            "nand_consistency_normalization_ports": len(NAND_MODULE),
            "copy_normalization_ports": len(COPY_MODULE),
            "pair_margins": 6,
            "product_tag_coordinates": 2,
        },
        "copy_orientations": ["forward", "reversed"],
        "legal_fibers_checked": len(records),
        "common_legal_squared_energy": LEGAL_ENERGY,
        "soundness_threshold_17E": THRESHOLD,
        "bounded_pair_movements_searched": searched,
        "nonzero_pair_kernel_moves_in_box": len(kernel_moves),
        "witness": list(WITNESS),
        "witness_squared_coefficient_weight": sum(value * value for value in WITNESS),
        "minimum_lifted_squared_energy_in_searched_kernel": min(record["energy"] for record in records),
        "all_legal_pairs_have_energy_42_lift": all(record["energy"] == 42 for record in records),
        "representative_lift": records[0],
        "finding": (
            "the exact movement extends through every row of both serialized seam "
            "orientations and gives energy 42 < 306 for every legal pair"
        ),
        "scope": (
            "finite kill of this serialized smallest completion only; the absent "
            "maximal-order O/P^2 tile, fusion, Q1, Q2, and all-depth behavior remain open"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
