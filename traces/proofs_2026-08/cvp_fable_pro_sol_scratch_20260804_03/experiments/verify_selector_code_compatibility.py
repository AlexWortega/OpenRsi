#!/usr/bin/env python3
"""Generation-13 compatibility audit for raw-selector syndrome codes.

Any linear hash that accepts every globally consistent one-hot encoding with a
common target must annihilate their difference space.  This verifier computes
the maximal compatible syndrome spaces over p=2,3,5,127 and attacks them with
the previously verified selector witnesses.

The Generation-11 unique-triple parity is an *integral affine combination* of
the 16 globally consistent encodings.  Its affine coefficients sum to one, so
it has exactly the same hash target over the integers and modulo every prime.
This finite obstruction kills the bounded raw-selector Construction-A/code
mutation before carries or a lattice are emitted.  It is not an asymptotic
impossibility theorem for unrelated encodings.
"""

from __future__ import annotations

import argparse
import hashlib
from itertools import product
import json
from pathlib import Path

import verify_global_psd_metric as gen9
import verify_degree3_global_psd_metric as gen11

PRIMES = (2, 3, 5, 127)
N_SELECTORS = gen9.N_SELECTORS
ASSIGNMENTS = tuple(product((0, 1), repeat=4))
MANIFEST_PATH = Path(__file__).with_name("gen13_selector_code_compatibility_manifest.json")


def sparse(vector):
    return [[index, int(value)] for index, value in enumerate(vector) if value]


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def rref_mod(rows, prime):
    matrix = [[value % prime for value in row] for row in rows]
    if not matrix:
        return (), ()
    row = 0
    pivots = []
    for column in range(len(matrix[0])):
        pivot = next(
            (candidate for candidate in range(row, len(matrix))
             if matrix[candidate][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        inverse = pow(matrix[row][column], -1, prime)
        matrix[row] = [(inverse * value) % prime for value in matrix[row]]
        for other in range(len(matrix)):
            if other == row or not matrix[other][column]:
                continue
            scale = matrix[other][column]
            matrix[other] = [
                (value - scale * pivot_value) % prime
                for value, pivot_value in zip(matrix[other], matrix[row])
            ]
        pivots.append(column)
        row += 1
        if row == len(matrix):
            break
    nonzero = tuple(tuple(values) for values in matrix[:row])
    return nonzero, tuple(pivots)


def nullspace_mod(rows, prime):
    """Canonical right-nullspace basis of rows over F_prime."""
    reduced, pivots = rref_mod(rows, prime)
    n_columns = len(rows[0])
    free = tuple(column for column in range(n_columns) if column not in pivots)
    basis = []
    for free_column in free:
        vector = [0] * n_columns
        vector[free_column] = 1
        for pivot_row, pivot_column in enumerate(pivots):
            vector[pivot_column] = (-reduced[pivot_row][free_column]) % prime
        basis.append(tuple(vector))
    for vector in basis:
        assert all(dot(row, vector) % prime == 0 for row in rows)
    return tuple(basis), pivots


def syndrome(basis, vector, prime):
    return tuple(dot(row, vector) % prime for row in basis)


def clauses_and_honest_encodings():
    clauses = gen9.clause_data(gen9.UNSAT_EDGES)
    encodings = tuple(
        gen9.honest_selector(clauses, assignment)[0]
        for assignment in ASSIGNMENTS
    )
    assert len(set(encodings)) == 16
    return clauses, encodings


def three_term_attack(clauses, honest_encodings):
    selector = list(honest_encodings[0])
    selector[gen9.selector_index(0, 0)] = 0
    selector[gen9.selector_index(0, gen9.PATTERNS.index((0, 1, 1)))] = 1
    selector[gen9.selector_index(0, gen9.PATTERNS.index((1, 0, 0)))] = 1
    selector[gen9.selector_index(0, gen9.PATTERNS.index((1, 1, 1)))] = -1
    return tuple(selector)


def embedded_g5_circuits():
    # Generation-5 representative on the seven legal patterns 001,...,111.
    legal_move = (-1, 0, 1, 1, -1, 0, 0)
    block = (0,) + legal_move
    circuits = []
    for clause in range(9):
        vector = [0] * N_SELECTORS
        vector[8 * clause:8 * clause + 8] = block
        circuits.append(tuple(vector))
    return tuple(circuits)


def simple_clause_drops(honest_encodings):
    drops = []
    for assignment_index, encoding in enumerate(honest_encodings):
        for clause in range(9):
            selector = list(encoding)
            selector[8 * clause:8 * clause + 8] = (0,) * 8
            drops.append((assignment_index, clause, tuple(selector)))
    return tuple(drops)


def anchor_extra(selector):
    return sum(4 * value * (value - 1) for value in selector)


def attack_records(clauses, honest_encodings):
    attacks = []
    attacks.append(("G7_three_term", three_term_attack(clauses, honest_encodings)))
    attacks.append((
        "G9_degree_two_parity",
        tuple(gen9.exact_zero_residual_search(clauses)["selector"]),
    ))
    attacks.append((
        "G11_unique_triple_parity",
        tuple(gen11.exact_zero_residual_search(clauses)["selector"]),
    ))
    # The exact Generation-12 clause-drop witness is assignment 0000 with
    # clause 0 removed.  Include all 16*9 analogous drops in the audit below.
    drop = list(honest_encodings[0])
    drop[:8] = (0,) * 8
    attacks.append(("G12_exact_clause_drop", tuple(drop)))
    return tuple(attacks)


def affine_collision_certificate(honest_encodings, collision):
    # Lexicographic assignments 0000,...,1111.  This exact coefficient vector
    # was obtained by rational elimination and is checked from scratch below.
    coefficients = (1, -1, -1, 1, 0, 0, 0, 0,
                    -1, 1, 1, -1, 1, 0, 0, 0)
    assert sum(coefficients) == 1
    reconstructed = tuple(
        sum(coefficients[index] * honest_encodings[index][coordinate]
            for index in range(16))
        for coordinate in range(N_SELECTORS)
    )
    assert reconstructed == collision
    return coefficients


def build_audit():
    clauses, honest = clauses_and_honest_encodings()
    differences = tuple(
        tuple(value - reference for value, reference in zip(encoding, honest[0]))
        for encoding in honest[1:]
    )
    attacks = attack_records(clauses, honest)
    collision = dict(attacks)["G11_unique_triple_parity"]
    coefficients = affine_collision_certificate(honest, collision)
    collision_deviation = tuple(
        value - reference for value, reference in zip(collision, honest[0])
    )

    prime_records = []
    for prime in PRIMES:
        compatible_basis, pivots = nullspace_mod(differences, prime)
        assert len(pivots) == 14
        assert len(compatible_basis) == N_SELECTORS - len(pivots) == 58
        # This is maximal: every compatible linear row lies in this nullspace.
        assert all(
            not any(syndrome(compatible_basis, difference, prime))
            for difference in differences
        )
        records = []
        for name, selector in attacks:
            deviation = tuple(
                value - reference for value, reference in zip(selector, honest[0])
            )
            syn = syndrome(compatible_basis, deviation, prime)
            records.append({
                "name": name,
                "anchor_extra": anchor_extra(selector),
                "syndrome_weight": sum(value != 0 for value in syn),
                "zero_syndrome": not any(syn),
            })
        g5 = []
        for clause, deviation in enumerate(embedded_g5_circuits()):
            syn = syndrome(compatible_basis, deviation, prime)
            g5.append({
                "clause": clause,
                "syndrome_weight": sum(value != 0 for value in syn),
                "zero_syndrome": not any(syn),
            })
        drops = []
        for assignment_index, clause, selector in simple_clause_drops(honest):
            deviation = tuple(
                value - reference for value, reference in zip(selector, honest[0])
            )
            syn = syndrome(compatible_basis, deviation, prime)
            drops.append({
                "assignment": "".join(map(str, ASSIGNMENTS[assignment_index])),
                "clause": clause,
                "syndrome_weight": sum(value != 0 for value in syn),
                "zero_syndrome": not any(syn),
            })
        assert not any(syndrome(compatible_basis, collision_deviation, prime))
        prime_records.append({
            "prime": prime,
            "difference_rank": len(pivots),
            "maximal_compatible_syndrome_dimension": len(compatible_basis),
            "rref_pivots": list(pivots),
            "maximal_compatible_syndrome_basis": [sparse(row) for row in compatible_basis],
            "attacks": records,
            "g5_representative_embeddings": g5,
            "all_simple_clause_drops": drops,
        })

    payload = {
        "schema": "gen13-selector-code-compatibility-v1",
        "finite_claim_only": True,
        "selector_count": N_SELECTORS,
        "assignments": ["".join(map(str, assignment)) for assignment in ASSIGNMENTS],
        "honest_encodings": [sparse(encoding) for encoding in honest],
        "difference_generators": [sparse(row) for row in differences],
        "affine_collision": {
            "name": "G11_unique_triple_parity",
            "selector": sparse(collision),
            "anchor_extra": anchor_extra(collision),
            "coefficients_on_lexicographic_honest_encodings": list(coefficients),
            "coefficient_sum": sum(coefficients),
            "identity": "collision=sum_i coefficients[i]*honest_encoding[i] over Z",
        },
        "prime_audits": prime_records,
        "conclusion": (
            "the G11 selector has the common honest hash under every linear "
            "compatible syndrome, over Z and modulo every tested or untested prime"
        ),
        "scope": (
            "finite obstruction to raw 72-selector linear hashing; no claim "
            "about nonlinear or enlarged encodings"
        ),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["audit_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args()

    expected = build_audit()
    if args.write_manifest:
        MANIFEST_PATH.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
        print(MANIFEST_PATH)
        return

    manifest = json.loads(MANIFEST_PATH.read_text())
    assert manifest == expected
    collision = manifest["affine_collision"]
    assert collision["anchor_extra"] == 24 <= 36
    for audit in manifest["prime_audits"]:
        record = next(
            attack for attack in audit["attacks"]
            if attack["name"] == "G11_unique_triple_parity"
        )
        assert record["zero_syndrome"]
        assert record["syndrome_weight"] == 0

    print(json.dumps({
        "manifest": str(MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[1])),
        "audit_sha256": manifest["audit_sha256"],
        "primes": list(PRIMES),
        "difference_rank_each_prime": 14,
        "maximal_compatible_syndrome_dimension_each_prime": 58,
        "affine_collision_anchor_extra": collision["anchor_extra"],
        "affine_collision_coefficients": collision[
            "coefficients_on_lexicographic_honest_encodings"
        ],
        "coefficient_sum": collision["coefficient_sum"],
        "finding": (
            "the Generation-11 unique-triple parity is an integral affine "
            "combination of honest encodings and has zero maximal compatible "
            "syndrome for p=2,3,5,127"
        ),
        "falsification": (
            "Construction-A carries or syndrome scaling cannot charge this "
            "exact compatibility collision"
        ),
        "scope": manifest["scope"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
