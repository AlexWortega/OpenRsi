#!/usr/bin/env python3
"""Finite eager-materialization counterexample after the iterative repair.

The iterative v1 parser/scheduler is not the same thing as the literal full
``serialize`` interface: the latter eagerly creates every padded program mode,
row/column metadata dictionary, sparse C entry, systematic D entry, and target
coordinate in Python containers.  This verifier supplies both a bounded full
pass and a resource-capped finite failure.  The cap is part of the claim.
Nothing here says that the polynomial mathematical construction is impossible,
or that a streaming emitter cannot repair the implementation.
"""
from __future__ import annotations

import json
import os
import resource
import subprocess
import sys
from pathlib import Path

from verify_u0a_canonical_serialize_manifest import (
    encode_formula, exact_count_model, padding_for_S, serialize,
    serialize_dry_run,
)

CAP_MIB = 256


def limited_child():
    cap = CAP_MIB * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))

    # Parsing and scheduling are already iterative and fit this declared cap.
    encoded = encode_formula((0, 1))
    dry = serialize_dry_run(16, encoded)
    assert dry["factor_counts_only"]["C_shape"] == [493440, 330304]

    # The same valid input through the advertised eager full serializer does
    # not fit the cap.  MemoryError is the exact finite implementation result.
    try:
        serialize(16, encoded)
    except MemoryError:
        print("EXPECTED_MEMORYERROR_AFTER_DRY_RUN_PASS")
        return 0
    print("UNEXPECTED_EAGER_SUCCESS")
    return 3


def right_deep(leaves: int):
    assert leaves >= 1
    f = 0
    for _ in range(leaves - 1):
        f = (0, f)
    return f


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--limited-child":
        raise SystemExit(limited_child())
    assert len(sys.argv) == 1

    # Bounded positive control: complete factor, D and target really are
    # materialized at S=4.
    encoded4 = encode_formula((0, 1))
    manifest4, factor4, target4, program4 = serialize(4, encoded4)
    assert factor4["C"]["shape"] == [8060, 5456]
    assert factor4["D"]["shape"] == [8060, 13516]
    assert len(target4) == 8060
    assert len(program4["modes"]) == 4 * 68
    assert manifest4["factor"]["payload_hash"] == (
        "355b469b8ec4c5cc37101ac04c56615b1d64279ba4566d1bcf87078c3ab4b241")

    # Exact eager-container counts.  These are counts, not estimates of bytes.
    counts = {}
    for S in (4, 8, 16, 32, 1101):
        width, depth = padding_for_S(S)
        m, k = exact_count_model(width, depth)
        counts[S] = {
            "width": width,
            "depth": depth,
            "padded_program_mode_cells": width * depth,
            "C_rows": m,
            "C_columns": k,
            "D_columns": m + k,
            # make_factor explicitly inserts one [i,i,1] triple per row,
            # before adding any -C entries.
            "systematic_D_identity_triples_lower_bound": m,
        }
    assert counts[16] == {
        "width": 16, "depth": 1032, "padded_program_mode_cells": 16512,
        "C_rows": 493440, "C_columns": 330304, "D_columns": 823744,
        "systematic_D_identity_triples_lower_bound": 493440,
    }
    assert counts[1101] == {
        "width": 2048, "depth": 991254,
        "padded_program_mode_cells": 2030088192,
        "C_rows": 60900681684, "C_columns": 40601772032,
        "D_columns": 101502453716,
        "systematic_D_identity_triples_lower_bound": 60900681684,
    }

    # Old deep witness passes the repaired iterative canonical/scheduler path;
    # its dry manifest deliberately omits program grid, factor and target.
    deep_encoded = encode_formula(right_deep(1101))
    deep_dry = serialize_dry_run(1101, deep_encoded)
    assert deep_dry["input"]["formula_statistics"]["leaf_occurrences"] == 1101
    assert deep_dry["program_schedule"]["materialized"] is False
    assert deep_dry["program_schedule"]["gate_stages"] == 991254
    assert deep_dry["factor_counts_only"]["factor_materialized"] is False

    # Isolate the cap so the main verifier remains able to print its result.
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    proc = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "--limited-child"],
        text=True, capture_output=True, env=env, timeout=30,
    )
    assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
    assert proc.stdout.strip() == "EXPECTED_MEMORYERROR_AFTER_DRY_RUN_PASS"

    summary = {
        "finite_claim_only": True,
        "bounded_full_serialize_pass": {
            "S": 4,
            "C_shape": factor4["C"]["shape"],
            "D_shape": factor4["D"]["shape"],
            "target_coordinates": len(target4),
        },
        "iterative_deep_dry_run_pass": {
            "S": 1101,
            "leaves": 1101,
            "width": deep_dry["padding"]["width"],
            "depth": deep_dry["padding"]["gate_stages"],
        },
        "resource_capped_eager_counterexample": {
            "S": 16,
            "formula": "(V0 NAND V1)",
            "RLIMIT_AS_MiB": CAP_MIB,
            "result": proc.stdout.strip(),
        },
        "exact_container_counts": {str(k): v for k, v in counts.items()},
        "interpretation": (
            "The recursion repair establishes iterative parse/scheduling only. "
            "The current full serializer is still eager and fails this explicit "
            "finite memory cap. Counts remain polynomial; this is not a "
            "mathematical impossibility and a streaming emitter may repair it."
        ),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("PASS: exact bounded eager-materialization resource counterexample")


if __name__ == "__main__":
    main()
