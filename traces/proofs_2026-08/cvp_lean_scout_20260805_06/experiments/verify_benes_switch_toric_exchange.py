#!/usr/bin/env python3
"""Finite exact toric-exchange attack on a marked width-four Beneš serialization.

The sole cross-review survivor is the target-only Beneš-routing proposal for L1.
This verifier freezes the smallest standard pair-linearized realization: a fixed
three-stage width-four Beneš matrix with physical wire/switch columns, complete
2x2 (switch-state,input-bit) tables at both ports of every switch,
normalization/marginal/routing rows, shared wire columns as glue, and an explicit
DROP column fixed to zero.  No semantic column is mixed or relabelled.

Exact {-1,0,1} search on one switch finds a support-eight primitive movement:
the same 2x2 rectangle is added to both port tables.  It preserves every row
because each rectangle has zero marginals and the two product changes cancel in
the COPY/SWAP output equations.  More seriously, the movement is exactly

    h(0,0,0) - h(0,1,1) - h(1,0,0) + h(1,1,1),

an integer combination of four honest switch states whose coefficients sum to
zero.  It is therefore in the honest affine-difference lattice, where an L2/L3
detector that vanishes on honest differences cannot separate it.

The movement embeds unchanged for all 24 routed permutations and all 16 input
words.  With the explicit half-integral anchor normalization used here, its
best malformed representative has squared energy 92 or 108 versus legal energy
76, and has exactly zero non-anchor residual.

This is finite evidence killing only this frozen pair-linearized switch brick.
Extra rows that do not vanish on honest affine differences, or a different
full brick, are unspecified and are not refuted.  No all-size claim is made.
"""

from __future__ import annotations

from itertools import product
import hashlib
import json

WIDTH = 4
TOPOLOGY = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 1), (2, 3)),
)


def q_name(stage: int, slot: int, port: int, setting: int, bit: int) -> str:
    return f"q_{stage}_{slot}_{port}_{setting}_{bit}"


VARIABLE_NAMES = (
    tuple(f"w_{layer}_{wire}" for layer in range(4) for wire in range(WIDTH))
    + tuple(f"switch_{stage}_{slot}" for stage in range(3) for slot in range(2))
    + tuple(
        q_name(stage, slot, port, setting, bit)
        for stage in range(3)
        for slot in range(2)
        for port in range(2)
        for setting in range(2)
        for bit in range(2)
    )
    + tuple(f"drop_{stage}_{slot}" for stage in range(3) for slot in range(2))
)
INDEX = {name: index for index, name in enumerate(VARIABLE_NAMES)}
VARIABLES = len(VARIABLE_NAMES)
assert VARIABLES == 76


def sparse_row(entries: dict[str, int]) -> tuple[int, ...]:
    row = [0] * VARIABLES
    for name, coefficient in entries.items():
        row[INDEX[name]] += coefficient
    return tuple(row)


def build_matrix() -> tuple[tuple[int, ...], ...]:
    rows = []
    for stage, pairs in enumerate(TOPOLOGY):
        for slot, wires in enumerate(pairs):
            switch = f"switch_{stage}_{slot}"
            products = []
            for port, wire in enumerate(wires):
                table = tuple(
                    q_name(stage, slot, port, setting, bit)
                    for setting in range(2)
                    for bit in range(2)
                )
                rows.append(sparse_row({name: 1 for name in table}))
                rows.append(sparse_row({
                    q_name(stage, slot, port, 1, 0): 1,
                    q_name(stage, slot, port, 1, 1): 1,
                    switch: -1,
                }))
                rows.append(sparse_row({
                    q_name(stage, slot, port, 0, 1): 1,
                    q_name(stage, slot, port, 1, 1): 1,
                    f"w_{stage}_{wire}": -1,
                }))
                products.append(q_name(stage, slot, port, 1, 1))

            left, right = wires
            # y_left = x_left + s*x_right - s*x_left
            rows.append(sparse_row({
                f"w_{stage + 1}_{left}": 1,
                f"w_{stage}_{left}": -1,
                products[1]: -1,
                products[0]: 1,
            }))
            # y_right = x_right + s*x_left - s*x_right
            rows.append(sparse_row({
                f"w_{stage + 1}_{right}": 1,
                f"w_{stage}_{right}": -1,
                products[0]: -1,
                products[1]: 1,
            }))
            rows.append(sparse_row({f"drop_{stage}_{slot}": 1}))
    assert len(rows) == 54
    return tuple(rows)


MATRIX = build_matrix()


def matrix_vector(matrix, vector):
    return tuple(
        sum(coefficient * value for coefficient, value in zip(row, vector))
        for row in matrix
    )


def simulate(settings: tuple[int, ...], input_word: tuple[int, ...]):
    layers = [tuple(input_word)]
    for stage, pairs in enumerate(TOPOLOGY):
        output = list(layers[-1])
        for slot, (left, right) in enumerate(pairs):
            if settings[2 * stage + slot]:
                output[left], output[right] = output[right], output[left]
        layers.append(tuple(output))
    return tuple(layers)


def permutation_of(settings: tuple[int, ...]) -> tuple[int, ...]:
    # Route distinct labels, so the final layer is the induced permutation.
    layers = [tuple(range(WIDTH))]
    for stage, pairs in enumerate(TOPOLOGY):
        output = list(layers[-1])
        for slot, (left, right) in enumerate(pairs):
            if settings[2 * stage + slot]:
                output[left], output[right] = output[right], output[left]
        layers.append(tuple(output))
    return layers[-1]


# Select the lexicographically first switch setting for each permutation.
FIRST_SETTINGS = {}
for candidate in product((0, 1), repeat=6):
    FIRST_SETTINGS.setdefault(permutation_of(candidate), candidate)
assert len(FIRST_SETTINGS) == 24
ROUTES = tuple(sorted(FIRST_SETTINGS.items()))


def honest_vector(settings: tuple[int, ...], input_word: tuple[int, ...]):
    layers = simulate(settings, input_word)
    vector = [0] * VARIABLES
    for layer in range(4):
        for wire in range(WIDTH):
            vector[INDEX[f"w_{layer}_{wire}"]] = layers[layer][wire]
    for stage, pairs in enumerate(TOPOLOGY):
        for slot, wires in enumerate(pairs):
            setting = settings[2 * stage + slot]
            vector[INDEX[f"switch_{stage}_{slot}"]] = setting
            for port, wire in enumerate(wires):
                bit = layers[stage][wire]
                vector[INDEX[q_name(stage, slot, port, setting, bit)]] = 1
            # DROP remains zero.
    vector = tuple(vector)
    residual = matrix_vector(MATRIX, vector)
    assert residual == tuple(
        1 if row_index % 9 in (0, 3) else 0
        for row_index in range(len(MATRIX))
    )
    return vector


def local_honest(setting: int, left_bit: int, right_bit: int):
    """One-switch state in the coordinates of stage 0, slot 0."""
    settings = (setting, 0, 0, 0, 0, 0)
    word = (left_bit, right_bit, 0, 0)
    return honest_vector(settings, word)


def local_pair_move(entries: tuple[int, ...]):
    vector = [0] * VARIABLES
    names = tuple(
        q_name(0, 0, port, setting, bit)
        for port in range(2)
        for setting in range(2)
        for bit in range(2)
    )
    for name, value in zip(names, entries):
        vector[INDEX[name]] = value
    return tuple(vector)


# Exact low-weight search in the eight marked pair coordinates.
LOCAL_KERNEL = []
for entries in product((-1, 0, 1), repeat=8):
    if not any(entries):
        continue
    movement = local_pair_move(entries)
    if not any(matrix_vector(MATRIX, movement)):
        LOCAL_KERNEL.append((sum(value != 0 for value in entries), entries, movement))
assert LOCAL_KERNEL
MIN_SUPPORT = min(record[0] for record in LOCAL_KERNEL)
MINIMAL = tuple(record for record in LOCAL_KERNEL if record[0] == MIN_SUPPORT)
assert MIN_SUPPORT == 8
assert len(MINIMAL) == 2

RECTANGLE = (1, -1, -1, 1)
EXPECTED_ENTRIES = RECTANGLE + RECTANGLE
MOVE = local_pair_move(EXPECTED_ENTRIES)
assert any(record[2] == MOVE for record in MINIMAL)
assert matrix_vector(MATRIX, MOVE) == (0,) * len(MATRIX)

# A conformal summand of MOVE must vanish outside these eight coordinates and
# have each local entry in {0, MOVE_i}.  Exact enumeration leaves only MOVE
# itself, certifying Graver primitiveness for this frozen matrix.
CONFORMAL_COMPONENTS = tuple(
    record for record in LOCAL_KERNEL
    if all(value in (0, bound) for value, bound in zip(record[1], EXPECTED_ENTRIES))
)
assert len(CONFORMAL_COMPONENTS) == 1
assert CONFORMAL_COMPONENTS[0][2] == MOVE

# Exact honest-affine collision.  Coefficients sum to zero, and every physical,
# glue, DROP, and nonlocal pair coordinate cancels.
AFFINE_COMBINATION = tuple(
    a - b - c + d
    for a, b, c, d in zip(
        local_honest(0, 0, 0),
        local_honest(0, 1, 1),
        local_honest(1, 0, 0),
        local_honest(1, 1, 1),
    )
)
assert AFFINE_COMBINATION == MOVE


def squared_energy(vector, rhs):
    # Kannan-style half-integral anchor normalization: factor [2I; A], target
    # [1; rhs].  Every binary honest vector has one unit per anchor coordinate.
    anchor = sum((2 * value - 1) ** 2 for value in vector)
    residual = matrix_vector(MATRIX, vector)
    constraint = sum((value - target) ** 2 for value, target in zip(residual, rhs))
    return anchor + constraint


records = []
for permutation, settings in ROUTES:
    for input_word in product((0, 1), repeat=WIDTH):
        legal = honest_vector(settings, input_word)
        rhs = matrix_vector(MATRIX, legal)
        legal_energy = squared_energy(legal, rhs)
        assert legal_energy == VARIABLES
        candidates = []
        for sign in (-1, 1):
            attack = tuple(value + sign * delta for value, delta in zip(legal, MOVE))
            assert matrix_vector(MATRIX, attack) == rhs
            candidates.append((squared_energy(attack, rhs), sign, attack))
        attack_energy, sign, attack = min(candidates)
        assert attack_energy in (92, 108)
        assert any(value not in (0, 1) for value in attack)
        records.append({
            "permutation": permutation,
            "settings": settings,
            "input": input_word,
            "attack_sign": sign,
            "attack_energy": attack_energy,
        })

SERIALIZATION = {
    "variable_names": VARIABLE_NAMES,
    "matrix": MATRIX,
    "routes": ROUTES,
}
SPECIFICATION_SHA256 = hashlib.sha256(json.dumps(
    SERIALIZATION, sort_keys=True, separators=(",", ":")
).encode("ascii")).hexdigest()
# Filled with the frozen value after constructing this exact serialization.
EXPECTED_SPECIFICATION_SHA256 = "d72ee30bf0081a0390906d5d0ddb91dbc9bd1c783636fa610a97df500e10bfcf"


def main():
    assert SPECIFICATION_SHA256 == EXPECTED_SPECIFICATION_SHA256
    representative = records[0]
    print(json.dumps({
        "selected_surviving_proposal": "Fable 1 / Pro 1 marked oblivious Benes routing",
        "causal_mechanism": (
            "a fixed COPY/SWAP topology is pair-linearized so formula-specific routing "
            "is placed in switch targets while the marked compiler matrix stays fixed"
        ),
        "expected_frontier_move": (
            "the frozen width-four matrix would be an L1 candidate only if its low-weight "
            "kernel had no malformed primitive inside the honest affine-difference lattice"
        ),
        "falsification_condition": (
            "a nonzero short marked pair movement preserves every emitted row and is an "
            "integer affine combination of honest switch states"
        ),
        "specification_sha256": SPECIFICATION_SHA256,
        "matrix_shape": [len(MATRIX), VARIABLES],
        "permutations_checked": len(ROUTES),
        "input_words_per_permutation": 16,
        "fibers_checked": len(records),
        "local_candidates_searched": 3 ** 8 - 1,
        "minimum_nonzero_local_kernel_support": MIN_SUPPORT,
        "minimum_support_kernel_vectors": len(MINIMAL),
        "proper_nonzero_conformal_summands": len(CONFORMAL_COMPONENTS) - 1,
        "primitive_pair_move": list(EXPECTED_ENTRIES),
        "primitive_move_squared_weight": sum(value * value for value in EXPECTED_ENTRIES),
        "honest_affine_identity": "h000 - h011 - h100 + h111",
        "honest_affine_coefficients_sum": 0,
        "legal_energy": VARIABLES,
        "attack_energy_values": sorted(set(record["attack_energy"] for record in records)),
        "maximum_attack_to_legal_ratio": max(record["attack_energy"] for record in records) / VARIABLES,
        "all_nonanchor_residuals_zero": True,
        "representative_attack": {
            key: list(value) if isinstance(value, tuple) else value
            for key, value in representative.items()
        },
        "finding": (
            "all 384 tested route/input fibers admit the same support-eight primitive "
            "zero-residual toric exchange; it lies in the honest affine-difference lattice"
        ),
        "scope": (
            "finite kill of this frozen marked pair-linearized width-four switch brick only; "
            "unspecified extra rows or a different full brick are not refuted, and no "
            "all-size statement is claimed"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
