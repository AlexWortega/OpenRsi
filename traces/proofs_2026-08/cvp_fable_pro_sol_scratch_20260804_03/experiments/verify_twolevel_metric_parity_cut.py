#!/usr/bin/env python3
"""Generation-37 exact first cutting plane for repaired metric synthesis.

Freeze the G31/G32 incidence feature family with one composition rule:
copy-local anchor and Walsh blocks are orthogonal, and every within/cross-copy
moment discrepancy is an emitted residual feature.  Let anchor/Walsh weights
alpha,beta be nonnegative with 72(alpha+beta)=1; residual rows retain weight
100.  This gives legal squared radii 1 and 2 and Q >= I/18.

For every metric in this rational family, the one-copy G11/G13 parity witness
has cost 96 alpha+120 beta.  Two compatible copies have zero cross residual
and cost 192 alpha+240 beta, exactly twice the fixed one-copy witness.  Hence
the first exact separation cut is delta<=0 and no strict two-level margin is
possible.  A rational feasible factor at alpha=beta=1/144 is fully emitted.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import verify_crosscopy_walsh_composition as gen32
import verify_equal_radius_walsh_gram as gen31
import verify_global_psd_metric as gen9

ALPHA = Fraction(1, 144)
BETA = Fraction(1, 144)
RESIDUAL_WEIGHT = 100
ONE_RANK = 72
TWO_RANK = 144
MANIFEST_PATH = Path(__file__).with_name("gen37_twolevel_metric_parity_cut_manifest.json")


def fraction_text(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def sparse_fraction(row):
    return [[index, fraction_text(value)] for index, value in enumerate(row) if value]


def normalized_factor(checks, clause_count):
    rank = 8 * clause_count
    rows = []
    target = []
    # sqrt(alpha)=sqrt(beta)=1/12 is rational.
    for index in range(rank):
        row = [Fraction(0)] * rank
        row[index] = Fraction(1, 6)  # (1/12)*2
        rows.append(tuple(row))
        target.append(Fraction(1, 12))
    for clause in range(clause_count):
        for walsh_row in range(8):
            row = [Fraction(0)] * rank
            for pattern in range(8):
                row[8 * clause + pattern] = Fraction(gen31.walsh_entry(walsh_row, pattern), 12)
            rows.append(tuple(row))
            target.append(Fraction(0))
    for check in checks:
        rows.append(tuple(Fraction(10 * value) for value in check["coefficients"]))
        target.append(Fraction(10 * check["rhs"]))
    return tuple(rows), tuple(target)


def factor_hash(factor, target):
    payload = {
        "factor_rows": [sparse_fraction(row) for row in factor],
        "target": [fraction_text(value) for value in target],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def emit_factor_record(name, checks, clause_count):
    factor, target = normalized_factor(checks, clause_count)
    return {
        "name": name,
        "lattice_rank": 8 * clause_count,
        "ambient_dimension": len(factor),
        "factor_rows": [sparse_fraction(row) for row in factor],
        "target": [fraction_text(value) for value in target],
        "factor_target_sha256": factor_hash(factor, target),
        "factor_rule": "(1/12)[2I;F] plus residual block 10A",
        "gram_eigenvalue_lower_bound": "1/12",
    }


def raw_components(checks, selector):
    anchor = sum((2 * value - 1) ** 2 for value in selector)
    walsh = 8 * sum(value * value for value in selector)
    raw = gen31.residual(checks, selector) if len(selector) == 72 else gen32.residual(checks, selector)
    return {
        "anchor": anchor,
        "walsh": walsh,
        "raw_residual_squared": sum(value * value for value in raw),
    }


def selected_cost(components):
    return (
        ALPHA * components["anchor"]
        + BETA * components["walsh"]
        + RESIDUAL_WEIGHT * components["raw_residual_squared"]
    )


def one_copy_data(edges):
    clauses = gen9.clause_data(edges)
    checks = gen31.gen11.build_checks(clauses)
    return clauses, checks


def honest_onecopy(clauses, assignment):
    selector, falsified = gen9.honest_selector(clauses, assignment)
    return selector, falsified


def family_trace_upper_bound(two_checks):
    # For 72(alpha+beta)=1, 4alpha+8beta<=1/9, so the base
    # trace on rank 144 is <=16.  The residual trace is
    # 100*sum ||row||^2.  Since Q is PSD, lambda_max(Q)<=trace(Q).
    residual_row_norm_sum = sum(
        sum(value * value for value in check["coefficients"])
        for check in two_checks
    )
    return 16 + 100 * residual_row_norm_sum, residual_row_norm_sum


def evaluate_witnesses():
    unsat_clauses, unsat_checks = one_copy_data(gen9.UNSAT_EDGES)
    control_clauses, control_checks = one_copy_data(gen9.CONTROL_EDGES)
    source = json.loads(gen32.MANIFEST_PATH.read_text())
    assert source["one_copy_search"]["exact_minimum_squared"] == 216
    one_parity = tuple(source["one_copy_search"]["selector"])
    one_control, falsified = honest_onecopy(control_clauses, (1, 1, 1, 0))
    assert not falsified

    two_unsat_clauses = gen32.build_union_clauses(gen9.UNSAT_EDGES)
    two_unsat_checks = gen32.build_checks(two_unsat_clauses)
    two_control_clauses = gen32.build_union_clauses(gen9.CONTROL_EDGES)
    two_control_checks = gen32.build_checks(two_control_clauses)
    two_parity = gen32.mapped_parity_witness(two_unsat_clauses)
    assignment = {0: 1, 1: 1, 2: 1, 3: 0, 4: 1, 5: 0}
    two_control, falsified = gen32.honest_selector(two_control_clauses, assignment)
    assert not falsified

    records = {}
    for name, checks, selector in (
        ("one_copy_control", control_checks, one_control),
        ("one_copy_parity", unsat_checks, one_parity),
        ("two_copy_control", two_control_checks, two_control),
        ("two_copy_compatible_parity", two_unsat_checks, two_parity),
    ):
        components = raw_components(checks, selector)
        records[name] = {
            "components": components,
            "selected_metric_squared_cost": fraction_text(selected_cost(components)),
            "selector": list(selector),
        }

    assert records["one_copy_control"]["components"] == {
        "anchor": 72, "walsh": 72, "raw_residual_squared": 0,
    }
    assert records["one_copy_parity"]["components"] == {
        "anchor": 96, "walsh": 120, "raw_residual_squared": 0,
    }
    assert records["two_copy_control"]["components"] == {
        "anchor": 144, "walsh": 144, "raw_residual_squared": 0,
    }
    assert records["two_copy_compatible_parity"]["components"] == {
        "anchor": 192, "walsh": 240, "raw_residual_squared": 0,
    }
    # Exact selected-metric minima for the controls and one-copy obstruction:
    # a nonzero integral residual costs at least 100. At zero residual each
    # normalized/legal block has unscaled anchor+Walsh cost at least 16.
    # Thus controls cost at least 9*16/144=1 and 18*16/144=2. For the
    # obstruction, G32's exact search gives zero-residual base at least 216,
    # while every nonzero-residual state costs over 100, proving 3/2 exactly.
    assert min(cost for cost, _ in gen32.one_copy_local_states()) == 16
    return records, (
        unsat_checks, control_checks, two_unsat_checks, two_control_checks
    )


def build_manifest():
    witnesses, checks = evaluate_witnesses()
    unsat_checks, control_checks, two_unsat_checks, two_control_checks = checks
    upper_bound, residual_norm_sum = family_trace_upper_bound(two_unsat_checks)
    return {
        "schema": "gen37-twolevel-incidence-metric-parity-cut-v1",
        "finite_claim_only": True,
        "selected_proposal": "repaired Pro proposal 6: adversarial two-level Voronoi metric synthesis",
        "feature_family": {
            "composition_rule": "orthogonal copy-local anchor/Walsh blocks plus all emitted within/cross-copy moment residual rows",
            "parameters": "alpha,beta>=0, 72(alpha+beta)=1; residual squared weight fixed at 100",
            "legal_squared_radii": ["1", "2"],
            "uniform_eigenvalue_lower_bound": "1/18",
            "uniform_eigenvalue_upper_bound_M": str(upper_bound),
            "two_copy_residual_row_norm_squared_sum": residual_norm_sum,
            "coefficient_domain": "all integers",
            "external_filters": [],
        },
        "fixed_valid_onecopy_adverse_witness_cost": "96*alpha+120*beta",
        "compatible_twocopy_witness_cost": "192*alpha+240*beta",
        "exact_cutting_plane": "delta <= (192*alpha+240*beta)-2*(96*alpha+120*beta) = 0",
        "optimized_margin_upper_bound": "0",
        "strict_positive_margin_possible": False,
        "selected_rational_metric": {
            "alpha": fraction_text(ALPHA),
            "beta": fraction_text(BETA),
            "residual_squared_weight": RESIDUAL_WEIGHT,
            "one_copy_control_exact_minimum_squared": "1",
            "one_copy_obstruction_exact_minimum_squared": "3/2",
            "two_copy_control_exact_minimum_squared": "2",
            "two_copy_compatible_parity_squared_cost": "3",
            "one_copy_coefficient_interval_through_3/2": [-3, 3],
            "two_copy_coefficient_interval_through_3": [-4, 5],
        },
        "witnesses": witnesses,
        "factors": [
            emit_factor_record("one_copy_obstruction", unsat_checks, 9),
            emit_factor_record("one_copy_control", control_checks, 9),
            emit_factor_record("two_copy_obstruction", two_unsat_checks, 18),
            emit_factor_record("two_copy_control", two_control_checks, 18),
        ],
        "finding": "the compatible parity is an exact universal cut delta<=0 for the entire normalized feature family",
        "scope": "finite kill of this frozen orthogonal incidence-orbit metric family",
    }


def evaluate_factor(factor_record, selector):
    total = Fraction(0)
    for row_terms, target_text in zip(factor_record["factor_rows"], factor_record["target"]):
        target = Fraction(target_text)
        value = sum(Fraction(coefficient) * selector[index] for index, coefficient in row_terms)
        total += (value - target) ** 2
    return total


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
    assert manifest["optimized_margin_upper_bound"] == "0"
    assert not manifest["strict_positive_margin_possible"]

    factor_by_name = {record["name"]: record for record in manifest["factors"]}
    for witness_name, factor_name in (
        ("one_copy_control", "one_copy_control"),
        ("one_copy_parity", "one_copy_obstruction"),
        ("two_copy_control", "two_copy_control"),
        ("two_copy_compatible_parity", "two_copy_obstruction"),
    ):
        witness = manifest["witnesses"][witness_name]
        exact = evaluate_factor(factor_by_name[factor_name], witness["selector"])
        assert fraction_text(exact) == witness["selected_metric_squared_cost"]

    assert manifest["witnesses"]["one_copy_control"]["selected_metric_squared_cost"] == "1"
    assert manifest["witnesses"]["one_copy_parity"]["selected_metric_squared_cost"] == "3/2"
    assert manifest["witnesses"]["two_copy_control"]["selected_metric_squared_cost"] == "2"
    assert manifest["witnesses"]["two_copy_compatible_parity"]["selected_metric_squared_cost"] == "3"

    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[1])),
        "legal_squared_radii": manifest["feature_family"]["legal_squared_radii"],
        "uniform_eigenvalue_bounds": [
            manifest["feature_family"]["uniform_eigenvalue_lower_bound"],
            manifest["feature_family"]["uniform_eigenvalue_upper_bound_M"],
        ],
        "one_copy_adverse_cost": manifest["witnesses"]["one_copy_parity"]["selected_metric_squared_cost"],
        "two_copy_parity_cost": manifest["witnesses"]["two_copy_compatible_parity"]["selected_metric_squared_cost"],
        "exact_cutting_plane": manifest["exact_cutting_plane"],
        "optimized_margin_upper_bound": manifest["optimized_margin_upper_bound"],
        "strict_positive_margin_possible": manifest["strict_positive_margin_possible"],
        "finding": manifest["finding"],
        "scope": manifest["scope"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
