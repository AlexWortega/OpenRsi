#!/usr/bin/env python3
"""Generation-9 exact audit of a two-parameter global PSD metric template.

The template is fixed before seeing satisfiability.  It has anchor scale 2 and
one shared residual scale s.  For every clause it emits normalization and
legality rows.  For every global monomial of degree one or two it emits all
pairwise differences between clause occurrences of that monomial.  Thus row
permutations induced by variable/clause permutations do not change the Gram
form.  At s=5 the lattice basis and target realize

    ||2z-1||^2 + 25 ||Az-b||^2.

The same rule is applied to the Generation-7 nine-clause obstruction and to a
fixed satisfiable nine-clause overlapping control.  Exact low-anchor-weight
search includes signed coefficients and finds the degree-two cube-parity
attack.  These are finite-instance facts, not an asymptotic theorem.
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

PATTERNS = tuple(product((0, 1), repeat=3))
MONOMIALS = tuple((i,) for i in range(4)) + tuple(combinations(range(4), 2))
UNSAT_EDGES = (
    ("0000", "1000"),
    ("1000", "1100"),
    ("0100", "0110"),
    ("0110", "0111"),
    ("0001", "0011"),
    ("0010", "1010"),
    ("0101", "1101"),
    ("1001", "1011"),
    ("1110", "1111"),
)
# Replace the final forbidden edge by a duplicate of clause 3.  This retains
# nine overlapping clauses and is satisfied by 1110 and 1111.
CONTROL_EDGES = UNSAT_EDGES[:-1] + (("0110", "0111"),)
ANCHOR_SCALE = 2
RESIDUAL_SCALE = 5
PARAMETER_COUNT = 2
N_CLAUSES = len(UNSAT_EDGES)
N_SELECTORS = 8 * N_CLAUSES
BASELINE_RADIUS2 = N_SELECTORS
ZERO_KERNEL_EXTRA = 24
UNSAT_MINIMUM2 = BASELINE_RADIUS2 + ZERO_KERNEL_EXTRA
MANIFEST_PATH = Path(__file__).with_name("gen9_global_psd_metric_manifest.json")


def bits(text):
    return tuple(int(value) for value in text)


def clause_data(edges):
    clauses = []
    for left_text, right_text in edges:
        left, right = bits(left_text), bits(right_text)
        differing = [i for i in range(4) if left[i] != right[i]]
        assert len(differing) == 1
        omitted = differing[0]
        variables = tuple(i for i in range(4) if i != omitted)
        false_bits = tuple(left[i] for i in variables)
        clauses.append({
            "edge": (left_text, right_text),
            "omitted_variable": omitted,
            "variables": variables,
            "false_bits": false_bits,
        })
    return tuple(clauses)


def selector_index(clause_index, pattern_index):
    return 8 * clause_index + pattern_index


def global_pattern(clause, pattern):
    return tuple(
        pattern[position] ^ clause["false_bits"][position]
        for position in range(3)
    )


def monomial_value(clause, pattern, monomial):
    values = global_pattern(clause, pattern)
    positions = tuple(clause["variables"].index(variable) for variable in monomial)
    return int(all(values[position] for position in positions))


def sparse(vector):
    return [[index, int(value)] for index, value in enumerate(vector) if value]


def build_checks(clauses):
    checks = []
    for clause_index in range(len(clauses)):
        row = [0] * N_SELECTORS
        for pattern_index in range(8):
            row[selector_index(clause_index, pattern_index)] = 1
        checks.append({
            "kind": "normalization",
            "clause": clause_index,
            "coefficients": tuple(row),
            "rhs": 1,
        })

        row = [0] * N_SELECTORS
        row[selector_index(clause_index, 0)] = 1
        checks.append({
            "kind": "legality",
            "clause": clause_index,
            "coefficients": tuple(row),
            "rhs": 0,
        })

    # All occurrence pairs, rather than a distinguished reference occurrence,
    # make A^T A invariant under permutations preserving the incidence data.
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
                    row[selector_index(clause_index, pattern_index)] += (
                        sign * monomial_value(clause, pattern, monomial)
                    )
            checks.append({
                "kind": "moment_consistency",
                "monomial": monomial,
                "clauses": (left_clause, right_clause),
                "coefficients": tuple(row),
                "rhs": 0,
            })
    return tuple(checks)


def factor_and_target(checks, residual_scale=RESIDUAL_SCALE):
    rows = []
    target = []
    for selector in range(N_SELECTORS):
        row = [0] * N_SELECTORS
        row[selector] = ANCHOR_SCALE
        rows.append(tuple(row))
        target.append(1)
    for check in checks:
        rows.append(tuple(residual_scale * value for value in check["coefficients"]))
        target.append(residual_scale * check["rhs"])
    return tuple(rows), tuple(target)


def gram_linear_center(factor, target):
    B = Matrix(factor)
    t = Matrix(target)
    gram = B.T * B
    linear = B.T * t
    center = gram.inv() * linear
    kappa = (t.T * t)[0] - (linear.T * center)[0]
    return gram, linear, center, kappa


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
    clauses = clause_data(edges)
    checks = build_checks(clauses)
    factor, target = factor_and_target(checks)
    gram, linear, center, kappa = gram_linear_center(factor, target)
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
        "schema": "gen9-global-psd-metric-v1",
        "finite_claim_only": True,
        "template": {
            "description": "anchors plus all-pairs global degree-at-most-two moment consistency",
            "shared_parameter_count": PARAMETER_COUNT,
            "shared_parameters": {
                "anchor_scale": ANCHOR_SCALE,
                "residual_scale": RESIDUAL_SCALE,
            },
            "parameter_selection": (
                "smallest positive integer residual scale s with s^2 greater "
                "than the exactly searched zero-kernel anchor excess 24"
            ),
            "equivariance": (
                "variable/clause incidence permutations only permute factor rows and columns"
            ),
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
    clauses = clause_data(tuple(tuple(edge) for edge in record["edges"]))
    checks = build_checks(clauses)
    factor, target = factor_and_target(checks)
    dimension = record["ambient_dimension"]

    emitted_factor = []
    for terms in record["factor_rows"]:
        row = [0] * N_SELECTORS
        for column, value in terms:
            assert row[column] == 0
            row[column] = value
        emitted_factor.append(tuple(row))
    emitted_target = [0] * dimension
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


def squared_distance(checks, selector, residual_scale=RESIDUAL_SCALE):
    anchor = sum((ANCHOR_SCALE * value - 1) ** 2 for value in selector)
    raw = residual(checks, selector)
    return anchor + residual_scale * residual_scale * sum(value * value for value in raw)


def honest_selector(clauses, assignment):
    selector = [0] * N_SELECTORS
    falsified = []
    for clause_index, clause in enumerate(clauses):
        pattern = tuple(
            assignment[variable] ^ clause["false_bits"][position]
            for position, variable in enumerate(clause["variables"])
        )
        pattern_index = PATTERNS.index(pattern)
        selector[selector_index(clause_index, pattern_index)] = 1
        if pattern_index == 0:
            falsified.append(clause_index)
    return tuple(selector), tuple(falsified)


def local_states_through_extra_24():
    # If total anchor energy is at most 72+24, every coordinate has excess
    # 4z(z-1) <= 24, hence z is in {-2,-1,0,1,2,3}.  This is a derived range.
    states = []
    for legal_values in product(range(-2, 4), repeat=7):
        block = (0,) + legal_values
        if sum(block) != 1:
            continue
        extra = sum(4 * value * (value - 1) for value in block)
        if extra > ZERO_KERNEL_EXTRA:
            continue
        local_moments = {}
        for monomial in ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2)):
            local_moments[monomial] = sum(
                block[pattern_index]
                * int(all(PATTERNS[pattern_index][position] for position in monomial))
                for pattern_index in range(8)
            )
        states.append((extra, block, local_moments))
    assert Counter(extra for extra, _, _ in states) == {0: 7, 8: 105, 16: 252, 24: 595}
    return tuple(states)


def global_state_record(clause, state):
    extra, block, _ = state
    moments = {}
    for monomial in MONOMIALS:
        if all(variable in clause["variables"] for variable in monomial):
            moments[monomial] = sum(
                block[pattern_index] * monomial_value(clause, pattern, monomial)
                for pattern_index, pattern in enumerate(PATTERNS)
            )
    return extra, block, moments


def exact_zero_residual_search(clauses):
    """Dynamic program over every signed state in the derived anchor shell."""
    states = local_states_through_extra_24()
    tables = [tuple(global_state_record(clause, state) for state in states)
              for clause in clauses]

    # A key records the globally shared degree-one/two moments, with None for
    # monomials not encountered yet.  Keeping the cheapest path per key is
    # exact because later checks depend only on this key.
    dp = {(None,) * len(MONOMIALS): (0, ())}
    layer_counts = []
    for table in tables:
        next_dp = {}
        for key, (cost, witness) in dp.items():
            for extra, block, moments in table:
                next_cost = cost + extra
                if next_cost > ZERO_KERNEL_EXTRA:
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
    selector = tuple(value for block in blocks for value in block)
    return {
        "local_states_checked_per_clause": len(states),
        "local_state_extra_histogram": dict(sorted(Counter(
            extra for extra, _, _ in states
        ).items())),
        "dynamic_program_layer_counts": layer_counts,
        "minimum_anchor_extra": minimum,
        "global_moments": list(key),
        "selector": list(selector),
    }


def parse_rational(text):
    return Fraction(text)


def verify_center_and_coefficient_bound(record, factor, target):
    gram, linear, center, kappa = gram_linear_center(factor, target)
    assert matrix_upper_sparse(gram) == record["gram_upper_triangle"]
    assert [int(value) for value in linear] == record["linear_term"]
    assert [rational_text(value) for value in center] == record["center"]
    assert rational_text(kappa) == record["orthogonal_target_energy"]

    # Exact coercivity: Q = 4I + 25 A^T A, so lambda_min(Q) >= 4.
    assert all(gram[index, index] >= 4 for index in range(N_SELECTORS))
    for row in range(N_SELECTORS):
        assert gram[row, row] - 4 == sum(
            factor_row[row] * factor_row[row]
            for factor_row in factor[N_SELECTORS:]
        )
    assert record["certified_gram_eigenvalue_lower_bound"] == 4

    # The centered identity and lambda bound give an explicit unrestricted
    # coefficient bound for every point through the tested radius 96.
    centered_budget = Fraction(UNSAT_MINIMUM2) - parse_rational(
        record["orthogonal_target_energy"]
    )
    assert centered_budget >= 0
    norm_bound2 = centered_budget / 4
    max_center = max(abs(parse_rational(value)) for value in record["center"])
    coefficient_bound = 0
    while (Fraction(coefficient_bound) - max_center) ** 2 <= norm_bound2:
        coefficient_bound += 1
    # |z_i| >= coefficient_bound contradicts the centered norm bound.
    assert coefficient_bound == 4
    return {
        "lambda_min_lower_bound": 4,
        "centered_norm_bound_squared": str(norm_bound2),
        "strict_absolute_coefficient_bound": coefficient_bound,
        "integer_coefficient_interval": [-(coefficient_bound - 1), coefficient_bound - 1],
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
    assert manifest["template"]["shared_parameter_count"] == 2 < 30
    assert RESIDUAL_SCALE == min(
        scale for scale in range(1, 100) if scale * scale > ZERO_KERNEL_EXTRA
    )

    reconstructed = []
    for record in manifest["instances"]:
        clauses, checks, factor, target = reconstruct_instance(record)
        assert factor_hash(factor, target) == record["factor_target_sha256"]
        assert len(factor) == record["ambient_dimension"]
        assert len(factor[0]) == record["lattice_rank"] == N_SELECTORS
        # The first 72 rows are 2I, so this rational Euclidean Gram factor has
        # full column rank without an external coefficient restriction.
        assert all(
            factor[row][column] == (2 if row == column else 0)
            for row in range(N_SELECTORS) for column in range(N_SELECTORS)
        )
        reconstructed.append((record, clauses, checks, factor, target))

    unsat_record, unsat_clauses, unsat_checks, unsat_factor, unsat_target = reconstructed[0]
    control_record, control_clauses, control_checks, control_factor, control_target = reconstructed[1]

    # Exhaustive finite truth-table checks: the obstruction covers all 16
    # assignments, while the fixed control has an honest overlapping witness.
    coverage = {}
    for assignment in product((0, 1), repeat=4):
        _, falsified = honest_selector(unsat_clauses, assignment)
        assert falsified
        coverage["".join(map(str, assignment))] = list(falsified)
    assert len(coverage) == 16

    control_assignment = (1, 1, 1, 0)
    control_selector, control_falsified = honest_selector(control_clauses, control_assignment)
    assert not control_falsified
    assert not any(residual(control_checks, control_selector))
    assert squared_distance(control_checks, control_selector) == BASELINE_RADIUS2
    # Every integer anchor contributes at least one, so 72 is also the exact
    # unrestricted CVP minimum for the control.
    assert all((2 * value - 1) ** 2 >= 1 for value in range(-20, 21))
    control_exact_minimum2 = BASELINE_RADIUS2

    # Attack the old signed selector explicitly.  It still preserves mass and
    # singleton marginals, but the new pair moments make its actual fixed-
    # target residual nonzero.
    old_attack, falsified = honest_selector(unsat_clauses, (0, 0, 0, 0))
    assert falsified == (0,)
    old_attack = list(old_attack)
    old_attack[selector_index(0, 0)] = 0
    old_attack[selector_index(0, PATTERNS.index((0, 1, 1)))] = 1
    old_attack[selector_index(0, PATTERNS.index((1, 0, 0)))] = 1
    old_attack[selector_index(0, PATTERNS.index((1, 1, 1)))] = -1
    old_attack = tuple(old_attack)
    old_residual = residual(unsat_checks, old_attack)
    assert any(old_residual)
    old_attack_distance2 = squared_distance(unsat_checks, old_attack)

    search = exact_zero_residual_search(unsat_clauses)
    assert search["minimum_anchor_extra"] == ZERO_KERNEL_EXTRA
    cube_selector = tuple(search["selector"])
    assert not any(residual(unsat_checks, cube_selector))
    assert squared_distance(unsat_checks, cube_selector) == UNSAT_MINIMUM2

    # Exact unrestricted minimum: anchors always cost at least 72.  A nonzero
    # integral residual costs at least 25, hence at least 97 total.  The exact
    # signed search proves that a zero residual costs at least 72+24, and its
    # displayed cube-parity selector attains 96.
    assert BASELINE_RADIUS2 + RESIDUAL_SCALE ** 2 > UNSAT_MINIMUM2
    unsat_exact_minimum2 = UNSAT_MINIMUM2

    coefficient_bound = verify_center_and_coefficient_bound(
        unsat_record, unsat_factor, unsat_target
    )
    verify_center_and_coefficient_bound(control_record, control_factor, control_target)

    # Exact pass test: sqrt(96/72) > 11/10, checked without floating point.
    assert 100 * unsat_exact_minimum2 > 121 * control_exact_minimum2

    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[1])),
        "template_shared_parameters": PARAMETER_COUNT,
        "rational_anchor_scale": ANCHOR_SCALE,
        "rational_residual_scale": RESIDUAL_SCALE,
        "unsat_factor_target_sha256": unsat_record["factor_target_sha256"],
        "control_factor_target_sha256": control_record["factor_target_sha256"],
        "unsat_check_count": len(unsat_checks),
        "control_check_count": len(control_checks),
        "covered_unsat_assignments": len(coverage),
        "control_assignment": list(control_assignment),
        "control_exact_unrestricted_minimum_squared": control_exact_minimum2,
        "old_three_term_attack_residual_squared": sum(value * value for value in old_residual),
        "old_three_term_attack_distance_squared": old_attack_distance2,
        "exact_low_weight_search": search,
        "unsat_exact_unrestricted_minimum_squared": unsat_exact_minimum2,
        "squared_distance_ratio": "4/3",
        "distance_ratio_exceeds": "11/10",
        "coefficient_bound_from_gram": coefficient_bound,
        "finding": (
            "the two-parameter degree-two global PSD template passes the finite 1.1 test; "
            "its exact nearest unsatisfiable vector is the seven-term cube-parity attack"
        ),
        "scope": (
            "finite only: no uniform synthesis theorem, composition theorem, or polynomial gap"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
