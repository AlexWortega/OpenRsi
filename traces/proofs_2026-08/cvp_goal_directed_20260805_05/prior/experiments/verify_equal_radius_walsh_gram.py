#!/usr/bin/env python3
"""Generation-31 exact finite audit of an equal-radius discrepancy Gram.

For the Generation-11 degree-three selector checks A z=b, emit

    ||2z-1||^2 + ||Fz||^2 + 100||Az-b||^2,

where F is block diagonal with nine copies of the 8-by-8 Walsh matrix.  Thus
Q=4I+C^T C with C=[F;10A], and F^T F=8I.  Every one-hot global encoding has
the same discrepancy energy 144 before formula residuals.  The satisfiable
control has exact minimum 144.

The verifier exhausts the unrestricted obstruction shell through 192, the
four-thirds boundary.  Residual norm zero is handled by exact signed-state
moment DP; residual norm one is handled by complete low-base enumeration.
No vector occurs through 192, while a G11 affine parity has cost 216.  This is
finite evidence for this frozen Gram only, not a dimension-dependent lemma.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path

from sympy import Matrix

import verify_degree3_global_psd_metric as gen11
import verify_global_psd_metric as gen9

N_SELECTORS = 72
N_CLAUSES = 9
WALSH_SIZE = 8
RESIDUAL_SCALE = 10
CONTROL_RADIUS2 = 144
AUDIT_THRESHOLD2 = 192
STRICT_LOWER_BOUND2 = 193
ZERO_LOCAL_CAP2 = 64
DISCREPANCY_TRACE_BUDGET = 576
MANIFEST_PATH = Path(__file__).with_name("gen31_equal_radius_walsh_gram_manifest.json")

PATTERNS = gen9.PATTERNS
MONOMIALS = gen11.MONOMIALS


def walsh_entry(row, column):
    return -1 if ((row & column).bit_count() & 1) else 1


def build_walsh_rows():
    rows = []
    for clause in range(N_CLAUSES):
        for walsh_row in range(WALSH_SIZE):
            row = [0] * N_SELECTORS
            for pattern in range(WALSH_SIZE):
                row[8 * clause + pattern] = walsh_entry(walsh_row, pattern)
            rows.append(tuple(row))
    assert len(rows) == N_SELECTORS
    return tuple(rows)


def factor_and_target(checks):
    rows = []
    target = []
    for selector in range(N_SELECTORS):
        row = [0] * N_SELECTORS
        row[selector] = 2
        rows.append(tuple(row))
        target.append(1)
    rows.extend(build_walsh_rows())
    target.extend([0] * N_SELECTORS)
    for check in checks:
        rows.append(tuple(RESIDUAL_SCALE * value for value in check["coefficients"]))
        target.append(RESIDUAL_SCALE * check["rhs"])
    return tuple(rows), tuple(target)


def coordinate_energy(value):
    # (2z-1)^2 + 8z^2, using F^T F=8I.
    return 12 * value * value - 4 * value + 1


def base_energy(selector):
    return sum(coordinate_energy(value) for value in selector)


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


def verify_walsh_identity():
    rows = build_walsh_rows()[:WALSH_SIZE]
    gram = [[sum(rows[k][i] * rows[k][j] for k in range(WALSH_SIZE))
             for j in range(WALSH_SIZE)] for i in range(WALSH_SIZE)]
    assert gram == [[8 if i == j else 0 for j in range(8)] for i in range(8)]


def local_zero_states():
    """Every normalized/legal local state that can occur through 192."""
    states = []
    # The other eight normalized/legal blocks cost at least 16 each, so one
    # block costs at most 64.  Its other seven coordinates cost at least one;
    # coordinate_energy(z)<=57 forces z in [-2,2].
    for legal_values in product(range(-2, 3), repeat=7):
        block = (0,) + legal_values
        if sum(block) != 1:
            continue
        cost = sum(coordinate_energy(value) for value in block)
        if cost <= ZERO_LOCAL_CAP2:
            states.append((cost, block))
    states.sort()
    assert Counter(cost for cost, _ in states) == {16: 7, 40: 105, 64: 252}
    return tuple(states)


def global_state_record(clause, state):
    cost, block = state
    moments = {}
    for monomial in MONOMIALS:
        if all(variable in clause["variables"] for variable in monomial):
            moments[monomial] = sum(
                block[pattern_index] * gen9.monomial_value(clause, pattern, monomial)
                for pattern_index, pattern in enumerate(PATTERNS)
            )
    return cost, block, moments


def exact_zero_residual_shell(clauses):
    """Exact DP for every zero-residual vector of base cost at most 192."""
    states = local_zero_states()
    tables = [tuple(global_state_record(clause, state) for state in states) for clause in clauses]
    dp = {(None,) * len(MONOMIALS): (0, ())}
    layer_counts = []
    for table in tables:
        next_dp = {}
        for key, (cost, witness) in dp.items():
            for local_cost, block, moments in table:
                new_cost = cost + local_cost
                if new_cost > AUDIT_THRESHOLD2:
                    continue
                new_key = list(key)
                compatible = True
                for monomial, value in moments.items():
                    index = MONOMIALS.index(monomial)
                    if new_key[index] is None:
                        new_key[index] = value
                    elif new_key[index] != value:
                        compatible = False
                        break
                if not compatible:
                    continue
                new_key = tuple(new_key)
                old = next_dp.get(new_key)
                if old is None or new_cost < old[0]:
                    next_dp[new_key] = (new_cost, witness + (block,))
        dp = next_dp
        layer_counts.append(len(dp))
    assert not dp
    return {
        "local_state_count": len(states),
        "local_cost_histogram": {str(key): value for key, value in sorted(Counter(
            cost for cost, _ in states
        ).items())},
        "dynamic_program_layer_counts": layer_counts,
        "complete_final_state_count": 0,
    }


def exact_residual_one_shell(checks):
    """Enumerate every vector that could have residual square one through 192."""
    # Base energy is 72 plus coordinate extras.  Residual square one leaves
    # base <=92, hence extra <=20.  Values 1 and -1 cost extra 8 and 16;
    # every other nonzero value costs extra at least 40.  Therefore the list
    # below is complete: zero, one +1, one -1, or two +1 coordinates.
    candidates = [[0] * N_SELECTORS]
    for index in range(N_SELECTORS):
        positive = [0] * N_SELECTORS
        positive[index] = 1
        candidates.append(positive)
        negative = [0] * N_SELECTORS
        negative[index] = -1
        candidates.append(negative)
    for left, right in combinations(range(N_SELECTORS), 2):
        selector = [0] * N_SELECTORS
        selector[left] = selector[right] = 1
        candidates.append(selector)
    assert len(candidates) == 2701

    histogram = Counter()
    minimum_residual_squared = None
    minimizer = None
    for selector in candidates:
        assert base_energy(selector) <= 92
        raw = residual(checks, selector)
        residual_squared = sum(value * value for value in raw)
        histogram[residual_squared] += 1
        if minimum_residual_squared is None or residual_squared < minimum_residual_squared:
            minimum_residual_squared = residual_squared
            minimizer = selector
    assert minimum_residual_squared == 7
    return {
        "candidate_count": len(candidates),
        "minimum_raw_residual_squared": minimum_residual_squared,
        "minimum_witness": minimizer,
        "residual_squared_histogram": {str(key): value for key, value in sorted(histogram.items())},
    }


def parity_attack(clauses):
    selector = gen11.seven_term_attack(clauses, (1, 1, 0, 0), 1)
    return selector


def clause_drop_attack(clauses):
    selector, falsified = gen9.honest_selector(clauses, (0, 0, 0, 0))
    assert falsified == (0,)
    selector = list(selector)
    selector[:8] = [0] * 8
    return tuple(selector)


def instance_manifest(name, edges):
    clauses = gen9.clause_data(edges)
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
        "check_count": len(checks),
        "check_count_by_degree": {
            str(degree): count for degree, count in sorted(Counter(
                check["degree"] for check in checks
            ).items())
        },
        "checks": [{
            key: (list(value) if isinstance(value, tuple) else value)
            for key, value in check.items() if key != "coefficients"
        } | {"terms": gen11.sparse(check["coefficients"])} for check in checks],
        "lattice_rank": N_SELECTORS,
        "ambient_dimension": len(factor),
        "factor_rows": [gen11.sparse(row) for row in factor],
        "target": gen11.sparse(target),
        "factor_target_sha256": gen11.factor_hash(factor, target),
        "gram_upper_triangle": gen11.matrix_upper_sparse(gram),
        "linear_term": [int(value) for value in linear],
        "center": [gen11.rational_text(value) for value in center],
        "orthogonal_target_energy": gen11.rational_text(kappa),
        "certified_gram_eigenvalue_lower_bound": 12,
    }


def reconstruct_instance(record):
    clauses = gen9.clause_data(tuple(tuple(edge) for edge in record["edges"]))
    checks = gen11.build_checks(clauses)
    factor, target = factor_and_target(checks)
    assert gen11.factor_hash(factor, target) == record["factor_target_sha256"]
    assert [gen11.sparse(row) for row in factor] == record["factor_rows"]
    assert gen11.sparse(target) == record["target"]
    return clauses, checks, factor, target


def build_manifest():
    return {
        "schema": "gen31-equal-radius-walsh-gram-v1",
        "finite_claim_only": True,
        "selected_proposal": "Pro proposal 7: equal-radius discrepancy Gram search",
        "mechanism": "equal-norm discrepancy rows may charge signed affine selectors without a common syndrome",
        "expected_move": "obstruction squared distance strictly above four thirds of the control radius",
        "falsification_condition": "factor failure, control mismatch, or any unrestricted obstruction vector through 192",
        "template": {
            "coefficient_domain": "all integers",
            "external_filters": [],
            "objective": "||2z-1||^2+||Fz||^2+100||Az-b||^2",
            "gram_identity": "Q=4I+C^T C=12I+100 A^T A with C=[F;10A]",
            "walsh_rule": "nine block-diagonal copies of H_8",
            "discrepancy_trace_budget": DISCREPANCY_TRACE_BUDGET,
            "discrepancy_trace_realized": DISCREPANCY_TRACE_BUDGET,
            "residual_scale": RESIDUAL_SCALE,
            "frozen_before_shell_search": True,
        },
        "equal_radius_set": {
            "description": "all 16 globally consistent one-hot selector encodings before formula residual",
            "count": 16,
            "anchor_squared": 72,
            "walsh_squared": 72,
            "discrepancy_squared_radius": CONTROL_RADIUS2,
        },
        "control_exact_minimum_squared": CONTROL_RADIUS2,
        "audited_obstruction_shell_squared": AUDIT_THRESHOLD2,
        "certified_obstruction_lower_bound_squared": STRICT_LOWER_BOUND2,
        "certified_obstruction_upper_bound_squared": 216,
        "target_squared_ratio": "193/144",
        "strictly_above_four_thirds": 3 * STRICT_LOWER_BOUND2 > 4 * CONTROL_RADIUS2,
        "coefficient_bound": {
            "global_shell_argument": "base energy <=192 and the other 71 coordinates cost at least one, so 12z_i^2-4z_i+1<=121",
            "inclusive_interval": [-3, 3],
            "zero_residual_local_interval": [-2, 2],
        },
        "instances": [
            instance_manifest("generation7_obstruction", gen9.UNSAT_EDGES),
            instance_manifest("satisfiable_overlapping_control", gen9.CONTROL_EDGES),
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args()

    verify_walsh_identity()
    expected = build_manifest()
    if args.write_manifest:
        MANIFEST_PATH.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
        print(MANIFEST_PATH)
        return

    manifest = json.loads(MANIFEST_PATH.read_text())
    assert manifest == expected
    reconstructed = [reconstruct_instance(record) for record in manifest["instances"]]
    unsat_clauses, unsat_checks, unsat_factor, unsat_target = reconstructed[0]
    control_clauses, control_checks, _, _ = reconstructed[1]

    # All globally consistent one-hot encodings have discrepancy energy 144.
    for clauses in (unsat_clauses, control_clauses):
        for assignment in product((0, 1), repeat=4):
            selector, _ = gen9.honest_selector(clauses, assignment)
            assert base_energy(selector) == CONTROL_RADIUS2

    # A satisfying control encoding attains 144.  Any vector below 144 must
    # have zero residual because base>=72 and a residual costs 100.  Zero
    # residual enforces each block normalized/legal, whose integer minimum is
    # 16, proving the exact global lower bound 9*16=144.
    control_selector, falsified = gen9.honest_selector(control_clauses, (1, 1, 1, 0))
    assert not falsified
    assert objective_breakdown(control_checks, control_selector) == {
        "base_discrepancy": 144,
        "raw_residual_squared": 0,
        "total": 144,
    }

    zero_search = exact_zero_residual_shell(unsat_clauses)
    assert zero_search["dynamic_program_layer_counts"] == [364, 4030, 4103, 979, 153, 56, 13, 3, 0]
    residual_one_search = exact_residual_one_shell(unsat_checks)

    # Since base>=72, a vector through 192 has residual square zero or one.
    # Both branches above are exhaustive and empty, proving lower bound 193.
    assert residual_one_search["minimum_raw_residual_squared"] == 7
    assert manifest["strictly_above_four_thirds"]

    parity = parity_attack(unsat_clauses)
    parity_breakdown = objective_breakdown(unsat_checks, parity)
    assert parity_breakdown == {
        "base_discrepancy": 216,
        "raw_residual_squared": 0,
        "total": 216,
    }
    drop = clause_drop_attack(unsat_clauses)
    drop_breakdown = objective_breakdown(unsat_checks, drop)
    assert drop_breakdown == {
        "base_discrepancy": 136,
        "raw_residual_squared": 1,
        "total": 236,
    }

    # Check the exact emitted Gram identity and rational center data.
    B, t = Matrix(unsat_factor), Matrix(unsat_target)
    gram = B.T * B
    checks_matrix = Matrix([check["coefficients"] for check in unsat_checks])
    assert gram == 12 * Matrix.eye(N_SELECTORS) + 100 * checks_matrix.T * checks_matrix
    assert manifest["instances"][0]["certified_gram_eigenvalue_lower_bound"] == 12

    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[1])),
        "lattice_rank": N_SELECTORS,
        "ambient_dimension": len(unsat_factor),
        "equal_discrepancy_radius_squared": CONTROL_RADIUS2,
        "control_exact_unrestricted_minimum_squared": CONTROL_RADIUS2,
        "audited_obstruction_shell_squared": AUDIT_THRESHOLD2,
        "certified_obstruction_lower_bound_squared": STRICT_LOWER_BOUND2,
        "certified_obstruction_upper_bound_squared": parity_breakdown["total"],
        "certified_squared_ratio_lower_bound": "193/144",
        "coefficient_interval": manifest["coefficient_bound"]["inclusive_interval"],
        "zero_residual_shell_search": zero_search,
        "residual_one_shell_search": residual_one_search,
        "G13_G11_parity_breakdown": parity_breakdown,
        "clause_drop_breakdown": drop_breakdown,
        "finding": "no unrestricted obstruction vector exists through 192 while the control exact minimum is 144",
        "scope": "finite pass for this frozen rational Gram; no composition or asymptotic gap claim",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
