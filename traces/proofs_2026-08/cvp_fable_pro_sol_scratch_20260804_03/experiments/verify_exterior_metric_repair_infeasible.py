#!/usr/bin/env python3
"""Generation-34 exact metric-repair feasibility audit for G33 tags.

For each of the same 512 clause-sign rules, seek one symmetric rational 6x6
Gram G shared by the control and obstruction, with separate centers/radii,
trace(G)=1, and G >= I/100.  Equal-sphere equations are linearized by h=Gc.
Eliminating each formula's center yields homogeneous linear constraints on
the 21 upper-triangular entries of G.

For every sign rule the combined exact constraint row space is identical. Its
RREF contains the unit equation G[1,1]=0.  This contradicts G-I/100 >= 0,
which requires G[1,1]>=1/100.  Thus all 512 repairs are algebraically
infeasible before any factor or shell search.  This is finite evidence only.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import product
import hashlib
import json
from pathlib import Path

from sympy import Matrix

import verify_exterior_bivector_completeness as gen33
import verify_global_psd_metric as gen9

DIMENSION = 6
GRAM_PAIRS = tuple((i, j) for i in range(DIMENSION) for j in range(i, DIMENSION))
GRAM_VARIABLE_COUNT = len(GRAM_PAIRS)
DIAGONAL_ONE_INDEX = GRAM_PAIRS.index((1, 1))
SIGN_RULE_COUNT = 512
LOWER_BOUND = "1/100"
MANIFEST_PATH = Path(__file__).with_name("gen34_exterior_metric_repair_manifest.json")


def affine_sphere_constraints(points):
    """Eliminate center/radius and return exact homogeneous rows on Gram(G)."""
    # Equal G-squared radii mean q_i=p_i^T G p_i lies in the column space of
    # [1,p_i].  Every alpha in its left kernel therefore gives
    # sum_i alpha_i p_i^T G p_i=0.
    design = Matrix([[1, *point] for point in points])
    dependencies = design.T.nullspace()
    rows = []
    for alpha in dependencies:
        row = []
        for left, right in GRAM_PAIRS:
            value = sum(
                alpha[index] * points[index][left] * points[index][right]
                for index in range(len(points))
            )
            row.append(value if left == right else 2 * value)
        rows.append(row)
    assert design.rank() == 5
    assert len(dependencies) == 11
    return Matrix(rows)


def rational_text(value):
    return str(value.p) if value.q == 1 else f"{value.p}/{value.q}"


def canonical_nonzero_rref_rows(rref):
    return [
        [rational_text(value) for value in rref.row(row)]
        for row in range(rref.rows)
        if any(rref[row, column] for column in range(rref.cols))
    ]


def rref_hash(rows):
    return hashlib.sha256(
        json.dumps(rows, separators=(",", ":")).encode()
    ).hexdigest()


def audit_all_sign_rules():
    control_table = gen33.honest_label_table(gen9.CONTROL_EDGES)
    obstruction_table = gen33.honest_label_table(gen9.UNSAT_EDGES)
    pivot_histogram = Counter()
    rref_hash_histogram = Counter()
    representative_rows = None

    for signs in product((-1, 1), repeat=9):
        control_points = gen33.global_points(control_table, signs)
        obstruction_points = gen33.global_points(obstruction_table, signs)
        control_constraints = affine_sphere_constraints(control_points)
        obstruction_constraints = affine_sphere_constraints(obstruction_points)
        combined = control_constraints.col_join(obstruction_constraints)
        rref, pivots = combined.rref()
        rows = canonical_nonzero_rref_rows(rref)
        digest = rref_hash(rows)
        pivot_histogram[pivots] += 1
        rref_hash_histogram[digest] += 1

        # Exact facial-reduction certificate: the unit equation on G[1,1]
        # belongs to the homogeneous equal-sphere constraint row space.
        unit = ["0"] * GRAM_VARIABLE_COUNT
        unit[DIAGONAL_ONE_INDEX] = "1"
        assert unit in rows
        if representative_rows is None:
            representative_rows = rows

    expected_pivots = (6, 7, 9, 10, 11, 13, 14, 18, 19, 20)
    assert pivot_histogram == {expected_pivots: SIGN_RULE_COUNT}
    assert len(rref_hash_histogram) == 1
    assert representative_rows is not None
    return {
        "sign_rules_checked": SIGN_RULE_COUNT,
        "combined_constraint_rank_histogram": {"10": SIGN_RULE_COUNT},
        "pivot_columns": list(expected_pivots),
        "distinct_combined_rref_count": len(rref_hash_histogram),
        "common_rref_sha256": next(iter(rref_hash_histogram)),
        "common_nonzero_rref_rows": representative_rows,
        "forced_zero_gram_entry": {
            "matrix_coordinate": [1, 1],
            "upper_triangle_variable_index": DIAGONAL_ONE_INDEX,
            "equation": "G[1,1]=0",
        },
    }


def build_manifest():
    return {
        "schema": "gen34-exterior-metric-repair-v1",
        "finite_claim_only": True,
        "selected_proposal": "Fable proposal 1: positive-definite Gram repair of G33 exterior tags",
        "mechanism": "a learned positive-definite metric might restore equal completeness for shared bivector fingerprints",
        "expected_move": "one shared rational G and separate formula centers make both 16-point honest sets cospherical",
        "falsification_condition": "exact infeasibility or only singular metrics",
        "tag_manifest": "experiments/gen33_exterior_bivector_completeness_manifest.json",
        "integral_bivector_tags": [list(tag) for tag in gen33.TAGS],
        "gram_variable_order": [list(pair) for pair in GRAM_PAIRS],
        "metric_constraints": {
            "symmetric_dimension": DIMENSION,
            "trace": "1",
            "lower_bound": "G-(1/100)I positive semidefinite",
            "shared_metric": True,
            "separate_control_obstruction_centers_and_radii": True,
        },
        "linearization": (
            "for each formula, affine dependencies alpha of [1,p_i] impose "
            "sum_i alpha_i p_i^T G p_i=0; positive definite G then recovers c=G^-1 h"
        ),
        "exact_audit": audit_all_sign_rules(),
        "infeasibility_certificate": {
            "equal_sphere_constraints_force": "G[1,1]=0",
            "positive_definite_lower_bound_forces": "G[1,1]>=1/100",
            "conclusion": "all 512 sign rules infeasible; trace normalization cannot repair the contradiction",
        },
        "precondition_result": "REJECT: no rational factor/center exists, so no soundness shell is authorized",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args()

    expected = build_manifest()
    if args.write_manifest:
        MANIFEST_PATH.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
        print(MANIFEST_PATH)
        return

    manifest = json.loads(MANIFEST_PATH.read_text())
    assert manifest == expected
    audit = manifest["exact_audit"]
    assert audit["sign_rules_checked"] == 512
    assert audit["distinct_combined_rref_count"] == 1
    assert audit["combined_constraint_rank_histogram"] == {"10": 512}
    assert audit["forced_zero_gram_entry"] == {
        "matrix_coordinate": [1, 1],
        "upper_triangle_variable_index": 6,
        "equation": "G[1,1]=0",
    }
    unit = ["0"] * GRAM_VARIABLE_COUNT
    unit[DIAGONAL_ONE_INDEX] = "1"
    assert unit in audit["common_nonzero_rref_rows"]

    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[1])),
        "sign_rules_checked": audit["sign_rules_checked"],
        "combined_constraint_rank_histogram": audit["combined_constraint_rank_histogram"],
        "distinct_combined_rref_count": audit["distinct_combined_rref_count"],
        "common_rref_sha256": audit["common_rref_sha256"],
        "forced_zero_gram_entry": audit["forced_zero_gram_entry"],
        "metric_lower_bound": manifest["metric_constraints"]["lower_bound"],
        "finding": "equal-sphere constraints force G[1,1]=0 for every sign rule, contradicting G>=I/100",
        "scope": "finite infeasibility of this repaired G33 family; no claim about arbitrary tags or metrics",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
