#!/usr/bin/env python3
"""Exact bounded test of Pro proposal 6 (affine/Graver isolation).

Core: one falsified OR clause at global marginals (0,0,0). The seven
satisfying patterns are selector columns. A harmful signed selector y has
sum(y)=1 and P^T y=0 although no legal one-hot satisfying selector has
those marginals. Moves are measured from every legal one-hot selector.

Candidate matrices have 12 columns (7 selectors, 5 auxiliaries), 1--3
rows, and exactly one 1 in each column. Thus all r^12 degree-one
left-regular 0/1 matrices are covered. Row permutations are retained.
For each matrix, dynamic programming exactly minimizes auxiliary squared
norm for each row-sum signature while selectors are enumerated in
[-3,3]^7. The auxiliary coefficient box is also [-3,3]^5.

This finite experiment deliberately allows an isolating outcome. It does
not claim anything about more rows, larger boxes, higher column degree,
or an asymptotic matrix family.
"""

from itertools import product
import hashlib
import json

BOUND = 3
AUX_COLUMNS = 5
MAX_ROWS = 3
PATTERNS = tuple(p for p in product((0, 1), repeat=3) if p != (0, 0, 0))
N = len(PATTERNS)


def harmful_selector_moves():
    moves = []
    harmful_count = 0
    for y in product(range(-BOUND, BOUND + 1), repeat=N):
        if sum(y) != 1:
            continue
        if any(sum(coef * p[j] for coef, p in zip(y, PATTERNS)) for j in range(3)):
            continue
        harmful_count += 1
        for legal_index in range(N):
            move = tuple(coef - (i == legal_index) for i, coef in enumerate(y))
            norm2 = sum(value * value for value in move)
            if norm2:
                moves.append((norm2, move, y, legal_index))
    return harmful_count, tuple(sorted(moves))


def signature(move, assignment, row_count):
    result = [0] * row_count
    for column, value in enumerate(move):
        result[assignment[column]] += value
    return tuple(result)


def compressed_selector_maps(row_count, moves):
    """For each selector-column placement, keep the best move/signature."""
    maps = []
    for assignment in product(range(row_count), repeat=N):
        table = {}
        for norm2, move, y, legal_index in moves:
            sig = signature(move, assignment, row_count)
            candidate = (norm2, move, y, legal_index)
            if sig not in table or candidate < table[sig]:
                table[sig] = candidate
        maps.append((assignment, table))
    return maps


def compressed_aux_maps(row_count):
    """For each auxiliary placement, exact DP over [-3,3]^5 moves."""
    maps = []
    for assignment in product(range(row_count), repeat=AUX_COLUMNS):
        table = {}
        for move in product(range(-BOUND, BOUND + 1), repeat=AUX_COLUMNS):
            sig = signature(move, assignment, row_count)
            candidate = (sum(value * value for value in move), move)
            if sig not in table or candidate < table[sig]:
                table[sig] = candidate
        maps.append((assignment, table))
    return maps


def main() -> None:
    harmful_count, moves = harmful_selector_moves()
    assert harmful_count == 140

    canonical = (1, 1, -1, 0, 0, 0, 0)  # 001 + 010 - 011
    assert any(y == canonical for _, _, y, _ in moves)

    results = {}
    for row_count in range(1, MAX_ROWS + 1):
        selector_maps = compressed_selector_maps(row_count, moves)
        aux_maps = compressed_aux_maps(row_count)
        histogram = {}
        isolated = 0
        first_isolating = None
        worst_finite = None

        for selector_assignment, selector_table in selector_maps:
            for aux_assignment, aux_table in aux_maps:
                best = None
                for sig, selector_record in selector_table.items():
                    aux_record = aux_table.get(tuple(-value for value in sig))
                    if aux_record is None:
                        continue
                    candidate = (selector_record[0] + aux_record[0],
                                 selector_record, aux_record, sig)
                    if best is None or candidate < best:
                        best = candidate
                if best is None:
                    isolated += 1
                    if first_isolating is None:
                        first_isolating = {
                            "selector_column_rows": list(selector_assignment),
                            "auxiliary_column_rows": list(aux_assignment),
                        }
                else:
                    norm2 = best[0]
                    histogram[norm2] = histogram.get(norm2, 0) + 1
                    if worst_finite is None or best[0] > worst_finite[0]:
                        worst_finite = (best[0], selector_assignment,
                                        aux_assignment, best)

        matrices = row_count ** (N + AUX_COLUMNS)
        assert matrices == len(selector_maps) * len(aux_maps)
        assert sum(histogram.values()) + isolated == matrices
        result = {
            "matrices_checked": matrices,
            "minimum_harmful_squared_norm_histogram": {
                str(k): v for k, v in sorted(histogram.items())
            },
            "isolating_matrices_in_box": isolated,
            "first_isolating_matrix": first_isolating,
        }
        if worst_finite is not None:
            norm2, selector_assignment, aux_assignment, best = worst_finite
            _, selector_record, aux_record, sig = best
            result["largest_finite_minimum_squared_norm"] = norm2
            result["largest_finite_example"] = {
                "selector_column_rows": list(selector_assignment),
                "auxiliary_column_rows": list(aux_assignment),
                "selector_move": list(selector_record[1]),
                "harmful_selector": list(selector_record[2]),
                "legal_one_hot_index": selector_record[3],
                "auxiliary_move": list(aux_record[1]),
                "selector_row_signature": list(sig),
            }
        results[row_count] = result

    assert results[1]["isolating_matrices_in_box"] == 0
    assert results[2]["isolating_matrices_in_box"] == 0
    assert results[3]["isolating_matrices_in_box"] == 18
    assert results[3]["first_isolating_matrix"] == {
        "selector_column_rows": [0, 0, 1, 0, 1, 1, 2],
        "auxiliary_column_rows": [0, 0, 0, 0, 0],
    }

    survivor_set = []
    first = results[3]["first_isolating_matrix"]
    # The full list is reconstructed during the exact loop above; rerun its
    # isolating branch into a canonical list for provenance checking.
    selector_maps = compressed_selector_maps(3, moves)
    aux_maps = compressed_aux_maps(3)
    for selector_assignment, selector_table in selector_maps:
        for aux_assignment, aux_table in aux_maps:
            if not any(
                tuple(-value for value in sig) in aux_table
                for sig in selector_table
            ):
                survivor_set.append((selector_assignment, aux_assignment))
    assert len(survivor_set) == 18
    canonical_survivors = json.dumps(survivor_set, separators=(",", ":"))
    survivor_sha256 = hashlib.sha256(canonical_survivors.encode()).hexdigest()

    print(json.dumps({
        "core": "one falsified OR clause with zero global marginals",
        "patterns": [list(pattern) for pattern in PATTERNS],
        "coefficient_box": [-BOUND, BOUND],
        "harmful_signed_selectors": harmful_count,
        "columns": N + AUX_COLUMNS,
        "column_degree": 1,
        "results_by_row_count": {str(k): v for k, v in results.items()},
        "canonical_survivors": survivor_set,
        "canonical_survivor_sha256": survivor_sha256,
        "finding": "18 of 531441 three-row matrices isolate this fiber in the tested box; one- and two-row matrices do not"
    }, sort_keys=True))


if __name__ == "__main__":
    main()
