#!/usr/bin/env python3
"""Finite regression for the repaired deep-formula compiler front end.

Two layers are checked at a deliberately low recursion limit.  A 61-leaf
right-deep formula is fully compiled to its padded width-64 modes grid and
simulated.  The former 1,101-leaf counterexample is canonically encoded,
decoded, and exactly scheduled in dry-run form, avoiding the roughly two
billion mode cells of its width-2048 padded grid.

This is finite implementation evidence only.  The large dry run does not emit
C, D, target_y, or a GapCVP instance and proves no soundness or hardness claim.
"""
from __future__ import annotations

import hashlib
import json
import sys

from verify_u0a_butterfly_formula_compiler import (
    compile_formula, compile_formula_dry_run, eval_formula, simulate,
)
from verify_u0a_canonical_serialize_manifest import (
    decode_formula, encode_formula, formula_statistics, serialize_dry_run,
)


def right_deep(extra_gates):
    formula = 0
    for _ in range(extra_gates):
        formula = (0, formula)
    return formula


def main():
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(50)
    try:
        # A real materialized compile, not merely a parser test.
        medium = right_deep(60)
        medium_encoded = encode_formula(medium)
        medium_decoded = decode_formula(medium_encoded)
        assert encode_formula(medium_decoded) == medium_encoded
        p = compile_formula(medium_decoded)
        d = compile_formula_dry_run(medium_decoded)
        assert p["width"] == 64 and p["gate_stages"] == 9228
        assert p["output_lane"] == d["output_lane"]
        assert p["raw_events"] == d["raw_events"]
        first_pad = next(i for i, event in enumerate(p["trace"])
                         if event["kind"] == "PAD")
        assert first_pad == d["raw_stage_count_before_padding"]
        for bit in (0, 1):
            assignment = {0: bit}
            vals = simulate(p, assignment)
            assert vals[(p["gate_stages"], p["output_lane"])] == eval_formula(
                medium_decoded, assignment)

        # The exact former blocker: its padded grid would have about two
        # billion entries, so totality is certified through the dry-run layer.
        deep = right_deep(1100)
        deep_encoded = encode_formula(deep)
        deep_decoded = decode_formula(deep_encoded)
        assert encode_formula(deep_decoded) == deep_encoded
        stats = formula_statistics(deep_decoded)
        assert stats == {"leaf_occurrences": 1101, "nand_gates": 1100,
                         "nodes": 2201, "variables": [0]}
        manifest = serialize_dry_run(1101, deep_encoded)
        schedule = manifest["program_schedule"]
        direct = compile_formula_dry_run(deep_decoded)
        assert schedule == direct
        assert schedule["width"] == 2048
        assert schedule["gate_stages"] == 991254
        assert schedule["leaf_occurrences"] == 1101
        assert schedule["nand_gates"] == 1100
        assert schedule["raw_stage_count_before_padding"] < schedule["gate_stages"]
        assert schedule["pad_stages"] + schedule["raw_stage_count_before_padding"] + 1 == schedule["gate_stages"]
        assert manifest["factor_counts_only"]["factor_materialized"] is False
    finally:
        sys.setrecursionlimit(old_limit)

    summary = {
        "finite_claim_only": True,
        "recursion_limit_during_test": 50,
        "materialized_witness": {
            "leaf_occurrences": 61,
            "nand_gates": 60,
            "width": p["width"],
            "gate_stages": p["gate_stages"],
            "canonical_encoding_sha256": hashlib.sha256(medium_encoded).hexdigest(),
        },
        "repaired_old_witness": {
            "leaf_occurrences": stats["leaf_occurrences"],
            "nand_gates": stats["nand_gates"],
            "width": schedule["width"],
            "gate_stages": schedule["gate_stages"],
            "raw_stage_count_before_padding": schedule["raw_stage_count_before_padding"],
            "pad_stages": schedule["pad_stages"],
            "unpadded_trace_sha256": schedule["unpadded_trace_sha256"],
            "canonical_encoding_sha256": hashlib.sha256(deep_encoded).hexdigest(),
            "dry_manifest_sha256": manifest["manifest_hash_excluding_this_field"],
        },
        "scope": "finite iterative parse/encode/scheduling repair; large C,D,target are deliberately not materialized",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("PASS: former 1,101-leaf RecursionError witness passes iterative dry-run serialization")


if __name__ == "__main__":
    main()
