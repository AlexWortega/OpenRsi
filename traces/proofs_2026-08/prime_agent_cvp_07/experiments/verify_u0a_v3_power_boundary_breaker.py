#!/usr/bin/env python3
"""Exact finite-lane breaker for v3 traces at large power-of-two boundaries.

This checker is intentionally independent of the scheduler's mutable token maps.
It consumes a JSON-round-tripped v3 artifact, maintains both token->lane and
lane->token maps, derives every canonical explicit delta from the reached state,
and checks every endpoint, delta destination, override and output lane is in the
finite hypercube.  Large cases retain no per-event snapshots.

The result is finite implementation evidence, not an asymptotic theorem.
"""
from __future__ import annotations

import copy
import json
import resource
import subprocess
import sys
from collections import Counter
from pathlib import Path

from verify_u0a_sparse_program_stream import compile_formula_sparse

CAP_MIB = 768
EVENT_KEYS = {"stage", "kind", "dimension", "lanes", "mode_overrides",
              "semantic", "token_delta"}
MODES = {"COPY_B", "NAND", "ZERO"}
LARGE_CASES = (
    (2047, "comb-distinct", 2047, 0x2047),
    (2048, "comb-distinct", 2048, 0x2048),
    (2049, "comb-distinct", 2049, 0x2049),
    (8193, "comb-distinct", 8193, 0x8193),
)


def xorshift64(x):
    x ^= (x << 13) & ((1 << 64) - 1)
    x ^= x >> 7
    x ^= (x << 17) & ((1 << 64) - 1)
    return x & ((1 << 64) - 1)


def leaf_value(i, variables, seed):
    # A permutation-like mix avoids a trivial periodic allocation pattern.
    x = xorshift64((i + 1) ^ seed)
    return int(x % variables)


def comb_formula(n, variables, seed):
    f = leaf_value(0, variables, seed)
    for i in range(1, n):
        f = (leaf_value(i, variables, seed), f)
    return f


def fuzz_formula(n, variables, seed):
    """Deterministic nonuniform binary tree, with logarithmic recursion depth."""
    state = seed

    def build(lo, count):
        nonlocal state
        if count == 1:
            return leaf_value(lo, variables, seed)
        state = xorshift64(state)
        # Keep both children at least count/4 when possible.  This makes the
        # tree genuinely non-balanced without risking a Python stack artifact.
        q = max(1, count // 4)
        span = count - 2 * q + 1
        left = q + state % span
        if left >= count:
            left = count - 1
        return (build(lo, left), build(lo + left, count - left))

    return build(0, n)


def make_formula(n, shape, variables, seed):
    if shape == "comb-distinct":
        f = 0
        for i in range(1, n):
            f = (i, f)
        return f
    if shape == "comb-repeat":
        return comb_formula(n, variables, seed)
    if shape == "fuzz-repeat":
        return fuzz_formula(n, variables, seed)
    raise AssertionError(shape)


def json_artifact(formula):
    p = compile_formula_sparse(formula, certificate_version="v3")
    # Cross the real external representation boundary; no tuple identity or
    # producer-owned map can be consulted by the verifier below.
    return json.loads(json.dumps(p, ensure_ascii=True, sort_keys=True,
                                 separators=(",", ":")))


def parse_delta(raw, width):
    ans = []
    for item in raw:
        assert isinstance(item, list) and len(item) == 2
        assert isinstance(item[0], str) and item[0]
        lane = item[1]
        assert lane is None or (isinstance(lane, int) and 0 <= lane < width)
        ans.append((item[0], lane))
    assert len({t for t, _ in ans}) == len(ans), "duplicate token delta"
    return tuple(ans)


def parse_overrides(raw, width):
    ans = tuple((int(x[0]), str(x[1])) for x in raw)
    assert ans == tuple(sorted(ans))
    assert len({lane for lane, _ in ans}) == len(ans)
    assert all(0 <= lane < width and mode in MODES for lane, mode in ans)
    return ans


def verify(a, expected_leaves=None):
    c = a["event_certificate"]
    assert c["schema"] == "u0a-butterfly-event-certificate-v3"
    width = int(a["width"])
    assert int(c["width"]) == width and width >= 4
    assert width & (width - 1) == 0
    logw = width.bit_length() - 1
    leaves = tuple((str(t), int(v)) for t, v in c["leaf_table"])
    gates = tuple((str(o), str(x), str(y)) for o, x, y in c["gate_table"])
    if expected_leaves is not None:
        assert len(leaves) == expected_leaves
        assert width == 1 << (max(4, expected_leaves) - 1).bit_length()
    assert len(gates) + 1 == len(leaves)
    assert all(t == f"leaf:{i}" and v >= 0
               for i, (t, v) in enumerate(leaves))

    declared = {t for t, _ in leaves}
    demand = Counter()
    for i, (out, left, right) in enumerate(gates):
        assert out == f"gate:{i}" and out not in declared
        assert left in declared and right in declared and left != right
        declared.add(out)
        demand[left] += 1
        demand[right] += 1
    root = str(c["root_token"])
    assert root in declared and demand[root] == 0
    assert all(demand[t] == (0 if t == root else 1) for t in declared)

    occ = {}
    for token, variable in leaves:
        occ.setdefault(variable, []).append(token)
    used = sorted(occ)
    expected_initial = tuple(sorted((occ[v][0], lane)
                                    for lane, v in enumerate(used)))
    initial = tuple((str(t), int(lane)) for t, lane in c["initial_token_map"])
    assert initial == expected_initial
    assert len({lane for _, lane in initial}) == len(initial)
    assert all(0 <= lane < width for _, lane in initial)
    token_lane = dict(initial)
    lane_token = [None] * width
    for token, lane in initial:
        assert lane_token[lane] is None
        lane_token[lane] = token

    source = tuple((int(lane), str(mode)) for lane, mode in a["source_overrides"])
    assert a["source_default"] == "FIX0"
    assert source == tuple((lane, "FREE") for lane in range(len(used)))

    duplicate_need = [(occ[v][0], token) for v in used for token in occ[v][1:]]
    duplicate_i = nand_i = 0
    raw_overrides = a["raw_gate_overrides"]
    raw_i = 0
    raw = int(a["raw_stage_count"])
    events = c["events"]
    assert len(events) == raw
    counts = Counter()
    delta_records = one_swaps = two_swaps = 0
    max_lane_seen = -1

    for expected_stage, event in enumerate(events, 1):
        assert set(event) == EVENT_KEYS
        stage = int(event["stage"])
        dim = int(event["dimension"])
        kind = str(event["kind"])
        assert stage == expected_stage
        assert 0 <= dim < logw
        assert dim == ((stage - 1) // 2) % logw
        lanes = tuple(int(x) for x in event["lanes"])
        assert all(0 <= x < width for x in lanes)
        if lanes:
            max_lane_seen = max(max_lane_seen, *lanes)
        ovs = parse_overrides(event["mode_overrides"], width)
        supplied = parse_delta(event["token_delta"], width)
        semantic = tuple(event["semantic"])
        counts[kind] += 1
        delta_records += len(supplied)

        # Bind each event override to the single canonical program stream
        # without constructing a second flattened O(events) list.
        for lane, mode in ovs:
            assert raw_i < len(raw_overrides)
            assert raw_overrides[raw_i] == [stage, lane, mode]
            raw_i += 1

        if kind == "WAIT":
            assert lanes == ovs == semantic == supplied == ()
            expected = ()
        elif kind == "SWAP":
            assert len(lanes) == 2 and semantic == ()
            x, y = lanes
            assert x != y and x ^ y == 1 << dim
            assert ovs == tuple(sorted(((x, "COPY_B"), (y, "COPY_B"))))
            tx, ty = lane_token[x], lane_token[y]
            assert tx is not None or ty is not None, "empty/empty route"
            expected = tuple((t, dst) for t, dst in ((tx, y), (ty, x))
                             if t is not None)
            one_swaps += len(expected) == 1
            two_swaps += len(expected) == 2
        elif kind == "DUPLICATE":
            assert len(lanes) == 2 and len(semantic) == 4
            source_t, new_t, sx, sy = semantic
            source_t, new_t = str(source_t), str(new_t)
            sx, sy = int(sx), int(sy)
            x, y = lanes
            assert (x, y) == (sx, sy) and x != y and x ^ y == 1 << dim
            assert token_lane.get(source_t) == x and lane_token[x] == source_t
            assert new_t not in token_lane and lane_token[y] is None
            assert ovs == ((y, "COPY_B"),)
            assert duplicate_i < len(duplicate_need)
            assert (source_t, new_t) == duplicate_need[duplicate_i]
            duplicate_i += 1
            expected = ((new_t, y),)
        elif kind == "NAND":
            assert len(lanes) == 2 and len(semantic) == 5
            left, right, out, sx, sy = semantic
            left, right, out = str(left), str(right), str(out)
            sx, sy = int(sx), int(sy)
            x, y = lanes
            assert (x, y) == (sx, sy) and x != y and x ^ y == 1 << dim
            assert token_lane.get(left) == x and lane_token[x] == left
            assert token_lane.get(right) == y and lane_token[y] == right
            assert left != right and out not in token_lane
            assert ovs == tuple(sorted(((x, "NAND"), (y, "ZERO"))))
            assert nand_i < len(gates)
            gout, gleft, gright = gates[nand_i]
            assert (left, right, out) == (gleft, gright, gout)
            nand_i += 1
            expected = ((left, None), (right, None), (out, x))
        else:
            raise AssertionError(kind)
        assert supplied == expected

        # Independently execute generic simultaneous changes in both maps.
        old_lanes = {}
        for token, after in supplied:
            if token in token_lane:
                old = token_lane.pop(token)
                assert lane_token[old] == token
                lane_token[old] = None
                old_lanes[token] = old
            else:
                assert after is not None, "delete of absent token"
        for token, after in supplied:
            if after is not None:
                assert lane_token[after] is None, "lane collision"
                assert token not in token_lane
                token_lane[token] = after
                lane_token[after] = token
        assert len(token_lane) == sum(x is not None for x in lane_token)

    assert raw_i == len(raw_overrides)
    assert duplicate_i == len(duplicate_need) and nand_i == len(gates)
    final = tuple((str(t), int(lane)) for t, lane in c["final_token_map"])
    assert final == tuple(sorted(token_lane.items()))
    output = int(c["output_lane"])
    assert 0 <= output < width and output == int(a["output_lane"])
    assert token_lane == {root: output} and lane_token[output] == root

    budget = 4 * width * logw * logw + 2 * logw
    assert int(a["gate_stages"]) == budget and raw < budget
    assert a["padding"] == {"start_stage": raw + 1,
                            "count": budget - raw - 1,
                            "default_mode": "COPY_A"}
    assert a["cleanup"] == {"stage": budget, "default_mode": "ZERO",
                             "overrides": [[output, "COPY_A"]]}
    assert a["raw_gate_default"] == "COPY_A"
    assert set(a["event_counts"]) == {"WAIT", "SWAP", "DUPLICATE", "NAND"}
    assert all(int(a["event_counts"][k]) == counts[k]
               for k in ("WAIT", "SWAP", "DUPLICATE", "NAND"))
    return {"leaves": len(leaves), "width": width, "events": raw,
            "delta_records": delta_records, "one_sided_swaps": one_swaps,
            "two_sided_swaps": two_swaps, "max_lane_seen": max_lane_seen,
            "snapshot_fields": sum("token_map_before" in e or
                                   "token_map_after" in e for e in events)}


def rejected(a, expected_leaves):
    try:
        verify(a, expected_leaves)
    except (AssertionError, KeyError, TypeError, ValueError, IndexError):
        return True
    return False


def mutation_suite():
    n = 513
    base = json_artifact(fuzz_formula(n, 31, 0xC0FFEE))
    assert verify(base, n)["width"] == 1024
    mutations = []

    def add(name, change):
        bad = copy.deepcopy(base)
        change(bad)
        mutations.append((name, bad))

    def first(kind, a):
        return next(e for e in a["event_certificate"]["events"]
                    if e["kind"] == kind)

    add("lane-equals-width", lambda a: first("SWAP", a)["lanes"].__setitem__(
        0, a["width"]))
    add("negative-override-lane", lambda a: first("SWAP", a)[
        "mode_overrides"][0].__setitem__(0, -1))
    add("dimension-equals-logwidth", lambda a: first("SWAP", a).__setitem__(
        "dimension", a["width"].bit_length() - 1))
    add("non-neighbor-endpoint", lambda a: first("SWAP", a)["lanes"].__setitem__(
        1, first("SWAP", a)["lanes"][0]))
    add("delta-destination-out-of-range", lambda a: next(
        e for e in a["event_certificate"]["events"] if e["token_delta"]
        and e["token_delta"][0][1] is not None)["token_delta"][0].__setitem__(
            1, a["width"]))
    add("duplicate-source-collision", lambda a: first("DUPLICATE", a)[
        "token_delta"][0].__setitem__(1, first("DUPLICATE", a)["lanes"][0]))
    add("missing-explicit-delta", lambda a: first("NAND", a)[
        "token_delta"].pop())
    add("stage-gap", lambda a: a["event_certificate"]["events"][10].__setitem__(
        "stage", 12))
    add("program-lane-out-of-range", lambda a: a["raw_gate_overrides"][0].__setitem__(
        1, a["width"]))
    add("output-lane-out-of-range", lambda a: a["event_certificate"].__setitem__(
        "output_lane", a["width"]))
    add("snapshot-field-injected", lambda a: first("WAIT", a).__setitem__(
        "token_map_before", []))
    add("forged-double-width", lambda a: (a.__setitem__("width", 2*a["width"]),
                                           a["event_certificate"].__setitem__(
                                               "width", a["width"])))
    names = [name for name, bad in mutations if rejected(bad, n)]
    assert names == [name for name, _ in mutations], names
    return names


def child(n, shape, variables, seed):
    cap = CAP_MIB * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    f = make_formula(n, shape, variables, seed)
    a = json_artifact(f)
    got = verify(a, n)
    assert got["snapshot_fields"] == 0
    # Every event has the short explicit v3 delta field, including WAIT=[];
    # total storage is linear in events rather than live_tokens*events.
    assert all(set(e) == EVENT_KEYS for e in a["event_certificate"]["events"])
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    got.update(shape=shape, variables=variables, seed=seed,
               maxrss_kib=rss, cap_MiB=CAP_MIB)
    assert rss < CAP_MIB * 1024
    print(json.dumps(got, sort_keys=True))


def main():
    if len(sys.argv) == 6 and sys.argv[1] == "--child":
        child(int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
        return
    assert len(sys.argv) == 1
    mutants = mutation_suite()
    cases = []
    for n, shape, variables, seed in LARGE_CASES:
        q = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                            "--child", str(n), shape, str(variables), str(seed)],
                           text=True, capture_output=True, timeout=240)
        assert q.returncode == 0, (n, q.returncode, q.stdout, q.stderr)
        cases.append(json.loads(q.stdout))
    assert [x["leaves"] for x in cases] == [2047, 2048, 2049, 8193]
    assert [x["width"] for x in cases] == [2048, 2048, 4096, 16384]
    print(json.dumps({
        "schema": "u0a-v3-power-boundary-breaker-v1",
        "mutants_rejected": len(mutants), "mutant_names": mutants,
        "large_cases": cases, "cap_MiB_each_child": CAP_MIB,
        "json_roundtrip": True, "full_event_snapshots": False,
        "finite_claim_only": True,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
