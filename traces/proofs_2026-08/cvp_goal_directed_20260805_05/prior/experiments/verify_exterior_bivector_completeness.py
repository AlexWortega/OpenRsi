#!/usr/bin/env python3
"""Generation-33 preregistered completeness audit for exterior tags.

Each of the eight local labels receives the six Plucker coordinates of
v(t) wedge v(t+1), where v(t)=(1,t,t^2,t^3) and t is the label index.
For every one of the 2^9 clause-incidence sign rules, sum the selected tags
in one shared six-dimensional block.  Exact rational linear algebra asks
whether the 16 globally consistent encodings lie on any sphere, allowing an
arbitrary rational center.

No sign rule is cospherical for either the matched control or obstruction:
the center-equation matrix always has rank 4 and augmented rank 5.  The
preregistered equal-completeness condition therefore fails before any CVP
shell search.  This is a finite kill of this exact tag/sign family only.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import reduce
from itertools import product
import hashlib
import json
import math
from pathlib import Path

from sympy import Matrix, ilcm

import verify_global_psd_metric as gen9

TAG_DIMENSION = 6
LABEL_COUNT = 8
CLAUSE_COUNT = 9
SIGN_RULE_COUNT = 2 ** CLAUSE_COUNT
MANIFEST_PATH = Path(__file__).with_name("gen33_exterior_bivector_completeness_manifest.json")


def vandermonde(t):
    return (1, t, t * t, t * t * t)


def bivector_tag(label):
    left = vandermonde(label)
    right = vandermonde(label + 1)
    return tuple(
        left[i] * right[j] - left[j] * right[i]
        for i in range(4) for j in range(i + 1, 4)
    )


TAGS = tuple(bivector_tag(label) for label in range(LABEL_COUNT))


def plucker_value(tag):
    p01, p02, p03, p12, p13, p23 = tag
    return p01 * p23 - p02 * p13 + p03 * p12


def honest_label_table(edges):
    clauses = gen9.clause_data(edges)
    records = []
    for assignment in product((0, 1), repeat=4):
        selector, _ = gen9.honest_selector(clauses, assignment)
        labels = tuple(
            selector[8 * clause:8 * clause + 8].index(1)
            for clause in range(CLAUSE_COUNT)
        )
        records.append({
            "assignment": assignment,
            "labels": labels,
        })
    return tuple(records)


def global_points(label_table, signs):
    points = []
    for record in label_table:
        point = [0] * TAG_DIMENSION
        for clause, label in enumerate(record["labels"]):
            for coordinate, value in enumerate(TAGS[label]):
                point[coordinate] += signs[clause] * value
        points.append(tuple(point))
    return tuple(points)


def sphere_system(points):
    reference = points[0]
    matrix = Matrix([
        [2 * (point[coordinate] - reference[coordinate]) for coordinate in range(TAG_DIMENSION)]
        for point in points[1:]
    ])
    rhs = Matrix([
        sum(value * value for value in point)
        - sum(value * value for value in reference)
        for point in points[1:]
    ])
    return matrix, rhs


def primitive_integer_vector(vector):
    denominator = ilcm(*[value.q for value in vector])
    integers = [int(value * denominator) for value in vector]
    divisor = reduce(math.gcd, (abs(value) for value in integers if value), 0)
    if divisor:
        integers = [value // divisor for value in integers]
    first = next((value for value in integers if value), 1)
    if first < 0:
        integers = [-value for value in integers]
    return tuple(integers)


def inconsistency_certificate(matrix, rhs):
    for vector in matrix.T.nullspace():
        pairing = (vector.T * rhs)[0]
        if pairing:
            integer_vector = primitive_integer_vector(vector)
            integer_pairing = sum(integer_vector[index] * int(rhs[index]) for index in range(rhs.rows))
            assert integer_pairing
            assert all(
                sum(integer_vector[row] * int(matrix[row, column]) for row in range(matrix.rows)) == 0
                for column in range(matrix.cols)
            )
            return integer_vector, integer_pairing
    raise AssertionError("inconsistent system lacks a left-kernel certificate")


def audit_formula(name, edges):
    label_table = honest_label_table(edges)
    rank_histogram = Counter()
    cospherical = []
    best_zero_centered = None
    representative_certificate = None

    for signs in product((-1, 1), repeat=CLAUSE_COUNT):
        points = global_points(label_table, signs)
        matrix, rhs = sphere_system(points)
        rank = matrix.rank()
        augmented_rank = matrix.row_join(rhs).rank()
        rank_histogram[(rank, augmented_rank)] += 1
        if rank == augmented_rank:
            cospherical.append(signs)

        norms = tuple(sum(value * value for value in point) for point in points)
        spread = max(norms) - min(norms)
        candidate = (spread, signs, min(norms), max(norms), len(set(norms)))
        if best_zero_centered is None or candidate < best_zero_centered:
            best_zero_centered = candidate

        if signs == (-1,) * CLAUSE_COUNT:
            certificate, pairing = inconsistency_certificate(matrix, rhs)
            representative_certificate = {
                "signs": list(signs),
                "left_kernel_vector": list(certificate),
                "nonzero_rhs_pairing": pairing,
                "matrix_rank": rank,
                "augmented_rank": augmented_rank,
            }

    assert len(cospherical) == 0
    assert rank_histogram == {(4, 5): SIGN_RULE_COUNT}
    assert representative_certificate is not None
    return {
        "name": name,
        "honest_encoding_count": len(label_table),
        "label_table": [{
            "assignment": list(record["assignment"]),
            "labels": list(record["labels"]),
        } for record in label_table],
        "sign_rules_checked": SIGN_RULE_COUNT,
        "cospherical_sign_rule_count": len(cospherical),
        "rank_augmented_rank_histogram": {
            f"{rank},{augmented}": count
            for (rank, augmented), count in sorted(rank_histogram.items())
        },
        "best_zero_centered_norm_spread": {
            "spread": best_zero_centered[0],
            "signs": list(best_zero_centered[1]),
            "minimum_squared_norm": best_zero_centered[2],
            "maximum_squared_norm": best_zero_centered[3],
            "distinct_squared_norm_count": best_zero_centered[4],
        },
        "representative_inconsistency_certificate": representative_certificate,
    }


def tag_hash():
    return hashlib.sha256(
        json.dumps(TAGS, separators=(",", ":")).encode()
    ).hexdigest()


def build_manifest():
    return {
        "schema": "gen33-exterior-bivector-completeness-v1",
        "finite_claim_only": True,
        "selected_proposal": "Fable proposal 6: exterior-algebra coherence fingerprint",
        "mechanism": "shared exterior tags might make affine parity energy coherent across clauses and copies",
        "expected_move": "all honest encodings have a common completeness sphere before one/two-copy soundness search",
        "falsification_condition": "no canonical incidence-sign rule admits a common rational center and radius",
        "tag_rule": "Plucker coordinates of v(t) wedge v(t+1), v(t)=(1,t,t^2,t^3), t=0,...,7",
        "coordinate_order": ["01", "02", "03", "12", "13", "23"],
        "integral_bivector_tags": [list(tag) for tag in TAGS],
        "tag_sha256": tag_hash(),
        "plucker_values": [plucker_value(tag) for tag in TAGS],
        "incidence_sign_rule": {
            "domain": "all clausewise signs in {-1,+1}^9",
            "canonical_order": "lexicographic with -1 before +1",
            "rule_count": SIGN_RULE_COUNT,
            "chosen_rule": None,
        },
        "center_rule": "arbitrary rational c in Q^6, tested by 2(p_i-p_0).c=||p_i||^2-||p_0||^2",
        "precondition_result": "REJECT: no equal-completeness sphere, so no CVP factor/target or shell is authorized",
        "formula_audits": [
            audit_formula("satisfiable_overlapping_control", gen9.CONTROL_EDGES),
            audit_formula("generation7_obstruction", gen9.UNSAT_EDGES),
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args()

    assert len(set(TAGS)) == LABEL_COUNT
    assert all(plucker_value(tag) == 0 for tag in TAGS)
    expected = build_manifest()
    if args.write_manifest:
        MANIFEST_PATH.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
        print(MANIFEST_PATH)
        return

    manifest = json.loads(MANIFEST_PATH.read_text())
    assert manifest == expected
    control, obstruction = manifest["formula_audits"]
    assert control["rank_augmented_rank_histogram"] == {"4,5": 512}
    assert obstruction["rank_augmented_rank_histogram"] == {"4,5": 512}
    assert control["cospherical_sign_rule_count"] == 0
    assert obstruction["cospherical_sign_rule_count"] == 0
    assert control["best_zero_centered_norm_spread"] == {
        "spread": 9340400,
        "signs": [-1, 1, 1, -1, 1, -1, -1, 1, 1],
        "minimum_squared_norm": 202907,
        "maximum_squared_norm": 9543307,
        "distinct_squared_norm_count": 12,
    }
    assert obstruction["best_zero_centered_norm_spread"] == {
        "spread": 8094048,
        "signs": [-1, 1, -1, 1, 1, -1, -1, 1, -1],
        "minimum_squared_norm": 116339,
        "maximum_squared_norm": 8210387,
        "distinct_squared_norm_count": 14,
    }

    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[1])),
        "tag_dimension": TAG_DIMENSION,
        "integral_bivector_tags": manifest["integral_bivector_tags"],
        "plucker_values": manifest["plucker_values"],
        "sign_rules_checked_per_formula": SIGN_RULE_COUNT,
        "control_rank_audit": control["rank_augmented_rank_histogram"],
        "obstruction_rank_audit": obstruction["rank_augmented_rank_histogram"],
        "control_cospherical_rules": control["cospherical_sign_rule_count"],
        "obstruction_cospherical_rules": obstruction["cospherical_sign_rule_count"],
        "control_best_zero_centered_spread": control["best_zero_centered_norm_spread"],
        "obstruction_best_zero_centered_spread": obstruction["best_zero_centered_norm_spread"],
        "finding": "all 512 incidence-sign rules fail the exact common-sphere equations already on the matched control",
        "scope": "finite kill of this exact bivector/sign family; no claim about arbitrary exterior Grams",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
