#!/usr/bin/env python3
"""Finite breaker: factor streaming does not yet stream the dense program.

The Generation-14 factor emitter honestly declares that it retains the eager
padded program.  This verifier pins the remaining practical consequence: at
S=128, a valid two-leaf formula still raises MemoryError under 256 MiB before
matrix streaming begins.  The emitted object has polynomial size, so this is
an implementation/cap counterexample only, not a mathematical impossibility.
"""
from __future__ import annotations

import resource
import subprocess
import sys
from pathlib import Path

from verify_u0a_butterfly_formula_compiler import stage_budget
from verify_u0a_canonical_serialize_manifest import encode_formula, padding_for_S
from verify_u0a_canonical_streaming_emitter import stream_serialize

CAP_MIB = 256
S = 128


def child():
    cap = CAP_MIB * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    try:
        stream_serialize(S, encode_formula((0, 1)))
    except MemoryError:
        print("EXPECTED_DENSE_PROGRAM_MEMORY_ERROR")
        return 0
    print("UNEXPECTED_SUCCESS")
    return 1


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--child":
        raise SystemExit(child())
    assert len(sys.argv) == 1
    width, depth = padding_for_S(S)
    assert (width, depth) == (128, stage_budget(128)) == (128, 25102)
    # compile_formula eagerly constructs this many dictionary entries even for
    # the tiny formula, because formula-oblivious padding is dense.
    assert width * depth == 3_213_056
    proc = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "--child"],
        capture_output=True, text=True, timeout=90,
    )
    assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
    assert "EXPECTED_DENSE_PROGRAM_MEMORY_ERROR" in proc.stdout
    print("certified remaining streamed-program resource failure")
    print("S=128, width=128, depth=25102, dense mode cells=3213056")
    print("fresh address-space cap: 256 MiB; result: MemoryError")
    print("scope: practical implementation cap only; counts remain polynomial")


if __name__ == "__main__":
    main()
