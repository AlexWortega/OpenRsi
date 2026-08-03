#!/usr/bin/env python3
"""Attack polynomial dense foldings of tiny pointed tensor codes.

The experiments are exact GF(2) enumeration. They illustrate that folding a tensor
code by permutation-orbit XORs or generic dense linear maps admits pointed words
much lighter than pure tensor powers. This is finite evidence, not an asymptotic
no-go theorem.
"""
from __future__ import annotations
import itertools, random
import numpy as np


def row_basis(G):
    basis = {}
    keep = []
    for row in np.asarray(G, dtype=np.uint8):
        mask = sum(int(x) << i for i, x in enumerate(row))
        z = mask
        while z:
            p = z.bit_length() - 1
            if p not in basis:
                basis[p] = z; keep.append(row.copy()); break
            z ^= basis[p]
    return np.asarray(keep, dtype=np.uint8)


def words(G):
    G = row_basis(G)
    for coeff in itertools.product((0, 1), repeat=len(G)):
        w = np.zeros(G.shape[1], dtype=np.uint8)
        for b, g in zip(coeff, G):
            if b: w ^= g
        yield w


def pointed_distance(G, star=0):
    vals = [int(w.sum()) for w in words(G) if w[star]]
    return min(vals) if vals else None


def tensor_generator(G, q=2):
    H = np.array([[1]], dtype=np.uint8)
    for _ in range(q):
        H = np.asarray([np.kron(a, b) % 2 for a in H for b in G], dtype=np.uint8)
    return row_basis(H)


def orbit_xor_q2(L):
    """Map L^2 coords to unordered-pair orbits, XORing both orientations."""
    pairs = [(i, j) for i in range(L) for j in range(i, L)]
    P = np.zeros((L * L, len(pairs)), dtype=np.uint8)
    for out, (i, j) in enumerate(pairs):
        P[i * L + j, out] = 1
        if i != j: P[j * L + i, out] = 1
    return P, pairs


def random_dense_fold(input_len, m, rng):
    """First output is exactly the distinguished input; others are dense."""
    P = np.zeros((input_len, m), dtype=np.uint8)
    P[0, 0] = 1
    for j in range(1, m):
        P[:, j] = [rng.randrange(2) for _ in range(input_len)]
    return P


def pure_pointed_images(G, P):
    vals = []
    for x in words(G):
        if x[0]: vals.append(int((np.kron(x, x).dot(P) % 2).sum()))
    return vals


def run():
    # Pointed distance 2: a=(1,1,0), b=(1,0,1).
    G = np.array([[1, 1, 0], [1, 0, 1]], dtype=np.uint8)
    T = tensor_generator(G, 2)
    assert pointed_distance(G) == 2 and pointed_distance(T) == 4

    Porb, pairs = orbit_xor_q2(3)
    Orb = row_basis(T.dot(Porb) % 2)
    orbit_delta = pointed_distance(Orb, pairs.index((0, 0)))
    pure_orbit = pure_pointed_images(G, Porb)

    rng = random.Random(11)
    histogram = {}
    examples = []
    for _ in range(200):
        P = random_dense_fold(9, 6, rng)
        H = row_basis(T.dot(P) % 2)
        d = pointed_distance(H, 0)
        histogram[d] = histogram.get(d, 0) + 1
        pure = min(pure_pointed_images(G, P))
        if d < pure and len(examples) < 3:
            examples.append((d, pure, len(H)))

    result = {
        'base_delta': 2, 'full_tensor_delta': 4,
        'orbit_outputs': len(pairs), 'orbit_fold_delta': orbit_delta,
        'orbit_pure_weights': pure_orbit,
        'random_dense_delta_histogram': histogram,
        'arbitrary_below_pure_examples': examples,
    }
    print(result)
    return result


if __name__ == '__main__': run()
