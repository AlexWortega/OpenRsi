#!/usr/bin/env python3
"""Exact checks for the characteristic-independent affine parallelogram cheat."""
from __future__ import annotations
import itertools, random
import numpy as np


def vertices(k): return list(itertools.product((0, 1), repeat=k))


def add(u, v): return tuple(a ^ b for a, b in zip(u, v))


def verify(k=3):
    rng = random.Random(19)
    tested = 0
    for modulus in (0, 2, 3, 5, 6, 10):  # modulus 0 means integer equality
        for _ in range(50):
            u = tuple(rng.randrange(2) for _ in range(k))
            # Flip two distinct Boolean coordinates; these four vertices form
            # an affine parallelogram over the integers, not only over F2.
            i, j = rng.sample(range(k), 2)
            p = tuple(int(h == i) for h in range(k))
            q = tuple(int(h == j) for h in range(k))
            a, b, c = add(u, p), add(u, q), add(add(u, p), q)
            # Random affine integer signature g(x)=A x+c0.
            A = np.array([[rng.randrange(-5, 6) for _ in range(k)] for _ in range(7)], dtype=int)
            c0 = np.array([rng.randrange(-5, 6) for _ in range(7)], dtype=int)
            def g(x): return A.dot(np.array(x, dtype=int)) + c0
            lhs = g(a) + g(b) - g(c)
            rhs = g(u)
            if modulus:
                assert np.array_equal(lhs % modulus, rhs % modulus)
            else:
                assert np.array_equal(lhs, rhs)
            assert a != u and b != u and c != u
            tested += 1
    print({'dimensions': k, 'integer_and_modular_affine_identities_checked': tested,
           'moduli': ['Z',2,3,5,6,10]})

if __name__ == '__main__': verify()
