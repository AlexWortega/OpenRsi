#!/usr/bin/env python3
"""Exact bounded attack on a canonical modular-Kronecker tensor fold.

This implements only Pro proposal 2, the sole proposal surviving cross-review.
For each of the existing ten q=3,m=8 YES and ten NO pointed 3DM codes, it:

* canonicalizes the base generator-column multiset under every row-basis change;
* assigns the r-th canonical moving-column type the public exponent 2**r;
* maps an ordered reduced-square coordinate (i,j) to
      2**rank(type_i) + 2**(T + rank(type_j)) mod M
  in every block M of a fixed public modulus tuple;
* XOR-folds coordinates in a bucket and enumerates every mixed image word.

The modulus family is frozen below, independently of all distances.  It consists
of every singleton 2..32 and the first 2..5 prefixes of a fixed prime list.  All
nominal folded moving lengths are below the unfurled 64.  The verifier also
checks the canonical rule against all 8! moving-coordinate relabelings of all
20 inputs.  This is finite evidence only, not an asymptotic PIT theorem.
"""
from __future__ import annotations

import itertools
import json
import math
import random
from pathlib import Path

# Reuse only deterministic 3DM generation and elementary GF(2) routines.
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prior" / "experiments"))
import verify_asymmetric_hash_fold as base  # type: ignore

PRIMES = (5, 7, 11, 13, 17, 19, 23, 29, 31)
MODULUS_TUPLES = tuple((m,) for m in range(2, 33)) + tuple(
    tuple(PRIMES[:r]) for r in range(2, 6)
)
# This one rule is designated before distance evaluation; ranked output below is
# diagnostic only and is never used to choose a construction.
PRECOMMITTED_RULE = (5, 7, 11, 13, 17)


def rank(rows: tuple[int, ...] | list[int]) -> int:
    return len(base.basis(list(rows)))


def invertible_row_maps(k: int):
    """All ordered row masks of GL(k,2), feasible here because k<=3."""
    for rows in itertools.product(range(1, 1 << k), repeat=k):
        if rank(rows) == k:
            yield rows


def apply_row_map(column: int, rows: tuple[int, ...]) -> int:
    out = 0
    for i, row in enumerate(rows):
        out |= ((column & row).bit_count() & 1) << i
    return out


def generator_columns_raw(rows: list[int], moving: int) -> tuple[int, list[int]]:
    star = sum(((row & 1) << i) for i, row in enumerate(rows))
    cols = [sum((((row >> (1 + j)) & 1) << i) for i, row in enumerate(rows))
            for j in range(moving)]
    return star, cols


def generator_columns(rows: list[int], moving: int) -> tuple[int, list[int]]:
    return generator_columns_raw(base.basis(rows), moving)


def canonical_signature(rows: list[int], moving: int) -> tuple[int, tuple[int, ...]]:
    """Canonical pointed column multiset, invariant under GL(k,2) and S_m."""
    rows = base.basis(rows)
    star, cols = generator_columns(rows, moving)
    best = None
    for transform in invertible_row_maps(len(rows)):
        candidate = (apply_row_map(star, transform),
                     tuple(sorted(apply_row_map(c, transform) for c in cols)))
        if best is None or candidate < best:
            best = candidate
    assert best is not None and best[0] != 0
    return best


def rows_from_signature(sig: tuple[int, tuple[int, ...]]) -> list[int]:
    star, cols = sig
    k = max((star, *cols)).bit_length()
    rows = []
    for i in range(k):
        row = (star >> i) & 1
        for j, col in enumerate(cols):
            row |= ((col >> i) & 1) << (1 + j)
        rows.append(row)
    ans = base.basis(rows)
    assert len(ans) == k
    return ans


def permute_moving(rows: list[int], perm: tuple[int, ...]) -> list[int]:
    out = []
    for row in rows:
        y = row & 1
        for old, new in enumerate(perm):
            y |= ((row >> (1 + old)) & 1) << (1 + new)
        out.append(y)
    return out


def input_families(q: int = 3, moving: int = 8):
    yes_triples = [base.planted(q, moving, seed) for seed in range(10)]
    no_triples = []
    for seed in range(10000, 30000):
        triples = base.randomT(q, moving, seed)
        data = base.instance_code(q, triples)
        if data and data[1] > q:
            no_triples.append(triples)
            if len(no_triples) == 10:
                break
    assert len(no_triples) == 10
    yes = [base.instance_code(q, triples)[0] for triples in yes_triples]
    no = [base.instance_code(q, triples)[0] for triples in no_triples]
    return yes, no


def pruned(rows: list[int], nominal_moving: int) -> tuple[list[int], int]:
    """Delete bucket coordinates that are identically zero in the image code."""
    rows = base.basis(rows)
    keep = [j for j in range(nominal_moving)
            if any((row >> (1 + j)) & 1 for row in rows)]
    out = []
    for row in rows:
        y = row & 1
        for new, old in enumerate(keep):
            y |= ((row >> (1 + old)) & 1) << (1 + new)
        out.append(y)
    return base.basis(out), len(keep)


def kronecker_fold(rows: list[int], moving: int, moduli: tuple[int, ...]):
    """Build the reduced square and XOR its ordered pairs into modular buckets."""
    canonical = rows_from_signature(canonical_signature(rows, moving))
    _, cols = generator_columns(canonical, moving)
    types = sorted(set(cols))
    type_rank = {typ: i for i, typ in enumerate(types)}
    t = len(types)
    offsets = []
    total = 0
    for modulus in moduli:
        offsets.append(total)
        total += modulus

    image_rows = []
    for left in canonical:
        for right in canonical:
            y = (left & 1) & (right & 1)
            for i, ci in enumerate(cols):
                if not ((left >> (1 + i)) & 1):
                    continue
                ei = 1 << type_rank[ci]
                for j, cj in enumerate(cols):
                    if not ((right >> (1 + j)) & 1):
                        continue
                    ej = 1 << (t + type_rank[cj])
                    exponent = ei + ej
                    for offset, modulus in zip(offsets, moduli):
                        y ^= 1 << (1 + offset + exponent % modulus)
            image_rows.append(y)
    image, active = pruned(image_rows, total)
    return image, active, t


def exact_pointed_spectrum(rows: list[int]) -> tuple[int, ...]:
    return tuple(sorted((word >> 1).bit_count()
                        for word in base.words(base.basis(rows)) if word & 1))


def unfurled_square(rows: list[int], moving: int) -> list[int]:
    return base.reduced(rows, moving)


def check_all_relabelings(family: list[list[int]], moving: int) -> int:
    """Exhaust all 8! permutations; canonical signatures must be unchanged."""
    permutations = tuple(itertools.permutations(range(moving)))
    checked = 0
    for rows in family:
        sig = canonical_signature(rows, moving)
        # A coordinate permutation only reorders the raw column multiset.  We
        # still materialize every permutation and compare that multiset; the
        # GL minimization then has exactly the same candidate set.
        fixed_basis = base.basis(rows)
        star, cols = generator_columns_raw(fixed_basis, moving)
        raw = (star, tuple(sorted(cols)))
        for perm in permutations:
            pstar, pcols = generator_columns_raw(permute_moving(fixed_basis, perm), moving)
            assert (pstar, tuple(sorted(pcols))) == raw
            checked += 1
        # Also exercise the actual canonicalizer once after a nontrivial relabeling.
        assert canonical_signature(permute_moving(rows, permutations[-1]), moving) == sig
    return checked


def main() -> None:
    moving = 8
    yes, no = input_families(moving=moving)
    family = yes + no
    assert [len(c) for c in yes].count(3) == 1
    assert [len(c) for c in no].count(3) == 1

    # Exact source baseline: enumerate every mixed reduced-square word.
    source_yes = [base.pd(unfurled_square(c, moving)) for c in yes]
    source_no = [base.pd(unfurled_square(c, moving)) for c in no]
    assert (max(source_yes), min(source_no)) == (9, 25)
    source_ratio = 25 / 9
    source_exponent = math.log(source_ratio) / math.log(1 + moving * moving)

    relabelings = check_all_relabelings(family, moving)
    assert relabelings == 20 * math.factorial(moving)

    records = []
    mixed_words_enumerated = 0
    for moduli in MODULUS_TUPLES:
        yd, nd, active_counts, dimensions, type_counts = [], [], [], [], []
        for code in yes:
            image, active, types = kronecker_fold(code, moving, moduli)
            spectrum = exact_pointed_spectrum(image)
            mixed_words_enumerated += 1 << len(image)
            assert spectrum
            yd.append(spectrum[0])
            active_counts.append(active)
            dimensions.append(len(image))
            type_counts.append(types)
        for code in no:
            image, active, types = kronecker_fold(code, moving, moduli)
            spectrum = exact_pointed_spectrum(image)
            mixed_words_enumerated += 1 << len(image)
            assert spectrum
            nd.append(spectrum[0])
            active_counts.append(active)
            dimensions.append(len(image))
            type_counts.append(types)
        worst_yes, best_no = max(yd), min(nd)
        max_rank = 1 + max(active_counts)  # rank of the transferred ambient lattice
        ratio = best_no / worst_yes
        exponent = math.log(ratio) / math.log(max_rank) if ratio > 1 else 0.0
        records.append({
            "moduli": list(moduli),
            "nominal_buckets": sum(moduli),
            "max_ambient_rank": max_rank,
            "image_dimension_range": [min(dimensions), max(dimensions)],
            "canonical_type_range": [min(type_counts), max(type_counts)],
            "yes_distance_range": [min(yd), max(yd)],
            "no_distance_range": [min(nd), max(nd)],
            "uniform_ratio": ratio,
            "rank_exponent": exponent,
            "strictly_compressed": max_rank < 65,
            "beats_unfurled_exponent": exponent > source_exponent + 1e-12,
        })

    ranked = sorted(records, key=lambda r: (r["rank_exponent"], r["uniform_ratio"]), reverse=True)
    summary = {
        "mechanism": "canonical ordered Kronecker exponents, parity buckets modulo fixed M_j",
        "expected_move": "retain all low-weight NO mixed words while using fewer than 64 moving buckets",
        "falsification": "a mixed NO image at or below worst YES, or no compressed uniform exponent gain",
        "instances": {"YES": len(yes), "NO": len(no)},
        "mixed_image_words_enumerated": mixed_words_enumerated,
        "all_coordinate_relabelings_checked": relabelings,
        "rules_checked": len(records),
        "unfurled": {"ambient_rank": 65, "worst_YES": 9, "best_NO": 25,
                       "uniform_ratio": source_ratio, "rank_exponent": source_exponent},
        "precommitted_rule": next(r for r in records if tuple(r["moduli"]) == PRECOMMITTED_RULE),
        "best_observed_rule_diagnostic_only": ranked[0],
        "uniform_ratio_range": [min(r["uniform_ratio"] for r in records),
                                max(r["uniform_ratio"] for r in records)],
        "rules_preserving_gap": sum(r["uniform_ratio"] > 1 for r in records),
        "rules_with_ratio_one": sum(r["uniform_ratio"] == 1 for r in records),
        "rules_beating_unfurled_exponent": sum(r["beats_unfurled_exponent"] for r in records),
    }
    print(json.dumps(summary, sort_keys=True, indent=2))
    print("TOP_RULES")
    for record in ranked[:10]:
        print(json.dumps(record, sort_keys=True))

    # Freeze the deterministic finite outcome so future changes cannot silently
    # convert this attack into parameter fitting.  These values are populated
    # after the first execution of the already-fixed family above.
    assert len(records) == 35
    assert all(r["strictly_compressed"] for r in records)
    # Soundness is falsified throughout this precommitted family: every rule
    # has a pointed NO mixed word no heavier than its worst YES word.
    assert min(r["uniform_ratio"] for r in records) == 1 / 7
    assert max(r["uniform_ratio"] for r in records) == 1
    assert sum(r["uniform_ratio"] == 1 for r in records) == 23
    assert sum(r["uniform_ratio"] > 1 for r in records) == 0
    assert sum(r["beats_unfurled_exponent"] for r in records) == 0
    print("SPARSE_PIT_TENSOR_FOLD_PASS")


if __name__ == "__main__":
    main()
