#!/usr/bin/env python3
"""Generation-7 unrestricted audit of the selected multi-order radix barrier.

The finite formula is the nine-clause, four-variable edge-cover obstruction
from the Generation-6 review.  Each clause is falsified by the two endpoints
of one listed hypercube edge.  There are eight integral truth-table selector
coefficients per clause.

For selector vector z, the emitted lattice and single target realize

    ||2z-1||^2 + ||Az-b||^2 + ||R(Az-b)||^2,

where A includes every normalization, false-label legality, and occurrence-
consistency row.  R consists of all cyclic base-33 orders of those residuals.
There are no carries, slacks, coefficient filters, or changing targets.

The completeness squared radius is 72, the number of selector anchors.  The
anchor bound itself implies that every vector through that radius is Boolean,
so the bounded CVP audit is unrestricted.  The verifier also performs exact
low-weight search for an integral zero-residual pseudoassignment.  It finds
one at squared distance 80, proving that radix weighting cannot amplify this
exact kernel.  These are finite facts, not an asymptotic theorem.
"""

from __future__ import annotations

import argparse
import hashlib
from itertools import product
import json
from pathlib import Path

from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form

RADIX = 33
PATTERNS = tuple(product((0, 1), repeat=3))
EDGES = (
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
N_CLAUSES = len(EDGES)
N_SELECTORS = N_CLAUSES * len(PATTERNS)
COMPLETENESS_RADIUS2 = N_SELECTORS
WITNESS_RADIUS2 = COMPLETENESS_RADIUS2 + 8
MANIFEST_PATH = Path(__file__).with_name("gen7_multiorder_radix_manifest.json")


def bits(text):
    return tuple(int(value) for value in text)


def clause_data():
    clauses = []
    for left_text, right_text in EDGES:
        left, right = bits(left_text), bits(right_text)
        differing = [i for i in range(4) if left[i] != right[i]]
        assert len(differing) == 1
        omitted = differing[0]
        variables = tuple(i for i in range(4) if i != omitted)
        false_bits = tuple(left[i] for i in variables)
        clauses.append({
            "edge": [left_text, right_text],
            "omitted_variable": omitted,
            "variables": variables,
            "false_bits": false_bits,
        })
    return tuple(clauses)


CLAUSES = clause_data()


def selector_index(clause_index, pattern_index):
    return 8 * clause_index + pattern_index


def sparse(vector):
    return [[i, int(value)] for i, value in enumerate(vector) if value]


def global_bit_coefficient(clause, local_position, pattern):
    """Coefficient of this selector in the indicated global-bit marginal."""
    return pattern[local_position] ^ clause["false_bits"][local_position]


def build_checks():
    """Return semantic check records and the exact integer pair (A,b)."""
    checks = []

    for clause_index, clause in enumerate(CLAUSES):
        row = [0] * N_SELECTORS
        for pattern_index in range(8):
            row[selector_index(clause_index, pattern_index)] = 1
        checks.append({
            "kind": "normalization",
            "clause": clause_index,
            "coefficients": tuple(row),
            "rhs": 1,
        })

    for clause_index, clause in enumerate(CLAUSES):
        row = [0] * N_SELECTORS
        row[selector_index(clause_index, 0)] = 1
        checks.append({
            "kind": "legality",
            "clause": clause_index,
            "local_pattern": [0, 0, 0],
            "coefficients": tuple(row),
            "rhs": 0,
        })

    occurrences = {variable: [] for variable in range(4)}
    for clause_index, clause in enumerate(CLAUSES):
        for local_position, variable in enumerate(clause["variables"]):
            occurrences[variable].append((clause_index, local_position))

    for variable in range(4):
        reference_clause, reference_position = occurrences[variable][0]
        reference = CLAUSES[reference_clause]
        for clause_index, local_position in occurrences[variable][1:]:
            clause = CLAUSES[clause_index]
            row = [0] * N_SELECTORS
            for pattern_index, pattern in enumerate(PATTERNS):
                row[selector_index(clause_index, pattern_index)] += (
                    global_bit_coefficient(clause, local_position, pattern)
                )
                row[selector_index(reference_clause, pattern_index)] -= (
                    global_bit_coefficient(reference, reference_position, pattern)
                )
            checks.append({
                "kind": "occurrence_consistency",
                "variable": variable,
                "clause": clause_index,
                "local_position": local_position,
                "reference_clause": reference_clause,
                "reference_local_position": reference_position,
                "coefficients": tuple(row),
                "rhs": 0,
            })

    rows = [record["coefficients"] for record in checks]
    rhs = [record["rhs"] for record in checks]
    return checks, rows, rhs


def radix_matrix(number_of_checks):
    """Every cyclic order; each check is the leading digit in one row."""
    rows = []
    orders = []
    for shift in range(number_of_checks):
        order = tuple((shift + position) % number_of_checks
                      for position in range(number_of_checks))
        row = [0] * number_of_checks
        for position, check_index in enumerate(order):
            row[check_index] = RADIX ** (number_of_checks - 1 - position)
        rows.append(tuple(row))
        orders.append(order)
    return tuple(rows), tuple(orders)


def mat_vec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def mat_mul(left, right):
    columns = tuple(zip(*right))
    return [[sum(a * b for a, b in zip(row, column)) for column in columns]
            for row in left]


def semantic_basis_and_target():
    checks, check_rows, rhs = build_checks()
    radix_rows, orders = radix_matrix(len(checks))
    radix_check_rows = mat_mul(radix_rows, check_rows)
    radix_rhs = mat_vec(radix_rows, rhs)

    dimension = N_SELECTORS + 2 * len(checks)
    columns = []
    for selector in range(N_SELECTORS):
        column = [0] * dimension
        column[selector] = 2
        for check_index, row in enumerate(check_rows):
            column[N_SELECTORS + check_index] = row[selector]
        for radix_index, row in enumerate(radix_check_rows):
            column[N_SELECTORS + len(checks) + radix_index] = row[selector]
        columns.append(tuple(column))

    target = [1] * N_SELECTORS + list(rhs) + radix_rhs
    return checks, radix_rows, orders, tuple(columns), tuple(target)


def basis_sha256(columns, target):
    payload = {"columns": [sparse(column) for column in columns], "target": sparse(target)}
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def canonical_hnf_sha256(columns):
    basis = Matrix.hstack(*(Matrix(column) for column in columns))
    hnf = hermite_normal_form(basis)
    assert hnf.shape == basis.shape
    payload = [[int(hnf[row, column]) for column in range(hnf.cols)]
               for row in range(hnf.rows)]
    return hashlib.sha256(
        json.dumps(payload, separators=(",", ":")).encode()
    ).hexdigest(), hnf


def build_manifest(include_hnf=True):
    checks, radix_rows, orders, columns, target = semantic_basis_and_target()
    hnf_hash = canonical_hnf_sha256(columns)[0] if include_hnf else None
    return {
        "schema": "gen7-multiorder-radix-v1",
        "finite_instance": "nine 3-clauses on four variables defined by falsification edges",
        "falsification_edges": [list(edge) for edge in EDGES],
        "radix": RADIX,
        "selector_count": N_SELECTORS,
        "check_count": len(checks),
        "ambient_dimension": len(target),
        "lattice_rank": len(columns),
        "completeness_squared_radius": COMPLETENESS_RADIUS2,
        "coordinates": {
            "anchors": [0, N_SELECTORS],
            "raw_residuals": [N_SELECTORS, N_SELECTORS + len(checks)],
            "cyclic_radix_residuals": [N_SELECTORS + len(checks), len(target)],
        },
        "selectors": [{
            "index": selector_index(clause_index, pattern_index),
            "clause": clause_index,
            "local_pattern": list(pattern),
            "legal": pattern != (0, 0, 0),
        } for clause_index in range(N_CLAUSES)
          for pattern_index, pattern in enumerate(PATTERNS)],
        "checks": [{
            key: (list(value) if isinstance(value, tuple) else value)
            for key, value in record.items() if key != "coefficients"
        } | {"terms": sparse(record["coefficients"])} for record in checks],
        "radix_orders": [{
            "row": row_index,
            "check_order_high_to_low": list(order),
            "weights_high_to_low": [RADIX ** exponent
                                     for exponent in range(len(checks) - 1, -1, -1)],
        } for row_index, order in enumerate(orders)],
        "basis_columns": [{"index": index, "entries": sparse(column)}
                          for index, column in enumerate(columns)],
        "target": sparse(target),
        "basis_target_sha256": basis_sha256(columns, target),
        "canonical_column_hnf_sha256": hnf_hash,
        "slack_coordinates": [],
        "carry_coordinates": [],
        "external_constraints": [],
    }


def reconstruct_manifest_basis(manifest):
    dimension = manifest["ambient_dimension"]
    columns = []
    for expected_index, record in enumerate(manifest["basis_columns"]):
        assert record["index"] == expected_index
        column = [0] * dimension
        for row, value in record["entries"]:
            assert column[row] == 0
            column[row] = value
        columns.append(tuple(column))
    target = [0] * dimension
    for row, value in manifest["target"]:
        assert target[row] == 0
        target[row] = value
    return tuple(columns), tuple(target)


def residual(checks, selector):
    return tuple(sum(a * z for a, z in zip(record["coefficients"], selector))
                 - record["rhs"] for record in checks)


def squared_distance(columns, target, coefficients):
    point = [0] * len(target)
    for coefficient, column in zip(coefficients, columns):
        if coefficient:
            for row, value in enumerate(column):
                point[row] += coefficient * value
    return sum((value - wanted) ** 2 for value, wanted in zip(point, target))


def honest_selector(assignment):
    selector = [0] * N_SELECTORS
    falsified = []
    for clause_index, clause in enumerate(CLAUSES):
        local_pattern = tuple(
            assignment[variable] ^ clause["false_bits"][local_position]
            for local_position, variable in enumerate(clause["variables"])
        )
        pattern_index = PATTERNS.index(local_pattern)
        selector[selector_index(clause_index, pattern_index)] = 1
        if pattern_index == 0:
            falsified.append(clause_index)
    return tuple(selector), tuple(falsified)


def low_weight_zero_residual_search(checks):
    """Exact search through anchor energy 80, with bounds derived from it."""
    # Relative to the unavoidable one unit per anchor, a coefficient z costs
    # (2z-1)^2-1 = 4z(z-1).  A total budget of eight therefore forces every
    # coefficient into {-1,0,1,2}; this is a consequence, not a search box.
    local_states = []
    for legal_values in product((-1, 0, 1, 2), repeat=7):
        block = (0,) + legal_values
        extra = sum((2 * value - 1) ** 2 - 1 for value in block)
        if extra > WITNESS_RADIUS2 - COMPLETENESS_RADIUS2 or sum(block) != 1:
            continue
        literal_marginals = tuple(
            sum(block[pattern_index] * PATTERNS[pattern_index][position]
                for pattern_index in range(8))
            for position in range(3)
        )
        local_states.append((extra, block, literal_marginals))

    # For each clause and partial four-variable marginal, retain every
    # minimum-extra block.  Enumerating the derived marginal values then
    # exactly joins all occurrence-consistency constraints.
    tables = []
    marginal_values = [set() for _ in range(4)]
    for clause in CLAUSES:
        table = {}
        for extra, block, literal_marginals in local_states:
            global_marginals = tuple(
                literal_marginals[position] if false_bit == 0
                else 1 - literal_marginals[position]
                for position, false_bit in enumerate(clause["false_bits"])
            )
            key = global_marginals
            old = table.get(key)
            if old is None or extra < old[0]:
                table[key] = (extra, block)
            for variable, value in zip(clause["variables"], global_marginals):
                marginal_values[variable].add(value)
        tables.append(table)

    minimum_extra = None
    witness = None
    feasible_marginals = 0
    for global_marginals in product(*(sorted(values) for values in marginal_values)):
        total_extra = 0
        blocks = []
        for clause, table in zip(CLAUSES, tables):
            key = tuple(global_marginals[variable] for variable in clause["variables"])
            record = table.get(key)
            if record is None:
                break
            total_extra += record[0]
            blocks.append(record[1])
        else:
            if total_extra <= WITNESS_RADIUS2 - COMPLETENESS_RADIUS2:
                feasible_marginals += 1
                if minimum_extra is None or total_extra < minimum_extra:
                    minimum_extra = total_extra
                    witness = (global_marginals, tuple(value for block in blocks for value in block))

    assert witness is not None
    global_marginals, selector = witness
    assert minimum_extra == 8
    assert not any(residual(checks, selector))
    return {
        "local_states_checked": len(local_states),
        "derived_marginal_values": [sorted(values) for values in marginal_values],
        "feasible_global_marginals_through_extra_8": feasible_marginals,
        "minimum_zero_residual_anchor_extra": minimum_extra,
        "global_marginals": list(global_marginals),
        "selector": list(selector),
    }


def check_no_carry_bound_for_boolean_residuals(checks, radix_rows):
    """Derive the digit bound used below from all Boolean check rows."""
    bounds = []
    for record in checks:
        positive = sum(value for value in record["coefficients"] if value > 0)
        negative = -sum(value for value in record["coefficients"] if value < 0)
        bounds.append(max(abs(-negative - record["rhs"]),
                          abs(positive - record["rhs"])))
    digit_bound = max(bounds)
    assert digit_bound == 7
    assert all(
        digit_bound * (RADIX ** exponent - 1) // (RADIX - 1) < RADIX ** exponent
        for exponent in range(len(checks))
    )

    # Any nonzero bounded digit vector has a highest nonzero base-33 digit in
    # every cyclic order; lower digits cannot cancel it.  Hence all 41 radix
    # coordinates are nonzero.  The inequality above is the exhaustive
    # symbolic bound, independent of a coefficient box.
    assert len(radix_rows) == len(checks)
    return digit_bound


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args()

    expected = build_manifest(include_hnf=True)
    if args.write_manifest:
        MANIFEST_PATH.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
        print(MANIFEST_PATH)
        return

    manifest = json.loads(MANIFEST_PATH.read_text())
    assert manifest == expected
    emitted_columns, emitted_target = reconstruct_manifest_basis(manifest)
    checks, radix_rows, orders, semantic_columns, semantic_target = semantic_basis_and_target()
    assert emitted_columns == semantic_columns
    assert emitted_target == semantic_target
    assert basis_sha256(emitted_columns, emitted_target) == manifest["basis_target_sha256"]

    semantic_hnf_hash, semantic_hnf = canonical_hnf_sha256(semantic_columns)
    emitted_hnf_hash, emitted_hnf = canonical_hnf_sha256(emitted_columns)
    assert semantic_hnf == emitted_hnf
    assert semantic_hnf_hash == emitted_hnf_hash == manifest["canonical_column_hnf_sha256"]
    assert semantic_hnf.rank() == N_SELECTORS

    # The nine falsification edges cover all assignments, exactly certifying
    # unsatisfiability of this finite formula.  Multiple assignments are
    # checked, but all distances use the one emitted target above.
    coverage = {}
    for assignment in product((0, 1), repeat=4):
        _, falsified = honest_selector(assignment)
        assert falsified
        coverage["".join(map(str, assignment))] = list(falsified)
    assert len(coverage) == 16

    # Exact unrestricted CVP through radius^2=72: each anchor contributes at
    # least one for every integer coefficient.  Equality forces z in {0,1}^72.
    # With no residual budget, Az=b.  Binary normalization gives one label per
    # clause, legality excludes 000, and consistency gives one global Boolean
    # assignment, contradicted by the exhaustive 16-assignment edge coverage.
    assert all((2 * value - 1) ** 2 >= 1 for value in range(-10, 11))
    digit_bound = check_no_carry_bound_for_boolean_residuals(checks, radix_rows)

    attack = low_weight_zero_residual_search(checks)
    attack_selector = tuple(attack["selector"])
    attack_distance2 = squared_distance(emitted_columns, emitted_target, attack_selector)
    assert attack_distance2 == WITNESS_RADIUS2

    # This also proves the exact unrestricted CVP minimum is 80.  Below 80,
    # anchor energy is either 72 or at least 80 because every anchor excess is
    # a nonnegative multiple of eight.  In the first case z is Boolean.  A
    # nonzero residual then has all 41 radix coordinates nonzero by the
    # derived digit bound, so its squared distance is at least 72+1+41>80;
    # a zero residual would be a satisfying assignment, which coverage rules
    # out.  The displayed zero-residual witness attains 80.
    assert COMPLETENESS_RADIUS2 + 1 + len(checks) > WITNESS_RADIUS2

    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[1])),
        "basis_target_sha256": manifest["basis_target_sha256"],
        "canonical_column_hnf_sha256": semantic_hnf_hash,
        "falsification_edges": len(EDGES),
        "covered_assignments": len(coverage),
        "selector_coordinates": N_SELECTORS,
        "raw_checks": len(checks),
        "cyclic_radix_rows": len(orders),
        "ambient_dimension": len(emitted_target),
        "lattice_rank": N_SELECTORS,
        "radix": RADIX,
        "derived_boolean_residual_digit_bound": digit_bound,
        "completeness_squared_radius": COMPLETENESS_RADIUS2,
        "exact_unrestricted_cvp_minimum_squared": attack_distance2,
        "zero_residual_attack": attack,
        "finding": "an exact signed-selector kernel has squared distance 80, so every base-33 radix residual is zero and the mutation is killed at finite size",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
