#!/usr/bin/env python3
"""Finite exact attack on a quadratic-character COPY-cycle brick.

The only Generation-7 proposal allowed by cross-review replaces a common linear
syndrome by the equal-radius words

    q(a,b) = (1, (-1)^a, (-1)^b, 17*(-1)^(a*b)).

This verifier freezes the smallest emitted brick that tests the proposal's
claimed cure rather than another common-fibre proxy.  It contains physical
0/1/DROP selectors, three four-state COPY selectors, both straight and swapped
COPY orientations in a three-COPY cycle, all four transported character rows,
one NAND selector, an output selector, transfer auxiliaries, normalization,
glue, and explicit DROP rows.  Formula/assignment choices occur only through
honest coefficient vectors; the matrix and target are fixed.

Exact search of all 3^12 signed movements on the COPY selectors finds a
support-12 primitive: the same mixed rectangle is applied at all three cycle
vertices.  Every linear and quadratic-character glue row cancels around the
cycle.  For each of the four honest pair states, one sign of this movement
reflects the quadratic character while leaving its magnitude unchanged.
Thus the malformed vector has exactly the legal Euclidean energy even though
the frozen residual scale makes the all-zero DROP vector more than 17 times as
expensive.

This is finite evidence against this hash-locked three-COPY realization only.
It is not a theorem about every quadratic-character compiler or every size.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json

BITS = (0, 1)
SYMS = (0, 1, 2)  # 2 is explicit DROP.
STATES = tuple(product(BITS, repeat=2))
# Straight, swap, swap has trivial monodromy and contains both orientations.
ORIENTATIONS = (0, 1, 1)
QUADRATIC_SCALE = 17
RESIDUAL_SCALE = 100
ADVERSE_FACTOR_SQ = 17
RECTANGLE = (1, -1, -1, 1)  # state order 00, 01, 10, 11.


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
        row = {j: coefficient for j, coefficient in row.items() if coefficient}
        self.row_index[name] = len(self.rows)
        self.rows.append((name, row))


def p_key(node: int, port: int, symbol: int) -> tuple:
    return ("physical", node, port, symbol)


def h_key(node: int, state: tuple[int, int]) -> tuple:
    return ("copy_pair", node, *state)


def n_key(state: tuple[int, int]) -> tuple:
    return ("nand", *state)


def o_key(symbol: int) -> tuple:
    return ("nand_output", symbol)


def t_key(state: tuple[int, int]) -> tuple:
    return ("transfer", *state)


def d_key(node: int) -> tuple:
    return ("drop_aux", node)


def character_column(state: tuple[int, int]) -> tuple[int, int, int, int]:
    a, b = state
    return (1, (-1) ** a, (-1) ** b, QUADRATIC_SCALE * ((-1) ** (a * b)))


Q_COLUMNS = tuple(character_column(state) for state in STATES)
# Character rows, with states as columns.
Q_ROWS = tuple(tuple(Q_COLUMNS[j][i] for j in range(4)) for i in range(4))
SWAP_CHARACTER = (0, 2, 1, 3)


def build_serialization() -> tuple[Serialization, tuple[int, ...]]:
    s = Serialization()

    # Canonical allocation makes the hash independent of row-construction order.
    for node in range(3):
        for port in range(2):
            for symbol in SYMS:
                s.col(p_key(node, port, symbol))
    for node in range(3):
        for state in STATES:
            s.col(h_key(node, state))
    for state in STATES:
        s.col(n_key(state))
    for symbol in SYMS:
        s.col(o_key(symbol))
    for state in STATES:
        s.col(t_key(state))
    for node in range(3):
        s.col(d_key(node))

    target: list[int] = []

    def emit(name: str, terms: list[tuple[int, tuple]], rhs: int = 0) -> None:
        s.add_row(name, terms)
        target.append(rhs)

    # Physical selectors and explicit physical DROP exclusion.
    for node in range(3):
        for port in range(2):
            emit(
                f"physical:{node}:{port}:norm",
                [(1, p_key(node, port, symbol)) for symbol in SYMS],
                1,
            )
            emit(f"physical:{node}:{port}:drop", [(1, p_key(node, port, 2))])

    # Each four-state COPY selector exposes both bit marginals.
    for node in range(3):
        emit(f"copy:{node}:norm", [(1, h_key(node, state)) for state in STATES], 1)
        for port in range(2):
            for bit in BITS:
                emit(
                    f"copy:{node}:marginal:{port}:{bit}",
                    [(1, h_key(node, state)) for state in STATES if state[port] == bit]
                    + [(-1, p_key(node, port, bit))],
                )

    # Three physical COPY edges, including straight and swapped orientations.
    for node, orientation in enumerate(ORIENTATIONS):
        next_node = (node + 1) % 3
        for out_port in range(2):
            in_port = out_port ^ orientation
            for symbol in SYMS:
                emit(
                    f"edge:{node}:physical:{out_port}:{symbol}",
                    [
                        (1, p_key(next_node, out_port, symbol)),
                        (-1, p_key(node, in_port, symbol)),
                    ],
                )

        # Transport every character, including the quadratic character.
        for character in range(4):
            source_character = SWAP_CHARACTER[character] if orientation else character
            emit(
                f"edge:{node}:character:{character}",
                [(Q_ROWS[character][j], h_key(next_node, STATES[j])) for j in range(4)]
                + [(-Q_ROWS[source_character][j], h_key(node, STATES[j])) for j in range(4)],
            )

    # One NAND, attached to node 0, plus output and transfer auxiliaries.
    emit("nand:norm", [(1, n_key(state)) for state in STATES], 1)
    for port in range(2):
        for bit in BITS:
            emit(
                f"nand:input:{port}:{bit}",
                [(1, n_key(state)) for state in STATES if state[port] == bit]
                + [(-1, p_key(0, port, bit))],
            )
    for bit in BITS:
        emit(
            f"nand:output:{bit}",
            [(1, n_key(state)) for state in STATES if 1 - state[0] * state[1] == bit]
            + [(-1, o_key(bit))],
        )
    emit("nand:output:norm", [(1, o_key(symbol)) for symbol in SYMS], 1)
    emit("nand:output:drop", [(1, o_key(2))])
    for state in STATES:
        emit(f"transfer:{state}", [(1, t_key(state)), (-1, n_key(state))])
    emit("transfer:norm", [(1, t_key(state)) for state in STATES], 1)

    # Separate auxiliary DROP coordinates are emitted rather than filtered.
    for node in range(3):
        emit(f"drop_aux:{node}", [(1, d_key(node))])

    assert len(target) == len(s.rows)
    return s, tuple(target)


def matvec(s: Serialization, vector: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    return tuple(
        sum(coefficient * vector[j] for j, coefficient in row.items())
        for _, row in s.rows
    )


def honest_vector(s: Serialization, initial: tuple[int, int]) -> tuple[int, ...]:
    states = [initial]
    for orientation in ORIENTATIONS[:-1]:
        a, b = states[-1]
        states.append((b, a) if orientation else (a, b))
    # The final edge closes the cycle.
    a, b = states[-1]
    closing = (b, a) if ORIENTATIONS[-1] else (a, b)
    assert closing == initial

    vector = [0] * len(s.columns)
    for node, state in enumerate(states):
        for port, bit in enumerate(state):
            vector[s.col_index[p_key(node, port, bit)]] = 1
        vector[s.col_index[h_key(node, state)]] = 1
    vector[s.col_index[n_key(initial)]] = 1
    vector[s.col_index[o_key(1 - initial[0] * initial[1])]] = 1
    vector[s.col_index[t_key(initial)]] = 1
    return tuple(vector)


def copy_mark_energy(s: Serialization, vector: tuple[int, ...] | list[int]) -> int:
    energy = 0
    for node in range(3):
        coefficients = [vector[s.col_index[h_key(node, state)]] for state in STATES]
        image = [sum(row[j] * coefficients[j] for j in range(4)) for row in Q_ROWS]
        energy += sum(value * value for value in image)
    return energy


def anchor_energy(s: Serialization, vector: tuple[int, ...] | list[int]) -> int:
    # COPY selector blocks use the proposed character geometry.  Every other
    # emitted coordinate uses its standard integral Euclidean anchor.
    copy_indices = {s.col_index[h_key(node, state)] for node in range(3) for state in STATES}
    return copy_mark_energy(s, vector) + sum(
        value * value for j, value in enumerate(vector) if j not in copy_indices
    )


def objective(
    s: Serialization, vector: tuple[int, ...] | list[int], target: tuple[int, ...]
) -> int:
    residual = matvec(s, vector)
    return anchor_energy(s, vector) + RESIDUAL_SCALE**2 * sum(
        (value - rhs) ** 2 for value, rhs in zip(residual, target)
    )


def copy_movement(s: Serialization, entries: tuple[int, ...]) -> tuple[int, ...]:
    assert len(entries) == 12
    vector = [0] * len(s.columns)
    k = 0
    for node in range(3):
        for state in STATES:
            vector[s.col_index[h_key(node, state)]] = entries[k]
            k += 1
    return tuple(vector)


def exact_copy_box_kernel(s: Serialization) -> tuple[int, list[tuple[int, ...]], int]:
    """Exhaust the complete {-1,0,1}^12 COPY-selector box exactly."""
    best_support: int | None = None
    minimizers: list[tuple[int, ...]] = []
    searched = 0
    zero = (0,) * len(s.rows)
    for entries in product((-1, 0, 1), repeat=12):
        searched += 1
        if not any(entries):
            continue

        # Cheap exact rejection by each local normalization and two marginals.
        local_ok = True
        for node in range(3):
            block = entries[4 * node : 4 * node + 4]
            if sum(block) != 0:
                local_ok = False
                break
            if block[2] + block[3] != 0 or block[1] + block[3] != 0:
                local_ok = False
                break
        if not local_ok:
            continue

        movement = copy_movement(s, entries)
        if matvec(s, movement) != zero:
            continue
        support = sum(value != 0 for value in entries)
        if best_support is None or support < best_support:
            best_support = support
            minimizers = [entries]
        elif support == best_support:
            minimizers.append(entries)

    assert best_support is not None
    return best_support, minimizers, searched


def specification_hash(s: Serialization, target: tuple[int, ...]) -> str:
    payload = {
        "columns": s.columns,
        "rows": [(name, sorted(row.items())) for name, row in s.rows],
        "target": target,
        "quadratic_scale": QUADRATIC_SCALE,
        "residual_scale": RESIDUAL_SCALE,
        "orientations": ORIENTATIONS,
    }
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main() -> None:
    s, target = build_serialization()
    assert len(s.columns) == 44
    assert len(s.rows) == 74

    # Swapping ports is a marked column permutation and swaps only the two
    # linear-character rows; constant and quadratic characters are fixed.
    swapped_states = tuple((b, a) for a, b in STATES)
    permutation = tuple(STATES.index(state) for state in swapped_states)
    for character in range(4):
        source = SWAP_CHARACTER[character]
        assert tuple(Q_ROWS[character][permutation[j]] for j in range(4)) == Q_ROWS[source]

    best_support, minimizers, searched = exact_copy_box_kernel(s)
    expected_entries = RECTANGLE * 3
    assert searched == 3**12
    assert best_support == 12
    assert set(minimizers) == {expected_entries, tuple(-x for x in expected_entries)}

    movement = copy_movement(s, expected_entries)
    assert matvec(s, movement) == (0,) * len(s.rows)

    # A conformal summand is coordinatewise either zero or the corresponding
    # signed entry of movement.  Exhausting all proper subsets proves that this
    # movement is primitive for the full frozen matrix, not merely for a
    # projected local matrix.
    support_indices = [j for j, value in enumerate(movement) if value]
    assert len(support_indices) == 12
    proper_conformal_kernel_summands = 0
    for mask in range(1, (1 << len(support_indices)) - 1):
        candidate = [0] * len(s.columns)
        for bit, j in enumerate(support_indices):
            if (mask >> bit) & 1:
                candidate[j] = movement[j]
        if matvec(s, candidate) == (0,) * len(s.rows):
            proper_conformal_kernel_summands += 1
    assert proper_conformal_kernel_summands == 0

    legal_energy: int | None = None
    attack_records = []
    for state in STATES:
        legal = honest_vector(s, state)
        assert matvec(s, legal) == target
        energy = objective(s, legal, target)
        legal_energy = energy if legal_energy is None else legal_energy
        assert energy == legal_energy

        candidates = []
        for sign in (-1, 1):
            attack = tuple(value + sign * delta for value, delta in zip(legal, movement))
            assert matvec(s, attack) == target
            candidates.append((objective(s, attack, target), sign, attack))
        attack_energy, sign, attack = min(candidates)
        assert attack_energy == energy
        assert any(value not in (0, 1) for value in attack)
        attack_records.append((state, sign, attack_energy))

    assert legal_energy == 3 * (3 + QUADRATIC_SCALE**2) + 9 == 885

    # Exact physical-only Hamming-one/two audit.  It is not the successful
    # attack, but keeps the older physical-flip gate visible in this brick.
    physical_indices = [
        j for j, key in enumerate(s.columns) if key[0] in ("physical", "nand_output")
    ]
    physical_tests = 0
    for weight in (1, 2):
        for coordinates in combinations(physical_indices, weight):
            for signs in product((-1, 1), repeat=weight):
                candidate = [0] * len(s.columns)
                for j, sign in zip(coordinates, signs):
                    candidate[j] = sign
                assert matvec(s, candidate) != (0,) * len(s.rows)
                physical_tests += 1

    # DROP is deliberately made expensive, so it cannot explain the failure.
    zero = (0,) * len(s.columns)
    drop_energy = objective(s, zero, target)
    assert sum(rhs * rhs for rhs in target) == 12
    assert drop_energy == 120000
    assert drop_energy > ADVERSE_FACTOR_SQ * legal_energy

    digest = specification_hash(s, target)
    expected_digest = "cf9365eecc24a9758b52060bdf0efbfbf40da0037b7cce0b0635a744582ce297"
    assert digest == expected_digest

    print(json.dumps({
        "selected_surviving_proposal": "Pro 2 quadratic-character equal-radius switch encoding",
        "causal_mechanism": (
            "transport the quadratic character along every COPY edge so the old local mixed "
            "rectangle has nonzero character image while all four honest words have one radius"
        ),
        "expected_frontier_move": (
            "a complete marked COPY/NAND brick would evade the Generation-6 common-fibre "
            "exchange and become eligible for the L1 depth-1/2/3 serialization"
        ),
        "falsification_condition": (
            "an exact low-weight malformed kernel movement survives full character transport "
            "with energy at most the legal energy, or DROP remains below 17 times legal energy"
        ),
        "scope": (
            "finite kill of this hash-locked three-COPY realization only; no claim about all "
            "quadratic-character compilers, depths, or instance sizes"
        ),
        "specification_sha256": digest,
        "matrix_shape": [len(s.rows), len(s.columns)],
        "copy_orientations": ["straight" if x == 0 else "swap" for x in ORIENTATIONS],
        "routing_actions_are_marked_permutations": True,
        "all_four_characters_transported": True,
        "honest_states_checked": len(STATES),
        "copy_box_candidates_searched": searched,
        "minimum_nonzero_copy_kernel_support": best_support,
        "minimum_support_copy_kernel_vectors": len(minimizers),
        "proper_conformal_kernel_summands": proper_conformal_kernel_summands,
        "primitive_movement": list(expected_entries),
        "legal_energy": legal_energy,
        "attack_energies": sorted({record[2] for record in attack_records}),
        "attack_to_legal_ratio": 1,
        "attack_signs_by_state": {"".join(map(str, state)): sign for state, sign, _ in attack_records},
        "physical_hamming_one_two_tests": physical_tests,
        "drop_energy": drop_energy,
        "adverse_threshold": ADVERSE_FACTOR_SQ * legal_energy,
        "finding": (
            "the synchronized three-rectangle primitive reflects the transported quadratic "
            "character at every COPY vertex and has exactly the legal energy in all four fibers"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
