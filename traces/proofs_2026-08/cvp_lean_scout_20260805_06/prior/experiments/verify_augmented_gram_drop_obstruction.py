#!/usr/bin/env python3
"""Generation-8 exact DROP obstruction for the repaired free-Gram family.

Only repaired Fable proposal 3 survives cross-review.  The prescribed bounded
family has D=8 coefficient columns, canonical one-hot selectors for the four
legal NAND words, four zero-port auxiliary columns, and an extended rational
Gram

    H = [[Q,-h],[-h^T,s]]

whose entries have absolute value at most 64.  Every legal selector is required
to have squared energy 64, and every adverse state must cost at least
(65/64)*64 = 65.

The unrestricted coefficient vector z=0 is already fatal.  Its emitted port is
000 because the port map is linear and every auxiliary has zero port.  NAND
rejects 000, so this is a FALSE/DROP state.  Its exact energy is

    [0;1]^T H [0;1] = s <= 64,

contradicting the required lower bound 65.  Positive semidefiniteness or strict
diagonal dominance only gives a lower bound on s and cannot repair this upper
bound.  Thus no Gram in the frozen normalized family reaches the first NAND
soundness gate; COPY and transfer tables are not authorized.

This rejects only the exact entry-bound/legal-radius normalization prescribed
by the review.  It is not a no-go theorem for rescaled or differently centered
augmented tiles.
"""

from __future__ import annotations

from fractions import Fraction
import json

D = 8
EXTENDED_DIMENSION = D + 1
ENTRY_BOUND = Fraction(64)
LEGAL_ENERGY = Fraction(64)
REQUIRED_RATIO = Fraction(65, 64)
REQUIRED_ADVERSE_ENERGY = REQUIRED_RATIO * LEGAL_ENERGY
DIAGONAL_DOMINANCE_MARGIN = Fraction(1)

NAND_LEGAL = (
    (0, 0, 1),
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 0),
)
FALSE_DROP_PORT = (0, 0, 0)
assert FALSE_DROP_PORT not in NAND_LEGAL

# Integral port map: the first four columns are the legal words and the four
# auxiliary columns have zero port, exactly as frozen by the repaired proposal.
PORT_COLUMNS = NAND_LEGAL + (FALSE_DROP_PORT,) * 4
assert len(PORT_COLUMNS) == D

LEGAL_SELECTORS = tuple(
    tuple(int(index == legal) for index in range(D))
    for legal in range(4)
)
DROP_SELECTOR = (0,) * D


def emitted_port(selector):
    return tuple(
        sum(selector[column] * PORT_COLUMNS[column][coordinate] for column in range(D))
        for coordinate in range(3)
    )


assert tuple(emitted_port(selector) for selector in LEGAL_SELECTORS) == NAND_LEGAL
assert emitted_port(DROP_SELECTOR) == FALSE_DROP_PORT

# For z=0, all Q and h terms vanish.  The only remaining energy is the
# bottom-right extended-Gram entry s.  The bounded family imposes |s|<=64;
# PSD/strict diagonal dominance additionally imposes s>=1, but cannot increase
# the maximum possible DROP energy.
maximum_drop_energy = ENTRY_BOUND
assert REQUIRED_ADVERSE_ENERGY == 65
assert maximum_drop_energy == LEGAL_ENERGY
assert maximum_drop_energy < REQUIRED_ADVERSE_ENERGY
assert maximum_drop_energy / LEGAL_ENERGY == 1 < REQUIRED_RATIO

# Exact two-line infeasibility certificate for the candidate master system:
#     s >= 65   (FALSE/DROP soundness)
#     s <= 64   (entry bound)
# Their nonnegative sum gives 0 >= 1.
certificate = {
    "soundness_inequality": "s>=65",
    "entry_bound_inequality": "s<=64",
    "combined_contradiction": "0>=1",
}


def main():
    print(json.dumps({
        "family": "D=8 canonical one-hot NAND selectors with four zero-port auxiliaries",
        "extended_gram_dimension": EXTENDED_DIMENSION,
        "extended_gram_entry_bound": str(ENTRY_BOUND),
        "diagonal_dominance_margin": str(DIAGONAL_DOMINANCE_MARGIN),
        "legal_words": [list(word) for word in NAND_LEGAL],
        "legal_squared_energy": str(LEGAL_ENERGY),
        "required_adverse_ratio": str(REQUIRED_RATIO),
        "required_adverse_squared_energy": str(REQUIRED_ADVERSE_ENERGY),
        "drop_selector": list(DROP_SELECTOR),
        "drop_port": list(emitted_port(DROP_SELECTOR)),
        "maximum_possible_drop_squared_energy": str(maximum_drop_energy),
        "maximum_drop_to_legal_ratio": "1",
        "exact_infeasibility_certificate": certificate,
        "gram_search_status": "empty before enumeration",
        "copy_and_transfer_status": "not authorized after NAND DROP failure",
        "finding": "the bottom-right entry bound caps the unrestricted zero-vector DROP at legal energy, below 65/64",
        "scope": "finite symbolic rejection of the frozen normalization only; rescaled augmented families remain untested",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
