#!/usr/bin/env python3
"""Exact finite bridge from a sparse formula program to streamed C and D rows.

For every tested assignment this verifier constructs the one selected local-state
column at every source/gate cell directly from ``compile_formula_sparse``.  It
then consumes the canonical C and D emitters row by row (never materializing a
matrix) and checks normalization, program, edge, separator, output, physical,
and systematic-kernel moments.  In particular this is stronger than checking
only that the last output evaluates the formula: each physical stage is tied to
one actual emitted gate-selector column.  The final cleanup stage is audited
cell by cell.

All claims are finite implementation evidence.  The verifier does not prove a
space bound, compiler correctness for all formulas, CVP soundness, or a gap.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import resource
import subprocess
import sys
from pathlib import Path

from verify_u0a_butterfly_formula_compiler import eval_formula, stage_budget
from verify_u0a_canonical_serialize_manifest import exact_count_model
from verify_u0a_canonical_streaming_emitter import (
    GATE_STATES, SOURCE_STATES, column_index, iter_C_entries, iter_D_entries,
    iter_row_marks,
)
from verify_u0a_sparse_program_stream import (
    compile_formula_sparse, gate_mode_at, iter_gate_modes, iter_target_sparse,
    output_at, source_mode_at,
)
from verify_u0a_universal_topology_serializer import gate_value

CAP_MIB = 256


def row_stream(entries, row_count):
    """Group a sorted triple stream, buffering at most one emitted row."""
    it = iter(entries)
    item = next(it, None)
    for row in range(row_count):
        buf = []
        while item is not None and item[0] == row:
            assert item[2] != 0
            buf.append(item)
            item = next(it, None)
        assert item is None or item[0] > row
        yield buf
    assert item is None


def selected_trace(p, assignment):
    """Return selected column indices and final values using O(width*depth) ids.

    No selector vector of length k, matrix, row-mark list, or dense mode grid is
    retained.  The set has one integer per logical node and is precisely the
    support of the honest selector witness.
    """
    w, depth = p["width"], p["gate_stages"]
    inverse_source = {lane: var for var, lane in p["source_lane"].items()}
    selected = set()
    h = hashlib.sha256()
    prev = []

    # Actual selected source columns.
    for lane in range(w):
        mode = source_mode_at(p, lane)
        bit = assignment[inverse_source[lane]] if lane in inverse_source else 0
        state = (mode, bit)
        assert state in SOURCE_STATES
        local = SOURCE_STATES.index(state)
        j = column_index(w, 0, lane, local)
        assert 4 * lane <= j < 4 * (lane + 1)
        assert j not in selected
        selected.add(j)
        prev.append(bit)
        h.update(f"0:{lane}:{j}:{mode}:{bit};".encode())

    # The program stream, selected gate states, and numerical evolution are
    # consumed together in stage-major order.
    mode_it = iter(iter_gate_modes(p))
    raw_override_coords = {(s, lane): mode for s, lane, mode
                           in p["raw_gate_overrides"]}
    observed_overrides = 0
    cleanup_records = []
    for stage in range(1, depth + 1):
        off = 1 << (((stage - 1) // 2) % (w.bit_length() - 1))
        cur = [0] * w
        stage_columns = []
        for lane in range(w):
            got_stage, got_lane, mode = next(mode_it)
            assert (got_stage, got_lane) == (stage, lane)
            assert mode == gate_mode_at(p, stage, lane)
            if stage < depth and (stage, lane) in raw_override_coords:
                assert mode == raw_override_coords[(stage, lane)] != "COPY_A"
                observed_overrides += 1
            elif stage < depth:
                assert mode == "COPY_A"
            a, b = prev[lane], prev[lane ^ off]
            c = gate_value(mode, a, b)
            cur[lane] = c
            state = (mode, a, b, c)
            assert state in GATE_STATES
            local = GATE_STATES.index(state)
            j = column_index(w, stage, lane, local)
            block = 4 * w + 20 * ((stage - 1) * w + lane)
            assert block <= j < block + 20
            assert j not in selected
            selected.add(j)
            stage_columns.append(j)
            h.update(f"{stage}:{lane}:{j}:{mode}:{a}{b}{c};".encode())
            if stage == depth:
                cleanup_records.append((lane, mode, a, b, c, j))
        # Exactly one actual gate column was selected for each lane this stage.
        assert len(stage_columns) == w and stage_columns == sorted(stage_columns)
        prev = cur
    assert next(mode_it, None) is None
    assert observed_overrides == len(raw_override_coords)

    # Cell-by-cell cleanup semantics, including the selected local-state column.
    assert p["cleanup"] == {
        "stage": depth, "default_mode": "ZERO",
        "overrides": ((p["output_lane"], "COPY_A"),),
    }
    for lane, mode, a, _b, c, j in cleanup_records:
        expected_mode = "COPY_A" if lane == p["output_lane"] else "ZERO"
        assert mode == expected_mode
        assert c == (a if lane == p["output_lane"] else 0)
        assert (j - (4 * w + 20 * ((depth - 1) * w + lane))) // 4 == (
            ("COPY_A", "COPY_B", "NAND", "ZERO", "ONE").index(mode))
    assert len(selected) == w * (depth + 1)
    return selected, prev, h.hexdigest()


def audit_assignment(formula, width, assignment, assert_bit=1):
    p = compile_formula_sparse(formula, width=width, assert_bit=assert_bit)
    w, depth = width, p["gate_stages"]
    m, k = exact_count_model(w, depth)
    selected, final_values, trace_hash = selected_trace(p, assignment)
    assert all(0 <= j < k for j in selected)
    expected_formula = eval_formula(formula, assignment)
    assert final_values[p["output_lane"]] == expected_formula
    assert all(final_values[lane] == 0 for lane in range(w)
               if lane != p["output_lane"])

    crows = row_stream(iter_C_entries(w, depth), m)
    drows = row_stream(iter_D_entries(w, depth), m)
    rows = iter(iter_row_marks(w, depth))
    targets = iter(iter_target_sparse(w, depth, p))
    kind_counts = {}
    energy = 0

    for i, (crow, drow) in enumerate(zip(crows, drows)):
        mark = next(rows)
        target = next(targets)
        assert mark["index"] == i
        assert all(x[0] == i for x in crow + drow)

        # Exact emitted systematic D=[I|-C], checked entry-by-entry.  The D
        # moment on (Cz,z) is consequently zero for this actual streamed row.
        expected_drow = [[i, i, 1]] + [[i, m + j, -v] for _, j, v in crow]
        assert drow == expected_drow
        cmoment = sum(v for _, j, v in crow if j in selected)
        dmoment = cmoment + sum(v for _, j, v in drow[1:]
                                if (j - m) in selected)
        assert dmoment == 0

        kind = mark["kind"]
        kind_counts[kind] = kind_counts.get(kind, 0) + 1
        if kind == "NORM_DROP_GUARD":
            assert cmoment == 1 == target
        elif kind in ("SOURCE_PROGRAM", "GATE_PROGRAM"):
            assert cmoment == target
        elif kind in ("EDGE_CONSISTENCY", "DYADIC_SEPARATOR"):
            assert cmoment == 0 == target
        elif kind == "OUTPUT_INTERFACE":
            assert cmoment == final_values[mark["lane"]]
            assert target == output_at(p, mark["lane"])
        elif kind == "PHYSICAL_SELECTOR":
            assert cmoment == int(mark["selector_column"] in selected)
            assert target == 0
        else:
            raise AssertionError(kind)
        energy += (cmoment - target) ** 2

    assert next(rows, None) is None and next(targets, None) is None
    node_count = w * (depth + 1)
    assert energy == node_count + (expected_formula - assert_bit) ** 2
    assert kind_counts["NORM_DROP_GUARD"] == node_count
    assert kind_counts["GATE_PROGRAM"] == 5 * w * depth
    assert kind_counts["EDGE_CONSISTENCY"] == 2 * w * depth
    assert kind_counts["PHYSICAL_SELECTOR"] == k
    return {
        "width": w, "depth": depth, "rows": m, "columns": k,
        "selected_columns": len(selected), "formula_value": expected_formula,
        "energy": energy, "trace_sha256": trace_hash,
    }


def balanced(leaves):
    if len(leaves) == 1:
        return leaves[0]
    mid = len(leaves) // 2
    return (balanced(leaves[:mid]), balanced(leaves[mid:]))


def limited_child():
    resource.setrlimit(resource.RLIMIT_AS,
                       (CAP_MIB * 1024 * 1024, CAP_MIB * 1024 * 1024))
    # One larger finite pass consumes every C and D entry under the cap.
    f = balanced(tuple(i % 4 for i in range(16)))
    ans = audit_assignment(f, 16, {i: i & 1 for i in range(4)})
    assert ans["selected_columns"] == 16 * (stage_budget(16) + 1)
    print(json.dumps({"limited_child": ans}, sort_keys=True))


def main():
    cases = [
        (0, 1),
        ((0, 1), (0, 1)),                 # balanced reconvergence
        ((0, 1), (1, 0)),                 # asymmetric values/repeated inputs
    ]
    summaries = []
    for formula in cases:
        used = sorted(set(_leaves(formula)))
        for bits in itertools.product((0, 1), repeat=len(used)):
            assignment = dict(zip(used, bits))
            summaries.append(audit_assignment(formula, 4, assignment))

    # Three butterfly dimensions and all eight assignments.
    f8 = (((0, 1), (2, 0)), ((1, 2), (0, 2)))
    for bits in itertools.product((0, 1), repeat=3):
        summaries.append(audit_assignment(f8, 8, dict(enumerate(bits))))

    child = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--limited-child"],
                           text=True, capture_output=True, check=True)
    limited = json.loads(child.stdout)["limited_child"]
    out = {
        "schema": "u0a-sparse-matrix-trace-finite-v1",
        "assignments_checked": len(summaries) + 1,
        "small_widths": sorted({x["width"] for x in summaries}),
        "satisfying": sum(x["formula_value"] for x in summaries),
        "false": sum(1 - x["formula_value"] for x in summaries),
        "all_C_D_rows_checked": sum(x["rows"] for x in summaries) + limited["rows"],
        "limited_child_width": limited["width"],
        "limited_child_selected_columns": limited["selected_columns"],
        "limited_child_trace_sha256": limited["trace_sha256"],
    }
    print(json.dumps(out, sort_keys=True))


def _leaves(formula):
    stack = [formula]
    while stack:
        x = stack.pop()
        if isinstance(x, int):
            yield x
        else:
            stack.extend(reversed(x))


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--limited-child":
        limited_child()
    else:
        assert len(sys.argv) == 1
        main()
