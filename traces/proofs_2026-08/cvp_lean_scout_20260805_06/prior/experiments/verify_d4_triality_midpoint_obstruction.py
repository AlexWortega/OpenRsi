#!/usr/bin/env python3
"""Generation-3 exact midpoint obstruction for the repaired D4 triality tile.

Only the repaired Pro proposal 5 survived cross-review.  This verifier freezes
its requested finite family:

* three dimension-4 triality blocks, using the 24 scaled Voronoi vertices of
  D4 split into the vector, even-spinor, and odd-spinor 8-sets;
* Boolean values represented by antipodal pairs in the assigned triality set;
* every assignment of the three triality sets to the two inputs and output;
* every oriented antipodal truth labeling;
* symmetric off-block Gram orbits Q=I+tS, with three off-block signs,
  t=p/q, |p|<=16, 1<=q<=16, retaining exactly the positive-definite Q.

The family fails before a factor or transfer table is authorized.  The two
legal COPY representatives 000 and 111 are antipodes, so their midpoint 0 is
an allowed lattice point and lies strictly inside every positive-definite
sphere on which the legal pair has equal radius.  NAND has the same problem:
the midpoint of legal 011 and 101 is the malformed port (0,0,output-1), also
an allowed lattice point, and is strictly inside their common shell.

The proof is the exact midpoint identity

 ||(x+y)/2-c||_Q^2 = (||x-c||_Q^2+||y-c||_Q^2)/2
                     - ||x-y||_Q^2/4.

Thus no exact 24-cell facet or outside-shell certificate can classify every
non-codebook state beyond the legal radius in this frozen family.  This is a
finite family rejection, not a theorem about arbitrary D4/Voronoi tiles.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import permutations, product
import hashlib
import json


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def negate(vector):
    return tuple(-value for value in vector)


def same_parity_lattice(vector):
    """Membership in 2 D4*: all four coordinates have one parity."""
    parities = {value & 1 for value in vector}
    return len(parities) == 1


# Scaled D4 Voronoi vertices.  Their union is the 24-cell, and each set is an
# 8-vertex cross polytope permuted with the other two by triality.
VECTOR = []
for coordinate in range(4):
    for value in (-2, 2):
        vertex = [0] * 4
        vertex[coordinate] = value
        VECTOR.append(tuple(vertex))

EVEN_SPINOR = []
ODD_SPINOR = []
for vertex in product((-1, 1), repeat=4):
    negative_parity = sum(value < 0 for value in vertex) & 1
    (ODD_SPINOR if negative_parity else EVEN_SPINOR).append(vertex)

VECTOR = tuple(sorted(VECTOR))
EVEN_SPINOR = tuple(sorted(EVEN_SPINOR))
ODD_SPINOR = tuple(sorted(ODD_SPINOR))
TRIALITY_CLASSES = (VECTOR, EVEN_SPINOR, ODD_SPINOR)
CLASS_NAMES = ("vector", "even-spinor", "odd-spinor")

assert tuple(map(len, TRIALITY_CLASSES)) == (8, 8, 8)
assert len(set().union(*map(set, TRIALITY_CLASSES))) == 24
for triality_class in TRIALITY_CLASSES:
    assert set(map(negate, triality_class)) == set(triality_class)
    assert all(dot(vertex, vertex) == 4 for vertex in triality_class)
    assert all(same_parity_lattice(vertex) for vertex in triality_class)


# The declared finite rational parameter set.
T_VALUES = tuple(sorted({
    Fraction(numerator, denominator)
    for numerator in range(-16, 17)
    for denominator in range(1, 17)
}))
SIGN_ORBITS = tuple(product((-1, 1), repeat=3))  # (input-input, input-output, input-output)


def determinant(signs, t):
    sign_product = signs[0] * signs[1] * signs[2]
    return 1 - 3 * t * t + 2 * sign_product * t * t * t


def positive_definite(signs, t):
    # Sylvester criterion for K=[[1,s01*t,s02*t],...], and Q=K tensor I4.
    return 1 - t * t > 0 and determinant(signs, t) > 0


PD_GRAMS = tuple(
    (signs, t)
    for signs in SIGN_ORBITS
    for t in T_VALUES
    if positive_definite(signs, t)
)
assert PD_GRAMS


# Enumerate all class-to-port assignments and oriented antipodal truth labels.
# Group them by the three cross-block dot products; the signature compression
# is exact because both midpoint deficits depend only on these products.
SIGNATURES = Counter()
LABELING_HASH = hashlib.sha256()
labeling_count = 0
for class_assignment in permutations(range(3)):
    classes = tuple(TRIALITY_CLASSES[index] for index in class_assignment)
    for input_left_zero in classes[0]:
        for input_right_zero in classes[1]:
            for output_zero in classes[2]:
                labeling_count += 1
                signature = (
                    dot(input_left_zero, input_right_zero),
                    dot(input_left_zero, output_zero),
                    dot(input_right_zero, output_zero),
                )
                SIGNATURES[signature] += 1
                LABELING_HASH.update(json.dumps([
                    list(class_assignment),
                    list(input_left_zero),
                    list(input_right_zero),
                    list(output_zero),
                ], separators=(",", ":")).encode() + b"\n")

assert labeling_count == 6 * 8 ** 3 == 3072
assert sum(SIGNATURES.values()) == labeling_count


def copy_midpoint_deficit(signature, signs, t):
    """R^2-cost(0), where legal 000 and 111 are antipodal."""
    ab, ac, bc = signature
    # p000 has three norm-4 blocks.  Since p111=-p000, the legal chord's
    # quarter squared length is ||p000||_Q^2.
    return 12 + 2 * t * (signs[0] * ab + signs[1] * ac + signs[2] * bc)


def nand_midpoint_deficit(signature, signs, t):
    """R^2-cost(midpoint(011,101))."""
    ab = signature[0]
    # The legal chord is (2*a0,-2*b0,0), so one quarter of its Q-norm is
    # 8-2*t*s01*<a0,b0>.
    return 8 - 2 * t * signs[0] * ab


minimum_copy = None
minimum_nand = None
minimum_copy_witness = None
minimum_nand_witness = None
candidate_count = 0
for signature, multiplicity in sorted(SIGNATURES.items()):
    for signs, t in PD_GRAMS:
        copy_deficit = copy_midpoint_deficit(signature, signs, t)
        nand_deficit = nand_midpoint_deficit(signature, signs, t)
        # Exact strictness: Q is positive definite and each legal chord is
        # nonzero.  These assertions audit every compressed candidate.
        assert copy_deficit > 0
        assert nand_deficit > 0
        candidate_count += multiplicity
        if minimum_copy is None or copy_deficit < minimum_copy:
            minimum_copy = copy_deficit
            minimum_copy_witness = (signature, signs, t)
        if minimum_nand is None or nand_deficit < minimum_nand:
            minimum_nand = nand_deficit
            minimum_nand_witness = (signature, signs, t)

assert candidate_count == labeling_count * len(PD_GRAMS)


# Explicit malformed midpoint membership, independent of the signature.
ZERO_BLOCK = (0, 0, 0, 0)
assert same_parity_lattice(ZERO_BLOCK)
for output_class in TRIALITY_CLASSES:
    for output_zero in output_class:
        output_one = negate(output_zero)
        copy_midpoint = (ZERO_BLOCK, ZERO_BLOCK, ZERO_BLOCK)
        nand_midpoint = (ZERO_BLOCK, ZERO_BLOCK, output_one)
        assert all(same_parity_lattice(block) for block in copy_midpoint)
        assert all(same_parity_lattice(block) for block in nand_midpoint)
        assert ZERO_BLOCK not in output_class


def fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def witness_record(witness):
    signature, signs, t = witness
    return {
        "cross_dot_signature": list(signature),
        "off_block_signs": list(signs),
        "t": fraction_text(t),
    }


def main():
    print(json.dumps({
        "family": "three scaled D4 triality blocks with antipodal truth labels",
        "coefficient_lattice_per_block": "2D4* = integer vectors of common coordinate parity",
        "triality_class_sizes": {
            name: len(triality_class)
            for name, triality_class in zip(CLASS_NAMES, TRIALITY_CLASSES)
        },
        "rational_t_count": len(T_VALUES),
        "symmetric_sign_orbit_count": len(SIGN_ORBITS),
        "positive_definite_gram_count": len(PD_GRAMS),
        "truth_labeling_count": labeling_count,
        "compressed_cross_dot_signature_count": len(SIGNATURES),
        "exact_candidate_count": candidate_count,
        "truth_labeling_sha256": LABELING_HASH.hexdigest(),
        "copy_midpoint": "(0,0,0)",
        "nand_midpoint": "(0,0,output-1)",
        "copy_minimum_exact_inward_deficit": fraction_text(minimum_copy),
        "copy_minimum_witness": witness_record(minimum_copy_witness),
        "nand_minimum_exact_inward_deficit": fraction_text(minimum_nand),
        "nand_minimum_witness": witness_record(minimum_nand_witness),
        "outside_shell_certificate": "impossible: an allowed malformed lattice midpoint is strictly inside every equal-legal-radius shell",
        "transfer_table_status": "not authorized after exact Delaunay/Voronoi completeness failure",
        "finding": "every retained positive-definite D4 triality candidate has an interior malformed midpoint for both COPY and NAND",
        "scope": "finite rejection of the declared repaired-Pro-5 family; no theorem about arbitrary Voronoi tiles",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
