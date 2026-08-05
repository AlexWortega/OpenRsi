#!/usr/bin/env python3
"""Exact finite k=2 audit of the Generation-19 signed-flow splice.

This verifier instantiates a complete ordered-pair lift of the hash-locked
Generation-19 width-5 program.  It emits pair-flow, both unary marginals,
complete repeated-query pair totals, unary query totals, and every source,
conservation, ACCEPT, marginal, and query-marginal row.  It also emits the
strong diagonal coherence equations: off-diagonal transition pairs are zero
and each diagonal pair equals its unary marginal. Every integer coordinate
has the usual odd anchor `(2z-1)^2`, and every emitted residual row has scale
5, giving the fixed objective `||2z-1||^2+25||Az-b||^2`.

The Generation-19 unrestricted search is rerun through anchor excess 16.  Its
minimum two-negative accepting flow s has two natural lifts.  The pure moment
s tensor s satisfies all flow/marginal/query rows but not diagonal coherence.
More strongly, the diagonal embedding diag(s), with s in both unary marginals,
satisfies every row including diagonal coherence.  The script compares its
exact squared cost with both 4R_2^2/3 and the actual ROADMAP frontier value
16R_2^2/9.  A matched honest control is checked too.

This is a finite counterexample to this explicit raw ordered-pair lift.  It is
not an exact computation of the k=2 optimum and not an impossibility theorem
for every possible amended coherence construction.
"""

from __future__ import annotations

from collections import Counter
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


for filename, expected_hash in LOCKED_HASHES.items():
    path = PRIOR / filename
    assert sha256_file(path) == expected_hash, (filename, sha256_file(path))
sys.path.insert(0, str(PRIOR))
g19 = importlib.import_module("verify_barrington_signed_flow")

K = 2
RESIDUAL_SCALE = 5
PAIR_PATTERNS = tuple((a, b) for a in (0, 1) for b in (0, 1))


def edges_of(layer):
    edges = []
    if layer[0] == -1:
        permutation = layer[1]
        for source in range(g19.WIDTH):
            edges.append((source, None, permutation[source]))
    else:
        _, zero, one = layer
        for source in range(g19.WIDTH):
            edges.append((source, 0, zero[source]))
            edges.append((source, 1, one[source]))
    return tuple(edges)


class Layout:
    """Canonical coordinates for the complete pair lift."""

    def __init__(self, program):
        self.program = tuple(program)
        self.edges = tuple(edges_of(layer) for layer in program)
        offset = 0
        self.pair_offsets = []
        for edges in self.edges:
            self.pair_offsets.append(offset)
            offset += len(edges) ** 2
        self.unary_offsets = []
        for edges in self.edges:
            self.unary_offsets.append((offset, offset + len(edges)))
            offset += 2 * len(edges)
        self.pair_query_offset = offset
        offset += g19.N_VARIABLES * len(PAIR_PATTERNS)
        self.unary_query_offset = offset
        offset += g19.N_VARIABLES * K * 2
        self.rank = offset

    def pair(self, layer, first, second):
        size = len(self.edges[layer])
        return self.pair_offsets[layer] + first * size + second

    def unary(self, layer, position, edge):
        return self.unary_offsets[layer][position] + edge

    def pair_query(self, variable, pattern):
        return self.pair_query_offset + 4 * variable + PAIR_PATTERNS.index(pattern)

    def unary_query(self, variable, position, bit):
        return self.unary_query_offset + 4 * variable + 2 * position + bit


# Rows are (kind, metadata, sparse integer terms, rhs).  Metadata is included
# in the canonical hash; terms alone determine the emitted lattice row.
def emitted_rows(layout: Layout):
    edges_by_layer = layout.edges
    first_edges = edges_by_layer[0]
    for states in ((u, v) for u in range(g19.WIDTH) for v in range(g19.WIDTH)):
        terms = []
        for i, edge_i in enumerate(first_edges):
            if edge_i[0] != states[0]:
                continue
            for j, edge_j in enumerate(first_edges):
                if edge_j[0] == states[1]:
                    terms.append((layout.pair(0, i, j), 1))
        yield "pair_source", states, tuple(terms), int(states == (g19.START_STATE,) * K)

    for layer in range(len(layout.program) - 1):
        left, right = edges_by_layer[layer], edges_by_layer[layer + 1]
        for states in ((u, v) for u in range(g19.WIDTH) for v in range(g19.WIDTH)):
            terms = []
            for i, edge_i in enumerate(left):
                if edge_i[2] != states[0]:
                    continue
                for j, edge_j in enumerate(left):
                    if edge_j[2] == states[1]:
                        terms.append((layout.pair(layer, i, j), 1))
            for i, edge_i in enumerate(right):
                if edge_i[0] != states[0]:
                    continue
                for j, edge_j in enumerate(right):
                    if edge_j[0] == states[1]:
                        terms.append((layout.pair(layer + 1, i, j), -1))
            yield "pair_conservation", (layer,) + states, tuple(terms), 0

    last_layer = len(layout.program) - 1
    last_edges = edges_by_layer[-1]
    for states in ((u, v) for u in range(g19.WIDTH) for v in range(g19.WIDTH)):
        terms = []
        for i, edge_i in enumerate(last_edges):
            if edge_i[2] != states[0]:
                continue
            for j, edge_j in enumerate(last_edges):
                if edge_j[2] == states[1]:
                    terms.append((layout.pair(last_layer, i, j), 1))
        yield "pair_accept", states, tuple(terms), int(states == (g19.ACCEPT_STATE,) * K)

    # Complete ordered-pair-to-unary transition marginals.
    for layer, edges in enumerate(edges_by_layer):
        for position in range(K):
            for edge in range(len(edges)):
                terms = []
                for other in range(len(edges)):
                    pair = (edge, other) if position == 0 else (other, edge)
                    terms.append((layout.pair(layer, *pair), 1))
                terms.append((layout.unary(layer, position, edge), -1))
                yield "transition_marginal", (layer, position, edge), tuple(terms), 0

    # Strong same-path/Boolean diagonal coherence.  This is deliberately more
    # restrictive than raw marginal consistency.  It still cannot remove a
    # signed flow because that flow embeds linearly on the diagonal.
    for layer, edges in enumerate(edges_by_layer):
        for first in range(len(edges)):
            for second in range(len(edges)):
                terms = [(layout.pair(layer, first, second), 1)]
                if first == second:
                    terms.append((layout.unary(layer, 0, first), -1))
                yield "transition_diagonal", (layer, first, second), tuple(terms), 0

    # Both unary marginals physically carry complete flow equations.
    for position in range(K):
        for state in range(g19.WIDTH):
            terms = tuple(
                (layout.unary(0, position, edge), 1)
                for edge, data in enumerate(first_edges) if data[0] == state
            )
            yield "unary_source", (position, state), terms, int(state == g19.START_STATE)
        for layer in range(len(layout.program) - 1):
            left, right = edges_by_layer[layer], edges_by_layer[layer + 1]
            for state in range(g19.WIDTH):
                terms = [
                    (layout.unary(layer, position, edge), 1)
                    for edge, data in enumerate(left) if data[2] == state
                ]
                terms.extend(
                    (layout.unary(layer + 1, position, edge), -1)
                    for edge, data in enumerate(right) if data[0] == state
                )
                yield "unary_conservation", (position, layer, state), tuple(terms), 0
        for state in range(g19.WIDTH):
            terms = tuple(
                (layout.unary(last_layer, position, edge), 1)
                for edge, data in enumerate(last_edges) if data[2] == state
            )
            yield "unary_accept", (position, state), terms, int(state == g19.ACCEPT_STATE)

    # Complete branch-pair totals are shared by every occurrence of a query.
    for layer, instruction in enumerate(layout.program):
        variable = instruction[0]
        if variable == -1:
            continue
        edges = edges_by_layer[layer]
        for pattern in PAIR_PATTERNS:
            terms = []
            for i, edge_i in enumerate(edges):
                if edge_i[1] != pattern[0]:
                    continue
                for j, edge_j in enumerate(edges):
                    if edge_j[1] == pattern[1]:
                        terms.append((layout.pair(layer, i, j), 1))
            terms.append((layout.pair_query(variable, pattern), -1))
            yield "pair_repeated_query", (layer, variable) + pattern, tuple(terms), 0
        for position in range(K):
            for bit in (0, 1):
                terms = [
                    (layout.unary(layer, position, edge), 1)
                    for edge, data in enumerate(edges) if data[1] == bit
                ]
                terms.append((layout.unary_query(variable, position, bit), -1))
                yield "unary_repeated_query", (layer, variable, position, bit), tuple(terms), 0

    # Pair query totals must project to the physically emitted unary totals.
    for variable in range(g19.N_VARIABLES):
        for position in range(K):
            for bit in (0, 1):
                terms = [
                    (layout.pair_query(variable, pattern), 1)
                    for pattern in PAIR_PATTERNS if pattern[position] == bit
                ]
                terms.append((layout.unary_query(variable, position, bit), -1))
                yield "query_marginal", (variable, position, bit), tuple(terms), 0


def lift_selector(layout: Layout, base_selector, base_query_offset, mode="diagonal"):
    """Lift a one-flow by its pure moment or its signed diagonal embedding."""
    assert mode in ("tensor", "diagonal")
    selector = {}
    old_layers = g19.build_layout(layout.program)[0]
    for layer, edges in enumerate(layout.edges):
        old_layer = old_layers[layer]
        values = base_selector[old_layer["offset"]:old_layer["offset"] + len(edges)]
        for i, first in enumerate(values):
            if first:
                selector[layout.unary(layer, 0, i)] = first
                selector[layout.unary(layer, 1, i)] = first
            for j, second in enumerate(values):
                value = first * second if mode == "tensor" else (first if i == j else 0)
                if value:
                    selector[layout.pair(layer, i, j)] = value
    for variable in range(g19.N_VARIABLES):
        one = base_selector[base_query_offset + variable]
        branch = (1 - one, one)
        for pattern in PAIR_PATTERNS:
            value = branch[pattern[0]] * branch[pattern[1]]
            if value:
                selector[layout.pair_query(variable, pattern)] = value
        for position in range(K):
            for bit in (0, 1):
                value = branch[bit]
                if value:
                    selector[layout.unary_query(variable, position, bit)] = value
    return selector


def dot(terms, selector):
    return sum(coefficient * selector.get(index, 0) for index, coefficient in terms)


def audit_instance(layout, selector, require_zero=True):
    digest = hashlib.sha256()
    counts = Counter()
    residual_counts = Counter()
    residual_square = 0
    row_count = 0
    digest.update(
        f"anchor=2I,target=1,residual_scale={RESIDUAL_SCALE},rank={layout.rank}\n".encode()
    )
    for kind, metadata, terms, rhs in emitted_rows(layout):
        row_count += 1
        counts[kind] += 1
        residual = dot(terms, selector) - rhs
        if residual:
            residual_counts[kind] += 1
            residual_square += residual * residual
        payload = [kind, list(metadata), [list(term) for term in terms], rhs]
        digest.update(json.dumps(payload, separators=(",", ":")).encode() + b"\n")
    if require_zero:
        assert not residual_counts, residual_counts
    return (
        row_count,
        dict(sorted(counts.items())),
        digest.hexdigest(),
        dict(sorted(residual_counts.items())),
        residual_square,
    )


def anchor_cost(rank, selector):
    return rank + 8 * sum(value * (value - 1) // 2 for value in selector.values())


def main():
    manifest = json.loads(g19.MANIFEST_PATH.read_text())
    unsat_program, _, unsat_query_offset, dimension, unsat_checks = g19.reconstruct(
        manifest["instances"][0]
    )
    control_program, _, control_query_offset, control_dimension, control_checks = g19.reconstruct(
        manifest["instances"][1]
    )
    assert dimension == control_dimension == 22754

    # Re-run the exact unrestricted Generation-19 low-weight search.  This is
    # the adversarial seed search: no accepting flow has excess <=8, and the
    # reconstructed minimum exact-flow witness has excess 16.
    below = g19.exact_accept_shell_dp(unsat_program, 1, keep_parents=False)
    assert below["minimum_units"] is None
    seed_search = g19.exact_accept_shell_dp(unsat_program, 2, keep_parents=True)
    assert seed_search["minimum_units"] == 2
    seed = tuple(seed_search["selector"])
    assert not any(g19.residual(unsat_checks, seed))
    assert g19.squared_distance(unsat_checks, seed) == dimension + 16
    assert Counter(seed) == Counter({0: 19500, 1: 3252, -1: 2})
    assert seed[unsat_query_offset:] == (0, 0, 0, 0)

    unsat_layout = Layout(unsat_program)
    tensor_seed = lift_selector(unsat_layout, seed, unsat_query_offset, mode="tensor")
    tensor_audit = audit_instance(unsat_layout, tensor_seed, require_zero=False)
    assert tensor_audit[3] == {"transition_diagonal": 14}
    assert tensor_audit[4] == 20
    diagonal_seed = lift_selector(unsat_layout, seed, unsat_query_offset, mode="diagonal")
    unsat_rows, row_counts, unsat_hash, unsat_residuals, unsat_residual2 = audit_instance(
        unsat_layout, diagonal_seed
    )
    assert not unsat_residuals and unsat_residual2 == 0

    control_assignment = (1, 1, 1, 0)
    control_seed, endpoint = g19.honest_path_selector(control_program, control_assignment)
    assert endpoint == g19.ACCEPT_STATE
    assert not any(g19.residual(control_checks, control_seed))
    control_layout = Layout(control_program)
    control_lift = lift_selector(control_layout, control_seed, control_query_offset, mode="diagonal")
    control_rows, control_row_counts, control_hash, control_residuals, control_residual2 = audit_instance(
        control_layout, control_lift
    )
    assert not control_residuals and control_residual2 == 0

    assert unsat_layout.rank == control_layout.rank == 224282
    assert unsat_rows == control_rows == 348451
    assert row_counts == control_row_counts
    assert row_counts == {
        "pair_accept": 25,
        "pair_conservation": 81225,
        "pair_repeated_query": 5200,
        "pair_source": 25,
        "query_marginal": 16,
        "transition_diagonal": 178750,
        "transition_marginal": 45500,
        "unary_accept": 10,
        "unary_conservation": 32490,
        "unary_repeated_query": 5200,
        "unary_source": 10,
    }

    radius2 = control_layout.rank
    assert anchor_cost(control_layout.rank, control_lift) == radius2
    attack_cost2 = anchor_cost(unsat_layout.rank, diagonal_seed)
    assert attack_cost2 == radius2 + 48 == 224330
    assert 3 * attack_cost2 < 4 * radius2       # below 4R_2^2/3
    assert 9 * attack_cost2 < 16 * radius2      # below (4/3)^2 R_2^2

    histogram = Counter(diagonal_seed.values())
    histogram[0] = unsat_layout.rank - len(diagonal_seed)
    print(json.dumps({
        "source": "hash-locked Generation-19 obstruction and control",
        "k": K,
        "program_length": len(unsat_program),
        "lift_rank": unsat_layout.rank,
        "emitted_row_count": unsat_rows,
        "row_count_by_kind": row_counts,
        "unsat_factor_rule_sha256": unsat_hash,
        "control_factor_rule_sha256": control_hash,
        "control_exact_minimum_squared": radius2,
        "control_minimum_reason": "honest zero-residual lift attains the universal odd-anchor lower bound",
        "seed_search": {
            "no_accepting_flow_through_anchor_excess": 8,
            "minimum_exact_flow_anchor_excess": 16,
            "negative_coefficients": 2,
        },
        "pure_tensor_diagonal_row_nonzero_count": tensor_audit[3]["transition_diagonal"],
        "diagonal_splice_coefficient_histogram": dict(sorted(histogram.items())),
        "diagonal_splice_residual_squared": 0,
        "diagonal_splice_squared_cost": attack_cost2,
        "diagonal_splice_anchor_excess": attack_cost2 - radius2,
        "weaker_threshold_comparison": f"3*{attack_cost2} < 4*{radius2}",
        "frontier_threshold_comparison": f"9*{attack_cost2} < 16*{radius2}",
        "finding": "although diagonal rows reject the pure tensor, the signed diagonal embedding survives every emitted k=2 row far below both thresholds",
        "scope": "finite counterexample to this explicit complete raw ordered-pair lift; no exact k=2 optimum or general impossibility theorem claimed",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
