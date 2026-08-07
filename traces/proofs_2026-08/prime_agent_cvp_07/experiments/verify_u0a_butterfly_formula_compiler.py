#!/usr/bin/env python3
"""Finite compiler/verifier for NAND formula trees on the U0a butterfly factor.

The compiler is a deterministic register-machine embedding.  Hypercube-edge
swaps are implemented by COPY_B at the two endpoints; duplication uses
COPY_A/COPY_B; and a formula gate uses NAND on two adjacent live tokens.  It
handles arbitrary binary NAND formula trees whose number of leaf occurrences
fits the chosen power-of-two width.  This file only *certifies finitely* the
exhaustive two-variable family with 2--4 leaves (plus one 8-leaf example).
It is not a CVP soundness or hardness claim.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from functools import lru_cache

from verify_u0a_universal_topology_serializer import (
    gate_value, honest_vector, make_factor, matvec, target_y,
)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def leaves_and_gates(formula):
    """Give leaves and gates stable postorder ids without Python recursion.

    ``results`` is the explicit return-value stack for the old recursive
    traversal.  In particular, token numbering is byte-for-byte unchanged on
    the finite regression family.
    """
    leaves = []
    gates = []
    work = [(formula, False)]
    results = []
    while work:
        f, exiting = work.pop()
        if isinstance(f, int):
            token = f"leaf:{len(leaves)}"
            leaves.append((token, f))
            results.append(token)
        else:
            assert isinstance(f, tuple) and len(f) == 2
            if not exiting:
                work.append((f, True))
                work.append((f[1], False))
                work.append((f[0], False))
            else:
                right = results.pop()
                left = results.pop()
                token = f"gate:{len(gates)}"
                gates.append((token, left, right))
                results.append(token)
    assert len(results) == 1
    return leaves, gates, results[0]


def eval_formula(formula, assignment):
    """Evaluate iteratively in the same postorder used by the compiler."""
    leaves, gates, root = leaves_and_gates(formula)
    values = {token: assignment[v] for token, v in leaves}
    for token, left, right in gates:
        values[token] = 1 - values[left] * values[right]
    return values[root]


def stage_budget(width):
    """Formula-oblivious polynomial padding budget for at most width leaves.

    There are fewer than 2*width logical COPY/NAND operations.  Each uses at
    most log(width) edge operations and waiting for any requested hypercube
    dimension costs at most 2*log(width) physical stages.  The deliberately
    loose bound below is enough for this compiler and is checked at runtime.
    """
    logw = width.bit_length() - 1
    return 4 * width * logw * logw + 2 * logw


def compile_formula(formula, width=None, assert_bit=1):
    """Compile a binary NAND formula to one fixed-depth target program.

    Formula leaves are nonnegative integer variable names.  Only one FREE
    source is allocated per used variable; COPY operations create all repeated
    occurrences, so repeated-variable consistency is not assumed externally.
    """
    assert assert_bit in (0, 1)
    leaves, gates, root = leaves_and_gates(formula)
    assert leaves and all(v >= 0 for _, v in leaves)
    need = max(4, len(leaves))
    if width is None:
        width = 1 << (need - 1).bit_length()
    assert width >= need and width & (width - 1) == 0
    logw = width.bit_length() - 1
    used_vars = sorted({v for _, v in leaves})
    assert len(used_vars) <= width

    # Logical token placement.  Unoccupied lanes may contain physical junk;
    # COPY_A keeps it from affecting any occupied token.
    lane_token = [None] * width
    token_lane = {}
    occurrences = {v: [] for v in used_vars}
    for token, v in leaves:
        occurrences[v].append(token)
    source_lane = {}
    for lane, v in enumerate(used_vars):
        source_lane[v] = lane
        first = occurrences[v][0]
        lane_token[lane] = first
        token_lane[first] = lane

    stages = []
    trace = []
    def current_dim():
        s = len(stages) + 1
        return ((s - 1) // 2) % logw
    def emit_at_dim(dim, modes, event):
        while current_dim() != dim:
            wait_dim = current_dim()
            stages.append(["COPY_A"] * width)
            trace.append({"kind": "WAIT", "dimension": wait_dim})
        stages.append(modes)
        trace.append(event)
    def swap_edge(a, b):
        dim = (a ^ b).bit_length() - 1
        assert a ^ b == 1 << dim
        modes = ["COPY_A"] * width
        modes[a] = modes[b] = "COPY_B"
        emit_at_dim(dim, modes, {"kind": "SWAP", "lanes": [a, b], "dimension": dim})
        ta, tb = lane_token[a], lane_token[b]
        lane_token[a], lane_token[b] = tb, ta
        if ta is not None: token_lane[ta] = b
        if tb is not None: token_lane[tb] = a
    def duplicate(source_token, new_token):
        a = token_lane[source_token]
        free = min(i for i, t in enumerate(lane_token) if t is None)
        dims = [d for d in range(logw) if ((a ^ free) >> d) & 1]
        assert dims
        # Move the source to a neighbor of the selected free lane.
        for dim in dims[:-1]:
            b = a ^ (1 << dim)
            swap_edge(a, b)
            a = b
        dim = dims[-1]
        assert a ^ free == 1 << dim and lane_token[free] is None
        modes = ["COPY_A"] * width
        modes[a] = "COPY_A"
        modes[free] = "COPY_B"  # free reads the source at its B parent
        emit_at_dim(dim, modes, {"kind": "DUPLICATE", "source": source_token,
                                  "new": new_token, "lanes": [a, free], "dimension": dim})
        lane_token[free] = new_token
        token_lane[new_token] = free
    def nand_tokens(left, right, out):
        a, b = token_lane[left], token_lane[right]
        assert a != b
        dims = [d for d in range(logw) if ((a ^ b) >> d) & 1]
        assert dims
        # Move left to a neighbor of right; arbitrary intervening tokens are
        # permuted and their locations are updated exactly.
        for dim in dims[:-1]:
            c = a ^ (1 << dim)
            swap_edge(a, c)
            a = c
        dim = dims[-1]
        assert a ^ b == 1 << dim
        modes = ["COPY_A"] * width
        modes[a] = "NAND"
        modes[b] = "ZERO"       # the second consumed register becomes free
        emit_at_dim(dim, modes, {"kind": "NAND", "inputs": [left, right],
                                  "output": out, "lanes": [a, b], "dimension": dim})
        del token_lane[left]
        del token_lane[right]
        lane_token[a] = out
        lane_token[b] = None
        token_lane[out] = a

    # Make one token for every repeated variable occurrence.
    for v in used_vars:
        base = occurrences[v][0]
        for token in occurrences[v][1:]:
            duplicate(base, token)
    # Postorder evaluation consumes two child tokens and creates one parent.
    for out, left, right in gates:
        nand_tokens(left, right, out)
    assert set(token_lane) == {root}
    output_lane = token_lane[root]

    # Pad before a final cleanup.  Thus all unused output lanes are constants,
    # and the target asks only that the formula root equal assert_bit.
    budget = stage_budget(width)
    assert len(stages) < budget, (len(stages), budget)
    while len(stages) < budget - 1:
        stages.append(["COPY_A"] * width)
        trace.append({"kind": "PAD", "dimension": current_dim()})
    cleanup = ["ZERO"] * width
    cleanup[output_lane] = "COPY_A"
    stages.append(cleanup)
    trace.append({"kind": "CLEANUP", "output_lane": output_lane})
    assert len(stages) == budget

    source_modes = ["FIX0"] * width
    for v, lane in source_lane.items():
        source_modes[lane] = "FREE"
    modes = {(s + 1, lane): stages[s][lane]
             for s in range(budget) for lane in range(width)}
    outputs = [0] * width
    outputs[output_lane] = assert_bit
    return {
        "formula": formula, "width": width, "gate_stages": budget,
        "assert_bit": assert_bit, "used_vars": used_vars,
        "source_lane": source_lane, "source_modes": source_modes,
        "modes": modes, "outputs": outputs, "output_lane": output_lane,
        "raw_events": sum(t["kind"] not in ("WAIT", "PAD") for t in trace),
        "swap_events": sum(t["kind"] == "SWAP" for t in trace),
        "trace": trace,
    }


def compile_formula_dry_run(formula, width=None, assert_bit=1):
    """Schedule a formula without allocating the padded ``width * depth`` grid.

    This executes the same token-placement decisions as :func:`compile_formula`
    but stores only O(width + syntax-size) state.  Padding is represented by a
    count.  It is therefore the appropriate totality check for large inputs;
    it is *not* an emitted factor or a CVP soundness certificate.
    """
    assert assert_bit in (0, 1)
    leaves, gates, root = leaves_and_gates(formula)
    assert leaves and all(v >= 0 for _, v in leaves)
    need = max(4, len(leaves))
    if width is None:
        width = 1 << (need - 1).bit_length()
    assert width >= need and width & (width - 1) == 0
    logw = width.bit_length() - 1
    used_vars = sorted({v for _, v in leaves})
    assert len(used_vars) <= width

    lane_token = [None] * width
    token_lane = {}
    occurrences = {v: [] for v in used_vars}
    for token, v in leaves:
        occurrences[v].append(token)
    source_lane = {}
    for lane, v in enumerate(used_vars):
        source_lane[v] = lane
        first = occurrences[v][0]
        lane_token[lane] = first
        token_lane[first] = lane

    stage_count = 0
    event_counts = {"WAIT": 0, "SWAP": 0, "DUPLICATE": 0, "NAND": 0}
    trace_hasher = hashlib.sha256()
    mode_overrides = []  # sorted [stage,lane,mode], default is COPY_A

    def current_dim():
        return (stage_count // 2) % logw

    def record(kind, event, overrides=()):
        nonlocal stage_count
        stage_count += 1
        event_counts[kind] += 1
        for lane, mode in sorted(overrides):
            assert mode != "COPY_A"
            mode_overrides.append([stage_count, lane, mode])
        # Length framing makes this an unambiguous streaming transcript.
        encoded = canonical(event).encode("ascii")
        trace_hasher.update(len(encoded).to_bytes(8, "big"))
        trace_hasher.update(encoded)

    def emit_at_dim(dim, event, overrides=()):
        while current_dim() != dim:
            record("WAIT", {"kind": "WAIT", "dimension": current_dim()})
        record(event["kind"], event, overrides)

    def swap_edge(a, b):
        dim = (a ^ b).bit_length() - 1
        assert a ^ b == 1 << dim
        emit_at_dim(dim, {"kind": "SWAP", "lanes": [a, b], "dimension": dim},
                    [(a, "COPY_B"), (b, "COPY_B")])
        ta, tb = lane_token[a], lane_token[b]
        lane_token[a], lane_token[b] = tb, ta
        if ta is not None:
            token_lane[ta] = b
        if tb is not None:
            token_lane[tb] = a

    def duplicate(source_token, new_token):
        a = token_lane[source_token]
        free = min(i for i, t in enumerate(lane_token) if t is None)
        dims = [d for d in range(logw) if ((a ^ free) >> d) & 1]
        assert dims
        for dim in dims[:-1]:
            b = a ^ (1 << dim)
            swap_edge(a, b)
            a = b
        dim = dims[-1]
        assert a ^ free == 1 << dim and lane_token[free] is None
        emit_at_dim(dim, {"kind": "DUPLICATE", "source": source_token,
                          "new": new_token, "lanes": [a, free], "dimension": dim},
                    [(free, "COPY_B")])
        lane_token[free] = new_token
        token_lane[new_token] = free

    def nand_tokens(left, right, out):
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
        emit_at_dim(dim, {"kind": "NAND", "inputs": [left, right],
                          "output": out, "lanes": [a, b], "dimension": dim},
                    [(a, "NAND"), (b, "ZERO")])
        del token_lane[left]
        del token_lane[right]
        lane_token[a] = out
        lane_token[b] = None
        token_lane[out] = a

    for v in used_vars:
        base = occurrences[v][0]
        for token in occurrences[v][1:]:
            duplicate(base, token)
    for out, left, right in gates:
        nand_tokens(left, right, out)
    assert set(token_lane) == {root}
    output_lane = token_lane[root]

    raw_stage_count = stage_count
    budget = stage_budget(width)
    assert raw_stage_count < budget, (raw_stage_count, budget)
    pad_stages = budget - raw_stage_count - 1
    # CLEANUP is the last physical stage, but deliberately is not expanded to
    # a width-entry modes row in this dry run.
    event_counts["CLEANUP"] = 1
    for lane in range(width):
        if lane != output_lane:
            mode_overrides.append([budget, lane, "ZERO"])
    assert mode_overrides == sorted(mode_overrides)
    assert len({(a, b) for a, b, _ in mode_overrides}) == len(mode_overrides)
    return {
        "schema": "u0a-butterfly-program-dry-run-v1",
        "materialized": False,
        "width": width,
        "gate_stages": budget,
        "assert_bit": assert_bit,
        "leaf_occurrences": len(leaves),
        "nand_gates": len(gates),
        "used_vars": used_vars,
        "source_lane": source_lane,
        "output_lane": output_lane,
        "raw_stage_count_before_padding": raw_stage_count,
        "pad_stages": pad_stages,
        "event_counts": event_counts,
        "raw_events": (event_counts["SWAP"] + event_counts["DUPLICATE"]
                       + event_counts["NAND"] + 1),
        "unpadded_trace_sha256": trace_hasher.hexdigest(),
        "default_gate_mode": "COPY_A",
        "mode_overrides": mode_overrides,
        "source_modes": ["FREE" if lane in set(source_lane.values()) else "FIX0"
                         for lane in range(width)],
        "outputs": [assert_bit if lane == output_lane else 0
                    for lane in range(width)],
        "omitted": ["formula", "modes", "trace",
                    "factor_C", "factor_D", "target_y"],
    }


def simulate(program, assignment):
    w, L = program["width"], program["gate_stages"]
    vals = {}
    inverse = {lane: v for v, lane in program["source_lane"].items()}
    for lane in range(w):
        vals[(0, lane)] = assignment[inverse[lane]] if lane in inverse else 0
    logw = w.bit_length() - 1
    for s in range(1, L + 1):
        off = 1 << (((s - 1) // 2) % logw)
        for lane in range(w):
            a = vals[(s - 1, lane)]
            b = vals[(s - 1, lane ^ off)]
            vals[(s, lane)] = gate_value(program["modes"][(s, lane)], a, b)
    return vals


@lru_cache(None)
def formulas(exact_leaves, variables=2):
    if exact_leaves == 1:
        return tuple(range(variables))
    ans = []
    for left_n in range(1, exact_leaves):
        right_n = exact_leaves - left_n
        for a in formulas(left_n, variables):
            for b in formulas(right_n, variables):
                ans.append((a, b))
    return tuple(ans)


def verify_program(payload, program, assignment):
    vals = simulate(program, assignment)
    actual = vals[(program["gate_stages"], program["output_lane"])]
    expected = eval_formula(program["formula"], assignment)
    assert actual == expected
    # Cleanup makes every non-root output exactly zero.
    for lane in range(program["width"]):
        if lane != program["output_lane"]:
            assert vals[(program["gate_stages"], lane)] == 0
    z = honest_vector(payload, program["source_modes"], program["modes"], vals)
    t = target_y(payload, program["source_modes"], program["modes"], program["outputs"])
    Cz = matvec(payload["C"]["shape"], payload["C"]["entries"], z)
    mismatches = []
    for i, row in enumerate(payload["row_marks"]):
        if row["kind"] == "PHYSICAL_SELECTOR":
            assert Cz[i] - t[i] == z[row["selector_column"]]
        elif Cz[i] != t[i]:
            mismatches.append((row["kind"], row["id"], Cz[i] - t[i]))
    if expected == program["assert_bit"]:
        assert mismatches == []
    else:
        assert mismatches == [("OUTPUT_INTERFACE", f"output:{program['output_lane']}",
                               expected - program["assert_bit"])]
    m, _ = payload["C"]["shape"]
    assert matvec(payload["D"]["shape"], payload["D"]["entries"], Cz + z) == [0] * m
    node_count = program["width"] * (program["gate_stages"] + 1)
    energy = sum((a - b) ** 2 for a, b in zip(Cz, t))
    assert energy == node_count + (expected - program["assert_bit"]) ** 2
    return expected, energy


def main():
    family = [f for n in range(2, 5) for f in formulas(n, 2)]
    assert len(family) == 100
    # Explicitly ensure the family contains balanced branching and genuine
    # repeated-variable reconvergence, rather than only chains.
    witness = ((0, 1), (0, 1))
    assert witness in family

    programs = [compile_formula(f, width=4, assert_bit=1) for f in family]
    depths = {p["gate_stages"] for p in programs}
    assert depths == {stage_budget(4)}
    payload, _, _ = make_factor(4, stage_budget(4))
    fixed_targets = None
    assignments_checked = 0
    satisfying = 0
    false = 0
    max_swaps = 0
    target_hashes = []
    for p in programs:
        t = target_y(payload, p["source_modes"], p["modes"], p["outputs"])
        fixed = tuple(t[r["index"]] for r in payload["row_marks"]
                      if r["kind"] not in {"SOURCE_PROGRAM", "GATE_PROGRAM", "OUTPUT_INTERFACE"})
        if fixed_targets is None: fixed_targets = fixed
        assert fixed == fixed_targets
        target_hashes.append(hashlib.sha256(bytes(t)).hexdigest())
        max_swaps = max(max_swaps, p["swap_events"])
        for bits in itertools.product((0, 1), repeat=2):
            e, _ = verify_program(payload, p, dict(enumerate(bits)))
            assignments_checked += 1
            satisfying += e
            false += 1 - e

    # A separate width-8, 8-leaf balanced example exercises three butterfly
    # dimensions and both fanout and branching.  This is one more finite case.
    f8 = (((0, 1), (2, 0)), ((1, 2), (0, 2)))
    p8 = compile_formula(f8, width=8, assert_bit=1)
    payload8, _, _ = make_factor(8, stage_budget(8))
    checks8 = 0
    for bits in itertools.product((0, 1), repeat=3):
        verify_program(payload8, p8, dict(enumerate(bits)))
        checks8 += 1

    summary = {
        "finite_claim_only": True,
        "width4_formula_count": len(family),
        "width4_assignments_checked": assignments_checked,
        "width4_satisfying_evaluations": satisfying,
        "width4_false_evaluations": false,
        "width4_gate_stages": stage_budget(4),
        "width4_factor_shape_C": payload["C"]["shape"],
        "width4_max_swap_events": max_swaps,
        "width4_distinct_target_hashes": len(set(target_hashes)),
        "branching_reconvergent_witness": canonical(witness),
        "width8_assignments_checked": checks8,
        "width8_gate_stages": stage_budget(8),
        "width8_factor_shape_C": payload8["C"]["shape"],
        "limitation": "finite completeness/evaluation only; false outputs cost only additive 1 and unrestricted integer soundness is not audited",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("PASS: deterministic butterfly COPY/NAND compiler on the declared finite formula family")


if __name__ == "__main__":
    main()
