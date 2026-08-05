#!/usr/bin/env python3
"""Generation-5 exact attack on independent-coupling D4 triality tiles.

Both cross-reviews select only the frozen mutation

    Q = K(x,y,z) tensor I_4,
    K = [[1,x,y],[x,1,z],[y,z,1]],
    x,y,z in {-7/16,...,7/16},

with every ordered distinct non-antipodal truth pair in the three D4 triality
classes.  Independent couplings genuinely evade the Generation-4 Boolean
identity: this verifier finds all candidates with four strictly positive false
Boolean excesses.

They nevertheless all fail the global shell gate.  Legal NAND words 001 and
011 differ only in the B-port label b0 versus b1.  Every non-antipodal pair in
one triality class differs in at least two coordinate positions.  Swap one
changed coordinate to form two hybrid labels h,h'.  Both lie in 2D4*, neither
is a Boolean B label, and, because Q is K tensor I4, squared distance is a sum
over the four coordinate positions.  For every center c,

    E(a0,h,c1)+E(a0,h',c1) = E(a0,b0,c1)+E(a0,b1,c1).

If the two legal points have common radius R, at least one hybrid costs at most
R.  If it is cheaper, shell emptiness fails; if both are no cheaper, both tie
and the closed shell contains malformed points.  Thus exact CVP enumeration is
unnecessary after an explicit all-lattice certificate.

This rejects the declared independent-coupling grid only; it is not a theorem
about nonseparable coordinate Grams or arbitrary Voronoi tiles.
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
    return len({value & 1 for value in vector}) == 1


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
assert all(same_parity_lattice(v) for cls in TRIALITY_CLASSES for v in cls)


def nonantipodal_pairs(values):
    return tuple(
        (zero, one)
        for zero in values
        for one in values
        if one != zero and one != negate(zero)
    )


PAIR_SETS = tuple(nonantipodal_pairs(values) for values in TRIALITY_CLASSES)
assert tuple(map(len, PAIR_SETS)) == (48, 48, 48)


def difference(pair):
    return tuple(pair[1][index] - pair[0][index] for index in range(4))


# Exact signature compression for the Boolean gate.
INTERACTION_SIGNATURES = Counter()
LABELING_HASH = hashlib.sha256()
labeling_count = 0
for class_assignment in permutations(range(3)):
    pair_sets = tuple(PAIR_SETS[index] for index in class_assignment)
    for left_pair in pair_sets[0]:
        delta_left = difference(left_pair)
        for right_pair in pair_sets[1]:
            delta_right = difference(right_pair)
            delta_lr = dot(delta_left, delta_right)
            for output_pair in pair_sets[2]:
                delta_output = difference(output_pair)
                signature = (
                    delta_lr,
                    dot(delta_left, delta_output),
                    dot(delta_right, delta_output),
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
assert len(INTERACTION_SIGNATURES) == 43
assert sum(INTERACTION_SIGNATURES.values()) == labeling_count

COUPLINGS = tuple(Fraction(value, 16) for value in range(-7, 8))


def determinant(x, y, z):
    return 1 + 2 * x * y * z - x * x - y * y - z * z


def positive_definite(x, y, z):
    return 1 - x * x > 0 and determinant(x, y, z) > 0


PD_GRAMS = tuple(
    (x, y, z)
    for x in COUPLINGS
    for y in COUPLINGS
    for z in COUPLINGS
    if positive_definite(x, y, z)
)
# The frozen box is safely inside the 3x3 correlation cone.
assert len(PD_GRAMS) == 15 ** 3 == 3375

FALSE_WORDS = ("000", "010", "100", "111")
strict_boolean_survivors = 0
surviving_signature_gram_pairs = 0
first_failure_counts = Counter()
best_margin = None
best_record = None
compressed_tests = 0

for signature, multiplicity in sorted(INTERACTION_SIGNATURES.items()):
    delta_ab, delta_ac, delta_bc = signature
    for x, y, z in PD_GRAMS:
        interaction_ab = 2 * x * delta_ab
        interaction_ac = 2 * y * delta_ac
        interaction_bc = 2 * z * delta_bc
        gaps = (
            -interaction_ab + interaction_ac + interaction_bc,
            -interaction_ab + interaction_ac,
            -interaction_ab + interaction_bc,
            interaction_ab,
        )
        compressed_tests += 1
        margin = min(gaps)
        if margin > 0:
            strict_boolean_survivors += multiplicity
            surviving_signature_gram_pairs += 1
            if best_margin is None or margin > best_margin:
                best_margin = margin
                best_record = (signature, (x, y, z), gaps)
        else:
            first = next(index for index, gap in enumerate(gaps) if gap <= 0)
            first_failure_counts[FALSE_WORDS[first]] += multiplicity

candidate_count = labeling_count * len(PD_GRAMS)
assert compressed_tests == len(INTERACTION_SIGNATURES) * len(PD_GRAMS) == 145125
assert candidate_count == 2239488000
assert strict_boolean_survivors == 24344064
assert surviving_signature_gram_pairs > 0
assert best_margin == 3


# Exact recombination certificate for every possible non-antipodal B pair.
# A representative A/C value is irrelevant because those blocks do not change.
recombination_certificates = []
for class_index, pair_set in enumerate(PAIR_SETS):
    for zero, one in pair_set:
        changed = [index for index in range(4) if zero[index] != one[index]]
        assert len(changed) >= 2
        coordinate = changed[0]
        hybrid = list(zero)
        complement = list(one)
        hybrid[coordinate] = one[coordinate]
        complement[coordinate] = zero[coordinate]
        hybrid = tuple(hybrid)
        complement = tuple(complement)
        assert same_parity_lattice(hybrid)
        assert same_parity_lattice(complement)
        assert hybrid not in (zero, one)
        assert complement not in (zero, one)
        # At every coordinate the unordered B-value pair is unchanged.  Since
        # A and C are fixed and Q has no cross-coordinate terms, this is the
        # exact energy-sum identity for arbitrary center and x,y,z.
        for index in range(4):
            assert sorted((zero[index], one[index])) == sorted((hybrid[index], complement[index]))
        recombination_certificates.append((class_index, zero, one, hybrid, complement))

assert len(recombination_certificates) == 3 * 48 == 144


def fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def main():
    signature, couplings, gaps = best_record
    print(json.dumps({
        "family": "independent-coupling non-antipodal D4 triality NAND codebooks",
        "gram_rule": "K(x,y,z) tensor I4",
        "coupling_grid": "x,y,z in {-7/16,...,7/16}",
        "positive_definite_gram_count": len(PD_GRAMS),
        "truth_labeling_count": labeling_count,
        "truth_labeling_sha256": LABELING_HASH.hexdigest(),
        "interaction_signature_count": len(INTERACTION_SIGNATURES),
        "compressed_exact_boolean_tests": compressed_tests,
        "exact_candidate_count": candidate_count,
        "strict_false_boolean_survivors": strict_boolean_survivors,
        "surviving_signature_gram_pairs": surviving_signature_gram_pairs,
        "best_strict_boolean_margin": fraction_text(best_margin),
        "best_boolean_record": {
            "interaction_signature": list(signature),
            "couplings_xyz": [fraction_text(value) for value in couplings],
            "false_gaps_000_010_100_111": [fraction_text(value) for value in gaps],
        },
        "failed_boolean_candidate_first_ports": dict(sorted(first_failure_counts.items())),
        "recombination_certificate_count": len(recombination_certificates),
        "recombination_identity": "E(a0,h,c1)+E(a0,h',c1)=E(001)+E(011)=2R^2",
        "global_shell_result": "every strict Boolean survivor has a malformed 2D4* recombination on or inside the legal radius",
        "copy_and_transfer_status": "not authorized after the NAND global-shell failure",
        "finding": "independent couplings create strict Boolean gaps, but coordinate separability forces a malformed recombination into every legal shell",
        "scope": "finite rejection of the frozen independent-coupling grid; nonseparable coordinate Grams remain untested",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
