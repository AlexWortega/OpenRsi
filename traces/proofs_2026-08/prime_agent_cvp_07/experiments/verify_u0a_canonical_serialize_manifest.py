#!/usr/bin/env python3
"""Canonical finite Serialize(S,F) manifest and actual-factor stress audit.

This makes the Generation-11 interface byte-level precise on a declared
formula domain.  S is a *leaf-occurrence capacity*.  A formula is an ordered
binary NAND tree with at most S leaves and variable indices in [0,S).  Its
only accepted wire encoding is canonical JSON using ["V",i] and ["N",a,b].

For fixed S, padding width/depth and hence the complete sparse C and
D=[I|-C], row marks, and column marks are independent of F and of an
assignment.  F changes only the declared program/output target rows.  The
main audit is finite (all 100 ordered two-variable trees with 2--4 leaves,
and their 400 assignments); the displayed polynomial inequalities are
executable arithmetic checks, not an asymptotic proof or a soundness claim.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass
from functools import lru_cache

from verify_u0a_butterfly_formula_compiler import (
    compile_formula, compile_formula_dry_run, formulas, leaves_and_gates,
    stage_budget, verify_program,
)
from verify_u0a_universal_topology_serializer import make_factor, target_y

SCHEMA = "u0a-canonical-serialize-manifest-v1"
MUTABLE_TARGET_KINDS = {"SOURCE_PROGRAM", "GATE_PROGRAM", "OUTPUT_INTERFACE"}


class CanonicalInputError(ValueError):
    pass


def canonical_bytes(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_bytes(x):
    return hashlib.sha256(x).hexdigest()


def digest_obj(x):
    return digest_bytes(canonical_bytes(x))


def ast_of_formula(f):
    """Construct the wire AST iteratively (mainly for compatibility/tests)."""
    work = [(f, False)]
    results = []
    while work:
        node, exiting = work.pop()
        if type(node) is int and node >= 0:  # bool is deliberately not a leaf
            results.append(["V", node])
        elif type(node) is tuple and len(node) == 2:
            if not exiting:
                work.append((node, True))
                work.append((node[1], False))
                work.append((node[0], False))
            else:
                right = results.pop()
                left = results.pop()
                results.append(["N", left, right])
        else:
            raise CanonicalInputError(
                "formula must be a tuple NAND tree over nonnegative integer leaves")
    if len(results) != 1:
        raise CanonicalInputError("bad formula")
    return results[0]


def parse_ast(x):
    """Inverse of ``ast_of_formula`` with an explicit return-value stack."""
    work = [(x, False)]
    results = []
    while work:
        node, exiting = work.pop()
        if type(node) is list and len(node) == 2 and node[0] == "V":
            if type(node[1]) is not int or node[1] < 0:
                raise CanonicalInputError("bad variable")
            results.append(node[1])
        elif type(node) is list and len(node) == 3 and node[0] == "N":
            if not exiting:
                work.append((node, True))
                work.append((node[2], False))
                work.append((node[1], False))
            else:
                right = results.pop()
                left = results.pop()
                results.append((left, right))
        else:
            raise CanonicalInputError("bad canonical NAND AST")
    if len(results) != 1:
        raise CanonicalInputError("bad canonical NAND AST")
    return results[0]


def encode_formula(f):
    """Emit the exact v1 canonical JSON grammar without recursive json.dumps."""
    out = bytearray()
    work = [f]
    while work:
        node = work.pop()
        if type(node) is bytes:
            out.extend(node)
        elif type(node) is int and node >= 0:
            out.extend(b'["V",')
            out.extend(str(node).encode("ascii"))
            out.extend(b']')
        elif type(node) is tuple and len(node) == 2:
            # Stack order is the reverse of ["N", left, right].
            work.extend((b']', node[1], b',', node[0], b'["N",'))
        else:
            raise CanonicalInputError(
                "formula must be a tuple NAND tree over nonnegative integer leaves")
    return bytes(out)


def decode_formula(encoded):
    """Parse only the exact canonical v1 bytes, using no recursive JSON parser."""
    if type(encoded) is not bytes:
        raise CanonicalInputError("encoding must be bytes")
    pos = 0
    values = []
    tasks = [("parse", None)]
    n = len(encoded)
    try:
        while tasks:
            kind, payload = tasks.pop()
            if kind == "literal":
                literal = payload
                if not encoded.startswith(literal, pos):
                    raise CanonicalInputError("noncanonical JSON bytes")
                pos += len(literal)
            elif kind == "parse":
                if encoded.startswith(b'["V",', pos):
                    pos += 5
                    start = pos
                    while pos < n and 48 <= encoded[pos] <= 57:
                        pos += 1
                    if start == pos or pos >= n or encoded[pos] != ord(']'):
                        raise CanonicalInputError("bad variable")
                    digits = encoded[start:pos]
                    if len(digits) > 1 and digits[0] == ord('0'):
                        raise CanonicalInputError("noncanonical integer")
                    values.append(int(digits))
                    pos += 1
                elif encoded.startswith(b'["N",', pos):
                    pos += 5
                    # parse left, comma, parse right, close, then combine
                    tasks.append(("combine", None))
                    tasks.append(("literal", b']'))
                    tasks.append(("parse", None))
                    tasks.append(("literal", b','))
                    tasks.append(("parse", None))
                else:
                    raise CanonicalInputError("bad canonical NAND AST")
            else:
                right = values.pop()
                left = values.pop()
                values.append((left, right))
    except (IndexError, ValueError) as exc:
        raise CanonicalInputError("bad canonical NAND AST") from exc
    if pos != n or len(values) != 1:
        raise CanonicalInputError("noncanonical JSON bytes")
    return values[0]


def formula_statistics(f):
    leaves, gates, _ = leaves_and_gates(f)
    variables = sorted({v for _, v in leaves})
    return {"leaf_occurrences": len(leaves), "nand_gates": len(gates),
            "nodes": len(leaves) + len(gates), "variables": variables}


def padding_for_S(S):
    if type(S) is not int or S < 2:
        raise CanonicalInputError("S must be an integer at least 2")
    width = 1 << (max(4, S) - 1).bit_length()
    return width, stage_budget(width)


def exact_count_model(width, depth):
    k = 4 * width + 20 * width * depth
    m = 30 * width * depth + 9 * width - 2 * depth
    return m, k


def program_record(p):
    """JSON-safe, fully ordered record; no Python tuple-key dictionaries."""
    w, d = p["width"], p["gate_stages"]
    return {
        "source_modes": list(p["source_modes"]),
        "gate_modes_stage_major": [
            [p["modes"][(s, lane)] for lane in range(w)]
            for s in range(1, d + 1)
        ],
        "outputs": list(p["outputs"]),
        "output_lane": p["output_lane"],
        "assert_bit": p["assert_bit"],
    }


def serialize(S, encoded_formula, factor=None):
    """Return the canonical manifest plus the complete actual factor and target."""
    f = decode_formula(encoded_formula)
    stats = formula_statistics(f)
    if stats["leaf_occurrences"] > S:
        raise CanonicalInputError("formula exceeds declared leaf capacity S")
    if stats["variables"] and stats["variables"][-1] >= S:
        raise CanonicalInputError("variable index is outside [0,S)")
    width, depth = padding_for_S(S)
    p = compile_formula(f, width=width, assert_bit=1)
    if factor is None:
        factor, _, _ = make_factor(width, depth)
    assert factor["width"] == width and factor["gate_stages"] == depth
    m, k = exact_count_model(width, depth)
    assert factor["C"]["shape"] == [m, k]
    assert factor["D"]["shape"] == [m, m + k]
    t = target_y(factor, p["source_modes"], p["modes"], p["outputs"])
    rec = program_record(p)
    manifest = {
        "schema": SCHEMA,
        "input": {
            "S_leaf_capacity": S,
            "formula_encoding_ascii": encoded_formula.decode("ascii"),
            "formula_sha256": digest_bytes(encoded_formula),
            "formula_statistics": stats,
        },
        "padding": {"width": width, "gate_stages": depth,
                    "rule": "w=nextPow2(max(4,S)); d=4*w*log2(w)^2+2*log2(w)"},
        "dependency_contract": {
            "factor_key": [S, width, depth],
            "formula_independent": ["row_marks", "column_marks", "C", "D"],
            "formula_dependent": ["program_record", "target_y"],
            "assignment_dependent": [],
            "mutable_target_row_kinds": sorted(MUTABLE_TARGET_KINDS),
        },
        "factor": {
            "schema": factor["schema"],
            "C_shape": factor["C"]["shape"],
            "D_shape": factor["D"]["shape"],
            "C_nnz": len(factor["C"]["entries"]),
            "D_nnz": len(factor["D"]["entries"]),
            "component_hashes": factor["component_hashes"],
            "payload_hash": factor["payload_hash_excluding_this_field"],
        },
        "program_record": rec,
        "program_sha256": digest_obj(rec),
        "target_y": t,
        "target_y_sha256": digest_obj(t),
    }
    manifest["manifest_hash_excluding_this_field"] = digest_obj(manifest)
    return manifest, factor, t, p


def serialize_dry_run(S, encoded_formula):
    """Validate and schedule a large input without constructing C, D or target.

    The returned manifest is a finite implementation witness for parsing and
    placement totality only.  Exact factor *shapes* follow ``exact_count_model``;
    factor entries and target rows are intentionally not claimed or hashed.
    """
    f = decode_formula(encoded_formula)
    stats = formula_statistics(f)
    if stats["leaf_occurrences"] > S:
        raise CanonicalInputError("formula exceeds declared leaf capacity S")
    if stats["variables"] and stats["variables"][-1] >= S:
        raise CanonicalInputError("variable index is outside [0,S)")
    width, depth = padding_for_S(S)
    schedule = compile_formula_dry_run(f, width=width, assert_bit=1)
    m, k = exact_count_model(width, depth)
    manifest = {
        "schema": "u0a-canonical-serialize-dry-run-v1",
        "input": {
            "S_leaf_capacity": S,
            "formula_sha256": digest_bytes(encoded_formula),
            "formula_encoding_bytes": len(encoded_formula),
            "formula_statistics": stats,
        },
        "padding": {"width": width, "gate_stages": depth},
        "factor_counts_only": {
            "C_shape": [m, k], "D_shape": [m, m + k],
            "factor_materialized": False,
        },
        "program_schedule": schedule,
        "scope": ("iterative canonical parse and exact scheduler decisions; "
                  "no C/D entries, target_y, assignment audit, soundness, or gap"),
    }
    manifest["manifest_hash_excluding_this_field"] = digest_obj(manifest)
    return manifest


def check_polynomial_count_bounds():
    """Check the stated coarse bounds over a wide finite integer range.

    For S>=4: w<2S, log2(w)<=S, d<=48S^3, k<=1928S^4,
    m<=2898S^4, and m+k<=4826S^4.  The inequalities also follow by the
    displayed substitutions, but this script provides finite regression only.
    """
    for S in range(4, 4097):
        w, d = padding_for_S(S)
        m, k = exact_count_model(w, d)
        assert w < 2*S
        assert w.bit_length() - 1 <= S
        assert d <= 48*S**3
        assert k <= 1928*S**4
        assert m <= 2898*S**4
        assert m + k <= 4826*S**4
        # Even the dense encoding is polynomial; actual factors are sparse.
        assert m * k + m <= 2898 * (1928 + 1) * S**8


def main():
    check_polynomial_count_bounds()

    # Strict byte-level decoder: alternative JSON whitespace is not accepted,
    # and invalid domain declarations are rejected deterministically.
    f0 = (0, 1)
    assert decode_formula(encode_formula(f0)) == f0
    rejected = 0
    for bad_S, bad in [
        (4, b'["N", ["V",0], ["V",1]]'),  # valid JSON, noncanonical bytes
        (4, b'["X",["V",0],["V",1]]'),
        (4, b'["V",true]'),
        (2, b'["V",2]'),                 # canonical but variable outside domain
    ]:
        try:
            serialize(bad_S, bad)
        except CanonicalInputError:
            rejected += 1
    assert rejected == 4

    S = 4
    width, depth = padding_for_S(S)
    factor, _, _ = make_factor(width, depth)
    # Re-emission is byte-identical all the way through the complete C,D.
    factor2, _, _ = make_factor(width, depth)
    assert canonical_bytes(factor2) == canonical_bytes(factor)
    del factor2

    family = [f for n in range(2, 5) for f in formulas(n, 2)]
    assert len(family) == 100
    encodings = [encode_formula(f) for f in family]
    assert len(set(encodings)) == 100
    assert len({digest_bytes(e) for e in encodings}) == 100

    baseline_components = factor["component_hashes"]
    baseline_payload_hash = factor["payload_hash_excluding_this_field"]
    first_fixed_target = None
    manifests = []
    assignment_checks = 0
    for f, encoded in zip(family, encodings):
        a, fac, t, p = serialize(S, encoded, factor=factor)
        b, _, t2, p2 = serialize(S, encoded, factor=factor)
        assert canonical_bytes(a) == canonical_bytes(b)
        assert t == t2 and program_record(p) == program_record(p2)
        assert fac["component_hashes"] == baseline_components
        assert fac["payload_hash_excluding_this_field"] == baseline_payload_hash
        # All fixed-role targets agree; every formula difference is confined
        # to exactly the three declared target-program row kinds.
        fixed = tuple(t[r["index"]] for r in fac["row_marks"]
                      if r["kind"] not in MUTABLE_TARGET_KINDS)
        if first_fixed_target is None:
            first_fixed_target = fixed
        assert fixed == first_fixed_target
        for bits in itertools.product((0, 1), repeat=2):
            before = canonical_bytes(a)
            verify_program(fac, p, dict(enumerate(bits)))
            # Assignment evaluation cannot mutate the program or manifest.
            assert canonical_bytes(a) == before
            assignment_checks += 1
        manifests.append(a)

    # Actual numerical shape/count and systematic D construction, not a
    # constraint surrogate.  Rebuild every D entry independently from C.
    m, k = exact_count_model(width, depth)
    assert factor["C"]["shape"] == [m, k]
    assert factor["D"]["shape"] == [m, m+k]
    expected_D = [[i, i, 1] for i in range(m)] + [
        [i, m + j, -v] for i, j, v in factor["C"]["entries"]
    ]
    expected_D.sort()
    assert factor["D"]["entries"] == expected_D
    assert len(factor["D"]["entries"]) == m + len(factor["C"]["entries"])
    assert max(abs(v) for _, _, v in factor["C"]["entries"]) <= width

    # Freeze this finite audit so later serializer changes are explicit.
    assert baseline_payload_hash == "355b469b8ec4c5cc37101ac04c56615b1d64279ba4566d1bcf87078c3ab4b241"
    assert manifests[0]["manifest_hash_excluding_this_field"] == "47345ffad289862826c6270f3bb8fedcece061441800c761238503706b0a8d58"
    assert manifests[-1]["manifest_hash_excluding_this_field"] == "6cc4242a0f54d79f9c91bf3fd53a3bc27cb159834d3b032e58ce9dd02e637569"

    summary = {
        "finite_claim_only": True,
        "schema": SCHEMA,
        "S_leaf_capacity": S,
        "formula_count": len(family),
        "assignment_checks_on_actual_C_D": assignment_checks,
        "rejected_noncanonical_or_out_of_domain_inputs": rejected,
        "width": width,
        "gate_stages": depth,
        "C_shape": factor["C"]["shape"],
        "D_shape": factor["D"]["shape"],
        "C_nnz": len(factor["C"]["entries"]),
        "D_nnz": len(factor["D"]["entries"]),
        "factor_payload_hash": baseline_payload_hash,
        "first_manifest_hash": manifests[0]["manifest_hash_excluding_this_field"],
        "last_manifest_hash": manifests[-1]["manifest_hash_excluding_this_field"],
        "polynomial_count_contract": "for S>=4: w<2S,d<=48S^3,k<=1928S^4,m<=2898S^4,m+k<=4826S^4; finite-checked S<=4096",
        "limitation": "finite serializer regression only; no unrestricted integer soundness, class exclusion, generic compiler proof, or GapCVP gap",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("PASS: canonical assignment-independent Serialize(S,F) manifest on the declared finite audit")


if __name__ == "__main__":
    main()
