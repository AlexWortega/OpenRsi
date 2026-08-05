#!/usr/bin/env python3
"""Generation-2 exact attack on the surviving A5 convolution tile.

The frozen depth-two instance has three fusion tiles.  A tile has one integral
selector z[g,h] for every ordered pair in A5^2.  The two child tiles have both
leaf marginals fixed to delta_identity.  Their product marginals are glued to
the root's left and right marginals, and the root product is fixed to the
Barrington ACCEPT 5-cycle.  Normalization and every left, right, product,
source/COPY, and ACCEPT equation is an emitted lattice row.  For factors
C=[a I; b A], 1 <= a,b <= 12, the objective is

    a^2 ||2z-1||^2 + b^2 ||Az-rhs||^2.

A bicyclic unit u=1+x in Z[A5], x^2=0, and a shifted inverse
v=(1-x) ACCEPT satisfy u*v=ACCEPT. Exact signed child couplings produce u and
v from identity leaf marginals; their outer-product root coupling produces
ACCEPT. The matched satisfiable control uses honest leaves `(e,e,e,ACCEPT)`
and the same ACCEPT target. The unrestricted attack has zero residual and
squared anchor 10936 a^2, while the control has exact squared radius
10800 a^2. Since 32*10936 < 33*10800, all 144 factor pairs fail the required
33/32 depth-two squared-growth gate.

This is a finite counterexample to this explicit fusion tile, not a theorem
about every nonabelian or nonlinear construction.
"""

from __future__ import annotations

from collections import Counter
from itertools import permutations, product
import hashlib
import importlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PRIOR = ROOT / "prior" / "experiments"
LOCKED_HASHES = {
    "verify_barrington_signed_flow.py": "9535cc40e3cda3afe1b20209d34a008ccb0f9d7d1a879a84bd7ff74a6da4626e",
    "gen19_barrington_signed_flow_manifest.json": "b6d8d9b966e74ce8ee000c89b397d490b1aafdf2707022f23804f5ec58f728ff",
    "verify_global_psd_metric.py": "34fee18f59bf758a36d5ea9cb2ce9adf561440e656080622c86d1e81b0cceaab",
}


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


for filename, expected in LOCKED_HASHES.items():
    assert file_hash(PRIOR / filename) == expected

sys.path.insert(0, str(PRIOR))
g19 = importlib.import_module("verify_barrington_signed_flow")

GROUP_SIZE = 60
TILE_RANK = GROUP_SIZE * GROUP_SIZE
TILE_COUNT = 3
RANK = TILE_COUNT * TILE_RANK
LEFT_CHILD = 0
RIGHT_CHILD = 1
ROOT_TILE = 2


def sign(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(5) for j in range(i + 1, 5)
    )
    return -1 if inversions & 1 else 1


A5 = tuple(permutation for permutation in permutations(range(5)) if sign(permutation) == 1)
INDEX = {permutation: index for index, permutation in enumerate(A5)}
IDENTITY_PERMUTATION = tuple(range(5))
IDENTITY = INDEX[IDENTITY_PERMUTATION]
ACCEPT = INDEX[g19.TARGET_PERMUTATION]
assert len(A5) == GROUP_SIZE
assert IDENTITY == 0
assert ACCEPT == 16


def multiply_permutations(first, second):
    """Apply first and then second, matching the locked Barrington compiler."""
    return tuple(second[first[state]] for state in range(5))


MULTIPLICATION = tuple(
    tuple(INDEX[multiply_permutations(left, right)] for right in A5)
    for left in A5
)


def coordinate(tile, left, right):
    return tile * TILE_RANK + left * GROUP_SIZE + right


def add(measure, group, value):
    measure[group] = measure.get(group, 0) + value
    if measure[group] == 0:
        del measure[group]


def convolution(left, right):
    result = {}
    for g, left_value in left.items():
        for h, right_value in right.items():
            add(result, MULTIPLICATION[g][h], left_value * right_value)
    return result


def scale(measure, scalar):
    return {group: scalar * value for group, value in measure.items() if scalar * value}


def shifted_right(measure, group):
    result = {}
    for element, value in measure.items():
        add(result, MULTIPLICATION[element][group], value)
    return result


def find_bicyclic_unit():
    """Lexicographically first x=(1-g)h(1+g) with four distinct terms."""
    for g in range(1, GROUP_SIZE):
        if MULTIPLICATION[g][g] != IDENTITY:
            continue
        for h in range(GROUP_SIZE):
            x = {}
            add(x, h, 1)
            add(x, MULTIPLICATION[h][g], 1)
            add(x, MULTIPLICATION[g][h], -1)
            add(x, MULTIPLICATION[MULTIPLICATION[g][h]][g], -1)
            if len(x) == 4 and IDENTITY not in x and not convolution(x, x):
                return g, h, x
    raise AssertionError("no bicyclic unit")


G_INVOLUTION, H_ELEMENT, X = find_bicyclic_unit()
assert (G_INVOLUTION, H_ELEMENT) == (3, 1)
assert X == {1: 1, 5: 1, 6: -1, 10: -1}
UNIT = {IDENTITY: 1, **X}
UNIT_INVERSE = {IDENTITY: 1, **scale(X, -1)}
SHIFTED_INVERSE = shifted_right(UNIT_INVERSE, ACCEPT)
assert convolution(X, X) == {}
assert convolution(UNIT, UNIT_INVERSE) == {IDENTITY: 1}
assert convolution(UNIT, SHIFTED_INVERSE) == {ACCEPT: 1}

LEFT_SUPPORT = ((0, 0), (16, 12), (16, 50), (19, 12), (19, 50))
RIGHT_SUPPORT = (
    (0, 16), (5, 14), (5, 16), (37, 0),
    (37, 26), (41, 14), (41, 26),
)


def coupling_marginals(coupling):
    left = {}
    right = {}
    product_port = {}
    for (g, h), value in coupling.items():
        add(left, g, value)
        add(right, h, value)
        add(product_port, MULTIPLICATION[g][h], value)
    return left, right, product_port


def exact_support_search(support, target_product):
    """Exhaust {-1,0,1} on a frozen support; return least-negative solution."""
    best = None
    feasible = 0
    for values in product((-1, 0, 1), repeat=len(support)):
        coupling = {pair: value for pair, value in zip(support, values) if value}
        if coupling_marginals(coupling) != (
            {IDENTITY: 1}, {IDENTITY: 1}, target_product,
        ):
            continue
        feasible += 1
        key = (sum(value < 0 for value in values), values)
        if best is None or key < best[0]:
            best = (key, coupling)
    assert best is not None
    return best[1], feasible, 3 ** len(support)


LEFT_COUPLING, LEFT_FEASIBLE, LEFT_SEARCHED = exact_support_search(LEFT_SUPPORT, UNIT)
RIGHT_COUPLING, RIGHT_FEASIBLE, RIGHT_SEARCHED = exact_support_search(
    RIGHT_SUPPORT, SHIFTED_INVERSE
)
assert LEFT_COUPLING == {
    (0, 0): 1, (16, 12): 1, (16, 50): -1, (19, 12): -1, (19, 50): 1,
}
assert RIGHT_COUPLING == {
    (0, 16): 1, (5, 14): 1, (5, 16): -1, (37, 0): 1,
    (37, 26): -1, (41, 14): -1, (41, 26): 1,
}
ROOT_COUPLING = {
    (left, right): left_value * right_value
    for left, left_value in UNIT.items()
    for right, right_value in SHIFTED_INVERSE.items()
}


DELTA_IDENTITY = {IDENTITY: 1}
DELTA_ACCEPT = {ACCEPT: 1}
assert coupling_marginals(LEFT_COUPLING) == (DELTA_IDENTITY, DELTA_IDENTITY, UNIT)
assert coupling_marginals(RIGHT_COUPLING) == (
    DELTA_IDENTITY,
    DELTA_IDENTITY,
    SHIFTED_INVERSE,
)
assert coupling_marginals(ROOT_COUPLING) == (UNIT, SHIFTED_INVERSE, DELTA_ACCEPT)


def combine_selector(couplings):
    selector = {}
    for tile, coupling in enumerate(couplings):
        for (left, right), value in coupling.items():
            if value:
                selector[coordinate(tile, left, right)] = value
    return selector


ATTACK = combine_selector((LEFT_COUPLING, RIGHT_COUPLING, ROOT_COUPLING))
CONTROL_LEFT = {(IDENTITY, IDENTITY): 1}
CONTROL_RIGHT = {(IDENTITY, ACCEPT): 1}
CONTROL_ROOT = {(IDENTITY, ACCEPT): 1}
CONTROL = combine_selector((CONTROL_LEFT, CONTROL_RIGHT, CONTROL_ROOT))
NO_LEAVES = ((IDENTITY, IDENTITY), (IDENTITY, IDENTITY))
CONTROL_LEAVES = ((IDENTITY, IDENTITY), (IDENTITY, ACCEPT))


def pair_terms(tile, predicate, coefficient=1):
    return tuple(
        (coordinate(tile, left, right), coefficient)
        for left in range(GROUP_SIZE)
        for right in range(GROUP_SIZE)
        if predicate(left, right)
    )


def emitted_rows(leaf_pairs, accept_group):
    # One normalization per tile.
    for tile in range(TILE_COUNT):
        yield "normalization", (tile,), pair_terms(tile, lambda _g, _h: True), 1

    # Four legal identity leaf ports (source/repeated-query/COPY boundaries).
    for tile in (LEFT_CHILD, RIGHT_CHILD):
        left_target, right_target = leaf_pairs[tile]
        for group in range(GROUP_SIZE):
            yield (
                "leaf_left",
                (tile, group),
                pair_terms(tile, lambda left, _right, group=group: left == group),
                int(group == left_target),
            )
            yield (
                "leaf_right",
                (tile, group),
                pair_terms(tile, lambda _left, right, group=group: right == group),
                int(group == right_target),
            )

    # Complete child-product to root-port gluing.
    for child, root_side in ((LEFT_CHILD, 0), (RIGHT_CHILD, 1)):
        for group in range(GROUP_SIZE):
            terms = list(pair_terms(
                child,
                lambda left, right, group=group: MULTIPLICATION[left][right] == group,
            ))
            if root_side == 0:
                terms.extend(pair_terms(
                    ROOT_TILE,
                    lambda left, _right, group=group: left == group,
                    coefficient=-1,
                ))
            else:
                terms.extend(pair_terms(
                    ROOT_TILE,
                    lambda _left, right, group=group: right == group,
                    coefficient=-1,
                ))
            yield "fusion_copy", (child, root_side, group), tuple(terms), 0

    # Root ACCEPT product port.
    for group in range(GROUP_SIZE):
        yield (
            "accept_product",
            (group,),
            pair_terms(
                ROOT_TILE,
                lambda left, right, group=group: MULTIPLICATION[left][right] == group,
            ),
            int(group == accept_group),
        )


def dot(terms, selector):
    return sum(value * selector.get(index, 0) for index, value in terms)


def audit_rows(leaf_pairs, accept_group, selector):
    digest = hashlib.sha256()
    counts = Counter()
    residuals = []
    for kind, metadata, terms, rhs in emitted_rows(leaf_pairs, accept_group):
        counts[kind] += 1
        residual = dot(terms, selector) - rhs
        if residual:
            residuals.append((kind, metadata, residual))
        digest.update(json.dumps(
            [kind, list(metadata), [list(term) for term in terms], rhs],
            separators=(",", ":"),
        ).encode() + b"\n")
    return dict(sorted(counts.items())), residuals, digest.hexdigest()


def triangular(value):
    return value * (value - 1) // 2


def anchor_unscaled(selector):
    return RANK + 8 * sum(triangular(value) for value in selector.values())


def histogram(selector, total=RANK):
    result = Counter(selector.values())
    result[0] = total - len(selector)
    return dict(sorted(result.items()))


def no_boolean_accepting_vector():
    """Exact proof for the all-zero anchor shell, with no external filter."""
    # Zero anchor excess forces every coefficient to 0/1.  Normalization then
    # makes each tile one-hot.  Child leaf rows force both child pairs (e,e),
    # gluing forces the root pair (e,e), whose product is not ACCEPT.
    assert MULTIPLICATION[IDENTITY][IDENTITY] == IDENTITY
    assert IDENTITY != ACCEPT
    return True


def main():
    attack_counts, attack_residuals, no_hash = audit_rows(NO_LEAVES, ACCEPT, ATTACK)
    control_counts, control_residuals, control_hash = audit_rows(
        CONTROL_LEAVES, ACCEPT, CONTROL
    )
    assert attack_counts == control_counts == {
        "accept_product": 60,
        "fusion_copy": 120,
        "leaf_left": 120,
        "leaf_right": 120,
        "normalization": 3,
    }
    assert sum(attack_counts.values()) == 423
    assert not attack_residuals
    assert not control_residuals
    assert no_boolean_accepting_vector()

    assert histogram(LEFT_COUPLING, TILE_RANK) == {-1: 2, 0: 3595, 1: 3}
    assert histogram(RIGHT_COUPLING, TILE_RANK) == {-1: 3, 0: 3593, 1: 4}
    assert histogram(ROOT_COUPLING, TILE_RANK) == {-1: 12, 0: 3575, 1: 13}
    assert histogram(ATTACK) == {-1: 17, 0: 10763, 1: 20}
    assert anchor_unscaled(CONTROL) == RANK == 10800
    assert anchor_unscaled(ATTACK) == RANK + 136 == 10936
    assert 32 * 10936 < 33 * 10800

    factor_results = []
    for anchor_scale in range(1, 13):
        for residual_scale in range(1, 13):
            control_radius2 = anchor_scale * anchor_scale * RANK
            attack_cost2 = anchor_scale * anchor_scale * 10936
            # Both vectors have exact zero residual, so b cannot repair the gap.
            assert 32 * attack_cost2 < 33 * control_radius2
            factor_results.append((anchor_scale, residual_scale))
    assert len(factor_results) == 144

    # Positive anchor block gives a finite unrestricted shell automatically.
    # Through the attack radius, all other RANK-1 anchors contribute at least
    # a^2, so (2z_i-1)^2 <= 137 and every coefficient lies in [-5,6].
    assert 11 * 11 <= 137 < 13 * 13
    coefficient_bound = (-5, 6)

    print(json.dumps({
        "group": "A5 in lexicographic even-permutation order",
        "group_size": GROUP_SIZE,
        "accept_permutation": list(g19.TARGET_PERMUTATION),
        "accept_index": ACCEPT,
        "tile_selector_count": TILE_RANK,
        "depth_two_rank": RANK,
        "emitted_row_count": sum(attack_counts.values()),
        "row_count_by_kind": attack_counts,
        "no_instance_factor_target_sha256": no_hash,
        "control_factor_target_sha256": control_hash,
        "bicyclic_unit": {
            "involution_index": G_INVOLUTION,
            "h_index": H_ELEMENT,
            "x": dict(sorted(X.items())),
            "x_squared": {},
            "unit_times_inverse": {str(IDENTITY): 1},
        },
        "falsifying_port_class": "zero-divisor/bicyclic SPLICE with legal leaves and legal ACCEPT output",
        "exact_low_weight_support_search": {
            "left_assignments": LEFT_SEARCHED,
            "left_feasible": LEFT_FEASIBLE,
            "right_assignments": RIGHT_SEARCHED,
            "right_feasible": RIGHT_FEASIBLE,
            "scope": "complete {-1,0,1} enumeration on the two frozen sparse supports",
        },
        "left_false_fusion_histogram": histogram(LEFT_COUPLING, TILE_RANK),
        "right_false_fusion_histogram": histogram(RIGHT_COUPLING, TILE_RANK),
        "root_virtual_unit_histogram": histogram(ROOT_COUPLING, TILE_RANK),
        "depth_two_attack_histogram": histogram(ATTACK),
        "depth_two_attack_residual_squared": 0,
        "control_exact_minimum_squared_at_a1": RANK,
        "depth_two_attack_squared_at_a1": 10936,
        "growth_comparison": "32*10936 < 33*10800",
        "factor_pairs_rejected": len(factor_results),
        "factor_range": "1<=a,b<=12",
        "unrestricted_attack_shell_coefficient_bound": list(coefficient_bound),
        "recession_audit": "aI is positive definite for every tested a>=1",
        "potential_lp_status": "not opened: the explicit legal-boundary primal NO vector already violates the distance consequence below 33/32",
        "no_yes_isometry_audit": "rejected: control attains the anchor lower bound, while NO has no Boolean zero-residual vector",
        "finding": "a bicyclic virtual unit fuses legal identity leaves to ACCEPT at squared ratio 10936/10800 < 33/32",
        "scope": "finite kill of this explicit A5 fusion tile for all 144 tested factors; no general nonabelian impossibility theorem",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
