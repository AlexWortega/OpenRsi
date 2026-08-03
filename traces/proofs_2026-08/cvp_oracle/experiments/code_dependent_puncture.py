#!/usr/bin/env python3
"""Exact search for smallest code-dependent puncturing preserving pointed distance."""
from __future__ import annotations
import itertools, random, sys
import numpy as np
sys.path.insert(0, 'experiments')
from dense_fold_attack import row_basis, words, pointed_distance, tensor_generator


def puncture(G, S): return row_basis(np.asarray(G)[:, list(S)])


def min_preserving_sample(G, star, target):
    L = G.shape[1]
    others = [i for i in range(L) if i != star]
    for m in range(target, L + 1):  # need at least target output positions
        sols=[]
        for rest in itertools.combinations(others, m - 1):
            S=(star,)+rest
            if pointed_distance(puncture(G,S),0) == target: sols.append(S)
        if sols: return m, sols
    return None, []


def random_pointed_codes(seed=31, trials=40):
    rng=random.Random(seed); records=[]
    for _ in range(trials):
        L=4; k=2
        while True:
            G=np.array([[rng.randrange(2) for _ in range(L)] for _ in range(k)],dtype=np.uint8)
            G=row_basis(G)
            if len(G)==k and any(w[0] for w in words(G)): break
        d=pointed_distance(G)
        T=tensor_generator(G,2); target=d*d
        m,sols=min_preserving_sample(T,0,target)
        records.append((d,m,T.shape[1],len(sols)))
    return records


def run():
    G=np.array([[1,1,0],[1,0,1]],dtype=np.uint8)
    T=tensor_generator(G,2)
    m,sols=min_preserving_sample(T,0,4)
    records=random_pointed_codes()
    hist={}
    for rec in records: hist[rec[:2]]=hist.get(rec[:2],0)+1
    result={'canonical_full_len':9,'canonical_min_sample':m,
            'canonical_preserving_samples':sols,
            'random_(base_delta,min_sample)_histogram':hist}
    print(result); return result
if __name__=='__main__':run()
