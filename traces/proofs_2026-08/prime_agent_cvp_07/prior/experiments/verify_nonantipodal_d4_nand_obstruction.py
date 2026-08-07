#!/usr/bin/env python3
"""Generation-4 exact gate for non-antipodal D4 triality NAND labels.

Both cross-reviews authorize only the non-antipodal continuation of the D4
triality family.  This verifier covers the prescribed finite family exactly:

* all six assignments of the vector/even-spinor/odd-spinor triality classes
  to input A, input B, and output C;
* every ordered distinct non-antipodal Boolean pair in each 8-set;
* all eight symmetric off-block sign orbits in Q=I+tS;
* every distinct t=p/q with |p|<=16 and 1<=q<=16 for which Q is positive
  definite (the same 952 Gram parameters as Generation 3).

The candidate dies before center or Fincke--Pohst enumeration.  Restrict the
squared Q-distance to the eight Boolean port representatives.  It is a
quadratic pseudo-Boolean function

  q(a,b,c)=k+la*a+lb*b+lc*c+A*ab+B*ac+C*bc.

If the four legal NAND words 001,011,101,110 have common squared radius R^2,
then the four false-word excesses over R^2 are, respectively,

  000: -A+B+C,  010: -A+B,  100: -A+C,  111: A.

Here A,B,C are computed exactly from the three truth-label differences and the
frozen Gram.  Exhaustive signature compression proves that for every retained
label/Gram candidate at least one excess is <=0.  That false Boolean lattice
point is on or inside the legal shell, so the required NAND Delaunay shell and
65/64 adverse separation are impossible.  Candidates without a common center
already fail completeness; candidates with one fail this identity.

This is a finite rejection of the declared non-antipodal D4 family, not a
no-go theorem for arbitrary Voronoi tiles.
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


VECTOR = []
for coordinate in range(4):
    for value in (-2, 2):
        vertex = [0] * 4
        vertex[coordinate] = value
        VECTOR.append(tuple(vertex))

EVEN_SPINOR = []
ODD_SPINOR = []
for vertex in product((-1, 1), repeat=4):
    target = ODD_SPINOR if sum(value < 0 for value in vertex) & 1 else EVEN_SPINOR
    target.append(vertex)

TRIALITY_CLASSES = tuple(tuple(sorted(values)) for values in (
    VECTOR, EVEN_SPINOR, ODD_SPINOR,
))
CLASS_NAMES = ("vector", "even-spinor", "odd-spinor")
assert tuple(map(len, TRIALITY_CLASSES)) == (8, 8, 8)
assert len(set().union(*map(set, TRIALITY_CLASSES))) == 24
assert all(dot(vertex, vertex) == 4 for values in TRIALITY_CLASSES for vertex in values)


def nonantipodal_pairs(values):
    return tuple(
        (zero, one)
        for zero in values
        for one in values
        if one != zero and one != negate(zero)
    )


PAIR_SETS = tuple(nonantipodal_pairs(values) for values in TRIALITY_CLASSES)
assert tuple(map(len, PAIR_SETS)) == (48, 48, 48)

T_VALUES = tuple(sorted({
    Fraction(numerator, denominator)
    for numerator in range(-16, 17)
    for denominator in range(1, 17)
}))
SIGN_ORBITS = tuple(product((-1, 1), repeat=3))


def gram_determinant(signs, t):
    return 1 - 3 * t * t + 2 * signs[0] * signs[1] * signs[2] * t * t * t


def positive_definite(signs, t):
    # Exact Sylvester criterion for the 3x3 block matrix K; Q=K tensor I4.
    return 1 - t * t > 0 and gram_determinant(signs, t) > 0


PD_GRAMS = tuple(
    (signs, t)
    for signs in SIGN_ORBITS
    for t in T_VALUES
    if positive_definite(signs, t)
)
assert len(PD_GRAMS) == 952


def difference(pair):
    zero, one = pair
    return tuple(one[index] - zero[index] for index in range(4))


# Machine-checked exact symmetry compression.  The NAND false-word excesses
# depend only on the three cross-dot products of the truth differences.
INTERACTION_SIGNATURES = Counter()
LABELING_HASH = hashlib.sha256()
labeling_count = 0
for class_assignment in permutations(range(3)):
    pair_sets = tuple(PAIR_SETS[index] for index in class_assignment)
    for left_pair in pair_sets[0]:
        left_difference = difference(left_pair)
        for right_pair in pair_sets[1]:
            right_difference = difference(right_pair)
            left_right = dot(left_difference, right_difference)
            for output_pair in pair_sets[2]:
                output_difference = difference(output_pair)
                signature = (
                    left_right,
                    dot(left_difference, output_difference),
                    dot(right_difference, output_difference),
                )
                INTERACTION_SIGNATURES[signature] += 1
                labeling_count += 1
                LABELING_HASH.update(json.dumps([
                    list(class_assignment),
                    [list(left_pair[0]), list(left_pair[1])],
                    [list(right_pair[0]), list(right_pair[1])],
                    [list(output_pair[0]), list(output_pair[1])],
                ], separators=(",", ":")).encode() + b"\n")

assert labeling_count == 6 * 48 ** 3 == 663552
assert sum(INTERACTION_SIGNATURES.values()) == labeling_count
assert len(INTERACTION_SIGNATURES) == 43

FALSE_WORDS = ("000", "010", "100", "111")
false_first_counts = Counter()
tied_candidate_count = 0
strictly_inside_candidate_count = 0
best_minimum_gap = None
best_record = None
compressed_tests = 0

for signature, multiplicity in sorted(INTERACTION_SIGNATURES.items()):
    delta_ab, delta_ac, delta_bc = signature
    for signs, t in PD_GRAMS:
        # Pair coefficients of the restricted quadratic distance function.
        interaction_ab = 2 * t * signs[0] * delta_ab
        interaction_ac = 2 * t * signs[1] * delta_ac
        interaction_bc = 2 * t * signs[2] * delta_bc
        gaps = (
            -interaction_ab + interaction_ac + interaction_bc,  # 000
            -interaction_ab + interaction_ac,                   # 010
            -interaction_ab + interaction_bc,                   # 100
            interaction_ab,                                     # 111
        )
        minimum_gap = min(gaps)
        # This is the complete discriminator: strict positivity of all four
        # false ports never occurs.
        assert minimum_gap <= 0
        compressed_tests += 1
        if minimum_gap == 0:
            tied_candidate_count += multiplicity
        else:
            strictly_inside_candidate_count += multiplicity
        first_failure = next(index for index, gap in enumerate(gaps) if gap <= 0)
        false_first_counts[FALSE_WORDS[first_failure]] += multiplicity
        if best_minimum_gap is None or minimum_gap > best_minimum_gap:
            best_minimum_gap = minimum_gap
            best_record = (signature, signs, t, gaps)

candidate_count = labeling_count * len(PD_GRAMS)
assert compressed_tests == len(INTERACTION_SIGNATURES) * len(PD_GRAMS)
assert tied_candidate_count + strictly_inside_candidate_count == candidate_count
assert candidate_count == 631701504
assert best_minimum_gap == 0
assert strictly_inside_candidate_count > 0


def fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def main():
    signature, signs, t, gaps = best_record
    print(json.dumps({
        "family": "non-antipodal scaled-D4 triality NAND codebooks",
        "triality_class_sizes": {
            name: len(values) for name, values in zip(CLASS_NAMES, TRIALITY_CLASSES)
        },
        "ordered_nonantipodal_pairs_per_class": 48,
        "truth_labeling_count": labeling_count,
        "truth_labeling_sha256": LABELING_HASH.hexdigest(),
        "interaction_signature_count": len(INTERACTION_SIGNATURES),
        "rational_t_count": len(T_VALUES),
        "symmetric_sign_orbit_count": len(SIGN_ORBITS),
        "positive_definite_gram_count": len(PD_GRAMS),
        "compressed_exact_tests": compressed_tests,
        "exact_candidate_count": candidate_count,
        "strictly_inside_false_port_candidates": strictly_inside_candidate_count,
        "tied_false_port_candidates": tied_candidate_count,
        "first_nonpositive_false_port_counts": dict(sorted(false_first_counts.items())),
        "best_possible_minimum_false_gap": fraction_text(best_minimum_gap),
        "best_record": {
            "interaction_signature": list(signature),
            "off_block_signs": list(signs),
            "t": fraction_text(t),
            "false_gaps_000_010_100_111": [fraction_text(gap) for gap in gaps],
        },
        "sphere_gate": "failed: every equal-radius NAND shell has a false Boolean port on or inside it",
        "fincke_pohst_status": "not needed after an explicit in-shell lattice point for every candidate",
        "copy_and_transfer_status": "not authorized because the NAND prerequisite fails for the complete family",
        "finding": "no retained non-antipodal D4 candidate has all four false NAND ports strictly outside the legal shell",
        "scope": "finite rejection of the prescribed non-antipodal D4/Gram grid; no arbitrary-Voronoi no-go theorem",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
