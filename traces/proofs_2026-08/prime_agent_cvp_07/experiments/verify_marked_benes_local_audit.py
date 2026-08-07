#!/usr/bin/env python3
"""Exact finite audit of a width-four marked Beneš routing serialization.

This is a falsifier for the cross-review-surviving oblivious-routing proposal,
not an asymptotic claim.  It freezes one natural full, fixed-matrix encoding:
physical selectors include 0/1/DROP, switch transition selectors are the pair
coordinates, NAND selectors are the four legal words, and transfer selectors
are explicit copies of the NAND selectors.  Formula-dependent switch choices
occur only in the target.

The script checks all 24 width-four permutations and all 16 input words.  It
also exhausts the complete {-1,0,1} kernel of one marked 2x2 switch and embeds
every minimum primitive into every switch.  Finally it checks the all-zero
DROP vector against the frozen residual scale 5.  Finding an attack is an
expected, verified finite outcome, so success exits zero.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product

SYMS = (0, 1, 2)  # 2 is explicit DROP
STAGE_PAIRS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 1), (2, 3)))
NAND_WORDS = ((0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0))
RESIDUAL_SCALE_SQ = 25
ADVERSE_FACTOR_SQ = 17


class Serialization:
    def __init__(self) -> None:
        self.columns: list[tuple] = []
        self.col_index: dict[tuple, int] = {}
        self.rows: list[tuple[str, dict[int, int]]] = []
        self.row_index: dict[str, int] = {}

    def col(self, key: tuple) -> int:
        if key not in self.col_index:
            self.col_index[key] = len(self.columns)
            self.columns.append(key)
        return self.col_index[key]

    def add_row(self, name: str, terms: list[tuple[int, tuple]]) -> None:
        assert name not in self.row_index
        row: dict[int, int] = {}
        for coefficient, key in terms:
            j = self.col(key)
            row[j] = row.get(j, 0) + coefficient
        row = {j: a for j, a in row.items() if a}
        self.row_index[name] = len(self.rows)
        self.rows.append((name, row))


def p_key(layer: int, wire: int, symbol: int) -> tuple:
    return ("physical", layer, wire, symbol)


def q_key(stage: int, switch: int, i: int, j: int, symbol: int) -> tuple:
    return ("pair", stage, switch, i, j, symbol)


def n_key(gate: int, word: tuple[int, int, int]) -> tuple:
    return ("nand", gate, *word)


def o_key(gate: int, symbol: int) -> tuple:
    return ("physical_out", gate, symbol)


def t_key(gate: int, word: tuple[int, int, int]) -> tuple:
    return ("transfer", gate, *word)


def build_serialization() -> Serialization:
    s = Serialization()

    # Allocate in a canonical category order before rows are emitted.
    for layer in range(4):
        for wire in range(4):
            for symbol in SYMS:
                s.col(p_key(layer, wire, symbol))
    for stage in range(3):
        for switch in range(2):
            for i in range(2):
                for j in range(2):
                    for symbol in SYMS:
                        s.col(q_key(stage, switch, i, j, symbol))
    for gate in range(2):
        for word in NAND_WORDS:
            s.col(n_key(gate, word))
        for symbol in SYMS:
            s.col(o_key(gate, symbol))
        for word in NAND_WORDS:
            s.col(t_key(gate, word))

    # Full switch incidence and all four edge-color rows.  The matrix is fixed;
    # only the right-hand sides of edge_total rows encode straight/cross.
    for stage, pairs in enumerate(STAGE_PAIRS):
        for switch, wires in enumerate(pairs):
            for i, wire in enumerate(wires):
                for symbol in SYMS:
                    s.add_row(
                        f"sw:{stage}:{switch}:in:{i}:{symbol}",
                        [(1, q_key(stage, switch, i, j, symbol)) for j in range(2)]
                        + [(-1, p_key(stage, wire, symbol))],
                    )
            for j, wire in enumerate(wires):
                for symbol in SYMS:
                    s.add_row(
                        f"sw:{stage}:{switch}:out:{j}:{symbol}",
                        [(1, q_key(stage, switch, i, j, symbol)) for i in range(2)]
                        + [(-1, p_key(stage + 1, wire, symbol))],
                    )
            for i in range(2):
                for j in range(2):
                    s.add_row(
                        f"sw:{stage}:{switch}:edge_total:{i}:{j}",
                        [(1, q_key(stage, switch, i, j, symbol)) for symbol in SYMS],
                    )

    # Source normalization and explicit source DROP exclusion.
    for wire in range(4):
        s.add_row(
            f"source:norm:{wire}",
            [(1, p_key(0, wire, symbol)) for symbol in SYMS],
        )
        s.add_row(f"source:drop:{wire}", [(1, p_key(0, wire, 2))])

    # One fixed layer of two NAND gates.  NAND selectors are also the local
    # pair selectors; transfer auxiliaries are retained, rather than filtered.
    for gate, wires in enumerate(((0, 1), (2, 3))):
        s.add_row(f"nand:{gate}:norm", [(1, n_key(gate, w)) for w in NAND_WORDS])
        for port, wire in enumerate(wires):
            for bit in (0, 1):
                s.add_row(
                    f"nand:{gate}:input:{port}:{bit}",
                    [(1, n_key(gate, w)) for w in NAND_WORDS if w[port] == bit]
                    + [(-1, p_key(3, wire, bit))],
                )
            s.add_row(f"nand:{gate}:input:{port}:drop", [(1, p_key(3, wire, 2))])
        for bit in (0, 1):
            s.add_row(
                f"nand:{gate}:output:{bit}",
                [(1, n_key(gate, w)) for w in NAND_WORDS if w[2] == bit]
                + [(-1, o_key(gate, bit))],
            )
        s.add_row(f"nand:{gate}:output:drop", [(1, o_key(gate, 2))])
        s.add_row(
            f"nand:{gate}:output:norm",
            [(1, o_key(gate, symbol)) for symbol in SYMS],
        )
        for word in NAND_WORDS:
            s.add_row(
                f"nand:{gate}:transfer:{''.join(map(str, word))}",
                [(1, t_key(gate, word)), (-1, n_key(gate, word))],
            )
        s.add_row(
            f"nand:{gate}:transfer:norm",
            [(1, t_key(gate, word)) for word in NAND_WORDS],
        )
    return s


def route(settings: tuple[int, ...], inputs: tuple[int, ...]):
    assert len(settings) == 6
    current_tokens = list(range(4))
    current_bits = list(inputs)
    boundaries = [tuple(current_bits)]
    transitions = []
    k = 0
    for stage, pairs in enumerate(STAGE_PAIRS):
        next_tokens = [None] * 4
        next_bits = [None] * 4
        for switch, wires in enumerate(pairs):
            setting = settings[k]
            k += 1
            local = []
            for i, in_wire in enumerate(wires):
                j = i ^ setting
                out_wire = wires[j]
                next_tokens[out_wire] = current_tokens[in_wire]
                next_bits[out_wire] = current_bits[in_wire]
                local.append((i, j, current_bits[in_wire]))
            transitions.append((stage, switch, tuple(local)))
        assert all(x is not None for x in next_tokens + next_bits)
        current_tokens = next_tokens
        current_bits = next_bits
        boundaries.append(tuple(current_bits))
    return tuple(current_tokens), tuple(boundaries), tuple(transitions)


def canonical_settings() -> dict[tuple[int, ...], tuple[int, ...]]:
    result: dict[tuple[int, ...], tuple[int, ...]] = {}
    for settings in product((0, 1), repeat=6):
        permutation, _, _ = route(settings, (0, 0, 0, 0))
        result.setdefault(permutation, settings)
    assert len(result) == 24
    return dict(sorted(result.items()))


def target(s: Serialization, settings: tuple[int, ...]) -> list[int]:
    b = [0] * len(s.rows)
    k = 0
    for stage in range(3):
        for switch in range(2):
            setting = settings[k]
            k += 1
            for i in range(2):
                for j in range(2):
                    name = f"sw:{stage}:{switch}:edge_total:{i}:{j}"
                    b[s.row_index[name]] = int(j == (i ^ setting))
    for wire in range(4):
        b[s.row_index[f"source:norm:{wire}"]] = 1
    for gate in range(2):
        b[s.row_index[f"nand:{gate}:norm"]] = 1
        b[s.row_index[f"nand:{gate}:output:norm"]] = 1
        b[s.row_index[f"nand:{gate}:transfer:norm"]] = 1
    return b


def honest_vector(
    s: Serialization, settings: tuple[int, ...], inputs: tuple[int, ...]
) -> list[int]:
    _, boundaries, transitions = route(settings, inputs)
    z = [0] * len(s.columns)
    for layer, bits in enumerate(boundaries):
        for wire, bit in enumerate(bits):
            z[s.col_index[p_key(layer, wire, bit)]] = 1
    for stage, switch, local in transitions:
        for i, j, bit in local:
            z[s.col_index[q_key(stage, switch, i, j, bit)]] = 1
    final = boundaries[-1]
    for gate, wires in enumerate(((0, 1), (2, 3))):
        a, b = final[wires[0]], final[wires[1]]
        word = (a, b, 1 - a * b)
        assert word in NAND_WORDS
        z[s.col_index[n_key(gate, word)]] = 1
        z[s.col_index[o_key(gate, word[2])]] = 1
        z[s.col_index[t_key(gate, word)]] = 1
    return z


def matvec(s: Serialization, z: list[int] | tuple[int, ...]) -> list[int]:
    return [sum(a * z[j] for j, a in row.items()) for _, row in s.rows]


def anchor_energy(z: list[int] | tuple[int, ...]) -> int:
    return sum((2 * x - 1) ** 2 for x in z)


def objective(s: Serialization, z: list[int], b: list[int]) -> int:
    az = matvec(s, z)
    return anchor_energy(z) + RESIDUAL_SCALE_SQ * sum(
        (x - y) ** 2 for x, y in zip(az, b)
    )


def local_switch_kernel() -> list[tuple[int, ...]]:
    # Coordinate order (i,j,symbol), then exact row/column symbol marginals and
    # exact edge totals.  Exhausting 3^12 vectors is the complete signed box.
    keys = tuple((i, j, symbol) for i in range(2) for j in range(2) for symbol in SYMS)
    feasible: list[tuple[int, ...]] = []
    best = None
    for v in product((-1, 0, 1), repeat=len(keys)):
        if not any(v):
            continue
        value = dict(zip(keys, v))
        if any(sum(value[i, j, symbol] for j in range(2)) for i in range(2) for symbol in SYMS):
            continue
        if any(sum(value[i, j, symbol] for i in range(2)) for j in range(2) for symbol in SYMS):
            continue
        if any(sum(value[i, j, symbol] for symbol in SYMS) for i in range(2) for j in range(2)):
            continue
        sq = sum(x * x for x in v)
        if best is None or sq < best:
            best = sq
            feasible = [v]
        elif sq == best:
            feasible.append(v)
    assert best == 8
    assert len(feasible) == 6  # two signs for each unordered pair of symbols

    # Every minimizer is a conformally primitive box move: no nonempty proper
    # subset of its signed support is itself in the kernel.
    for v in feasible:
        support = [i for i, x in enumerate(v) if x]
        assert len(support) == 8
        for mask in range(1, (1 << len(support)) - 1):
            w = [0] * len(keys)
            for bit, coordinate in enumerate(support):
                if (mask >> bit) & 1:
                    w[coordinate] = v[coordinate]
            value = dict(zip(keys, w))
            in_kernel = (
                not any(sum(value[i, j, symbol] for j in range(2)) for i in range(2) for symbol in SYMS)
                and not any(sum(value[i, j, symbol] for i in range(2)) for j in range(2) for symbol in SYMS)
                and not any(sum(value[i, j, symbol] for symbol in SYMS) for i in range(2) for j in range(2))
            )
            assert not in_kernel
    return feasible


def embed_local(
    s: Serialization, stage: int, switch: int, v: tuple[int, ...]
) -> list[int]:
    delta = [0] * len(s.columns)
    keys = tuple((i, j, symbol) for i in range(2) for j in range(2) for symbol in SYMS)
    for value, (i, j, symbol) in zip(v, keys):
        delta[s.col_index[q_key(stage, switch, i, j, symbol)]] = value
    return delta


def canonical_hash(s: Serialization, targets: list[list[int]]) -> str:
    h = sha256()
    for key in s.columns:
        h.update((repr(key) + "\n").encode())
    for name, row in s.rows:
        h.update((name + ":" + repr(sorted(row.items())) + "\n").encode())
    for b in targets:
        h.update((repr(b) + "\n").encode())
    return h.hexdigest()


def main() -> None:
    s = build_serialization()
    permutations = canonical_settings()
    assert len(s.columns) == 142
    assert len(s.rows) == 136

    targets = []
    legal_vectors: dict[tuple[tuple[int, ...], tuple[int, ...]], list[int]] = {}
    for permutation, settings in permutations.items():
        b = target(s, settings)
        targets.append(b)
        for inputs in product((0, 1), repeat=4):
            z = honest_vector(s, settings, inputs)
            assert all(x in (0, 1) for x in z)
            assert matvec(s, z) == b
            assert anchor_energy(z) == len(s.columns)
            assert objective(s, z, b) == len(s.columns)
            legal_vectors[(permutation, inputs)] = z

    # The marked matrix is literally identical for all switch settings.  Thus
    # the permitted marked column map is P=I; formula dependence is target-only.
    assert len({tuple(sorted(row.items())) for _, row in s.rows}) == len(s.rows)

    primitives = local_switch_kernel()
    zero_row = [0] * len(s.rows)
    minimum_malformed_energy = None
    audited_embeddings = 0
    quotient_detections = 0
    for permutation, settings in permutations.items():
        b = target(s, settings)
        for inputs in product((0, 1), repeat=4):
            z = legal_vectors[(permutation, inputs)]
            setting_index = 0
            for stage in range(3):
                for switch in range(2):
                    setting = settings[setting_index]
                    setting_index += 1
                    for v in primitives:
                        delta = embed_local(s, stage, switch, v)
                        assert matvec(s, delta) == zero_row
                        candidate = [x + d for x, d in zip(z, delta)]
                        assert matvec(s, candidate) == b
                        energy = objective(s, candidate, b)
                        minimum_malformed_energy = (
                            energy if minimum_malformed_energy is None else min(minimum_malformed_energy, energy)
                        )
                        audited_embeddings += 1

                        # For this fixed color, every honest vector is zero on
                        # forbidden edges.  Each rectangle has a nonzero such
                        # coordinate, so a full-coordinate quotient detects it
                        # and it is not in that color's honest affine span.
                        found = False
                        keys = tuple((i, j, symbol) for i in range(2) for j in range(2) for symbol in SYMS)
                        for value, (i, j, symbol) in zip(v, keys):
                            if value and j != (i ^ setting):
                                found = True
                                break
                        assert found
                        quotient_detections += 1
    assert minimum_malformed_energy == len(s.columns) + 16
    assert audited_embeddings == 24 * 16 * 6 * len(primitives)
    assert quotient_detections == audited_embeddings

    # Exact physical-only Hamming-one/two audit.  No +/-1 change of at most two
    # physical selector coordinates, with pair/NAND/transfer coordinates held
    # fixed, lies in the integer kernel.
    physical = [
        j for j, key in enumerate(s.columns) if key[0] in ("physical", "physical_out")
    ]
    physical_tests = 0
    for size in (1, 2):
        for coordinates in combinations(physical, size):
            for signs in product((-1, 1), repeat=size):
                delta = [0] * len(s.columns)
                for j, sign in zip(coordinates, signs):
                    delta[j] = sign
                assert matvec(s, delta) != zero_row
                physical_tests += 1

    # The natural residual scale fails the explicit DROP gate.  This is the
    # earliest preregistered falsifier, so no depth-2/3 Lawrence inference is
    # made from the local routing pass.
    representative_settings = next(iter(permutations.values()))
    representative_target = target(s, representative_settings)
    drop = [0] * len(s.columns)
    drop_energy = objective(s, drop, representative_target)
    target_weight = sum(x * x for x in representative_target)
    assert target_weight == 22
    assert drop_energy == len(s.columns) + RESIDUAL_SCALE_SQ * target_weight == 692
    assert drop_energy < ADVERSE_FACTOR_SQ * len(s.columns)

    digest = canonical_hash(s, targets)
    assert digest == "8ceacac2408540f7b46c1f74b8b753c6d6a25489129c814b58d063a8580dd20b"

    print("marked Beneš local audit: finite verified outcome")
    print(f"matrix={len(s.rows)}x{len(s.columns)} permutations=24 legal_vectors={len(legal_vectors)}")
    print(f"sha256={digest}")
    print(f"local_box=3^12 minimum_kernel_sq=8 primitive_minimizers={len(primitives)}")
    print(f"embedded_primitive_audits={audited_embeddings} minimum_malformed_energy={minimum_malformed_energy}")
    print(f"physical_only_hamming_1_2_tests={physical_tests}")
    print(f"legal_energy={len(s.columns)} drop_energy={drop_energy} adverse_threshold={ADVERSE_FACTOR_SQ * len(s.columns)}")
    print("finding: target-only marked routing passes locally, but this frozen scale is killed by explicit DROP")


if __name__ == "__main__":
    main()
