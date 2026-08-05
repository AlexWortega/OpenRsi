#!/usr/bin/env python3
"""Generation-19 exact audit of a width-5 Barrington flow lattice.

A deterministic balanced AND/OR formula is compiled to a width-5 permutation
branching program.  The emitted integer variables are transition-edge flows
and four shared query values.  Source, sink=ACCEPT, conservation, and repeated
query consistency are all fixed-target lattice rows.  Constant permutation
layers use five edges; queried layers use ten.

The objective is ||2z-1||^2 + 25||Az-b||^2.  A certified dynamic program over
the exact anchor shell finds a zero-residual accepting signed flow for the
unsatisfiable nine-clause instance with anchor excess 16.  It exhausts all
integer vectors with smaller anchor excess.  Since any nonzero integral
residual costs at least 25, this also gives the exact unrestricted CVP minimum.
These are finite-instance facts only.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from itertools import permutations, product
import hashlib
import json
from pathlib import Path

import verify_global_psd_metric as gen9

WIDTH = 5
N_VARIABLES = 4
ANCHOR_SCALE = 2
RESIDUAL_SCALE = 5
MANIFEST_PATH = Path(__file__).with_name("gen19_barrington_signed_flow_manifest.json")
IDENTITY = tuple(range(WIDTH))


def compose(first, second):
    """Permutation obtained by applying first and then second."""
    return tuple(second[first[state]] for state in range(WIDTH))


def inverse(permutation):
    result = [0] * WIDTH
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def is_five_cycle(permutation):
    seen = []
    state = 0
    for _ in range(WIDTH):
        seen.append(state)
        state = permutation[state]
    return state == 0 and len(set(seen)) == WIDTH


FIVE_CYCLES = tuple(
    permutation for permutation in permutations(range(WIDTH))
    if is_five_cycle(permutation)
)
TARGET_PERMUTATION = FIVE_CYCLES[0]
ACCEPT_STATE = TARGET_PERMUTATION[0]
START_STATE = 0


def commutator(first, second):
    return compose(compose(compose(first, second), inverse(first)), inverse(second))


@lru_cache(None)
def commutator_pair(target):
    for first in FIVE_CYCLES:
        for second in FIVE_CYCLES:
            if commutator(first, second) == target:
                return first, second
    raise AssertionError("no deterministic commutator pair")


def literal(variable, positive):
    return ("literal", variable, bool(positive))


def negate(formula):
    return ("not", formula)


def conjunction(left, right):
    return ("and", left, right)


def disjunction(left, right):
    return negate(conjunction(negate(left), negate(right)))


def balanced(operator, formulas):
    formulas = list(formulas)
    while len(formulas) > 1:
        next_level = []
        for index in range(0, len(formulas), 2):
            if index + 1 == len(formulas):
                next_level.append(formulas[index])
            else:
                next_level.append(operator(formulas[index], formulas[index + 1]))
        formulas = next_level
    return formulas[0]


def cnf_formula(edges):
    clauses = gen9.clause_data(edges)
    formulas = []
    for clause in clauses:
        literals = [
            literal(variable, clause["false_bits"][position] == 0)
            for position, variable in enumerate(clause["variables"])
        ]
        formulas.append(balanced(disjunction, literals))
    return balanced(conjunction, formulas)


def inverse_program(program):
    return tuple(
        (variable, inverse(zero), inverse(one))
        for variable, zero, one in reversed(program)
    )


def compile_formula(formula, target):
    kind = formula[0]
    if kind == "literal":
        _, variable, positive = formula
        return ((variable, IDENTITY, target),) if positive else ((variable, target, IDENTITY),)
    if kind == "not":
        program = compile_formula(formula[1], inverse(target))
        # Same permutation on both branches is a constant layer.
        return program + ((-1, target, target),)
    if kind == "and":
        first_target, second_target = commutator_pair(target)
        first = compile_formula(formula[1], first_target)
        second = compile_formula(formula[2], second_target)
        return first + second + inverse_program(first) + inverse_program(second)
    raise AssertionError(kind)


def build_program(edges):
    program = compile_formula(cnf_formula(edges), TARGET_PERMUTATION)
    assert len(program) == 3250
    assert Counter(variable == -1 for variable, _, _ in program) == {False: 1300, True: 1950}
    return program


def evaluate_program(program, assignment):
    state = START_STATE
    for variable, zero, one in program:
        permutation = one if variable == -1 or assignment[variable] else zero
        state = permutation[state]
    return state


def formula_satisfied(edges, assignment):
    clauses = gen9.clause_data(edges)
    return not gen9.honest_selector(clauses, assignment)[1]


def validate_program(program, edges):
    outputs = {}
    for assignment in product((0, 1), repeat=N_VARIABLES):
        state = evaluate_program(program, assignment)
        satisfied = formula_satisfied(edges, assignment)
        assert state == (ACCEPT_STATE if satisfied else START_STATE)
        outputs["".join(map(str, assignment))] = state
    return outputs


def build_layout(program):
    layers = []
    offset = 0
    for index, (variable, zero, one) in enumerate(program):
        constant = variable == -1
        size = WIDTH if constant else 2 * WIDTH
        layers.append({
            "index": index,
            "variable": variable,
            "zero_permutation": zero,
            "one_permutation": one,
            "constant": constant,
            "offset": offset,
            "size": size,
        })
        offset += size
    query_offset = offset
    dimension = query_offset + N_VARIABLES
    assert query_offset == 22750
    assert dimension == 22754
    return tuple(layers), query_offset, dimension


def edge_index(layer, state, branch=None):
    if layer["constant"]:
        assert branch is None
        return layer["offset"] + state
    assert branch in (0, 1)
    return layer["offset"] + 2 * state + branch


def outgoing_terms(layer, state):
    if layer["constant"]:
        return ((edge_index(layer, state), 1),)
    return ((edge_index(layer, state, 0), 1), (edge_index(layer, state, 1), 1))


def incoming_terms(layer, target_state):
    terms = []
    if layer["constant"]:
        permutation = layer["zero_permutation"]
        for source in range(WIDTH):
            if permutation[source] == target_state:
                terms.append((edge_index(layer, source), 1))
    else:
        for source in range(WIDTH):
            if layer["zero_permutation"][source] == target_state:
                terms.append((edge_index(layer, source, 0), 1))
            if layer["one_permutation"][source] == target_state:
                terms.append((edge_index(layer, source, 1), 1))
    return tuple(terms)


def make_terms(terms):
    combined = {}
    for index, value in terms:
        combined[index] = combined.get(index, 0) + value
    return tuple((index, value) for index, value in sorted(combined.items()) if value)


def build_checks(program, layers, query_offset, dimension):
    checks = []
    first = layers[0]
    for state in range(WIDTH):
        checks.append({
            "kind": "source_flow",
            "state": state,
            "terms": make_terms(outgoing_terms(first, state)),
            "rhs": int(state == START_STATE),
        })

    for index in range(len(layers) - 1):
        left, right = layers[index], layers[index + 1]
        for state in range(WIDTH):
            terms = list(incoming_terms(left, state))
            terms.extend((coordinate, -value) for coordinate, value in outgoing_terms(right, state))
            checks.append({
                "kind": "flow_conservation",
                "layers": (index, index + 1),
                "state": state,
                "terms": make_terms(terms),
                "rhs": 0,
            })

    last = layers[-1]
    for state in range(WIDTH):
        checks.append({
            "kind": "accept_sink",
            "state": state,
            "terms": make_terms(incoming_terms(last, state)),
            "rhs": int(state == ACCEPT_STATE),
        })

    for layer in layers:
        if layer["constant"]:
            continue
        variable = layer["variable"]
        terms = [
            (edge_index(layer, state, 1), 1)
            for state in range(WIDTH)
        ]
        terms.append((query_offset + variable, -1))
        checks.append({
            "kind": "repeated_query_consistency",
            "layer": layer["index"],
            "variable": variable,
            "terms": make_terms(terms),
            "rhs": 0,
        })

    assert Counter(check["kind"] for check in checks) == {
        "source_flow": 5,
        "flow_conservation": 16245,
        "accept_sink": 5,
        "repeated_query_consistency": 1300,
    }
    assert len(checks) == 17555
    return tuple(checks)


def factor_target_hash(checks, dimension):
    payload = {
        "anchor_rule": "2I target all-ones",
        "dimension": dimension,
        "residual_rows": [
            [[index, RESIDUAL_SCALE * value] for index, value in check["terms"]]
            for check in checks
        ],
        "residual_target": [RESIDUAL_SCALE * check["rhs"] for check in checks],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def instance_data(name, edges):
    program = build_program(edges)
    outputs = validate_program(program, edges)
    layers, query_offset, dimension = build_layout(program)
    checks = build_checks(program, layers, query_offset, dimension)
    record = {
        "name": name,
        "edges": [list(edge) for edge in edges],
        "program_length": len(program),
        "start_state": START_STATE,
        "accept_state": ACCEPT_STATE,
        "target_permutation": list(TARGET_PERMUTATION),
        "instructions": [{
            "layer": index,
            "variable": variable,
            "zero_permutation": list(zero),
            "one_permutation": list(one),
        } for index, (variable, zero, one) in enumerate(program)],
        "truth_table_outputs": outputs,
        "edge_variable_count": query_offset,
        "query_variable_offset": query_offset,
        "lattice_rank": dimension,
        "check_count": len(checks),
        "check_count_by_kind": dict(sorted(Counter(check["kind"] for check in checks).items())),
        "checks": [{
            key: ([list(term) for term in value] if key == "terms" else
                  list(value) if isinstance(value, tuple) else value)
            for key, value in check.items()
        } for check in checks],
        "ambient_dimension": dimension + len(checks),
        "factor_rule": "[2I;5A]",
        "target_rule": "[1;5b]",
        "factor_target_sha256": factor_target_hash(checks, dimension),
        "certified_gram_eigenvalue_lower_bound": 4,
    }
    return program, layers, query_offset, dimension, checks, record


def build_manifest():
    unsat = instance_data("generation_7_obstruction", gen9.UNSAT_EDGES)[5]
    control = instance_data("satisfiable_overlapping_control", gen9.CONTROL_EDGES)[5]
    assert unsat["lattice_rank"] == control["lattice_rank"] == 22754
    return {
        "schema": "gen19-barrington-signed-flow-v1",
        "finite_claim_only": True,
        "compiler": {
            "formula_tree": "balanced binary OR within clauses and balanced binary AND across clauses",
            "width": WIDTH,
            "five_cycle_order": "lexicographic",
            "commutator_pair_order": "lexicographic",
            "constant_layers": "same permutation on both branches, represented by five edges",
            "coefficient_domain": "all integers",
            "external_filters": [],
            "objective": "||2z-1||^2+25||Az-b||^2",
        },
        "instances": [unsat, control],
    }


def reconstruct(record):
    edges = tuple(tuple(edge) for edge in record["edges"])
    program = build_program(edges)
    assert validate_program(program, edges) == record["truth_table_outputs"]
    layers, query_offset, dimension = build_layout(program)
    checks = build_checks(program, layers, query_offset, dimension)
    assert factor_target_hash(checks, dimension) == record["factor_target_sha256"]
    emitted = [{
        key: ([list(term) for term in value] if key == "terms" else
              list(value) if isinstance(value, tuple) else value)
        for key, value in check.items()
    } for check in checks]
    assert emitted == record["checks"]
    return program, layers, query_offset, dimension, checks


def triangular(value):
    return value * (value - 1) // 2


def exact_accept_shell_dp(program, budget, keep_parents=False):
    """Exhaust all integral exact-flow vectors with anchor excess <=8*budget."""
    values = tuple(
        value for value in range(-budget - 2, budget + 3)
        if triangular(value) <= budget
    )
    start_key = ((1, 0, 0, 0, 0), (None,) * N_VARIABLES)
    dp = {start_key: 0}
    history = []
    layer_counts = []

    for layer_index, (variable, zero, one) in enumerate(program):
        next_dp = {}
        parent_records = {} if keep_parents else None
        for key, cost in dp.items():
            flow, queries = key
            remaining = budget - cost
            if variable == -1:
                edge_cost = sum(triangular(value) for value in flow)
                next_cost = cost + edge_cost
                if next_cost > budget:
                    continue
                next_flow = [0] * WIDTH
                for state, value in enumerate(flow):
                    next_flow[zero[state]] += value
                next_key = (tuple(next_flow), queries)
                old = next_dp.get(next_key)
                if old is None or next_cost < old:
                    next_dp[next_key] = next_cost
                    if keep_parents:
                        parent_records[next_key] = (key, tuple(flow))
                continue

            if queries[variable] is None:
                query_values = tuple(value for value in values if triangular(value) <= remaining)
            else:
                query_values = (queries[variable],)

            coordinate_choices = []
            for state_flow in flow:
                coordinate_choices.append(tuple(
                    branch_one for branch_one in values
                    if triangular(branch_one) + triangular(state_flow - branch_one) <= remaining
                ))

            for branch_one_values in product(*coordinate_choices):
                query_value = sum(branch_one_values)
                if query_value not in query_values:
                    continue
                edge_cost = sum(
                    triangular(branch_one) + triangular(state_flow - branch_one)
                    for branch_one, state_flow in zip(branch_one_values, flow)
                )
                query_cost = triangular(query_value) if queries[variable] is None else 0
                next_cost = cost + edge_cost + query_cost
                if next_cost > budget:
                    continue
                next_flow = [0] * WIDTH
                edge_values = []
                for state, (branch_one, state_flow) in enumerate(zip(branch_one_values, flow)):
                    branch_zero = state_flow - branch_one
                    edge_values.extend((branch_zero, branch_one))
                    next_flow[zero[state]] += branch_zero
                    next_flow[one[state]] += branch_one
                next_queries = list(queries)
                next_queries[variable] = query_value
                next_key = (tuple(next_flow), tuple(next_queries))
                old = next_dp.get(next_key)
                if old is None or next_cost < old:
                    next_dp[next_key] = next_cost
                    if keep_parents:
                        parent_records[next_key] = (key, tuple(edge_values))
        dp = next_dp
        layer_counts.append(len(dp))
        if keep_parents:
            history.append(parent_records)
        if not dp:
            break

    target_flow = tuple(int(state == ACCEPT_STATE) for state in range(WIDTH))
    candidates = sorted(
        (cost, key) for key, cost in dp.items() if key[0] == target_flow
    )
    if not candidates:
        return {
            "budget_units": budget,
            "minimum_units": None,
            "layer_state_counts": layer_counts,
            "maximum_layer_states": max(layer_counts, default=0),
            "selector": None,
        }

    minimum, final_key = candidates[0]
    selector = None
    if keep_parents:
        layer_edges = [None] * len(program)
        key = final_key
        for layer_index in range(len(program) - 1, -1, -1):
            previous_key, edges = history[layer_index][key]
            layer_edges[layer_index] = edges
            key = previous_key
        assert key == start_key
        query_values = final_key[1]
        selector = tuple(value for edges in layer_edges for value in edges) + tuple(query_values)
    return {
        "budget_units": budget,
        "minimum_units": minimum,
        "layer_state_counts": layer_counts,
        "maximum_layer_states": max(layer_counts, default=0),
        "selector": selector,
    }


def residual(checks, selector):
    return tuple(
        sum(value * selector[index] for index, value in check["terms"]) - check["rhs"]
        for check in checks
    )


def squared_distance(checks, selector):
    anchor = sum((2 * value - 1) ** 2 for value in selector)
    raw = residual(checks, selector)
    return anchor + RESIDUAL_SCALE ** 2 * sum(value * value for value in raw)


def honest_path_selector(program, assignment):
    layers, query_offset, dimension = build_layout(program)
    selector = [0] * dimension
    state = START_STATE
    for layer in layers:
        if layer["constant"]:
            selector[edge_index(layer, state)] = 1
            state = layer["zero_permutation"][state]
        else:
            branch = assignment[layer["variable"]]
            selector[edge_index(layer, state, branch)] = 1
            permutation = layer["one_permutation"] if branch else layer["zero_permutation"]
            state = permutation[state]
    for variable, value in enumerate(assignment):
        selector[query_offset + variable] = value
    return tuple(selector), state


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
    unsat_program, _, _, dimension, unsat_checks = reconstruct(manifest["instances"][0])
    control_program, _, _, control_dimension, control_checks = reconstruct(manifest["instances"][1])
    assert dimension == control_dimension == 22754

    # Control completeness and exact minimum: the honest path reaches ACCEPT,
    # has zero residual, and every integral anchor coordinate costs at least 1.
    control_assignment = (1, 1, 1, 0)
    control_selector, control_endpoint = honest_path_selector(control_program, control_assignment)
    assert control_endpoint == ACCEPT_STATE
    assert not any(residual(control_checks, control_selector))
    assert squared_distance(control_checks, control_selector) == dimension
    control_exact_minimum2 = dimension

    # Exact unrestricted accepting-fiber search.  Budget one exhausts every
    # integer vector of anchor excess <=8 and finds none.  Budget two finds and
    # reconstructs the minimum signed accepting flow at excess 16.
    below = exact_accept_shell_dp(unsat_program, 1, keep_parents=False)
    assert below["minimum_units"] is None
    search = exact_accept_shell_dp(unsat_program, 2, keep_parents=True)
    assert search["minimum_units"] == 2
    attack = tuple(search["selector"])
    assert len(attack) == dimension
    raw = residual(unsat_checks, attack)
    assert not any(raw)
    attack_anchor = sum((2 * value - 1) ** 2 for value in attack)
    assert attack_anchor == dimension + 16

    # Full unrestricted CVP minimum: a nonzero integral residual costs at
    # least 25 above the universal anchor baseline, while the exact ACCEPT
    # fiber witness costs baseline+16.
    assert dimension + RESIDUAL_SCALE ** 2 > attack_anchor
    unsat_exact_minimum2 = attack_anchor

    coefficient_histogram = dict(sorted(Counter(attack).items()))
    assert any(value < 0 for value in attack)

    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[1])),
        "program_length": len(unsat_program),
        "lattice_rank": dimension,
        "check_count": len(unsat_checks),
        "control_exact_unrestricted_minimum_squared": control_exact_minimum2,
        "budget_one_exact_search": below,
        "budget_two_exact_search": {
            key: value for key, value in search.items() if key != "selector"
        },
        "signed_accepting_flow_coefficient_histogram": coefficient_histogram,
        "signed_accepting_flow_anchor_excess": 16,
        "signed_accepting_flow_residual_squared": 0,
        "unsat_exact_unrestricted_minimum_squared": unsat_exact_minimum2,
        "squared_distance_ratio": f"{unsat_exact_minimum2}/{control_exact_minimum2}",
        "finding": (
            "the unsatisfiable Barrington flow lattice has an exact zero-residual "
            "accepting signed flow at anchor excess 16"
        ),
        "scope": (
            "finite kill of this emitted branching-program flow encoding; no O5/O8 theorem"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
