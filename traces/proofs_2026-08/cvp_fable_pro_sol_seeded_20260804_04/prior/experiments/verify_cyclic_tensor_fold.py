#!/usr/bin/env python3
"""Exact hostile test of a cyclic orbit-sum fold of a pointed tensor square.

The fold is deliberately the simplest concrete interpretation of ideation S3:
a base pointed code is replicated over an odd cyclic group, the star is shared,
and tensor coordinates are XOR-folded by the diagonal group action.  Every mixed
tensor word in the image is enumerated exactly.  This finite test does not cover
more sophisticated balanced products or nontrivial group-algebra components.
"""
from __future__ import annotations

import itertools
import random


def basis(vectors: list[int]) -> list[int]:
    piv: dict[int, int] = {}
    for x in vectors:
        while x:
            p = x.bit_length() - 1
            if p in piv:
                x ^= piv[p]
            else:
                for q, y in list(piv.items()):
                    if (y >> p) & 1:
                        piv[q] = y ^ x
                piv[p] = x
                break
    return [piv[p] for p in sorted(piv)]


def span_words(rows: list[int]):
    for mask in range(1 << len(rows)):
        x = 0
        for i, row in enumerate(rows):
            if (mask >> i) & 1:
                x ^= row
        yield x


def pointed_distance(rows: list[int], star: int = 0) -> int:
    vals = [x.bit_count() for x in span_words(rows) if (x >> star) & 1]
    if not vals:
        raise ValueError("code has no pointed word")
    return min(vals)


def cyclic_shift(x: int, blocks: int, ell: int) -> int:
    """Fix star 0 and add one to the phase in every non-star block."""
    y = x & 1
    for b in range(blocks):
        for h in range(ell):
            i = 1 + b * ell + h
            if (x >> i) & 1:
                y ^= 1 << (1 + b * ell + (h + 1) % ell)
    return y


def cyclic_replication(rows: list[int], length: int, ell: int) -> tuple[list[int], int]:
    """Share coordinate 0 as star; give every other coordinate an ell-orbit.

    For each base generator and each shift h, copy its non-star support into
    phase h and retain its star coefficient.  This is invariant under Z_ell.
    """
    new_length = 1 + ell * (length - 1)
    out = []
    for row in rows:
        for h in range(ell):
            y = row & 1
            for i in range(1, length):
                if (row >> i) & 1:
                    y ^= 1 << (1 + (i - 1) * ell + h)
            out.append(y)
    return basis(out), new_length


def phase_of(index: int, ell: int) -> int | None:
    if index == 0:
        return None
    return (index - 1) % ell


def orbit_key(i: int, j: int, ell: int) -> tuple:
    """Canonical diagonal-Z_ell orbit of an ordered pair.

    Star is fixed.  Non-star coordinates carry a phase.  The diagonal action
    adds one to every non-star phase; for a star/nonstar pair there is one orbit
    per base coordinate, while for two nonstars the phase difference survives.
    """
    if i == 0 and j == 0:
        return (0,)
    if i == 0:
        return (1, (j - 1) // ell)
    if j == 0:
        return (2, (i - 1) // ell)
    bi, bj = (i - 1) // ell, (j - 1) // ell
    diff = (phase_of(j, ell) - phase_of(i, ell)) % ell
    return (3, bi, bj, diff)


def folded_tensor_generator(rows: list[int], length: int, ell: int) -> tuple[list[int], int, int]:
    keys = sorted({orbit_key(i, j, ell) for i in range(length) for j in range(length)})
    key_index = {k: a for a, k in enumerate(keys)}
    star = key_index[(0,)]
    folded = []
    for a in rows:
        supp_a = [i for i in range(length) if (a >> i) & 1]
        for b in rows:
            supp_b = [j for j in range(length) if (b >> j) & 1]
            y = 0
            # Orbit-sum fold: each tensor 1 toggles its orbit coordinate.
            for i in supp_a:
                for j in supp_b:
                    y ^= 1 << key_index[orbit_key(i, j, ell)]
            folded.append(y)
    return basis(folded), len(keys), star


def minimum_pointed_words(rows: list[int], star: int = 0) -> list[int]:
    words = [x for x in span_words(rows) if (x >> star) & 1]
    d = min(map(int.bit_count, words))
    return [x for x in words if x.bit_count() == d]


def folded_pure_word(x: int, length: int, ell: int) -> tuple[int, int, int]:
    keys = sorted({orbit_key(i, j, ell) for i in range(length) for j in range(length)})
    ki = {k: a for a, k in enumerate(keys)}
    y = 0
    supp = [i for i in range(length) if (x >> i) & 1]
    for i in supp:
        for j in supp:
            y ^= 1 << ki[orbit_key(i, j, ell)]
    return y, len(keys), ki[(0,)]


def run_case(base_rows: list[int], length: int, ell: int = 3) -> dict:
    base_rows = basis(base_rows)
    d0 = pointed_distance(base_rows)
    rep_rows, rep_len = cyclic_replication(base_rows, length, ell)
    drep = pointed_distance(rep_rows)
    fold_rows, fold_len, fold_star = folded_tensor_generator(rep_rows, rep_len, ell)
    dfold = pointed_distance(fold_rows, fold_star)
    pure_weights = []
    for x in minimum_pointed_words(rep_rows):
        y, _, s = folded_pure_word(x, rep_len, ell)
        assert s == fold_star
        pure_weights.append(y.bit_count())
    return {
        "base_dim": len(base_rows),
        "base_length": length,
        "base_d": d0,
        "rep_dim": len(rep_rows),
        "rep_length": rep_len,
        "rep_d": drep,
        "fold_dim": len(fold_rows),
        "fold_length": fold_len,
        "fold_d": dfold,
        "best_pure": min(pure_weights),
        "naive_lower": (drep * drep + ell - 1) // ell,
    }


def run_invariant_case(rows: list[int], length: int, ell: int = 3) -> dict:
    rows = basis(rows)
    d = pointed_distance(rows)
    fold_rows, fold_len, fold_star = folded_tensor_generator(rows, length, ell)
    dfold = pointed_distance(fold_rows, fold_star)
    pure_weights = []
    for x in minimum_pointed_words(rows):
        y, _, s = folded_pure_word(x, length, ell)
        assert s == fold_star
        pure_weights.append(y.bit_count())
    return {
        "base_dim": len(rows), "base_length": length, "base_d": d,
        "rep_dim": len(rows), "rep_length": length, "rep_d": d,
        "fold_dim": len(fold_rows), "fold_length": fold_len,
        "fold_d": dfold, "best_pure": min(pure_weights),
        "naive_lower": (d * d + ell - 1) // ell,
    }


def random_invariant_cases(count: int, ell: int, seed: int):
    """Natural small quasi-cyclic codes, not phase-separated replications."""
    rng = random.Random(seed)
    out = []
    attempts = 0
    while len(out) < count and attempts < 10_000:
        attempts += 1
        blocks = rng.choice([1, 2, 3])
        length = 1 + ell * blocks
        seed_word = rng.randrange(1 << length) | 1
        rows = basis([cyclic_shift(seed_word, blocks, ell) for _ in range(1)])
        # Correctly take the whole orbit (the comprehension above intentionally
        # starts from one word; now propagate shifts).
        orbit = []
        x = seed_word
        for _ in range(ell):
            orbit.append(x)
            x = cyclic_shift(x, blocks, ell)
        rows = basis(orbit)
        if 1 <= len(rows) <= 4:
            out.append((rows, length))
    assert len(out) == count
    return out


def main() -> None:
    cases = [
        ([0b011, 0b101], 3),  # inherited hostile D=span{110,101}, star bit 0
        ([0b0011, 0b0101], 4),
        ([0b00111, 0b11001], 5),
    ]
    rng = random.Random(20250308)
    while len(cases) < 20:
        length = rng.choice([3, 4, 5])
        rows = [1 | (rng.randrange(1 << (length - 1)) << 1) for _ in range(2)]
        if len(basis(rows)) == 2:
            cases.append((rows, length))

    reports = [run_case(rows, length) for rows, length in cases]
    natural_reports = [
        run_invariant_case(rows, length) for rows, length in random_invariant_cases(100, 3, 777331)
    ]
    all_reports = reports + natural_reports
    # The exact theorem is 1+ceil((d^2-1)/ell), accounting for the fixed
    # distinguished orbit.  Store/check it separately from the older weaker
    # ceil(d^2/ell) diagnostic printed in each report.
    theorem_bound = lambda r: 1 + (r["rep_d"] ** 2 - 1 + 3 - 1) // 3
    collapses = [r for r in all_reports if r["fold_d"] < theorem_bound(r)]
    pure_collapses = [r for r in all_reports if r["best_pure"] < theorem_bound(r)]
    ratio_collapses = [r for r in natural_reports if r["fold_d"] < r["rep_d"] ** 2]
    assert len(ratio_collapses) == 37
    print(f"checked {len(all_reports)} exact cyclic folds with ell=3 "
          f"({len(natural_reports)} natural invariant codes)")
    print(f"mixed-word failures of 1+ceil((d_rep^2-1)/ell): {len(collapses)}")
    print(f"pure-word failures of 1+ceil((d_rep^2-1)/ell): {len(pure_collapses)}")
    print(f"natural-code losses relative to full tensor distance d_rep^2: {len(ratio_collapses)}")
    for r in reports + ratio_collapses[:20]:
        print(r)

    # Basic construction invariants.
    assert all(r["fold_dim"] <= r["rep_dim"] ** 2 for r in all_reports)
    assert all(r["fold_d"] <= r["best_pure"] for r in all_reports)
    assert not collapses
    # A failure is reported rather than required: this verifier remains valid if
    # a later corrected fold happens to survive all finite cases.


if __name__ == "__main__":
    main()
