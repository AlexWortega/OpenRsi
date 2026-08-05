#!/usr/bin/env python3
"""Generation-11 exact audit of the authorized cubic-moment mutation.

This extends the Generation-9 fixed-target lattice by every available
squarefree global degree-three moment-consistency row.  The objective is

    ||2z-1||^2 + 25 ||A_{<=3} z-b||^2

with unrestricted integral selector coefficients.  All rows, the rational
Gram factor, target, Gram matrix, and center are emitted in the checked
manifest.  The experiment is finite evidence only.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

from sympy import Matrix

import verify_global_psd_metric as gen9

PATTERNS = gen9.PATTERNS
UNSAT_EDGES = gen9.UNSAT_EDGES
CONTROL_EDGES = gen9.CONTROL_EDGES
N_SELECTORS = gen9.N_SELECTORS
BASELINE_RADIUS2 = gen9.BASELINE_RADIUS2
ANCHOR_SCALE = gen9.ANCHOR_SCALE
RESIDUAL_SCALE = gen9.RESIDUAL_SCALE
MAX_ZERO_KERNEL_EXTRA = 24
MONOMIALS = (
    tuple((i,) for i in range(4))
    + tuple(combinations(range(4), 2))
    + tuple(combinations(range(4), 3))
)
MANIFEST_PATH = Path(__file__).with_name("gen11_degree3_global_psd_metric_manifest.json")


def sparse(vector):
    return [[index, int(value)] for index, value in enumerate(vector) if value]


def build_checks(clauses):
    """Emit degree zero/legality and all-pairs degree 1--3 consistency."""
    checks = []
    for clause_index in range(len(clauses)):
        row = [0] * N_SELECTORS
        for pattern_index in range(8):
            row[gen9.selector_index(clause_index, pattern_index)] = 1
        checks.append({
            "kind": "normalization",
            "degree": 0,
            "clause": clause_index,
            "coefficients": tuple(row),
            "rhs": 1,
        })

        row = [0] * N_SELECTORS
        row[gen9.selector_index(clause_index, 0)] = 1
        checks.append({
            "kind": "legality",
            "degree": 3,
            "clause": clause_index,
            "coefficients": tuple(row),
            "rhs": 0,
        })

    for monomial in MONOMIALS:
        occurrences = [
            clause_index for clause_index, clause in enumerate(clauses)
            if all(variable in clause["variables"] for variable in monomial)
        ]
        for left_clause, right_clause in combinations(occurrences, 2):
            row = [0] * N_SELECTORS
            for sign, clause_index in ((1, left_clause), (-1, right_clause)):
                clause = clauses[clause_index]
                for pattern_index, pattern in enumerate(PATTERNS):
                    row[gen9.selector_index(clause_index, pattern_index)] += (
                        sign * gen9.monomial_value(clause, pattern, monomial)
                    )
            checks.append({
                "kind": "moment_consistency",
                "degree": len(monomial),
                "monomial": monomial,
                "clauses": (left_clause, right_clause),
                "coefficients": tuple(row),
                "rhs": 0,
            })
    return tuple(checks)


def factor_and_target(checks):
    rows = []
    target = []
    for selector in range(N_SELECTORS):
        row = [0] * N_SELECTORS
        row[selector] = ANCHOR_SCALE
        rows.append(tuple(row))
        target.append(1)
    for check in checks:
        rows.append(tuple(RESIDUAL_SCALE * value for value in check["coefficients"]))
        target.append(RESIDUAL_SCALE * check["rhs"])
    return tuple(rows), tuple(target)


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
    clauses = gen9.clause_data(edges)
    checks = build_checks(clauses)
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
        "check_count_by_degree": {
            str(degree): count for degree, count in sorted(Counter(
                check["degree"] for check in checks
            ).items())
        },
        "checks": [{
            key: (list(value) if isinstance(value, tuple) else value)
            for key, value in check.items() if key != "coefficients"
        } | {"terms": sparse(check["coefficients"])} for check in checks],
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
        "schema": "gen11-degree3-global-psd-metric-v1",
        "finite_claim_only": True,
        "template": {
            "description": (
                "anchors, normalization, legality, and all-pairs consistency "
                "of every available squarefree global moment of degree 1--3"
            ),
            "anchor_scale": ANCHOR_SCALE,
            "residual_scale": RESIDUAL_SCALE,
            "gram_identity": "Q=4I+25 A_{<=3}^T A_{<=3}",
            "coefficient_domain": "all integers",
            "external_filters": [],
        },
        "baseline_squared_radius": BASELINE_RADIUS2,
        "instances": [
            instance_manifest("generation_7_obstruction", UNSAT_EDGES),
            instance_manifest("satisfiable_overlapping_control", CONTROL_EDGES),
        ],
    }


def reconstruct_instance(record):
    clauses = gen9.clause_data(tuple(tuple(edge) for edge in record["edges"]))
    checks = build_checks(clauses)
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


def residual(checks, selector):
    return tuple(
        sum(value * coefficient for value, coefficient in zip(check["coefficients"], selector))
        - check["rhs"]
        for check in checks
    )


def squared_distance(checks, selector):
    anchor = sum((ANCHOR_SCALE * value - 1) ** 2 for value in selector)
    raw = residual(checks, selector)
    return anchor + RESIDUAL_SCALE ** 2 * sum(value * value for value in raw)


def local_states_through_extra_24():
    # In a zero-residual vector legality fixes the forbidden coordinate to zero
    # and normalization fixes the block sum to one.  Through anchor extra 24,
    # every integral coordinate lies in the derived interval [-2,3].
    states = []
    for legal_values in product(range(-2, 4), repeat=7):
        block = (0,) + legal_values
        if sum(block) != 1:
            continue
        extra = sum(4 * value * (value - 1) for value in block)
        if extra > MAX_ZERO_KERNEL_EXTRA:
            continue
        states.append((extra, block))
    assert Counter(extra for extra, _ in states) == {0: 7, 8: 105, 16: 252, 24: 595}
    return tuple(states)


def global_state_record(clause, state):
    extra, block = state
    moments = {}
    for monomial in MONOMIALS:
        if all(variable in clause["variables"] for variable in monomial):
            moments[monomial] = sum(
                block[pattern_index] * gen9.monomial_value(clause, pattern, monomial)
                for pattern_index, pattern in enumerate(PATTERNS)
            )
    return extra, block, moments


def exact_zero_residual_search(clauses):
    """Exact DP over every signed normalized/legal state through extra 24."""
    states = local_states_through_extra_24()
    tables = [
        tuple(global_state_record(clause, state) for state in states)
        for clause in clauses
    ]
    dp = {(None,) * len(MONOMIALS): (0, ())}
    layer_counts = []
    for table in tables:
        next_dp = {}
        for key, (cost, witness) in dp.items():
            for extra, block, moments in table:
                next_cost = cost + extra
                if next_cost > MAX_ZERO_KERNEL_EXTRA:
                    continue
                next_key = list(key)
                compatible = True
                for monomial, value in moments.items():
                    index = MONOMIALS.index(monomial)
                    if next_key[index] is None:
                        next_key[index] = value
                    elif next_key[index] != value:
                        compatible = False
                        break
                if not compatible:
                    continue
                next_key = tuple(next_key)
                old = next_dp.get(next_key)
                if old is None or next_cost < old[0]:
                    next_dp[next_key] = (next_cost, witness + (block,))
        dp = next_dp
        layer_counts.append(len(dp))
    assert dp
    minimum = min(cost for cost, _ in dp.values())
    key, (cost, blocks) = next(
        (key, record) for key, record in dp.items() if record[0] == minimum
    )
    return {
        "local_states_checked_per_clause": len(states),
        "local_state_extra_histogram": dict(sorted(Counter(
            extra for extra, _ in states
        ).items())),
        "dynamic_program_layer_counts": layer_counts,
        "minimum_anchor_extra": cost,
        "global_moments": list(key),
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
    # The displayed factor starts with 2I, certifying full rank and
    # Q=4I+25 A^T A >= 4I over all real, hence all integral, coefficients.
    assert all(
        factor[row][column] == (2 if row == column else 0)
        for row in range(N_SELECTORS) for column in range(N_SELECTORS)
    )
    assert record["certified_gram_eigenvalue_lower_bound"] == 4


def seven_term_attack(clauses, assignment, attacked_clause):
    selector, falsified = gen9.honest_selector(clauses, assignment)
    assert attacked_clause in falsified
    selector = list(selector)
    parity_block = (0, 1, 1, -1, 1, -1, -1, 1)
    selector[8 * attacked_clause:8 * attacked_clause + 8] = parity_block
    return tuple(selector)


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
        reconstructed.append((record, clauses, checks, factor, target))

    unsat_record, unsat_clauses, unsat_checks, _, _ = reconstructed[0]
    _, control_clauses, control_checks, _, _ = reconstructed[1]

    # The formula is unsatisfiable by direct coverage of all 16 assignments.
    coverage = {}
    for assignment in product((0, 1), repeat=4):
        _, falsified = gen9.honest_selector(unsat_clauses, assignment)
        assert falsified
        coverage["".join(map(str, assignment))] = list(falsified)
    assert len(coverage) == 16

    # Honest witnesses make every emitted moment row zero.  The universal
    # integral anchor lower bound proves the control optimum is exactly 72.
    control_assignment = (1, 1, 1, 0)
    control_selector, falsified = gen9.honest_selector(control_clauses, control_assignment)
    assert not falsified
    assert not any(residual(control_checks, control_selector))
    assert squared_distance(control_checks, control_selector) == BASELINE_RADIUS2
    control_exact_minimum2 = BASELINE_RADIUS2

    # The old three-term attack is charged already in degree two, and gains
    # two additional nonzero cubic comparisons in clause 0's occurrence class.
    old_attack, falsified = gen9.honest_selector(unsat_clauses, (0, 0, 0, 0))
    assert falsified == (0,)
    old_attack = list(old_attack)
    old_attack[gen9.selector_index(0, 0)] = 0
    old_attack[gen9.selector_index(0, PATTERNS.index((0, 1, 1)))] = 1
    old_attack[gen9.selector_index(0, PATTERNS.index((1, 0, 0)))] = 1
    old_attack[gen9.selector_index(0, PATTERNS.index((1, 1, 1)))] = -1
    old_attack = tuple(old_attack)
    old_raw = residual(unsat_checks, old_attack)

    # Reconstruct the deterministic Generation-9 nearest witness (clause 3).
    inherited_search = gen9.exact_zero_residual_search(unsat_clauses)
    inherited_selector = tuple(inherited_search["selector"])
    inherited_raw = residual(unsat_checks, inherited_selector)
    assert not any(gen9.residual(gen9.build_checks(unsat_clauses), inherited_selector))
    assert sum(value * value for value in inherited_raw) == 1

    search = exact_zero_residual_search(unsat_clauses)
    assert search["minimum_anchor_extra"] == MAX_ZERO_KERNEL_EXTRA
    surviving_selector = tuple(search["selector"])
    surviving_raw = residual(unsat_checks, surviving_selector)
    assert not any(surviving_raw)
    assert squared_distance(unsat_checks, surviving_selector) == 96

    # The surviving cube parity sits in clause 1, the unique occurrence of
    # global triple (0,2,3).  No all-pairs consistency row exists for a single
    # occurrence, so its altered top moment is invisible.
    changed_blocks = [
        clause for clause in range(9)
        if sum(4 * value * (value - 1)
               for value in surviving_selector[8 * clause:8 * clause + 8])
    ]
    assert changed_blocks == [1]
    triple_occurrences = {
        monomial: sum(
            all(variable in clause["variables"] for variable in monomial)
            for clause in unsat_clauses
        )
        for monomial in combinations(range(4), 3)
    }
    assert triple_occurrences[(0, 2, 3)] == 1

    # Exact unrestricted minimum: every integral anchor costs at least 72.
    # A nonzero integral residual costs at least 25, hence at least 97.  In the
    # zero-residual branch the exhaustive derived-shell DP proves extra >=24,
    # and the displayed selector attains it.
    assert BASELINE_RADIUS2 + RESIDUAL_SCALE ** 2 == 97
    unsat_exact_minimum2 = 96
    assert 100 * unsat_exact_minimum2 > 121 * control_exact_minimum2

    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[1])),
        "factor_target_sha256": unsat_record["factor_target_sha256"],
        "unsat_check_count": len(unsat_checks),
        "check_count_by_degree": unsat_record["check_count_by_degree"],
        "triple_occurrence_counts": {str(key): value for key, value in triple_occurrences.items()},
        "covered_unsat_assignments": len(coverage),
        "control_exact_unrestricted_minimum_squared": control_exact_minimum2,
        "old_three_term_attack_residual_squared": sum(value * value for value in old_raw),
        "old_three_term_attack_distance_squared": squared_distance(unsat_checks, old_attack),
        "inherited_seven_term_attack_residual_squared": sum(value * value for value in inherited_raw),
        "inherited_seven_term_attack_distance_squared": squared_distance(unsat_checks, inherited_selector),
        "exact_degree_0_through_3_zero_kernel_search": search,
        "surviving_attack_clause": changed_blocks[0],
        "unsat_exact_unrestricted_minimum_squared": unsat_exact_minimum2,
        "squared_distance_ratio": "4/3",
        "finding": (
            "cubic rows charge the inherited clause-3 parity witness but a clause-1 "
            "seven-term parity remains an exact zero residual at the same distance"
        ),
        "scope": "finite falsification of this fixed cubic mutation only",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
