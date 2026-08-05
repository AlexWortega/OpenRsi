#!/usr/bin/env python3
"""Generation-12 exact audit of a bounded spherical-fingerprint candidate.

The predeclared tag is the top Walsh character on each clause truth table,

    chi(a) = (-1)^(1 + |a|),

placed in one clause-specific coordinate.  Every one-hot local label has tag
squared norm one, so every honest nine-clause encoding gains the same H=9.
The complete unrestricted fixed-target objective is

    ||2z-1||^2 + 25 ||A_{<=3}z-b||^2 + ||Fz||^2.

The tag charges both unique and synchronized seven-term parity selectors.  An
exact shell DP nevertheless finds a cheaper clause-drop vector.  All claims
are finite-instance claims only.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path

from sympy import Matrix

import verify_degree3_global_psd_metric as gen11

PATTERNS = gen11.PATTERNS
MONOMIALS = gen11.MONOMIALS
UNSAT_EDGES = gen11.UNSAT_EDGES
CONTROL_EDGES = gen11.CONTROL_EDGES
N_SELECTORS = gen11.N_SELECTORS
N_CLAUSES = 9
ANCHOR_SCALE = 2
RESIDUAL_SCALE = 5
FINGERPRINT_SCALE = 1
FINGERPRINT_DIMENSION = N_CLAUSES
HONEST_FINGERPRINT_RADIUS2 = N_CLAUSES
COMPLETENESS_RADIUS2 = 72 + HONEST_FINGERPRINT_RADIUS2
AUDIT_THRESHOLD2 = 4 * COMPLETENESS_RADIUS2 // 3
assert 4 * COMPLETENESS_RADIUS2 % 3 == 0
MANIFEST_PATH = Path(__file__).with_name("gen12_spherical_parity_fingerprint_manifest.json")

# The degree-three Walsh character.  Entries lie in the prescribed [-2,2].
PARITY_TAG = tuple((-1) ** (1 + sum(pattern)) for pattern in PATTERNS)
assert PARITY_TAG == (-1, 1, 1, -1, 1, -1, -1, 1)


def sparse(vector):
    return [[index, int(value)] for index, value in enumerate(vector) if value]


def fingerprint_rows():
    rows = []
    for clause in range(N_CLAUSES):
        row = [0] * N_SELECTORS
        row[8 * clause:8 * clause + 8] = PARITY_TAG
        rows.append(tuple(row))
    return tuple(rows)


def factor_and_target(checks):
    factor, target = gen11.factor_and_target(checks)
    tags = fingerprint_rows()
    return factor + tags, target + (0,) * len(tags)


def rational_text(value):
    value = Fraction(int(value.p), int(value.q))
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def matrix_upper_sparse(matrix):
    return [
        [row, column, int(matrix[row, column])]
        for row in range(matrix.rows)
        for column in range(row, matrix.cols)
        if matrix[row, column]
    ]


def factor_hash(factor, target):
    payload = {
        "factor_rows": [sparse(row) for row in factor],
        "target": sparse(target),
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def instance_manifest(name, edges):
    clauses = gen11.gen9.clause_data(edges)
    checks = gen11.build_checks(clauses)
    factor, target = factor_and_target(checks)
    B, t = Matrix(factor), Matrix(target)
    gram = B.T * B
    linear = B.T * t
    center = gram.inv() * linear
    kappa = (t.T * t)[0] - (linear.T * center)[0]
    return {
        "name": name,
        "edges": [list(edge) for edge in edges],
        "clauses": [{
            "edge": list(clause["edge"]),
            "omitted_variable": clause["omitted_variable"],
            "variables": list(clause["variables"]),
            "false_bits": list(clause["false_bits"]),
        } for clause in clauses],
        "check_count": len(checks),
        "checks": [{
            key: (list(value) if isinstance(value, tuple) else value)
            for key, value in check.items() if key != "coefficients"
        } | {"terms": sparse(check["coefficients"])} for check in checks],
        "fingerprint_rows": [{
            "kind": "clause_top_walsh_fingerprint",
            "clause": clause,
            "target": 0,
            "terms": sparse(row),
        } for clause, row in enumerate(fingerprint_rows())],
        "ambient_dimension": len(factor),
        "lattice_rank": N_SELECTORS,
        "factor_rows": [sparse(row) for row in factor],
        "target": sparse(target),
        "factor_target_sha256": factor_hash(factor, target),
        "gram_upper_triangle": matrix_upper_sparse(gram),
        "linear_term": [int(value) for value in linear],
        "center": [rational_text(value) for value in center],
        "orthogonal_target_energy": rational_text(kappa),
        "certified_gram_eigenvalue_lower_bound": 4,
    }


def build_manifest():
    return {
        "schema": "gen12-spherical-parity-fingerprint-v1",
        "finite_claim_only": True,
        "template": {
            "description": (
                "degree-at-most-three global PSD metric plus one top-Walsh "
                "spherical fingerprint coordinate per clause"
            ),
            "predeclared_tag": list(PARITY_TAG),
            "fingerprint_dimension": FINGERPRINT_DIMENSION,
            "fingerprint_entry_interval": [-1, 1],
            "fingerprint_target": 0,
            "honest_fingerprint_squared_radius": HONEST_FINGERPRINT_RADIUS2,
            "objective": "||2z-1||^2 + 25||A_{<=3}z-b||^2 + ||Fz||^2",
            "gram_identity": "Q=4I+25 A_{<=3}^T A_{<=3}+F^T F",
            "equivariance": (
                "clause permutations permute tag rows; local literal flips "
                "change a tag-row sign and leave F^T F invariant"
            ),
            "coefficient_domain": "all integers",
            "external_filters": [],
        },
        "completeness_squared_radius": COMPLETENESS_RADIUS2,
        "four_thirds_audit_threshold_squared": AUDIT_THRESHOLD2,
        "instances": [
            instance_manifest("generation_7_obstruction", UNSAT_EDGES),
            instance_manifest("satisfiable_overlapping_control", CONTROL_EDGES),
        ],
    }


def reconstruct_instance(record):
    clauses = gen11.gen9.clause_data(tuple(tuple(edge) for edge in record["edges"]))
    checks = gen11.build_checks(clauses)
    factor, target = factor_and_target(checks)
    emitted_factor = []
    for terms in record["factor_rows"]:
        row = [0] * N_SELECTORS
        for column, value in terms:
            assert row[column] == 0
            row[column] = value
        emitted_factor.append(tuple(row))
    emitted_target = [0] * record["ambient_dimension"]
    for row, value in record["target"]:
        assert emitted_target[row] == 0
        emitted_target[row] = value
    assert tuple(emitted_factor) == factor
    assert tuple(emitted_target) == target
    return clauses, checks, factor, target


def raw_residual(checks, selector):
    return tuple(
        sum(value * coefficient for value, coefficient in zip(check["coefficients"], selector))
        - check["rhs"]
        for check in checks
    )


def fingerprint(selector):
    return tuple(
        sum(PARITY_TAG[p] * selector[8 * clause + p] for p in range(8))
        for clause in range(N_CLAUSES)
    )


def objective_breakdown(checks, selector):
    anchors = sum((2 * value - 1) ** 2 for value in selector)
    residual = raw_residual(checks, selector)
    tags = fingerprint(selector)
    return {
        "anchor": anchors,
        "raw_residual_squared": sum(value * value for value in residual),
        "fingerprint_squared": sum(value * value for value in tags),
        "total": anchors + 25 * sum(value * value for value in residual)
        + sum(value * value for value in tags),
    }


def local_cost(block):
    """Anchor, fingerprint, normalization, and legality contribution."""
    anchor = sum((2 * value - 1) ** 2 for value in block)
    tag = sum(value * coefficient for value, coefficient in zip(block, PARITY_TAG))
    normalization = sum(block) - 1
    legality = block[0]
    return anchor + tag * tag + 25 * (normalization * normalization + legality * legality)


def bounded_local_states():
    # In a global vector of cost <=108, the other eight blocks contribute at
    # least their anchor lower bound 8 each.  Hence one block has local cost
    # <=44.  A coordinate outside [-2,3] alone gives block anchor >=56.
    local_cap = AUDIT_THRESHOLD2 - 8 * (N_CLAUSES - 1)
    assert local_cap == 44
    states = []
    for block in product(range(-2, 4), repeat=8):
        cost = local_cost(block)
        if cost <= local_cap:
            states.append((cost, block))
    histogram = Counter(cost for cost, _ in states)
    assert len(states) == 1348
    assert histogram == {
        9: 7, 17: 75, 25: 174, 33: 377, 34: 1,
        37: 9, 41: 660, 42: 45,
    }
    return tuple(states)


def exact_shell_dp(clauses):
    """Enumerate every unrestricted integer vector of total cost at most 108.

    Local normalization/legality costs are included directly.  For a global
    monomial, when occurrence value v is inserted after values u_i, the new
    all-pairs residual is sum_i (v-u_i)^2.  The running sum and sum of squares
    are sufficient statistics, so keeping the cheapest path per key is exact.
    """
    states = bounded_local_states()
    dp = {((0, 0),) * len(MONOMIALS): (0, ())}
    layer_counts = []
    for clause_index, clause in enumerate(clauses):
        available = [
            index for index, monomial in enumerate(MONOMIALS)
            if all(variable in clause["variables"] for variable in monomial)
        ]
        previous_counts = {
            index: sum(
                all(variable in clauses[prior]["variables"]
                    for variable in MONOMIALS[index])
                for prior in range(clause_index)
            )
            for index in available
        }
        next_dp = {}
        remaining_blocks = N_CLAUSES - clause_index - 1
        for key, (cost, witness) in dp.items():
            for block_cost, block in states:
                next_cost = cost + block_cost
                if next_cost + 8 * remaining_blocks > AUDIT_THRESHOLD2:
                    continue
                next_key = list(key)
                for index in available:
                    monomial = MONOMIALS[index]
                    value = sum(
                        block[pattern_index]
                        * gen11.gen9.monomial_value(clause, pattern, monomial)
                        for pattern_index, pattern in enumerate(PATTERNS)
                    )
                    old_sum, old_sumsq = next_key[index]
                    count = previous_counts[index]
                    pair_residual = (
                        count * value * value - 2 * value * old_sum + old_sumsq
                    )
                    assert pair_residual >= 0
                    next_cost += 25 * pair_residual
                    if next_cost + 8 * remaining_blocks > AUDIT_THRESHOLD2:
                        break
                    next_key[index] = (
                        old_sum + value,
                        old_sumsq + value * value,
                    )
                else:
                    next_key = tuple(next_key)
                    old = next_dp.get(next_key)
                    if old is None or next_cost < old[0]:
                        next_dp[next_key] = (
                            next_cost,
                            witness + (block,),
                        )
        dp = next_dp
        layer_counts.append(len(dp))
    assert dp
    minimum = min(cost for cost, _ in dp.values())
    key, (cost, blocks) = next(
        (key, record) for key, record in dp.items() if record[0] == minimum
    )
    return {
        "audit_threshold_squared": AUDIT_THRESHOLD2,
        "derived_integer_coefficient_interval": [-2, 3],
        "local_states_checked_per_clause": len(states),
        "local_state_cost_histogram": dict(sorted(Counter(
            state_cost for state_cost, _ in states
        ).items())),
        "dynamic_program_layer_counts": layer_counts,
        "minimum_squared_distance": cost,
        "moment_sum_sumsq_key": [[a, b] for a, b in key],
        "selector": [value for block in blocks for value in block],
    }


def check_emitted_gram(record, factor, target):
    B, t = Matrix(factor), Matrix(target)
    gram = B.T * B
    linear = B.T * t
    center = gram.inv() * linear
    kappa = (t.T * t)[0] - (linear.T * center)[0]
    assert matrix_upper_sparse(gram) == record["gram_upper_triangle"]
    assert [int(value) for value in linear] == record["linear_term"]
    assert [rational_text(value) for value in center] == record["center"]
    assert rational_text(kappa) == record["orthogonal_target_energy"]
    assert all(
        factor[row][column] == (2 if row == column else 0)
        for row in range(N_SELECTORS) for column in range(N_SELECTORS)
    )
    assert record["certified_gram_eigenvalue_lower_bound"] == 4


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
    reconstructed = []
    for record in manifest["instances"]:
        clauses, checks, factor, target = reconstruct_instance(record)
        assert factor_hash(factor, target) == record["factor_target_sha256"]
        assert len(factor) == record["ambient_dimension"]
        assert len(factor[0]) == record["lattice_rank"] == N_SELECTORS
        check_emitted_gram(record, factor, target)
        reconstructed.append((record, clauses, checks))

    unsat_record, unsat_clauses, unsat_checks = reconstructed[0]
    _, control_clauses, control_checks = reconstructed[1]

    # Every one-hot clause block has fingerprint squared norm one, including
    # after local sign flips.  Thus every honest nine-clause encoding has H=9.
    for pattern_index in range(8):
        block = tuple(int(index == pattern_index) for index in range(8))
        assert sum(value * value for value in fingerprint(block * N_CLAUSES)) == 9

    control_assignment = (1, 1, 1, 0)
    control_selector, falsified = gen11.gen9.honest_selector(
        control_clauses, control_assignment
    )
    assert not falsified
    control_breakdown = objective_breakdown(control_checks, control_selector)
    assert control_breakdown == {
        "anchor": 72,
        "raw_residual_squared": 0,
        "fingerprint_squared": 9,
        "total": COMPLETENESS_RADIUS2,
    }

    # Local cost is at least 9 for every integral block: anchor >=8; equality
    # forces a Boolean block, and normalization+legality then force one legal
    # label whose Walsh tag has square one.  The control witness attains 81.
    assert min(cost for cost, _ in bounded_local_states()) == 9
    control_exact_minimum2 = COMPLETENESS_RADIUS2

    inherited_search = gen11.exact_zero_residual_search(unsat_clauses)
    cube_selector = tuple(inherited_search["selector"])
    cube_breakdown = objective_breakdown(unsat_checks, cube_selector)
    assert cube_breakdown["fingerprint_squared"] == 57
    assert cube_breakdown["total"] == 153

    unsat_search = exact_shell_dp(unsat_clauses)
    unsat_selector = tuple(unsat_search["selector"])
    unsat_breakdown = objective_breakdown(unsat_checks, unsat_selector)
    assert unsat_breakdown == {
        "anchor": 72,
        "raw_residual_squared": 1,
        "fingerprint_squared": 8,
        "total": 105,
    }
    assert unsat_search["minimum_squared_distance"] == unsat_breakdown["total"]
    dropped_clauses = [
        clause for clause in range(N_CLAUSES)
        if not any(unsat_selector[8 * clause:8 * clause + 8])
    ]
    assert dropped_clauses == [0]

    # The shell DP includes every vector through 108 and finds minimum 105;
    # its displayed witness makes the global minimum exactly 105.  Independently
    # run the same adversarial shell enumeration on the control.
    control_search = exact_shell_dp(control_clauses)
    assert control_search["minimum_squared_distance"] == control_exact_minimum2
    assert 3 * unsat_breakdown["total"] < 4 * COMPLETENESS_RADIUS2

    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[1])),
        "factor_target_sha256": unsat_record["factor_target_sha256"],
        "fingerprint_dimension": FINGERPRINT_DIMENSION,
        "fingerprint_tag": list(PARITY_TAG),
        "honest_fingerprint_squared_radius": HONEST_FINGERPRINT_RADIUS2,
        "control_exact_unrestricted_minimum_squared": control_exact_minimum2,
        "four_thirds_audit_threshold_squared": AUDIT_THRESHOLD2,
        "inherited_cube_parity_breakdown": cube_breakdown,
        "unsat_exact_shell_search": unsat_search,
        "unsat_nearest_vector_breakdown": unsat_breakdown,
        "dropped_clause": dropped_clauses[0],
        "unsat_exact_unrestricted_minimum_squared": unsat_breakdown["total"],
        "squared_ratio_to_completeness": "35/27",
        "control_shell_search": control_search,
        "finding": (
            "the spherical Walsh tag charges cube parity, but dropping clause 0 "
            "costs 105, below the prescribed four-thirds threshold 108"
        ),
        "scope": "finite falsification of this explicit dimension-9 fingerprint only",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
