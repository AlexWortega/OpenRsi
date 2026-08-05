#!/usr/bin/env python3
"""Generation-28 frozen depth-two min-plus audit of a reduced G14 tile.

Each tile consists of two same-variable Generation-14 pair bags.  A bag has
one integral coefficient for each of the eight assignments, normalization,
and two endpoint-legality rows.  The tile equates the bags' complete
assignment ports.  Two tiles are glued by one fixed identity port map.

The obstruction's eight legality rows forbid all eight assignments.  A
matched control replaces the last forbidden assignment by a duplicate, so it
has one honest assignment.  The exact objective is

    ||2z-1||^2 + 25 ||Az-b||^2.

The verifier serializes the factor/target, port classes, complete depth-one
and depth-two tables through the preregistered radius 57, and known DROP,
G13, and G19-style attacks.  This is a finite recursion-rule audit only.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

ANCHOR_SCALE = 2
RESIDUAL_SCALE = 5
PORT_DIMENSION = 8
TILE_DIMENSION = 16
DEPTH2_DIMENSION = 32
LOCAL_TABLE_RADIUS2 = 41
DEPTH2_RADIUS2 = 57
COEFFICIENT_MIN = -2
COEFFICIENT_MAX = 3
IDENTITY_SEAM = tuple(range(PORT_DIMENSION))
MANIFEST_PATH = Path(__file__).with_name("gen28_frozen_minplus_pair_tile_manifest.json")

TILE_A = ((0, 1), (2, 3))
TILE_B_UNSAT = ((4, 5), (6, 7))
TILE_B_CONTROL = ((4, 5), (6, 0))
G13_BASE = (0, 1, 1, -1, 1, -1, -1, 1)
G13_PORTS = tuple(sorted({tuple(G13_BASE[index ^ shift] for index in range(8)) for shift in range(8)}))
G19_SEEDS = tuple(
    tuple(-1 if index in negatives else 1 if index in positives else 0 for index in range(8))
    for negatives in combinations(range(8), 2)
    for positives in combinations(tuple(index for index in range(8) if index not in negatives), 3)
)


def sparse(row):
    return [[index, int(value)] for index, value in enumerate(row) if value]


def is_one_hot(port):
    return sum(port) == 1 and all(value in (0, 1) for value in port)


def is_g19_style(port):
    """Include the exact two-negative seeds and cheaper one-negative splices."""
    return (
        sum(port) == 1
        and not is_one_hot(port)
        and all(value in (-1, 0, 1) for value in port)
        and 1 <= sum(value < 0 for value in port) <= 2
    )


def classify(blocks, residual_squared):
    """A disjoint and exhaustive priority partition of every integral state."""
    zero = (0,) * PORT_DIMENSION
    if any(block == zero for block in blocks):
        return "DROP"
    if any(block in G13_PORTS for block in blocks):
        return "G13"
    if any(is_g19_style(block) for block in blocks):
        return "G19"
    if all(is_one_hot(block) for block in blocks):
        return "LEGAL" if residual_squared == 0 else "ILLEGAL"
    return "MALFORMED"


def bag_breakdown(port, forbidden):
    anchor = sum((2 * value - 1) ** 2 for value in port)
    residuals = (sum(port) - 1,) + tuple(port[index] for index in forbidden)
    residual_squared = sum(value * value for value in residuals)
    return anchor, residual_squared, anchor + 25 * residual_squared


def tile_breakdown(left, right, tile):
    left_anchor, left_residual, _ = bag_breakdown(left, tile[0])
    right_anchor, right_residual, _ = bag_breakdown(right, tile[1])
    seam = tuple(left[index] - right[index] for index in IDENTITY_SEAM)
    residual_squared = left_residual + right_residual + sum(value * value for value in seam)
    anchor = left_anchor + right_anchor
    return {
        "anchor": anchor,
        "raw_residual_squared": residual_squared,
        "total": anchor + 25 * residual_squared,
    }


def depth2_breakdown(blocks, right_tile):
    left, middle_left, middle_right, right = blocks
    first = tile_breakdown(left, middle_left, TILE_A)
    second = tile_breakdown(middle_right, right, right_tile)
    seam = tuple(middle_left[index] - middle_right[index] for index in IDENTITY_SEAM)
    residual_squared = (
        first["raw_residual_squared"]
        + second["raw_residual_squared"]
        + sum(value * value for value in seam)
    )
    anchor = first["anchor"] + second["anchor"]
    return {
        "anchor": anchor,
        "anchor_extra": anchor - DEPTH2_DIMENSION,
        "raw_residual_squared": residual_squared,
        "total": anchor + 25 * residual_squared,
    }


def enumerate_bag_states(forbidden, cap):
    """Enumerate every unrestricted integral bag whose local cost is <= cap."""
    states = []

    def visit(prefix, anchor):
        coordinate = len(prefix)
        if coordinate == PORT_DIMENSION:
            breakdown = bag_breakdown(prefix, forbidden)
            if breakdown[2] <= cap:
                states.append((tuple(prefix), breakdown[2]))
            return
        for value in range(COEFFICIENT_MIN, COEFFICIENT_MAX + 1):
            new_anchor = anchor + (2 * value - 1) ** 2
            remaining_minimum = PORT_DIMENSION - coordinate - 1
            if new_anchor + remaining_minimum <= cap:
                visit(prefix + (value,), new_anchor)

    visit((), 0)
    states.sort()
    return tuple(states)


def complete_tile_table(tile):
    # A depth-two vector through 57 leaves at most 41 for either tile because
    # the other tile has the universal 16-coordinate anchor lower bound.
    left_states = enumerate_bag_states(tile[0], LOCAL_TABLE_RADIUS2 - PORT_DIMENSION)
    right_states = enumerate_bag_states(tile[1], LOCAL_TABLE_RADIUS2 - PORT_DIMENSION)
    records = []
    for left, _ in left_states:
        for right, _ in right_states:
            breakdown = tile_breakdown(left, right, tile)
            if breakdown["total"] <= LOCAL_TABLE_RADIUS2:
                records.append({
                    "left_port": list(left),
                    "right_port": list(right),
                    "anchor": breakdown["anchor"],
                    "raw_residual_squared": breakdown["raw_residual_squared"],
                    "cost": breakdown["total"],
                    "class": classify((left, right), breakdown["raw_residual_squared"]),
                })
    records.sort(key=lambda record: (
        record["cost"], record["left_port"], record["right_port"]
    ))
    return records


def compose_tables(left_table, right_table, right_tile):
    records = []
    for first in left_table:
        middle_left = tuple(first["right_port"])
        for second in right_table:
            middle_right = tuple(second["left_port"])
            seam_residual_squared = sum(
                (middle_left[index] - middle_right[index]) ** 2
                for index in IDENTITY_SEAM
            )
            cost = first["cost"] + second["cost"] + 25 * seam_residual_squared
            if cost > DEPTH2_RADIUS2:
                continue
            blocks = (
                tuple(first["left_port"]), middle_left,
                middle_right, tuple(second["right_port"]),
            )
            breakdown = depth2_breakdown(blocks, right_tile)
            assert breakdown["total"] == cost
            records.append({
                "left_port": first["left_port"],
                "middle_left_port": first["right_port"],
                "middle_right_port": second["left_port"],
                "right_port": second["right_port"],
                "anchor": breakdown["anchor"],
                "raw_residual_squared": breakdown["raw_residual_squared"],
                "seam_residual_squared": seam_residual_squared,
                "cost": cost,
                "class": classify(blocks, breakdown["raw_residual_squared"]),
            })
    records.sort(key=lambda record: (
        record["cost"], record["left_port"], record["middle_left_port"],
        record["middle_right_port"], record["right_port"],
    ))
    return records


def build_checks(right_tile):
    checks = []
    tiles = (TILE_A, right_tile)
    for tile_index, tile in enumerate(tiles):
        tile_offset = tile_index * TILE_DIMENSION
        for bag_index, forbidden in enumerate(tile):
            offset = tile_offset + bag_index * PORT_DIMENSION
            row = [0] * DEPTH2_DIMENSION
            for index in range(PORT_DIMENSION):
                row[offset + index] = 1
            checks.append({"kind": "normalization", "tile": tile_index, "bag": bag_index,
                           "rhs": 1, "terms": sparse(row)})
            for forbidden_index in forbidden:
                row = [0] * DEPTH2_DIMENSION
                row[offset + forbidden_index] = 1
                checks.append({"kind": "endpoint_legality", "tile": tile_index,
                               "bag": bag_index, "forbidden_assignment": forbidden_index,
                               "rhs": 0, "terms": sparse(row)})
        for index in range(PORT_DIMENSION):
            row = [0] * DEPTH2_DIMENSION
            row[tile_offset + index] = 1
            row[tile_offset + PORT_DIMENSION + IDENTITY_SEAM[index]] = -1
            checks.append({"kind": "internal_full_port_glue", "tile": tile_index,
                           "port_coordinate": index, "rhs": 0, "terms": sparse(row)})
    for index in range(PORT_DIMENSION):
        row = [0] * DEPTH2_DIMENSION
        row[PORT_DIMENSION + index] = 1
        row[TILE_DIMENSION + IDENTITY_SEAM[index]] = -1
        checks.append({"kind": "depth2_full_port_glue", "port_coordinate": index,
                       "rhs": 0, "terms": sparse(row)})
    assert Counter(check["kind"] for check in checks) == {
        "normalization": 4,
        "endpoint_legality": 8,
        "internal_full_port_glue": 16,
        "depth2_full_port_glue": 8,
    }
    return checks


def factor_target_hash(checks):
    payload = {
        "anchor_rows": [[[index, 2]] for index in range(DEPTH2_DIMENSION)],
        "anchor_target": [1] * DEPTH2_DIMENSION,
        "residual_rows": [
            [[index, RESIDUAL_SCALE * value] for index, value in check["terms"]]
            for check in checks
        ],
        "residual_target": [RESIDUAL_SCALE * check["rhs"] for check in checks],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def attack_audit(right_tile):
    zero = (0,) * PORT_DIMENSION
    drop = depth2_breakdown((zero, zero, zero, zero), right_tile)
    g13 = []
    for port in G13_PORTS:
        result = depth2_breakdown((port, port, port, port), right_tile)
        g13.append((result["total"], port, result))
    g19 = []
    for port in G19_SEEDS:
        result = depth2_breakdown((port, port, port, port), right_tile)
        g19.append((result["total"], port, result))
    best_g13 = min(g13)
    best_g19 = min(g19)
    return {
        "DROP_all_zero": drop,
        "G13_orbit_size": len(G13_PORTS),
        "G13_best_diagonal_port": list(best_g13[1]),
        "G13_best_diagonal_breakdown": best_g13[2],
        "G19_exact_two_negative_seed_count": len(G19_SEEDS),
        "G19_best_diagonal_port": list(best_g19[1]),
        "G19_best_diagonal_breakdown": best_g19[2],
    }


def summarize_table(table):
    class_minima = {}
    for record in table:
        name = record["class"]
        class_minima[name] = min(class_minima.get(name, record["cost"]), record["cost"])
    return {
        "entry_count": len(table),
        "cost_histogram": {str(key): value for key, value in sorted(Counter(r["cost"] for r in table).items())},
        "class_histogram": dict(sorted(Counter(r["class"] for r in table).items())),
        "class_minimum_cost": dict(sorted(class_minima.items())),
    }


TILE_A_TABLE = complete_tile_table(TILE_A)
UNSAT_TILE_TABLE = complete_tile_table(TILE_B_UNSAT)
CONTROL_TILE_TABLE = complete_tile_table(TILE_B_CONTROL)


def instance_record(name, right_tile, right_table):
    checks = build_checks(right_tile)
    depth2_table = compose_tables(TILE_A_TABLE, right_table, right_tile)
    return {
        "name": name,
        "right_tile_forbidden_assignments": [list(pair) for pair in right_tile],
        "lattice_rank": DEPTH2_DIMENSION,
        "ambient_dimension": DEPTH2_DIMENSION + len(checks),
        "checks": checks,
        "factor_rule": "[2I;5A]",
        "target_rule": "[1;5b]",
        "factor_target_sha256": factor_target_hash(checks),
        "certified_gram_eigenvalue_lower_bound": 4,
        "right_tile_table": right_table,
        "right_tile_table_summary": summarize_table(right_table),
        "depth2_table": depth2_table,
        "depth2_table_summary": summarize_table(depth2_table),
        "attack_audit": attack_audit(right_tile),
    }


def build_manifest():
    unsat = instance_record("all_eight_assignments_forbidden", TILE_B_UNSAT, UNSAT_TILE_TABLE)
    control = instance_record("last_forbidden_assignment_replaced_by_duplicate_zero", TILE_B_CONTROL, CONTROL_TILE_TABLE)
    adverse_depth1 = min(
        record["cost"] for table in (TILE_A_TABLE, UNSAT_TILE_TABLE)
        for record in table if record["class"] != "LEGAL"
    )
    unsat_depth2 = min(record["cost"] for record in unsat["depth2_table"])
    legal_depth1 = min(record["cost"] for record in TILE_A_TABLE if record["class"] == "LEGAL")
    legal_depth2 = min(record["cost"] for record in control["depth2_table"] if record["class"] == "LEGAL")
    return {
        "schema": "gen28-frozen-reduced-pair-tile-v1",
        "finite_claim_only": True,
        "mechanism": "complete full-assignment ports should make illegal min-plus cost grow faster than legal cost",
        "falsification_condition": "nonclosure, omitted state, control mismatch, or illegal growth lambda no larger than legal growth mu",
        "coefficient_domain": "all integers",
        "external_filters": [],
        "objective": "||2z-1||^2+25||Az-b||^2",
        "port_dimension": PORT_DIMENSION,
        "tile_dimension": TILE_DIMENSION,
        "depth2_lattice_rank": DEPTH2_DIMENSION,
        "left_tile_forbidden_assignments": [list(pair) for pair in TILE_A],
        "allowed_seam_permutations": [list(IDENTITY_SEAM)],
        "glue_topology": "tile0.right == tile1.left in all eight full-assignment coordinates",
        "local_table_radius_squared": LOCAL_TABLE_RADIUS2,
        "depth2_preregistered_radius_squared": DEPTH2_RADIUS2,
        "radius_witness": "a common one-hot assignment violates exactly one of the eight legality rows and has cost 32+25=57",
        "coefficient_bound_derivation": {
            "gram_eigenvalue_lower_bound": 4,
            "global_argument": "at radius 57 the other 31 odd anchor squares contribute at least 31, so (2z_i-1)^2<=26",
            "local_argument": "at local radius 41 the other 15 odd anchor squares contribute at least 15, so (2z_i-1)^2<=26",
            "inclusive_integer_interval": [COEFFICIENT_MIN, COEFFICIENT_MAX],
        },
        "class_partition_priority": [
            "DROP: at least one all-zero port",
            "G13: at least one XOR translate of (0,1,1,-1,1,-1,-1,1)",
            "G19: at least one normalized {-1,0,1} port with one or two negatives",
            "LEGAL: every port is one-hot and every emitted residual is zero",
            "ILLEGAL: every port is one-hot but some emitted residual is nonzero",
            "MALFORMED: every remaining integral state",
        ],
        "left_tile_table": TILE_A_TABLE,
        "left_tile_table_summary": summarize_table(TILE_A_TABLE),
        "instances": [unsat, control],
        "growth_audit": {
            "depth1_minimum_adverse_cost": adverse_depth1,
            "depth2_obstruction_minimum_cost": unsat_depth2,
            "lambda_illegal": f"{unsat_depth2}/{adverse_depth1}",
            "depth1_minimum_legal_cost": legal_depth1,
            "depth2_control_minimum_legal_cost": legal_depth2,
            "mu_legal": f"{legal_depth2}/{legal_depth1}",
            "lambda_strictly_greater_than_mu": Fraction(unsat_depth2, adverse_depth1) > Fraction(legal_depth2, legal_depth1),
        },
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

    # The anchor block 2I makes both emitted factors full column rank and gives
    # Q=4I+25 A^T A >= 4I.  The serialized coefficient interval is exhaustive.
    assert manifest["coefficient_bound_derivation"]["inclusive_integer_interval"] == [-2, 3]
    assert (2 * COEFFICIENT_MIN - 1) ** 2 <= 26
    assert (2 * COEFFICIENT_MAX - 1) ** 2 <= 26
    assert (2 * (COEFFICIENT_MIN - 1) - 1) ** 2 > 26
    assert (2 * (COEFFICIENT_MAX + 1) - 1) ** 2 > 26

    unsat, control = manifest["instances"]
    assert len(TILE_A_TABLE) == len(UNSAT_TILE_TABLE) == len(CONTROL_TILE_TABLE) == 20
    assert unsat["depth2_table_summary"] == {
        "entry_count": 8,
        "cost_histogram": {"57": 8},
        "class_histogram": {"ILLEGAL": 8},
        "class_minimum_cost": {"ILLEGAL": 57},
    }
    assert control["depth2_table_summary"] == {
        "entry_count": 7,
        "cost_histogram": {"32": 1, "57": 6},
        "class_histogram": {"ILLEGAL": 6, "LEGAL": 1},
        "class_minimum_cost": {"ILLEGAL": 57, "LEGAL": 32},
    }

    # Exact minima also follow without trusting enumeration: zero residual in
    # the obstruction equates all four ports, then its eight legality rows set
    # all coordinates to zero while normalization requires sum one.  Therefore
    # one integral residual (cost 25) is unavoidable above anchor baseline 32.
    # A common one-hot port attains 57.  The control's e_7 witness attains the
    # universal anchor lower bound 32.
    unsat_minimum = min(record["cost"] for record in unsat["depth2_table"])
    control_minimum = min(record["cost"] for record in control["depth2_table"])
    assert unsat_minimum == 57
    assert control_minimum == 32

    growth = manifest["growth_audit"]
    assert growth == {
        "depth1_minimum_adverse_cost": 32,
        "depth2_obstruction_minimum_cost": 57,
        "lambda_illegal": "57/32",
        "depth1_minimum_legal_cost": 16,
        "depth2_control_minimum_legal_cost": 32,
        "mu_legal": "32/16",
        "lambda_strictly_greater_than_mu": False,
    }

    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[1])),
        "lattice_rank": DEPTH2_DIMENSION,
        "ambient_dimension": unsat["ambient_dimension"],
        "coefficient_interval": [COEFFICIENT_MIN, COEFFICIENT_MAX],
        "left_tile_table": manifest["left_tile_table_summary"],
        "unsat_right_tile_table": unsat["right_tile_table_summary"],
        "control_right_tile_table": control["right_tile_table_summary"],
        "unsat_complete_depth2_table": unsat["depth2_table_summary"],
        "control_complete_depth2_table": control["depth2_table_summary"],
        "unsat_exact_minimum_squared": unsat_minimum,
        "control_exact_minimum_squared": control_minimum,
        "DROP_squared_cost": unsat["attack_audit"]["DROP_all_zero"]["total"],
        "G13_best_diagonal_squared_cost": unsat["attack_audit"]["G13_best_diagonal_breakdown"]["total"],
        "G19_best_diagonal_squared_cost": unsat["attack_audit"]["G19_best_diagonal_breakdown"]["total"],
        "growth_audit": growth,
        "finding": "the complete frozen table is closed through 57, but lambda=57/32 is smaller than mu=2",
        "scope": "finite failure of this serialized recursion rule; no asymptotic theorem",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
