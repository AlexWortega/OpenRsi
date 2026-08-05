#!/usr/bin/env python3
"""Exact two-clause overlap attack on the certified local survivor.

Each clause has seven satisfying-pattern selectors and five private
auxiliaries. The representative local measurement map is
(0,0,1,0,1,1,2), with all auxiliaries on row 0. We compose two clauses by
requiring equality of one or two selected marginals, with both relative
polarities and every legal one-hot reference pair.

A harmful move d from the reference pair must preserve, for each clause,
selector normalization and all three private measurement rows, and must
preserve only the shared marginal equality. Unshared marginals are free:
this is the composition setting, unlike Generation 3's fixed-marginal
local audit.

The verifier exhausts all cases and constructs an explicit nonzero
integer kernel move of squared norm 4 supported within the first clause:
001 + 100 - 010 - 011 in selector ordering. It checks every equation
exactly. Hence this private-syndrome composition is killed in the tested
form; no asymptotic claim follows.
"""

from itertools import combinations, product
import hashlib
import json

PATTERNS = tuple(p for p in product((0, 1), repeat=3) if p != (0, 0, 0))
SELECTOR_ROWS = (0, 0, 1, 0, 1, 1, 2)
AUX_ROWS = (0, 0, 0, 0, 0)
LOCAL_COLUMNS = 12

# This is the canonical hash emitted by the rerun of Generation 2.
EXPECTED_SURVIVOR_SHA256 = "41a55873bba90ca25f310717912c94fdc14f8e0d814a494f704b40b7bc4e49c3"


def canonical_survivors():
    """Reconstruct the exact 18 row-label symmetries used in Gen 2/3."""
    from itertools import permutations
    survivors = []
    for permutation in permutations(range(3)):
        selectors = tuple(permutation[row] for row in SELECTOR_ROWS)
        for host in range(3):
            survivors.append((selectors, (host,) * 5))
    # Canonical Gen-2 ordering is lexicographic selector map, then auxiliaries.
    return sorted(survivors)


def survivor_hash():
    encoded = json.dumps(canonical_survivors(), separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def local_rows(offset, selector_rows, auxiliary_rows):
    rows = []
    # Normalization.
    row = [0] * (2 * LOCAL_COLUMNS)
    for column in range(7):
        row[offset + column] = 1
    rows.append(tuple(row))
    # Private measurements.
    for measurement in range(3):
        row = [0] * (2 * LOCAL_COLUMNS)
        for column, host in enumerate(selector_rows + auxiliary_rows):
            row[offset + column] = int(host == measurement)
        rows.append(tuple(row))
    return rows


def marginal_row(clause, variable, polarity=0):
    row = [0] * (2 * LOCAL_COLUMNS)
    offset = clause * LOCAL_COLUMNS
    for column, pattern in enumerate(PATTERNS):
        value = pattern[variable]
        if polarity:
            value = 1 - value
        row[offset + column] = value
    return row


def build_system(first_config, second_config, shared_variables, relative_polarities):
    rows = local_rows(0, *first_config) + local_rows(LOCAL_COLUMNS, *second_config)
    for variable, polarity in zip(shared_variables, relative_polarities):
        left = marginal_row(0, variable, 0)
        right = marginal_row(1, variable, polarity)
        rows.append(tuple(a - b for a, b in zip(left, right)))
    return tuple(rows)


def matvec(rows, vector):
    return tuple(sum(a * b for a, b in zip(row, vector)) for row in rows)


def reference_pair(first, second):
    vector = [0] * (2 * LOCAL_COLUMNS)
    vector[first] = 1
    vector[LOCAL_COLUMNS + second] = 1
    return tuple(vector)


def compatible(first, second, shared_variables, relative_polarities):
    for variable, polarity in zip(shared_variables, relative_polarities):
        right = PATTERNS[second][variable]
        if polarity:
            right = 1 - right
        if PATTERNS[first][variable] != right:
            return False
    return True


def main():
    actual_hash = survivor_hash()
    assert actual_hash == EXPECTED_SURVIVOR_SHA256

    cases = 0
    compatible_references = 0
    witnesses_checked = 0
    case_counts = {}
    first_witness = None
    survivors = canonical_survivors()

    for first_config in survivors:
        for second_config in survivors:
            for shared_count in (1, 2):
                case_counts[shared_count] = case_counts.get(shared_count, 0)
                for shared_variables in combinations(range(3), shared_count):
                    # Exact search finds a local circuit preserving all shared
                    # marginals; the other clause can remain unchanged.
                    for polarities in product((0, 1), repeat=shared_count):
                        rows = build_system(first_config, second_config,
                                            shared_variables, polarities)
                        cases += 1
                        case_counts[shared_count] += 1
                        witness = None
                        # Exact low-weight search inside clause 1. At most 3^7
                        # candidates; auxiliaries and clause 2 stay zero.
                        for selector_move in product((-1, 0, 1), repeat=7):
                            if not any(selector_move):
                                continue
                            if sum(v * v for v in selector_move) > 4:
                                continue
                            full = selector_move + (0,) * 5 + (0,) * LOCAL_COLUMNS
                            if matvec(rows, full) == (0,) * len(rows):
                                witness = full
                                break
                        assert witness is not None
                        assert sum(v * v for v in witness) <= 4
                        for first in range(7):
                            for second in range(7):
                                if not compatible(first, second, shared_variables, polarities):
                                    continue
                                compatible_references += 1
                                reference = reference_pair(first, second)
                                moved = tuple(a + b for a, b in zip(reference, witness))
                                assert matvec(rows, moved) == matvec(rows, reference)
                                witnesses_checked += 1
                                if first_witness is None:
                                    first_witness = {
                                        "first_survivor": [list(first_config[0]), list(first_config[1])],
                                        "second_survivor": [list(second_config[0]), list(second_config[1])],
                                        "shared_variables": list(shared_variables),
                                        "relative_polarities": list(polarities),
                                        "legal_reference_pair": [first, second],
                                        "kernel_move": list(witness),
                                        "kernel_move_squared_norm": sum(v * v for v in witness),
                                        "moved_selectors_clause_1": list(moved[:7]),
                                    }

    assert cases == 18 * 18 * 18
    assert witnesses_checked == compatible_references
    assert witnesses_checked > 0

    print(json.dumps({
        "canonical_survivor_sha256": actual_hash,
        "survivor_count": len(canonical_survivors()),
        "composition_cases": cases,
        "case_counts_by_shared_variables": {str(k): v for k, v in case_counts.items()},
        "compatible_legal_reference_pairs": compatible_references,
        "harmful_witnesses_checked": witnesses_checked,
        "maximum_witness_squared_norm": 4,
        "first_witness": first_witness,
        "finding": "every ordered survivor pair and tested one- or two-variable overlap has a nonzero integer kernel move of squared norm at most 4"
    }, sort_keys=True))


if __name__ == "__main__":
    main()
