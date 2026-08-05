#!/usr/bin/env python3
"""Finite exact low-weight audit of the smallest genuine product-tag seam.

This freezes the current four-state N=8 NAND survivor and the lexicographically
first saturated rank-2 COPY code.  On their 4x2 all-pairs selector table it uses
F_289 labels

    a = (0, 1, u, 1+u),  b = (0, 1),  u^2 = 3.

Every one of the six ordinary 2x2 transportation moves has a nonzero product
tag, and the false-111 affine coefficient vector (-1,1,1,0) also has nonzero
tag in either COPY orientation.  The experiment then rebuilds the kernel after
the tag is emitted and exhausts every {-1,0,1}^8 signed move.  It finds exactly
one move up to sign, of coefficient L1 and squared weight 8, whose row margins,
column margins, and both integer tag coordinates are all zero.  Because the
cancellation is over Z[u]/(u^2-3), it remains zero modulo 17 and 17^2.

This kills only this smallest label specialization.  The coefficient weight is
not asserted to be CVP energy, and no claim is made about other O/P^2 labels,
the complete N=8 pair-selector enlargement, Q1, Q2, or any asymptotic gap.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import hashlib
import json

P = 17
P2 = P * P
NONSQUARE = 3

# Hash-locked current survivor and deterministic smallest saturated COPY seam.
NAND_LEGAL = ((0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0))
NAND_SIGNATURE_INDICES = (1, 2, 6, 6, 6, 6, 6, 9)
NAND_CODE = tuple(
    tuple(int(bit) for bit in f"{index:04b}")
    for index in NAND_SIGNATURE_INDICES
)
COPY_CODE = ((0, 1), (1, 0))


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


assert determinant(COPY_CODE) == -1  # saturated over Z
frozen_payload = {
    "nand_legal": NAND_LEGAL,
    "nand_signature_indices": NAND_SIGNATURE_INDICES,
    "copy_code": COPY_CODE,
}
frozen_sha256 = hashlib.sha256(
    json.dumps(frozen_payload, sort_keys=True, separators=(",", ":")).encode("ascii")
).hexdigest()
EXPECTED_FROZEN_SHA256 = "3bf332d40b3628f960b392305d349de6bfac78941ad0d3de5cb921070fcc99de"
assert frozen_sha256 == EXPECTED_FROZEN_SHA256

# Pair arithmetic in Z[u]/(u^2-3).  Reduction modulo 17 gives F_289 because 3
# is a nonsquare modulo 17; exact zero here is stronger than zero modulo P^2.
def qadd(left, right):
    return (left[0] + right[0], left[1] + right[1])


def qscale(scale, value):
    return (scale * value[0], scale * value[1])


def qmul(left, right):
    return (
        left[0] * right[0] + NONSQUARE * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def qmod(value, modulus):
    return (value[0] % modulus, value[1] % modulus)


assert pow(NONSQUARE, (P - 1) // 2, P) == P - 1
A_LABELS = ((0, 0), (1, 0), (0, 1), (1, 1))
B_LABELS = ((0, 0), (1, 0))
TAG_TABLE = tuple(
    tuple(qmul(a_label, b_label) for b_label in B_LABELS)
    for a_label in A_LABELS
)


def at(vector, row, column):
    return vector[2 * row + column]


def margins(vector):
    rows = tuple(sum(at(vector, row, column) for column in range(2)) for row in range(4))
    columns = tuple(sum(at(vector, row, column) for row in range(4)) for column in range(2))
    return rows, columns


def transfer(vector):
    answer = (0, 0)
    for row in range(4):
        for column in range(2):
            answer = qadd(answer, qscale(at(vector, row, column), TAG_TABLE[row][column]))
    return answer


def transportation_move(first, second, orientation=1):
    vector = [0] * 8
    vector[2 * first] += orientation
    vector[2 * first + 1] -= orientation
    vector[2 * second] -= orientation
    vector[2 * second + 1] += orientation
    return tuple(vector)


# The six old 4x2 transportation quadratics all acquire nonzero initial tags.
old_records = []
for first, second in combinations(range(4), 2):
    move = transportation_move(first, second)
    assert margins(move) == ((0, 0, 0, 0), (0, 0))
    exact_tag = transfer(move)
    assert qmod(exact_tag, P) != (0, 0)
    old_records.append({
        "rows": [first, second],
        "move": list(move),
        "tag_Zu": list(exact_tag),
        "tag_mod_17": list(qmod(exact_tag, P)),
    })

# In legal-state coefficients, false 111 = -001 + 011 + 101.
FALSE_111_COEFFICIENTS = (-1, 1, 1, 0)
false_tag = (0, 0)
for coefficient, a_label in zip(FALSE_111_COEFFICIENTS, A_LABELS):
    false_tag = qadd(false_tag, qscale(coefficient, a_label))
assert false_tag == (1, 1)
assert qmod(false_tag, P) != (0, 0)
assert qmod(qscale(-1, false_tag), P) != (0, 0)  # reversed COPY orientation

# Exact bounded low-weight search in the enlarged emitted kernel.  Row/column
# margins and both product-tag coordinates are checked over Z, not numerically.
kernel_moves = []
searched = 0
for vector in product((-1, 0, 1), repeat=8):
    searched += 1
    if not any(vector):
        continue
    if margins(vector) != ((0, 0, 0, 0), (0, 0)):
        continue
    if transfer(vector) != (0, 0):
        continue
    kernel_moves.append(vector)

assert searched == 3**8
assert len(kernel_moves) == 2
assert kernel_moves[1] == tuple(-value for value in kernel_moves[0])
WITNESS = min(kernel_moves)
assert sum(abs(value) for value in WITNESS) == 8
assert sum(value * value for value in WITNESS) == 8
assert qmod(transfer(WITNESS), P) == (0, 0)
assert qmod(transfer(WITNESS), P2) == (0, 0)

# Finite conformal-primitivity check: because every witness entry is +/-1,
# every conformal submove is obtained by retaining or deleting support entries.
conformal_kernel_submoves = []
for mask in range(1 << 8):
    submove = tuple(
        WITNESS[index] if (mask >> index) & 1 else 0
        for index in range(8)
    )
    if margins(submove) == ((0, 0, 0, 0), (0, 0)) and transfer(submove) == (0, 0):
        conformal_kernel_submoves.append(submove)
assert conformal_kernel_submoves == [(0,) * 8, WITNESS]


def main():
    print(json.dumps({
        "selected_surviving_proposal": (
            "generic quaternion-product specialization with enlarged-kernel audit"
        ),
        "causal_mechanism": (
            "genuine pair products can separate old marginal-preserving quadratics, "
            "but soundness also requires that their signed sums do not create a new "
            "zero-transfer kernel move"
        ),
        "expected_frontier_move": (
            "retain the smallest product alphabet only if old quadratics and the "
            "false-111 defect are nonzero and the enlarged low-weight kernel is empty"
        ),
        "falsification_condition": (
            "an exact low-weight signed all-pairs move preserves both margins and "
            "has zero product transfer after the old moves individually pass"
        ),
        "frozen_input_sha256": frozen_sha256,
        "nand_signature_indices": list(NAND_SIGNATURE_INDICES),
        "copy_code": [list(row) for row in COPY_CODE],
        "copy_determinant": int(determinant(COPY_CODE)),
        "ring": "Z[u]/(u^2-3), reduced modulo 17 or 289",
        "a_labels": [list(value) for value in A_LABELS],
        "b_labels": [list(value) for value in B_LABELS],
        "old_quadratic_count": len(old_records),
        "old_quadratics": old_records,
        "false_111_coefficients": list(FALSE_111_COEFFICIENTS),
        "false_111_tag_mod_17": list(qmod(false_tag, P)),
        "false_111_reversed_tag_mod_17": list(qmod(qscale(-1, false_tag), P)),
        "bounded_vectors_searched": searched,
        "enlarged_kernel_moves_in_box": len(kernel_moves),
        "minimum_nonzero_l1_weight_in_box": 8,
        "minimum_nonzero_squared_coefficient_weight_in_box": 8,
        "zero_transfer_witness": list(WITNESS),
        "witness_row_column_margins": [list(values) for values in margins(WITNESS)],
        "witness_tag_over_Zu": list(transfer(WITNESS)),
        "witness_tag_mod_17": list(qmod(transfer(WITNESS), P)),
        "witness_tag_mod_289": list(qmod(transfer(WITNESS), P2)),
        "conformal_kernel_submoves": len(conformal_kernel_submoves),
        "finding": (
            "the smallest natural product labels detect all six old 4x2 quadratics "
            "and false 111, but their enlarged pair-selector matrix has a primitive "
            "exact zero-transfer signed move of coefficient weight 8"
        ),
        "scope": (
            "finite kill of this frozen 4x2 label specialization only; coefficient "
            "weight is not CVP energy, and other O/P^2 assignments, full Q1/Q2, "
            "and all-depth behavior remain open"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
