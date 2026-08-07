#!/usr/bin/env python3
"""Breaker audit for the canonical sparse U0a program representation.

This independently checks the failure modes that a default-plus-overrides
encoding can hide: duplicate or noncanonical override coordinates, wrong
COPY_A defaults, an off-by-one padding/cleanup boundary, and a streamed target
that disagrees with the eager target.  Claims are finite implementation tests.
"""
from __future__ import annotations

import itertools
import json
import resource
import subprocess
import sys
from pathlib import Path

from verify_u0a_butterfly_formula_compiler import compile_formula, formulas, stage_budget
from verify_u0a_canonical_serialize_manifest import exact_count_model
from verify_u0a_canonical_streaming_emitter import iter_target
from verify_u0a_sparse_program_stream import (
    compile_formula_sparse, dense_equivalent_program_record, gate_mode_at,
    hash_program_stream_sparse, iter_gate_modes, iter_target_sparse,
    output_at, source_mode_at,
)
from verify_u0a_canonical_serialize_manifest import digest_obj, program_record
from verify_u0a_universal_topology_serializer import GATE_MODES

CAP_MIB = 256
RESOURCE_WIDTH = 256


def assert_exact(got, want):
    sentinel = object()
    for i, (a, b) in enumerate(itertools.zip_longest(got, want, fillvalue=sentinel)):
        assert a is not sentinel and b is not sentinel and a == b, (i, a, b)


def audit_one(formula, width, assert_bit):
    sparse = compile_formula_sparse(formula, width=width, assert_bit=assert_bit)
    eager = compile_formula(formula, width=width, assert_bit=assert_bit)
    d = stage_budget(width)

    # The raw override stream is a canonical partial function, not an
    # order-dependent "last write wins" list.
    ov = sparse["raw_gate_overrides"]
    coords = [(s, lane) for s, lane, _ in ov]
    assert coords == sorted(coords)
    assert len(coords) == len(set(coords))
    assert all(1 <= s <= sparse["raw_stage_count"] for s, _ in coords)
    assert all(0 <= lane < width for _, lane in coords)
    assert all(mode in GATE_MODES and mode != "COPY_A" for _, _, mode in ov)
    sov = sparse["source_overrides"]
    assert [lane for lane, _ in sov] == sorted({lane for lane, _ in sov})
    assert all(mode == "FREE" and mode != sparse["source_default"]
               for _, mode in sov)
    oov = sparse["output_overrides"]
    assert [lane for lane, _ in oov] == sorted({lane for lane, _ in oov})
    assert all(value != sparse["output_default"] for _, value in oov)
    assert oov == (((sparse["output_lane"], assert_bit),) if assert_bit else ())

    # Padding is precisely the half-open gap after raw scheduling and before
    # the final cleanup.  Cleanup changes the default to ZERO and preserves
    # exactly the root lane with COPY_A.
    pad = sparse["padding"]
    cleanup = sparse["cleanup"]
    assert pad == {"start_stage": sparse["raw_stage_count"] + 1,
                   "count": d - sparse["raw_stage_count"] - 1,
                   "default_mode": "COPY_A"}
    assert pad["start_stage"] + pad["count"] == d
    assert cleanup == {"stage": d, "default_mode": "ZERO",
                       "overrides": ((sparse["output_lane"], "COPY_A"),)}
    assert all(gate_mode_at(sparse, d, lane) ==
               ("COPY_A" if lane == sparse["output_lane"] else "ZERO")
               for lane in range(width))

    # Full logical grid: exact order, cardinality, random-access lookup, and
    # equality to the old eager implementation.
    streamed = list(iter_gate_modes(sparse))
    assert len(streamed) == width * d
    assert [(s, lane) for s, lane, _ in streamed] == [
        (s, lane) for s in range(1, d + 1) for lane in range(width)]
    assert_exact((mode for _, _, mode in streamed),
                 (eager["modes"][(s, lane)]
                  for s in range(1, d + 1) for lane in range(width)))
    for s, lane, mode in streamed:
        assert gate_mode_at(sparse, s, lane) == mode

    # Source/output defaults and every target row agree, not only a digest.
    assert [source_mode_at(sparse, lane) for lane in range(width)] == eager["source_modes"]
    assert [output_at(sparse, lane) for lane in range(width)] == eager["outputs"]
    target = list(iter_target_sparse(width, d, sparse))
    m, _ = exact_count_model(width, d)
    assert len(target) == m
    assert_exact(target, iter_target(width, d, eager))
    dense_record = program_record(eager)
    assert dense_equivalent_program_record(sparse) == dense_record
    assert hash_program_stream_sparse(sparse)[0] == digest_obj(dense_record)
    return len(ov), len(target)


def limited_child():
    resource.setrlimit(resource.RLIMIT_AS,
                       (CAP_MIB * 1024 * 1024, CAP_MIB * 1024 * 1024))
    p = compile_formula_sparse((0, 1), width=RESOURCE_WIDTH, assert_bit=1)
    digest, cells = hash_program_stream_sparse(p)
    assert cells == RESOURCE_WIDTH * stage_budget(RESOURCE_WIDTH) == 16_781_312
    assert p["dense_mode_cells_retained"] == 0
    assert len(p["raw_gate_overrides"]) == 2
    # The huge target/factor is not traversed here: probe its two program
    # boundaries to distinguish a space repair from a time/output-size claim.
    assert gate_mode_at(p, 1, 0) == "NAND"
    assert gate_mode_at(p, p["gate_stages"], p["output_lane"]) == "COPY_A"
    print("SPARSE_BREAKER_RESOURCE_OK " + json.dumps({
        "width": RESOURCE_WIDTH, "depth": p["gate_stages"],
        "logical_cells_hashed": cells, "sha256": digest,
    }, sort_keys=True))


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--limited-child":
        limited_child()
        return
    assert len(sys.argv) == 1

    # Exhaust all 100 ordered two-variable trees through four leaves at width
    # four, with both assertion bits.  Add width 8/16 cases to cover longer
    # padding, a third butterfly dimension, fanout, and nontrivial cleanup lanes.
    family4 = [f for n in range(2, 5) for f in formulas(n, 2)]
    assert len(family4) == 100
    cases = 0
    max_ov = 0
    for f in family4:
        for bit in (0, 1):
            n, _ = audit_one(f, 4, bit)
            max_ov = max(max_ov, n)
            cases += 1
    extras = [
        ((((0, 1), (2, 0)), ((1, 2), (0, 2))), 8),
        (((((0, 0), 1), (2, 3)), ((1, 2), (3, 0))), 16),
    ]
    for f, w in extras:
        for bit in (0, 1):
            n, _ = audit_one(f, w, bit)
            max_ov = max(max_ov, n)
            cases += 1

    proc = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                           "--limited-child"], capture_output=True, text=True,
                          timeout=90)
    assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
    assert "SPARSE_BREAKER_RESOURCE_OK" in proc.stdout
    print("PASS sparse-program breaker audit")
    print(f"exact eager comparisons={cases}, max_raw_overrides={max_ov}")
    print(proc.stdout.strip())
    print("Scope: finite implementation audit only; the S=256 resource child "
          "hashes the logical program, not the enormous complete factor/target.")


if __name__ == "__main__":
    main()
