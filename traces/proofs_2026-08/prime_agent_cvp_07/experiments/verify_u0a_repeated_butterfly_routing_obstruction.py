#!/usr/bin/env python3
"""Exact finite breaker for the repeated U0a butterfly topology.

Claims are deliberately finite.  Under the generator's default depth
``2*log2(width)+2``, widths 2 and 4 can realize every permutation of
independent input coordinates, but width 8 cannot: the output permutation
(0,1,2,4,3,5,6,7) is absent.  This remains true even when every local gate
may use COPY_A/COPY_B/NAND/ZERO/ONE, rather than only COPY, because a circuit
whose overall map {0,1}^8 -> {0,1}^8 is a coordinate permutation must be
bijective at every stage, and exhaustive local truth-table enumeration shows
that the only bijective two-wire gate layers are identity and swap.

One further stage (depth 9, whose offset is 2) realizes all 8! permutations,
so this is not an all-depth obstruction.  The verifier also records that the
serializer's example target_y helper is witness-dependent on a FREE/COPY
program; that is an audit warning, not an impossibility theorem for a proper
SAT compiler with fixed/unused output lanes.
"""
from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path

HERE = Path(__file__).resolve().parent
SERIALIZER = HERE / "verify_u0a_universal_topology_serializer.py"
spec = importlib.util.spec_from_file_location("u0a_serializer", SERIALIZER)
assert spec is not None and spec.loader is not None
u0a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u0a)


def offsets_from_actual_payload(width: int, depth: int | None = None) -> tuple[int, ...]:
    payload, _, _ = u0a.make_factor(width, gate_stages=depth)
    return tuple(layer["offset"] for layer in payload["topology"])


def local_truth(mode_lo: str, mode_hi: str):
    """Truth table on a paired lane (lo,hi).

    The low lane sees ports (A,B)=(a,b), while the high lane sees (b,a),
    exactly as in make_factor's XOR-offset edge equations.
    """
    return tuple(
        (u0a.gate_value(mode_lo, a, b), u0a.gate_value(mode_hi, b, a))
        for a, b in itertools.product((0, 1), repeat=2)
    )


def audit_local_bijections():
    injective = []
    for ml, mh in itertools.product(u0a.GATE_MODES, repeat=2):
        table = local_truth(ml, mh)
        if len(set(table)) == 4:
            injective.append((ml, mh, table))
    # Exhausts all 5^2 mode pairs.  These are respectively identity and swap.
    assert [(x[0], x[1]) for x in injective] == [
        ("COPY_A", "COPY_A"),
        ("COPY_B", "COPY_B"),
    ]
    assert injective[0][2] == ((0, 0), (0, 1), (1, 0), (1, 1))
    assert injective[1][2] == ((0, 0), (1, 0), (0, 1), (1, 1))
    return injective


def advance_switch_layer(states: set[tuple[int, ...]], offset: int):
    """Exact image under all bijective local mode choices at one actual layer."""
    width = len(next(iter(states)))
    edges = tuple((i, i ^ offset) for i in range(width) if i < (i ^ offset))
    out = set()
    for state in states:
        for swap_bits in itertools.product((0, 1), repeat=len(edges)):
            q = list(state)
            for do_swap, (a, b) in zip(swap_bits, edges):
                if do_swap:
                    q[a], q[b] = q[b], q[a]
            out.add(tuple(q))
    return out


def reachable_permutations(width: int, depth: int | None = None):
    states = {tuple(range(width))}
    counts = []
    offsets = offsets_from_actual_payload(width, depth)
    for off in offsets:
        states = advance_switch_layer(states, off)
        counts.append(len(states))
        assert all(len(set(p)) == width for p in states)
    return offsets, counts, states


def assignment_values(width, depth, source_bits):
    vals = {(0, i): source_bits[i] for i in range(width)}
    offsets = offsets_from_actual_payload(width, depth)
    for s, off in enumerate(offsets, start=1):
        for i in range(width):
            # The audited example program is COPY_A everywhere.
            vals[(s, i)] = u0a.gate_value(
                "COPY_A", vals[(s - 1, i)], vals[(s - 1, i ^ off)]
            )
    return vals


def audit_witness_dependent_example_target():
    width = 8
    payload, _, _ = u0a.make_factor(width)
    depth = payload["gate_stages"]
    source_modes = ["FREE"] * width
    gate_modes = {
        (s, i): "COPY_A"
        for s in range(1, depth + 1)
        for i in range(width)
    }
    x0 = [0] * width
    x1 = [0] * width
    x1[3] = 1
    vals0 = assignment_values(width, depth, x0)
    vals1 = assignment_values(width, depth, x1)
    outs0 = [vals0[(depth, i)] for i in range(width)]
    outs1 = [vals1[(depth, i)] for i in range(width)]
    assert outs0 == x0 and outs1 == x1
    t0 = u0a.target_y(payload, source_modes, gate_modes, outs0)
    t1 = u0a.target_y(payload, source_modes, gate_modes, outs1)
    changed = [
        payload["row_marks"][i]
        for i, (a, b) in enumerate(zip(t0, t1))
        if a != b
    ]
    assert [(r["kind"], r["lane"]) for r in changed] == [
        ("OUTPUT_INTERFACE", 3)
    ]
    # Both are perfectly honest base-energy witnesses, but for two targets.
    for vals, target in ((vals0, t0), (vals1, t1)):
        z = u0a.honest_vector(payload, source_modes, gate_modes, vals)
        Cz = u0a.matvec(payload["C"]["shape"], payload["C"]["entries"], z)
        assert sum((a - b) ** 2 for a, b in zip(Cz, target)) == width * (depth + 1)
    return changed[0]["id"]


def main():
    injective = audit_local_bijections()

    # Exact minimal-width audit for powers of two supported by make_factor.
    results = {}
    for width in (2, 4, 8):
        offsets, counts, states = reachable_permutations(width)
        total = 1
        for j in range(2, width + 1):
            total *= j
        results[width] = (offsets, counts, len(states), total)
        if width < 8:
            assert len(states) == total

    offsets8, counts8, states8 = reachable_permutations(8)
    forbidden = (0, 1, 2, 4, 3, 5, 6, 7)
    assert forbidden not in states8
    assert len(states8) == 18688 < 40320
    # Lexicographically first absent coordinate permutation, independently
    # exhaustively selected from all 8! candidates.
    first_missing = next(
        p for p in itertools.permutations(range(8)) if p not in states8
    )
    assert first_missing == forbidden

    # An extra actual scheduled stage has offset 2 and repairs permutation routing.
    offsets9, counts9, states9 = reachable_permutations(8, depth=9)
    assert offsets9 == (1, 1, 2, 2, 4, 4, 1, 1, 2)
    assert len(states9) == 40320

    changed_output = audit_witness_dependent_example_target()

    print("local mode pairs exhausted:", len(u0a.GATE_MODES) ** 2)
    print("bijective pairs:", [(a, b) for a, b, _ in injective])
    for width in (2, 4, 8):
        offs, counts, got, total = results[width]
        print(f"width={width} offsets={offs} counts={counts} final={got}/{total}")
    print("width=8 first missing permutation:", forbidden)
    print("width=8 depth=9 counts:", counts9)
    print("witness-dependent example target row:", changed_output)
    print("PASS: exact finite routing obstruction and target audit")


if __name__ == "__main__":
    main()
