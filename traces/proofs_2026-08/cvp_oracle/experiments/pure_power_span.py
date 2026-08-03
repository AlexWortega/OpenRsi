#!/usr/bin/env python3
"""Exact pointed distance of spans of pure tensor powers (not full tensor codes)."""
from __future__ import annotations
import itertools, math, random, sys
import numpy as np
sys.path.insert(0,'experiments')
from dense_fold_attack import row_basis, words, pointed_distance, tensor_generator


def pure_power_generator(G,q):
    rows=[]
    for x in words(G):
        y=np.array([1],dtype=np.uint8)
        for _ in range(q): y=np.kron(y,x)%2
        rows.append(y)
    return row_basis(np.asarray(rows,dtype=np.uint8))


def symmetric_representatives(L, q):
    reps=[]
    for tup in itertools.combinations_with_replacement(range(L),q):
        idx=0
        for x in tup: idx=idx*L+x
        reps.append(idx)
    return reps


def random_codes(seed=41,trials=50):
    rng=random.Random(seed); records=[]
    for _ in range(trials):
        L=rng.choice((3,4)); k=2
        while True:
            G=row_basis(np.array([[rng.randrange(2) for _ in range(L)] for _ in range(k)],dtype=np.uint8))
            if len(G)==k and any(w[0] for w in words(G)):break
        d=pointed_distance(G)
        rec=[L,d]
        for q in (2,3):
            P=pure_power_generator(G,q)
            reps=symmetric_representatives(L,q)
            S=row_basis(P[:,reps])
            rec.extend([len(P),pointed_distance(P),d**q,pointed_distance(S),len(reps)])
        records.append(tuple(rec))
    return records


def run():
    G=np.array([[1,1,0],[1,0,1]],dtype=np.uint8)
    out={}
    for q in (1,2,3,4):
        P=pure_power_generator(G,q)
        out[q]={'rank':len(P),'delta':pointed_distance(P),'expected_full':2**q,'length':P.shape[1]}
    sym={}
    for q in (1,2,3,4,5):
        P=pure_power_generator(G,q); reps=symmetric_representatives(3,q)
        S=row_basis(P[:,reps]); sym[q]={'length':len(reps),'rank':len(S),'delta':pointed_distance(S)}
    records=random_codes(); failures=sum(rec[3]!=rec[4] or rec[8]!=rec[9] for rec in records)
    lower_bound_failures=sum(rec[5]*math.factorial(2)<rec[4] or rec[10]*math.factorial(3)<rec[9] for rec in records)
    result={'canonical':out,'canonical_symmetric':sym,'random_records':len(records),
            'nonmultiplicative_records':failures,'symmetric_lower_bound_failures':lower_bound_failures,
            'first_failures':[r for r in records if r[3]!=r[4] or r[8]!=r[9]][:5]}
    print(result);return result
if __name__=='__main__':run()
