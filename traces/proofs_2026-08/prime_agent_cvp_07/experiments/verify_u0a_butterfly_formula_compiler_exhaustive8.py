#!/usr/bin/env python3
"""Finite breaker audit of the U0a formula compiler's token scheduler.

Exhausts every ordered full binary tree with at most 8 leaves and every
variable-equality pattern on those leaves (restricted-growth strings).  Thus
variable *names* are quotiented out but all patterns of repeated occurrences
are retained.  It independently executes the placement/duplicate/routing/NAND
logic with packed truth tables and counts the exact physical stages generated
by emit_at_dim.  Selected worst-stage witnesses are then passed through the
actual compile_formula/simulate implementation.

This is finite evidence only, not a proof for arbitrary formula size.
"""
from __future__ import annotations

import itertools
import json
from functools import lru_cache

from verify_u0a_butterfly_formula_compiler import (
    compile_formula, eval_formula, simulate, stage_budget,
)


@lru_cache(None)
def shapes(n):
    if n == 1:
        return ("L",)
    return tuple((a, b)
                 for left_n in range(1, n)
                 for a in shapes(left_n)
                 for b in shapes(n - left_n))


@lru_cache(None)
def equality_patterns(n):
    """Canonical restricted-growth strings, one per set partition."""
    if n == 0:
        return ((),)
    ans = []
    for prefix in equality_patterns(n - 1):
        for x in range(max(prefix, default=-1) + 2):
            ans.append(prefix + (x,))
    return tuple(ans)


def gate_schedule(shape):
    leaves = []
    gates = []

    def visit(node):
        if node == "L":
            token = len(leaves)
            leaves.append(token)
            return token
        a, b = visit(node[0]), visit(node[1])
        token = ("gate", len(gates))
        gates.append((token, a, b))
        return token

    root = visit(shape)
    return gates, root


def as_formula(shape, pattern):
    pos = 0

    def visit(node):
        nonlocal pos
        if node == "L":
            ans = pattern[pos]
            pos += 1
            return ans
        return (visit(node[0]), visit(node[1]))

    ans = visit(shape)
    assert pos == len(pattern)
    return ans


def audit_schedule(shape, pattern):
    """Return exact raw stage count after checking the packed truth table."""
    n = len(pattern)
    width = max(4, 1 << (n - 1).bit_length())
    logw = width.bit_length() - 1
    gates, root = gate_schedule(shape)
    var_count = max(pattern) + 1

    lanes = [None] * width
    token_lane = {}
    occurrences = [[] for _ in range(var_count)]
    for token, var in enumerate(pattern):
        occurrences[var].append(token)

    # One bit for each complete assignment to the equality-pattern variables.
    truth_mask = (1 << (1 << var_count)) - 1
    token_value = {}
    for var in range(var_count):
        value = sum(1 << assignment
                    for assignment in range(1 << var_count)
                    if (assignment >> var) & 1)
        base = occurrences[var][0]
        lanes[var] = base
        token_lane[base] = var
        token_value[base] = value

    stages = 0

    def emit_at_dim(dim):
        nonlocal stages
        while (stages // 2) % logw != dim:
            stages += 1
        stages += 1

    def swap_edge(a, b):
        dim = (a ^ b).bit_length() - 1
        assert a ^ b == 1 << dim
        emit_at_dim(dim)
        ta, tb = lanes[a], lanes[b]
        lanes[a], lanes[b] = tb, ta
        if ta is not None:
            token_lane[ta] = b
        if tb is not None:
            token_lane[tb] = a

    # Same deterministic duplication order as compile_formula.
    for var in range(var_count):
        base = occurrences[var][0]
        for new in occurrences[var][1:]:
            a = token_lane[base]
            free = lanes.index(None)
            dims = [d for d in range(logw) if ((a ^ free) >> d) & 1]
            assert dims
            for dim in dims[:-1]:
                b = a ^ (1 << dim)
                swap_edge(a, b)
                a = b
            dim = dims[-1]
            assert a ^ free == 1 << dim and lanes[free] is None
            emit_at_dim(dim)
            lanes[free] = new
            token_lane[new] = free
            token_value[new] = token_value[base]

    for out, left, right in gates:
        a, b = token_lane[left], token_lane[right]
        assert a != b
        dims = [d for d in range(logw) if ((a ^ b) >> d) & 1]
        assert dims
        for dim in dims[:-1]:
            c = a ^ (1 << dim)
            swap_edge(a, c)
            a = c
        dim = dims[-1]
        assert a ^ b == 1 << dim
        emit_at_dim(dim)
        del token_lane[left]
        del token_lane[right]
        lanes[a] = out
        lanes[b] = None
        token_lane[out] = a
        token_value[out] = truth_mask ^ (token_value[left] & token_value[right])

    assert set(token_lane) == {root}
    assert stages < stage_budget(width)

    # Independent recursive truth-table evaluation of the formula shape.
    leaf_pos = 0

    def expected(node):
        nonlocal leaf_pos
        if node == "L":
            var = pattern[leaf_pos]
            leaf_pos += 1
            return sum(1 << assignment
                       for assignment in range(1 << var_count)
                       if (assignment >> var) & 1)
        return truth_mask ^ (expected(node[0]) & expected(node[1]))

    want = expected(shape)
    assert leaf_pos == n and token_value[root] == want
    return stages


def main():
    total = 0
    by_n = {}
    worst_witnesses = []
    for n in range(1, 9):
        maximum = -1
        witness = None
        count = 0
        for shape in shapes(n):
            for pattern in equality_patterns(n):
                raw = audit_schedule(shape, pattern)
                count += 1
                if raw > maximum:
                    maximum = raw
                    witness = (shape, pattern)
        expected_count = len(shapes(n)) * len(equality_patterns(n))
        assert count == expected_count
        total += count
        by_n[n] = {
            "ordered_shapes": len(shapes(n)),
            "equality_patterns": len(equality_patterns(n)),
            "cases": count,
            "max_raw_stages": maximum,
            "width": max(4, 1 << (n - 1).bit_length()),
            "budget": stage_budget(max(4, 1 << (n - 1).bit_length())),
        }
        worst_witnesses.append(witness)

    # Anchor the independent scheduler audit to the actual implementation on
    # every per-n worst witness, checking every assignment to its variables.
    implementation_assignments = 0
    for shape, pattern in worst_witnesses:
        formula = as_formula(shape, pattern)
        program = compile_formula(formula)
        for bits in itertools.product((0, 1), repeat=max(pattern) + 1):
            assignment = dict(enumerate(bits))
            vals = simulate(program, assignment)
            actual = vals[(program["gate_stages"], program["output_lane"])]
            assert actual == eval_formula(formula, assignment)
            assert all(vals[(program["gate_stages"], lane)] == 0
                       for lane in range(program["width"])
                       if lane != program["output_lane"])
            implementation_assignments += 1

    assert total == 1_901_166
    summary = {
        "finite_claim_only": True,
        "cases": total,
        "by_leaf_count": by_n,
        "actual_implementation_worst_witness_assignments": implementation_assignments,
        "limitation": (
            "exhaustive only through 8 leaves; the full compiler was run only "
            "on the per-size worst-stage witnesses, while the exhaustive core "
            "independently mirrors and audits its token scheduler"
        ),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("PASS: exhaustive <=8-leaf token/equality-pattern audit")


if __name__ == "__main__":
    main()
