#!/usr/bin/env python3
"""Canonical constant-buffer emitter for the complete Generation-13 factor.

This verifier repairs the *implementation* failure exhibited by
``verify_u0a_eager_materialization_resource_counterexample.py``.  It emits the
row/column marks, sparse ``C``, systematic ``D=[I|-C]``, target, and padded
program in their eager canonical order.  Matrix triples are consumed directly
by SHA-256/count sinks; no list of triples, rows, columns, or target entries is
built.  A small formula is allowed to retain its dense padded program: that is
made explicit in the returned scope/count fields.

The claims here are finite.  Exact entry-by-entry agreement with ``make_factor``
is checked at S=4, and a fresh S=16 process completes under RLIMIT_AS=256 MiB.
This is not a universal space theorem, a butterfly correctness proof, CVP
soundness, or a gap result.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import resource
import subprocess
import sys
from pathlib import Path

from verify_u0a_butterfly_formula_compiler import compile_formula
from verify_u0a_canonical_serialize_manifest import (
    decode_formula, digest_obj, encode_formula, exact_count_model,
    formula_statistics, padding_for_S, program_record,
)
from verify_u0a_universal_topology_serializer import (
    GATE_MODES, SOURCE_MODES, gate_value, make_factor, target_y,
)

CAP_MIB = 256


def canonical_bytes(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def _source_states():
    # Exact make_factor order: mode, then legal bit.
    for mode in SOURCE_MODES:
        for bit in (0, 1):
            if mode == "FREE" or (mode == "FIX0" and bit == 0) or (mode == "FIX1" and bit == 1):
                yield mode, bit


def _gate_states():
    # Exact make_factor order: mode, a, b.
    for mode in GATE_MODES:
        for a in (0, 1):
            for b in (0, 1):
                yield mode, a, b, gate_value(mode, a, b)


SOURCE_STATES = tuple(_source_states())
GATE_STATES = tuple(_gate_states())


def column_index(width, stage, lane, local):
    if stage == 0:
        return 4 * lane + local
    return 4 * width + 20 * ((stage - 1) * width + lane) + local


def iter_column_marks(width, depth):
    j = 0
    for lane in range(width):
        for mode, bit in SOURCE_STATES:
            yield {"index": j, "id": f"src:{lane}:{mode}:{bit}",
                   "kind": "SOURCE_SELECTOR", "stage": 0, "lane": lane,
                   "state": {"mode": mode, "bit": bit},
                   "physical_selector": True}
            j += 1
    for stage in range(1, depth + 1):
        for lane in range(width):
            for mode, a, b, c in GATE_STATES:
                yield {"index": j, "id": f"gate:{stage}:{lane}:{mode}:{a}{b}{c}",
                       "kind": "GATE_SELECTOR", "stage": stage, "lane": lane,
                       "state": {"mode": mode, "a": a, "b": b, "c": c},
                       "physical_selector": True}
                j += 1


def iter_row_marks(width, depth):
    logw = width.bit_length() - 1
    i = 0
    for stage in range(depth + 1):
        nk = "source" if stage == 0 else "gate"
        for lane in range(width):
            yield {"index": i, "id": f"norm:{stage}:{lane}",
                   "kind": "NORM_DROP_GUARD", "target_role": "FIXED_ONE",
                   "stage": stage, "lane": lane, "node_kind": nk,
                   "drop_guard": True}
            i += 1
    for lane in range(width):
        for mode in SOURCE_MODES:
            yield {"index": i, "id": f"srcprog:{lane}:{mode}",
                   "kind": "SOURCE_PROGRAM", "target_role": "PROGRAM_BIT",
                   "stage": 0, "lane": lane, "mode": mode}
            i += 1
    for stage in range(1, depth + 1):
        for lane in range(width):
            for mode in GATE_MODES:
                yield {"index": i, "id": f"gateprog:{stage}:{lane}:{mode}",
                       "kind": "GATE_PROGRAM", "target_role": "PROGRAM_BIT",
                       "stage": stage, "lane": lane, "mode": mode}
                i += 1
    for stage in range(1, depth + 1):
        off = 1 << (((stage - 1) // 2) % logw)
        for lane in range(width):
            for port, parent_lane in (("A", lane), ("B", lane ^ off)):
                yield {"index": i, "id": f"edge:{stage}:{lane}:{port}",
                       "kind": "EDGE_CONSISTENCY", "target_role": "FIXED_ZERO",
                       "stage": stage, "lane": lane, "port": port,
                       "parent_stage": stage - 1, "parent_lane": parent_lane,
                       "offset": off}
                i += 1
    for stage in range(1, depth + 1):
        for port in ("A", "B"):
            for q in range(1, logw + 1):
                size = 1 << q
                for start in range(0, width, size):
                    yield {"index": i, "id": f"sep:{stage}:{port}:{size}:{start}",
                           "kind": "DYADIC_SEPARATOR", "target_role": "FIXED_ZERO",
                           "stage": stage, "port": port, "block_start": start,
                           "block_size": size, "redundant_sum_of_edges": True}
                    i += 1
    for lane in range(width):
        yield {"index": i, "id": f"output:{lane}",
               "kind": "OUTPUT_INTERFACE", "target_role": "OUTPUT_BIT",
               "stage": depth, "lane": lane}
        i += 1
    for col in iter_column_marks(width, depth):
        j = col["index"]
        yield {"index": i, "id": f"physical:{j}",
               "kind": "PHYSICAL_SELECTOR", "target_role": "FIXED_ZERO",
               "selector_column": j, "selector_id": col["id"],
               "physical_coordinate": True}
        i += 1


def _selected_node_columns(width, stage, lane, field=None, mode=None):
    """Yield (column,value) in increasing column order, omitting zeros."""
    if stage == 0:
        for local, (smode, bit) in enumerate(SOURCE_STATES):
            if mode is not None:
                value = int(smode == mode)
            elif field == "out":
                value = bit
            else:  # normalization
                value = 1
            if value:
                yield column_index(width, stage, lane, local), value
    else:
        for local, (gmode, a, b, c) in enumerate(GATE_STATES):
            if mode is not None:
                value = int(gmode == mode)
            elif field == "a":
                value = a
            elif field == "b":
                value = b
            elif field == "out":
                value = c
            else:  # normalization
                value = 1
            if value:
                yield column_index(width, stage, lane, local), value


def iter_C_entries(width, depth):
    """Yield eager-canonical ``[row,column,value]`` triples with O(1) buffering."""
    logw = width.bit_length() - 1
    row = 0
    # Normalization rows.
    for stage in range(depth + 1):
        for lane in range(width):
            for j, v in _selected_node_columns(width, stage, lane):
                yield [row, j, v]
            row += 1
    # Source program rows.
    for lane in range(width):
        for mode in SOURCE_MODES:
            for j, v in _selected_node_columns(width, 0, lane, mode=mode):
                yield [row, j, v]
            row += 1
    # Gate program rows.
    for stage in range(1, depth + 1):
        for lane in range(width):
            for mode in GATE_MODES:
                for j, v in _selected_node_columns(width, stage, lane, mode=mode):
                    yield [row, j, v]
                row += 1
    # Edge rows.  Previous-stage columns precede current-stage columns.
    for stage in range(1, depth + 1):
        off = 1 << (((stage - 1) // 2) % logw)
        for lane in range(width):
            for port, parent_lane in (("A", lane), ("B", lane ^ off)):
                for j, v in _selected_node_columns(width, stage - 1, parent_lane, field="out"):
                    yield [row, j, -v]
                for j, v in _selected_node_columns(width, stage, lane, field=port.lower()):
                    yield [row, j, v]
                row += 1
    # Separator rows.  Sort by actual column, not by the child-lane order of
    # their constituent edges; this is the subtle ordering used by make_factor.
    for stage in range(1, depth + 1):
        off = 1 << (((stage - 1) // 2) % logw)
        for port in ("A", "B"):
            for q in range(1, logw + 1):
                size = 1 << q
                for start in range(0, width, size):
                    stop = start + size
                    for parent_lane in range(width):
                        child_lane = parent_lane if port == "A" else parent_lane ^ off
                        if start <= child_lane < stop:
                            for j, v in _selected_node_columns(width, stage - 1, parent_lane, field="out"):
                                yield [row, j, -v]
                    for child_lane in range(start, stop):
                        for j, v in _selected_node_columns(width, stage, child_lane, field=port.lower()):
                            yield [row, j, v]
                    row += 1
    # Outputs.
    for lane in range(width):
        for j, v in _selected_node_columns(width, depth, lane, field="out"):
            yield [row, j, v]
        row += 1
    # Explicit physical selector identity rows.
    k = 4 * width + 20 * width * depth
    for j in range(k):
        yield [row, j, 1]
        row += 1
    m, _ = exact_count_model(width, depth)
    assert row == m


def iter_D_entries(width, depth):
    """Yield systematic D in sorted eager order (provided as a public API)."""
    m, _ = exact_count_model(width, depth)
    source = iter(iter_C_entries(width, depth))
    c = next(source, None)
    for i in range(m):
        yield [i, i, 1]
        while c is not None and c[0] == i:
            yield [i, m + c[1], -c[2]]
            c = next(source, None)
    assert c is None


def iter_target(width, depth, p):
    for r in iter_row_marks(width, depth):
        kind = r["kind"]
        if kind == "NORM_DROP_GUARD":
            yield 1
        elif kind in ("EDGE_CONSISTENCY", "DYADIC_SEPARATOR", "PHYSICAL_SELECTOR"):
            yield 0
        elif kind == "SOURCE_PROGRAM":
            yield int(p["source_modes"][r["lane"]] == r["mode"])
        elif kind == "GATE_PROGRAM":
            yield int(p["modes"][(r["stage"], r["lane"])] == r["mode"])
        elif kind == "OUTPUT_INTERFACE":
            yield p["outputs"][r["lane"]]
        else:
            raise AssertionError(kind)


def _hash_list(items):
    h = hashlib.sha256()
    h.update(b"[")
    count = 0
    for item in items:
        if count:
            h.update(b",")
        h.update(canonical_bytes(item))
        count += 1
    h.update(b"]")
    return h.hexdigest(), count


def _triple_bytes(t):
    # All emitted entries are small signed decimal integers.  This is exactly
    # json.dumps([i,j,v], separators=(",", ":")) but avoids temporary dicts.
    return f"[{t[0]},{t[1]},{t[2]}]".encode("ascii")


def hash_C_and_D(width, depth):
    """Hash both matrices in one pass over C; retain no matrix triple."""
    m, k = exact_count_model(width, depth)
    hc, hd = hashlib.sha256(), hashlib.sha256()
    hc.update(b'{"entries":[')
    hd.update(b'{"entries":[')
    cn = dn = 0
    next_identity = 0
    for c in iter_C_entries(width, depth):
        if cn:
            hc.update(b",")
        hc.update(_triple_bytes(c))
        cn += 1
        while next_identity <= c[0]:
            if dn:
                hd.update(b",")
            hd.update(_triple_bytes([next_identity, next_identity, 1]))
            dn += 1
            next_identity += 1
        d = [c[0], m + c[1], -c[2]]
        hd.update(b",")  # that row's identity was already emitted
        hd.update(_triple_bytes(d))
        dn += 1
    while next_identity < m:
        if dn:
            hd.update(b",")
        hd.update(_triple_bytes([next_identity, next_identity, 1]))
        dn += 1
        next_identity += 1
    hc.update(b'],"shape":' + canonical_bytes([m, k]) + b"}")
    hd.update(b'],"shape":' + canonical_bytes([m, m + k]) + b"}")
    return hc.hexdigest(), cn, hd.hexdigest(), dn


def hash_program_stream(p):
    """Hash the canonical program object without constructing program_record."""
    h = hashlib.sha256()
    # json sort_keys order: assert_bit, gate_modes_stage_major, output_lane,
    # outputs, source_modes.
    h.update(b'{"assert_bit":' + str(p["assert_bit"]).encode("ascii"))
    h.update(b',"gate_modes_stage_major":[')
    w, d = p["width"], p["gate_stages"]
    for stage in range(1, d + 1):
        if stage > 1:
            h.update(b",")
        h.update(b"[")
        for lane in range(w):
            if lane:
                h.update(b",")
            h.update(canonical_bytes(p["modes"][(stage, lane)]))
        h.update(b"]")
    h.update(b'],"output_lane":' + str(p["output_lane"]).encode("ascii"))
    h.update(b',"outputs":')
    h.update(canonical_bytes(p["outputs"]))
    h.update(b',"source_modes":')
    h.update(canonical_bytes(p["source_modes"]))
    h.update(b"}")
    return h.hexdigest(), w * d


def stream_serialize(S, encoded_formula):
    """Consume the complete canonical serialization into hashes and counts."""
    f = decode_formula(encoded_formula)
    stats = formula_statistics(f)
    if stats["leaf_occurrences"] > S:
        raise ValueError("formula exceeds S")
    if stats["variables"] and stats["variables"][-1] >= S:
        raise ValueError("variable outside [0,S)")
    width, depth = padding_for_S(S)
    p = compile_formula(f, width=width, assert_bit=1)
    m, k = exact_count_model(width, depth)

    rows_hash, rows_count = _hash_list(iter_row_marks(width, depth))
    cols_hash, cols_count = _hash_list(iter_column_marks(width, depth))
    C_hash, C_nnz, D_hash, D_nnz = hash_C_and_D(width, depth)
    target_hash, target_count = _hash_list(iter_target(width, depth, p))
    program_hash, dense_mode_cells = hash_program_stream(p)
    assert (rows_count, cols_count, target_count) == (m, k, m)
    return {
        "schema": "u0a-canonical-stream-summary-v1",
        "S": S, "width": width, "gate_stages": depth,
        "C_shape": [m, k], "D_shape": [m, m + k],
        "rows_sha256": rows_hash, "rows_count": rows_count,
        "columns_sha256": cols_hash, "columns_count": cols_count,
        "C_sha256": C_hash, "C_nnz": C_nnz,
        "D_sha256": D_hash, "D_nnz": D_nnz,
        "target_y_sha256": target_hash, "target_count": target_count,
        "program_sha256": program_hash,
        "dense_program_mode_cells_retained": dense_mode_cells,
        "matrix_triples_retained": 0,
        "scope": ("finite canonical emission/count/hash; factor, row/column marks, "
                  "and target stream with O(1) emitter buffering; the small formula's "
                  "dense padded program is retained; no universal space/correctness, "
                  "CVP soundness, or approximation-gap claim"),
    }


def _assert_iter_equal(got, expected):
    sentinel = object()
    for n, (a, b) in enumerate(itertools.zip_longest(got, expected, fillvalue=sentinel)):
        assert a is not sentinel and b is not sentinel and a == b, (n, a, b)


def limited_child():
    cap = CAP_MIB * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    summary = stream_serialize(16, encode_formula((0, 1)))
    assert summary["C_shape"] == [493440, 330304]
    assert summary["D_shape"] == [493440, 823744]
    assert summary["matrix_triples_retained"] == 0
    assert summary["dense_program_mode_cells_retained"] == 16 * 1032
    print("STREAM_S16_OK " + json.dumps(summary, sort_keys=True, separators=(",", ":")))
    return 0


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--limited-child":
        raise SystemExit(limited_child())
    assert len(sys.argv) == 1

    # Exact small-instance oracle comparison, not merely shape agreement.
    encoded = encode_formula((0, 1))
    summary = stream_serialize(4, encoded)
    factor, _, _ = make_factor(4, 68)
    p = compile_formula((0, 1), width=4, assert_bit=1)
    eager_target = target_y(factor, p["source_modes"], p["modes"], p["outputs"])
    eager_program = program_record(p)

    _assert_iter_equal(iter_row_marks(4, 68), factor["row_marks"])
    _assert_iter_equal(iter_column_marks(4, 68), factor["column_marks"])
    _assert_iter_equal(iter_C_entries(4, 68), factor["C"]["entries"])
    _assert_iter_equal(iter_D_entries(4, 68), factor["D"]["entries"])
    _assert_iter_equal(iter_target(4, 68, p), eager_target)
    assert summary["rows_sha256"] == factor["component_hashes"]["rows"]
    assert summary["columns_sha256"] == factor["component_hashes"]["columns"]
    assert summary["C_sha256"] == factor["component_hashes"]["C"]
    assert summary["D_sha256"] == factor["component_hashes"]["D"]
    assert summary["target_y_sha256"] == digest_obj(eager_target)
    assert summary["program_sha256"] == digest_obj(eager_program)
    assert summary["C_nnz"] == len(factor["C"]["entries"])
    assert summary["D_nnz"] == len(factor["D"]["entries"])

    # Fresh process: the address-space limit is applied before any factor work.
    proc = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "--limited-child"],
        text=True, capture_output=True, timeout=240,
    )
    assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
    line = next(x for x in proc.stdout.splitlines() if x.startswith("STREAM_S16_OK "))
    summary16 = json.loads(line.split(" ", 1)[1])
    assert summary16["C_nnz"] > 0 and summary16["D_nnz"] == summary16["C_nnz"] + 493440

    print("PASS canonical streaming emitter")
    print("S=4 exact eager agreement:", json.dumps(summary, sort_keys=True))
    print("S=16 under 256 MiB:", json.dumps(summary16, sort_keys=True))
    print("Scope: finite resource/canonical-order repair only; dense small-formula program retained; no universal theorem, soundness, or gap.")


if __name__ == "__main__":
    main()
