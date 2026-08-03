#!/usr/bin/env python3
"""Verify bounded-degree Boolean finite-difference relations exactly."""
from __future__ import annotations
import itertools, math, random
import numpy as np


def monomial_matrix(k, d):
    verts = list(itertools.product((0, 1), repeat=k))
    mons = [T for r in range(d + 1) for T in itertools.combinations(range(k), r)]
    M = np.array([[math.prod(x[i] for i in T) for x in verts] for T in mons], dtype=object)
    return M, verts, mons


def flip(u, S):
    return tuple(bit ^ int(i in S) for i, bit in enumerate(u))


def verify():
    tested = 0
    rng = random.Random(23)
    for k in range(2, 7):
        for d in range(k):
            M, verts, _ = monomial_matrix(k, d)
            index = {x:i for i,x in enumerate(verts)}
            for _ in range(20):
                u = rng.choice(verts)
                J = tuple(rng.sample(range(k), d + 1))
                lam = np.zeros(len(verts), dtype=object)
                for r in range(d + 2):
                    for S in itertools.combinations(J, r):
                        lam[index[flip(u, S)]] += (-1) ** r
                assert np.all(M.dot(lam) == 0)
                for mod in (2, 3, 5, 6, 10): assert np.all(np.asarray(M.dot(lam),dtype=int) % mod == 0)
                # Solving for u uses every other subcube vertex with coefficients +/-1.
                assert int(lam[index[u]]) == 1
                assert sum(int(x != 0) for x in lam) == 2 ** (d + 1)
                tested += 1
    M, verts, _ = monomial_matrix(3, 2)
    # Our lexicographic order is 000,001,010,011,100,101,110,111.
    lam = np.array([1,-1,-1,1,-1,1,1,-1], dtype=object)
    assert np.all(M.dot(lam) == 0)
    print({'finite_difference_instances':tested,'k_range':[2,6],
           'degree_range':'0..k-1','quadratic_cube_rank_shape':M.shape})

if __name__ == '__main__': verify()
