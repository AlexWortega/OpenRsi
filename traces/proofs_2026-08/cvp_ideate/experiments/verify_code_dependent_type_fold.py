#!/usr/bin/env python3
"""Exact test of a polynomial-time code-dependent puncture.

For a binary generator G, two coordinates have the same *column type* when
all codewords agree on them.  Equality of column types is basis invariant and
can be found by Gaussian elimination, without computing a nearest word.  For
an integer budget B, retain ceil(m_a/B) representatives of every type of
multiplicity m_a.  Thus every source word of weight w maps to weight w' with

    w/B <= w' <= w/B + (# active column types).

The construction is tested on reduced tensor squares of tiny 3DM syndrome
fibers, against every mixed word.  Selection uses only the code, never the
YES/NO label or a closest word.  Relabeling invariance is checked exactly.
"""
from __future__ import annotations
import random
import verify_asymmetric_hash_fold as base


def canonical_rows(rows: list[int]) -> list[int]:
    return base.basis(rows)


def type_classes(rows: list[int], ncoords: int) -> dict[int, list[int]]:
    """Classes among moving coordinates 1..ncoords; star is not punctured."""
    rows = canonical_rows(rows)
    out: dict[int, list[int]] = {}
    for j in range(ncoords):
        typ = 0
        for i, r in enumerate(rows):
            typ |= ((r >> (1+j)) & 1) << i
        out.setdefault(typ, []).append(j)
    return out


def puncture_by_types(rows: list[int], ncoords: int, budget: int) -> tuple[list[int], list[int]]:
    classes = type_classes(rows, ncoords)
    keep: list[int] = []
    for typ in sorted(classes):
        js = classes[typ]
        count = (len(js) + budget - 1) // budget
        keep.extend(js[:count])
    image = []
    for r in canonical_rows(rows):
        y = r & 1
        for k, j in enumerate(keep):
            if (r >> (1+j)) & 1:
                y |= 1 << (1+k)
        image.append(y)
    return canonical_rows(image), keep


def permute_moving(rows: list[int], perm: list[int]) -> list[int]:
    out = []
    for r in rows:
        y = r & 1
        for old, new in enumerate(perm):
            if (r >> (1+old)) & 1:
                y |= 1 << (1+new)
        out.append(y)
    return canonical_rows(out)


def spectrum(rows: list[int]) -> list[int]:
    return sorted((z >> 1).bit_count() for z in base.words(rows) if z & 1)


def check_rounding_bound(rows: list[int], keep: list[int], ncoords: int, budget: int) -> None:
    classes = type_classes(rows, ncoords)
    src = canonical_rows(rows)
    projected = []
    for r in src:
        y = r & 1
        for k, j in enumerate(keep):
            if (r >> (1+j)) & 1:
                y |= 1 << (1+k)
        projected.append(y)
    for mask in range(1 << len(src)):
        x = y = 0
        for i in range(len(src)):
            if (mask >> i) & 1:
                x ^= src[i]
                y ^= projected[i]
        w, wp = (x >> 1).bit_count(), (y >> 1).bit_count()
        active = 0
        for js in classes.values():
            if (x >> (1+js[0])) & 1:
                active += 1
        assert w <= budget * wp
        assert wp <= w / budget + active


def main() -> None:
    q, m = 3, 8
    yes, no = base.samples(q, m)
    reports = []
    for budget in [1, 2, 3, 4, 8, 16, 64]:
        yd = []
        nd = []
        lengths = []
        type_counts = []
        for label, family, dest in [("YES", yes, yd), ("NO", no, nd)]:
            for idx, code in enumerate(family):
                ncoords = m*m
                image, keep = puncture_by_types(code, ncoords, budget)
                check_rounding_bound(code, keep, ncoords, budget)
                dest.append(base.pd(image))
                lengths.append(1+len(keep))
                type_counts.append(len(type_classes(code, ncoords)))
                # Coordinate relabeling changes representatives but not the image spectrum.
                rng = random.Random(100000*budget + 1000*(label == "NO") + idx)
                perm = list(range(ncoords)); rng.shuffle(perm)
                relabeled = permute_moving(code, perm)
                image2, _ = puncture_by_types(relabeled, ncoords, budget)
                assert spectrum(image2) == spectrum(image)
        Y, N = max(yd), min(nd)
        reports.append((budget, min(lengths), max(lengths), min(type_counts),
                        max(type_counts), min(yd), Y, N, max(nd), N/Y))
    print("B,minL,maxL,minTypes,maxTypes,minY,maxY,minN,maxN,uniformRatio")
    for r in reports:
        print(r)
    # Deterministic finite finding: type puncturing is well-defined and exact,
    # but on this adversarial family no budget improves the unfurled rank exponent.
    import math
    base_exp = math.log(25/9)/math.log(65)
    best_exp = max(math.log(r[-1])/math.log(r[2]) if r[-1] > 1 else 0 for r in reports)
    print({"base_exponent": base_exp, "best_type_puncture_exponent": best_exp})
    assert best_exp <= base_exp + 1e-12
    print("code-dependent column-type puncture checks pass")


if __name__ == "__main__":
    main()
