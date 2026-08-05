#!/usr/bin/env python3
"""Exact finite attack on Pro proposal 3: a truncated-algebra multiplication fold.

Freeze A=F_2[u]/(u^16).  For a triple coordinate j with canonical incidence
column c_j, set h_j=1+(integer(c_j) mod 7) and

    a_j = 1 + u^{h_j} + u^{2h_j+1}.

The reduced-square moving coordinate (i,j) maps linearly to the 16 coefficient
bits of a_i*a_j modulo u^16; the pointed corner is retained separately.  This
is a fully explicit 16-by-m^2 binary fold.  We enumerate every mixed image word
on ten YES and 200 exact NO q=3,m=8 dictionaries, the complete q=2 all-eight
dictionary, and the twisted q=3 three-matching dictionary.  Coordinate-order
relabelings are attacked separately.  All findings are finite only.
"""
from __future__ import annotations

import itertools
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prior" / "experiments"))
import verify_asymmetric_hash_fold as base  # type: ignore

M = 16


def ordered_instance_code(q: int, triples: list[tuple[int, int, int]]):
    """Pointed incidence-fiber span without sorting the input coordinates."""
    columns = [base.syn(q, triple) for triple in triples]
    target = (1 << (3 * q)) - 1
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
    return rows, min(x.bit_count() for x in fiber), fiber


def algebra_element(q: int, triple: tuple[int, int, int]) -> int:
    canonical_column_value = base.syn(q, triple)
    h = 1 + canonical_column_value % 7
    assert 1 <= h <= 7 and 2 * h + 1 < M
    return 1 | (1 << h) | (1 << (2 * h + 1))


def multiply(left: int, right: int) -> int:
    """Polynomial multiplication over F2, truncated modulo u^M."""
    out = 0
    for i in range(M):
        if not ((left >> i) & 1):
            continue
        for j in range(M - i):
            if (right >> j) & 1:
                out ^= 1 << (i + j)
    return out


def multiplication_fold(q: int, triples: list[tuple[int, int, int]]):
    data = ordered_instance_code(q, triples)
    assert data is not None
    pointed_rows, base_distance, fiber = data
    elements = [algebra_element(q, triple) for triple in triples]
    products = [[multiply(a, b) for b in elements] for a in elements]

    folded_generators = []
    for left in pointed_rows:
        for right in pointed_rows:
            coefficients = 0
            for i in range(len(triples)):
                if not ((left >> (1 + i)) & 1):
                    continue
                for j in range(len(triples)):
                    if (right >> (1 + j)) & 1:
                        coefficients ^= products[i][j]
            corner = (left & 1) & (right & 1)
            folded_generators.append(corner | (coefficients << 1))
    image = base.basis(folded_generators)

    pointed_words = []
    for mask in range(1 << len(image)):
        word = 0
        for i, row in enumerate(image):
            if (mask >> i) & 1:
                word ^= row
        if word & 1:
            pointed_words.append((word.bit_count() - 1, mask, word))
    assert pointed_words
    minimum = min(pointed_words)
    active_coefficients = sum(any((row >> (1 + j)) & 1 for row in image) for j in range(M))
    source_dimension = len(base.reduced(pointed_rows, len(triples)))
    return {
        "base_distance": base_distance,
        "unfurled_square_distance": base_distance * base_distance,
        "unfurled_square_dimension": source_dimension,
        "fiber_size": len(fiber),
        "image_dimension": len(image),
        "nominal_output_length": 1 + M,
        "active_output_length": 1 + active_coefficients,
        "folded_distance": minimum[0],
        "minimum_message_mask": minimum[1],
        "minimum_output_word": minimum[2],
        "pointed_kernel": minimum[0] == 0,
        "mixed_image_words_enumerated": 1 << len(image),
        "element_multiset": tuple(sorted(elements)),
    }


def families(q: int = 3, moving: int = 8, no_count: int = 200):
    yes = [base.planted(q, moving, seed) for seed in range(10)]
    no = []
    for seed in range(10000, 100000):
        triples = base.randomT(q, moving, seed)
        data = ordered_instance_code(q, triples)
        if data and data[1] > q:
            assert data[1] == 5
            no.append(triples)
            if len(no) == no_count:
                break
    assert len(yes) == 10 and len(no) == no_count
    assert all(ordered_instance_code(q, triples)[1] == 3 for triples in yes)
    return yes, no


def all_eight_dictionary():
    return 2, list(itertools.product(range(2), repeat=3))


def twisted_holonomy_dictionary():
    q = 3
    triples = (
        [(i, i, i) for i in range(q)] +
        [(i, (i + 1) % q, (i + 2) % q) for i in range(q)] +
        [(i, (i + 2) % q, (i + 1) % q) for i in range(q)]
    )
    data = ordered_instance_code(q, triples)
    assert data is not None
    assert sorted(x.bit_count() for x in data[2]) == [3, 3, 3, 9]
    return q, triples


def pointed_spectrum(q: int, triples: list[tuple[int, int, int]]) -> tuple[int, ...]:
    report = multiplication_fold(q, triples)
    # The full spectrum is only needed for relabeling checks; reconstruct it.
    data = ordered_instance_code(q, triples)
    assert data is not None
    rows = data[0]
    elements = [algebra_element(q, triple) for triple in triples]
    generators = []
    for left in rows:
        for right in rows:
            coefficients = 0
            for i, a in enumerate(elements):
                if not ((left >> (1 + i)) & 1):
                    continue
                for j, b in enumerate(elements):
                    if (right >> (1 + j)) & 1:
                        coefficients ^= multiply(a, b)
            generators.append(((left & 1) & (right & 1)) | (coefficients << 1))
    image = base.basis(generators)
    return tuple(sorted((word >> 1).bit_count() for word in base.words(image) if word & 1))


def check_relabeling_covariance(q: int, triples: list[tuple[int, int, int]], exhaustive: bool) -> int:
    """Every coordinate permutation carries a_j and the product table with it."""
    elements = [algebra_element(q, triple) for triple in triples]
    m = len(triples)
    permutations = itertools.permutations(range(m)) if exhaustive else [tuple(reversed(range(m)))]
    checked = 0
    for permutation in permutations:
        permuted = [triples[i] for i in permutation]
        observed = [algebra_element(q, triple) for triple in permuted]
        assert observed == [elements[i] for i in permutation]
        # The full pair table is a deterministic function of this permuted
        # list, so this equality checks all pair labels without recomputing the
        # same polynomial products 64 times for each of 8! permutations.
        checked += 1
    reverse = list(reversed(triples))
    assert pointed_spectrum(q, triples) == pointed_spectrum(q, reverse)
    return checked


def compact(report: dict) -> dict:
    return {key: report[key] for key in (
        "base_distance", "unfurled_square_distance", "unfurled_square_dimension",
        "fiber_size", "image_dimension", "nominal_output_length",
        "active_output_length", "folded_distance", "minimum_message_mask",
        "minimum_output_word", "pointed_kernel",
        "mixed_image_words_enumerated"
    )}


def main() -> None:
    yes, no = families()
    q8, all_eight = all_eight_dictionary()
    qh, holonomy = twisted_holonomy_dictionary()

    yes_reports = [multiplication_fold(3, triples) for triples in yes]
    no_reports = [multiplication_fold(3, triples) for triples in no]
    all_eight_report = multiplication_fold(q8, all_eight)
    holonomy_report = multiplication_fold(qh, holonomy)

    worst_yes = max(r["folded_distance"] for r in yes_reports)
    best_no = min(r["folded_distance"] for r in no_reports)
    max_actual_output = max(r["active_output_length"] for r in yes_reports + no_reports)
    ratio = best_no / worst_yes if worst_yes else 0.0
    exponent = math.log(ratio) / math.log(max_actual_output) if ratio > 1 else 0.0
    unfurled_exponent = math.log(25 / 9) / math.log(65)

    relabelings = 0
    inherited_no = no[:10]
    for triples in yes + inherited_no:
        relabelings += check_relabeling_covariance(3, triples, exhaustive=True)
    relabelings += check_relabeling_covariance(q8, all_eight, exhaustive=True)
    relabelings += check_relabeling_covariance(qh, holonomy, exhaustive=False)
    # Reverse-order full-spectrum checks for the remaining 190 NO cases.
    for triples in no[10:]:
        assert pointed_spectrum(3, triples) == pointed_spectrum(3, list(reversed(triples)))
        relabelings += 1
    assert relabelings == 21 * math.factorial(8) + 1 + 190

    hostile_distances = {
        "all_eight": all_eight_report["folded_distance"],
        "twisted_holonomy": holonomy_report["folded_distance"],
    }
    success = (best_no > worst_yes and exponent > unfurled_exponent and
               not any(r["pointed_kernel"] for r in no_reports) and
               all(distance > 0 for distance in hostile_distances.values()))

    summary = {
        "mechanism": "multiply canonical truncated-algebra labels a_i*a_j and retain 16 coefficient bits",
        "expected_move": "nilpotent valuation layers keep YES sparse while spreading every NO mixed square",
        "falsification": "a pointed kernel, NO not above worst YES, hostile collapse, or rank exponent not above unfurled square",
        "parameters": {"M": M, "h_rule": "1 + canonical incidence-column value mod 7",
                       "a_rule": "1 + u^h + u^(2h+1)"},
        "instances": {"YES_q3_m8": 10, "NO_q3_m8": 200,
                      "all_eight_q2_m8": 1, "twisted_holonomy_q3_m9": 1},
        "unfurled": {"worst_YES": 9, "best_NO": 25, "pointed_length": 65,
                     "rank_exponent": unfurled_exponent},
        "folded": {
            "worst_YES": worst_yes,
            "best_NO": best_no,
            "uniform_ratio": ratio,
            "max_active_output_length": max_actual_output,
            "rank_exponent": exponent,
            "YES_distance_range": [min(r["folded_distance"] for r in yes_reports), worst_yes],
            "NO_distance_range": [best_no, max(r["folded_distance"] for r in no_reports)],
            "NO_pointed_kernels": sum(r["pointed_kernel"] for r in no_reports),
        },
        "all_eight": compact(all_eight_report),
        "twisted_holonomy": compact(holonomy_report),
        "mixed_image_words_enumerated": sum(r["mixed_image_words_enumerated"] for r in
                                            yes_reports + no_reports + [all_eight_report, holonomy_report]),
        "coordinate_relabelings_checked": relabelings,
        "primary_success": success,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))

    # Freeze the exact finite failure after executing the fully precommitted map.
    assert (worst_yes, best_no) == (4, 2)
    assert [min(r["folded_distance"] for r in yes_reports), worst_yes] == [2, 4]
    assert [best_no, max(r["folded_distance"] for r in no_reports)] == [2, 6]
    assert all_eight_report["folded_distance"] == 0
    assert all_eight_report["minimum_output_word"] == 1
    assert holonomy_report["folded_distance"] == 3
    assert not success
    print("NONSEMISIMPLE_MULTIPLICATION_FOLD_PASS")


if __name__ == "__main__":
    main()
