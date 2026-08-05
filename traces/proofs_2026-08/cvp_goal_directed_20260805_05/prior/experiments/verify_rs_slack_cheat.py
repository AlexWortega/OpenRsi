#!/usr/bin/env python3
"""Exact finite attack on RS-amplified affine clause residuals.

The formula contains all eight sign patterns on x,y,z and is unsatisfiable.
Each clause has two integer slack bits a_i,b_i and residual

    r_i = (sum of its three literal values) - 1 - a_i - b_i.

The amplified block evaluates R(T)=sum_i r_i T^i at T=1,...,64.
Every integer coordinate has the (scaled) half-integral Boolean anchor
(2z-1)^2. Thus the squared objective is the sum of all 19 anchor costs
and the 64 squared evaluations. A Boolean encoding has baseline 19.

The search is exact for objective at most the exhibited upper bound 27.
It also exhaustively optimizes every residual-zero slack pair in [-20,20]^2
for every variable assignment in [-20,20]^3.  Slack clauses separate once
r=0, so this is equivalent to jointly minimizing their anchor sum.
"""

from itertools import product
import json

BOUND = 20
N_EVAL = 64
M = 8

# A sign 1 means x; a sign 0 means (1-x).  All sign patterns occur.
CLAUSES = tuple(product((0, 1), repeat=3))


def anchor(z: int) -> int:
    """Four times the squared distance from integer z to target 1/2."""
    return (2 * z - 1) ** 2


def literal_sum(xs: tuple[int, int, int], signs: tuple[int, int, int]) -> int:
    return sum(x if sign else 1 - x for x, sign in zip(xs, signs))


def residuals(xs: tuple[int, int, int], slack: tuple[int, ...]) -> tuple[int, ...]:
    assert len(slack) == 2 * M
    return tuple(
        literal_sum(xs, signs) - 1 - slack[2 * i] - slack[2 * i + 1]
        for i, signs in enumerate(CLAUSES)
    )


def rs_energy(rs: tuple[int, ...]) -> int:
    total = 0
    for t in range(1, N_EVAL + 1):
        value = 0
        for coefficient in reversed(rs):
            value = value * t + coefficient
        total += value * value
    return total


def objective(xs: tuple[int, int, int], slack: tuple[int, ...]) -> int:
    rs = residuals(xs, slack)
    return sum(map(anchor, xs)) + sum(map(anchor, slack)) + rs_energy(rs)


def best_pair_table() -> dict[int, tuple[int, tuple[int, int]]]:
    """Exhaust all 41^2 slack pairs and retain the cheapest for each sum."""
    table: dict[int, tuple[int, tuple[int, int]]] = {}
    for a in range(-BOUND, BOUND + 1):
        for b in range(-BOUND, BOUND + 1):
            cost = anchor(a) + anchor(b)
            old = table.get(a + b)
            candidate = (cost, (a, b))
            if old is None or candidate < old:
                table[a + b] = candidate
    return table


def exact_residual_zero_box_search() -> tuple[int, tuple[int, ...], tuple[int, ...], int]:
    """Minimize anchors over all box candidates constrained by r=0.

    Given x, clause i requires a_i+b_i=literal_sum_i-1.  The precomputed
    table exactly minimizes each independent pair, avoiding a vacuous
    41^19 Cartesian loop without weakening exhaustiveness.
    """
    table = best_pair_table()
    best_cost = None
    best_xs: tuple[int, ...] | None = None
    best_slack: tuple[int, ...] | None = None
    assignments = 0
    for xs in product(range(-BOUND, BOUND + 1), repeat=3):
        assignments += 1
        cost = sum(map(anchor, xs))
        chosen: list[int] = []
        feasible = True
        for signs in CLAUSES:
            required_sum = literal_sum(xs, signs) - 1
            entry = table.get(required_sum)
            if entry is None:
                feasible = False
                break
            pair_cost, pair = entry
            cost += pair_cost
            chosen.extend(pair)
        if feasible:
            candidate_slack = tuple(chosen)
            candidate = (cost, xs, candidate_slack)
            if best_cost is None or candidate < (best_cost, best_xs, best_slack):
                best_cost, best_xs, best_slack = candidate
    assert best_cost is not None and best_xs is not None and best_slack is not None
    return best_cost, best_xs, best_slack, assignments


def exhaustive_zero_anchor_search() -> int:
    """Count Boolean assignments to all 19 coordinates with r=0."""
    satisfying = 0
    for xs in product((0, 1), repeat=3):
        for slack in product((0, 1), repeat=2 * M):
            if not any(residuals(xs, slack)):
                satisfying += 1
    return satisfying


def main() -> None:
    assert len(CLAUSES) == M
    assert len(set(CLAUSES)) == M

    # The RS lower bound is exact arithmetic: a nonzero degree-at-most-7
    # polynomial has at most seven roots among 64 distinct evaluation points.
    nonzero_residual_energy_lower_bound = N_EVAL - (M - 1)
    assert nonzero_residual_energy_lower_bound == 57

    best_cost, xs, slack, assignments = exact_residual_zero_box_search()
    assert assignments == 41 ** 3
    boolean_anchor_baseline = 3 + 2 * M
    assert boolean_anchor_baseline == 19
    assert best_cost == 27
    assert not any(residuals(xs, slack))
    assert objective(xs, slack) == best_cost

    # Exhaustively rule out a residual-zero point at the Boolean baseline.
    # Any nonzero residual has total objective at least 19+57=76, while the
    # residual-zero box search is exhaustive below 27. Thus 27 is global.
    zero_anchor_solutions = exhaustive_zero_anchor_search()
    assert zero_anchor_solutions == 0
    assert boolean_anchor_baseline + nonzero_residual_energy_lower_bound > best_cost

    # A transparent Boolean witness: exactly one of the eight clauses is
    # false, and one of that clause's slack bits moves from 0 to -1.
    witness_xs = (0, 0, 0)
    witness_slack: list[int] = []
    false_clauses = 0
    for signs in CLAUSES:
        q = literal_sum(witness_xs, signs) - 1
        if q == -1:
            false_clauses += 1
            witness_slack.extend((-1, 0))
        elif q == 0:
            witness_slack.extend((0, 0))
        elif q == 1:
            witness_slack.extend((0, 1))
        elif q == 2:
            witness_slack.extend((1, 1))
        else:
            raise AssertionError(q)
    witness_slack_tuple = tuple(witness_slack)
    assert false_clauses == 1
    assert not any(residuals(witness_xs, witness_slack_tuple))
    assert rs_energy(residuals(witness_xs, witness_slack_tuple)) == 0
    assert objective(witness_xs, witness_slack_tuple) == 27

    # The box result is global at this weight: any integer outside [-20,20]
    # has anchor cost already exceeding the cost-27 witness.
    assert min(anchor(-21), anchor(21)) > best_cost

    print(json.dumps({
        "formula": "all eight 3-literal sign patterns on x,y,z",
        "evaluation_points": N_EVAL,
        "box": [-BOUND, BOUND],
        "variable_assignments_checked": assignments,
        "slack_pairs_checked_per_required_sum": (2 * BOUND + 1) ** 2,
        "boolean_assignments_checked": 2 ** (3 + 2 * M),
        "boolean_residual_zero_solutions": zero_anchor_solutions,
        "boolean_anchor_baseline_squared": boolean_anchor_baseline,
        "nonzero_residual_squared_energy_lower_bound": nonzero_residual_energy_lower_bound,
        "claimed_nonzero_residual_norm_lower_bound": "sqrt(57)",
        "exact_minimum_squared_objective": best_cost,
        "exact_minimum_norm": "sqrt(27)",
        "distance_ratio_over_boolean_baseline": "sqrt(27/19)",
        "witness_variables": list(witness_xs),
        "witness_slacks": list(witness_slack_tuple),
        "witness_amplified_energy": 0,
        "finding": "integer slack bits zero every residual; squared cost is only 8 above the Boolean anchor baseline"
    }, sort_keys=True))


if __name__ == "__main__":
    main()
