#!/usr/bin/env python3
"""Exact construction attempt: cyclic closure of a 3DM pointed code.

Embed the m triple-selection coordinates injectively into Z_ell, adjoin the
shared star, and close every kernel generator and one affine-fiber generator
under cyclic shifts.  This installs a free symmetry WITHOUT ell disjoint copies
or multiplying the planted witness weight.  We then apply the reduced orbit
fold and enumerate every mixed image word.

The construction is falsifiable: cyclic closure may create short pointed words
and erase the YES/NO distinction.  We test planted YES and exact NO odd-cover
instances under deterministic and randomized coordinate embeddings.
"""
from __future__ import annotations

import itertools
import random
from collections import Counter


def basis(rows: list[int]) -> list[int]:
    piv: dict[int, int] = {}
    for z in rows:
        while z:
            p = z.bit_length() - 1
            if p in piv:
                z ^= piv[p]
            else:
                for q, y in list(piv.items()):
                    if (y >> p) & 1:
                        piv[q] = y ^ z
                piv[p] = z
                break
    return [piv[p] for p in sorted(piv)]


def words(rows: list[int]):
    for mask in range(1 << len(rows)):
        z = 0
        for i, r in enumerate(rows):
            if (mask >> i) & 1:
                z ^= r
        yield z


def pointed_moving_distance(rows: list[int]) -> int:
    vals = [(z >> 1).bit_count() for z in words(rows) if z & 1]
    if not vals:
        raise ValueError("no pointed word")
    return min(vals)


def syndrome(q: int, triple: tuple[int, int, int]) -> int:
    return (1 << triple[0]) | (1 << (q + triple[1])) | (1 << (2*q + triple[2]))


def fiber_code(q: int, triples: list[tuple[int, int, int]]):
    cols = [syndrome(q, u) for u in triples]
    target = (1 << (3*q)) - 1
    ker, fib = [], []
    for mask in range(1 << len(cols)):
        syn = 0
        for j, c in enumerate(cols):
            if (mask >> j) & 1:
                syn ^= c
        if syn == 0:
            ker.append(mask)
        if syn == target:
            fib.append(mask)
    if not fib:
        return None
    return basis(ker), min(fib, key=int.bit_count), min(map(int.bit_count, fib))


def rotate_moving(z: int, ell: int) -> int:
    star = z & 1
    m = z >> 1
    m = ((m << 1) & ((1 << ell) - 1)) | (m >> (ell - 1))
    return star | (m << 1)


def embed(mask: int, positions: tuple[int, ...]) -> int:
    z = 0
    for j, p in enumerate(positions):
        if (mask >> j) & 1:
            z ^= 1 << (1 + p)
    return z


def cyclic_closure(q: int, triples, ell: int, positions: tuple[int, ...]):
    data = fiber_code(q, triples)
    if data is None:
        return None
    ker, point, original_d = data
    seeds = [embed(z, positions) for z in ker]
    seeds.append(1 | embed(point, positions))
    rows = []
    for seed in seeds:
        z = seed
        for _ in range(ell):
            rows.append(z)
            z = rotate_moving(z, ell)
    rows = basis(rows)
    return rows, original_d


def reduced_fold(rows: list[int], ell: int) -> list[int]:
    # One free moving orbit: folded coordinate is phase difference.
    out = []
    for a in rows:
        for b in rows:
            z = (a & 1) & (b & 1)
            for i in range(ell):
                if not ((a >> (1+i)) & 1):
                    continue
                for j in range(ell):
                    if (b >> (1+j)) & 1:
                        z ^= 1 << (1 + (j-i) % ell)
            out.append(z)
    return basis(out)


def planted(q: int, m: int, seed: int):
    rng = random.Random(seed)
    diag = [(i, i, i) for i in range(q)]
    rest = [u for u in itertools.product(range(q), repeat=3) if u not in diag]
    rng.shuffle(rest)
    return diag + rest[:m-q]


def random_instance(q: int, m: int, seed: int):
    rng = random.Random(seed)
    all_t = list(itertools.product(range(q), repeat=3))
    rng.shuffle(all_t)
    return all_t[:m]


def collect_instances(q: int, m: int, need_yes: int, need_no: int):
    yes = [("planted", s, planted(q, m, s)) for s in range(need_yes)]
    no = []
    for s in range(10000, 20000):
        T = random_instance(q, m, s)
        data = fiber_code(q, T)
        if data is not None and data[2] > q:
            no.append(("NO", s, T))
            if len(no) == need_no:
                break
    assert len(no) == need_no
    return yes + no


def main() -> None:
    q, m, ell = 3, 8, 11
    instances = collect_instances(q, m, 20, 20)
    rng = random.Random(73021)
    reports = []
    for label, seed, triples in instances:
        embeddings = [tuple(range(m))]
        for _ in range(9):
            embeddings.append(tuple(rng.sample(range(ell), m)))
        for ei, pos in enumerate(embeddings):
            result = cyclic_closure(q, triples, ell, pos)
            assert result is not None
            rows, original_d = result
            # Exact enumeration is bounded by ell+1 dimensions.
            assert len(rows) <= ell + 1
            d = pointed_moving_distance(rows)
            folded = reduced_fold(rows, ell)
            dp = pointed_moving_distance(folded)
            lower = (d*d + ell - 1) // ell
            assert dp >= lower
            reports.append({
                "case": "YES" if label == "planted" else "NO",
                "seed": seed, "embedding": ei, "original_d": original_d,
                "closure_dim": len(rows), "closure_d": d,
                "fold_dim": len(folded), "fold_d": dp, "lower": lower,
            })

    yes = [r for r in reports if r["case"] == "YES"]
    no = [r for r in reports if r["case"] == "NO"]
    distribution = Counter((r["case"], r["original_d"], r["closure_d"], r["fold_d"])
                           for r in reports)
    print(f"checked {len(reports)} exact cyclic-closure assemblies")
    print("distribution (case, original_d, closure_d, fold_d): count")
    for k, v in sorted(distribution.items()):
        print(k, v)
    best_yes = min(r["fold_d"] for r in yes)
    best_no = min(r["fold_d"] for r in no)
    print({"best_YES_fold": best_yes, "best_NO_fold": best_no,
           "NO/YES_using_uniform_best_thresholds": best_no / best_yes})
    # Soundness graveyard diagnostic: count transformed NO instances that have
    # a pointed word no heavier than some transformed YES witness.
    max_yes = max(r["fold_d"] for r in yes)
    cheated_no = sum(r["fold_d"] <= max_yes for r in no)
    print({"max_YES_fold": max_yes, "NO_at_or_below_max_YES": cheated_no,
           "NO_total": len(no)})
    assert len(reports) == 400
    assert set(distribution) == {("YES",3,1,1),("NO",5,1,1)}
    assert all(v==200 for v in distribution.values())
    assert cheated_no == len(no) == 200


if __name__ == "__main__":
    main()
