#!/usr/bin/env python3
"""Search random small UNSAT 3CNFs for exact connected-view pseudoassignments."""
from __future__ import annotations
import argparse, itertools, random, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from connected_views import build, satisfies


def is_sat(clauses, n):
    for bits in itertools.product((0, 1), repeat=n):
        val = dict(enumerate(bits, 1))
        if all(satisfies(c, val) for c in clauses):
            return True
    return False


def gf2_solve(H, t):
    """Return one solution to Hx=t, or None. Python-int row elimination."""
    H = H.tocsr()
    rows = []
    p = H.shape[1]
    for i in range(H.shape[0]):
        mask = 0
        for j in H.indices[H.indptr[i]:H.indptr[i + 1]]:
            mask ^= 1 << int(j)
        rows.append(mask | (int(t[i]) << p))
    pivot_rows = {}
    for row in rows:
        x = row & ((1 << p) - 1)
        while x:
            pivot = x.bit_length() - 1
            if pivot not in pivot_rows:
                pivot_rows[pivot] = row
                break
            row ^= pivot_rows[pivot]
            x = row & ((1 << p) - 1)
        else:
            if (row >> p) & 1:
                return None
    sol = 0
    for pivot in sorted(pivot_rows):
        row = pivot_rows[pivot]
        rhs = (row >> p) & 1
        lower = row & ((1 << pivot) - 1)
        bit = rhs ^ ((lower & sol).bit_count() & 1)
        if bit:
            sol |= 1 << pivot
    return sol


def random_clause(rng, n):
    vs = rng.sample(range(1, n + 1), 3)
    return tuple(v if rng.randrange(2) else -v for v in vs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=5)
    ap.add_argument('--m', type=int, default=18)
    ap.add_argument('--d', type=int, default=2)
    ap.add_argument('--trials', type=int, default=1000)
    ap.add_argument('--seed', type=int, default=1)
    args = ap.parse_args(); rng = random.Random(args.seed)
    unsat = 0
    for trial in range(args.trials):
        clauses = []
        while len(clauses) < args.m:
            c = random_clause(rng, args.n)
            if c not in clauses:
                clauses.append(c)
        if is_sat(clauses, args.n):
            continue
        unsat += 1
        inst = build(clauses, args.d)
        sol = gf2_solve(inst.H, inst.target)
        if sol is not None:
            weight = sol.bit_count()
            print({'FOUND': True, 'trial': trial, 'unsat_seen': unsat, 'n': args.n,
                   'm': args.m, 'd': args.d, 'groups': len(inst.groups),
                   'rows': inst.H.shape[0], 'columns': inst.H.shape[1],
                   'one_solution_weight': weight, 'K': len(inst.groups),
                   'clauses': clauses})
            return
    print({'FOUND': False, 'trials': args.trials, 'unsat_seen': unsat})

if __name__ == '__main__': main()
