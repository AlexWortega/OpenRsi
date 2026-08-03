#!/usr/bin/env python3
"""Exact verification of the bounded-fan-in circuit-tableau fault."""
import sys
sys.path.insert(0, 'experiments')
from circuit_tableau_fault import build, explicit_witness, enumerate_one_faults, run
import numpy as np

r = run()
assert r['blocks_G'] == 30
assert r['columns_N'] == 108
assert r['rows_r'] == 82
assert r['binary_weight'] == r['blocks_G'] + 2 == 32
assert r['integer_squared_norm'] == 32
assert r['binary_residual_zero'] and r['integer_residual_zero']
assert r['accepting_one_fault_transcripts'] > 0

A, b, e, lam, meta, blocks = explicit_witness()
# Arbitrary deterministic dense row mixing preserves the exact faults.
rng = np.random.default_rng(941)
Lz = rng.integers(-5, 6, size=(37, A.shape[0]), dtype=np.int64).astype(object)
assert np.all(Lz @ (A @ lam - b) == 0)
L2 = rng.integers(0, 2, size=(41, A.shape[0]), dtype=np.int8).astype(object)
assert np.all((L2 @ (A @ e - b)) % 2 == 0)

# Verify the exact local affine identity, including coverage.
v01 = np.array([1, 0, 1, 1], dtype=int)
v10 = np.array([1, 1, 0, 1], dtype=int)
v11 = np.array([1, 1, 1, 1], dtype=int)
forbidden = np.array([1, 0, 0, 1], dtype=int)
assert np.array_equal(v01 + v10 - v11, forbidden)
assert np.array_equal((v01 + v10 + v11) % 2, forbidden)

# The exact enumeration ranges over all support-G+2 binary witnesses: block
# coverage implies precisely one 3-column exceptional block and singletons else.
accepts = enumerate_one_faults()
assert ((0, 0, 0), 'or0b', ((0, 1, 1), (1, 0, 1), (1, 1, 1)), (0, 0, 1)) in accepts
print('circuit-tableau support-three fault verified exactly')
