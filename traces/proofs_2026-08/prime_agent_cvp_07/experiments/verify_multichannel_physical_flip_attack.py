#!/usr/bin/env python3
"""Finite exact low-weight attack on r=1..4 direct-sum product transfers.

The Generation-5 cross-review overlap retains only the multi-channel product-tag
mutation on the hash-locked 18-variable NAND/COPY skeleton.  This verifier adds
four explicit Z[u]/(u^2-3) product channels, one prefix at a time.  The first two
channels have rank three on the mod-17 transportation seam, so they remove the
old pair-only dependency rather than merely replaying it.

The adversarial search also varies the ten physical NAND/COPY selectors while
holding the pair table fixed.  Such a move is invisible to every appended tag
row in each tested serialization.  For all legal cells, both COPY orientations,
and r=1,2,3,4, exact Hamming-one search finds a binary malformed vector of
squared distance 20, while legal energy is E=18 and 17E=306.

This is finite evidence about the four serialized, unscaled 18-variable
factors.  It does not refute unspecified extra/scaled pair-dependent rows, Q1,
or any all-size claim.
"""

from __future__ import annotations

import hashlib
import json

from verify_product_tag_full_lift_attack import (
    NAND_SIZE, COPY_SIZE, PAIR_SIZE, VARIABLES, emitted_matrix,
    legal_vector, matrix_vector, x_index,
)

P = 17
NONSQUARE = 3
CHANNELS = (
    # Exact lexicographically first rank-three pair synthesized independently
    # by verify_multichannel_product_shell.py from {0,1,u} labels.
    (((0, 0), (0, 0), (0, 0), (1, 0)), ((0, 0), (1, 0))),
    (((0, 0), (1, 0), (0, 1), (0, 0)), ((0, 0), (1, 0))),
    # Two further fixed channels stress the authorized r<=4 extension.
    (((1, 1), (2, 1), (3, 1), (4, 1)), ((1, 0), (2, 1))),
    (((1, 2), (2, 3), (3, 5), (5, 8)), ((1, 1), (2, 3))),
)
OLD_PAIR_WITNESS = (-1, 1, 1, -1, 1, -1, -1, 1)


def qmul(left, right):
    return (
        left[0] * right[0] + NONSQUARE * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def channel_table(channel, orientation):
    left, right = channel
    table = tuple(tuple(qmul(left[i], right[j]) for j in range(2)) for i in range(4))
    if orientation == "forward":
        return table
    return tuple(tuple(tuple(-v for v in table[i][1 - j]) for j in range(2)) for i in range(4))


def build_matrix(r, orientation):
    # Keep all 20 non-transfer rows of the prior hash-locked matrix and replace
    # its single two-component tag by r explicit two-component product tags.
    rows = list(emitted_matrix(orientation)[:-2])
    for channel in CHANNELS[:r]:
        table = channel_table(channel, orientation)
        for component in range(2):
            row = [0] * VARIABLES
            for i in range(4):
                for j in range(2):
                    row[x_index(i, j)] = table[i][j][component]
            rows.append(tuple(row))
    return tuple(rows)


def rank_mod_p(matrix, p):
    work = [[entry % p for entry in row] for row in matrix]
    rank = 0
    columns = len(work[0]) if work else 0
    for column in range(columns):
        pivot = next((i for i in range(rank, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inv = pow(work[rank][column], -1, p)
        work[rank] = [(v * inv) % p for v in work[rank]]
        for i in range(len(work)):
            if i != rank and work[i][column]:
                scale = work[i][column]
                work[i] = [(a - scale * b) % p for a, b in zip(work[i], work[rank])]
        rank += 1
    return rank


# The three-dimensional 4x2 zero-margin seam is parameterized by row
# coefficients c_1,c_2,c_3 (with c_0=-sum c_i).  Verify that the first two
# channels already give rank three modulo 17.
seam_map = []
for channel in CHANNELS[:2]:
    table = channel_table(channel, "forward")
    for component in range(2):
        seam_map.append(tuple(
            (table[i][0][component] - table[i][1][component]
             - table[0][0][component] + table[0][1][component]) % P
            for i in range(1, 4)
        ))
assert rank_mod_p(seam_map, P) == 3

records = []
serialization = {}
for r in range(1, 5):
    for orientation in ("forward", "reverse"):
        matrix = build_matrix(r, orientation)
        serialization[f"r{r}_{orientation}"] = matrix
        # Confirm that r>=2 actually defeats the old pair-only witness.
        old_move = (0,) * (NAND_SIZE + COPY_SIZE) + OLD_PAIR_WITNESS
        old_residual = matrix_vector(matrix, old_move)
        if r >= 2:
            assert any(value % P for value in old_residual[-2 * r:])

        for state in range(4):
            for copy_state in range(2):
                legal = legal_vector(orientation, state, copy_state)
                rhs = matrix_vector(matrix, legal)
                factor = tuple(
                    tuple(2 * int(i == j) for j in range(VARIABLES))
                    for i in range(VARIABLES)
                ) + matrix
                target = (1,) * VARIABLES + rhs
                legal_image = matrix_vector(factor, legal)
                legal_energy = sum((a - b) ** 2 for a, b in zip(legal_image, target))
                assert legal_energy == 18

                candidates = []
                # Exact low-weight search: flip one of ten physical selectors,
                # keeping all eight pair selectors (and hence every tag) fixed.
                for coordinate in range(NAND_SIZE + COPY_SIZE):
                    attack = list(legal)
                    attack[coordinate] = 1 - attack[coordinate]
                    attack = tuple(attack)
                    image = matrix_vector(factor, attack)
                    energy = sum((a - b) ** 2 for a, b in zip(image, target))
                    transfer_residual = tuple(
                        image[VARIABLES + len(matrix) - 2 * r + k]
                        - target[VARIABLES + len(matrix) - 2 * r + k]
                        for k in range(2 * r)
                    )
                    assert transfer_residual == (0,) * (2 * r)
                    candidates.append((energy, coordinate, attack))
                energy, coordinate, attack = min(candidates)
                assert energy == 20 and energy < 17 * legal_energy
                nonanchor_residual = tuple(
                    a - b for a, b in zip(matrix_vector(matrix, attack), rhs)
                )
                assert sum(v * v for v in nonanchor_residual) == 2
                assert any(nonanchor_residual[:-2 * r])
                records.append({
                    "r": r,
                    "orientation": orientation,
                    "cell": [state, copy_state],
                    "flipped_physical_coordinate": coordinate,
                    "attack_energy": energy,
                    "nontransfer_residual_squared": 2,
                    "transfer_residual": list((0,) * (2 * r)),
                })

SPECIFICATION_SHA256 = hashlib.sha256(json.dumps(
    {"channels": CHANNELS, "matrices": serialization},
    sort_keys=True, separators=(",", ":"),
).encode("ascii")).hexdigest()
EXPECTED_SPECIFICATION_SHA256 = "98b128c26ac87c4db6df5c6c2a174ce0dbe8c04d98e26ad7476f182b649ccd04"


def main():
    assert SPECIFICATION_SHA256 == EXPECTED_SPECIFICATION_SHA256
    print(json.dumps({
        "selected_surviving_proposal": "Fable 2 / Pro 1 multi-channel product transfer",
        "causal_mechanism": (
            "direct-sum product symbols add enough residue dimensions to remove the "
            "old pair-only dependency; soundness still requires unrestricted malformed "
            "vectors, including physical-selector deviations, to be costly or detected"
        ),
        "expected_frontier_move": (
            "the first two channels clear the old three-dimensional transportation seam, "
            "then exact low-weight search tests whether pair-only transfer detects the full factor"
        ),
        "falsification_condition": "a malformed sub-17E vector has zero residual in every appended transfer row",
        "specification_sha256": SPECIFICATION_SHA256,
        "channels_tested": [1, 2, 3, 4],
        "first_two_channel_transportation_rank_mod_17": rank_mod_p(seam_map, P),
        "factors_checked": 8,
        "legal_fibers_checked": len(records),
        "hamming_one_candidates_checked": len(records) * (NAND_SIZE + COPY_SIZE),
        "legal_energy_E": 18,
        "threshold_17E": 306,
        "minimum_attack_energy": min(record["attack_energy"] for record in records),
        "all_attacks_have_zero_vector_transfer": all(not any(record["transfer_residual"]) for record in records),
        "representative_attack": next(record for record in records if record["r"] == 2),
        "finding": (
            "in all 64 tested cell/orientation/channel-prefix fibers, a one-bit physical "
            "selector flip has exact vector-transfer residual zero and energy 20<306"
        ),
        "scope": (
            "finite kill of the four serialized unscaled 18-variable direct-sum factors; "
            "unspecified extra or scaled rows, the absent maximal-order tile, Q1-Q5, and "
            "all-size behavior remain open"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
