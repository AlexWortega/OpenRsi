#!/usr/bin/env python3
"""Exact finite attack on BMT 3DM incidence + local-exchange quotient.

This does not prove an asymptotic claim.  It enumerates every binary selection for
small 3DM dictionaries, verifies the BMT counting lemma, constructs the span B
of all 2<->2 and 3<->3 exact-packing exchanges, and checks whether illegal odd
covers share the quotient class of a perfect matching.
"""
from __future__ import annotations

import itertools
import random
from dataclasses import dataclass


def wt(x: int) -> int:
    return x.bit_count()


class BinarySpan:
    def __init__(self, vectors=()):
        self.pivots: dict[int, int] = {}
        for x in vectors:
            self.add(x)

    def reduce(self, x: int) -> int:
        while x:
            p = x.bit_length() - 1
            y = self.pivots.get(p)
            if y is None:
                return x
            x ^= y
        return 0

    def add(self, x: int) -> bool:
        x = self.reduce(x)
        if not x:
            return False
        p = x.bit_length() - 1
        # Reduced-echelon cleanup makes canonical class labels reproducible.
        for q, y in list(self.pivots.items()):
            if (y >> p) & 1:
                self.pivots[q] = y ^ x
        self.pivots[p] = x
        return True

    def contains(self, x: int) -> bool:
        return self.reduce(x) == 0

    @property
    def rank(self) -> int:
        return len(self.pivots)


@dataclass
class Report:
    q: int
    m: int
    fiber_size: int
    matchings: int
    minimum: int
    exchange_rank: int
    quotient_distance: int | None
    legal_differences_contained: bool
    illegal_in_exchange_class: int
    lightest_illegal_in_exchange_class: int | None
    legal_span_rank: int
    illegal_in_minimal_legal_affine_span: int
    lightest_illegal_in_minimal_legal_affine_span: int | None


def incidence_mask(q: int, triple: tuple[int, int, int]) -> int:
    return (1 << triple[0]) | (1 << (q + triple[1])) | (1 << (2 * q + triple[2]))


def xor_columns(columns: list[int], selection: int) -> int:
    ans = 0
    while selection:
        bit = selection & -selection
        ans ^= columns[bit.bit_length() - 1]
        selection ^= bit
    return ans


def is_exact_matching(q: int, triples: list[tuple[int, int, int]], selection: int) -> bool:
    if wt(selection) != q:
        return False
    seen = [set(), set(), set()]
    for j, u in enumerate(triples):
        if (selection >> j) & 1:
            for part in range(3):
                if u[part] in seen[part]:
                    return False
                seen[part].add(u[part])
    return all(len(s) == q for s in seen)


def packing_key(triples: list[tuple[int, int, int]], inds: tuple[int, ...]) -> tuple[tuple[int, ...], ...] | None:
    parts = tuple(tuple(sorted(triples[j][p] for j in inds)) for p in range(3))
    if any(len(set(v)) != len(inds) for v in parts):
        return None
    return parts


def exchange_span(triples: list[tuple[int, int, int]], max_exchange: int = 3) -> BinarySpan:
    B = BinarySpan()
    m = len(triples)
    for r in range(2, max_exchange + 1):
        buckets: dict[tuple[tuple[int, ...], ...], int] = {}
        for inds in itertools.combinations(range(m), r):
            key = packing_key(triples, inds)
            if key is None:
                continue
            vec = sum(1 << j for j in inds)
            if key in buckets:
                B.add(vec ^ buckets[key])
            else:
                buckets[key] = vec
    return B


def analyze(q: int, triples: list[tuple[int, int, int]]) -> Report:
    m = len(triples)
    cols = [incidence_mask(q, u) for u in triples]
    target = (1 << (3 * q)) - 1
    fiber: list[int] = []
    kernel: list[int] = []
    matchings: list[int] = []
    for x in range(1 << m):
        syn = xor_columns(cols, x)
        if syn == 0:
            kernel.append(x)
        if syn == target:
            fiber.append(x)
            if is_exact_matching(q, triples, x):
                matchings.append(x)
    if not fiber:
        raise ValueError("experiment requires a nonempty parity-cover fiber")

    # Exact BMT counting: no fiber word below q; weight q iff perfect matching.
    assert all(wt(x) >= q for x in fiber)
    assert all(is_exact_matching(q, triples, x) == (wt(x) == q) for x in fiber)

    B = exchange_span(triples)
    assert all(xor_columns(cols, z) == 0 for z in B.pivots.values())
    qdist = min((wt(z) for z in kernel if z and not B.contains(z)), default=None)

    contained = True
    illegal_same: list[int] = []
    legal_span = BinarySpan()
    illegal_legal_span: list[int] = []
    if matchings:
        ref = matchings[0]
        contained = all(B.contains(ref ^ y) for y in matchings)
        illegal_same = [x for x in fiber if not is_exact_matching(q, triples, x) and B.contains(x ^ ref)]
        # This is the MINIMAL linear subspace that any quotient must declare
        # cheap if every perfect matching is to share ref's quotient class.
        for y in matchings[1:]:
            legal_span.add(ref ^ y)
        illegal_legal_span = [
            x for x in fiber
            if not is_exact_matching(q, triples, x) and legal_span.contains(x ^ ref)
        ]

    return Report(
        q=q,
        m=m,
        fiber_size=len(fiber),
        matchings=len(matchings),
        minimum=min(map(wt, fiber)),
        exchange_rank=B.rank,
        quotient_distance=qdist,
        legal_differences_contained=contained,
        illegal_in_exchange_class=len(illegal_same),
        lightest_illegal_in_exchange_class=min(map(wt, illegal_same), default=None),
        legal_span_rank=legal_span.rank,
        illegal_in_minimal_legal_affine_span=len(illegal_legal_span),
        lightest_illegal_in_minimal_legal_affine_span=min(map(wt, illegal_legal_span), default=None),
    )


def planted_instance(q: int, m: int, seed: int) -> list[tuple[int, int, int]]:
    rng = random.Random(seed)
    universe = list(itertools.product(range(q), repeat=3))
    planted = [(i, i, i) for i in range(q)]
    rest = [u for u in universe if u not in planted]
    rng.shuffle(rest)
    return planted + rest[: m - q]


def random_instance(q: int, m: int, seed: int) -> list[tuple[int, int, int]]:
    rng = random.Random(seed)
    universe = list(itertools.product(range(q), repeat=3))
    rng.shuffle(universe)
    return universe[:m]


def main() -> None:
    reports: list[tuple[str, int, Report]] = []
    # Planted YES cases are guaranteed to exercise legal-difference quotienting.
    for q, m, seeds in [(3, 13, range(20)), (4, 16, range(30))]:
        for seed in seeds:
            r = analyze(q, planted_instance(q, m, seed))
            reports.append(("YES", seed, r))

    # Keep random cases with parity covers; m=8 has many exact NO fibers while
    # remaining small enough for exhaustive enumeration.
    no_count = 0
    for seed in range(3000):
        triples = random_instance(3, 8, 10_000 + seed)
        try:
            r = analyze(3, triples)
        except ValueError:
            continue
        reports.append(("YES" if r.matchings else "NO", 10_000 + seed, r))
        if not r.matchings:
            no_count += 1
        if no_count >= 20:
            break

    assert reports
    assert no_count >= 5, "deterministic sample unexpectedly found too few NO parity covers"
    assert all(r.minimum == r.q for tag, _, r in reports if tag == "YES")
    assert all(r.minimum >= r.q + 1 for tag, _, r in reports if tag == "NO")

    same_class = [(tag, seed, r) for tag, seed, r in reports if r.illegal_in_exchange_class]
    info_theoretic = [
        (tag, seed, r) for tag, seed, r in reports
        if r.illegal_in_minimal_legal_affine_span
    ]
    print(f"checked {len(reports)} exact instances; NO parity-cover instances={no_count}")
    print(f"instances where an illegal odd cover shares a matching's exchange-B class: {len(same_class)}")
    print("instances where an illegal odd cover lies in the minimal affine span of all matchings: "
          f"{len(info_theoretic)}")
    for tag, seed, r in same_class[:10]:
        print(tag, seed, r)
    print("sample reports:")
    for row in reports[:5] + [x for x in reports if x[0] == "NO"][:5]:
        print(*row)

    # This is a finite diagnostic, not an assertion that the candidate survives.
    # Every arithmetic/counting claim made by the script has been asserted above.


if __name__ == "__main__":
    main()
