#!/usr/bin/env python3
"""Machine gate for a proofs generation: exit 0 only if the result packet is
well-formed and every verifier it names passes.

Usage:
  gate_verify.py <run_dir> <packet_path>

Python verifiers must live at experiments/verify_*.py or gen-N/experiments/verify_*.py
and exit 0. Lean verifiers must live at lean/Verify_*.lean, contain no sorry/admit/axiom,
and compile via `lake env lean` inside OPENRSI_LEAN_PROJECT.

Designed to be passed to a worker as an autonomous completion gate, so the worker keeps
going until the same checks the harness will run independently actually pass. Failure
output is written to stdout so the worker sees exactly what to fix.
"""
import json
import os
import re
import subprocess
import sys

PY_RE = re.compile(r"^(?:experiments|gen-\d+/experiments)/verify_[^/]+\.py$")
LEAN_RE = re.compile(r"^lean/[Vv]erify_[^/]+\.lean$")
BANNED = re.compile(r"\b(sorry|admit)\b|^\s*axiom\b", re.MULTILINE)
PY_TIMEOUT = int(os.environ.get("OPENRSI_VERIFIER_TIMEOUT_S", "600"))
LEAN_TIMEOUT = int(os.environ.get("OPENRSI_LEAN_TIMEOUT_S", "900"))


def fail(message):
    print(f"GATE FAIL: {message}")
    sys.exit(1)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    run_dir = os.path.abspath(sys.argv[1])
    packet_path = os.path.abspath(sys.argv[2])

    if not os.path.exists(packet_path):
        fail(f"result packet {os.path.relpath(packet_path, run_dir)} does not exist yet")
    try:
        packet = json.load(open(packet_path))
    except (json.JSONDecodeError, OSError) as e:
        fail(f"result packet is not readable JSON: {e}")

    missing = [k for k in ("summary", "hypothesis", "verifiers", "claimed_progress") if k not in packet]
    if missing:
        fail(f"result packet is missing required keys: {', '.join(missing)}")
    verifiers = packet.get("verifiers")
    if not isinstance(verifiers, list) or not 1 <= len(verifiers) <= 5:
        fail("result packet must name 1-5 verifier paths in its verifiers array")
    if packet.get("claimed_progress") not in ("NONE", "FINITE", "LEMMA", "GOAL"):
        fail("claimed_progress must be one of NONE, FINITE, LEMMA, GOAL")

    lean_project = os.environ.get("OPENRSI_LEAN_PROJECT", os.path.expanduser("~/leanverify"))
    lake = os.environ.get("OPENRSI_LAKE", os.path.expanduser("~/.elan/bin/lake"))

    for item in verifiers:
        rel = str(item)
        absolute = os.path.abspath(os.path.join(run_dir, rel))
        if not absolute.startswith(run_dir + os.sep):
            fail(f"verifier path escapes the run directory: {rel}")
        is_lean = bool(LEAN_RE.match(rel))
        if not is_lean and not PY_RE.match(rel):
            fail(f"verifier path {rel} is not experiments/verify_*.py or lean/Verify_*.lean")
        if not os.path.exists(absolute):
            fail(f"named verifier {rel} does not exist")

        if is_lean:
            source = open(absolute, encoding="utf-8", errors="replace").read()
            if BANNED.search(source):
                fail(f"{rel} contains sorry/admit/axiom, so it proves nothing")
            cmd, cwd, timeout = [lake, "env", "lean", absolute], lean_project, LEAN_TIMEOUT
        else:
            cmd, cwd, timeout = [sys.executable, absolute], run_dir, PY_TIMEOUT

        try:
            done = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            fail(f"{rel} did not finish within {timeout}s")
        except OSError as e:
            fail(f"{rel} could not be executed: {e}")
        if done.returncode != 0:
            tail = (done.stdout + done.stderr)[-4000:]
            fail(f"{rel} exited {done.returncode}\n{tail}")

    print(f"GATE PASS: packet valid, {len(verifiers)} verifier(s) passed")


if __name__ == "__main__":
    main()
