#!/usr/bin/env python3
"""Finite grade-zero audit of the natural redundant-NAND defect map.

The cross-reviewed finite-transducer proposal needs a nonzero leading defect
before a P^2 state can be normalized.  This verifier freezes the only integral
map actually emitted by the known N=8 redundant-signature NAND survivor: four
code-consistency rows followed by normalization and three boundary rows.  It
checks saturation exactly, solves every Boolean boundary fiber, and performs an
independent exhaustive signed search through squared anchor energy 64.

Result: three false NAND boundaries already have exact zero integer residual
(and hence zero class in F_289 and modulo P^2).  The cheapest cost 56.  Their
coefficients lie in the F_17 subfield, so Frobenius parity does not remove them.
Thus this natural defect-map instantiation cannot seed the proposed transducer.
This is a finite counterexample to that frozen instantiation only; it says
nothing universal about other quaternionic lifts, COPY tiles, or all-depth Q2.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import json

P = 17
NONSQUARE = 3
SHELL = 64


def determinant(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    answer = Fraction(1)
    sign = 1
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
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
        value = work[column][column]
        work[column] = [entry / value for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(work[row], work[column])
            ]
    return tuple(tuple(row[size:]) for row in work)


def row_mat(row, matrix):
    return tuple(
        sum(row[index] * matrix[index][column] for index in range(len(row)))
        for column in range(len(matrix[0]))
    )


def mat_vec(matrix, vector):
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(len(vector)))
        for row in range(len(matrix))
    )


def anchor_energy(vector):
    return sum((2 * value - 1) ** 2 for value in vector)


# F_289 = F_17[u]/(u^2-3), used only to check the claimed Frobenius parity.
def fadd(left, right):
    return ((left[0] + right[0]) % P, (left[1] + right[1]) % P)


def fmul(left, right):
    return (
        (left[0] * right[0] + NONSQUARE * left[1] * right[1]) % P,
        (left[0] * right[1] + left[1] * right[0]) % P,
    )


def fpow(value, exponent):
    answer = (1, 0)
    while exponent:
        if exponent & 1:
            answer = fmul(answer, value)
        value = fmul(value, value)
        exponent >>= 1
    return answer


assert pow(NONSQUARE, (P - 1) // 2, P) == P - 1
assert fmul((0, 1), (0, 1)) == (NONSQUARE, 0)
assert fpow((0, 1), P) == (0, P - 1)


# The hash-locked best N=8 survivor: signatures 0001, 0010, five 0110,
# and 1001.  Columns correspond to legal words 001, 011, 101, 110.
CODE_ROWS = (
    (0, 0, 0, 1),
    (0, 0, 1, 0),
    (0, 1, 1, 0),
    (0, 1, 1, 0),
    (0, 1, 1, 0),
    (0, 1, 1, 0),
    (0, 1, 1, 0),
    (1, 0, 0, 1),
)
LEGAL_WORDS = ((0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0))
FALSE_WORDS = ((0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 1))
ACTIVE_POSITIONS = (0, 1, 2, 7)
active_matrix = tuple(CODE_ROWS[position] for position in ACTIVE_POSITIONS)
assert abs(determinant(active_matrix)) == 1
active_inverse = inverse(active_matrix)

# Reconstruct the exact 8x8 emitted map.  The first four rows force duplicate
# signature coordinates to agree with the active code coordinates.  The last
# four emit normalization and all three Boolean ports.
emitted_rows = []
for position in range(8):
    if position in ACTIVE_POSITIONS:
        continue
    active_coefficients = row_mat(CODE_ROWS[position], active_inverse)
    row = [Fraction(0)] * 8
    row[position] = 1
    for active_position, coefficient in zip(ACTIVE_POSITIONS, active_coefficients):
        row[active_position] -= coefficient
    emitted_rows.append(tuple(row))

augmented_rows = ((1, 1, 1, 1),) + tuple(
    tuple(word[coordinate] for word in LEGAL_WORDS) for coordinate in range(3)
)
for augmented_row in augmented_rows:
    active_coefficients = row_mat(augmented_row, active_inverse)
    row = [Fraction(0)] * 8
    for active_position, coefficient in zip(ACTIVE_POSITIONS, active_coefficients):
        row[active_position] = coefficient
    emitted_rows.append(tuple(row))

EMITTED = tuple(tuple(int(value) for value in row) for row in emitted_rows)
assert determinant(EMITTED) == 1
# A square integer matrix of determinant +-1 has SNF invariant factors all 1.
SNF_DIAGONAL = (1,) * 8
EMITTED_INVERSE = inverse(EMITTED)
assert all(value.denominator == 1 for row in EMITTED_INVERSE for value in row)


def rhs(boundary):
    return (0, 0, 0, 0, 1) + tuple(boundary)


def exact_fiber(boundary):
    vector = mat_vec(EMITTED_INVERSE, rhs(boundary))
    assert all(value.denominator == 1 for value in vector)
    return tuple(int(value) for value in vector)


def zero_mod_p_residual(vector, boundary):
    image = mat_vec(EMITTED, vector)
    return all((value - target) % P == 0 for value, target in zip(image, rhs(boundary)))


# Exact singleton fibers, stronger than a bounded search for exact residual 0.
all_boundaries = tuple(product((0, 1), repeat=3))
exact_records = {}
for boundary in all_boundaries:
    vector = exact_fiber(boundary)
    assert mat_vec(EMITTED, vector) == rhs(boundary)
    exact_records[boundary] = (vector, anchor_energy(vector))

assert tuple(exact_records[word][1] for word in LEGAL_WORDS) == (8, 8, 8, 8)
assert tuple(exact_records[word][1] for word in FALSE_WORDS) == (160, 64, 56, 56)

# Independent exact low-weight search.  The recursion enumerates every integer
# vector of anchor energy <=64; the per-coordinate lower bound is one.
coordinate_values = tuple(sorted(range(-4, 6), key=lambda z: ((2 * z - 1) ** 2, z)))
shell_minima = {boundary: None for boundary in all_boundaries}
shell_witnesses = {}
searched = 0


def search(prefix, energy):
    global searched
    remaining_after_choice = 7 - len(prefix)
    if len(prefix) == 8:
        searched += 1
        vector = tuple(prefix)
        for boundary in all_boundaries:
            if zero_mod_p_residual(vector, boundary):
                old = shell_minima[boundary]
                if old is None or energy < old:
                    shell_minima[boundary] = energy
                    shell_witnesses[boundary] = vector
        return
    for value in coordinate_values:
        new_energy = energy + (2 * value - 1) ** 2
        if new_energy + remaining_after_choice <= SHELL:
            search(prefix + [value], new_energy)


search([], 0)
assert searched == 334592
assert tuple(shell_minima[word] for word in LEGAL_WORDS) == (8, 8, 8, 8)
assert tuple(shell_minima[word] for word in FALSE_WORDS) == (None, 64, 56, 56)

# The searched adverse witnesses are exact zero-residual singleton fibers, not
# merely congruent aliases.  Base-field coefficients are Frobenius-fixed.
adverse_records = []
for boundary in FALSE_WORDS[1:]:
    vector = shell_witnesses[boundary]
    assert vector == exact_records[boundary][0]
    residual = tuple(value - target for value, target in zip(mat_vec(EMITTED, vector), rhs(boundary)))
    assert residual == (0,) * 8
    residues = tuple((value % P, 0) for value in vector)
    assert tuple(fpow(value, P) for value in residues) == residues
    adverse_records.append({
        "boundary": list(boundary),
        "selector": list(vector),
        "anchor_energy": anchor_energy(vector),
        "integer_residual": list(residual),
        "class_mod_P": [0] * 8,
        "class_mod_P2": [0] * 8,
        "frobenius_fixed": True,
    })

# DROP itself is not the counterexample: the zero selector misses normalization.
drop = (0,) * 8
drop_residual = tuple(value - target for value, target in zip(mat_vec(EMITTED, drop), rhs((0, 0, 0))))
assert drop_residual == (0, 0, 0, 0, -1, 0, 0, 0)


def main():
    print(json.dumps({
        "proposal": "mutated finite adverse transducer (seed audit)",
        "causal_mechanism_tested": "a transducer state needs a nonzero leading P-class; the natural emitted residual is the candidate defect map",
        "expected_frontier_move": "authorize P^2 transition construction only if every adverse seed has nonzero leading class",
        "falsification_condition": "a false boundary has an exact signed selector with zero emitted residual",
        "field": "F_289=F_17[u]/(u^2-3)",
        "signature_indices": [1, 2, 6, 6, 6, 6, 6, 9],
        "emitted_matrix": [list(row) for row in EMITTED],
        "emitted_determinant": int(determinant(EMITTED)),
        "snf_diagonal": list(SNF_DIAGONAL),
        "shell_squared_energy": SHELL,
        "signed_vectors_searched": searched,
        "exact_false_energies_000_010_100_111": [exact_records[word][1] for word in FALSE_WORDS],
        "shell_false_minima_000_010_100_111": [shell_minima[word] for word in FALSE_WORDS],
        "grade_zero_false_witnesses": adverse_records,
        "drop_residual": list(drop_residual),
        "finding": "the natural defect map has exact grade-zero false seeds at energies 64,56,56, so no normalized nonzero P-leading state exists for them",
        "scope": "finite kill of the natural emitted-map transducer seed only; no claim about other lifts, COPY, depth two, or all depths",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
