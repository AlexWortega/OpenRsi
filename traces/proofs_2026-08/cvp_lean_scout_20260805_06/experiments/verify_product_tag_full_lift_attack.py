#!/usr/bin/env python3
"""Finite exact lift attack on the canonical single-product-tag completion.

The only Generation-4 proposal surviving both opponent reviews is the fixed-
witness full-matrix audit.  No upstream file serializes such a matrix, so this
verifier freezes the smallest canonical completion of the current data:

* the determinant-one N=8 redundant NAND module;
* the determinant-one rank-2 COPY module, in both column orientations;
* a 4x2 pair-selector table coupled to those modules by all row and column
  margins; and
* the current two integral coordinates of one product tag in Z[u]/(u^2-3).

For each of the eight legal pair cells and both orientations it emits the exact
integer factor C=[2I;A] and target y=[1;b].  Legal squared energy is E=18.
Exact shell enumeration finds a malformed signed pair selector of squared
energy 32 while the unchanged NAND/COPY blocks cost 10, so its full squared
energy is 42 < 17E=306.  Its residual, including both product-tag coordinates,
is exactly zero.  The associated movement is also checked conformally
primitive in the full emitted integer kernel.

This is finite evidence against this hash-locked marginal-only completion.  It
does not claim that an unspecified completion with additional pair-dependent
rows has been serialized or refuted, and it proves no universal or asymptotic
statement.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import hashlib
import json

NAND_LEGAL = ((0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0))
NAND_SIGNATURE_INDICES = (1, 2, 6, 6, 6, 6, 6, 9)
NAND_CODE = tuple(
    tuple(int(bit) for bit in f"{index:04b}")
    for index in NAND_SIGNATURE_INDICES
)
COPY_CODE = ((0, 1), (1, 0))
A_LABELS = ((0, 0), (1, 0), (0, 1), (1, 1))
B_LABELS = ((0, 0), (1, 0))
NONSQUARE = 3
PAIR_ROWS = 4
PAIR_COLUMNS = 2
NAND_SIZE = 8
COPY_SIZE = 2
PAIR_SIZE = 8
VARIABLES = NAND_SIZE + COPY_SIZE + PAIR_SIZE


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
    active = None
    # The frozen modules have a lexicographically first unit minor.
    from itertools import combinations
    for positions in combinations(range(len(code_rows)), rank):
        minor = tuple(code_rows[position] for position in positions)
        if abs(determinant(minor)) == 1:
            active = positions, minor
            break
    assert active is not None
    positions, minor = active
    minor_inverse = inverse(minor)
    rows = []
    for position in range(len(code_rows)):
        if position in positions:
            continue
        coefficients = row_matrix(code_rows[position], minor_inverse)
        row = [Fraction(0)] * len(code_rows)
        row[position] = 1
        for active_position, coefficient in zip(positions, coefficients):
            row[active_position] -= coefficient
        rows.append(tuple(row))
    for boundary_row in boundary_rows:
        coefficients = row_matrix(boundary_row, minor_inverse)
        row = [Fraction(0)] * len(code_rows)
        for active_position, coefficient in zip(positions, coefficients):
            row[active_position] += coefficient
        rows.append(tuple(row))
    integral = tuple(tuple(int(value) for value in row) for row in rows)
    assert all(value.denominator == 1 for row in rows for value in row)
    assert abs(determinant(integral)) == 1
    return integral


NAND_BOUNDARY_ROWS = ((1, 1, 1, 1),) + tuple(
    tuple(word[coordinate] for word in NAND_LEGAL)
    for coordinate in range(3)
)
NAND_MODULE = affine_module(NAND_CODE, NAND_BOUNDARY_ROWS)
COPY_MODULE = affine_module(COPY_CODE, ((1, 1), (0, 1)))
assert abs(determinant(NAND_MODULE)) == 1
assert abs(determinant(COPY_MODULE)) == 1


def qmul(left, right):
    return (
        left[0] * right[0] + NONSQUARE * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


BASE_TAG_TABLE = tuple(
    tuple(qmul(A_LABELS[row], B_LABELS[column]) for column in range(PAIR_COLUMNS))
    for row in range(PAIR_ROWS)
)


def oriented_data(orientation):
    assert orientation in ("forward", "reverse")
    if orientation == "forward":
        return COPY_CODE, BASE_TAG_TABLE
    copy_code = tuple(tuple(row[1 - column] for column in range(2)) for row in COPY_CODE)
    tag_table = tuple(
        tuple(tuple(-value for value in BASE_TAG_TABLE[row][1 - column]) for column in range(2))
        for row in range(4)
    )
    return copy_code, tag_table


def x_index(row, column):
    return NAND_SIZE + COPY_SIZE + PAIR_COLUMNS * row + column


def emitted_matrix(orientation):
    copy_code, tag_table = oriented_data(orientation)
    rows = []
    for module_row in NAND_MODULE:
        rows.append(tuple(module_row) + (0,) * (VARIABLES - NAND_SIZE))
    for module_row in COPY_MODULE:
        rows.append((0,) * NAND_SIZE + tuple(module_row) + (0,) * PAIR_SIZE)
    # Every pair row margin generates the corresponding physical NAND selector.
    for physical in range(NAND_SIZE):
        row = [0] * VARIABLES
        row[physical] = 1
        for state in range(PAIR_ROWS):
            for copy_state in range(PAIR_COLUMNS):
                row[x_index(state, copy_state)] -= NAND_CODE[physical][state]
        rows.append(tuple(row))
    # Every pair column margin generates the corresponding physical COPY selector.
    for physical in range(COPY_SIZE):
        row = [0] * VARIABLES
        row[NAND_SIZE + physical] = 1
        for state in range(PAIR_ROWS):
            for copy_state in range(PAIR_COLUMNS):
                row[x_index(state, copy_state)] -= copy_code[physical][copy_state]
        rows.append(tuple(row))
    # One product-leading coordinate has two integral components.
    for component in range(2):
        row = [0] * VARIABLES
        for state in range(PAIR_ROWS):
            for copy_state in range(PAIR_COLUMNS):
                row[x_index(state, copy_state)] = tag_table[state][copy_state][component]
        rows.append(tuple(row))
    assert len(rows) == 22
    return tuple(rows)


def legal_vector(orientation, state, copy_state):
    copy_code, _ = oriented_data(orientation)
    nand = tuple(NAND_CODE[physical][state] for physical in range(NAND_SIZE))
    copy_selector = tuple(copy_code[physical][copy_state] for physical in range(COPY_SIZE))
    pair = tuple(
        int(row == state and column == copy_state)
        for row in range(PAIR_ROWS)
        for column in range(PAIR_COLUMNS)
    )
    vector = nand + copy_selector + pair
    assert len(vector) == VARIABLES and set(vector) <= {0, 1}
    return vector


def anchor_energy(vector):
    return sum((2 * value - 1) ** 2 for value in vector)


def pair_key(pair, tag_table):
    row_margins = tuple(
        sum(pair[PAIR_COLUMNS * row + column] for column in range(PAIR_COLUMNS))
        for row in range(PAIR_ROWS)
    )
    column_margins = tuple(
        sum(pair[PAIR_COLUMNS * row + column] for row in range(PAIR_ROWS))
        for column in range(PAIR_COLUMNS)
    )
    tag = tuple(
        sum(
            pair[PAIR_COLUMNS * row + column] * tag_table[row][column][component]
            for row in range(PAIR_ROWS)
            for column in range(PAIR_COLUMNS)
        )
        for component in range(2)
    )
    return row_margins, column_margins, tag


def shell_vectors(max_energy):
    # Outside [-2,3], one coordinate already costs at least 49 > max_energy.
    values = (-2, -1, 0, 1, 2, 3)
    searched = 0

    def visit(prefix, energy):
        nonlocal searched
        if len(prefix) == PAIR_SIZE:
            searched += 1
            yield tuple(prefix), energy
            return
        remaining = PAIR_SIZE - len(prefix) - 1
        for value in values:
            new_energy = energy + (2 * value - 1) ** 2
            if new_energy + remaining <= max_energy:
                yield from visit(prefix + [value], new_energy)

    yield from visit([], 0)
    shell_vectors.searched = searched


PAIR_SHELL = 32
shell = list(shell_vectors(PAIR_SHELL))
SHELL_VECTORS_SEARCHED = shell_vectors.searched
assert shell and all(energy <= PAIR_SHELL for _, energy in shell)

records = []
global_payload = {
    "nand_signature_indices": NAND_SIGNATURE_INDICES,
    "nand_module": NAND_MODULE,
    "copy_module": COPY_MODULE,
    "base_tag_table": BASE_TAG_TABLE,
    "orientations": {},
}

for orientation in ("forward", "reverse"):
    matrix = emitted_matrix(orientation)
    _, tag_table = oriented_data(orientation)

    # Exact {-1,0,1} low-weight kernel search with NAND/COPY movement fixed to 0.
    kernel_moves = []
    for pair_move in product((-1, 0, 1), repeat=PAIR_SIZE):
        full_move = (0,) * (NAND_SIZE + COPY_SIZE) + pair_move
        if any(pair_move) and matrix_vector(matrix, full_move) == (0,) * len(matrix):
            kernel_moves.append(pair_move)
    assert len(kernel_moves) == 2
    witness = min(kernel_moves)
    assert tuple(-value for value in witness) == max(kernel_moves)
    assert sum(value * value for value in witness) == 8

    # A +/-1 witness is conformally primitive iff no retained proper support is
    # another full emitted-kernel move.
    conformal = []
    for mask in range(1 << PAIR_SIZE):
        submove = tuple(
            witness[index] if (mask >> index) & 1 else 0
            for index in range(PAIR_SIZE)
        )
        full_submove = (0,) * (NAND_SIZE + COPY_SIZE) + submove
        if matrix_vector(matrix, full_submove) == (0,) * len(matrix):
            conformal.append(submove)
    assert conformal == [(0,) * PAIR_SIZE, witness]

    orientation_records = []
    target_hashes = []
    for state in range(PAIR_ROWS):
        for copy_state in range(PAIR_COLUMNS):
            legal = legal_vector(orientation, state, copy_state)
            rhs = matrix_vector(matrix, legal)
            assert anchor_energy(legal) == 18

            legal_pair = legal[NAND_SIZE + COPY_SIZE:]
            target_key = pair_key(legal_pair, tag_table)
            malformed = [
                (energy, pair)
                for pair, energy in shell
                if pair != legal_pair and pair_key(pair, tag_table) == target_key
            ]
            assert malformed
            minimum_pair_energy = min(energy for energy, _ in malformed)
            minimum_pairs = sorted(pair for energy, pair in malformed if energy == minimum_pair_energy)
            assert minimum_pair_energy == 32

            attack_pair = minimum_pairs[0]
            attack = legal[:NAND_SIZE + COPY_SIZE] + attack_pair
            assert matrix_vector(matrix, attack) == rhs
            attack_energy = anchor_energy(attack)
            assert attack_energy == 42
            assert attack_energy < 17 * anchor_energy(legal)
            move = tuple(after - before for after, before in zip(attack, legal))
            assert move[:NAND_SIZE + COPY_SIZE] == (0,) * (NAND_SIZE + COPY_SIZE)
            assert move[NAND_SIZE + COPY_SIZE:] in kernel_moves

            # Exact CVP factor C=[2I;A], y=[1;b].
            factor = tuple(
                tuple(2 * int(row == column) for column in range(VARIABLES))
                for row in range(VARIABLES)
            ) + matrix
            target = (1,) * VARIABLES + rhs
            factor_image = matrix_vector(factor, attack)
            squared_distance = sum((value - goal) ** 2 for value, goal in zip(factor_image, target))
            assert squared_distance == attack_energy

            target_hash = hashlib.sha256(
                json.dumps(
                    {"factor": factor, "target": target},
                    separators=(",", ":"),
                ).encode("ascii")
            ).hexdigest()
            target_hashes.append(target_hash)
            orientation_records.append({
                "cell": [state, copy_state],
                "legal_energy": anchor_energy(legal),
                "attack_energy": attack_energy,
                "threshold_17E": 17 * anchor_energy(legal),
                "attack_pair_selector": list(attack_pair),
                "kernel_move": list(move[NAND_SIZE + COPY_SIZE:]),
                "factor_target_sha256": target_hash,
            })

    matrix_hash = hashlib.sha256(
        json.dumps(matrix, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    global_payload["orientations"][orientation] = {
        "matrix": matrix,
        "matrix_sha256": matrix_hash,
        "target_hashes": target_hashes,
    }
    records.append({
        "orientation": orientation,
        "emitted_matrix_shape": [len(matrix), len(matrix[0])],
        "emitted_matrix_sha256": matrix_hash,
        "bounded_kernel_vectors_searched": 3 ** PAIR_SIZE,
        "nonzero_kernel_moves_in_box": len(kernel_moves),
        "conformally_primitive_witness": list(witness),
        "conformal_kernel_submoves": len(conformal),
        "cells": orientation_records,
    })

SPECIFICATION_SHA256 = hashlib.sha256(
    json.dumps(global_payload, sort_keys=True, separators=(",", ":")).encode("ascii")
).hexdigest()
EXPECTED_SPECIFICATION_SHA256 = "eeb4bd797781134bc73c6ae7f285f7c9901e01083428e3e83932c237eef1e2ce"


def main():
    assert SPECIFICATION_SHA256 == EXPECTED_SPECIFICATION_SHA256
    print(json.dumps({
        "selected_surviving_proposal": (
            "Fable 1 / Pro 1 fixed-witness full-matrix lift-or-kill audit"
        ),
        "causal_mechanism": (
            "extra emitted NAND/COPY rows could save one product tag only if they "
            "block the old zero-tag pair movement or force its exact energy to 17E"
        ),
        "expected_frontier_move": (
            "clear the certified witness by a complete lift obstruction or kill the "
            "hash-locked candidate with a sub-17E full-factor witness"
        ),
        "falsification_condition": (
            "a conformally primitive movement survives every emitted row and both "
            "tag components, and gives a malformed exact fiber below 17E"
        ),
        "specification_sha256": SPECIFICATION_SHA256,
        "variables": VARIABLES,
        "factor_shape": [VARIABLES + 22, VARIABLES],
        "legal_energy_E": 18,
        "threshold_17E": 306,
        "minimum_attack_energy": 42,
        "pair_shell_energy": PAIR_SHELL,
        "pair_shell_vectors_searched": SHELL_VECTORS_SEARCHED,
        "orientations": records,
        "finding": (
            "all 16 legal cell/orientation fibers admit an exact malformed signed "
            "selector at squared distance 42; its residual and product transfer are "
            "zero, and its movement is conformally primitive in the emitted kernel"
        ),
        "scope": (
            "finite kill of this serialized marginal-only single-tag completion; "
            "the upstream proposals supply no different complete matrix, so no "
            "claim is made about unspecified extra pair-dependent rows or Q1"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
