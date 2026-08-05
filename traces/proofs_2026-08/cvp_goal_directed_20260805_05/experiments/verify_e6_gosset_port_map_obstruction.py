#!/usr/bin/env python3
"""Generation-6 exact E6 Gosset-cell NAND port-map classification.

Only Fable proposal 3 survives cross-review, with the repaired gate prescribed
by the opponent review.  This verifier freezes the E6 root lattice in a simple
root basis, constructs the 27-vertex minuscule Gosset Delaunay cell, certifies
its empty sphere exactly, and classifies all integral 3x6 port maps with entries
in {-1,0,1}.

After translating one Gosset vertex to zero, any affine port map can likewise
be translated so zero maps to one legal NAND word.  If every shell vertex maps
to the four translated legal words, each row of the linear map must take only
the two values {0,1} or {0,-1} on all 27 vertices.  Exhausting all 3^6 rows
finds only the zero row.  Since every NAND port bit varies among the four legal
words, no 3-row map can be surjective onto all four legal words.  This exact
rowwise reduction covers all 3^18 maps; no unproved symmetry reduction is used.

Thus the E6 shell is genuinely empty, but this bounded integral-map family
cannot supply even a complete local NAND port classification.  COPY and
transfer growth are not authorized.  This is finite evidence only.
"""

from __future__ import annotations

from collections import Counter, deque
from fractions import Fraction
from itertools import product
import hashlib
import json


# Bourbaki-equivalent E6 diagram: 0-1-2-3-4 with node 5 attached to node 2.
CARTAN = (
    (2, -1, 0, 0, 0, 0),
    (-1, 2, -1, 0, 0, 0),
    (0, -1, 2, -1, 0, -1),
    (0, 0, -1, 2, -1, 0),
    (0, 0, 0, -1, 2, 0),
    (0, 0, -1, 0, 0, 2),
)
DIMENSION = 6


def mat_vec(matrix, vector):
    return tuple(sum(matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(matrix)))


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def quadratic(vector):
    return dot(vector, mat_vec(CARTAN, vector))


def determinant_bareiss(matrix):
    work = [list(map(int, row)) for row in matrix]
    sign = 1
    previous = 1
    for pivot in range(len(work) - 1):
        if work[pivot][pivot] == 0:
            swap = next(row for row in range(pivot + 1, len(work)) if work[row][pivot])
            work[pivot], work[swap] = work[swap], work[pivot]
            sign *= -1
        value = work[pivot][pivot]
        for row in range(pivot + 1, len(work)):
            for column in range(pivot + 1, len(work)):
                work[row][column] = (
                    work[row][column] * value - work[row][pivot] * work[pivot][column]
                ) // previous
        previous = value
    return sign * work[-1][-1]


assert determinant_bareiss(CARTAN) == 3


def inverse_fraction(matrix):
    size = len(matrix)
    augmented = [
        [Fraction(matrix[row][column]) for column in range(size)]
        + [Fraction(int(row == column)) for column in range(size)]
        for row in range(size)
    ]
    for column in range(size):
        pivot = next(row for row in range(column, size) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [
                    value - scale * pivot_value
                    for value, pivot_value in zip(augmented[row], augmented[column])
                ]
    return tuple(tuple(row[size:]) for row in augmented)


CARTAN_INVERSE = inverse_fraction(CARTAN)
assert max(CARTAN_INVERSE[index][index] for index in range(DIMENSION)) == 6


def reflect_dynkin(labels, root):
    """Simple reflection on Dynkin labels."""
    coefficient = labels[root]
    return tuple(
        labels[column] - coefficient * CARTAN[root][column]
        for column in range(DIMENSION)
    )


# Node 0 is minuscule.  Its Weyl orbit has 27 weights.
start = (1, 0, 0, 0, 0, 0)
weight_labels = {start}
queue = deque([start])
while queue:
    labels = queue.popleft()
    for root in range(DIMENSION):
        reflected = reflect_dynkin(labels, root)
        if reflected not in weight_labels:
            weight_labels.add(reflected)
            queue.append(reflected)
assert len(weight_labels) == 27


def root_coordinates(labels):
    return tuple(
        sum(CARTAN_INVERSE[row][column] * labels[column] for column in range(DIMENSION))
        for row in range(DIMENSION)
    )


ordered_labels = tuple(sorted(weight_labels))
weights = tuple(root_coordinates(labels) for labels in ordered_labels)
base_weight = weights[0]
vertices = []
for weight in weights:
    translated = tuple(weight[index] - base_weight[index] for index in range(DIMENSION))
    assert all(value.denominator == 1 for value in translated)
    vertices.append(tuple(value.numerator for value in translated))
vertices = tuple(sorted(vertices))
assert len(set(vertices)) == 27
assert (0,) * DIMENSION in vertices

# Original minuscule weights have norm 4/3.  After translating base_weight to
# zero, the Delaunay center is -base_weight.
center = tuple(-value for value in base_weight)
center_thirds = tuple(3 * value for value in center)
assert all(value.denominator == 1 for value in center_thirds)
center_numerator = tuple(value.numerator for value in center_thirds)
assert center_numerator == (2, 1, 0, -1, -2, 0)
radius_squared = Fraction(4, 3)


def scaled_centered_cost(point):
    """Return 9*||point-center||_Cartan^2 as an integer."""
    displacement = tuple(3 * point[index] - center_numerator[index] for index in range(DIMENSION))
    return quadratic(displacement)


assert all(scaled_centered_cost(vertex) == 12 for vertex in vertices)

# Exact all-lattice empty-sphere certificate.  If cost<=4/3 then, by
# |v_i|^2 <= cost*(A^{-1})_ii <= 8, each centered coordinate has magnitude <3.
# Since |center_i|<=2/3, every integer lattice coordinate lies in [-3,3].
assert max(abs(value) for value in center) == Fraction(2, 3)
inside_or_shell = []
for point in product(range(-3, 4), repeat=DIMENSION):
    cost9 = scaled_centered_cost(point)
    if cost9 <= 12:
        inside_or_shell.append((point, cost9))
assert len(inside_or_shell) == 27
assert {point for point, _cost in inside_or_shell} == set(vertices)
assert {cost for _point, cost in inside_or_shell} == {12}

VERTEX_HASH = hashlib.sha256(
    json.dumps([list(vertex) for vertex in vertices], separators=(",", ":")).encode()
).hexdigest()

# Generate every translated/per-port-relabelled NAND legal relation containing
# zero.  This records the exact target family even though the row obstruction
# below already kills every map.
NAND_LEGAL = tuple(
    word for word in product((0, 1), repeat=3)
    if word[2] == 1 - (word[0] & word[1])
)
assert NAND_LEGAL == ((0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0))
translated_relations = set()
for flips in product((0, 1), repeat=3):
    relabelled = tuple(tuple(word[index] ^ flips[index] for index in range(3)) for word in NAND_LEGAL)
    for base in relabelled:
        translated_relations.add(tuple(sorted(
            tuple(word[index] - base[index] for index in range(3))
            for word in relabelled
        )))
assert len(translated_relations) == 32
assert all((0, 0, 0) in relation for relation in translated_relations)
assert all(
    len({word[coordinate] for word in relation}) == 2
    for relation in translated_relations for coordinate in range(3)
)

# Full 3^6 row enumeration.  Any 3x6 map whose 27 images lie in one translated
# legal relation must have each row valued in {0,1} or {0,-1}.  Zero is present
# because the translated cell contains the zero vertex.
row_value_set_histogram = Counter()
admissible_rows = []
for row in product((-1, 0, 1), repeat=DIMENSION):
    values = tuple(dot(row, vertex) for vertex in vertices)
    value_set = frozenset(values)
    row_value_set_histogram[(min(value_set), max(value_set), len(value_set))] += 1
    if value_set <= {0, 1} or value_set <= {0, -1}:
        admissible_rows.append((row, value_set))

assert admissible_rows == [((0, 0, 0, 0, 0, 0), frozenset({0}))]
# The sole row cannot realize either value of any port bit, so no 3-row map is
# surjective onto a four-word translated NAND relation.
assert all(len(value_set) < 2 for _row, value_set in admissible_rows)
nominal_map_count = 3 ** (3 * DIMENSION)
assert nominal_map_count == 387420489


def main():
    print(json.dumps({
        "lattice": "E6 root lattice in a simple-root basis",
        "cartan_determinant": 3,
        "gosset_vertex_count": len(vertices),
        "gosset_vertices_sha256": VERTEX_HASH,
        "circumcenter": [str(value) for value in center],
        "radius_squared": str(radius_squared),
        "coefficient_bound": "every point through radius lies in [-3,3]^6 by the exact A^{-1} diagonal bound",
        "enumerated_lattice_points": 7 ** 6,
        "inside_or_shell_lattice_points": len(inside_or_shell),
        "strictly_inside_lattice_points": 0,
        "empty_sphere_certificate": "the 27 Gosset vertices are exactly all E6 points at cost <=4/3",
        "translated_relabelled_nand_relations": len(translated_relations),
        "row_search_count": 3 ** DIMENSION,
        "nominal_3x6_map_count_covered": nominal_map_count,
        "admissible_binary_rows": len(admissible_rows),
        "admissible_rows": [list(row) for row, _values in admissible_rows],
        "map_survivors": 0,
        "classification_result": "no integral {-1,0,1} port map sends all 27 shell vertices onto exactly the four legal NAND words",
        "copy_and_transfer_status": "not authorized after NAND port-map failure",
        "finding": "the E6 Gosset shell is exactly empty, but every nonzero bounded integral row takes at least three shell values",
        "scope": "finite rejection of the prescribed E6 port-map family; no claim about larger maps or other Delaunay cells",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
