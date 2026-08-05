#!/usr/bin/env python3
"""Exact finite attack on the surviving two-sided rank-condenser proposal.

Freeze F8=F2[u]/(u^3+u+1), canonical lexicographic triple order, and five
2-by-m / m-by-2 generalized Vandermonde blocks.  For block s=0,...,4,

  A_s[r,j] = x_j^e, e in (0,s+1),
  B_s[j,c] = x_j^f, f in (0,2s+1),

where x_j is field element j for m=8 (and j mod 8 for the m=9 holonomy
attack).  A reduced-square matrix W maps to all 20 F8 entries of A_s W B_s,
expanded in the fixed binary basis (1,u,u^2), for 60 nominal moving bits.

Every mixed image word is enumerated on ten YES, 200 NO, twenty affine-closure,
all-eight, and holonomy dictionaries.  Each image is converted to an explicit
binary parity-check fiber and exact-transfer rank.  This is finite evidence.
"""
from __future__ import annotations

import itertools
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prior" / "experiments"))
import verify_asymmetric_hash_fold as base  # type: ignore

BLOCKS = 5
NOMINAL_BITS = BLOCKS * 2 * 2 * 3
BLOCK_EXPONENTS = tuple(((0, s + 1), (0, 2*s + 1)) for s in range(BLOCKS))


def f8_mul(x: int, y: int) -> int:
    """Multiply modulo u^3+u+1 (binary polynomial 0b1011)."""
    product = 0
    a, b = x, y
    while b:
        if b & 1:
            product ^= a
        b >>= 1
        a <<= 1
    for degree in range(5, 2, -1):
        if (product >> degree) & 1:
            product ^= 0b1011 << (degree - 3)
    return product & 7


def f8_pow(x: int, exponent: int) -> int:
    result = 1
    for _ in range(exponent):
        result = f8_mul(result, x)
    return result


def condenser_blocks(m: int):
    nodes = [j % 8 for j in range(m)]
    blocks = []
    for left_exponents, right_exponents in BLOCK_EXPONENTS:
        left = tuple(tuple(f8_pow(node, exponent) for node in nodes)
                     for exponent in left_exponents)
        right = tuple(tuple(f8_pow(node, exponent) for node in nodes)
                      for exponent in right_exponents)
        # right stores the two columns of the fixed m-by-2 matrix B_s.
        blocks.append((left, right))
    return tuple(blocks)


# Serialize and freeze the exact m=8 matrices before any instance distances.
FROZEN_M8_BLOCKS = condenser_blocks(8)
assert NOMINAL_BITS == 60
assert len(FROZEN_M8_BLOCKS) == 5
assert f8_mul(2, 4) == 3  # u^3 = u+1


def incidence_fiber(q: int, triples: list[tuple[int, int, int]]) -> list[int]:
    triples = sorted(triples)
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


def pointed_code(q: int, triples: list[tuple[int, int,int]]):
    triples = sorted(triples)
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


def rref(rows: list[int], n: int):
    rows = [row & ((1 << n)-1) for row in rows if row]
    pivots, rank = [], 0
    for column in range(n):
        pivot = next((i for i in range(rank, len(rows)) if (rows[i] >> column) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> column) & 1):
                rows[i] ^= rows[rank]
        pivots.append(column)
        rank += 1
        if rank == len(rows):
            break
    return rows[:rank], pivots


def nullspace(rows: list[int], n: int):
    equations, pivots = rref(rows, n)
    answer = []
    for free in (j for j in range(n) if j not in pivots):
        vector = 1 << free
        for row, pivot in zip(equations, pivots):
            if (row & vector).bit_count() & 1:
                vector |= 1 << pivot
        answer.append(vector)
    assert all(not ((h & row).bit_count() & 1) for h in answer for row in rows)
    return answer


def prune_image(rows: list[int]):
    rows = base.basis(rows)
    active = [j for j in range(NOMINAL_BITS)
              if any((row >> (1+j)) & 1 for row in rows)]
    image = []
    for row in rows:
        word = row & 1
        for new, old in enumerate(active):
            word |= ((row >> (1+old)) & 1) << (1+new)
        image.append(word)
    return base.basis(image), active


def explicit_fiber(image: list[int], moving: int):
    pointed = next(row for row in image if row & 1)
    kernel = []
    for row in image:
        zero = row ^ (pointed if row & 1 else 0)
        if zero:
            kernel.append(zero >> 1)
    kernel = base.basis(kernel)
    checks = nullspace(kernel, moving)
    target = sum((((h & (pointed >> 1)).bit_count() & 1) << i) for i,h in enumerate(checks))
    assert len(kernel) + len(checks) == moving
    for row in image:
        syndrome = sum((((h & (row >> 1)).bit_count() & 1) << i) for i,h in enumerate(checks))
        assert syndrome == (target if row & 1 else 0)
    return checks, target


def fold_binary_matrix(matrix_rows: list[int], m: int) -> int:
    """Apply all frozen blocks to an m-by-m binary matrix."""
    output = 0
    bit = 0
    for left, right_columns in condenser_blocks(m):
        for a in range(2):
            for b in range(2):
                value = 0
                for i in range(m):
                    li = left[a][i]
                    if not li:
                        continue
                    row = matrix_rows[i]
                    for j in range(m):
                        if (row >> j) & 1:
                            value ^= f8_mul(li, right_columns[b][j])
                output |= (value & 7) << bit
                bit += 3
    assert bit == NOMINAL_BITS
    return output


def fold_report(q: int, triples: list[tuple[int,int,int]]):
    triples = sorted(triples)
    data = pointed_code(q, triples)
    assert data is not None
    rows, fiber = data
    m = len(triples)
    generators = []
    for left in rows:
        left_support = [i for i in range(m) if (left >> (1+i)) & 1]
        for right in rows:
            matrix = []
            right_bits = sum(((right >> (1+j)) & 1) << j for j in range(m))
            for i in range(m):
                matrix.append(right_bits if i in left_support else 0)
            folded = fold_binary_matrix(matrix, m)
            generators.append(((left & 1) & (right & 1)) | (folded << 1))
    image, active = prune_image(generators)

    pointed_words = []
    for mask in range(1 << len(image)):
        word = 0
        for i,row in enumerate(image):
            if (mask >> i) & 1:
                word ^= row
        if word & 1:
            pointed_words.append((word.bit_count()-1, mask, word))
    assert pointed_words
    minimum = min(pointed_words)
    checks, target = explicit_fiber(image, len(active))

    illegal_costs, legal_costs = [], []
    active_mask = sum(1 << j for j in active)
    for selection in fiber:
        selected = [j for j in range(m) if (selection >> j) & 1]
        row_bits = selection
        matrix = [row_bits if i in selected else 0 for i in range(m)]
        folded = fold_binary_matrix(matrix, m)
        cost = (folded & active_mask).bit_count()
        (legal_costs if selection.bit_count() == q else illegal_costs).append(cost)

    distance = min(x.bit_count() for x in fiber)
    return {
        "base_distance": distance,
        "unfurled_square_distance": distance*distance,
        "source_square_dimension": len(base.reduced(rows,m)),
        "fiber_size": len(fiber),
        "image_dimension": len(image),
        "nominal_pointed_length": 1+NOMINAL_BITS,
        "active_pointed_length": 1+len(active),
        "exact_transfer_rank": len(active),
        "parity_check_rank": len(checks),
        "target": target,
        "folded_distance": minimum[0],
        "minimum_message_mask": minimum[1],
        "minimum_output_word": minimum[2],
        "pointed_kernel": minimum[0] == 0,
        "cheapest_semantic_illegal_pure_square": min(illegal_costs, default=None),
        "legal_pure_square_range": None if not legal_costs else [min(legal_costs),max(legal_costs)],
        "mixed_words_enumerated": 1 << len(image),
    }


def families(no_count=200):
    yes=[base.planted(3,8,seed) for seed in range(10)]
    no=[]
    for seed in range(10000,100000):
        triples=base.randomT(3,8,seed); fiber=incidence_fiber(3,triples)
        if fiber and min(x.bit_count() for x in fiber)>3:
            assert min(x.bit_count() for x in fiber)==5
            no.append(triples)
            if len(no)==no_count:break
    assert len(no)==no_count
    return yes,no


def span_contains(rows,word):
    for row in sorted(base.basis(rows),key=int.bit_length,reverse=True):
        if word.bit_length()==row.bit_length():word^=row
    return word==0


def closure_witnesses(count=20):
    out=[]
    for seed in range(100000):
        triples=base.randomT(3,8,seed); fiber=incidence_fiber(3,triples)
        matches=[x for x in fiber if x.bit_count()==3]
        if not matches:continue
        ref=matches[0]; diffs=[x^ref for x in matches[1:]]
        bad=[x for x in fiber if x.bit_count()!=3 and span_contains(diffs,x^ref)]
        if bad:
            out.append((seed,triples,bad))
            if len(out)==count:break
    assert len(out)==count
    return out


def all_eight():return 2,list(itertools.product(range(2),repeat=3))
def holonomy():
    q=3; triples=([(i,i,i) for i in range(q)]+[(i,(i+1)%q,(i+2)%q) for i in range(q)]+[(i,(i+2)%q,(i+1)%q) for i in range(q)])
    assert sorted(x.bit_count() for x in incidence_fiber(q,triples))==[3,3,3,9]
    return q,triples


def check_relabel(q,triples,exhaustive):
    canonical=sorted(triples)
    permutations=itertools.permutations(range(len(triples))) if exhaustive else [tuple(reversed(range(len(triples))))]
    checked=0
    for permutation in permutations:
        assert sorted(triples[i] for i in permutation)==canonical
        checked+=1
    original=fold_report(q,triples); reverse=fold_report(q,list(reversed(triples)))
    for key in ("image_dimension","active_pointed_length","exact_transfer_rank","folded_distance","pointed_kernel","cheapest_semantic_illegal_pure_square","mixed_words_enumerated"):
        assert original[key]==reverse[key]
    return checked


def compact(r):
    return {k:r[k] for k in ("base_distance","unfurled_square_distance","source_square_dimension","fiber_size","image_dimension","nominal_pointed_length","active_pointed_length","exact_transfer_rank","parity_check_rank","folded_distance","pointed_kernel","cheapest_semantic_illegal_pure_square","legal_pure_square_range","mixed_words_enumerated")}


def serialized_blocks():
    return [{"A":[list(row) for row in left],
             "B_columns":[list(column) for column in right]}
            for left,right in FROZEN_M8_BLOCKS]


def main():
    yes,no=families(); closure=closure_witnesses(); q8,eight=all_eight(); qh,hol=holonomy()
    yr=[fold_report(3,t) for t in yes]; nr=[fold_report(3,t) for t in no]
    cr=[(seed,fold_report(3,t),bad) for seed,t,bad in closure]
    er=fold_report(q8,eight); hr=fold_report(qh,hol)

    worst=max(r["folded_distance"] for r in yr); best=min(r["folded_distance"] for r in nr)
    maxrank=max(r["exact_transfer_rank"] for r in yr+nr)
    ratio=best/worst if worst else 0.0
    exponent=math.log(ratio)/math.log(maxrank) if ratio>1 and maxrank>1 else 0.0
    baseline=math.log(25/9)/math.log(65)
    hostile=[r["cheapest_semantic_illegal_pure_square"] for _,r,_ in cr]+[er["cheapest_semantic_illegal_pure_square"],hr["cheapest_semantic_illegal_pure_square"]]
    assert all(x is not None for x in hostile)

    relabel=0
    for t in yes+no[:10]+[eight]:relabel+=check_relabel(2 if t is eight else 3,t,True)
    relabel+=check_relabel(qh,hol,False)
    for t in no[10:]+[x[1] for x in closure]:relabel+=check_relabel(3,t,False)
    assert relabel==21*math.factorial(8)+1+190+len(closure)

    all_reports=yr+nr+[er,hr]+[r for _,r,_ in cr]
    success=(not any(r["pointed_kernel"] for r in all_reports) and best>worst and exponent>baseline and min(hostile)>worst)
    summary={
      "mechanism":"five frozen two-sided generalized-Vandermonde blocks over F8",
      "expected_move":"preserve many dense slices of every NO mixed matrix while rank-one YES squares stay sparse",
      "falsification":"pointed kernel, NO not above worst YES, hostile illegal cost not above worst YES, or exponent not above baseline",
      "field":{"basis":["1","u","u^2"],"modulus":"u^3+u+1"},
      "block_exponents":[[list(a),list(b)] for a,b in BLOCK_EXPONENTS],
      "frozen_m8_blocks":serialized_blocks(),
      "instances":{"YES_q3_m8":10,"NO_q3_m8":200,"affine_closure_q3_m8":20,"all_eight_q2_m8":1,"holonomy_q3_m9":1},
      "unfurled":{"worst_YES":9,"best_NO":25,"exact_transfer_rank":64,"rank_exponent":baseline},
      "folded":{"worst_YES":worst,"best_NO":best,"uniform_ratio":ratio,"max_exact_transfer_rank":maxrank,"rank_exponent":exponent,"YES_distance_range":[min(r["folded_distance"] for r in yr),worst],"NO_distance_range":[best,max(r["folded_distance"] for r in nr)],"YES_pointed_kernels":sum(r["pointed_kernel"] for r in yr),"NO_pointed_kernels":sum(r["pointed_kernel"] for r in nr)},
      "all_eight":compact(er),"holonomy":compact(hr),
      "affine_closure":{"seeds":[s for s,_,_ in cr],"distance_range":[min(r["folded_distance"] for _,r,_ in cr),max(r["folded_distance"] for _,r,_ in cr)],"semantic_illegal_cost_range":[min(r["cheapest_semantic_illegal_pure_square"] for _,r,_ in cr),max(r["cheapest_semantic_illegal_pure_square"] for _,r,_ in cr)],"pointed_kernels":sum(r["pointed_kernel"] for _,r,_ in cr)},
      "mixed_words_enumerated":sum(r["mixed_words_enumerated"] for r in all_reports),
      "coordinate_relabelings_checked":relabel,"primary_success":success}
    print(json.dumps(summary,indent=2,sort_keys=True))
    # Freeze the finite failure of the precommitted five-block family.
    assert (worst, best, maxrank) == (31, 6, 48)
    assert [min(r["folded_distance"] for r in yr), worst] == [13, 31]
    assert [best, max(r["folded_distance"] for r in nr)] == [6, 33]
    assert not any(r["pointed_kernel"] for r in all_reports)
    assert (er["folded_distance"], er["cheapest_semantic_illegal_pure_square"]) == (2, 2)
    assert (hr["folded_distance"], hr["cheapest_semantic_illegal_pure_square"]) == (6, 6)
    assert not success
    print("F8_TWO_SIDED_CONDENSER_PASS")

if __name__=="__main__":main()
