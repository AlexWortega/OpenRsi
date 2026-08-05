#!/usr/bin/env python3
"""Generation-14 exact bounded audit of the complete pair-bag lift.

For every pair of the nine clauses, one integral selector is introduced for
each assignment to the union of the pair's variables.  The emitted rows are:

* one normalization per bag,
* one forbidden-label marginal per endpoint of each bag, and
* canonical-star equalities for all eight full label marginals of each clause.

The fixed-target objective is ||2z-1||^2 + 25||Az-b||^2.  The complete mesh is
stronger than any sparse expander choice.  The verifier proves there is no
obstruction vector through baseline B plus 32, while the control minimum is B.
This is finite evidence only; no fixed-level asymptotic gap is claimed.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, product
import hashlib
import json
from pathlib import Path

import verify_global_psd_metric as gen9
import verify_degree3_global_psd_metric as gen11

PATTERNS = gen9.PATTERNS
UNSAT_EDGES = gen9.UNSAT_EDGES
CONTROL_EDGES = gen9.CONTROL_EDGES
N_CLAUSES = 9
RESIDUAL_SCALE = 5
SHELL_EXCESS = 32
MANIFEST_PATH = Path(__file__).with_name("gen14_pair_bag_lift_manifest.json")


def bits(text):
    return tuple(int(value) for value in text)


def sparse(vector):
    return [[index, int(value)] for index, value in enumerate(vector) if value]


def build_bags(clauses):
    bags = []
    offset = 0
    for left, right in combinations(range(N_CLAUSES), 2):
        variables = tuple(sorted(set(clauses[left]["variables"]) | set(clauses[right]["variables"])))
        assignments = tuple(product((0, 1), repeat=len(variables)))
        bags.append({
            "index": len(bags),
            "clauses": (left, right),
            "variables": variables,
            "assignments": assignments,
            "offset": offset,
            "size": len(assignments),
        })
        offset += len(assignments)
    assert len(bags) == 36
    assert Counter(bag["size"] for bag in bags) == {8: 7, 16: 29}
    assert offset == 520
    return tuple(bags), offset


def bag_local_pattern(clause, bag, assignment):
    values = {variable: assignment[position] for position, variable in enumerate(bag["variables"])}
    return tuple(
        values[variable] ^ clause["false_bits"][position]
        for position, variable in enumerate(clause["variables"])
    )


def build_checks(clauses, bags, dimension):
    checks = []
    for bag in bags:
        row = [0] * dimension
        for local_index in range(bag["size"]):
            row[bag["offset"] + local_index] = 1
        checks.append({
            "kind": "bag_normalization",
            "bag": bag["index"],
            "coefficients": tuple(row),
            "rhs": 1,
        })
        for clause_index in bag["clauses"]:
            row = [0] * dimension
            clause = clauses[clause_index]
            for local_index, assignment in enumerate(bag["assignments"]):
                if bag_local_pattern(clause, bag, assignment) == (0, 0, 0):
                    row[bag["offset"] + local_index] = 1
            checks.append({
                "kind": "forbidden_label_marginal",
                "bag": bag["index"],
                "clause": clause_index,
                "coefficients": tuple(row),
                "rhs": 0,
            })

    incident = {
        clause: tuple(bag for bag in bags if clause in bag["clauses"])
        for clause in range(N_CLAUSES)
    }
    assert all(len(value) == 8 for value in incident.values())
    for clause_index in range(N_CLAUSES):
        canonical = incident[clause_index][0]
        clause = clauses[clause_index]
        for bag in incident[clause_index][1:]:
            for pattern_index, pattern in enumerate(PATTERNS):
                row = [0] * dimension
                for sign, selected_bag in ((1, bag), (-1, canonical)):
                    for local_index, assignment in enumerate(selected_bag["assignments"]):
                        if bag_local_pattern(clause, selected_bag, assignment) == pattern:
                            row[selected_bag["offset"] + local_index] += sign
                checks.append({
                    "kind": "clause_full_marginal_equality",
                    "clause": clause_index,
                    "label": pattern_index,
                    "bags": (bag["index"], canonical["index"]),
                    "coefficients": tuple(row),
                    "rhs": 0,
                })
    assert Counter(check["kind"] for check in checks) == {
        "bag_normalization": 36,
        "forbidden_label_marginal": 72,
        "clause_full_marginal_equality": 504,
    }
    return tuple(checks)


def factor_target_hash(checks, dimension):
    # Exact factor [2I;5A] and target [1;5b], represented canonically sparsely.
    payload = {
        "anchor_rows": [[index, 2] for index in range(dimension)],
        "anchor_target": [[index, 1] for index in range(dimension)],
        "residual_rows": [
            [[index, RESIDUAL_SCALE * value] for index, value in sparse(check["coefficients"])]
            for check in checks
        ],
        "residual_target": [RESIDUAL_SCALE * check["rhs"] for check in checks],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def instance_data(name, edges):
    clauses = gen9.clause_data(edges)
    bags, dimension = build_bags(clauses)
    checks = build_checks(clauses, bags, dimension)
    return clauses, bags, dimension, checks, {
        "name": name,
        "edges": [list(edge) for edge in edges],
        "selector_count_B": dimension,
        "bag_count": len(bags),
        "bags": [{
            "index": bag["index"],
            "clauses": list(bag["clauses"]),
            "variables": list(bag["variables"]),
            "offset": bag["offset"],
            "size": bag["size"],
            "assignments": [list(assignment) for assignment in bag["assignments"]],
        } for bag in bags],
        "check_count": len(checks),
        "checks": [{
            key: (list(value) if isinstance(value, tuple) else value)
            for key, value in check.items() if key != "coefficients"
        } | {"terms": sparse(check["coefficients"])} for check in checks],
        "lattice_rank": dimension,
        "ambient_dimension": dimension + len(checks),
        "factor_rule": "[2I;5A]",
        "target_rule": "[1;5b]",
        "factor_target_sha256": factor_target_hash(checks, dimension),
        "certified_gram_eigenvalue_lower_bound": 4,
    }


def build_manifest():
    unsat = instance_data("generation_7_obstruction", UNSAT_EDGES)[4]
    control = instance_data("satisfiable_overlapping_control", CONTROL_EDGES)[4]
    assert unsat["selector_count_B"] == control["selector_count_B"] == 520
    return {
        "schema": "gen14-complete-pair-bag-lift-v1",
        "finite_claim_only": True,
        "template": {
            "description": (
                "all intersecting clause pairs, all union assignments, bag normalization, "
                "endpoint legality, and complete canonical-star full-marginal equality"
            ),
            "coefficient_domain": "all integers",
            "objective": "||2z-1||^2+25||Az-b||^2",
            "external_filters": [],
        },
        "baseline_B": 520,
        "audited_shell_squared_radius": 552,
        "instances": [unsat, control],
    }


def reconstruct_instance(record):
    edges = tuple(tuple(edge) for edge in record["edges"])
    clauses = gen9.clause_data(edges)
    bags, dimension = build_bags(clauses)
    checks = build_checks(clauses, bags, dimension)
    assert dimension == record["selector_count_B"]
    assert len(checks) == record["check_count"]
    assert factor_target_hash(checks, dimension) == record["factor_target_sha256"]
    emitted_checks = [{
        key: (list(value) if isinstance(value, tuple) else value)
        for key, value in check.items() if key != "coefficients"
    } | {"terms": sparse(check["coefficients"])} for check in checks]
    assert emitted_checks == record["checks"]
    return clauses, bags, dimension, checks


def residual(checks, selector):
    return tuple(
        sum(value * coefficient for value, coefficient in zip(check["coefficients"], selector))
        - check["rhs"]
        for check in checks
    )


def objective_breakdown(checks, selector):
    anchor = sum((2 * value - 1) ** 2 for value in selector)
    raw = residual(checks, selector)
    return {
        "anchor": anchor,
        "anchor_extra": anchor - len(selector),
        "raw_residual_squared": sum(value * value for value in raw),
        "total": anchor + 25 * sum(value * value for value in raw),
    }


def honest_pair_selector(bags, assignment):
    selector = [0] * sum(bag["size"] for bag in bags)
    for bag in bags:
        local = tuple(assignment[variable] for variable in bag["variables"])
        local_index = bag["assignments"].index(local)
        selector[bag["offset"] + local_index] = 1
    return tuple(selector)


def satisfying_assignments(clauses):
    satisfying = []
    for assignment in product((0, 1), repeat=4):
        _, falsified = gen9.honest_selector(clauses, assignment)
        if not falsified:
            satisfying.append(assignment)
    return tuple(satisfying)


def compatible_legal_label_tuples(clauses):
    """Backtrack all legal clause labels that agree on every shared variable."""
    records = []

    def visit(clause_index, global_values, labels):
        if clause_index == N_CLAUSES:
            records.append((tuple(global_values.get(i) for i in range(4)), tuple(labels)))
            return
        clause = clauses[clause_index]
        for pattern_index in range(1, 8):
            pattern = PATTERNS[pattern_index]
            local_global = {
                variable: pattern[position] ^ clause["false_bits"][position]
                for position, variable in enumerate(clause["variables"])
            }
            if any(variable in global_values and global_values[variable] != value
                   for variable, value in local_global.items()):
                continue
            new_values = dict(global_values)
            new_values.update(local_global)
            visit(clause_index + 1, new_values, labels + [pattern_index])

    visit(0, {}, [])
    return tuple(records)


def verify_zero_residual_shell_structure(clauses, bags):
    # Anchor excess is 4*z*(z-1), hence a non-Boolean integral bag costs at
    # least 8.  Through excess 32 at most four of 36 bags are non-Boolean.
    max_nonboolean_bags = SHELL_EXCESS // 8
    assert max_nonboolean_bags == 4

    # Exhaust every possible exceptional-bag set of size at most four.  Each
    # clause has degree eight in the complete pair mesh, so it retains a
    # Boolean incident bag whose zero-residual normalization makes it one-hot.
    exceptional_sets = 0
    for size in range(max_nonboolean_bags + 1):
        for chosen in combinations(range(len(bags)), size):
            chosen = set(chosen)
            exceptional_sets += 1
            for clause in range(N_CLAUSES):
                assert any(
                    bag["index"] not in chosen
                    for bag in bags if clause in bag["clauses"]
                )
    assert exceptional_sets == sum(
        len(tuple(combinations(range(36), size))) for size in range(5)
    )

    # Full marginal equality propagates that one-hot label to every incident
    # bag.  Any joint table with one-hot endpoint marginals forces the labels
    # to agree on their shared variables (sum the table over each shared-value
    # fiber).  Thus zero residual would give a globally compatible legal label
    # tuple.  Enumerate those tuples exactly.
    compatible = compatible_legal_label_tuples(clauses)
    return {
        "max_nonboolean_bags_in_shell": max_nonboolean_bags,
        "exceptional_bag_sets_checked": exceptional_sets,
        "compatible_legal_label_tuple_count": len(compatible),
        "compatible_global_assignments": [list(record[0]) for record in compatible],
    }


def verify_one_residual_boolean_impossibility():
    # At total <=B+32, a nonzero integral residual costs 25 and leaves anchor
    # excess at most 7, so all coefficients are Boolean and residual^2=1.
    # Exactly one row would be nonzero.  Each possible row kind is impossible:
    # - a normalization error changes the sum of an endpoint full marginal,
    #   forcing a marginal-equality error;
    # - one forbidden one-hot marginal propagates to all eight incident bags;
    # - two different one-hot full marginals differ in two label coordinates.
    return {
        "residual_cost": 25,
        "remaining_anchor_excess": SHELL_EXCESS - 25,
        "coefficients_forced_boolean": True,
        "single_nonzero_row_cases_excluded": [
            "bag_normalization_forces_marginal_equality_error",
            "forbidden_label_propagates_to_eight_bags",
            "distinct_one_hot_marginals_differ_in_two_rows",
        ],
    }


def lift_affine_collision(clauses, bags, checks):
    coefficients = (1, -1, -1, 1, 0, 0, 0, 0,
                    -1, 1, 1, -1, 1, 0, 0, 0)
    assignments = tuple(product((0, 1), repeat=4))
    honest = tuple(honest_pair_selector(bags, assignment) for assignment in assignments)
    selector = tuple(
        sum(coefficients[index] * honest[index][coordinate] for index in range(16))
        for coordinate in range(len(honest[0]))
    )
    assert sum(coefficients) == 1
    assert not any(residual(checks, selector))
    breakdown = objective_breakdown(checks, selector)
    assert breakdown["anchor_extra"] == 928
    return selector, breakdown


def g7_extension_audit(clauses, bags):
    raw = [0] * 8
    raw[PATTERNS.index((0, 1, 1))] = 1
    raw[PATTERNS.index((1, 0, 0))] = 1
    raw[PATTERNS.index((1, 1, 1))] = -1
    assignment = (0, 0, 0, 0)
    failures = []
    for bag in bags:
        if 0 not in bag["clauses"]:
            continue
        other = bag["clauses"][0] if bag["clauses"][1] == 0 else bag["clauses"][1]
        overlap = tuple(sorted(set(clauses[0]["variables"]) & set(clauses[other]["variables"])))
        attack_overlap = {}
        for values in product((0, 1), repeat=len(overlap)):
            total = 0
            for pattern_index, coefficient in enumerate(raw):
                pattern = PATTERNS[pattern_index]
                global_bits = {
                    variable: pattern[position] ^ clauses[0]["false_bits"][position]
                    for position, variable in enumerate(clauses[0]["variables"])
                }
                if tuple(global_bits[v] for v in overlap) == values:
                    total += coefficient
            attack_overlap[values] = total
        honest_overlap = {
            values: int(values == tuple(assignment[v] for v in overlap))
            for values in product((0, 1), repeat=len(overlap))
        }
        if attack_overlap != honest_overlap:
            failures.append({
                "bag": bag["index"],
                "other_clause": other,
                "overlap": list(overlap),
                "attack_overlap": {"".join(map(str, key)): value for key, value in attack_overlap.items()},
                "honest_overlap": {"".join(map(str, key)): value for key, value in honest_overlap.items()},
            })
    assert failures
    return failures


def drop_audits(bags, checks, honest_selector):
    single_bag = []
    for bag in bags:
        selector = list(honest_selector)
        selector[bag["offset"]:bag["offset"] + bag["size"]] = (0,) * bag["size"]
        single_bag.append({
            "bag": bag["index"],
            "breakdown": objective_breakdown(checks, tuple(selector)),
        })
    single_clause = []
    for clause in range(N_CLAUSES):
        selector = list(honest_selector)
        dropped = []
        for bag in bags:
            if clause in bag["clauses"]:
                selector[bag["offset"]:bag["offset"] + bag["size"]] = (0,) * bag["size"]
                dropped.append(bag["index"])
        single_clause.append({
            "clause": clause,
            "bags": dropped,
            "breakdown": objective_breakdown(checks, tuple(selector)),
        })
    assert min(record["breakdown"]["total"] for record in single_bag) > len(honest_selector) + SHELL_EXCESS
    assert min(record["breakdown"]["total"] for record in single_clause) > len(honest_selector) + SHELL_EXCESS
    return single_bag, single_clause


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
    unsat_clauses, unsat_bags, B, unsat_checks = reconstruct_instance(manifest["instances"][0])
    control_clauses, control_bags, control_B, control_checks = reconstruct_instance(manifest["instances"][1])
    assert B == control_B == manifest["baseline_B"] == 520
    assert manifest["audited_shell_squared_radius"] == B + SHELL_EXCESS == 552

    unsat_satisfying = satisfying_assignments(unsat_clauses)
    control_satisfying = satisfying_assignments(control_clauses)
    assert not unsat_satisfying
    assert control_satisfying == ((1, 1, 1, 0), (1, 1, 1, 1))

    control_selector = honest_pair_selector(control_bags, control_satisfying[0])
    assert not any(residual(control_checks, control_selector))
    control_breakdown = objective_breakdown(control_checks, control_selector)
    assert control_breakdown == {
        "anchor": B,
        "anchor_extra": 0,
        "raw_residual_squared": 0,
        "total": B,
    }
    # Every integral anchor coordinate has odd square at least one, proving the
    # displayed control witness is the exact unrestricted minimum B.
    control_exact_minimum2 = B

    zero_shell = verify_zero_residual_shell_structure(unsat_clauses, unsat_bags)
    assert zero_shell["compatible_legal_label_tuple_count"] == 0
    one_residual = verify_one_residual_boolean_impossibility()

    # Together these are an exhaustive shell proof.  Zero residual through
    # extra 32 would imply a compatible legal label tuple; nonzero residual
    # through extra 32 would have exactly one residual row and Boolean
    # coefficients, excluded by the three structural cases above.
    obstruction_has_vector_through_shell = False

    lifted_g11, lifted_g11_breakdown = lift_affine_collision(
        unsat_clauses, unsat_bags, unsat_checks
    )
    assert lifted_g11_breakdown["total"] == B + 928
    g7_failures = g7_extension_audit(unsat_clauses, unsat_bags)

    single_bag_drops, single_clause_drops = drop_audits(
        control_bags, control_checks, control_selector
    )

    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[1])),
        "selector_count_B": B,
        "bag_count": len(unsat_bags),
        "check_count": len(unsat_checks),
        "audited_shell_squared_radius": B + SHELL_EXCESS,
        "control_exact_unrestricted_minimum_squared": control_exact_minimum2,
        "zero_residual_shell_certificate": zero_shell,
        "one_residual_boolean_certificate": one_residual,
        "obstruction_has_vector_through_audited_shell": obstruction_has_vector_through_shell,
        "G11_affine_collision_lift_breakdown": lifted_g11_breakdown,
        "G7_nonextendable_incident_bag_count": len(g7_failures),
        "G7_extension_failures": g7_failures,
        "single_bag_drop_minimum_squared_distance": min(
            record["breakdown"]["total"] for record in single_bag_drops
        ),
        "single_bag_drop_audit": single_bag_drops,
        "single_clause_drop_minimum_squared_distance": min(
            record["breakdown"]["total"] for record in single_clause_drops
        ),
        "single_clause_drop_audit": single_clause_drops,
        "finding": (
            "the complete pair-bag lift has no obstruction vector through B+32=552; "
            "the control exact minimum is B=520"
        ),
        "scope": (
            "finite pass only: fixed pair bags have no proved composition law or growing gap"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
