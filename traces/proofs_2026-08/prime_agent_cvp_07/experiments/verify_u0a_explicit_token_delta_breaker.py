#!/usr/bin/env python3
"""Independent exact mutation/resource audit for explicit v3 token deltas.

The checker consumes only a JSON-round-tripped artifact.  It reconstructs its
own token-to-lane state, derives the unique delta required by each physical
WAIT/SWAP/DUPLICATE/NAND event, compares the explicit delta entry-for-entry,
and separately applies it with simultaneous delete/write collision checks.
It never calls the scheduler while verifying.

This is finite implementation evidence, not a universal compiler theorem.
"""
from __future__ import annotations

import copy
import json
import resource
import subprocess
import sys
from collections import Counter
from pathlib import Path

from verify_u0a_butterfly_formula_compiler import formulas
from verify_u0a_sparse_program_stream import compile_formula_sparse

CAP_MIB = 256
RESOURCE_LEAVES = 4097
EVENT_KEYS = {
    "stage", "kind", "dimension", "lanes", "mode_overrides", "semantic",
    "token_delta",
}
MODES = {"COPY_B", "NAND", "ZERO"}


def comb(n):
    f = 0
    for i in range(1, n):
        f = (i, f)
    return f


def balanced(xs):
    if len(xs) == 1:
        return xs[0]
    m = len(xs) // 2
    return (balanced(xs[:m]), balanced(xs[m:]))


def artifact(formula, width=None, assert_bit=1):
    p = compile_formula_sparse(formula, width=width, assert_bit=assert_bit,
                               certificate_version="v3")
    # Establish the producer/verifier serialization boundary.  In particular,
    # tuple identity and Python object sharing cannot help the checker.
    return json.loads(json.dumps(p, ensure_ascii=True, sort_keys=True,
                                 separators=(",", ":")))


def parse_snapshot(seq, width):
    got = tuple((str(token), int(lane)) for token, lane in seq)
    assert got == tuple(sorted(got)), "noncanonical snapshot order"
    assert len({token for token, _ in got}) == len(got), "duplicate token"
    assert len({lane for _, lane in got}) == len(got), "token collision"
    assert all(0 <= lane < width for _, lane in got), "lane out of range"
    return got


def parse_overrides(seq, width):
    got = tuple((int(lane), str(mode)) for lane, mode in seq)
    assert got == tuple(sorted(got)), "noncanonical override order"
    assert len({lane for lane, _ in got}) == len(got), "duplicate override"
    assert all(0 <= lane < width and mode in MODES for lane, mode in got)
    return got


def parse_delta(seq, width):
    """Parse canonical generic Lean changes `(token,newLaneOrNone)`."""
    got = []
    for entry in seq:
        assert isinstance(entry, list) and len(entry) == 2
        token = str(entry[0])
        after = None if entry[1] is None else int(entry[1])
        assert token
        assert after is None or 0 <= after < width
        got.append((token, after))
    got = tuple(got)
    assert len({token for token, _ in got}) == len(got), "duplicate token write"
    return got


def apply_explicit_delta(state, delta, width):
    """Apply simultaneous generic token assignments after removing old values."""
    old = dict(state)
    nxt = dict(old)
    for token, after in delta:
        if after is None:
            assert token in old, "deleting absent token"
        # A non-null assignment may move an existing token or create a new one.
        if token in nxt:
            del nxt[token]
    for token, after in delta:
        if after is not None:
            assert token not in nxt
            assert after not in nxt.values(), "token lane collision"
            nxt[token] = after
    assert len(set(nxt.values())) == len(nxt)
    assert all(0 <= lane < width for lane in nxt.values())
    return nxt


def verify(a):
    c = a["event_certificate"]
    assert c["schema"] == "u0a-butterfly-event-certificate-v3"
    w = int(a["width"])
    raw = int(a["raw_stage_count"])
    depth = int(a["gate_stages"])
    assert int(c["width"]) == w and w >= 4 and w & (w - 1) == 0
    logw = w.bit_length() - 1

    leaves = tuple((str(t), int(v)) for t, v in c["leaf_table"])
    gates = tuple((str(o), str(x), str(y)) for o, x, y in c["gate_table"])
    assert leaves and all(t == f"leaf:{i}" and v >= 0
                          for i, (t, v) in enumerate(leaves))
    declared = {t for t, _ in leaves}
    demand = Counter()
    for i, (out, left, right) in enumerate(gates):
        assert out == f"gate:{i}" and out not in declared
        assert left in declared and right in declared and left != right
        demand[left] += 1
        demand[right] += 1
        declared.add(out)
    root = str(c["root_token"])
    assert root in declared and demand[root] == 0
    assert all(demand[t] == (0 if t == root else 1) for t in declared)

    occurrences = {}
    for token, var in leaves:
        occurrences.setdefault(var, []).append(token)
    used_vars = sorted(occurrences)
    expected_initial = tuple(sorted((occurrences[v][0], lane)
                                    for lane, v in enumerate(used_vars)))
    initial = parse_snapshot(c["initial_token_map"], w)
    assert initial == expected_initial
    state = dict(initial)
    assert a["source_default"] == "FIX0"
    assert tuple((int(x), str(y)) for x, y in a["source_overrides"]) == tuple(
        (lane, "FREE") for lane in range(len(used_vars)))

    demanded_duplicates = [(occurrences[v][0], token)
                            for v in used_vars for token in occurrences[v][1:]]
    demanded_nands = [(left, right, out) for out, left, right in gates]
    duplicate_seen, nand_seen, flat = [], [], []
    counts = Counter()
    nonempty_one_sided_swaps = 0
    two_sided_swaps = 0
    events = c["events"]
    assert len(events) == raw

    for expected_stage, event in enumerate(events, 1):
        assert set(event) == EVENT_KEYS, set(event)
        stage = int(event["stage"])
        kind = str(event["kind"])
        dim = int(event["dimension"])
        assert stage == expected_stage
        assert dim == ((stage - 1) // 2) % logw
        lanes = tuple(int(x) for x in event["lanes"])
        assert all(0 <= x < w for x in lanes)
        ovs = parse_overrides(event["mode_overrides"], w)
        flat.extend((stage, lane, mode) for lane, mode in ovs)
        sem = tuple(event["semantic"])
        supplied = parse_delta(event["token_delta"], w)
        counts[kind] += 1

        if kind == "WAIT":
            assert lanes == () and ovs == () and sem == ()
            expected = ()
        elif kind == "SWAP":
            assert len(lanes) == 2 and lanes[0] != lanes[1] and sem == ()
            x, y = lanes
            assert x ^ y == 1 << dim
            assert ovs == tuple(sorted(((x, "COPY_B"), (y, "COPY_B"))))
            at_x = next((t for t, lane in state.items() if lane == x), None)
            at_y = next((t for t, lane in state.items() if lane == y), None)
            # The compiler routes an occupied token; an empty/empty physical
            # swap is not a valid certificate event even though it is Boolean
            # identity on the current state.
            assert at_x is not None or at_y is not None, "empty SWAP endpoints"
            expected_list = []
            if at_x is not None:
                expected_list.append((at_x, y))
            if at_y is not None:
                expected_list.append((at_y, x))
            expected = tuple(expected_list)
            nonempty_one_sided_swaps += len(expected) == 1
            two_sided_swaps += len(expected) == 2
        elif kind == "DUPLICATE":
            assert len(sem) == 4 and len(lanes) == 2 and lanes[0] != lanes[1]
            source, new, x0, y0 = sem
            source, new, x, y = str(source), str(new), int(x0), int(y0)
            assert lanes == (x, y) and x ^ y == 1 << dim
            assert source in state and state[source] == x
            assert new not in state and y not in state.values()
            assert ovs == ((y, "COPY_B"),)
            expected = ((new, y),)
            duplicate_seen.append((source, new))
        elif kind == "NAND":
            assert len(sem) == 5 and len(lanes) == 2 and lanes[0] != lanes[1]
            left, right, out, x0, y0 = sem
            left, right, out = str(left), str(right), str(out)
            x, y = int(x0), int(y0)
            assert left != right and lanes == (x, y) and x ^ y == 1 << dim
            assert left in state and state[left] == x
            assert right in state and state[right] == y and out not in state
            assert ovs == tuple(sorted(((x, "NAND"), (y, "ZERO"))))
            expected = ((left, None), (right, None), (out, x))
            nand_seen.append((left, right, out))
        else:
            raise AssertionError(kind)

        # Exact sequence equality detects missing occupied-endpoint SWAP
        # records and also makes NAND deletion/creation order canonical.
        assert supplied == expected, (kind, supplied, expected)
        state = apply_explicit_delta(state, supplied, w)

    assert duplicate_seen == demanded_duplicates
    assert nand_seen == demanded_nands
    assert flat == [(int(s), int(l), str(m)) for s, l, m
                    in a["raw_gate_overrides"]]
    assert dict(parse_snapshot(c["final_token_map"], w)) == state
    assert state == {root: int(c["output_lane"])}
    assert int(c["output_lane"]) == int(a["output_lane"])
    assert set(a["event_counts"]) == {"WAIT", "SWAP", "DUPLICATE", "NAND"}
    assert all(int(a["event_counts"][kind]) == counts[kind]
               for kind in ("WAIT", "SWAP", "DUPLICATE", "NAND"))
    assert a["raw_gate_default"] == "COPY_A"
    assert a["padding"] == {"start_stage": raw + 1, "count": depth - raw - 1,
                            "default_mode": "COPY_A"}
    assert a["cleanup"] == {"stage": depth, "default_mode": "ZERO",
                            "overrides": [[a["output_lane"], "COPY_A"]]}
    assert raw < depth
    return {"events": raw, "delta_records": sum(
                len(e["token_delta"]) for e in events),
            "one_sided_swaps": nonempty_one_sided_swaps,
            "two_sided_swaps": two_sided_swaps}


def rejected(a):
    try:
        verify(a)
    except (AssertionError, KeyError, TypeError, ValueError):
        return True
    return False


def mutation_suite():
    # This repeated-variable shape contains both one- and two-occupied-endpoint
    # SWAPs as well as DUPLICATE and NAND records.
    base = artifact((1, (1, 0)), width=4)
    assert verify(base)["two_sided_swaps"] > 0
    mutants = []

    # Delete exactly one of the two occupied-token writes from a SWAP.
    bad = copy.deepcopy(base)
    sw = next(e for e in bad["event_certificate"]["events"]
              if e["kind"] == "SWAP" and len(e["token_delta"]) == 2)
    sw["token_delta"].pop()
    mutants.append(("missing-swap-token", bad))

    # Replace the first real SWAP by an otherwise well-formed physical swap of
    # the two empty lanes.  Bind its overrides to the program too, so rejection
    # specifically requires the nonempty-routing invariant rather than a mere
    # event/program mismatch.
    bad = copy.deepcopy(base)
    sw = next(e for e in bad["event_certificate"]["events"]
              if e["kind"] == "SWAP")
    assert sw["stage"] == 1 and sw["dimension"] == 0
    sw["lanes"] = [2, 3]
    sw["mode_overrides"] = [[2, "COPY_B"], [3, "COPY_B"]]
    sw["token_delta"] = []
    bad["raw_gate_overrides"][0:2] = [[1, 2, "COPY_B"], [1, 3, "COPY_B"]]
    mutants.append(("empty-empty-swap", bad))

    # A deletion must have after=null; retaining the consumed token is invalid.
    bad = copy.deepcopy(base)
    nd = next(e for e in bad["event_certificate"]["events"] if e["kind"] == "NAND")
    nd["token_delta"][0][1] = nd["semantic"][3]
    mutants.append(("wrong-deletion", bad))

    # NAND deltas have canonical left deletion, right deletion, output creation.
    bad = copy.deepcopy(base)
    nd = next(e for e in bad["event_certificate"]["events"] if e["kind"] == "NAND")
    nd["token_delta"][0], nd["token_delta"][1] = (
        nd["token_delta"][1], nd["token_delta"][0])
    mutants.append(("wrong-delta-order", bad))

    # Repeating a write to the same token is not interpreted sequentially.
    bad = copy.deepcopy(base)
    dup = next(e for e in bad["event_certificate"]["events"]
               if e["kind"] == "DUPLICATE")
    dup["token_delta"].append(copy.deepcopy(dup["token_delta"][0]))
    mutants.append(("duplicate-write", bad))

    # Inventing a token at an endpoint that was empty before a one-sided SWAP.
    bad = copy.deepcopy(base)
    sw = next(e for e in bad["event_certificate"]["events"]
              if e["kind"] == "SWAP" and len(e["token_delta"]) == 1)
    destination = sw["token_delta"][0][1]
    x, y = sw["lanes"]
    empty = x if destination == x else y
    sw["token_delta"].append(["ghost:empty-endpoint", empty])
    mutants.append(("empty-endpoint-token", bad))

    # Create a duplicate on its already occupied source lane.
    bad = copy.deepcopy(base)
    dup = next(e for e in bad["event_certificate"]["events"]
               if e["kind"] == "DUPLICATE")
    dup["token_delta"][0][1] = dup["semantic"][2]
    mutants.append(("token-lane-collision", bad))

    # Two distinct creation entries cannot write the same free lane.
    bad = copy.deepcopy(base)
    dup = next(e for e in bad["event_certificate"]["events"]
               if e["kind"] == "DUPLICATE")
    lane = dup["token_delta"][0][1]
    dup["token_delta"].append(["ghost:second-writer", lane])
    mutants.append(("two-writes-one-lane", bad))

    # An empty/null token cannot stand for an unoccupied SWAP endpoint.
    bad = copy.deepcopy(base)
    sw = next(e for e in bad["event_certificate"]["events"]
              if e["kind"] == "SWAP" and len(e["token_delta"]) == 1)
    sw["token_delta"].append([None, sw["lanes"][0]])
    mutants.append(("null-empty-endpoint-token", bad))

    rejected_names = [name for name, mutant in mutants if rejected(mutant)]
    assert rejected_names == [name for name, _ in mutants], rejected_names
    return rejected_names


def limited_child(n):
    cap = CAP_MIB * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    a = artifact(comb(n))
    got = verify(a)
    # Neither retired full snapshots nor hidden per-event state are permitted.
    assert all(set(e) == EVENT_KEYS for e in a["event_certificate"]["events"])
    assert all("token_map_before" not in e and "token_map_after" not in e
               for e in a["event_certificate"]["events"])
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(json.dumps({"leaves": n, "width": a["width"], **got,
                      "maxrss_kib": rss}, sort_keys=True))


def main():
    family = [f for n in range(1, 5) for f in formulas(n, 2)]
    assert len(family) == 102
    totals = Counter()
    for f in family:
        got = verify(artifact(f, width=4))
        totals.update(got)
    wide = verify(artifact(balanced(tuple(i % 4 for i in range(16))), width=16))
    rejected_names = mutation_suite()

    q = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "--limited-child",
         str(RESOURCE_LEAVES)], text=True, capture_output=True, timeout=180)
    assert q.returncode == 0, (q.returncode, q.stdout, q.stderr)
    capped = json.loads(q.stdout)
    assert capped["leaves"] == RESOURCE_LEAVES
    assert capped["maxrss_kib"] < CAP_MIB * 1024
    print(json.dumps({
        "schema": "u0a-explicit-token-delta-breaker-v1",
        "small_formulas": len(family), "small_totals": dict(totals),
        "width16": wide, "mutants_rejected": len(rejected_names),
        "mutant_names": rejected_names, "resource": capped,
        "cap_MiB": CAP_MIB, "finite_claim_only": True,
    }, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--limited-child":
        limited_child(int(sys.argv[2]))
    else:
        assert len(sys.argv) == 1
        main()
