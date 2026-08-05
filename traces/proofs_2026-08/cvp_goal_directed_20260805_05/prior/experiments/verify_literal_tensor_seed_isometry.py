#!/usr/bin/env python3
"""Generation-30 exact k=2 audit of the surviving literal-tensor proposal.

The frozen seeds are the two serialized Generation-28 depth-one right tiles:
NO uses endpoint forbiddens ((4,5),(6,7)); the matched control replaces 7 by
0.  For each seed C=[2I;5A], y=[1;5b].  The proposed tensor is literally
C tensor C with target y tensor y and an unrestricted 16-by-16 integral
coefficient matrix Z.

Swapping assignment coordinates 0 and 7 in both bags is an exact integral
isometry from the alleged NO seed to the control.  Its tensor square pairs
every unrestricted coefficient matrix, so R_1=R_2=1.  Exact low-l1 search
and named DROP/G13/G19/malformed attacks are included.  This is a finite
falsification of this particular seed pair, not a theorem about all tensors.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import hashlib
import json
from pathlib import Path

import verify_frozen_minplus_pair_tile as gen28

RANK = 16
SEED_AMBIENT = 30
TENSOR_RANK = RANK * RANK
TENSOR_AMBIENT = SEED_AMBIENT * SEED_AMBIENT
RESIDUAL_SCALE = 5
NO_TILE = gen28.TILE_B_UNSAT
YES_TILE = gen28.TILE_B_CONTROL
ASSIGNMENT_PERMUTATION = (7, 1, 2, 3, 4, 5, 6, 0)
COEFFICIENT_PERMUTATION = tuple(
    8 * bag + ASSIGNMENT_PERMUTATION[index]
    for bag in range(2) for index in range(8)
)
ATTACK_SHELL_RADIUS2 = 31285
COEFFICIENT_ABS_BOUND = 60
MANIFEST_PATH = Path(__file__).with_name("gen30_literal_tensor_seed_manifest.json")


def sparse(row):
    return [[index, int(value)] for index, value in enumerate(row) if value]


def build_seed(tile):
    rows = []
    target = []
    row_names = []
    for index in range(RANK):
        row = [0] * RANK
        row[index] = 2
        rows.append(tuple(row))
        target.append(1)
        row_names.append(f"anchor_{index}")
    for bag, forbidden in enumerate(tile):
        offset = 8 * bag
        row = [0] * RANK
        for index in range(8):
            row[offset + index] = RESIDUAL_SCALE
        rows.append(tuple(row))
        target.append(RESIDUAL_SCALE)
        row_names.append(f"normalization_{bag}")
        for forbidden_index in forbidden:
            row = [0] * RANK
            row[offset + forbidden_index] = RESIDUAL_SCALE
            rows.append(tuple(row))
            target.append(0)
            row_names.append(f"legality_{bag}_{forbidden_index}")
    for index in range(8):
        row = [0] * RANK
        row[index] = RESIDUAL_SCALE
        row[8 + index] = -RESIDUAL_SCALE
        rows.append(tuple(row))
        target.append(0)
        row_names.append(f"full_port_glue_{index}")
    assert len(rows) == SEED_AMBIENT
    return tuple(rows), tuple(target), tuple(row_names)


def gram_and_linear(rows, target):
    gram = tuple(tuple(
        sum(row[i] * row[j] for row in rows)
        for j in range(RANK)
    ) for i in range(RANK))
    linear = tuple(sum(row[i] * value for row, value in zip(rows, target)) for i in range(RANK))
    target_norm2 = sum(value * value for value in target)
    return gram, linear, target_norm2


def matmul(left, right):
    rows = len(left)
    middle = len(right)
    columns = len(right[0])
    return [[
        sum(left[i][k] * right[k][j] for k in range(middle))
        for j in range(columns)
    ] for i in range(rows)]


def tensor_objective(seed_data, matrix):
    gram, linear, target_norm2 = seed_data
    gz = matmul(gram, matrix)
    gzg = matmul(gz, gram)
    quadratic = sum(gzg[i][j] * matrix[i][j] for i in range(RANK) for j in range(RANK))
    target_pairing = sum(
        linear[i] * matrix[i][j] * linear[j]
        for i in range(RANK) for j in range(RANK)
    )
    return quadratic - 2 * target_pairing + target_norm2 * target_norm2


def outer(left, right):
    return [[left[i] * right[j] for j in range(RANK)] for i in range(RANK)]


def add_matrices(left, right):
    return [[left[i][j] + right[i][j] for j in range(RANK)] for i in range(RANK)]


def port_vector(port):
    return tuple(port) + tuple(port)


def one_hot(index):
    port = [0] * 8
    port[index] = 1
    return port_vector(tuple(port))


def permute_vector_no_to_yes(vector):
    result = [0] * RANK
    for old_index, new_index in enumerate(COEFFICIENT_PERMUTATION):
        result[new_index] = vector[old_index]
    return tuple(result)


def permute_matrix_no_to_yes(matrix):
    result = [[0] * RANK for _ in range(RANK)]
    for old_i, new_i in enumerate(COEFFICIENT_PERMUTATION):
        for old_j, new_j in enumerate(COEFFICIENT_PERMUTATION):
            result[new_i][new_j] = matrix[old_i][old_j]
    return result


def derive_ambient_permutation(no_rows, no_target, yes_rows, yes_target):
    # If z_yes[P(i)]=z_no[i], row r of C_yes P has entries
    # C_yes[r,P(i)].  Match every transformed row and target to C_no.
    available = {}
    for index, (row, target) in enumerate(zip(no_rows, no_target)):
        available.setdefault((row, target), []).append(index)
    permutation = []
    for yes_row, target in zip(yes_rows, yes_target):
        transformed = tuple(yes_row[COEFFICIENT_PERMUTATION[i]] for i in range(RANK))
        key = (transformed, target)
        assert key in available and available[key]
        permutation.append(available[key].pop(0))
    assert not any(available.values())
    return tuple(permutation)


def product_hash(rows, target):
    payload_rows = []
    payload_target = []
    for left_index, left in enumerate(rows):
        left_terms = sparse(left)
        for right_index, right in enumerate(rows):
            right_terms = sparse(right)
            terms = []
            for i, left_value in left_terms:
                for j, right_value in right_terms:
                    terms.append([RANK * i + j, left_value * right_value])
            payload_rows.append(terms)
            payload_target.append(target[left_index] * target[right_index])
    payload = {"rows": payload_rows, "target": payload_target}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def low_l1_search(seed_data):
    """Exhaust every integer 16x16 matrix of l1 norm at most two."""
    gram, linear, target_norm2 = seed_data
    constant = target_norm2 * target_norm2
    best = (constant, ())
    tested = 1

    def diagonal(position):
        i, j = divmod(position, RANK)
        return gram[i][i] * gram[j][j]

    def gradient(position):
        i, j = divmod(position, RANK)
        return linear[i] * linear[j]

    def interaction(first, second):
        i, j = divmod(first, RANK)
        k, ell = divmod(second, RANK)
        return gram[i][k] * gram[j][ell]

    for position in range(TENSOR_RANK):
        for coefficient in (-2, -1, 1, 2):
            tested += 1
            value = (
                constant + coefficient * coefficient * diagonal(position)
                - 2 * coefficient * gradient(position)
            )
            if value < best[0]:
                best = (value, ((position, coefficient),))
    for first, second in combinations(range(TENSOR_RANK), 2):
        for first_coefficient in (-1, 1):
            for second_coefficient in (-1, 1):
                tested += 1
                value = (
                    constant + diagonal(first) + diagonal(second)
                    + 2 * first_coefficient * second_coefficient * interaction(first, second)
                    - 2 * (
                        first_coefficient * gradient(first)
                        + second_coefficient * gradient(second)
                    )
                )
                if value < best[0]:
                    best = (value, (
                        (first, first_coefficient),
                        (second, second_coefficient),
                    ))
    assert tested == 1 + 4 * TENSOR_RANK + 4 * (TENSOR_RANK * (TENSOR_RANK - 1) // 2)
    return {"matrix_count": tested, "minimum_squared": best[0], "witness": [list(item) for item in best[1]]}


def attack_audit(seed_data, allowed_assignments):
    zero = [[0] * RANK for _ in range(RANK)]
    legal_vectors = tuple(one_hot(index) for index in allowed_assignments)
    legal_costs = tuple(tensor_objective(seed_data, outer(vector, vector)) for vector in legal_vectors)

    g13_records = []
    for port in gen28.G13_PORTS:
        vector = port_vector(port)
        g13_records.append((tensor_objective(seed_data, outer(vector, vector)), port))

    g19_records = []
    for port in gen28.G19_SEEDS:
        vector = port_vector(port)
        g19_records.append((tensor_objective(seed_data, outer(vector, vector)), port))

    malformed_records = []
    for left, right in combinations(legal_vectors, 2):
        matrix = add_matrices(outer(left, left), outer(right, right))
        malformed_records.append(tensor_objective(seed_data, matrix))

    best_g13 = min(g13_records)
    best_g19 = min(g19_records)
    return {
        "rank_one_legal_squared": min(legal_costs),
        "DROP_zero_matrix_squared": tensor_objective(seed_data, zero),
        "G13_diagonal_count": len(g13_records),
        "G13_best_diagonal_squared": best_g13[0],
        "G13_best_port": list(best_g13[1]),
        "G19_diagonal_count": len(g19_records),
        "G19_best_diagonal_squared": best_g19[0],
        "G19_best_port": list(best_g19[1]),
        "MALFORMED_rank_two_count": len(malformed_records),
        "MALFORMED_rank_two_best_squared": min(malformed_records),
    }


def seed_record(name, tile, rows, target, row_names, seed_data, allowed):
    return {
        "name": name,
        "tile_forbidden_assignments": [list(pair) for pair in tile],
        "rank": RANK,
        "ambient_dimension": SEED_AMBIENT,
        "factor_rows": [sparse(row) for row in rows],
        "target": list(target),
        "row_names": list(row_names),
        "factor_rule": "C=[2I;5A]",
        "target_rule": "y=[1;5b]",
        "gram_eigenvalue_lower_bound": 4,
        "target_squared_norm": seed_data[2],
        "allowed_honest_assignments": list(allowed),
        "exact_one_copy_minimum_squared": 16,
        "tensor_factor_rule": "C tensor C",
        "tensor_target_rule": "y tensor y",
        "tensor_rank": TENSOR_RANK,
        "tensor_ambient_dimension": TENSOR_AMBIENT,
        "tensor_factor_target_sha256": product_hash(rows, target),
        "attack_audit": attack_audit(seed_data, allowed),
        "low_l1_search": low_l1_search(seed_data),
    }


def build_manifest():
    no_rows, no_target, no_names = build_seed(NO_TILE)
    yes_rows, yes_target, yes_names = build_seed(YES_TILE)
    no_data = gram_and_linear(no_rows, no_target)
    yes_data = gram_and_linear(yes_rows, yes_target)
    ambient_permutation = derive_ambient_permutation(no_rows, no_target, yes_rows, yes_target)

    no_allowed = tuple(index for index in range(8) if index not in {4, 5, 6, 7})
    yes_allowed = tuple(index for index in range(8) if index not in {0, 4, 5, 6})
    assert tuple(sorted(ASSIGNMENT_PERMUTATION[index] for index in no_allowed)) == yes_allowed

    no_record = seed_record(
        "generation28_depth1_alleged_NO", NO_TILE,
        no_rows, no_target, no_names, no_data, no_allowed,
    )
    yes_record = seed_record(
        "generation28_depth1_matched_control", YES_TILE,
        yes_rows, yes_target, yes_names, yes_data, yes_allowed,
    )
    assert no_record["attack_audit"] == yes_record["attack_audit"]
    assert no_record["low_l1_search"] == yes_record["low_l1_search"]

    return {
        "schema": "gen30-literal-tensor-g28-depth1-v1",
        "finite_claim_only": True,
        "selected_proposal": "Fable proposal 3: literal tensoring of a deep-hole seed",
        "mechanism": "literal Kronecker products should increase the NO/YES squared-distance ratio",
        "expected_move": "R_2>R_1 for R_k=D_NO(k)/D_YES(k)",
        "falsification_condition": "R_2<=R_1 or an unrestricted entangled shortcut",
        "coefficient_domain": "all integer 16-by-16 matrices",
        "external_filters": [],
        "coefficient_permutation_NO_to_YES": list(COEFFICIENT_PERMUTATION),
        "ambient_permutation_YES_rows_to_NO_rows": list(ambient_permutation),
        "isometry_identity_k1": "C_YES P = Q C_NO and y_YES = Q y_NO",
        "isometry_identity_k2": "(C_YES tensor C_YES)(P tensor P)=(Q tensor Q)(C_NO tensor C_NO)",
        "complete_unrestricted_shell_pairing": (
            "Z_YES=(P tensor P)Z_NO bijects every integer matrix in both directions "
            "and preserves squared objective exactly"
        ),
        "attack_shell_squared_radius": ATTACK_SHELL_RADIUS2,
        "attack_shell_reason": "first radius containing a diagonal representative of DROP, G13, G19, and rank-two MALFORMED classes",
        "coefficient_bound": {
            "product_singular_value_lower_bound": 4,
            "product_target_norm": 66,
            "derivation": "if |Z_ij|>=61 then ||(C tensor C)Z-y tensor y|| >= 4*61-66=178",
            "strict_exclusion_check": "178^2=31684>31285",
            "inclusive_interval": [-COEFFICIENT_ABS_BOUND, COEFFICIENT_ABS_BOUND],
        },
        "seeds": [no_record, yes_record],
        "ratio_audit": {
            "D_NO_1": 16,
            "D_YES_1": 16,
            "R_1": "1",
            "D_NO_2_equals_D_YES_2": True,
            "D_2_exact_common_lower_bound": 256,
            "D_2_common_upper_bound": 1888,
            "R_2": "1",
            "R_2_strictly_greater_than_R_1": False,
        },
    }


def verify_isometry(manifest):
    no_rows, no_target, _ = build_seed(NO_TILE)
    yes_rows, yes_target, _ = build_seed(YES_TILE)
    ambient = tuple(manifest["ambient_permutation_YES_rows_to_NO_rows"])
    for yes_row_index, no_row_index in enumerate(ambient):
        transformed = tuple(
            yes_rows[yes_row_index][COEFFICIENT_PERMUTATION[index]]
            for index in range(RANK)
        )
        assert transformed == no_rows[no_row_index]
        assert yes_target[yes_row_index] == no_target[no_row_index]

    # Exhaust basis and signed two-basis matrices as an independent k=2 check
    # of the tensor permutation formula; linearity then covers every Z.
    no_data = gram_and_linear(no_rows, no_target)
    yes_data = gram_and_linear(yes_rows, yes_target)
    probes = []
    for i in range(RANK):
        for j in range(RANK):
            matrix = [[0] * RANK for _ in range(RANK)]
            matrix[i][j] = 1
            probes.append(matrix)
    for i in range(RANK):
        matrix = [[0] * RANK for _ in range(RANK)]
        matrix[i][i] = -1
        matrix[i][(i + 1) % RANK] = 1
        probes.append(matrix)
    for matrix in probes:
        assert tensor_objective(no_data, matrix) == tensor_objective(
            yes_data, permute_matrix_no_to_yes(matrix)
        )
    return len(probes)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args()

    expected = build_manifest()
    if args.write_manifest:
        MANIFEST_PATH.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
        print(MANIFEST_PATH)
        return

    manifest = json.loads(MANIFEST_PATH.read_text())
    assert manifest == expected
    probe_count = verify_isometry(manifest)

    no_record, yes_record = manifest["seeds"]
    assert no_record["exact_one_copy_minimum_squared"] == 16
    assert yes_record["exact_one_copy_minimum_squared"] == 16
    assert no_record["low_l1_search"] == {
        "matrix_count": 131585,
        "minimum_squared": 4356,
        "witness": [],
    }
    assert no_record["attack_audit"] == {
        "rank_one_legal_squared": 1888,
        "DROP_zero_matrix_squared": 4356,
        "G13_diagonal_count": 8,
        "G13_best_diagonal_squared": 31285,
        "G13_best_port": [-1, 1, 1, -1, 1, -1, 0, 1],
        "G19_diagonal_count": 560,
        "G19_best_diagonal_squared": 11749,
        "G19_best_port": [-1, -1, 1, 1, 0, 0, 0, 1],
        "MALFORMED_rank_two_count": 6,
        "MALFORMED_rank_two_best_squared": 4420,
    }
    assert manifest["ratio_audit"] == {
        "D_NO_1": 16,
        "D_YES_1": 16,
        "R_1": "1",
        "D_NO_2_equals_D_YES_2": True,
        "D_2_exact_common_lower_bound": 256,
        "D_2_common_upper_bound": 1888,
        "R_2": "1",
        "R_2_strictly_greater_than_R_1": False,
    }

    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[1])),
        "seed_rank": RANK,
        "seed_ambient_dimension": SEED_AMBIENT,
        "tensor_rank": TENSOR_RANK,
        "tensor_ambient_dimension": TENSOR_AMBIENT,
        "attack_shell_squared_radius": ATTACK_SHELL_RADIUS2,
        "coefficient_interval": [-COEFFICIENT_ABS_BOUND, COEFFICIENT_ABS_BOUND],
        "k2_isometry_probes_checked": probe_count,
        "low_l1_exact_search": no_record["low_l1_search"],
        "attack_audit": no_record["attack_audit"],
        "ratio_audit": manifest["ratio_audit"],
        "finding": "the alleged NO seed is permutation-isometric to the control, hence R1=R2=1 for unrestricted coefficients",
        "scope": "finite kill of this serialized seed pair; no claim about arbitrary tensor lattices",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
