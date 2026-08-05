#!/usr/bin/env python3
"""Exact finite attack on the surviving noncommutative ordered-pair fold.

Freeze F4=F2[a]/(a^2+a+1).  Enumerate every distinct nonzero rank-one 3x3
matrix over F4, sort its nine row-major entries lexicographically (entries are
encoded 0,1,a,1+a as 0,1,2,3), and assign the kth matrix to the kth
lexicographically sorted triple.  The ordered reduced-square coordinate (i,j)
maps to the 18 binary coefficient bits of L_i L_j; the pointed corner remains.

The verifier constructs the explicit binary image and parity-check fiber,
enumerates every mixed image word, and attacks ten YES, 200 NO, complete
all-eight, twisted-holonomy, and twenty deterministic affine-closure
witnesses.  This is a bounded finite test, never an asymptotic claim.
"""
from __future__ import annotations

import itertools
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prior" / "experiments"))
import verify_asymmetric_hash_fold as base  # type: ignore

W = 3


def f4_mul(x: int, y: int) -> int:
    """Multiply in basis (1,a), with a^2=a+1."""
    x0, x1 = x & 1, (x >> 1) & 1
    y0, y1 = y & 1, (y >> 1) & 1
    constant = (x0 & y0) ^ (x1 & y1)
    alpha = (x0 & y1) ^ (x1 & y0) ^ (x1 & y1)
    return constant | (alpha << 1)


def outer(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(f4_mul(left[i], right[j]) for i in range(W) for j in range(W))


def rank_one_labels() -> tuple[tuple[int, ...], ...]:
    vectors = [v for v in itertools.product(range(4), repeat=W) if any(v)]
    labels = sorted({outer(u, v) for u in vectors for v in vectors})
    assert len(labels) == ((4**W - 1) ** 2) // (4 - 1) == 1323
    assert all(any(label) for label in labels)
    return tuple(labels)


RANK_ONE_LABELS = rank_one_labels()


def matrix_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    out = []
    for i in range(W):
        for j in range(W):
            value = 0
            for k in range(W):
                value ^= f4_mul(left[W*i+k], right[W*k+j])
            out.append(value)
    return tuple(out)


def binary_expand(matrix: tuple[int, ...]) -> int:
    word = 0
    for j, value in enumerate(matrix):
        word |= (value & 1) << (2*j)
        word |= ((value >> 1) & 1) << (2*j + 1)
    return word


def coordinate_labels(triples: list[tuple[int, int, int]]) -> list[tuple[int, ...]]:
    ordered = sorted(triples)
    assert len(set(ordered)) == len(ordered) <= len(RANK_ONE_LABELS)
    by_triple = {triple: RANK_ONE_LABELS[k] for k, triple in enumerate(ordered)}
    return [by_triple[triple] for triple in triples]


def incidence_fiber(q: int, triples: list[tuple[int, int, int]]) -> list[int]:
    columns = [base.syn(q, triple) for triple in triples]
    target = (1 << (3*q)) - 1
    fiber = []
    for selection in range(1 << len(triples)):
        syndrome = 0
        for j, column in enumerate(columns):
            if (selection >> j) & 1:
                syndrome ^= column
        if syndrome == target:
            fiber.append(selection)
    return fiber


def pointed_code(q: int, triples: list[tuple[int, int, int]]):
    columns = [base.syn(q, triple) for triple in triples]
    target = (1 << (3*q)) - 1
    kernel, fiber = [], []
    for selection in range(1 << len(triples)):
        syndrome = 0
        for j, column in enumerate(columns):
            if (selection >> j) & 1:
                syndrome ^= column
        if syndrome == 0:
            kernel.append(selection)
        if syndrome == target:
            fiber.append(selection)
    if not fiber:
        return None
    point = min(fiber, key=lambda x: (x.bit_count(), x))
    rows = base.basis([word << 1 for word in kernel] + [1 | (point << 1)])
    return rows, fiber


def rref(rows: list[int], n: int) -> tuple[list[int], list[int]]:
    rows = [row & ((1 << n) - 1) for row in rows if row]
    pivot_columns = []
    rank = 0
    for column in range(n):
        pivot = next((i for i in range(rank, len(rows)) if (rows[i] >> column) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> column) & 1):
                rows[i] ^= rows[rank]
        pivot_columns.append(column)
        rank += 1
        if rank == len(rows):
            break
    return rows[:rank], pivot_columns


def nullspace(rows: list[int], n: int) -> list[int]:
    equations, pivots = rref(rows, n)
    free = [j for j in range(n) if j not in pivots]
    answer = []
    for f in free:
        vector = 1 << f
        for row, pivot in zip(equations, pivots):
            if (row & vector).bit_count() & 1:
                vector |= 1 << pivot
        answer.append(vector)
    assert len(answer) == n - len(pivots)
    assert all(not ((h & row).bit_count() & 1) for h in answer for row in rows)
    return answer


def prune_image(rows: list[int], nominal_moving: int):
    rows = base.basis(rows)
    active = [j for j in range(nominal_moving)
              if any((row >> (1+j)) & 1 for row in rows)]
    image = []
    for row in rows:
        word = row & 1
        for new, old in enumerate(active):
            word |= ((row >> (1+old)) & 1) << (1+new)
        image.append(word)
    return base.basis(image), active


def explicit_syndrome_fiber(image: list[int], moving: int):
    pointed = next(row for row in image if row & 1)
    kernel_rows = []
    for row in image:
        zero_star = row ^ (pointed if row & 1 else 0)
        if zero_star:
            kernel_rows.append(zero_star >> 1)
    kernel_rows = base.basis(kernel_rows)
    checks = nullspace(kernel_rows, moving)
    target = sum((((check & (pointed >> 1)).bit_count() & 1) << i)
                 for i, check in enumerate(checks))
    assert len(checks) == moving - len(kernel_rows)
    for row in image:
        syndrome = sum((((check & (row >> 1)).bit_count() & 1) << i)
                       for i, check in enumerate(checks))
        assert syndrome == (target if row & 1 else 0)
    return checks, target, len(kernel_rows)


def fold_report(q: int, triples: list[tuple[int, int, int]]):
    data = pointed_code(q, triples)
    assert data is not None
    rows, fiber = data
    labels = coordinate_labels(triples)
    products = [[binary_expand(matrix_mul(left, right)) for right in labels] for left in labels]
    # The frozen labels genuinely preserve some orientation.
    assert any(products[i][j] != products[j][i]
               for i in range(len(labels)) for j in range(len(labels)))

    generators = []
    for left in rows:
        for right in rows:
            moving_word = 0
            for i in range(len(triples)):
                if not ((left >> (1+i)) & 1):
                    continue
                for j in range(len(triples)):
                    if (right >> (1+j)) & 1:
                        moving_word ^= products[i][j]
            generators.append(((left & 1) & (right & 1)) | (moving_word << 1))
    image, active = prune_image(generators, 18)

    pointed_words = []
    for mask in range(1 << len(image)):
        word = 0
        for i, row in enumerate(image):
            if (mask >> i) & 1:
                word ^= row
        if word & 1:
            pointed_words.append((word.bit_count()-1, mask, word))
    assert pointed_words
    minimum = min(pointed_words)

    checks, target, kernel_dimension = explicit_syndrome_fiber(image, len(active))
    assert target < (1 << len(checks))
    assert kernel_dimension + len(checks) == len(active)

    illegal_pure_costs = []
    legal_pure_costs = []
    active_mask = sum(1 << old for old in active)
    for selection in fiber:
        output = 0
        for i in range(len(triples)):
            if not ((selection >> i) & 1):
                continue
            for j in range(len(triples)):
                if (selection >> j) & 1:
                    output ^= products[i][j]
        cost = (output & active_mask).bit_count()
        if selection.bit_count() == q:
            legal_pure_costs.append(cost)
        else:
            illegal_pure_costs.append(cost)

    base_distance = min(x.bit_count() for x in fiber)
    return {
        "base_distance": base_distance,
        "unfurled_square_distance": base_distance * base_distance,
        "source_square_dimension": len(base.reduced(rows, len(triples))),
        "fiber_size": len(fiber),
        "image_dimension": len(image),
        "nominal_pointed_length": 19,
        "active_pointed_length": 1 + len(active),
        "exact_transfer_rank": len(active),
        "parity_check_rank": len(checks),
        "target": target,
        "folded_distance": minimum[0],
        "minimum_message_mask": minimum[1],
        "minimum_output_word": minimum[2],
        "pointed_kernel": minimum[0] == 0,
        "cheapest_semantic_illegal_pure_square": min(illegal_pure_costs, default=None),
        "legal_pure_square_range": None if not legal_pure_costs else
            [min(legal_pure_costs), max(legal_pure_costs)],
        "mixed_words_enumerated": 1 << len(image),
        "active_coordinates": tuple(active),
    }


def families(no_count: int = 200):
    yes = [base.planted(3, 8, seed) for seed in range(10)]
    no = []
    for seed in range(10000, 100000):
        triples = base.randomT(3, 8, seed)
        fiber = incidence_fiber(3, triples)
        if fiber and min(x.bit_count() for x in fiber) > 3:
            assert min(x.bit_count() for x in fiber) == 5
            no.append(triples)
            if len(no) == no_count:
                break
    assert len(no) == no_count
    return yes, no


def span_contains(rows: list[int], word: int) -> bool:
    pivots = sorted(base.basis(rows), key=int.bit_length, reverse=True)
    for row in pivots:
        if word.bit_length() == row.bit_length():
            word ^= row
    return word == 0


def affine_closure_witnesses(count: int = 20):
    witnesses = []
    for seed in range(100000):
        triples = base.randomT(3, 8, seed)
        fiber = incidence_fiber(3, triples)
        matchings = [x for x in fiber if x.bit_count() == 3]
        if not matchings:
            continue
        reference = matchings[0]
        differences = [x ^ reference for x in matchings[1:]]
        illegal = [x for x in fiber if x.bit_count() != 3 and
                   span_contains(differences, x ^ reference)]
        if illegal:
            witnesses.append((seed, triples, illegal))
            if len(witnesses) == count:
                break
    assert len(witnesses) == count
    assert all(min(x.bit_count() for x in bad) >= 5 for _, _, bad in witnesses)
    return witnesses


def all_eight_dictionary():
    return 2, list(itertools.product(range(2), repeat=3))


def holonomy_dictionary():
    q = 3
    triples = ([(i, i, i) for i in range(q)] +
               [(i, (i+1)%q, (i+2)%q) for i in range(q)] +
               [(i, (i+2)%q, (i+1)%q) for i in range(q)])
    assert sorted(x.bit_count() for x in incidence_fiber(q, triples)) == [3,3,3,9]
    return q, triples


def check_relabeling(q: int, triples: list[tuple[int,int,int]], exhaustive: bool):
    labels = coordinate_labels(triples)
    permutations = itertools.permutations(range(len(triples))) if exhaustive else [tuple(reversed(range(len(triples))))]
    checked = 0
    for permutation in permutations:
        permuted = [triples[i] for i in permutation]
        assert coordinate_labels(permuted) == [labels[i] for i in permutation]
        checked += 1
    reverse_report = fold_report(q, list(reversed(triples)))
    original_report = fold_report(q, triples)
    for key in ("image_dimension", "active_pointed_length", "exact_transfer_rank",
                "folded_distance", "pointed_kernel",
                "cheapest_semantic_illegal_pure_square", "mixed_words_enumerated"):
        assert reverse_report[key] == original_report[key]
    return checked


def compact(report: dict):
    return {key: report[key] for key in (
        "base_distance", "unfurled_square_distance", "source_square_dimension",
        "fiber_size", "image_dimension", "nominal_pointed_length",
        "active_pointed_length", "exact_transfer_rank", "parity_check_rank",
        "folded_distance", "pointed_kernel",
        "cheapest_semantic_illegal_pure_square", "legal_pure_square_range",
        "mixed_words_enumerated"
    )}


def main() -> None:
    yes, no = families()
    closure = affine_closure_witnesses()
    q8, all_eight = all_eight_dictionary()
    qh, holonomy = holonomy_dictionary()

    yes_reports = [fold_report(3, triples) for triples in yes]
    no_reports = [fold_report(3, triples) for triples in no]
    closure_reports = [(seed, fold_report(3, triples), min(bad, key=int.bit_count))
                       for seed, triples, bad in closure]
    all_eight_report = fold_report(q8, all_eight)
    holonomy_report = fold_report(qh, holonomy)

    worst_yes = max(r["folded_distance"] for r in yes_reports)
    best_no = min(r["folded_distance"] for r in no_reports)
    max_rank = max(r["exact_transfer_rank"] for r in yes_reports + no_reports)
    ratio = best_no / worst_yes if worst_yes else 0.0
    exponent = math.log(ratio) / math.log(max_rank) if ratio > 1 and max_rank > 1 else 0.0
    baseline = math.log(25/9) / math.log(65)

    hostile_semantic_costs = [r["cheapest_semantic_illegal_pure_square"]
                              for _, r, _ in closure_reports]
    hostile_semantic_costs += [all_eight_report["cheapest_semantic_illegal_pure_square"],
                               holonomy_report["cheapest_semantic_illegal_pure_square"]]
    assert all(cost is not None for cost in hostile_semantic_costs)

    relabelings = 0
    for triples in yes + no[:10] + [all_eight]:
        relabelings += check_relabeling(2 if triples is all_eight else 3, triples, exhaustive=True)
    relabelings += check_relabeling(qh, holonomy, exhaustive=False)
    for triples in no[10:] + [item[1] for item in closure]:
        relabelings += check_relabeling(3, triples, exhaustive=False)
    assert relabelings == 21 * math.factorial(8) + 1 + 190 + len(closure)

    success = (not any(r["pointed_kernel"] for r in yes_reports + no_reports +
                       [all_eight_report, holonomy_report] + [r for _,r,_ in closure_reports]) and
               best_no > worst_yes and exponent > baseline and
               min(hostile_semantic_costs) > worst_yes)

    summary = {
        "mechanism": "lexicographically frozen rank-one 3x3 F4 labels with ordered matrix-product coefficients",
        "expected_move": "noncommutativity removes the symmetric-pair kernel while 18 bits retain the reduced-square gap",
        "falsification": "pointed kernel, best NO not above worst YES, hostile illegal cost not above worst YES, or exponent not above baseline",
        "field": {"basis": ["1", "a"], "relation": "a^2=a+1"},
        "rank_one_label_count": len(RANK_ONE_LABELS),
        "first_nine_labels": [list(label) for label in RANK_ONE_LABELS[:9]],
        "instances": {"YES_q3_m8": 10, "NO_q3_m8": 200,
                      "affine_closure_q3_m8": len(closure),
                      "all_eight_q2_m8": 1, "holonomy_q3_m9": 1},
        "unfurled": {"worst_YES": 9, "best_NO": 25,
                     "exact_transfer_rank": 64, "pointed_length": 65,
                     "rank_exponent": baseline},
        "folded": {
            "worst_YES": worst_yes, "best_NO": best_no,
            "uniform_ratio": ratio, "max_exact_transfer_rank": max_rank,
            "rank_exponent": exponent,
            "YES_distance_range": [min(r["folded_distance"] for r in yes_reports), worst_yes],
            "NO_distance_range": [best_no, max(r["folded_distance"] for r in no_reports)],
            "YES_pointed_kernels": sum(r["pointed_kernel"] for r in yes_reports),
            "NO_pointed_kernels": sum(r["pointed_kernel"] for r in no_reports),
            "pointed_kernels": sum(r["pointed_kernel"] for r in yes_reports + no_reports),
        },
        "all_eight": compact(all_eight_report),
        "holonomy": compact(holonomy_report),
        "affine_closure": {
            "seeds": [seed for seed,_,_ in closure_reports],
            "folded_distance_range": [min(r["folded_distance"] for _,r,_ in closure_reports),
                                      max(r["folded_distance"] for _,r,_ in closure_reports)],
            "semantic_illegal_cost_range": [min(r["cheapest_semantic_illegal_pure_square"] for _,r,_ in closure_reports),
                                            max(r["cheapest_semantic_illegal_pure_square"] for _,r,_ in closure_reports)],
            "pointed_kernels": sum(r["pointed_kernel"] for _,r,_ in closure_reports),
        },
        "mixed_words_enumerated": sum(r["mixed_words_enumerated"] for r in yes_reports + no_reports +
                                      [all_eight_report, holonomy_report] + [r for _,r,_ in closure_reports]),
        "coordinate_relabelings_checked": relabelings,
        "primary_success": success,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    # Freeze the exact failure of the precommitted lexicographic label rule.
    assert (worst_yes, best_no, max_rank) == (3, 0, 4)
    assert sum(r["pointed_kernel"] for r in no_reports) == 112
    assert holonomy_report["folded_distance"] == 0 and holonomy_report["pointed_kernel"]
    assert all_eight_report["folded_distance"] == 1
    assert sum(r["pointed_kernel"] for _,r,_ in closure_reports) == 18
    assert min(r["cheapest_semantic_illegal_pure_square"] for _,r,_ in closure_reports) == 0
    assert not success
    print("F4_ORDERED_PAIR_FOLD_PASS")


if __name__ == "__main__":
    main()
