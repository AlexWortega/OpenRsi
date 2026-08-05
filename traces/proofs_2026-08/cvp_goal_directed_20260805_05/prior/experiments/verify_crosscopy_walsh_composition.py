#!/usr/bin/env python3
"""Generation-32 exact composition audit of the Generation-31 Walsh Gram.

Two nine-clause copies share variables 0,1; the second copy renames original
variables 2,3 to 4,5.  All degree-at-most-three moment equalities are emitted
across all 18 clauses, including cross-copy rows.  The objective remains

    ||2z-1||^2 + ||Fz||^2 + 100||Az-b||^2,

with 18 H_8 Walsh blocks and unrestricted integral coefficients.

An exact one-copy shell DP proves d1^2=216.  A matched two-copy control has
exact minimum 288.  Two compatible G11/G13 parity witnesses satisfy every
cross-copy row and have cost 432=2*d1^2, falsifying strict superadditivity.
This is a finite kill of this coupling rule, not an asymptotic theorem.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, product
import hashlib
import json
from pathlib import Path

import verify_equal_radius_walsh_gram as gen31
import verify_global_psd_metric as gen9

COPY_SIZE = 9
N_CLAUSES = 18
N_SELECTORS = 144
VARIABLES = tuple(range(6))
MONOMIALS = tuple(
    monomial
    for degree in range(1, 4)
    for monomial in combinations(VARIABLES, degree)
)
FIRST_MAP = {0: 0, 1: 1, 2: 2, 3: 3}
SECOND_MAP = {0: 0, 1: 1, 2: 4, 3: 5}
ONE_COPY_RADIUS2 = 216
TWO_COPY_CONTROL_RADIUS2 = 288
SUPERADDITIVITY_THRESHOLD2 = 432
MANIFEST_PATH = Path(__file__).with_name("gen32_crosscopy_walsh_composition_manifest.json")


def sparse(row):
    return [[index, int(value)] for index, value in enumerate(row) if value]


def mapped_clauses(edges, variable_map, copy_index):
    clauses = []
    for local_index, clause in enumerate(gen9.clause_data(edges)):
        clauses.append({
            "index": copy_index * COPY_SIZE + local_index,
            "copy": copy_index,
            "source_clause": local_index,
            "variables": tuple(variable_map[value] for value in clause["variables"]),
            "false_bits": clause["false_bits"],
            "edge": clause["edge"],
        })
    return tuple(clauses)


def build_union_clauses(edges):
    return mapped_clauses(edges, FIRST_MAP, 0) + mapped_clauses(edges, SECOND_MAP, 1)


def selector_index(clause, pattern):
    return 8 * clause + pattern


def monomial_value(clause, pattern, monomial):
    global_values = {
        variable: pattern[position] ^ clause["false_bits"][position]
        for position, variable in enumerate(clause["variables"])
    }
    return int(all(global_values[variable] for variable in monomial))


def build_checks(clauses):
    checks = []
    for clause_index, clause in enumerate(clauses):
        row = [0] * N_SELECTORS
        for pattern in range(8):
            row[selector_index(clause_index, pattern)] = 1
        checks.append({
            "kind": "normalization", "degree": 0, "clause": clause_index,
            "coefficients": tuple(row), "rhs": 1,
        })
        row = [0] * N_SELECTORS
        row[selector_index(clause_index, 0)] = 1
        checks.append({
            "kind": "legality", "degree": 0, "clause": clause_index,
            "coefficients": tuple(row), "rhs": 0,
        })

    for monomial in MONOMIALS:
        occurrences = [
            clause_index for clause_index, clause in enumerate(clauses)
            if all(variable in clause["variables"] for variable in monomial)
        ]
        for left, right in combinations(occurrences, 2):
            row = [0] * N_SELECTORS
            for sign, clause_index in ((1, left), (-1, right)):
                clause = clauses[clause_index]
                for pattern_index, pattern in enumerate(gen9.PATTERNS):
                    row[selector_index(clause_index, pattern_index)] += (
                        sign * monomial_value(clause, pattern, monomial)
                    )
            checks.append({
                "kind": "moment_consistency", "degree": len(monomial),
                "monomial": monomial, "clauses": (left, right),
                "cross_copy": clauses[left]["copy"] != clauses[right]["copy"],
                "coefficients": tuple(row), "rhs": 0,
            })
    assert Counter(check["kind"] for check in checks) == {
        "normalization": 18,
        "legality": 18,
        "moment_consistency": 397,
    }
    return tuple(checks)


def build_walsh_rows():
    rows = []
    for clause in range(N_CLAUSES):
        for walsh_row in range(8):
            row = [0] * N_SELECTORS
            for pattern in range(8):
                row[8 * clause + pattern] = gen31.walsh_entry(walsh_row, pattern)
            rows.append(tuple(row))
    return tuple(rows)


def factor_and_target(checks):
    rows = []
    target = []
    for index in range(N_SELECTORS):
        row = [0] * N_SELECTORS
        row[index] = 2
        rows.append(tuple(row))
        target.append(1)
    rows.extend(build_walsh_rows())
    target.extend([0] * N_SELECTORS)
    for check in checks:
        rows.append(tuple(10 * value for value in check["coefficients"]))
        target.append(10 * check["rhs"])
    return tuple(rows), tuple(target)


def factor_hash(factor, target):
    payload = {
        "factor_rows": [sparse(row) for row in factor],
        "target": sparse(target),
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def base_energy(selector):
    return sum(gen31.coordinate_energy(value) for value in selector)


def residual(checks, selector):
    return tuple(
        sum(value * coefficient for value, coefficient in zip(check["coefficients"], selector))
        - check["rhs"]
        for check in checks
    )


def objective_breakdown(checks, selector):
    raw = residual(checks, selector)
    return {
        "base_discrepancy": base_energy(selector),
        "raw_residual_squared": sum(value * value for value in raw),
        "total": base_energy(selector) + 100 * sum(value * value for value in raw),
    }


def honest_selector(clauses, assignment):
    selector = [0] * (8 * len(clauses))
    falsified = []
    for clause_index, clause in enumerate(clauses):
        pattern = tuple(
            assignment[variable] ^ clause["false_bits"][position]
            for position, variable in enumerate(clause["variables"])
        )
        pattern_index = gen9.PATTERNS.index(pattern)
        selector[8 * clause_index + pattern_index] = 1
        if pattern_index == 0:
            falsified.append(clause_index)
    return tuple(selector), tuple(falsified)


def one_copy_local_states():
    states = []
    for legal_values in product(range(-2, 3), repeat=7):
        block = (0,) + legal_values
        if sum(block) != 1:
            continue
        cost = sum(gen31.coordinate_energy(value) for value in block)
        if cost <= 88:
            states.append((cost, block))
    states.sort()
    assert Counter(cost for cost, _ in states) == {16: 7, 40: 105, 64: 252, 88: 595}
    return tuple(states)


def exact_one_copy_search():
    """Exact unrestricted one-copy search through 216."""
    clauses = gen9.clause_data(gen9.UNSAT_EDGES)
    monomials = gen31.MONOMIALS
    states = one_copy_local_states()
    dp = {((0, 0),) * len(monomials): (0, ())}
    layer_counts = []
    for clause_index, clause in enumerate(clauses):
        available = [
            index for index, monomial in enumerate(monomials)
            if all(variable in clause["variables"] for variable in monomial)
        ]
        previous_counts = {
            index: sum(
                all(variable in clauses[prior]["variables"] for variable in monomials[index])
                for prior in range(clause_index)
            )
            for index in available
        }
        next_dp = {}
        remaining = 8 - clause_index
        for key, (cost, witness) in dp.items():
            for block_cost, block in states:
                new_cost = cost + block_cost
                if new_cost + 16 * remaining > ONE_COPY_RADIUS2:
                    continue
                new_key = list(key)
                for index in available:
                    monomial = monomials[index]
                    value = sum(
                        block[pattern_index] * gen9.monomial_value(clause, pattern, monomial)
                        for pattern_index, pattern in enumerate(gen9.PATTERNS)
                    )
                    old_sum, old_sumsq = new_key[index]
                    count = previous_counts[index]
                    pair_residual = count * value * value - 2 * value * old_sum + old_sumsq
                    new_cost += 100 * pair_residual
                    if new_cost + 16 * remaining > ONE_COPY_RADIUS2:
                        break
                    new_key[index] = (old_sum + value, old_sumsq + value * value)
                else:
                    new_key = tuple(new_key)
                    old = next_dp.get(new_key)
                    if old is None or new_cost < old[0]:
                        next_dp[new_key] = (new_cost, witness + (block,))
        dp = next_dp
        layer_counts.append(len(dp))
    assert dp
    minimum = min(record[0] for record in dp.values())
    key, (cost, blocks) = next(
        (key, record) for key, record in dp.items() if record[0] == minimum
    )
    selector = tuple(value for block in blocks for value in block)
    assert minimum == ONE_COPY_RADIUS2
    return {
        "malformed_local_global_lower_bound": 108 + 8 * 16,
        "local_state_count": len(states),
        "local_cost_histogram": {str(key): value for key, value in sorted(Counter(
            cost for cost, _ in states
        ).items())},
        "dynamic_program_layer_counts": layer_counts,
        "exact_minimum_squared": minimum,
        "moment_sum_sumsq_key": [[left, right] for left, right in key],
        "selector": list(selector),
    }


def mapped_parity_witness(clauses):
    assignment = {0: 1, 1: 1, 2: 0, 3: 0, 4: 0, 5: 0}
    selector, falsified = honest_selector(clauses, assignment)
    assert falsified == (1, 10)
    selector = list(selector)
    parity = gen31.gen11.seven_term_attack(
        gen9.clause_data(gen9.UNSAT_EDGES), (1, 1, 0, 0), 1
    )[8:16]
    assert tuple(parity) == gen31.gen11.seven_term_attack(
        gen9.clause_data(gen9.UNSAT_EDGES), (1, 1, 0, 0), 1
    )[8:16]
    selector[8:16] = parity
    selector[8 * 10:8 * 11] = parity
    return tuple(selector)


def control_certificate(control_clauses, control_checks):
    assignment = {0: 1, 1: 1, 2: 1, 3: 0, 4: 1, 5: 0}
    selector, falsified = honest_selector(control_clauses, assignment)
    assert not falsified
    breakdown = objective_breakdown(control_checks, selector)
    assert breakdown == {
        "base_discrepancy": TWO_COPY_CONTROL_RADIUS2,
        "raw_residual_squared": 0,
        "total": TWO_COPY_CONTROL_RADIUS2,
    }
    # Exhaustive branch accounting below 288:
    # base >=144, so residual square is 0 or 1.  At residual zero all 18
    # normalized/legal blocks cost >=16, giving base >=288.  If residual square
    # one is a moment row, the same bound applies.  If it is a local row, the
    # other 17 blocks are normalized/legal (>=272) and the malformed block has
    # base >=8, so total is at least 272+8+100=380.
    return {
        "witness_assignment": assignment,
        "witness_breakdown": breakdown,
        "below_288_residual_branches": {
            "residual_squared_0_lower_bound": 288,
            "residual_squared_1_moment_lower_bound": 388,
            "residual_squared_1_local_lower_bound": 380,
            "residual_squared_at_least_2_lower_bound": 344,
        },
        "exact_minimum_squared": TWO_COPY_CONTROL_RADIUS2,
    }


def instance_manifest(name, edges):
    clauses = build_union_clauses(edges)
    checks = build_checks(clauses)
    factor, target = factor_and_target(checks)
    return {
        "name": name,
        "copy_variable_maps": [
            [FIRST_MAP[index] for index in range(4)],
            [SECOND_MAP[index] for index in range(4)],
        ],
        "clauses": [{
            key: (list(value) if isinstance(value, tuple) else value)
            for key, value in clause.items()
        } for clause in clauses],
        "check_count": len(checks),
        "check_count_by_kind": dict(sorted(Counter(check["kind"] for check in checks).items())),
        "cross_copy_moment_row_count": sum(
            check.get("cross_copy", False) for check in checks
        ),
        "checks": [{
            key: (list(value) if isinstance(value, tuple) else value)
            for key, value in check.items() if key != "coefficients"
        } | {"terms": sparse(check["coefficients"])} for check in checks],
        "lattice_rank": N_SELECTORS,
        "ambient_dimension": len(factor),
        "factor_rows": [sparse(row) for row in factor],
        "target": sparse(target),
        "factor_target_sha256": factor_hash(factor, target),
        "gram_rule": "Q=12I+100 A^T A",
        "certified_gram_eigenvalue_lower_bound": 12,
    }


def one_copy_source_record():
    clauses = gen9.clause_data(gen9.UNSAT_EDGES)
    checks = gen31.gen11.build_checks(clauses)
    factor, target = gen31.factor_and_target(checks)
    return {
        "source_manifest": "experiments/gen31_equal_radius_walsh_gram_manifest.json",
        "lattice_rank": 72,
        "ambient_dimension": len(factor),
        "factor_target_sha256": gen31.gen11.factor_hash(factor, target),
        "factor_rule": "||2z-1||^2+||Fz||^2+100||Az-b||^2",
    }


def build_manifest():
    return {
        "schema": "gen32-crosscopy-walsh-composition-v1",
        "finite_claim_only": True,
        "selected_proposal": "Pro proposal 1: cross-copy moment coupling of G31",
        "mechanism": "cross-copy degree-at-most-three moments might force strict superadditivity",
        "expected_move": "d2^2>2*d1^2 while the two-copy control remains 288",
        "falsification_condition": "control mismatch or any unrestricted two-copy vector of cost at most 2*d1^2",
        "coefficient_domain": "all integers",
        "external_filters": [],
        "one_copy_exact_search_radius_squared": ONE_COPY_RADIUS2,
        "two_copy_superadditivity_threshold_squared": SUPERADDITIVITY_THRESHOLD2,
        "two_copy_coefficient_bound": {
            "derivation": "base<=432 and the other 143 coordinates cost at least one, so 12z_i^2-4z_i+1<=289",
            "inclusive_interval": [-4, 5],
        },
        "one_copy_instance": one_copy_source_record(),
        "one_copy_search": exact_one_copy_search(),
        "instances": [
            instance_manifest("two_copy_obstruction", gen9.UNSAT_EDGES),
            instance_manifest("two_copy_matched_control", gen9.CONTROL_EDGES),
        ],
    }


def reconstruct_instance(record, edges):
    clauses = build_union_clauses(edges)
    checks = build_checks(clauses)
    factor, target = factor_and_target(checks)
    assert factor_hash(factor, target) == record["factor_target_sha256"]
    assert [sparse(row) for row in factor] == record["factor_rows"]
    assert sparse(target) == record["target"]
    return clauses, checks, factor, target


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args()

    gen31.verify_walsh_identity()
    expected = build_manifest()
    if args.write_manifest:
        MANIFEST_PATH.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
        print(MANIFEST_PATH)
        return

    manifest = json.loads(MANIFEST_PATH.read_text())
    assert manifest == expected
    unsat_clauses, unsat_checks, unsat_factor, _ = reconstruct_instance(
        manifest["instances"][0], gen9.UNSAT_EDGES
    )
    control_clauses, control_checks, _, _ = reconstruct_instance(
        manifest["instances"][1], gen9.CONTROL_EDGES
    )

    one_copy_source = json.loads(gen31.MANIFEST_PATH.read_text())["instances"][0]
    assert one_copy_source["factor_target_sha256"] == manifest["one_copy_instance"]["factor_target_sha256"]
    one_copy = manifest["one_copy_search"]
    assert one_copy["exact_minimum_squared"] == ONE_COPY_RADIUS2
    assert one_copy["dynamic_program_layer_counts"] == [959, 2396, 891, 192, 63, 26, 15, 7, 1]

    control = control_certificate(control_clauses, control_checks)
    assert control["exact_minimum_squared"] == TWO_COPY_CONTROL_RADIUS2

    parity = mapped_parity_witness(unsat_clauses)
    parity_breakdown = objective_breakdown(unsat_checks, parity)
    assert parity_breakdown == {
        "base_discrepancy": SUPERADDITIVITY_THRESHOLD2,
        "raw_residual_squared": 0,
        "total": SUPERADDITIVITY_THRESHOLD2,
    }
    parity_block = (0, 1, 1, -1, 1, -1, -1, 1)
    changed_clauses = [
        clause for clause in range(N_CLAUSES)
        if tuple(parity[8 * clause:8 * clause + 8]) == parity_block
    ]
    assert changed_clauses == [1, 10]

    # The explicit unrestricted witness reaches 2*d1^2, so the required empty
    # shell is false and no further branch enumeration can rescue strict growth.
    assert parity_breakdown["total"] == 2 * one_copy["exact_minimum_squared"]

    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[1])),
        "lattice_rank": N_SELECTORS,
        "ambient_dimension": len(unsat_factor),
        "cross_copy_moment_row_count": manifest["instances"][0]["cross_copy_moment_row_count"],
        "one_copy_exact_minimum_squared": one_copy["exact_minimum_squared"],
        "one_copy_search": one_copy,
        "two_copy_control_certificate": control,
        "two_copy_control_exact_minimum_squared": control["exact_minimum_squared"],
        "two_copy_coefficient_interval_through_threshold": [-4, 5],
        "two_copy_parity_changed_clauses": changed_clauses,
        "two_copy_parity_breakdown": parity_breakdown,
        "strict_superadditivity": False,
        "finding": "compatible parity witnesses attain d2^2<=432=2*d1^2 despite all cross-copy moment rows",
        "scope": "finite kill of this cross-copy coupling rule; no asymptotic claim",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
