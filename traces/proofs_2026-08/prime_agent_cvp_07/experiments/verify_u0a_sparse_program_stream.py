#!/usr/bin/env python3
"""Canonical sparse program stream for the finite U0a serializer.

COPY_A is the default at every non-cleanup gate cell.  The compiler retains
only nondefault ``(stage,lane,mode)`` overrides for raw scheduled stages,
represents the all-COPY_A padding by a count, and represents the last cleanup
stage by default ZERO plus its one COPY_A output override.  Source and output
vectors likewise use fixed defaults with ordered overrides.

The verifier compares the dense-equivalent program record and target entry by
entry with the existing eager implementation at small S.  A fresh process at
S=128, under RLIMIT_AS=256 MiB, hashes the entire 3,213,056-cell logical
program and opens/consumes canonical C, D, and target streams without ever
constructing the dense modes dictionary.

This is finite implementation/resource evidence.  In particular, the S=128
factor and target streams are sampled, not exhaustively emitted or hashed; no
universal space theorem, compiler proof, CVP soundness, or gap is claimed.
"""
from __future__ import annotations

import bisect
import hashlib
import itertools
import json
import resource
import subprocess
import sys
from pathlib import Path

from verify_u0a_butterfly_formula_compiler import (
    compile_formula, leaves_and_gates, stage_budget,
)
from verify_u0a_canonical_serialize_manifest import (
    digest_obj, encode_formula, exact_count_model, padding_for_S, program_record,
)
from verify_u0a_canonical_streaming_emitter import (
    canonical_bytes, hash_program_stream, iter_C_entries, iter_D_entries,
    iter_target,
)
from verify_u0a_universal_topology_serializer import (
    GATE_MODES, SOURCE_MODES, make_factor, target_y,
)

CAP_MIB = 256
S_RESOURCE = 128


def compile_formula_sparse(formula, width=None, assert_bit=1, certificate_version="v1"):
    """Compile using ordered overrides rather than a padded modes grid.

    The executable sparse-program fields contain O(width + routing-events)
    cells rather than ``width * stage_budget(width)`` cells.  Certificate v1
    retains the historical complete per-event token-map snapshots; v2 omits
    them; and v3 instead records an explicit sparse ``token_delta`` on every
    event.  The override list is strictly ordered and has no COPY_A entries or
    duplicate coordinates.
    """
    assert assert_bit in (0, 1)
    assert certificate_version in ("v1", "v2", "v3")
    full_snapshots = certificate_version == "v1"
    explicit_deltas = certificate_version == "v3"
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
    overrides = []
    event_counts = {"WAIT": 0, "SWAP": 0, "DUPLICATE": 0, "NAND": 0}
    certificate_events = []

    def token_snapshot():
        """Canonical complete live-token map used by the event certificate."""
        return tuple(sorted(token_lane.items()))

    initial_token_map = token_snapshot()

    def current_dim():
        return (stage_count // 2) % logw

    def emit_at_dim(dim, nondefault, kind, semantic=(), event_lanes=None):
        """Emit a stage and return its unfinished certificate event index.

        WAIT records are completed immediately.  The caller completes an
        active record after applying its logical token-map transition.  Full
        before/after snapshots intentionally make the certificate checkable by
        a small replay verifier without invoking routing/compiler decisions.
        """
        nonlocal stage_count
        while current_dim() != dim:
            before = token_snapshot() if full_snapshots else None
            stage_count += 1                 # a default-COPY_A WAIT stage
            event_counts["WAIT"] += 1
            record = {
                "stage": stage_count, "kind": "WAIT",
                "dimension": ((stage_count - 1) // 2) % logw,
                "lanes": (), "mode_overrides": (), "semantic": (),
            }
            if full_snapshots:
                record.update(token_map_before=before, token_map_after=before)
            if explicit_deltas:
                record["token_delta"] = ()
            certificate_events.append(record)
        before = token_snapshot() if full_snapshots else None
        stage_count += 1
        event_counts[kind] += 1
        ordered = tuple(sorted(nondefault))
        # Canonical order is stage major, then lane.  COPY_A is never stored.
        for lane, mode in ordered:
            assert mode != "COPY_A"
            overrides.append((stage_count, lane, mode))
        record = {
            "stage": stage_count, "kind": kind, "dimension": dim,
            "lanes": tuple(lane for lane, _ in ordered)
                     if event_lanes is None else tuple(event_lanes),
            "mode_overrides": ordered, "semantic": tuple(semantic),
        }
        if full_snapshots:
            record.update(token_map_before=before, token_map_after=None)
        if explicit_deltas:
            record["token_delta"] = None
        certificate_events.append(record)
        return len(certificate_events) - 1

    def finish_event(index, token_delta=()):
        if full_snapshots:
            assert certificate_events[index]["token_map_after"] is None
            certificate_events[index]["token_map_after"] = token_snapshot()
        if explicit_deltas:
            assert certificate_events[index]["token_delta"] is None
            # Each change is the generic Lean delta assignment (token, value),
            # where a null value deletes the token.  Repeated token names are
            # forbidden by the v3 checker, so ordering is semantically inert
            # except that NAND canonically lists its two deletes before add.
            certificate_events[index]["token_delta"] = tuple(token_delta)

    def swap_edge(a, b):
        dim = (a ^ b).bit_length() - 1
        assert a ^ b == 1 << dim
        event = emit_at_dim(dim, [(a, "COPY_B"), (b, "COPY_B")], "SWAP",
                            event_lanes=(a, b))
        ta, tb = lane_token[a], lane_token[b]
        lane_token[a], lane_token[b] = tb, ta
        if ta is not None:
            token_lane[ta] = b
        if tb is not None:
            token_lane[tb] = a
        finish_event(event, tuple((token, destination) for token, destination in
                                  ((ta, b), (tb, a)) if token is not None))

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
        event = emit_at_dim(dim, [(free, "COPY_B")], "DUPLICATE",
                            (source_token, new_token, a, free), (a, free))
        lane_token[free] = new_token
        token_lane[new_token] = free
        finish_event(event, ((new_token, free),))

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
        event = emit_at_dim(dim, [(a, "NAND"), (b, "ZERO")], "NAND",
                            (left, right, out, a, b), (a, b))
        del token_lane[left]
        del token_lane[right]
        lane_token[a] = out
        lane_token[b] = None
        token_lane[out] = a
        finish_event(event, ((left, None), (right, None), (out, a)))

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
    source_overrides = tuple((lane, "FREE") for lane in sorted(source_lane.values()))
    raw_gate_overrides = tuple(overrides)
    assert all(a[:2] < b[:2] for a, b in zip(raw_gate_overrides, raw_gate_overrides[1:]))
    assert all(mode != "COPY_A" for _, _, mode in raw_gate_overrides)

    return {
        "schema": "u0a-sparse-program-v1",
        "width": width,
        "gate_stages": budget,
        "assert_bit": assert_bit,
        "used_vars": tuple(used_vars),
        "source_lane": source_lane,
        "source_default": "FIX0",
        "source_overrides": source_overrides,
        "raw_stage_count": raw_stage_count,
        "raw_gate_default": "COPY_A",
        "raw_gate_overrides": raw_gate_overrides,
        "padding": {
            "start_stage": raw_stage_count + 1,
            "count": pad_stages,
            "default_mode": "COPY_A",
        },
        "cleanup": {
            "stage": budget,
            "default_mode": "ZERO",
            "overrides": ((output_lane, "COPY_A"),),
        },
        "output_lane": output_lane,
        "output_default": 0,
        "output_overrides": ((output_lane, assert_bit),) if assert_bit else (),
        "event_counts": event_counts,
        "event_certificate": {
            "schema": f"u0a-butterfly-event-certificate-{certificate_version}",
            "width": width,
            "leaf_table": tuple(leaves),
            "gate_table": tuple(gates),
            "root_token": root,
            "initial_token_map": initial_token_map,
            "events": tuple(certificate_events),
            "final_token_map": token_snapshot(),
            "output_lane": output_lane,
        },
        "dense_mode_cells_retained": 0,
    }


def gate_mode_at(p, stage, lane):
    """Return one logical mode using the sparse canonical representation."""
    w, d = p["width"], p["gate_stages"]
    if not (1 <= stage <= d and 0 <= lane < w):
        raise IndexError((stage, lane))
    if stage == p["cleanup"]["stage"]:
        return "COPY_A" if lane == p["output_lane"] else "ZERO"
    ov = p["raw_gate_overrides"]
    pos = bisect.bisect_left(ov, (stage, lane, ""))
    if pos < len(ov) and ov[pos][0] == stage and ov[pos][1] == lane:
        return ov[pos][2]
    return "COPY_A"


def source_mode_at(p, lane):
    if not 0 <= lane < p["width"]:
        raise IndexError(lane)
    # FREE source lanes are exactly the consecutive canonical variable lanes.
    return "FREE" if lane < len(p["source_overrides"]) else "FIX0"


def output_at(p, lane):
    if not 0 <= lane < p["width"]:
        raise IndexError(lane)
    return p["assert_bit"] if lane == p["output_lane"] else 0


def iter_gate_modes(p):
    """Yield ``(stage,lane,mode)`` in dense stage-major logical order.

    This is a stream: the dense grid is never retained.
    """
    ov = iter(p["raw_gate_overrides"])
    item = next(ov, None)
    raw = p["raw_stage_count"]
    w, d = p["width"], p["gate_stages"]
    for stage in range(1, d):
        for lane in range(w):
            if item is not None and item[0] == stage and item[1] == lane:
                mode = item[2]
                item = next(ov, None)
            else:
                mode = "COPY_A"
            yield stage, lane, mode
    assert item is None
    for lane in range(w):
        yield d, lane, ("COPY_A" if lane == p["output_lane"] else "ZERO")


def iter_target_sparse(width, depth, p):
    """Yield target_y in exact row order without row marks or dense modes."""
    assert (width, depth) == (p["width"], p["gate_stages"])
    # Normalizations.
    yield from itertools.repeat(1, width * (depth + 1))
    # Source program rows: lane, then SOURCE_MODES.
    for lane in range(width):
        selected = source_mode_at(p, lane)
        for mode in SOURCE_MODES:
            yield int(mode == selected)
    # Gate program rows: stage, lane, then GATE_MODES.
    for stage, lane, selected in iter_gate_modes(p):
        for mode in GATE_MODES:
            yield int(mode == selected)
    # Edge and dyadic-separator equations.
    yield from itertools.repeat(0, 2 * width * depth)
    yield from itertools.repeat(0, 2 * depth * (width - 1))
    # Output interfaces.
    for lane in range(width):
        yield output_at(p, lane)
    # Physical selector coordinates.
    _, k = exact_count_model(width, depth)
    yield from itertools.repeat(0, k)


def dense_equivalent_program_record(p):
    """Materialize only for small-instance oracle tests."""
    rows = [[] for _ in range(p["gate_stages"])]
    for stage, lane, mode in iter_gate_modes(p):
        assert len(rows[stage - 1]) == lane
        rows[stage - 1].append(mode)
    return {
        "source_modes": [source_mode_at(p, lane) for lane in range(p["width"])],
        "gate_modes_stage_major": rows,
        "outputs": [output_at(p, lane) for lane in range(p["width"])],
        "output_lane": p["output_lane"],
        "assert_bit": p["assert_bit"],
    }


def hash_program_stream_sparse(p):
    """Hash the exact old dense program JSON while retaining no dense row."""
    h = hashlib.sha256()
    h.update(b'{"assert_bit":' + str(p["assert_bit"]).encode("ascii"))
    h.update(b',"gate_modes_stage_major":[')
    current_stage = 0
    for stage, lane, mode in iter_gate_modes(p):
        if stage != current_stage:
            if current_stage:
                h.update(b"],")
            h.update(b"[")
            current_stage = stage
        elif lane:
            h.update(b",")
        h.update(canonical_bytes(mode))
    h.update(b']],"output_lane":' + str(p["output_lane"]).encode("ascii"))
    h.update(b',"outputs":[')
    for lane in range(p["width"]):
        if lane:
            h.update(b",")
        h.update(str(output_at(p, lane)).encode("ascii"))
    h.update(b'],"source_modes":[')
    for lane in range(p["width"]):
        if lane:
            h.update(b",")
        h.update(canonical_bytes(source_mode_at(p, lane)))
    h.update(b"]}")
    return h.hexdigest(), p["width"] * p["gate_stages"]


def sparse_program_record(p):
    """Return the JSON-safe canonical sparse record (no derived dense fields)."""
    return {
        "schema": p["schema"],
        "width": p["width"],
        "gate_stages": p["gate_stages"],
        "assert_bit": p["assert_bit"],
        "source_default": p["source_default"],
        "source_overrides": [list(x) for x in p["source_overrides"]],
        "raw_stage_count": p["raw_stage_count"],
        "raw_gate_default": p["raw_gate_default"],
        "raw_gate_overrides": [list(x) for x in p["raw_gate_overrides"]],
        "padding": dict(p["padding"]),
        "cleanup": {
            "stage": p["cleanup"]["stage"],
            "default_mode": p["cleanup"]["default_mode"],
            "overrides": [list(x) for x in p["cleanup"]["overrides"]],
        },
        "output_lane": p["output_lane"],
        "output_default": p["output_default"],
        "output_overrides": [list(x) for x in p["output_overrides"]],
    }


def _assert_iter_equal(got, expected):
    sentinel = object()
    for n, (a, b) in enumerate(itertools.zip_longest(got, expected,
                                                      fillvalue=sentinel)):
        assert a is not sentinel and b is not sentinel and a == b, (n, a, b)


def limited_child():
    cap = CAP_MIB * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    width, depth = padding_for_S(S_RESOURCE)
    assert (width, depth) == (128, 25102)
    p = compile_formula_sparse((0, 1), width=width, assert_bit=1)
    assert p["dense_mode_cells_retained"] == 0
    assert p["padding"]["count"] > 25000
    program_hash, logical_cells = hash_program_stream_sparse(p)
    assert logical_cells == 3_213_056

    # Cross the generator boundary for each complete canonical artifact stream.
    # Full traversal at these dimensions is deliberately not claimed here.
    c_prefix = list(itertools.islice(iter_C_entries(width, depth), 10000))
    d_prefix = list(itertools.islice(iter_D_entries(width, depth), 10000))
    t_prefix = list(itertools.islice(iter_target_sparse(width, depth, p), 10000))
    assert len(c_prefix) == len(d_prefix) == len(t_prefix) == 10000
    assert c_prefix[0] == [0, 0, 1] and d_prefix[0] == [0, 0, 1]
    m, k = exact_count_model(width, depth)
    summary = {
        "S": S_RESOURCE, "width": width, "gate_stages": depth,
        "C_shape": [m, k], "D_shape": [m, m + k],
        "logical_program_cells_streamed": logical_cells,
        "dense_mode_cells_retained": 0,
        "raw_override_count": len(p["raw_gate_overrides"]),
        "padding_stage_count": p["padding"]["count"],
        "dense_equivalent_program_sha256": program_hash,
        "C_D_target_prefix_entries_consumed_each": 10000,
    }
    print("SPARSE_S128_OK " + json.dumps(summary, sort_keys=True,
                                           separators=(",", ":")))


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--limited-child":
        limited_child()
        return
    assert len(sys.argv) == 1

    # Multiple scheduler shapes; actual target_y oracle at the canonical S=4
    # factor.  These are exact entrywise comparisons, not merely hashes.
    formulas = [(0, 1), ((0, 0), (1, 0)), (((0, 1), 0), (1, 0))]
    checked = []
    for formula in formulas:
        leaves = len(leaves_and_gates(formula)[0])
        width = 1 << (max(4, leaves) - 1).bit_length()
        sparse = compile_formula_sparse(formula, width=width, assert_bit=1)
        dense = compile_formula(formula, width=width, assert_bit=1)
        dense_record = program_record(dense)
        assert dense_equivalent_program_record(sparse) == dense_record
        assert hash_program_stream_sparse(sparse)[0] == digest_obj(dense_record)
        _assert_iter_equal(
            (mode for _, _, mode in iter_gate_modes(sparse)),
            (dense["modes"][(stage, lane)]
             for stage in range(1, dense["gate_stages"] + 1)
             for lane in range(width)),
        )
        _assert_iter_equal(iter_target_sparse(width, dense["gate_stages"], sparse),
                           iter_target(width, dense["gate_stages"], dense))
        checked.append((formula, width, len(sparse["raw_gate_overrides"])))

    # Actual eager factor/target oracle (one small canonical S=4 instance).
    sparse = compile_formula_sparse((0, 1), width=4, assert_bit=1)
    dense = compile_formula((0, 1), width=4, assert_bit=1)
    factor, _, _ = make_factor(4, stage_budget(4))
    eager_target = target_y(factor, dense["source_modes"], dense["modes"],
                            dense["outputs"])
    _assert_iter_equal(iter_target_sparse(4, stage_budget(4), sparse), eager_target)

    proc = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "--limited-child"],
        text=True, capture_output=True, timeout=180,
    )
    assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
    line = next(x for x in proc.stdout.splitlines()
                if x.startswith("SPARSE_S128_OK "))
    summary = json.loads(line.split(" ", 1)[1])
    assert summary["dense_mode_cells_retained"] == 0
    assert summary["logical_program_cells_streamed"] == 3_213_056

    print("PASS canonical sparse U0a program stream")
    print("small exact dense program/target cases:", checked)
    print("S=128 under 256 MiB:", json.dumps(summary, sort_keys=True))
    print("Scope: finite exact/resource evidence; S=128 factor/target streams "
          "are prefix-consumed, not fully emitted/hashed; no universal theorem, "
          "soundness, or approximation gap.")


if __name__ == "__main__":
    main()
