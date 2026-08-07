#!/usr/bin/env python3
"""Independent mutation and resource breaker for the v2 delta certificate.

The checker consumes only a JSON round-tripped sparse-program artifact.  It
reconstructs the live token map from the initial map and the event deltas; it
does not call the scheduler.  Optional checkpoint hashes use a length-framed,
domain-separated canonical JSON encoding and are checked against replay state.

This is finite implementation evidence, not a universal compiler theorem.
"""
from __future__ import annotations

import copy
import hashlib
import itertools
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
EVENT_KEYS = {"stage", "kind", "dimension", "lanes", "mode_overrides", "semantic"}


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


def _snapshot(seq, width):
    """Parse and enforce the unique canonical token-to-lane representation."""
    ans = tuple((str(t), int(lane)) for t, lane in seq)
    assert ans == tuple(sorted(ans))
    assert len({t for t, _ in ans}) == len(ans)
    assert len({lane for _, lane in ans}) == len(ans)
    assert all(0 <= lane < width for _, lane in ans)
    return ans


def snapshot_bytes(snapshot):
    """Unambiguous bytes: domain and byte length frame canonical JSON."""
    body = json.dumps(list(snapshot), ensure_ascii=True, sort_keys=False,
                      separators=(",", ":")).encode("ascii")
    return b"u0a/token-map-checkpoint/v1\0" + len(body).to_bytes(8, "big") + body


def snapshot_digest(snapshot):
    return hashlib.sha256(snapshot_bytes(snapshot)).hexdigest()


def build_artifact(formula, width=None, assert_bit=1):
    """Producer boundary followed by serialization and optional checkpoints."""
    p = compile_formula_sparse(formula, width=width, assert_bit=assert_bit,
                               certificate_version="v2")
    a = json.loads(json.dumps(p, sort_keys=True, separators=(",", ":")))
    c = a["event_certificate"]
    raw = int(a["raw_stage_count"])
    # Optional endpoint checkpoints are small; the verifier derives their
    # truth from replay rather than trusting the supplied maps.
    c["checkpoints"] = [
        [0, snapshot_digest(_snapshot(c["initial_token_map"], int(a["width"])))],
    ]
    if raw:
        c["checkpoints"].append(
            [raw, snapshot_digest(_snapshot(c["final_token_map"], int(a["width"])))])
    return a


def _mode_overrides(event, width):
    ans = tuple((int(lane), str(mode)) for lane, mode in event["mode_overrides"])
    assert ans == tuple(sorted(ans))
    assert len({lane for lane, _ in ans}) == len(ans)
    assert all(0 <= lane < width and mode in {"COPY_B", "NAND", "ZERO"}
               for lane, mode in ans)
    return ans


def verify_delta_certificate(a):
    """Independently replay and bind every v2 delta to program overrides."""
    c = a["event_certificate"]
    assert c["schema"] == "u0a-butterfly-event-certificate-v2"
    w, raw, depth = int(a["width"]), int(a["raw_stage_count"]), int(a["gate_stages"])
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
    initial = _snapshot(c["initial_token_map"], w)
    assert initial == expected_initial
    state = dict(initial)
    assert a["source_default"] == "FIX0"
    assert tuple((int(x), str(y)) for x, y in a["source_overrides"]) == tuple(
        (lane, "FREE") for lane in range(len(used_vars)))

    checkpoints = tuple((int(stage), str(digest)) for stage, digest in c.get("checkpoints", ()))
    assert all(0 <= stage <= raw and len(digest) == 64 and
               digest == digest.lower() and all(x in "0123456789abcdef" for x in digest)
               for stage, digest in checkpoints)
    assert all(a0 < b0 for (a0, _), (b0, _) in zip(checkpoints, checkpoints[1:]))
    cp = dict(checkpoints)
    if 0 in cp:
        assert cp[0] == snapshot_digest(tuple(sorted(state.items())))

    demanded_duplicates = [(occurrences[v][0], token)
                            for v in used_vars for token in occurrences[v][1:]]
    demanded_nands = [(left, right, out) for out, left, right in gates]
    duplicate_seen, nand_seen, flat = [], [], []
    counts = Counter()
    events = c["events"]
    assert len(events) == raw
    for expected_stage, event in enumerate(events, 1):
        # No hidden full snapshots or unverified extension fields in v2 events.
        assert set(event) == EVENT_KEYS
        stage, kind, dim = int(event["stage"]), str(event["kind"]), int(event["dimension"])
        assert stage == expected_stage
        assert dim == ((stage - 1) // 2) % logw
        lanes = tuple(int(x) for x in event["lanes"])
        assert all(0 <= x < w for x in lanes)
        ovs = _mode_overrides(event, w)
        flat.extend((stage, lane, mode) for lane, mode in ovs)
        sem = tuple(event["semantic"])
        counts[kind] += 1

        if kind == "WAIT":
            assert lanes == () and ovs == () and sem == ()
        elif kind == "SWAP":
            assert len(lanes) == 2 and lanes[0] != lanes[1]
            x, y = lanes
            assert x ^ y == 1 << dim
            assert ovs == tuple(sorted(((x, "COPY_B"), (y, "COPY_B"))))
            assert sem == ()
            for token in tuple(state):
                if state[token] == x:
                    state[token] = y
                elif state[token] == y:
                    state[token] = x
        elif kind == "DUPLICATE":
            assert len(sem) == 4 and len(lanes) == 2 and lanes[0] != lanes[1]
            source, new, x0, y0 = sem
            source, new, x, y = str(source), str(new), int(x0), int(y0)
            assert lanes == (x, y) and source in state and state[source] == x
            assert new not in state and y not in state.values() and x ^ y == 1 << dim
            assert ovs == ((y, "COPY_B"),)
            state[new] = y
            duplicate_seen.append((source, new))
        elif kind == "NAND":
            assert len(sem) == 5 and len(lanes) == 2 and lanes[0] != lanes[1]
            left, right, out, x0, y0 = sem
            left, right, out = str(left), str(right), str(out)
            x, y = int(x0), int(y0)
            assert left != right and lanes == (x, y)
            assert left in state and right in state and out not in state
            assert state[left] == x and state[right] == y and x ^ y == 1 << dim
            assert ovs == tuple(sorted(((x, "NAND"), (y, "ZERO"))))
            del state[left]
            del state[right]
            state[out] = x
            nand_seen.append((left, right, out))
        else:
            raise AssertionError(kind)

        # This also rejects a checkpoint whose digest was made from an
        # ambiguous or noncanonical token-map serialization.
        if stage in cp:
            assert cp[stage] == snapshot_digest(tuple(sorted(state.items())))

    assert duplicate_seen == demanded_duplicates
    assert nand_seen == demanded_nands
    expected_flat = [(int(s), int(l), str(m)) for s, l, m in a["raw_gate_overrides"]]
    assert flat == expected_flat
    assert dict(_snapshot(c["final_token_map"], w)) == state
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
    return {"events": raw, "overrides": len(flat), "checkpoints": len(checkpoints)}


def rejected(a):
    try:
        verify_delta_certificate(a)
    except (AssertionError, KeyError, TypeError, ValueError):
        return True
    return False


def mutation_suite(base):
    mutants = []

    # Missing live token at initialization.
    bad = copy.deepcopy(base)
    bad["event_certificate"]["initial_token_map"].pop()
    mutants.append(("missing-token", bad))

    # Duplicate lane ownership (even if token names remain distinct).
    bad = copy.deepcopy(base)
    im = bad["event_certificate"]["initial_token_map"]
    im[1][1] = im[0][1]
    mutants.append(("duplicate-lane", bad))

    # Reordered records are not repaired by the replay checker.
    bad = copy.deepcopy(base)
    ev = bad["event_certificate"]["events"]
    ev[0], ev[1] = ev[1], ev[0]
    mutants.append(("wrong-event-order", bad))

    # Omit a program override while leaving the event delta untouched.
    bad = copy.deepcopy(base)
    bad["raw_gate_overrides"].pop(0)
    mutants.append(("omitted-program-override", bad))

    # Omit the event-side override as well: semantics still force it.
    bad = copy.deepcopy(base)
    active = next(e for e in bad["event_certificate"]["events"] if e["mode_overrides"])
    active["mode_overrides"].pop()
    mutants.append(("omitted-event-override", bad))

    # A well-formed digest of a different state cannot validate this checkpoint.
    bad = copy.deepcopy(base)
    wrong = (("leaf:1", 23),)
    bad["event_certificate"]["checkpoints"][0][1] = snapshot_digest(wrong)
    mutants.append(("checkpoint-hash-state-substitution", bad))

    # Missing semantic token after an otherwise syntactically valid JSON edit.
    bad = copy.deepcopy(base)
    active = next(e for e in bad["event_certificate"]["events"]
                  if e["kind"] in ("DUPLICATE", "NAND"))
    active["semantic"][0] = "missing:token"
    mutants.append(("missing-semantic-token", bad))

    rejected_names = [name for name, bad in mutants if rejected(bad)]
    assert rejected_names == [name for name, _ in mutants], rejected_names

    # Finite ambiguity probes against the old unsafe idea of delimiter-free
    # concatenation.  Canonical framed bytes (and their concrete SHA-256s) differ.
    probes = [
        (("leaf:1", 23),),
        (("leaf:12", 3),),
        (("x|1", 23),),
        (("x", 1), ("y", 23)),
    ]
    enc = [snapshot_bytes(x) for x in probes]
    dig = [snapshot_digest(x) for x in probes]
    assert len(set(enc)) == len(enc) and len(set(dig)) == len(dig)
    return rejected_names, len(probes)


def limited_child(n):
    cap = CAP_MIB * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    a = build_artifact(comb(n))
    got = verify_delta_certificate(a)
    # Explicitly exclude the retired quadratic full snapshots.
    assert all("token_map_before" not in e and "token_map_after" not in e
               for e in a["event_certificate"]["events"])
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(json.dumps({"leaves": n, "width": a["width"], **got,
                      "maxrss_kib": rss}, sort_keys=True))


def main():
    family = [f for n in range(1, 5) for f in formulas(n, 2)]
    assert len(family) == 102
    event_total = 0
    for f in family:
        event_total += verify_delta_certificate(build_artifact(f, width=4))["events"]
    wide = verify_delta_certificate(build_artifact(
        balanced(tuple(i % 4 for i in range(16))), width=16))

    base = build_artifact(((0, 1), (2, 3)), width=4)
    rejected_names, ambiguity_probes = mutation_suite(base)

    q = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "--limited-child",
         str(RESOURCE_LEAVES)], text=True, capture_output=True, timeout=180,
    )
    assert q.returncode == 0, (q.returncode, q.stdout, q.stderr)
    capped = json.loads(q.stdout)
    assert capped["leaves"] == RESOURCE_LEAVES and capped["maxrss_kib"] < CAP_MIB * 1024
    print(json.dumps({
        "schema": "u0a-delta-event-certificate-breaker-v1",
        "small_formulas": len(family), "small_events": event_total,
        "width16_events": wide["events"],
        "mutants_rejected": len(rejected_names), "mutant_names": rejected_names,
        "checkpoint_ambiguity_probes": ambiguity_probes,
        "resource": capped, "cap_MiB": CAP_MIB, "finite_claim_only": True,
    }, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--limited-child":
        limited_child(int(sys.argv[2]))
    else:
        assert len(sys.argv) == 1
        main()
