#!/usr/bin/env python3
"""Generation-11 exact grade-zero attack on the canonical F_289 NAND module.

Only Pro proposal 1 survives cross-review.  Following the repaired gate in the
opponent review, this verifier freezes a canonical eight-selector NAND module
over F_289=F_17[u]/(u^2-3): one selector for each Boolean triple, normalization,
three complete port rows, four forbidden-label rows, and the linearized NAND
product-table row.  All boundary values are emitted right-hand sides.

The four legal NAND columns form a unimodular affine simplex.  Consequently
every false Boolean boundary has a unique integral affine pseudosection using
only legal selectors.  The cheapest examples (010, 100, and 111) have one -1,
zero residual, anchor energy 16, and no positive-grade defect.  They are fixed
by Frobenius and therefore survive the grade-one skew copy as grade-zero
classes.  Since every nonzero element of the quaternion prime P above 17 has
trace energy at least 2*17=34, these witnesses violate the proposed adverse
filtration dichotomy already at depth one.

This kills only this canonical selector/template family.  No general statement
about other quaternion modules or the all-depth frontier is claimed.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import json

P = 17
NONSQUARE = 3

# 3 is a nonsquare modulo 17, so x^2-3 is irreducible.
assert pow(NONSQUARE, (P - 1) // 2, P) == P - 1


@dataclass(frozen=True, order=True)
class F289:
    a: int
    b: int = 0

    def __post_init__(self):
        object.__setattr__(self, "a", self.a % P)
        object.__setattr__(self, "b", self.b % P)

    def __add__(self, other):
        other = field(other)
        return F289(self.a + other.a, self.b + other.b)

    def __neg__(self):
        return F289(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-field(other))

    def __mul__(self, other):
        other = field(other)
        return F289(
            self.a * other.a + NONSQUARE * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    def inverse(self):
        assert self != ZERO
        norm = (self.a * self.a - NONSQUARE * self.b * self.b) % P
        inverse_norm = pow(norm, -1, P)
        return F289(self.a * inverse_norm, -self.b * inverse_norm)

    def __truediv__(self, other):
        return self * field(other).inverse()

    def __pow__(self, exponent):
        result = ONE
        base = self
        while exponent:
            if exponent & 1:
                result = result * base
            base = base * base
            exponent >>= 1
        return result

    def text(self):
        return str(self.a) if self.b == 0 else f"{self.a}+{self.b}u"


def field(value):
    return value if isinstance(value, F289) else F289(value)


ZERO = F289(0)
ONE = F289(1)
U = F289(0, 1)
assert U * U == F289(NONSQUARE)
assert U ** P == -U
assert all(element ** (P * P) == element for element in (
    ZERO, ONE, U, F289(5, 7), F289(16, 16),
))

WORDS = tuple(product((0, 1), repeat=3))
LEGAL = tuple(word for word in WORDS if word[2] == 1 - (word[0] & word[1]))
FALSE = tuple(word for word in WORDS if word not in LEGAL)
assert LEGAL == ((0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0))
assert FALSE == ((0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 1))
WORD_INDEX = {word: index for index, word in enumerate(WORDS)}

# Complete emitted depth-one row matrix.
rows = []
row_kinds = []
rows.append([1] * 8)
row_kinds.append("normalization")
for coordinate in range(3):
    rows.append([word[coordinate] for word in WORDS])
    row_kinds.append(f"port_{coordinate}")
for word in FALSE:
    row = [0] * 8
    row[WORD_INDEX[word]] = 1
    rows.append(row)
    row_kinds.append(f"forbidden_{''.join(map(str, word))}")
rows.append([word[0] * word[1] + word[2] - 1 for word in WORDS])
row_kinds.append("nand_product_table")
assert len(rows) == 9


def matrix_rank(matrix):
    work = [[field(value) for value in row] for row in matrix]
    rank = 0
    if not work:
        return 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(rank, len(work)) if work[row][column] != ZERO), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [value / scale for value in work[rank]]
        for row in range(len(work)):
            if row == rank or work[row][column] == ZERO:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(work[row], work[rank])
            ]
        rank += 1
    return rank


def solve_unique(matrix, rhs):
    augmented = [
        [field(value) for value in row] + [field(rhs[index])]
        for index, row in enumerate(matrix)
    ]
    columns = len(matrix[0])
    rank = 0
    pivots = []
    for column in range(columns):
        pivot = next((row for row in range(rank, len(augmented)) if augmented[row][column] != ZERO), None)
        if pivot is None:
            continue
        augmented[rank], augmented[pivot] = augmented[pivot], augmented[rank]
        scale = augmented[rank][column]
        augmented[rank] = [value / scale for value in augmented[rank]]
        for row in range(len(augmented)):
            if row == rank or augmented[row][column] == ZERO:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(augmented[row], augmented[rank])
            ]
        pivots.append(column)
        rank += 1
    assert all(any(row[column] != ZERO for column in range(columns)) or row[-1] == ZERO for row in augmented)
    assert rank == columns
    solution = [ZERO] * columns
    for row, column in enumerate(pivots):
        solution[column] = augmented[row][-1]
    return tuple(solution)


def rhs_for_boundary(boundary):
    return (1,) + tuple(boundary) + (0,) * 4 + (0,)


def integer_residual(selector, rhs):
    return tuple(
        sum(row[column] * selector[column] for column in range(8)) - rhs[index]
        for index, row in enumerate(rows)
    )


def anchor_energy(selector):
    return sum((2 * value - 1) ** 2 for value in selector)


# The normalization/port submatrix on legal columns has determinant one;
# together with the four forbidden unit rows this gives a saturated full-rank
# integer matrix.  List the exact unique integral affine representatives.
expected_legal_coefficients = {
    (0, 0, 0): (2, -1, -1, 1),
    (0, 1, 0): (1, 0, -1, 1),
    (1, 0, 0): (1, -1, 0, 1),
    (1, 1, 1): (-1, 1, 1, 0),
}

assert matrix_rank(rows) == 8
records = []
for boundary in FALSE:
    rhs = rhs_for_boundary(boundary)
    field_solution = solve_unique(rows, rhs)
    legal_coefficients = expected_legal_coefficients[boundary]
    selector = [0] * 8
    for word, coefficient in zip(LEGAL, legal_coefficients):
        selector[WORD_INDEX[word]] = coefficient
    selector = tuple(selector)
    assert integer_residual(selector, rhs) == (0,) * len(rows)
    assert field_solution == tuple(F289(value) for value in selector)
    # Base-field coefficients are fixed by the F_289/F_17 Frobenius, so the
    # same class remains in grade zero after a skew grade-one copy.
    assert tuple(value ** P for value in field_solution) == field_solution
    records.append({
        "boundary": boundary,
        "selector": selector,
        "anchor_energy": anchor_energy(selector),
        "negative_coefficients": sum(value < 0 for value in selector),
    })

minimum_record = min(records, key=lambda record: (record["anchor_energy"], record["boundary"]))
assert minimum_record["anchor_energy"] == 16
TRACE_THRESHOLD_P = 2 * P
assert TRACE_THRESHOLD_P == 34
assert minimum_record["anchor_energy"] < TRACE_THRESHOLD_P


def main():
    print(json.dumps({
        "field": "F_289=F_17[u]/(u^2-3)",
        "selector_count": 8,
        "emitted_row_count": len(rows),
        "row_kinds": row_kinds,
        "grade_zero_rank": matrix_rank(rows),
        "false_boundary_count": len(FALSE),
        "false_boundary_records": [{
            "boundary": list(record["boundary"]),
            "selector": list(record["selector"]),
            "anchor_energy": record["anchor_energy"],
            "negative_coefficients": record["negative_coefficients"],
            "residual_squared": 0,
            "frobenius_fixed": True,
        } for record in records],
        "minimum_false_anchor_energy": minimum_record["anchor_energy"],
        "minimum_nonzero_P_trace_energy": TRACE_THRESHOLD_P,
        "grade_one_result": "the base-field affine classes are Frobenius-fixed and remain in grade zero",
        "adverse_graded_injectivity": "failed at depth one",
        "maximal_order_lift_status": "not authorized after residue-field grade-zero failure",
        "copy_and_depth_two_status": "not authorized after NAND failure",
        "finding": "every false NAND boundary has an exact integral legal-selector pseudosection; the cheapest costs 16<34",
        "scope": "finite kill of the canonical eight-selector residue template; other quaternion modules remain untested",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
