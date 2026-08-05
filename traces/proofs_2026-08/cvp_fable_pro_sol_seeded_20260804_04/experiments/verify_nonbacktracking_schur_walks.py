#!/usr/bin/env python3
"""Exact finite attack on Pro proposal 7: collision-seeded Schur walks.

The map is frozen before evaluating distances.  For a 3DM dictionary T, form
its incompatibility graph (two distinct triples are adjacent when they share a
vertex).  For r in {2,3,4}, retain the original triple coordinates and append
one Boolean product coordinate for every ordered nonbacktracking r-vertex
walk.  Every matching makes every walk product zero.

The nonlinear lift of every point in the affine incidence fiber is explicit.
We row-reduce the span of all lifts and enumerate every pointed mixed word,
not only lifted fiber points.  The primary preregistered map is r=4; r=2,3 are
diagnostics and cannot rescue its failure.  Tests use the existing ten
q=3,m=8 YES and ten NO dictionaries, extend the same deterministic stream to
200 exact NO dictionaries, and include the q=2 complete-cube (all-eight)
dictionary and a q=3 union of three twisted permutation matchings whose odd
XOR is the all-nine parity cover.  These are finite diagnostics only.
"""
from __future__ import annotations

import itertools
import json
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prior" / "experiments"))
import verify_asymmetric_hash_fold as base  # type: ignore

PRIMARY_LENGTH = 4
DIAGNOSTIC_LENGTHS = (2, 3)


def incidence_fiber(q: int, triples: list[tuple[int, int, int]]) -> list[int]:
    columns = [base.syn(q, triple) for triple in triples]
    target = (1 << (3 * q)) - 1
    fiber = []
    for selection in range(1 << len(triples)):
        syndrome = 0
        for j, column in enumerate(columns):
            if (selection >> j) & 1:
                syndrome ^= column
        if syndrome == target:
            fiber.append(selection)
    assert fiber
    return fiber


def incompatible(left: tuple[int, int, int], right: tuple[int, int, int]) -> bool:
    return any(a == b for a, b in zip(left, right))


def incompatibility_rows(triples: list[tuple[int, int, int]]) -> tuple[int, ...]:
    rows = []
    for i, left in enumerate(triples):
        row = 0
        for j, right in enumerate(triples):
            if i != j and incompatible(left, right):
                row |= 1 << j
        rows.append(row)
    return tuple(rows)


def nonbacktracking_walks(triples: list[tuple[int, int, int]], length: int) -> tuple[tuple[int, ...], ...]:
    """Ordered walks with r vertices; only immediate reversal is forbidden."""
    assert length >= 2
    adjacency = incompatibility_rows(triples)
    walks = [(i, j) for i in range(len(triples))
             for j in range(len(triples)) if (adjacency[i] >> j) & 1]
    for _ in range(2, length):
        extended = []
        for walk in walks:
            previous, last = walk[-2], walk[-1]
            for nxt in range(len(triples)):
                if nxt != previous and ((adjacency[last] >> nxt) & 1):
                    extended.append(walk + (nxt,))
        walks = extended
    return tuple(walks)


def lift(selection: int, moving: int, walks: tuple[tuple[int, ...], ...]) -> int:
    word = 1 | (selection << 1)
    for index, walk in enumerate(walks):
        # Revisited vertices are idempotent Boolean factors.
        if all((selection >> vertex) & 1 for vertex in walk):
            word |= 1 << (1 + moving + index)
    return word


def lifted_code(q: int, triples: list[tuple[int, int, int]], length: int):
    fiber = incidence_fiber(q, triples)
    walks = nonbacktracking_walks(triples, length)
    pure = [lift(selection, len(triples), walks) for selection in fiber]
    rows = base.basis(pure)
    pointed = []
    illegal_pointed = []
    selection_mask = (1 << len(triples)) - 1
    for mask in range(1 << len(rows)):
        word = 0
        for i, row in enumerate(rows):
            if (mask >> i) & 1:
                word ^= row
        if word & 1:
            item = (word.bit_count() - 1, mask, word)
            pointed.append(item)
            selection = (word >> 1) & selection_mask
            if selection.bit_count() != q:
                illegal_pointed.append(item)
    assert pointed
    mixed_min, mixed_mask, mixed_word = min(pointed)
    cheapest_illegal = min(illegal_pointed, default=None)
    pure_min = min(word.bit_count() - 1 for word in pure)
    active_moving = sum(
        any((row >> coordinate) & 1 for row in rows)
        for coordinate in range(1, 1 + len(triples) + len(walks))
    )
    return {
        "fiber_size": len(fiber),
        "walks": len(walks),
        "nominal_length": 1 + len(triples) + len(walks),
        "active_ambient_rank": 1 + active_moving,
        "code_dimension": len(rows),
        "pure_min": pure_min,
        "mixed_min": mixed_min,
        "mixed_mask": mixed_mask,
        "mixed_word": mixed_word,
        "cheapest_illegal_mixed": None if cheapest_illegal is None else cheapest_illegal[0],
        "cheapest_illegal_original_weight": None if cheapest_illegal is None else
            (((cheapest_illegal[2] >> 1) & selection_mask).bit_count()),
        "mixed_words_enumerated": 1 << len(rows),
    }


def existing_families(q: int = 3, moving: int = 8, no_count: int = 200):
    yes = [base.planted(q, moving, seed) for seed in range(10)]
    no = []
    for seed in range(10000, 100000):
        triples = base.randomT(q, moving, seed)
        data = base.instance_code(q, triples)
        if data and data[1] > q:
            no.append(triples)
            if len(no) == no_count:
                break
    assert len(yes) == 10 and len(no) == no_count
    assert all(min(x.bit_count() for x in incidence_fiber(q, triples)) == 3 for triples in yes)
    assert all(min(x.bit_count() for x in incidence_fiber(q, triples)) == 5 for triples in no)
    return yes, no


def all_eight_dictionary() -> tuple[int, list[tuple[int, int, int]]]:
    return 2, list(itertools.product(range(2), repeat=3))


def odd_holonomy_dictionary() -> tuple[int, list[tuple[int, int, int]]]:
    """Three twisted permutation matchings; their odd XOR is an illegal cover."""
    q = 3
    matchings = [
        [(i, i, i) for i in range(q)],
        [(i, (i + 1) % q, (i + 2) % q) for i in range(q)],
        [(i, (i + 2) % q, (i + 1) % q) for i in range(q)],
    ]
    triples = [triple for matching in matchings for triple in matching]
    assert len(set(triples)) == 9
    fiber = incidence_fiber(q, triples)
    assert sorted(x.bit_count() for x in fiber) == [3, 3, 3, 9]
    assert (1 << 9) - 1 in fiber
    return q, triples


def permute_dictionary(triples: list[tuple[int, int, int]], permutation: tuple[int, ...]):
    return [triples[i] for i in permutation]


def check_relabelings(triples: list[tuple[int, int, int]], exhaustive: bool) -> int:
    """Check graph covariance; walks and product coordinates inherit the bijection."""
    m = len(triples)
    original = incompatibility_rows(triples)
    permutations = itertools.permutations(range(m)) if exhaustive else [tuple(reversed(range(m)))]
    checked = 0
    for permutation in permutations:
        relabeled = permute_dictionary(triples, permutation)
        observed = incompatibility_rows(relabeled)
        for new_i, old_i in enumerate(permutation):
            for new_j, old_j in enumerate(permutation):
                assert ((observed[new_i] >> new_j) & 1) == ((original[old_i] >> old_j) & 1)
        checked += 1
    # Exercise the complete primary lift on a nontrivial relabeling.
    reverse = tuple(reversed(range(m)))
    before = lifted_code(2 if m == 8 and set(triples) == set(itertools.product(range(2), repeat=3)) else 3,
                         triples, PRIMARY_LENGTH)
    after = lifted_code(2 if m == 8 and set(triples) == set(itertools.product(range(2), repeat=3)) else 3,
                        permute_dictionary(triples, reverse), PRIMARY_LENGTH)
    for key in ("walks", "nominal_length", "active_ambient_rank", "code_dimension",
                "pure_min", "mixed_min", "mixed_words_enumerated"):
        assert before[key] == after[key]
    return checked


def compact(report: dict) -> dict:
    return {key: report[key] for key in (
        "fiber_size", "walks", "nominal_length", "active_ambient_rank",
        "code_dimension", "pure_min", "mixed_min", "cheapest_illegal_mixed",
        "cheapest_illegal_original_weight", "mixed_words_enumerated"
    )}


def main() -> None:
    # The first ten NO dictionaries are the inherited suite.  We continue the
    # same deterministic seed stream to 200 NO dictionaries as an adversarial
    # generalization attack after the initial finite signal.
    yes, no = existing_families(no_count=200)
    inherited_no = no[:10]
    q8, all_eight = all_eight_dictionary()
    qh, holonomy = odd_holonomy_dictionary()

    by_length = {}
    total_words = 0
    detailed = {}
    for length in (*DIAGNOSTIC_LENGTHS, PRIMARY_LENGTH):
        yes_reports = [lifted_code(3, triples, length) for triples in yes]
        no_reports = [lifted_code(3, triples, length) for triples in no]
        all_eight_report = lifted_code(q8, all_eight, length)
        holonomy_report = lifted_code(qh, holonomy, length)
        total_words += sum(r["mixed_words_enumerated"] for r in
                           yes_reports + no_reports + [all_eight_report, holonomy_report])
        worst_yes = max(r["mixed_min"] for r in yes_reports)
        best_no = min(r["mixed_min"] for r in no_reports)
        max_output = max(r["nominal_length"] for r in yes_reports + no_reports)
        ratio = best_no / worst_yes
        exponent = math.log(ratio) / math.log(max_output) if ratio > 1 else 0.0
        by_length[length] = {
            "worst_YES": worst_yes,
            "best_NO": best_no,
            "uniform_ratio": ratio,
            "max_nominal_output_length": max_output,
            "max_active_ambient_rank": max(r["active_ambient_rank"] for r in yes_reports + no_reports),
            "max_code_dimension": max(r["code_dimension"] for r in yes_reports + no_reports),
            "YES_pure_min_range": [min(r["pure_min"] for r in yes_reports),
                                   max(r["pure_min"] for r in yes_reports)],
            "NO_pure_min_range": [min(r["pure_min"] for r in no_reports),
                                  max(r["pure_min"] for r in no_reports)],
            "NO_mixed_min_range": [min(r["mixed_min"] for r in no_reports),
                                   max(r["mixed_min"] for r in no_reports)],
            "rank_exponent": exponent,
            "all_eight": compact(all_eight_report),
            "odd_holonomy": compact(holonomy_report),
        }
        detailed[length] = (yes_reports, no_reports)

    # Base exponent uses the explicit pointed length 1+m=9.
    base_exponent = math.log(5 / 3) / math.log(9)
    primary = by_length[PRIMARY_LENGTH]
    success = (primary["worst_YES"] == 3 and primary["best_NO"] > 5 and
               primary["rank_exponent"] > base_exponent)

    relabelings = 0
    # Exhaust every 8! relabeling for the 20 primary dictionaries and all-eight.
    for triples in yes + inherited_no + [all_eight]:
        relabelings += check_relabelings(triples, exhaustive=True)
    # The nine-coordinate holonomy dictionary gets a complete reverse relabeling check.
    relabelings += check_relabelings(holonomy, exhaustive=False)
    assert relabelings == 21 * math.factorial(8) + 1

    summary = {
        "mechanism": "original triple coordinates plus products indexed by every ordered nonbacktracking incompatibility walk",
        "expected_move": "a collision in a NO odd cover seeds many walk coordinates while every matching has zero walk cost",
        "falsification": "primary length 4 fails unless YES=3, every NO>5, and the uniform rank exponent beats the base",
        "instances": {"YES_q3_m8": 10, "inherited_NO_q3_m8": 10,
                      "extended_NO_q3_m8": 200,
                      "all_eight_q2_m8": 1, "odd_holonomy_q3_m9": 1},
        "lengths": by_length,
        "base": {"worst_YES": 3, "best_NO": 5, "pointed_length": 9,
                 "rank_exponent": base_exponent},
        "primary_length": PRIMARY_LENGTH,
        "primary_success": success,
        "mixed_words_enumerated": total_words,
        "coordinate_relabelings_checked": relabelings,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))

    # Freeze exact finite outcomes after executing the preregistered map.
    assert primary["worst_YES"] == 3
    assert primary["best_NO"] == 33
    assert primary["uniform_ratio"] == 11
    assert success
    print("NONBACKTRACKING_SCHUR_WALKS_PASS")


if __name__ == "__main__":
    main()
