#!/usr/bin/env python3
"""Generation-7 complete rational-affine port classification on the E6 shell.

Both cross-reviews authorize only Proposal 1.  The Generation-6 verifier fixed
and exactly certified the 27-point E6 Gosset Delaunay shell, but searched only
linear rows with coefficients in {-1,0,1}.  Here the coefficient bound is
removed completely.

The 27 translated vertices have affine rank six.  Seven lexicographically
chosen affine-basis vertices therefore determine every rational affine row.
We enumerate all 2^7 assignments of binary values to that basis, solve each
7x7 system exactly over Q, and test the resulting row on all 27 vertices.
Only the two constant rows survive.  Consequently no triple of rational affine
rows can map the shell onto any translated, signed, or per-port-relabelled
four-word NAND relation.

This closes rational affine port projections of this fixed E6 cell only.  It
makes no COPY, gluing, transfer-growth, or hardness claim.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product
import hashlib
import json
import sys
from pathlib import Path

EXPERIMENTS = Path(__file__).resolve().parent
sys.path.insert(0, str(EXPERIMENTS))
import verify_e6_gosset_port_map_obstruction as e6  # noqa: E402

VERTICES = e6.vertices
DIMENSION = 6


def matrix_rank(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    rank = 0
    if not matrix:
        return 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(rank, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for row in range(len(matrix)):
            if row != rank and matrix[row][column]:
                scale = matrix[row][column]
                matrix[row] = [
                    value - scale * pivot_value
                    for value, pivot_value in zip(matrix[row], matrix[rank])
                ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def solve_square(matrix, rhs):
    size = len(matrix)
    augmented = [
        [Fraction(value) for value in matrix[row]] + [Fraction(rhs[row])]
        for row in range(size)
    ]
    for column in range(size):
        pivot = next(row for row in range(column, size) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column or not augmented[row][column]:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(augmented[row], augmented[column])
            ]
    return tuple(augmented[row][-1] for row in range(size))


def affine_vector(vertex):
    return tuple(vertex) + (1,)


def evaluate(coefficients, vertex):
    return sum(coefficients[index] * vertex[index] for index in range(DIMENSION)) + coefficients[-1]


assert matrix_rank([affine_vector(vertex) for vertex in VERTICES]) == 7

# Deterministic lexicographic affine basis, with a machine-checked rank increase
# at every selection.
basis_indices = []
for index, vertex in enumerate(VERTICES):
    trial = basis_indices + [index]
    if matrix_rank([affine_vector(VERTICES[item]) for item in trial]) > len(basis_indices):
        basis_indices.append(index)
    if len(basis_indices) == 7:
        break
assert basis_indices == [0, 1, 2, 3, 4, 5, 10]
basis_matrix = [affine_vector(VERTICES[index]) for index in basis_indices]
assert matrix_rank(basis_matrix) == 7

surviving_rows = []
rejection_certificates = []
certificate_hash = hashlib.sha256()
value_histogram = Counter()
for assignment in product((0, 1), repeat=7):
    coefficients = solve_square(basis_matrix, assignment)
    values = tuple(evaluate(coefficients, vertex) for vertex in VERTICES)
    value_histogram[(len(set(values)), max(value.denominator for value in values))] += 1
    if set(values) <= {Fraction(0), Fraction(1)}:
        surviving_rows.append({
            "assignment": assignment,
            "coefficients": coefficients,
            "values": values,
        })
        continue
    bad_index = next(index for index, value in enumerate(values) if value not in (0, 1))
    certificate = {
        "assignment": assignment,
        "coefficients": coefficients,
        "bad_vertex_index": bad_index,
        "bad_value": values[bad_index],
    }
    rejection_certificates.append(certificate)
    certificate_hash.update(json.dumps({
        "assignment": list(assignment),
        "coefficients": [str(value) for value in coefficients],
        "bad_vertex_index": bad_index,
        "bad_value": str(values[bad_index]),
    }, separators=(",", ":")).encode() + b"\n")

assert len(surviving_rows) == 2
assert len(rejection_certificates) == 126
assert {
    tuple(row["coefficients"]) for row in surviving_rows
} == {
    (Fraction(0),) * 7,
    (Fraction(0),) * 6 + (Fraction(1),),
}
assert {frozenset(row["values"]) for row in surviving_rows} == {
    frozenset({Fraction(0)}), frozenset({Fraction(1)})
}

# Generate every translated and independently relabelled legal NAND relation.
translated_relations = set()
for flips in product((0, 1), repeat=3):
    relabelled = tuple(
        tuple(word[index] ^ flips[index] for index in range(3))
        for word in e6.NAND_LEGAL
    )
    for base in relabelled:
        translated_relations.add(tuple(sorted(
            tuple(word[index] - base[index] for index in range(3))
            for word in relabelled
        )))
assert len(translated_relations) == 32

# Constants and their signed/translated forms remain constants.  Exhaust the
# retained triples explicitly; each image is a singleton, never a legal
# four-word relation.
triple_tests = 0
triple_survivors = []
for first in surviving_rows:
    for second in surviving_rows:
        for third in surviving_rows:
            triple_tests += 1
            image = tuple(sorted(set(zip(first["values"], second["values"], third["values"]))))
            if image in translated_relations:
                triple_survivors.append(image)
assert triple_tests == 8
assert not triple_survivors


def row_record(row):
    return {
        "assignment": list(row["assignment"]),
        "coefficients": [str(value) for value in row["coefficients"]],
        "image_size": len(set(row["values"])),
    }


def main():
    print(json.dumps({
        "source_shell": "exact 27-vertex E6 Gosset shell from Generation 6",
        "affine_dimension": 6,
        "augmented_affine_rank": 7,
        "affine_basis_indices": basis_indices,
        "basis_assignment_count": 128,
        "exact_systems_solved": 128,
        "rejected_nonbinary_rows": len(rejection_certificates),
        "rejection_certificates_sha256": certificate_hash.hexdigest(),
        "surviving_binary_rows": len(surviving_rows),
        "surviving_rows": [row_record(row) for row in surviving_rows],
        "translated_signed_relabelled_nand_relations": len(translated_relations),
        "retained_row_triples_tested": triple_tests,
        "nand_map_survivors": len(triple_survivors),
        "classification_result": "every rational affine binary-valued row on the E6 shell is constant",
        "copy_and_transfer_status": "not authorized after coefficient-unbounded NAND affine-map failure",
        "finding": "no rational affine projection maps the fixed E6 shell onto the four legal NAND words",
        "scope": "complete no-go for rational affine ports on this finite shell; nonlinear/redundant ports remain open",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
