#!/usr/bin/env python3
"""Finite diagonal-splice attack on the current redundant NAND/COPY glue.

The surviving proposal wants a finite P-adic transducer whose composed adverse
states gain valuation.  Before such extra transfer coordinates are supplied,
the only explicit tile is the determinant-one N=8 redundant NAND module.  This
verifier composes that exact module with every saturated binary-signature COPY
code of rank N <= 8, in both port orientations.

A false 111 NAND fiber is the integral selector
    (0, 1, 2, 2, 2, 2, 2, -1)
of anchor energy 56.  It can be placed on both sides of a legal 11 COPY fiber.
All affine-span, boundary, and glue residuals are exactly zero, while the total
anchor energy is 112+N <= 120.  Exhaustive Boolean-boundary search also proves
112 is the minimum energy of two adverse copies of this NAND module.

This is a finite counterexample to plain affine-span/boundary gluing of the
explicit tile family.  It is not a counterexample to an as-yet-unspecified
quaternionic transfer coupling, nor an all-depth or asymptotic statement.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
from math import gcd
import hashlib
import json


def determinant(matrix):
    """Exact determinant of a square matrix."""
    work = [[Fraction(value) for value in row] for row in matrix]
    result = Fraction(1)
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
        result *= value
        work[column] = [entry / value for entry in work[column]]
        for row in range(column + 1, len(work)):
            scale = work[row][column]
            work[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(work[row], work[column])
            ]
    return sign * result


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


def anchor_energy(selector):
    return sum((2 * value - 1) ** 2 for value in selector)


def active_unit_minor(code_rows, rank):
    for positions in combinations(range(len(code_rows)), rank):
        matrix = tuple(code_rows[position] for position in positions)
        if abs(determinant(matrix)) == 1:
            return positions, matrix
    return None


def saturated(code_rows, rank):
    """Primitive full column rank, checked by the gcd of maximal minors."""
    minor_gcd = 0
    for positions in combinations(range(len(code_rows)), rank):
        value = abs(int(determinant(tuple(code_rows[p] for p in positions))))
        minor_gcd = gcd(minor_gcd, value)
    return minor_gcd == 1


def affine_module(code_rows, boundary_rows):
    """Emit affine-span rows and independent boundary rows.

    boundary_rows are rows on legal-state coefficients.  The returned square
    matrix has one row per selector coordinate and determinant +/-1.
    """
    rank = len(code_rows[0])
    active_data = active_unit_minor(code_rows, rank)
    assert active_data is not None
    active, active_matrix = active_data
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
    return tuple(rows)


# The exact surviving N=8 redundant NAND signature code.
NAND_LEGAL = ((0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0))
NAND_FALSE = tuple(word for word in product((0, 1), repeat=3) if word not in NAND_LEGAL)
NAND_SIGNATURE_INDICES = (1, 2, 6, 6, 6, 6, 6, 9)
NAND_CODE = tuple(
    tuple(int(bit) for bit in f"{index:04b}")
    for index in NAND_SIGNATURE_INDICES
)
NAND_BOUNDARY_ROWS = ((1, 1, 1, 1),) + tuple(
    tuple(word[coordinate] for word in NAND_LEGAL)
    for coordinate in range(3)
)
NAND_MODULE = affine_module(NAND_CODE, NAND_BOUNDARY_ROWS)
NAND_AFFINE_INVERSE = inverse(NAND_BOUNDARY_ROWS)


def nand_selector(boundary):
    coefficients = matrix_vector(NAND_AFFINE_INVERSE, (1,) + tuple(boundary))
    assert all(value.denominator == 1 for value in coefficients)
    selector = tuple(
        sum(signature[index] * coefficients[index] for index in range(4))
        for signature in NAND_CODE
    )
    rhs = (0,) * (len(NAND_CODE) - 4) + (1,) + tuple(boundary)
    assert matrix_vector(NAND_MODULE, selector) == rhs
    return tuple(int(value) for value in selector)


NAND_RECORDS = {
    boundary: (nand_selector(boundary), anchor_energy(nand_selector(boundary)))
    for boundary in product((0, 1), repeat=3)
}
assert tuple(NAND_RECORDS[word][1] for word in NAND_LEGAL) == (8, 8, 8, 8)
assert tuple(NAND_RECORDS[word][1] for word in NAND_FALSE) == (160, 64, 56, 56)
FALSE_111 = NAND_RECORDS[(1, 1, 1)][0]
assert FALSE_111 == (0, 1, 2, 2, 2, 2, 2, -1)
assert anchor_energy(FALSE_111) == 56


# Exhaustive exact search on two glued NAND boundaries.  The shared child
# output is either parent input; both orientations are tested.
def search_two_nands(parent_shared_port):
    records = []
    for a, b, shared, other, output in product((0, 1), repeat=5):
        child_boundary = (a, b, shared)
        parent_boundary = (
            (shared, other, output)
            if parent_shared_port == 0
            else (other, shared, output)
        )
        if child_boundary in NAND_LEGAL or parent_boundary in NAND_LEGAL:
            continue
        child_selector, child_energy = NAND_RECORDS[child_boundary]
        parent_selector, parent_energy = NAND_RECORDS[parent_boundary]
        records.append({
            "child_boundary": child_boundary,
            "parent_boundary": parent_boundary,
            "child_selector": child_selector,
            "parent_selector": parent_selector,
            "energy": child_energy + parent_energy,
        })
    return min(
        records,
        key=lambda record: (
            record["energy"], record["child_boundary"], record["parent_boundary"]
        ),
    ), len(records)


TWO_NAND_MINIMA = []
for orientation in (0, 1):
    minimum, adverse_cases = search_two_nands(orientation)
    assert adverse_cases == 8
    assert minimum["energy"] == 112
    TWO_NAND_MINIMA.append(minimum)


# Enumerate every saturated two-state binary-signature COPY code through N=8.
# The two columns encode legal COPY boundaries 00 and 11.  Saturation over Z
# also gives full rank over F_289 because every retained unit minor is nonzero
# modulo 17.
COPY_SIGNATURES = tuple(product((0, 1), repeat=2))
copy_counts = {}
copy_records = []
splice_hash = hashlib.sha256()
for rank_n in range(1, 9):
    searched = 0
    saturated_count = 0
    for multiset in combinations_with_replacement(range(4), rank_n):
        searched += 1
        code = tuple(COPY_SIGNATURES[index] for index in multiset)
        if rank_n < 2 or not saturated(code, 2):
            continue
        saturated_count += 1
        # Independent rows are normalization and the common COPY value.
        module = affine_module(code, ((1, 1), (0, 1)))
        selector_11 = tuple(row[1] for row in code)
        selector_00 = tuple(row[0] for row in code)
        affine_rhs_zeros = (0,) * (rank_n - 2)
        assert matrix_vector(module, selector_11) == affine_rhs_zeros + (1, 1)
        assert matrix_vector(module, selector_00) == affine_rhs_zeros + (1, 0)
        assert set(selector_11) <= {0, 1}
        assert anchor_energy(selector_11) == rank_n
        # Both port orientations see the same legal 11 boundary.  Place the
        # exact false-111 selector on each neighboring NAND tile.
        for orientation in ("input-output", "output-input"):
            total_energy = 56 + rank_n + 56
            assert total_energy <= 120
            payload = (
                rank_n,
                multiset,
                orientation,
                FALSE_111,
                selector_11,
                FALSE_111,
                total_energy,
            )
            splice_hash.update(repr(payload).encode("ascii"))
        copy_records.append((rank_n, multiset, selector_11, 112 + rank_n))
    copy_counts[rank_n] = {
        "searched": searched,
        "saturated": saturated_count,
    }

assert copy_counts[1]["saturated"] == 0
assert copy_records
assert min(record[3] for record in copy_records) == 114
assert max(record[3] for record in copy_records) == 120
assert all(counts["saturated"] > 0 for n, counts in copy_counts.items() if n >= 2)

# Numeric depth-two benchmark stated by the proposed quaternion energy lemma.
P = 17
P_SQUARED_TRACE_BENCHMARK = 2 * P * P
assert P_SQUARED_TRACE_BENCHMARK == 578
assert max(record[3] for record in copy_records) < P_SQUARED_TRACE_BENCHMARK


def main():
    representative = copy_records[0]
    print(json.dumps({
        "selected_proposal": "mutated finite adverse transducer / COPY audit",
        "causal_mechanism_tested": (
            "strict P-adic gain must prevent an adverse selector from passing "
            "unchanged through a legal COPY state"
        ),
        "nand_signature_indices": list(NAND_SIGNATURE_INDICES),
        "false_111_selector": list(FALSE_111),
        "false_111_energy": 56,
        "two_nand_adverse_cases_per_orientation": 8,
        "two_nand_exact_minimum_each_orientation": [
            {
                "child_boundary": list(record["child_boundary"]),
                "parent_boundary": list(record["parent_boundary"]),
                "energy": record["energy"],
            }
            for record in TWO_NAND_MINIMA
        ],
        "copy_counts_by_rank": copy_counts,
        "saturated_copy_codes_total": len(copy_records),
        "copy_orientations_per_code": 2,
        "representative_copy": {
            "rank": representative[0],
            "signature_indices": list(representative[1]),
            "legal_11_selector": list(representative[2]),
            "splice_energy": representative[3],
        },
        "splice_energy_range": [
            min(record[3] for record in copy_records),
            max(record[3] for record in copy_records),
        ],
        "p_squared_trace_benchmark": P_SQUARED_TRACE_BENCHMARK,
        "certificate_sha256": splice_hash.hexdigest(),
        "finding": (
            "every saturated binary-signature COPY code of rank at most 8 "
            "admits the zero-residual false111-COPY11-false111 diagonal splice "
            "under plain affine gluing"
        ),
        "falsification_condition_met": (
            "a reachable repeated adverse signed selector has no emitted "
            "transfer coordinate forcing depth-two prime energy"
        ),
        "scope": (
            "finite kill of the explicit affine-only glue; an augmented "
            "quaternionic coupling and any all-depth claim remain untested"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
