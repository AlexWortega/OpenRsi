#!/usr/bin/env python3
"""Finite exact attack on Pro 2's quadratic-character switch mark.

The surviving proposal replaces a common linear syndrome by the four
constant-radius words

    c(a,b) = (1, (-1)^a, (-1)^b, (-1)^(ab)).

This verifier freezes exactly that local orbit, a one-hot state-selector
normalization, and the standard binary Kannan anchor.  Exhaustive search of
{-1,0,1}^4 finds three support-three normalized malformed selectors whose
images are new sign words on the same sphere.  For example,

    -c(0,0) + c(0,1) + c(1,0) = (1,-1,-1,1).

Thus the old four-state mixed derivative is indeed nonzero, but equal radius
introduces a shorter signed-affine ghost.  Its normalization residual is zero,
its mark squared norm is the legal value 4, and its anchor energy is 12 versus
4.  The script also checks mark scales 0..64 after choosing, for each scale,
the least integral normalization scale that makes local DROP cost at least
17 times legal energy.  The ghost remains below that threshold in every one
of those 65 finite cases.

This is finite evidence against this frozen local quadratic-character
realization only.  A larger brick could add explicitly specified rows that
charge these ghosts; no full compiler, all-size obstruction, or asymptotic
claim is proved here.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import product
import json

STATES = tuple(product((0, 1), repeat=2))
COEFFICIENT_BOX = (-1, 0, 1)
ADVERSE_FACTOR_SQ = 17
MAX_MARK_SCALE = 64
MAX_NORMALIZATION_SEARCH = 1024


def character_word(a: int, b: int) -> tuple[int, int, int, int]:
    return (1, 1 if a == 0 else -1, 1 if b == 0 else -1, 1 if a * b == 0 else -1)


CODEWORDS = tuple(character_word(a, b) for a, b in STATES)
HONEST_SELECTORS = tuple(
    tuple(int(i == j) for i in range(4)) for j in range(4)
)


def image(selector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sum(selector[j] * CODEWORDS[j][i] for j in range(4))
        for i in range(4)
    )


def squared_norm(vector: tuple[int, ...]) -> int:
    return sum(value * value for value in vector)


def anchor_energy(selector: tuple[int, ...]) -> int:
    # Squared distance from the half-integral binary anchor after clearing 2.
    return sum((2 * value - 1) ** 2 for value in selector)


def objective(selector: tuple[int, ...], mark_scale: int, normalization_scale: int) -> int:
    return (
        anchor_energy(selector)
        + mark_scale * mark_scale * squared_norm(image(selector))
        + normalization_scale * normalization_scale * (sum(selector) - 1) ** 2
    )


# The proposal's advertised escape is real: its old mixed derivative is not 0.
MIXED_DERIVATIVE = tuple(
    CODEWORDS[0][i] - CODEWORDS[1][i] - CODEWORDS[2][i] + CODEWORDS[3][i]
    for i in range(4)
)
assert MIXED_DERIVATIVE == (0, 0, 0, -2)

# All four honest words lie on the same standard Euclidean sphere.
assert {squared_norm(word) for word in CODEWORDS} == {4}
assert all(sum(selector) == 1 for selector in HONEST_SELECTORS)
assert tuple(image(selector) for selector in HONEST_SELECTORS) == CODEWORDS

# Complete exact low-weight search in the local signed coefficient box.
MALFORMED_NORMALIZED = []
for selector in product(COEFFICIENT_BOX, repeat=4):
    if sum(selector) != 1 or selector in HONEST_SELECTORS:
        continue
    MALFORMED_NORMALIZED.append({
        "selector": selector,
        "support": sum(value != 0 for value in selector),
        "image": image(selector),
        "mark_norm_sq": squared_norm(image(selector)),
        "anchor_energy": anchor_energy(selector),
    })

assert len(MALFORMED_NORMALIZED) == 12
MIN_SUPPORT = min(record["support"] for record in MALFORMED_NORMALIZED)
assert MIN_SUPPORT == 3
EQUAL_RADIUS_GHOSTS = tuple(
    record for record in MALFORMED_NORMALIZED
    if record["mark_norm_sq"] == 4
)
assert len(EQUAL_RADIUS_GHOSTS) == 3
assert {record["selector"] for record in EQUAL_RADIUS_GHOSTS} == {
    (-1, 1, 1, 0),
    (1, -1, 0, 1),
    (1, 0, -1, 1),
}
assert {record["anchor_energy"] for record in EQUAL_RADIUS_GHOSTS} == {12}
assert {record["image"] for record in EQUAL_RADIUS_GHOSTS} == {
    (1, -1, -1, 1),
    (1, -1, 1, -1),
    (1, 1, -1, -1),
}

# Tune normalization separately at each tested mark scale so local DROP clears
# the preregistered 17E gate.  The exactly normalized ghost is unaffected.
SCALE_AUDIT = []
for mark_scale in range(MAX_MARK_SCALE + 1):
    legal_energies = {
        objective(selector, mark_scale, 0) for selector in HONEST_SELECTORS
    }
    assert len(legal_energies) == 1
    legal_energy = legal_energies.pop()
    assert legal_energy == 4 + 4 * mark_scale * mark_scale

    normalization_scale = next(
        scale
        for scale in range(MAX_NORMALIZATION_SEARCH + 1)
        if objective((0, 0, 0, 0), mark_scale, scale)
        >= ADVERSE_FACTOR_SQ * legal_energy
    )
    drop_energy = objective((0, 0, 0, 0), mark_scale, normalization_scale)
    attack_records = []
    for record in MALFORMED_NORMALIZED:
        selector = record["selector"]
        attack_records.append((objective(selector, mark_scale, normalization_scale), selector))
    attack_energy, _ = min(attack_records)
    attack_selector = EQUAL_RADIUS_GHOSTS[0]["selector"]
    ghost_energy = objective(attack_selector, mark_scale, normalization_scale)
    assert ghost_energy == 12 + 4 * mark_scale * mark_scale
    assert attack_energy == ghost_energy
    assert drop_energy >= ADVERSE_FACTOR_SQ * legal_energy
    assert ghost_energy < ADVERSE_FACTOR_SQ * legal_energy
    SCALE_AUDIT.append({
        "mark_scale": mark_scale,
        "normalization_scale": normalization_scale,
        "legal_energy": legal_energy,
        "drop_energy": drop_energy,
        "attack_energy": ghost_energy,
        "attack_selector": attack_selector,
    })

SPECIFICATION = {
    "states": STATES,
    "codewords": CODEWORDS,
    "coefficient_box": COEFFICIENT_BOX,
    "adverse_factor_sq": ADVERSE_FACTOR_SQ,
    "max_mark_scale": MAX_MARK_SCALE,
    "max_normalization_search": MAX_NORMALIZATION_SEARCH,
}
SPECIFICATION_SHA256 = sha256(json.dumps(
    SPECIFICATION, sort_keys=True, separators=(",", ":")
).encode("ascii")).hexdigest()
EXPECTED_SPECIFICATION_SHA256 = "de0ffc8795bd916e1a71fb375cf07155cf59e67b3b0cf6d66a9be8685ba3cedf"


def main() -> None:
    assert SPECIFICATION_SHA256 == EXPECTED_SPECIFICATION_SHA256
    representative = EQUAL_RADIUS_GHOSTS[0]
    print(json.dumps({
        "selected_surviving_proposal": "Pro 2 quadratic-character equal-radius switch encoding",
        "causal_mechanism": (
            "the quadratic coordinate makes the old four-state mixed derivative nonzero "
            "while keeping all honest switch words on one Euclidean sphere"
        ),
        "expected_frontier_move": (
            "replace common-fibre linear syndromes by a cospherical marked orbit that "
            "can be transported by color-preserving signed permutations"
        ),
        "falsification_condition": (
            "a normalized short signed selector combination maps to a non-honest word "
            "on the same sphere and stays below the 17-times-legal energy gate"
        ),
        "specification_sha256": SPECIFICATION_SHA256,
        "mixed_derivative": MIXED_DERIVATIVE,
        "signed_candidates_searched": len(COEFFICIENT_BOX) ** 4,
        "normalized_malformed_candidates": len(MALFORMED_NORMALIZED),
        "minimum_malformed_support": MIN_SUPPORT,
        "equal_radius_ghosts": len(EQUAL_RADIUS_GHOSTS),
        "representative_ghost": representative,
        "mark_scales_checked": [0, MAX_MARK_SCALE],
        "normalization_rule": "least integer scale making local DROP energy >= 17*legal energy",
        "scale_cases_checked": len(SCALE_AUDIT),
        "maximum_attack_to_legal_ratio": max(
            record["attack_energy"] / record["legal_energy"] for record in SCALE_AUDIT
        ),
        "largest_normalization_scale_used": max(
            record["normalization_scale"] for record in SCALE_AUDIT
        ),
        "finding": (
            "all 65 tested mark scales retain a support-three equal-radius ghost after "
            "normalization is tuned to clear local DROP"
        ),
        "scope": (
            "finite kill of the frozen local quadratic-character objective only; "
            "unspecified extra rows in a full brick are not refuted"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
