#!/usr/bin/env python3
"""Generation-15 falsification of a preregistered weighted sparse hierarchy.

The hierarchy is the deterministic adjacent-pair laminar tree on the nine
clauses.  Leaves store clause assignments; internal nodes store assignments to
the union of their clauses' variables.  Every normalization, leaf-legality,
and parent/child full marginal equation is emitted.

Unscaled weights are frozen as epsilon_leaf=1, epsilon_internal=1/16, and
W=16 for residuals.  Multiplying squared distance by 256 gives the integral
factor used here:

* leaf anchors: (32z-16)^2,
* internal anchors: (2z-1)^2,
* residual rows: 256^2 (Az-b)^2.

The threshold is B + 256*m^(3/2), i.e. delta=1/2.  The Generation-13 affine
measure lifts through every node with zero residual and lies below this
threshold already at m=9.  This kills only this frozen hierarchy/weight rule.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import product
import hashlib
import json
from pathlib import Path

import verify_global_psd_metric as gen9
import verify_degree3_global_psd_metric as gen11

N_CLAUSES = 9
LEAF_ANCHOR_COEFFICIENT = 32
LEAF_ANCHOR_TARGET = 16
INTERNAL_ANCHOR_COEFFICIENT = 2
INTERNAL_ANCHOR_TARGET = 1
RESIDUAL_FACTOR = 256
DELTA_NUMERATOR = 1
DELTA_DENOMINATOR = 2
MANIFEST_PATH = Path(__file__).with_name("gen15_weighted_laminar_hierarchy_manifest.json")
AFFINE_COEFFICIENTS = (1, -1, -1, 1, 0, 0, 0, 0,
                       -1, 1, 1, -1, 1, 0, 0, 0)


def sparse(vector):
    return [[index, int(value)] for index, value in enumerate(vector) if value]


def build_nodes(clauses):
    nodes = []
    offset = 0
    for clause in range(N_CLAUSES):
        variables = tuple(clauses[clause]["variables"])
        assignments = tuple(product((0, 1), repeat=len(variables)))
        nodes.append({
            "index": len(nodes),
            "clauses": (clause,),
            "variables": variables,
            "assignments": assignments,
            "children": (),
            "level": 0,
            "offset": offset,
            "size": len(assignments),
        })
        offset += len(assignments)

    current = list(range(N_CLAUSES))
    level = 1
    while len(current) > 1:
        next_level = []
        position = 0
        while position < len(current):
            if position + 1 == len(current):
                next_level.append(current[position])
                position += 1
                continue
            left, right = current[position], current[position + 1]
            clause_indices = tuple(sorted(nodes[left]["clauses"] + nodes[right]["clauses"]))
            variables = tuple(sorted({
                variable
                for clause in clause_indices
                for variable in clauses[clause]["variables"]
            }))
            assignments = tuple(product((0, 1), repeat=len(variables)))
            nodes.append({
                "index": len(nodes),
                "clauses": clause_indices,
                "variables": variables,
                "assignments": assignments,
                "children": (left, right),
                "level": level,
                "offset": offset,
                "size": len(assignments),
            })
            offset += len(assignments)
            next_level.append(nodes[-1]["index"])
            position += 2
        current = next_level
        level += 1

    assert len(nodes) == 17
    assert current == [16]
    assert Counter(node["level"] for node in nodes) == {0: 9, 1: 4, 2: 2, 3: 1, 4: 1}
    assert all(node["size"] == 8 for node in nodes[:9])
    assert all(node["size"] == 16 for node in nodes[9:])
    assert offset == 200
    return tuple(nodes), offset


def clause_pattern(clause, assignment_by_variable):
    return tuple(
        assignment_by_variable[variable] ^ clause["false_bits"][position]
        for position, variable in enumerate(clause["variables"])
    )


def build_checks(clauses, nodes, dimension):
    checks = []
    for node in nodes:
        row = [0] * dimension
        for local in range(node["size"]):
            row[node["offset"] + local] = 1
        checks.append({
            "kind": "node_normalization",
            "node": node["index"],
            "coefficients": tuple(row),
            "rhs": 1,
        })

    for leaf in nodes[:N_CLAUSES]:
        clause_index = leaf["clauses"][0]
        clause = clauses[clause_index]
        row = [0] * dimension
        for local, assignment in enumerate(leaf["assignments"]):
            values = dict(zip(leaf["variables"], assignment))
            if clause_pattern(clause, values) == (0, 0, 0):
                row[leaf["offset"] + local] = 1
        checks.append({
            "kind": "leaf_legality",
            "node": leaf["index"],
            "clause": clause_index,
            "coefficients": tuple(row),
            "rhs": 0,
        })

    for parent in nodes[N_CLAUSES:]:
        for child_index in parent["children"]:
            child = nodes[child_index]
            child_positions = tuple(parent["variables"].index(v) for v in child["variables"])
            for child_local, child_assignment in enumerate(child["assignments"]):
                row = [0] * dimension
                row[child["offset"] + child_local] = 1
                for parent_local, parent_assignment in enumerate(parent["assignments"]):
                    restriction = tuple(parent_assignment[position] for position in child_positions)
                    if restriction == child_assignment:
                        row[parent["offset"] + parent_local] -= 1
                checks.append({
                    "kind": "parent_child_full_marginal",
                    "parent": parent["index"],
                    "child": child_index,
                    "child_assignment": child_local,
                    "coefficients": tuple(row),
                    "rhs": 0,
                })
    assert Counter(check["kind"] for check in checks) == {
        "node_normalization": 17,
        "leaf_legality": 9,
        "parent_child_full_marginal": 184,
    }
    return tuple(checks)


def baseline(nodes):
    leaf_coordinates = sum(node["size"] for node in nodes if node["level"] == 0)
    internal_coordinates = sum(node["size"] for node in nodes if node["level"] > 0)
    value = leaf_coordinates * LEAF_ANCHOR_TARGET ** 2 + internal_coordinates
    assert leaf_coordinates == 72 and internal_coordinates == 128
    assert value == 18560
    return value


def threshold_squared(nodes):
    m = N_CLAUSES
    # m^(1+delta)=9^(3/2)=27 exactly.
    additive = 256 * 27
    assert additive == 6912
    return baseline(nodes) + additive


def factor_target_hash(checks, nodes, dimension):
    anchor_rows = []
    anchor_target = []
    for node in nodes:
        coefficient = (
            LEAF_ANCHOR_COEFFICIENT if node["level"] == 0
            else INTERNAL_ANCHOR_COEFFICIENT
        )
        target = LEAF_ANCHOR_TARGET if node["level"] == 0 else INTERNAL_ANCHOR_TARGET
        for local in range(node["size"]):
            coordinate = node["offset"] + local
            anchor_rows.append([[coordinate, coefficient]])
            anchor_target.append(target)
    payload = {
        "anchor_rows": anchor_rows,
        "anchor_target": anchor_target,
        "residual_rows": [
            [[index, RESIDUAL_FACTOR * value] for index, value in sparse(check["coefficients"])]
            for check in checks
        ],
        "residual_target": [RESIDUAL_FACTOR * check["rhs"] for check in checks],
    }
    assert len(anchor_rows) == dimension
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def instance_data(name, edges):
    clauses = gen9.clause_data(edges)
    nodes, dimension = build_nodes(clauses)
    checks = build_checks(clauses, nodes, dimension)
    record = {
        "name": name,
        "edges": [list(edge) for edge in edges],
        "clause_count_m": N_CLAUSES,
        "selector_dimension": dimension,
        "node_count": len(nodes),
        "nodes": [{
            "index": node["index"],
            "clauses": list(node["clauses"]),
            "variables": list(node["variables"]),
            "assignments": [list(value) for value in node["assignments"]],
            "children": list(node["children"]),
            "level": node["level"],
            "offset": node["offset"],
            "size": node["size"],
        } for node in nodes],
        "check_count": len(checks),
        "checks": [{
            key: (list(value) if isinstance(value, tuple) else value)
            for key, value in check.items() if key != "coefficients"
        } | {"terms": sparse(check["coefficients"])} for check in checks],
        "lattice_rank": dimension,
        "ambient_dimension": dimension + len(checks),
        "factor_target_sha256": factor_target_hash(checks, nodes, dimension),
        "baseline_squared_radius_B": baseline(nodes),
        "threshold_squared_T": threshold_squared(nodes),
        "certified_gram_eigenvalue_lower_bound": 4,
    }
    return clauses, nodes, dimension, checks, record


def build_manifest():
    unsat = instance_data("generation_7_obstruction", gen9.UNSAT_EDGES)[4]
    control = instance_data("satisfiable_overlapping_control", gen9.CONTROL_EDGES)[4]
    return {
        "schema": "gen15-weighted-laminar-hierarchy-v1",
        "finite_claim_only": True,
        "preregistered_rule": {
            "hierarchy": "adjacent-pair laminar tree with odd-node carry",
            "levels": "clause leaves followed by 2,4,8,9-clause nodes",
            "unscaled_epsilon_leaf": "1",
            "unscaled_epsilon_internal": "1/16",
            "unscaled_residual_weight_W": "16",
            "integral_squared_distance_scale": 256,
            "delta": "1/2",
            "threshold": "B+256*m^(1+delta)",
            "coefficient_domain": "all integers",
            "external_filters": [],
        },
        "instances": [unsat, control],
    }


def reconstruct(record):
    edges = tuple(tuple(edge) for edge in record["edges"])
    clauses = gen9.clause_data(edges)
    nodes, dimension = build_nodes(clauses)
    checks = build_checks(clauses, nodes, dimension)
    assert dimension == record["selector_dimension"]
    assert len(checks) == record["check_count"]
    assert factor_target_hash(checks, nodes, dimension) == record["factor_target_sha256"]
    emitted = [{
        key: (list(value) if isinstance(value, tuple) else value)
        for key, value in check.items() if key != "coefficients"
    } | {"terms": sparse(check["coefficients"])} for check in checks]
    assert emitted == record["checks"]
    return clauses, nodes, dimension, checks


def residual(checks, selector):
    return tuple(
        sum(value * coefficient for value, coefficient in zip(check["coefficients"], selector))
        - check["rhs"]
        for check in checks
    )


def objective_breakdown(nodes, checks, selector):
    leaf_anchor = 0
    internal_anchor = 0
    for node in nodes:
        block = selector[node["offset"]:node["offset"] + node["size"]]
        if node["level"] == 0:
            leaf_anchor += sum((32 * value - 16) ** 2 for value in block)
        else:
            internal_anchor += sum((2 * value - 1) ** 2 for value in block)
    raw = residual(checks, selector)
    residual_energy = RESIDUAL_FACTOR ** 2 * sum(value * value for value in raw)
    return {
        "leaf_anchor": leaf_anchor,
        "internal_anchor": internal_anchor,
        "anchor": leaf_anchor + internal_anchor,
        "anchor_extra": leaf_anchor + internal_anchor - baseline(nodes),
        "raw_residual_squared": sum(value * value for value in raw),
        "residual_energy": residual_energy,
        "total": leaf_anchor + internal_anchor + residual_energy,
    }


def honest_hierarchy_selector(nodes, assignment):
    selector = [0] * sum(node["size"] for node in nodes)
    for node in nodes:
        local = tuple(assignment[variable] for variable in node["variables"])
        index = node["assignments"].index(local)
        selector[node["offset"] + index] = 1
    return tuple(selector)


def affine_lift(nodes):
    assignments = tuple(product((0, 1), repeat=4))
    honest = tuple(honest_hierarchy_selector(nodes, assignment) for assignment in assignments)
    assert sum(AFFINE_COEFFICIENTS) == 1
    return tuple(
        sum(AFFINE_COEFFICIENTS[index] * honest[index][coordinate]
            for index in range(16))
        for coordinate in range(len(honest[0]))
    )


def single_leaf_drops(nodes, checks, honest_selector):
    records = []
    for leaf in nodes[:N_CLAUSES]:
        selector = list(honest_selector)
        selector[leaf["offset"]:leaf["offset"] + leaf["size"]] = (0,) * leaf["size"]
        records.append({
            "clause": leaf["clauses"][0],
            "breakdown": objective_breakdown(nodes, checks, tuple(selector)),
        })
    return records


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
    unsat_clauses, unsat_nodes, dimension, unsat_checks = reconstruct(manifest["instances"][0])
    control_clauses, control_nodes, control_dimension, control_checks = reconstruct(manifest["instances"][1])
    assert dimension == control_dimension == 200
    B = baseline(unsat_nodes)
    T = threshold_squared(unsat_nodes)
    assert B == 18560 and T == 25472

    # Direct truth-table audit of obstruction and control.
    assert all(gen9.honest_selector(unsat_clauses, assignment)[1]
               for assignment in product((0, 1), repeat=4))
    control_assignment = (1, 1, 1, 0)
    _, falsified = gen9.honest_selector(control_clauses, control_assignment)
    assert not falsified

    control_selector = honest_hierarchy_selector(control_nodes, control_assignment)
    assert not any(residual(control_checks, control_selector))
    control_breakdown = objective_breakdown(control_nodes, control_checks, control_selector)
    assert control_breakdown["total"] == B
    # Every integral leaf anchor is at least 16^2 and every internal anchor at
    # least 1; residual energy is nonnegative, so B is the exact control min.
    control_exact_minimum2 = B

    attack = affine_lift(unsat_nodes)
    attack_breakdown = objective_breakdown(unsat_nodes, unsat_checks, attack)
    assert attack_breakdown == {
        "leaf_anchor": 24576,
        "internal_anchor": 384,
        "anchor": 24960,
        "anchor_extra": 6400,
        "raw_residual_squared": 0,
        "residual_energy": 0,
        "total": 24960,
    }
    assert attack_breakdown["total"] < T

    # Verify that leaf marginals reproduce the exact G11 selector.
    expected_g11 = tuple(gen11.exact_zero_residual_search(unsat_clauses)["selector"])
    lifted_leaf_blocks = []
    for leaf in unsat_nodes[:N_CLAUSES]:
        clause = unsat_clauses[leaf["clauses"][0]]
        block = [0] * 8
        for local, assignment in enumerate(leaf["assignments"]):
            values = dict(zip(leaf["variables"], assignment))
            pattern = clause_pattern(clause, values)
            block[gen9.PATTERNS.index(pattern)] = attack[leaf["offset"] + local]
        lifted_leaf_blocks.extend(block)
    lifted_leaves = tuple(lifted_leaf_blocks)
    assert lifted_leaves == expected_g11

    drops = single_leaf_drops(control_nodes, control_checks, control_selector)
    assert min(record["breakdown"]["total"] for record in drops) > T

    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[1])),
        "clause_count_m": N_CLAUSES,
        "selector_dimension": dimension,
        "node_count": len(unsat_nodes),
        "check_count": len(unsat_checks),
        "baseline_squared_radius_B": B,
        "threshold_squared_T": T,
        "delta": "1/2",
        "control_exact_unrestricted_minimum_squared": control_exact_minimum2,
        "G13_affine_lift_coefficients": list(AFFINE_COEFFICIENTS),
        "G13_G11_zero_residual_attack": attack_breakdown,
        "attack_margin_below_threshold": T - attack_breakdown["total"],
        "single_leaf_drop_minimum_squared_distance": min(
            record["breakdown"]["total"] for record in drops
        ),
        "single_leaf_drop_audit": drops,
        "finding": (
            "the preregistered weighted laminar hierarchy is falsified by a zero-residual "
            "affine lift at 24960 below threshold 25472"
        ),
        "scope": (
            "finite kill of this hierarchy and weight rule only; no asymptotic theorem"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
