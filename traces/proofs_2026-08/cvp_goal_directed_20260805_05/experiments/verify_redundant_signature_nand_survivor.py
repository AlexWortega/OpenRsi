#!/usr/bin/env python3
"""Generation-12 exact N=8 redundant-signature NAND audit.

Both cross-reviews select only the bounded redundant binary-signature gate.
The four legal NAND configurations are encoded by four binary codewords of
length N. Each coordinate is one of the 16 possible four-bit signatures. This
verifier exhausts every N=8 multiplicity vector (the smallest authorized rank),
requires augmented rank four and a saturated integral affine decoder, and
computes every false fiber exactly.

A bounded survivor exists. Its complete emitted affine-span/boundary matrix is
unimodular, so every integer false fiber is a singleton. The four exact false
energies are 160,64,56,56, exceeding both the independently certified
prime-ideal trace threshold 34 and (17/16)*8.

The threshold is derived from an explicit maximal order in the definite
quaternion algebra (-3,-17): multiplication closure, trace discriminant 17^2,
and the two-sided prime O*j of index 17^2 are checked. Exact enumeration with a
dual coefficient bound proves minimum nonzero prime trace energy 34.

This is only a finite depth-one NAND survivor. It proves no COPY module,
depth-two growth, adverse-filtration lemma, or hardness result.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
from math import gcd
import json


# ---------- Exact linear algebra ----------
def determinant(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    result = Fraction(1)
    sign = 1
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
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


def mat_vec(matrix, vector):
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(len(vector)))
        for row in range(len(matrix))
    )


def row_mat(row, matrix):
    return tuple(
        sum(row[index] * matrix[index][column] for index in range(len(row)))
        for column in range(len(matrix[0]))
    )


def transpose(matrix):
    return tuple(tuple(matrix[row][column] for row in range(len(matrix))) for column in range(len(matrix[0])))


def mat_mul(left, right):
    right_t = transpose(right)
    return tuple(tuple(sum(a * b for a, b in zip(row, column)) for column in right_t) for row in left)


# ---------- Explicit maximal order and ramified prime ----------
# D=(-3,-17), i^2=-3, j^2=-17, ij=k. Since (-3/17)=-1 and
# (-17/3)=1, the finite ramified prime is 17; both parameters are negative,
# so infinity is ramified.
assert pow((-3) % 17, 8, 17) == 16
assert pow((-17) % 3, 1, 3) == 1


def qmul(left, right):
    a, b, c, d = left
    e, f, g, h = right
    return (
        a * e - 3 * b * f - 17 * c * g - 51 * d * h,
        a * f + b * e + 17 * c * h - 17 * d * g,
        a * g + c * e - 3 * b * h + 3 * d * f,
        a * h + d * e + b * g - c * f,
    )


def conjugate(value):
    return (value[0], -value[1], -value[2], -value[3])


def trace_pair(left, right):
    return 2 * qmul(left, conjugate(right))[0]


ORDER_BASIS = (
    (Fraction(1), 0, 0, 0),
    (Fraction(1, 2), Fraction(1, 2), 0, 0),
    (0, 0, Fraction(1, 2), Fraction(1, 2)),
    (0, Fraction(1, 3), 0, Fraction(1, 3)),
)
BASIS_MATRIX = transpose(ORDER_BASIS)
BASIS_INVERSE = inverse(BASIS_MATRIX)
assert determinant(BASIS_MATRIX) == Fraction(1, 12)


def order_coordinates(value):
    coordinates = mat_vec(BASIS_INVERSE, value)
    assert all(entry.denominator == 1 for entry in coordinates)
    return tuple(int(entry) for entry in coordinates)


# Closure proves this is an order. Trace discriminant 17^2 proves maximality
# in the algebra of discriminant 17.
for left in ORDER_BASIS:
    for right in ORDER_BASIS:
        order_coordinates(qmul(left, right))
TRACE_GRAM = tuple(tuple(trace_pair(left, right) for right in ORDER_BASIS) for left in ORDER_BASIS)
assert determinant(TRACE_GRAM) == 17 ** 2

J = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
RIGHT_J = transpose(tuple(order_coordinates(qmul(basis, J)) for basis in ORDER_BASIS))
LEFT_J = transpose(tuple(order_coordinates(qmul(J, basis)) for basis in ORDER_BASIS))
assert abs(determinant(RIGHT_J)) == 17 ** 2
# O*j=j*O: the change of ideal bases is unimodular integral.
IDEAL_CHANGE = mat_mul(inverse(RIGHT_J), LEFT_J)
assert all(entry.denominator == 1 for row in IDEAL_CHANGE for entry in row)
assert abs(determinant(IDEAL_CHANGE)) == 1

PRIME_GRAM = mat_mul(transpose(RIGHT_J), mat_mul(TRACE_GRAM, RIGHT_J))
assert determinant(PRIME_GRAM) == 17 ** 6
PRIME_GRAM_INVERSE = inverse(PRIME_GRAM)
# If trace energy <=34, dual Cauchy bounds every coefficient by 1.
assert max(Fraction(34) * PRIME_GRAM_INVERSE[i][i] for i in range(4)) < 2
prime_shell = []
for coefficients in product((-1, 0, 1), repeat=4):
    if coefficients == (0, 0, 0, 0):
        continue
    energy = row_mat(coefficients, PRIME_GRAM)
    energy = sum(energy[index] * coefficients[index] for index in range(4))
    if energy <= 34:
        prime_shell.append((coefficients, int(energy)))
assert prime_shell
assert min(energy for _coefficients, energy in prime_shell) == 34
assert all(energy == 34 for _coefficients, energy in prime_shell)
PRIME_TRACE_MINIMUM = 34


# ---------- Exhaustive N=8 signature search ----------
SIGNATURES = tuple(product((0, 1), repeat=4))
FALSE_BOUNDARIES = ((0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 1))
AFFINE_COEFFICIENTS = (
    (2, -1, -1, 1),
    (1, 0, -1, 1),
    (1, -1, 0, 1),
    (-1, 1, 1, 0),
)
SIGNATURE_COSTS = tuple(tuple(
    (2 * sum(signature[index] * coefficients[index] for index in range(4)) - 1) ** 2
    for coefficients in AFFINE_COEFFICIENTS
) for signature in SIGNATURES)

minor_masks = []
unit_minor_masks = []
for indices in combinations(range(16), 4):
    value = abs(determinant(tuple(SIGNATURES[index] for index in indices)))
    if value:
        mask = sum(1 << index for index in indices)
        minor_masks.append((mask, int(value)))
        if value == 1:
            unit_minor_masks.append(mask)
assert len(unit_minor_masks) == 835

# Completeness certificate for the saturation test: for every support subset,
# gcd of maximal minors is one iff it contains a unit minor.
minor_gcd = [0] * (1 << 16)
contains_unit = [False] * (1 << 16)
full_mask = (1 << 16) - 1
for mask, value in minor_masks:
    complement = full_mask ^ mask
    subset = complement
    while True:
        support = mask | subset
        minor_gcd[support] = gcd(minor_gcd[support], value)
        if value == 1:
            contains_unit[support] = True
        if subset == 0:
            break
        subset = (subset - 1) & complement
assert all((minor_gcd[mask] == 1) == contains_unit[mask] for mask in range(1 << 16))

searched = 0
saturated = 0
survivors = 0
best = None
for multiset in combinations_with_replacement(range(16), 8):
    searched += 1
    support = 0
    energies = [0, 0, 0, 0]
    for signature_index in multiset:
        support |= 1 << signature_index
        for boundary in range(4):
            energies[boundary] += SIGNATURE_COSTS[signature_index][boundary]
    if not contains_unit[support]:
        continue
    saturated += 1
    minimum = min(energies)
    if minimum >= PRIME_TRACE_MINIMUM and Fraction(minimum, 8) > Fraction(17, 16):
        survivors += 1
        key = (-minimum, multiset)
        if best is None or key < best[0]:
            best = (key, multiset, tuple(energies))

assert searched == 490314
assert saturated == 403973
assert survivors == 13457
assert best is not None
_best_key, BEST_MULTISET, BEST_FALSE_ENERGIES = best
assert BEST_MULTISET == (1, 2, 6, 6, 6, 6, 6, 9)
assert BEST_FALSE_ENERGIES == (160, 64, 56, 56)

# ---------- Complete emitted affine module for the best survivor ----------
CODE_ROWS = tuple(SIGNATURES[index] for index in BEST_MULTISET)  # N x 4
active_positions = (0, 1, 2, 7)
ACTIVE_MATRIX = tuple(CODE_ROWS[position] for position in active_positions)
assert abs(determinant(ACTIVE_MATRIX)) == 1
ACTIVE_INVERSE = inverse(ACTIVE_MATRIX)
assert all(entry.denominator == 1 for row in ACTIVE_INVERSE for entry in row)

# Variables are the eight charged code coordinates z. Four rows define every
# duplicate coordinate from the four active coordinates; four rows emit
# normalization and the three boundary bits.
emitted_rows = []
emitted_rhs_template = []
for position in range(8):
    if position in active_positions:
        continue
    active_coefficients = row_mat(CODE_ROWS[position], ACTIVE_INVERSE)
    row = [Fraction(0)] * 8
    row[position] = 1
    for active_position, coefficient in zip(active_positions, active_coefficients):
        row[active_position] -= coefficient
    emitted_rows.append(tuple(row))
    emitted_rhs_template.append(0)

LEGAL_WORDS = ((0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0))
augmented_rows = ((1, 1, 1, 1),) + tuple(
    tuple(word[coordinate] for word in LEGAL_WORDS) for coordinate in range(3)
)
for affine_row in augmented_rows:
    active_coefficients = row_mat(affine_row, ACTIVE_INVERSE)
    row = [Fraction(0)] * 8
    for active_position, coefficient in zip(active_positions, active_coefficients):
        row[active_position] += coefficient
    emitted_rows.append(tuple(row))
    emitted_rhs_template.append(None)
assert len(emitted_rows) == 8
assert abs(determinant(emitted_rows)) == 1


def selector_for_coefficients(coefficients):
    return tuple(sum(signature[index] * coefficients[index] for index in range(4)) for signature in CODE_ROWS)


def energy(selector):
    return sum((2 * value - 1) ** 2 for value in selector)


def residual(selector, boundary):
    rhs = (0, 0, 0, 0, 1) + tuple(boundary)
    return tuple(sum(emitted_rows[row][column] * selector[column] for column in range(8)) - rhs[row] for row in range(8))

legal_records = []
for index, word in enumerate(LEGAL_WORDS):
    coefficients = tuple(int(position == index) for position in range(4))
    selector = selector_for_coefficients(coefficients)
    assert set(selector) <= {0, 1}
    assert residual(selector, word) == (0,) * 8
    assert energy(selector) == 8
    legal_records.append(selector)

false_records = []
for boundary, coefficients, expected_energy in zip(FALSE_BOUNDARIES, AFFINE_COEFFICIENTS, BEST_FALSE_ENERGIES):
    selector = selector_for_coefficients(coefficients)
    assert residual(selector, boundary) == (0,) * 8
    assert energy(selector) == expected_energy
    false_records.append(selector)

MINIMUM_FALSE = min(BEST_FALSE_ENERGIES)
assert MINIMUM_FALSE == 56
assert MINIMUM_FALSE >= PRIME_TRACE_MINIMUM
assert Fraction(MINIMUM_FALSE, 8) > Fraction(17, 16)


def main():
    print(json.dumps({
        "quaternion_algebra": "(-3,-17) ramified at 17 and infinity",
        "maximal_order_basis": [[str(value) for value in basis] for basis in ORDER_BASIS],
        "maximal_order_trace_gram": [[str(value) for value in row] for row in TRACE_GRAM],
        "maximal_order_trace_discriminant": str(determinant(TRACE_GRAM)),
        "prime_right_multiplication_matrix": [[str(value) for value in row] for row in RIGHT_J],
        "prime_ideal_index": str(abs(determinant(RIGHT_J))),
        "prime_trace_minimum": PRIME_TRACE_MINIMUM,
        "prime_minimum_shell_size": len(prime_shell),
        "signature_multisets_searched_N8": searched,
        "saturated_multisets_N8": saturated,
        "local_survivors_N8": survivors,
        "best_signature_indices": list(BEST_MULTISET),
        "best_signatures": [list(CODE_ROWS[index]) for index in range(8)],
        "best_false_energies_000_010_100_111": list(BEST_FALSE_ENERGIES),
        "legal_energy": 8,
        "minimum_false_energy": MINIMUM_FALSE,
        "minimum_false_to_legal_ratio": f"{MINIMUM_FALSE}/8",
        "emitted_matrix_determinant": str(determinant(emitted_rows)),
        "false_fiber_selectors": [list(selector) for selector in false_records],
        "finding": "a saturated N=8 redundant NAND code has exact false minima 160,64,56,56 above the certified threshold 34",
        "scope": "finite depth-one NAND survivor only; COPY, depth two, and all-depth filtration remain unproved",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
