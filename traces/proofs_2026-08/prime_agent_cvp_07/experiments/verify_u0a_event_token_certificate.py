#!/usr/bin/env python3
"""Finite independent verifier for sparse butterfly event certificates.

The producer now emits a JSON-safe, per-raw-stage transcript containing the
complete token map before and after each WAIT/SWAP/DUPLICATE/NAND event.  This
file deliberately separates production from checking: ``build_artifact`` is
the only function that calls ``compile_formula_sparse``; all verification
functions consume only a JSON round-tripped sparse record plus certificate.

For each assignment the checker also selects one actual source/gate column per
cell, streams canonical C, and checks every row after projection to those
selected columns.  In particular the PHYSICAL_SELECTOR row for every selected
column is checked to be the exact emitted singleton [row,column,1].

This is finite evidence, not a universal compiler theorem or CVP soundness.
"""
from __future__ import annotations

import copy
import itertools
import json
import resource
import subprocess
import sys
from collections import Counter
from pathlib import Path

from verify_u0a_butterfly_formula_compiler import formulas
from verify_u0a_canonical_serialize_manifest import exact_count_model
from verify_u0a_canonical_streaming_emitter import (
    GATE_STATES, SOURCE_STATES, column_index, iter_C_entries, iter_row_marks,
)
from verify_u0a_sparse_program_stream import (
    compile_formula_sparse, sparse_program_record,
)

CAP_MIB = 256


def build_artifact(formula, width, assert_bit=1):
    """Producer boundary.  Return only canonical JSON data, no live internals."""
    p = compile_formula_sparse(formula, width=width, assert_bit=assert_bit)
    out = sparse_program_record(p)
    out["event_certificate"] = p["event_certificate"]
    # The independent checker receives precisely what could be put on disk.
    return json.loads(json.dumps(out, sort_keys=True, separators=(",", ":")))


def _snapshot(x):
    ans = tuple((str(token), int(lane)) for token, lane in x)
    assert ans == tuple(sorted(ans))
    assert len({t for t, _ in ans}) == len(ans)
    assert len({lane for _, lane in ans}) == len(ans)
    return ans


def _put_snapshot(mapping):
    return tuple(sorted(mapping.items()))


def _mode_overrides(event):
    ans = tuple((int(lane), str(mode)) for lane, mode in event["mode_overrides"])
    assert ans == tuple(sorted(ans))
    assert len({lane for lane, _ in ans}) == len(ans)
    assert all(mode != "COPY_A" for _, mode in ans)
    return ans


def verify_event_certificate(a):
    """Replay all token transitions and bind them to the sparse mode stream."""
    c = a["event_certificate"]
    assert c["schema"] == "u0a-butterfly-event-certificate-v1"
    w = int(a["width"])
    depth = int(a["gate_stages"])
    raw = int(a["raw_stage_count"])
    assert c["width"] == w and w >= 4 and w & (w - 1) == 0
    logw = w.bit_length() - 1

    leaves = tuple((str(t), int(v)) for t, v in c["leaf_table"])
    gates = tuple((str(o), str(x), str(y)) for o, x, y in c["gate_table"])
    assert leaves and all(t == f"leaf:{i}" and v >= 0
                          for i, (t, v) in enumerate(leaves))
    declared = {t for t, _ in leaves}
    child_count = Counter()
    for i, (out, left, right) in enumerate(gates):
        assert out == f"gate:{i}" and out not in declared
        assert left in declared and right in declared and left != right
        child_count[left] += 1
        child_count[right] += 1
        declared.add(out)
    root = str(c["root_token"])
    assert root in declared
    assert child_count[root] == 0
    assert all(child_count[t] == (0 if t == root else 1) for t in declared)

    occurrences = {}
    for token, var in leaves:
        occurrences.setdefault(var, []).append(token)
    used_vars = sorted(occurrences)
    expected_initial = tuple((occurrences[v][0], lane)
                             for lane, v in enumerate(used_vars))
    expected_initial = tuple(sorted(expected_initial))
    state = dict(expected_initial)
    assert _snapshot(c["initial_token_map"]) == expected_initial
    assert a["source_default"] == "FIX0"
    assert tuple((int(x), str(y)) for x, y in a["source_overrides"]) == tuple(
        (lane, "FREE") for lane in range(len(used_vars)))

    demanded_duplicates = [(occurrences[v][0], token)
                            for v in used_vars for token in occurrences[v][1:]]
    demanded_nands = [(left, right, out) for out, left, right in gates]
    duplicate_seen = []
    nand_seen = []
    flat_overrides = []
    counts = Counter()

    events = c["events"]
    assert len(events) == raw
    for expected_stage, event in enumerate(events, 1):
        stage = int(event["stage"])
        kind = str(event["kind"])
        dim = int(event["dimension"])
        assert stage == expected_stage
        assert dim == ((stage - 1) // 2) % logw
        assert _snapshot(event["token_map_before"]) == _put_snapshot(state)
        ovs = _mode_overrides(event)
        flat_overrides.extend((stage, lane, mode) for lane, mode in ovs)
        semantic = tuple(event["semantic"])
        counts[kind] += 1

        if kind == "WAIT":
            assert tuple(event["lanes"]) == () and ovs == () and semantic == ()
        elif kind == "SWAP":
            lanes = tuple(int(x) for x in event["lanes"])
            assert len(lanes) == 2
            x, y = lanes
            assert x ^ y == 1 << dim
            assert ovs == tuple(sorted(((x, "COPY_B"), (y, "COPY_B"))))
            assert semantic == ()
            for token in list(state):
                if state[token] == x:
                    state[token] = y
                elif state[token] == y:
                    state[token] = x
        elif kind == "DUPLICATE":
            assert len(semantic) == 4
            source, new, x0, y0 = semantic
            x, y = int(x0), int(y0)
            source, new = str(source), str(new)
            assert tuple(int(z) for z in event["lanes"]) == (x, y)
            assert source in state and state[source] == x and new not in state
            assert y not in state.values() and x ^ y == 1 << dim
            assert ovs == ((y, "COPY_B"),)
            state[new] = y
            duplicate_seen.append((source, new))
        elif kind == "NAND":
            assert len(semantic) == 5
            left, right, out, x0, y0 = semantic
            left, right, out = str(left), str(right), str(out)
            x, y = int(x0), int(y0)
            assert left in state and right in state and out not in state
            assert state[left] == x and state[right] == y and x ^ y == 1 << dim
            assert ovs == tuple(sorted(((x, "NAND"), (y, "ZERO"))))
            assert tuple(int(z) for z in event["lanes"]) == (x, y)
            del state[left]
            del state[right]
            state[out] = x
            nand_seen.append((left, right, out))
        else:
            raise AssertionError(kind)
        assert _snapshot(event["token_map_after"]) == _put_snapshot(state)

    assert duplicate_seen == demanded_duplicates
    assert nand_seen == demanded_nands
    expected_ovs = [(int(s), int(l), str(m))
                    for s, l, m in a["raw_gate_overrides"]]
    assert flat_overrides == expected_ovs
    assert _snapshot(c["final_token_map"]) == _put_snapshot(state)
    assert state == {root: int(c["output_lane"])}
    assert int(c["output_lane"]) == int(a["output_lane"])
    assert a["raw_gate_default"] == "COPY_A"
    assert a["padding"] == {"start_stage": raw + 1,
                             "count": depth - raw - 1,
                             "default_mode": "COPY_A"}
    assert a["cleanup"] == {"stage": depth, "default_mode": "ZERO",
                             "overrides": [[a["output_lane"], "COPY_A"]]}
    assert raw < depth
    return {
        "events": len(events), "wait": counts["WAIT"],
        "swap": counts["SWAP"], "duplicate": counts["DUPLICATE"],
        "nand": counts["NAND"], "root": root,
    }


def _program_tables(a):
    raw_modes = {(int(s), int(l)): str(m)
                 for s, l, m in a["raw_gate_overrides"]}
    assert len(raw_modes) == len(a["raw_gate_overrides"])
    src_modes = {int(lane): str(mode) for lane, mode in a["source_overrides"]}
    return raw_modes, src_modes


def _gate_value(mode, x, y):
    if mode == "COPY_A": return x
    if mode == "COPY_B": return y
    if mode == "NAND": return 1 - x * y
    if mode == "ZERO": return 0
    if mode == "ONE": return 1
    raise AssertionError(mode)


def selected_columns(a, assignment):
    """Derive honest local columns from the certified artifact, not compiler."""
    w, depth = int(a["width"]), int(a["gate_stages"])
    c = a["event_certificate"]
    leaves = [(str(t), int(v)) for t, v in c["leaf_table"]]
    vars_used = sorted({v for _, v in leaves})
    raw_modes, src_modes = _program_tables(a)
    selected = set()
    prev = []
    for lane in range(w):
        mode = src_modes.get(lane, a["source_default"])
        bit = int(assignment[vars_used[lane]]) if lane < len(vars_used) else 0
        state = (mode, bit)
        assert state in SOURCE_STATES
        j = column_index(w, 0, lane, SOURCE_STATES.index(state))
        selected.add(j)
        prev.append(bit)
    output_lane = int(a["output_lane"])
    raw = int(a["raw_stage_count"])
    for stage in range(1, depth + 1):
        dim = ((stage - 1) // 2) % (w.bit_length() - 1)
        off = 1 << dim
        cur = []
        for lane in range(w):
            if stage == depth:
                mode = "COPY_A" if lane == output_lane else "ZERO"
            elif stage <= raw:
                mode = raw_modes.get((stage, lane), "COPY_A")
            else:
                mode = "COPY_A"
            x, y = prev[lane], prev[lane ^ off]
            z = _gate_value(mode, x, y)
            state = (mode, x, y, z)
            assert state in GATE_STATES
            j = column_index(w, stage, lane, GATE_STATES.index(state))
            assert j not in selected
            selected.add(j)
            cur.append(z)
        prev = cur
    return selected, prev, raw_modes, src_modes


def verify_selected_column_rows(a, assignment):
    """Stream every C row and check its projection onto selected columns."""
    w, depth = int(a["width"]), int(a["gate_stages"])
    m, k = exact_count_model(w, depth)
    selected, final, raw_modes, src_modes = selected_columns(a, assignment)
    assert len(selected) == w * (depth + 1)
    marks = iter(iter_row_marks(w, depth))
    entries = iter(iter_C_entries(w, depth))
    item = next(entries, None)
    selected_physical = 0
    rows_touched = 0
    output_lane = int(a["output_lane"])
    raw = int(a["raw_stage_count"])

    for row in range(m):
        crow = []
        while item is not None and item[0] == row:
            crow.append(item)
            item = next(entries, None)
        mark = next(marks)
        assert mark["index"] == row
        moment = sum(v for _, j, v in crow if j in selected)
        rows_touched += int(moment != 0)
        kind = mark["kind"]
        if kind == "NORM_DROP_GUARD":
            assert moment == 1
        elif kind == "SOURCE_PROGRAM":
            chosen = src_modes.get(mark["lane"], a["source_default"])
            assert moment == int(mark["mode"] == chosen)
        elif kind == "GATE_PROGRAM":
            stage, lane = mark["stage"], mark["lane"]
            if stage == depth:
                chosen = "COPY_A" if lane == output_lane else "ZERO"
            elif stage <= raw:
                chosen = raw_modes.get((stage, lane), "COPY_A")
            else:
                chosen = "COPY_A"
            assert moment == int(mark["mode"] == chosen)
        elif kind in ("EDGE_CONSISTENCY", "DYADIC_SEPARATOR"):
            assert moment == 0
        elif kind == "OUTPUT_INTERFACE":
            assert moment == final[mark["lane"]]
        elif kind == "PHYSICAL_SELECTOR":
            j = int(mark["selector_column"])
            assert crow == [[row, j, 1]]
            assert moment == int(j in selected)
            if j in selected:
                selected_physical += 1
        else:
            raise AssertionError(kind)
    assert item is None and next(marks, None) is None
    assert selected_physical == len(selected)

    # Evaluate the declared postorder table independently of routing.
    values = {str(t): int(assignment[int(v)])
              for t, v in a["event_certificate"]["leaf_table"]}
    for out, left, right in a["event_certificate"]["gate_table"]:
        values[str(out)] = 1 - values[str(left)] * values[str(right)]
    expected = values[str(a["event_certificate"]["root_token"])]
    assert final[output_lane] == expected
    assert all(x == 0 for lane, x in enumerate(final) if lane != output_lane)
    return {"rows": m, "columns": k, "selected": len(selected),
            "selected_physical_rows": selected_physical,
            "rows_with_nonzero_selected_projection": rows_touched,
            "formula_value": expected}


def balanced(xs):
    if len(xs) == 1: return xs[0]
    mid = len(xs) // 2
    return (balanced(xs[:mid]), balanced(xs[mid:]))


def limited_child():
    resource.setrlimit(resource.RLIMIT_AS,
                       (CAP_MIB * 1024 * 1024, CAP_MIB * 1024 * 1024))
    f = balanced(tuple(i % 4 for i in range(16)))
    a = build_artifact(f, 16)
    ev = verify_event_certificate(a)
    rows = verify_selected_column_rows(a, {i: i & 1 for i in range(4)})
    print(json.dumps({"events": ev, "rows": rows}, sort_keys=True))


def main():
    # Exhaust every ordered two-variable NAND tree through four leaves.
    family = [f for n in range(1, 5) for f in formulas(n, 2)]
    assert len(family) == 102
    cert_events = 0
    assignment_checks = 0
    selected_rows = 0
    projected_rows = 0
    for f in family:
        a = build_artifact(f, 4)
        ev = verify_event_certificate(a)
        cert_events += ev["events"]
        for bits in itertools.product((0, 1), repeat=2):
            got = verify_selected_column_rows(a, dict(enumerate(bits)))
            assignment_checks += 1
            selected_rows += got["selected_physical_rows"]
            projected_rows += got["rows"]

    # The checker, rather than producer assertions, rejects representative
    # certificate corruptions after the JSON artifact has been emitted.
    mutation_base = build_artifact(((0, 1), (0, 1)), 4)
    mutations = []
    bad = copy.deepcopy(mutation_base)
    bad["event_certificate"]["events"][0]["dimension"] ^= 1
    mutations.append(bad)
    bad = copy.deepcopy(mutation_base)
    active = next(e for e in bad["event_certificate"]["events"]
                  if e["kind"] != "WAIT")
    active["token_map_after"] = []
    mutations.append(bad)
    bad = copy.deepcopy(mutation_base)
    active = next(e for e in bad["event_certificate"]["events"]
                  if e["kind"] in ("DUPLICATE", "NAND"))
    active["semantic"][0] = "forged:token"
    mutations.append(bad)
    rejected_mutations = 0
    for bad in mutations:
        try:
            verify_event_certificate(bad)
        except (AssertionError, KeyError, ValueError):
            rejected_mutations += 1
    assert rejected_mutations == len(mutations)

    child = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "--limited-child"],
        text=True, capture_output=True, timeout=240, check=True,
    )
    capped = json.loads(child.stdout)
    out = {
        "schema": "u0a-event-token-certificate-finite-v1",
        "small_formulas_exhaustive": len(family),
        "small_assignments": assignment_checks,
        "certificate_events_replayed": cert_events + capped["events"]["events"],
        "C_rows_projected": projected_rows + capped["rows"]["rows"],
        "selected_physical_rows_exact": selected_rows + capped["rows"]["selected_physical_rows"],
        "capped_width": 16,
        "capped_rows": capped["rows"]["rows"],
        "capped_columns": capped["rows"]["columns"],
        "capped_selected_columns": capped["rows"]["selected"],
        "certificate_mutants_rejected": rejected_mutations,
        "finite_claim_only": True,
    }
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--limited-child":
        limited_child()
    else:
        assert len(sys.argv) == 1
        main()
