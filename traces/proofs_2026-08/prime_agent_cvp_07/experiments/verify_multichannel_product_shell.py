#!/usr/bin/env python3
"""Finite exact low-weight audit of a two-channel product-tag mutation.

Generation-5's two opponent reviews retain only the direct-sum/MDS product
transfer proposal.  This verifier applies its smallest discriminating test to
the hash-locked 18-variable margin completion already used in Generation 4.
It does not invent or claim the unavailable maximal-order NAND/fusion tile.

Each channel is a rank-one 4x2 table a_i b_j over
F_289 = F_17[u]/(u^2-3).  A deterministic exhaustive search over the alphabet
{0,1,u} synthesizes the first two-channel array whose transfer has rank three
on the three-dimensional 4x2 zero-margin seam.  No one-channel array can have
that rank.  The prior one-channel labels are retained as a regression.

For both COPY orientations and all eight legal cells, exact integer search
then enumerates every pair selector with the same row/column margins and total
squared distance below 17E while the NAND/COPY selectors stay fixed.  It tests
zero initial transfer modulo 17 componentwise and computes distance using the
fully emitted centered integer tag rows.  The old one-channel factor still has
energy-42 malformed states.  The synthesized two-channel factor has none in
this restricted shell and sends the certified weight-8 witness to a nonzero
vector syndrome.

This is finite evidence only for the frozen margin-preserving pair shell.  It
is not a complete Graver audit, does not enumerate changed NAND/COPY blocks,
DROP or false fibers, and proves neither Q1 nor any all-size statement.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import hashlib
import json

P = 17
NONSQUARE = 3
PAIR_ROWS = 4
PAIR_COLUMNS = 2
NAND_SIZE = 8
COPY_SIZE = 2
PAIR_SIZE = 8
VARIABLES = NAND_SIZE + COPY_SIZE + PAIR_SIZE
PAIR_OFFSET = NAND_SIZE + COPY_SIZE

NAND_LEGAL = ((0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0))
NAND_SIGNATURE_INDICES = (1, 2, 6, 6, 6, 6, 6, 9)
NAND_CODE = tuple(
    tuple(int(bit) for bit in f"{index:04b}")
    for index in NAND_SIGNATURE_INDICES
)
COPY_CODE = ((0, 1), (1, 0))
OLD_A_LABELS = ((0, 0), (1, 0), (0, 1), (1, 1))
B_LABELS = ((0, 0), (1, 0))
SYNTHESIS_ALPHABET = ((0, 0), (1, 0), (0, 1))
KNOWN_WITNESS = (-1, 1, 1, -1, 1, -1, -1, 1)


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
    minor = tuple(code_rows[position] for position in active)
    minor_inverse = inverse(minor)
    rows = []
    for position in range(len(code_rows)):
        if position in active:
            continue
        coefficients = row_matrix(code_rows[position], minor_inverse)
        row = [Fraction(0)] * len(code_rows)
        row[position] = 1
        for active_position, coefficient in zip(active, coefficients):
            row[active_position] -= coefficient
        rows.append(tuple(row))
    for boundary_row in boundary_rows:
        coefficients = row_matrix(boundary_row, minor_inverse)
        row = [Fraction(0)] * len(code_rows)
        for active_position, coefficient in zip(active, coefficients):
            row[active_position] += coefficient
        rows.append(tuple(row))
    assert all(value.denominator == 1 for row in rows for value in row)
    result = tuple(tuple(int(value) for value in row) for row in rows)
    assert abs(determinant(result)) == 1
    return result


NAND_BOUNDARY_ROWS = ((1, 1, 1, 1),) + tuple(
    tuple(word[coordinate] for word in NAND_LEGAL)
    for coordinate in range(3)
)
NAND_MODULE = affine_module(NAND_CODE, NAND_BOUNDARY_ROWS)
COPY_MODULE = affine_module(COPY_CODE, ((1, 1), (0, 1)))


def qmul(left, right, modulus=None):
    result = (
        left[0] * right[0] + NONSQUARE * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )
    if modulus is None:
        return result
    return tuple(value % modulus for value in result)


def tag_table(a_labels):
    return tuple(
        tuple(qmul(a_labels[row], B_LABELS[column]) for column in range(PAIR_COLUMNS))
        for row in range(PAIR_ROWS)
    )


def rectangle_basis_move(row):
    """Zero-margin rectangle using row 0 and the requested row 1..3."""
    move = [0] * PAIR_SIZE
    move[0] += 1
    move[1] -= 1
    move[2 * row] -= 1
    move[2 * row + 1] += 1
    return tuple(move)


SEAM_BASIS = tuple(rectangle_basis_move(row) for row in range(1, PAIR_ROWS))


def transfer(pair_move, tables, modulus=None):
    result = []
    for table in tables:
        for component in range(2):
            value = sum(
                pair_move[2 * row + column] * table[row][column][component]
                for row in range(PAIR_ROWS)
                for column in range(PAIR_COLUMNS)
            )
            result.append(value if modulus is None else value % modulus)
    return tuple(result)


def rank_mod_p(columns):
    if not columns:
        return 0
    matrix = [
        [columns[column][row] % P for column in range(len(columns))]
        for row in range(len(columns[0]))
    ]
    rank = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column] % P),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = pow(matrix[rank][column], -1, P)
        matrix[rank] = [(value * scale) % P for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank:
                continue
            scale = matrix[row][column] % P
            if scale:
                matrix[row] = [
                    (value - scale * pivot_value) % P
                    for value, pivot_value in zip(matrix[row], matrix[rank])
                ]
        rank += 1
    return rank


def seam_rank(tables):
    return rank_mod_p(tuple(transfer(move, tables, P) for move in SEAM_BASIS))


# Exhaust the declared finite synthesis family.  One F_289 channel contributes
# at most two F_17 rows, so rank three first becomes possible at two channels.
CHANNEL_CANDIDATES = tuple(product(SYNTHESIS_ALPHABET, repeat=PAIR_ROWS))
one_channel_ranks = tuple(seam_rank((tag_table(labels),)) for labels in CHANNEL_CANDIDATES)
assert max(one_channel_ranks) == 2
synthesis_pairs_tested = 0
SYNTHESIZED_LABELS = None
for first in CHANNEL_CANDIDATES:
    for second in CHANNEL_CANDIDATES:
        synthesis_pairs_tested += 1
        tables = (tag_table(first), tag_table(second))
        if seam_rank(tables) == 3:
            SYNTHESIZED_LABELS = (first, second)
            break
    if SYNTHESIZED_LABELS is not None:
        break
assert SYNTHESIZED_LABELS is not None
OLD_TABLES = (tag_table(OLD_A_LABELS),)
NEW_TABLES = tuple(tag_table(labels) for labels in SYNTHESIZED_LABELS)
OLD_MATRIX_SHA256 = {
    "forward": "f1f5706d6e129cb8dd5e2dad9751229d1e7187e2ed66ed8f73ea56ce0434e379",
    "reverse": "e2650cbca13d57b9067b403d6905d38a6d5c1b8fe2166567b4129604a2194d85",
}
assert seam_rank(OLD_TABLES) == 2
assert seam_rank(NEW_TABLES) == 3
assert transfer(KNOWN_WITNESS, OLD_TABLES, P) == (0, 0)
assert transfer(KNOWN_WITNESS, NEW_TABLES, P) != (0,) * 4


def x_index(row, column):
    return PAIR_OFFSET + PAIR_COLUMNS * row + column


def oriented_data(orientation, tables):
    assert orientation in ("forward", "reverse")
    if orientation == "forward":
        return COPY_CODE, tables
    copy_code = tuple(tuple(row[1 - column] for column in range(2)) for row in COPY_CODE)
    oriented_tables = tuple(
        tuple(
            tuple(
                tuple(-value for value in table[row][1 - column])
                for column in range(PAIR_COLUMNS)
            )
            for row in range(PAIR_ROWS)
        )
        for table in tables
    )
    return copy_code, oriented_tables


def emitted_matrix(orientation, tables):
    copy_code, oriented_tables = oriented_data(orientation, tables)
    rows = []
    for module_row in NAND_MODULE:
        rows.append(tuple(module_row) + (0,) * (VARIABLES - NAND_SIZE))
    for module_row in COPY_MODULE:
        rows.append((0,) * NAND_SIZE + tuple(module_row) + (0,) * PAIR_SIZE)
    for physical in range(NAND_SIZE):
        row = [0] * VARIABLES
        row[physical] = 1
        for state in range(PAIR_ROWS):
            for copy_state in range(PAIR_COLUMNS):
                row[x_index(state, copy_state)] -= NAND_CODE[physical][state]
        rows.append(tuple(row))
    for physical in range(COPY_SIZE):
        row = [0] * VARIABLES
        row[NAND_SIZE + physical] = 1
        for state in range(PAIR_ROWS):
            for copy_state in range(PAIR_COLUMNS):
                row[x_index(state, copy_state)] -= copy_code[physical][copy_state]
        rows.append(tuple(row))
    for table in oriented_tables:
        for component in range(2):
            row = [0] * VARIABLES
            for state in range(PAIR_ROWS):
                for copy_state in range(PAIR_COLUMNS):
                    row[x_index(state, copy_state)] = table[state][copy_state][component]
            rows.append(tuple(row))
    return tuple(rows)


for _orientation, _expected_hash in OLD_MATRIX_SHA256.items():
    _matrix_hash = hashlib.sha256(
        json.dumps(
            emitted_matrix(_orientation, OLD_TABLES), separators=(",", ":")
        ).encode("ascii")
    ).hexdigest()
    assert _matrix_hash == _expected_hash


def legal_vector(orientation, state, copy_state):
    copy_code, _ = oriented_data(orientation, ())
    nand = tuple(NAND_CODE[physical][state] for physical in range(NAND_SIZE))
    copy_selector = tuple(copy_code[physical][copy_state] for physical in range(COPY_SIZE))
    pair = tuple(
        int(row == state and column == copy_state)
        for row in range(PAIR_ROWS)
        for column in range(PAIR_COLUMNS)
    )
    return nand + copy_selector + pair


def squared_distance(factor, target, vector):
    image = matrix_vector(factor, vector)
    return sum((value - goal) ** 2 for value, goal in zip(image, target))


def same_margin_pair_shell(state, copy_state, max_pair_anchor_energy):
    """Enumerate the complete declared shell using four first-column values."""
    wanted_first_column_sum = int(copy_state == 0)
    values = range(-8, 10)
    for first_column in product(values, repeat=PAIR_ROWS):
        if sum(first_column) != wanted_first_column_sum:
            continue
        pair = []
        for row, value in enumerate(first_column):
            pair.extend((value, int(row == state) - value))
        pair = tuple(pair)
        energy = sum((2 * value - 1) ** 2 for value in pair)
        if energy <= max_pair_anchor_energy:
            yield pair


LEGAL_ENERGY = VARIABLES
THRESHOLD = 17 * LEGAL_ENERGY
assert LEGAL_ENERGY == 18 and THRESHOLD == 306
ANCHOR_FIXED_BLOCK_ENERGY = NAND_SIZE + COPY_SIZE
PAIR_ANCHOR_BUDGET = THRESHOLD - ANCHOR_FIXED_BLOCK_ENERGY - 1


def audit(tables):
    records = []
    total_shell = 0
    zero_initial_malformed = []
    serialization = {}
    for orientation in ("forward", "reverse"):
        matrix = emitted_matrix(orientation, tables)
        factor = tuple(
            tuple(2 * int(row == column) for column in range(VARIABLES))
            for row in range(VARIABLES)
        ) + matrix
        _, oriented_tables = oriented_data(orientation, tables)
        orientation_records = []
        for state in range(PAIR_ROWS):
            for copy_state in range(PAIR_COLUMNS):
                legal = legal_vector(orientation, state, copy_state)
                rhs = matrix_vector(matrix, legal)
                target = (1,) * VARIABLES + rhs
                assert squared_distance(factor, target, legal) == LEGAL_ENERGY
                legal_pair = legal[PAIR_OFFSET:]
                cell_shell = list(same_margin_pair_shell(state, copy_state, PAIR_ANCHOR_BUDGET))
                total_shell += len(cell_shell)
                bad = []
                for pair in cell_shell:
                    if pair == legal_pair:
                        continue
                    move = tuple(after - before for after, before in zip(pair, legal_pair))
                    syndrome = transfer(move, oriented_tables, P)
                    if syndrome != (0,) * (2 * len(tables)):
                        continue
                    candidate = legal[:PAIR_OFFSET] + pair
                    energy = squared_distance(factor, target, candidate)
                    if energy < THRESHOLD:
                        bad.append((energy, pair, move, syndrome))
                bad.sort()
                zero_initial_malformed.extend(
                    (orientation, state, copy_state) + item for item in bad
                )
                orientation_records.append({
                    "cell": [state, copy_state],
                    "same_margin_pair_vectors_checked": len(cell_shell),
                    "zero_initial_malformed_below_17E": len(bad),
                    "minimum_bad_energy": bad[0][0] if bad else None,
                })
        serialization[orientation] = {
            "matrix": matrix,
            "factor_shape": [len(factor), VARIABLES],
            "records": orientation_records,
        }
        records.extend(orientation_records)
    return {
        "records": records,
        "total_shell": total_shell,
        "bad": zero_initial_malformed,
        "serialization": serialization,
    }


old_audit = audit(OLD_TABLES)
new_audit = audit(NEW_TABLES)
assert old_audit["bad"]
assert min(item[3] for item in old_audit["bad"]) == 42
assert not new_audit["bad"]
assert old_audit["total_shell"] == new_audit["total_shell"] == 2 * 8 * 447

payload = {
    "nand_signature_indices": NAND_SIGNATURE_INDICES,
    "nand_module": NAND_MODULE,
    "copy_module": COPY_MODULE,
    "old_a_labels": OLD_A_LABELS,
    "synthesized_a_labels": SYNTHESIZED_LABELS,
    "b_labels": B_LABELS,
    "new_serialization": new_audit["serialization"],
}
SERIALIZATION_SHA256 = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("ascii")
).hexdigest()
EXPECTED_SERIALIZATION_SHA256 = "51b52cbfbce97be25caca9706508386ddbc53bea75ba5f7883e59edcdaac74d1"


def main():
    assert SERIALIZATION_SHA256 == EXPECTED_SERIALIZATION_SHA256
    print(json.dumps({
        "selected_surviving_proposal": (
            "Fable proposal 2 / Pro proposal 1: direct-sum product transfers"
        ),
        "causal_mechanism": (
            "two rank-one F_289 product channels provide four F_17 coordinates, "
            "enough to inject the frozen three-dimensional zero-margin seam"
        ),
        "expected_frontier_move": (
            "remove the certified one-channel weight-8 attack and every other "
            "zero-initial movement in the exact same-margin sub-17E pair shell"
        ),
        "falsification_condition": (
            "any malformed same-margin selector below 17E with zero vector transfer"
        ),
        "synthesis_alphabet": [list(value) for value in SYNTHESIS_ALPHABET],
        "one_channel_arrays_exhausted": len(CHANNEL_CANDIDATES),
        "maximum_one_channel_seam_rank": max(one_channel_ranks),
        "two_channel_pairs_tested_until_first_rank_three": synthesis_pairs_tested,
        "synthesized_a_labels": [
            [list(value) for value in labels] for labels in SYNTHESIZED_LABELS
        ],
        "b_labels": [list(value) for value in B_LABELS],
        "old_channel_count": 1,
        "new_channel_count": 2,
        "old_seam_rank_over_F17": seam_rank(OLD_TABLES),
        "new_seam_rank_over_F17": seam_rank(NEW_TABLES),
        "generation4_matrix_sha256": OLD_MATRIX_SHA256,
        "known_witness_old_syndrome": list(transfer(KNOWN_WITNESS, OLD_TABLES, P)),
        "known_witness_new_syndrome": list(transfer(KNOWN_WITNESS, NEW_TABLES, P)),
        "legal_energy_E": LEGAL_ENERGY,
        "threshold_17E": THRESHOLD,
        "orientations": ["forward", "reverse"],
        "legal_cells_checked": 16,
        "same_margin_shell_vectors_checked": new_audit["total_shell"],
        "old_zero_initial_malformed_count": len(old_audit["bad"]),
        "old_minimum_bad_energy": min(item[3] for item in old_audit["bad"]),
        "new_zero_initial_malformed_count": len(new_audit["bad"]),
        "serialization_sha256": SERIALIZATION_SHA256,
        "finding": (
            "the finite two-channel mutation blocks the known witness and has no "
            "zero-initial malformed state in the enumerated same-margin sub-17E shell"
        ),
        "scope": (
            "finite pass for the hash-locked margin-preserving pair shell only; "
            "changed NAND/COPY blocks, DROP, false fibers, the complete Graver basis, "
            "the missing maximal-order tile, Q1, Q2, and recursion remain open"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
