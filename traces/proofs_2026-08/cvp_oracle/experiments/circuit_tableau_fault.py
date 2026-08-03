#!/usr/bin/env python3
"""Circuit-tableau NCP/CVP encoding and exact support-three gate fault.

The circuit computes the conjunction of all eight clauses on three variables,
then ANDs its output with a constant one.  Local truth-table columns communicate
only through affine wire values.  A three-column OR superposition changes one
false clause output to true at additive support/squared-norm cost two.
"""
from __future__ import annotations

from itertools import combinations, product
import numpy as np


def graph(kind: str):
    if kind == 'SRC':
        return [(0,), (1,)]
    if kind == 'NOT':
        return [(0, 1), (1, 0)]
    if kind == 'OR':
        return [(a, b, a | b) for a, b in product((0, 1), repeat=2)]
    if kind == 'AND':
        return [(a, b, a & b) for a, b in product((0, 1), repeat=2)]
    raise ValueError(kind)


def all_eight_circuit():
    """Return ordered blocks, wires (producer, consumer, port), constants, output."""
    blocks: list[tuple[str, str]] = []
    wires: list[tuple[str, str, int]] = []
    constants: list[tuple[str, int, int]] = []

    def add(name, kind):
        blocks.append((name, kind))
        return name

    sources = [add(f'x{i}', 'SRC') for i in range(3)]
    neg = [add(f'n{i}', 'NOT') for i in range(3)]
    for i in range(3):
        wires.append((sources[i], neg[i], 0))

    clause_out = []
    for u in range(8):
        bits = [(u >> i) & 1 for i in range(3)]
        lits = [sources[i] if bits[i] == 0 else neg[i] for i in range(3)]
        a = add(f'or{u}a', 'OR')
        z = add(f'or{u}b', 'OR')
        wires += [(lits[0], a, 0), (lits[1], a, 1), (a, z, 0), (lits[2], z, 1)]
        clause_out.append(z)

    level = clause_out
    gate_id = 0
    while len(level) > 1:
        nxt = []
        for j in range(0, len(level), 2):
            g = add(f'and{gate_id}', 'AND')
            gate_id += 1
            wires += [(level[j], g, 0), (level[j + 1], g, 1)]
            nxt.append(g)
        level = nxt
    final = add('final', 'AND')
    wires.append((level[0], final, 0))
    constants.append((final, 1, 1))
    return blocks, wires, constants, final


def build():
    blocks, wires, constants, output = all_eight_circuit()
    kinds = dict(blocks)
    meta = []
    index = {}
    for name, kind in blocks:
        for tau in graph(kind):
            index[name, tau] = len(meta)
            meta.append((name, tau))

    rows: list[list[int]] = []
    target: list[int] = []

    def add(entries: list[tuple[int, int]], rhs: int):
        row = [0] * len(meta)
        for j, a in entries:
            row[j] += a
        rows.append(row)
        target.append(rhs)

    # Odd/exact block coverage.
    for name, kind in blocks:
        add([(index[name, tau], 1) for tau in graph(kind)], 1)

    def outbit(kind, tau):
        return tau[0] if kind == 'SRC' else tau[-1]

    # One affine equality row per driven input wire.
    for producer, consumer, port in wires:
        entries = []
        for tau in graph(kinds[producer]):
            entries.append((index[producer, tau], outbit(kinds[producer], tau)))
        for sigma in graph(kinds[consumer]):
            entries.append((index[consumer, sigma], -sigma[port]))
        add(entries, 0)

    for consumer, port, bit in constants:
        add([(index[consumer, tau], tau[port]) for tau in graph(kinds[consumer])], bit)
    add([(index[output, tau], tau[-1]) for tau in graph(kinds[output])], 1)

    A = np.asarray(rows, dtype=object)
    b = np.asarray(target, dtype=object)
    return A, b, meta, blocks, wires, constants, output


def honest_transcript(bits, forced=None):
    """One legal column per block, optionally force one block's interface tuple."""
    A, b, meta, blocks, wires, constants, output = build()
    kinds = dict(blocks)
    values = {f'x{i}': int(bits[i]) for i in range(3)}
    chosen = {}
    incoming = {(c, p): q for q, c, p in wires}
    const = {(c, p): bit for c, p, bit in constants}
    for name, kind in blocks:
        if kind == 'SRC':
            tau = (values[name],)
        else:
            arity = len(graph(kind)[0]) - 1
            ins = tuple(values[incoming[name, p]] if (name, p) in incoming else const[name, p]
                        for p in range(arity))
            tau = ins + ((1 - values[name]) if False else (ins[0] if kind == 'NOT' else
                           (ins[0] | ins[1] if kind == 'OR' else ins[0] & ins[1])),)
        chosen[name] = tau
        values[name] = tau[-1] if kind != 'SRC' else tau[0]
    return chosen, values[output]


def explicit_witness():
    """The x=000 transcript with the second OR of C_000 faulted."""
    A, b, meta, blocks, wires, constants, output = build()
    idx = {m: i for i, m in enumerate(meta)}
    chosen, accepted = honest_transcript((0, 0, 0))
    assert accepted == 0 and chosen['or0b'] == (0, 0, 0)

    # Re-evaluate downstream after forcing the false clause output to one.
    kinds = dict(blocks)
    values = {f'x{i}': 0 for i in range(3)}
    incoming = {(c, p): q for q, c, p in wires}
    const = {(c, p): bit for c, p, bit in constants}
    ordinary = {}
    for name, kind in blocks:
        if name == 'or0b':
            values[name] = 1
            continue
        if kind == 'SRC':
            tau = (values[name],)
        else:
            arity = len(graph(kind)[0]) - 1
            ins = tuple(values[incoming[name, p]] if (name, p) in incoming else const[name, p]
                        for p in range(arity))
            out = 1 - ins[0] if kind == 'NOT' else (ins[0] | ins[1] if kind == 'OR' else ins[0] & ins[1])
            tau = ins + (out,)
        ordinary[name] = tau
        values[name] = tau[0] if kind == 'SRC' else tau[-1]
    assert values[output] == 1

    e = np.zeros(len(meta), dtype=object)
    lam = np.zeros(len(meta), dtype=object)
    for name, tau in ordinary.items():
        e[idx[name, tau]] = 1
        lam[idx[name, tau]] = 1
    # (1,0,0,1) = 011 + 101 - 111, with coverage prepended implicitly.
    for tau, coeff in [((0, 1, 1), 1), ((1, 0, 1), 1), ((1, 1, 1), -1)]:
        e[idx['or0b', tau]] = 1
        lam[idx['or0b', tau]] = coeff
    return A, b, e, lam, meta, blocks


def enumerate_one_faults():
    """Exact search over every binary witness of weight G+2.

    Coverage forces one selected column per block except one 4-column block,
    where exactly three columns are selected.  Wire equations then determine
    whether the induced parity interfaces form an accepting transcript.
    """
    A, b, meta, blocks, wires, constants, output = build()
    kinds = dict(blocks)
    incoming = {(c, p): q for q, c, p in wires}
    const = {(c, p): bit for c, p, bit in constants}
    accepts = []
    for bits in product((0, 1), repeat=3):
        for exceptional, kind in blocks:
            table = graph(kind)
            if len(table) < 3:
                continue
            for subset in combinations(table, 3):
                iface = tuple(sum(t[j] for t in subset) & 1 for j in range(len(subset[0])))
                values = {f'x{i}': bits[i] for i in range(3)}
                okay = True
                for name, k in blocks:
                    if k == 'SRC':
                        tau = (values[name],)
                    else:
                        arity = len(graph(k)[0]) - 1
                        ins = tuple(values[incoming[name, p]] if (name, p) in incoming else const[name, p]
                                    for p in range(arity))
                        if name == exceptional:
                            if iface[:-1] != ins:
                                okay = False
                                break
                            tau = iface
                        else:
                            out = 1 - ins[0] if k == 'NOT' else (ins[0] | ins[1] if k == 'OR' else ins[0] & ins[1])
                            tau = ins + (out,)
                    values[name] = tau[0] if k == 'SRC' else tau[-1]
                if okay and values[output] == 1:
                    accepts.append((bits, exceptional, subset, iface))
    return accepts


def run():
    A, b, e, lam, meta, blocks = explicit_witness()
    accepts = enumerate_one_faults()
    result = {
        'blocks_G': len(blocks), 'columns_N': A.shape[1], 'rows_r': A.shape[0],
        'binary_weight': int(sum(e)), 'integer_squared_norm': int(sum(x * x for x in lam)),
        'binary_residual_zero': bool(np.all((A @ e - b) % 2 == 0)),
        'integer_residual_zero': bool(np.all(A @ lam == b)),
        'accepting_one_fault_transcripts': len(accepts),
        'explicit_fault': ('or0b', ((0, 1, 1), (1, 0, 1), (1, 1, 1))),
    }
    print(result)
    return result


if __name__ == '__main__':
    run()
