#!/usr/bin/env python3
"""Search phase-lifted 3-clause gadgets for low-support GF(2) trades.

A column (a,z), for a legal Boolean view a and phase z in Z/q, has one 1 in
row (occurrence j, bit a_j, phase z+alpha[j,a]).  We ask whether every singleton
boundary of the forbidden view has an expensive representation by legal columns.
All calculations are exact Python-integer XOR dynamic programming.
"""
from __future__ import annotations
import argparse, itertools, random

VIEWS=list(itertools.product((0,1),repeat=3)); FORBIDDEN=(0,0,0)
LEGAL=[a for a in VIEWS if a!=FORBIDDEN]

def row(j,b,z,q): return (j*2+b)*q+z

def mask_for(a,z,alpha,q):
    m=0
    for j in range(3): m ^= 1<<row(j,a[j],(z+alpha[a][j])%q,q)
    return m

def columns(alpha,q): return [mask_for(a,z,alpha,q) for a in LEGAL for z in range(q)]

def target(phases,q):
    return sum(1<<row(j,0,phases[j],q) for j in range(3))

def coset_minima(cols,max_states=2_000_000):
    dist={0:0}
    for c in cols:
        old=list(dist.items())
        for s,w in old:
            ns=s^c; nw=w+1
            if nw<dist.get(ns,10**9): dist[ns]=nw
        if len(dist)>max_states: return None
    return dist

def evaluate(alpha,q):
    dist=coset_minima(columns(alpha,q))
    if dist is None:return None
    vals={p:dist.get(target(p,q)) for p in itertools.product(range(q),repeat=3)}
    feasible=[v for v in vals.values() if v is not None]
    return {'rank_states':len(dist),'infeasible_targets':sum(v is None for v in vals.values()),
            'minimum_trade':None if not feasible else min(feasible),
            'maximum_trade':None if not feasible else max(feasible),
            'histogram':{w:feasible.count(w) for w in sorted(set(feasible))}}

def random_alpha(q,rng):
    return {a:tuple(rng.randrange(q) for _ in range(3)) for a in VIEWS}

def run(q=3,trials=100,seed=47):
    rng=random.Random(seed); hist={}; best=None; best_alpha=None
    for _ in range(trials):
        alpha=random_alpha(q,rng); e=evaluate(alpha,q)
        key=None if e is None else (e['minimum_trade'],e['infeasible_targets'])
        hist[key]=hist.get(key,0)+1
        score=(-1,-1) if e is None else (e['minimum_trade'] or 10**9,e['infeasible_targets'])
        if best is None or score>best:
            best=score;best_alpha=alpha;best_eval=e
    result={'q':q,'trials':trials,'outcome_histogram':hist,'best_score':best,
            'best_eval':best_eval,'best_alpha':best_alpha}
    print(result);return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--q',type=int,default=3);ap.add_argument('--trials',type=int,default=100);ap.add_argument('--seed',type=int,default=47)
    a=ap.parse_args();run(a.q,a.trials,a.seed)
