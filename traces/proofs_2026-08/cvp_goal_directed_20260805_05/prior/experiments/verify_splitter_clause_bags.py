#!/usr/bin/env python3
"""Generation-38 exact bounded audit of 3/4-clause splitter bags.

A deterministic 12-bag separating family is used on the nine-clause
obstruction and matched control.  Each bag has one unrestricted integral
selector for every assignment satisfying all clauses in that bag.  Emitted
rows are bag normalization and every complete shared-variable marginal
between every bag pair.  The objective is ||2z-1||^2+25||Az-b||^2.

Eleven bags contain all four variables.  Pairwise complete marginals force
their full signed distributions to agree whenever residual squared is below
10.  Their legal-support intersection is empty on the obstruction, so the
common distribution would be zero and eleven normalization rows would fail.
Thus no obstruction vector exists through B+64.  This is finite evidence only.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, product
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

import verify_global_psd_metric as gen9

CLAUSE_COUNT = 9
CANDIDATE_BAGS = tuple(combinations(range(CLAUSE_COUNT), 3)) + tuple(
    combinations(range(CLAUSE_COUNT), 4)
)
# Deterministic lexicographic refinement among cardinality-12 optima.
BAGS = (
    (0, 1, 2),
    (0, 3, 4),
    (0, 5, 6),
    (0, 7, 8),
    (1, 3, 5),
    (1, 4, 7),
    (1, 6, 8),
    (2, 3, 8),
    (2, 4, 6),
    (2, 5, 7),
    (3, 6, 7),
    (4, 5, 8),
)
SHELL_EXCESS = 64
MANIFEST_PATH = Path(__file__).with_name("gen38_splitter_clause_bags_manifest.json")
G13_COEFFICIENTS = (1, -1, -1, 1, 0, 0, 0, 0, -1, 1, 1, -1, 1, 0, 0, 0)


def splitter_requirements():
    return tuple(
        (support, distinguished)
        for size in range(1, 5)
        for support in combinations(range(CLAUSE_COUNT), size)
        for distinguished in support
    )


def bag_covers_requirement(bag, requirement):
    support, distinguished = requirement
    return distinguished in bag and set(bag).intersection(support) == {distinguished}


def verify_minimum_cardinality():
    requirements = splitter_requirements()
    incidence = np.zeros((len(requirements), len(CANDIDATE_BAGS)))
    for row, requirement in enumerate(requirements):
        for column, bag in enumerate(CANDIDATE_BAGS):
            incidence[row, column] = int(bag_covers_requirement(bag, requirement))
    result = milp(
        np.ones(len(CANDIDATE_BAGS)),
        integrality=np.ones(len(CANDIDATE_BAGS)),
        bounds=Bounds(0, 1),
        constraints=LinearConstraint(incidence, 1, np.inf),
        options={"mip_rel_gap": 0.0},
    )
    assert result.success
    assert result.mip_gap == 0
    optimum = int(round(result.fun))
    assert optimum == len(BAGS) == 12
    return {
        "candidate_bag_count": len(CANDIDATE_BAGS),
        "requirement_count": len(requirements),
        "minimum_cardinality": optimum,
        "solver": "scipy.optimize.milp/HiGHS",
        "mip_gap": float(result.mip_gap),
        "selected_family_covers_every_requirement": all(
            any(bag_covers_requirement(bag, requirement) for bag in BAGS)
            for requirement in requirements
        ),
    }


def bag_is_legal(clause_data, clause_indices, variables, assignment):
    values = dict(zip(variables, assignment))
    for clause_index in clause_indices:
        clause = clause_data[clause_index]
        pattern = tuple(
            values[variable] ^ clause["false_bits"][position]
            for position, variable in enumerate(clause["variables"])
        )
        if pattern == (0, 0, 0):
            return False
    return True


def build_bags(edges):
    clauses = gen9.clause_data(edges)
    records = []
    offset = 0
    for index, clause_indices in enumerate(BAGS):
        variables = tuple(sorted(set().union(*(
            set(clauses[clause]["variables"]) for clause in clause_indices
        ))))
        assignments = tuple(
            assignment for assignment in product((0, 1), repeat=len(variables))
            if bag_is_legal(clauses, clause_indices, variables, assignment)
        )
        records.append({
            "index": index,
            "clauses": clause_indices,
            "variables": variables,
            "assignments": assignments,
            "offset": offset,
            "size": len(assignments),
        })
        offset += len(assignments)
    return clauses, tuple(records), offset


def build_checks(bags, dimension):
    checks = []
    for bag in bags:
        row = [0] * dimension
        for local in range(bag["size"]):
            row[bag["offset"] + local] = 1
        checks.append({
            "kind": "normalization", "bag": bag["index"],
            "coefficients": tuple(row), "rhs": 1,
        })
    for left, right in combinations(bags, 2):
        overlap = tuple(sorted(set(left["variables"]) & set(right["variables"])))
        for overlap_assignment in product((0, 1), repeat=len(overlap)):
            row = [0] * dimension
            for sign, bag in ((1, left), (-1, right)):
                positions = tuple(bag["variables"].index(variable) for variable in overlap)
                for local, assignment in enumerate(bag["assignments"]):
                    if tuple(assignment[position] for position in positions) == overlap_assignment:
                        row[bag["offset"] + local] += sign
            checks.append({
                "kind": "complete_shared_marginal", "bags": (left["index"], right["index"]),
                "variables": overlap, "assignment": overlap_assignment,
                "coefficients": tuple(row), "rhs": 0,
            })
    assert Counter(check["kind"] for check in checks) == {
        "normalization": 12,
        "complete_shared_marginal": 968,
    }
    return tuple(checks)


def sparse(row):
    return [[index, int(value)] for index, value in enumerate(row) if value]


def factor_hash(checks, dimension):
    payload = {
        "anchor_rows": [[[index, 2]] for index in range(dimension)],
        "anchor_target": [1] * dimension,
        "residual_rows": [
            [[index, 5 * value] for index, value in check["terms"]]
            for check in checks
        ],
        "residual_target": [5 * check["rhs"] for check in checks],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def instance_record(name, edges):
    clauses, bags, dimension = build_bags(edges)
    checks_raw = build_checks(bags, dimension)
    emitted_checks = [{
        key: (list(value) if isinstance(value, tuple) else value)
        for key, value in check.items() if key != "coefficients"
    } | {"terms": sparse(check["coefficients"])} for check in checks_raw]
    return {
        "name": name,
        "edges": [list(edge) for edge in edges],
        "selector_count_B": dimension,
        "bags": [{
            "index": bag["index"],
            "clauses": list(bag["clauses"]),
            "variables": list(bag["variables"]),
            "assignments": [list(value) for value in bag["assignments"]],
            "offset": bag["offset"],
            "size": bag["size"],
        } for bag in bags],
        "check_count": len(checks_raw),
        "checks": emitted_checks,
        "lattice_rank": dimension,
        "ambient_dimension": dimension + len(checks_raw),
        "factor_rule": "[2I;5A]",
        "target_rule": "[1;5b]",
        "factor_target_sha256": factor_hash(emitted_checks, dimension),
        "gram_eigenvalue_lower_bound": 4,
    }


def reconstruct(record):
    edges = tuple(tuple(edge) for edge in record["edges"])
    clauses, bags, dimension = build_bags(edges)
    checks = build_checks(bags, dimension)
    emitted = [{
        key: (list(value) if isinstance(value, tuple) else value)
        for key, value in check.items() if key != "coefficients"
    } | {"terms": sparse(check["coefficients"])} for check in checks]
    assert emitted == record["checks"]
    assert factor_hash(emitted, dimension) == record["factor_target_sha256"]
    return clauses, bags, checks, dimension


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


def honest_selector(bags, assignment):
    selector = [0] * sum(bag["size"] for bag in bags)
    for bag in bags:
        local = tuple(assignment[variable] for variable in bag["variables"])
        index = bag["assignments"].index(local)
        selector[bag["offset"] + index] = 1
    return tuple(selector)


def projected_g13_selector(bags):
    global_assignments = tuple(product((0, 1), repeat=4))
    selector = [0] * sum(bag["size"] for bag in bags)
    for bag in bags:
        for local, local_assignment in enumerate(bag["assignments"]):
            coefficient = sum(
                G13_COEFFICIENTS[index]
                for index, assignment in enumerate(global_assignments)
                if tuple(assignment[variable] for variable in bag["variables"]) == local_assignment
            )
            selector[bag["offset"] + local] = coefficient
    return tuple(selector)


def shell_certificate(bags, dimension):
    full = tuple(bag for bag in bags if len(bag["variables"]) == 4)
    assert len(full) == 11
    # The full bags collectively contain every clause, so every global
    # assignment is forbidden by at least one of their legal supports.
    assignments = tuple(product((0, 1), repeat=4))
    common_legal = []
    for assignment in assignments:
        if all(tuple(assignment) in bag["assignments"] for bag in full):
            common_legal.append(assignment)
    assert not common_legal
    # If raw residual squared <=2, then for each assignment coordinate the 11
    # full-bag values must agree: any nonconstant integer vector on 11 entries
    # contributes at least 10 across the emitted all-pairs equality rows.
    # Their common vector has empty legal support, hence is zero, making all 11
    # normalization residuals -1. Contradiction. Thus raw residual^2>=3.
    return {
        "full_variable_bag_count": len(full),
        "full_variable_bag_indices": [bag["index"] for bag in full],
        "common_legal_assignment_count": len(common_legal),
        "minimum_pairwise_energy_of_nonconstant_11_integer_values": 10,
        "normalization_energy_if_common_vector_zero": 11,
        "certified_raw_residual_squared_lower_bound": 3,
        "audited_shell_squared": dimension + SHELL_EXCESS,
        "derived_coefficient_interval": [-3, 4],
    }


def build_manifest():
    splitter = verify_minimum_cardinality()
    unsat = instance_record("nine_clause_obstruction", gen9.UNSAT_EDGES)
    control = instance_record("matched_satisfiable_control", gen9.CONTROL_EDGES)
    return {
        "schema": "gen38-splitter-clause-bags-v1",
        "finite_claim_only": True,
        "selected_proposal": "Pro proposal 5: splitter-indexed logarithmic bags",
        "mechanism": "3/4-clause bags isolate every support of size at most four and may block affine parity lifts",
        "falsification_condition": "control mismatch, exact G13 lift, or any obstruction vector through B+64",
        "splitter_family": {
            "bags": [list(bag) for bag in BAGS],
            "selection_rule": "deterministic lexicographic refinement of a minimum-cardinality MILP solution",
            **splitter,
        },
        "coefficient_domain": "all integers",
        "external_filters": [],
        "objective": "||2z-1||^2+25||Az-b||^2",
        "shell_excess": SHELL_EXCESS,
        "instances": [unsat, control],
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
    unsat_clauses, unsat_bags, unsat_checks, unsat_B = reconstruct(manifest["instances"][0])
    control_clauses, control_bags, control_checks, control_B = reconstruct(manifest["instances"][1])
    assert unsat_B == 117
    assert control_B == 119

    control_selector = honest_selector(control_bags, (1, 1, 1, 0))
    control_breakdown = objective_breakdown(control_checks, control_selector)
    assert control_breakdown == {
        "anchor": control_B,
        "anchor_extra": 0,
        "raw_residual_squared": 0,
        "total": control_B,
    }
    # Universal odd anchor lower bound proves this control minimum exactly.

    certificate = shell_certificate(unsat_bags, unsat_B)
    assert 25 * certificate["certified_raw_residual_squared_lower_bound"] > SHELL_EXCESS

    g13 = projected_g13_selector(unsat_bags)
    g13_breakdown = objective_breakdown(unsat_checks, g13)
    assert g13_breakdown["total"] > unsat_B + SHELL_EXCESS
    zero = (0,) * unsat_B
    drop_breakdown = objective_breakdown(unsat_checks, zero)

    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[1])),
        "splitter_family": manifest["splitter_family"],
        "obstruction_selector_count_B": unsat_B,
        "control_selector_count_B": control_B,
        "check_count": len(unsat_checks),
        "control_exact_minimum_squared": control_B,
        "obstruction_shell_certificate": certificate,
        "obstruction_has_vector_through_B_plus_64": False,
        "projected_G13_breakdown": g13_breakdown,
        "all_zero_DROP_breakdown": drop_breakdown,
        "finding": "the frozen 12-bag family excludes every unrestricted obstruction vector through B+64",
        "scope": "finite shell pass only; no logarithmic-bag scaling or polynomial gap theorem",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
