#!/usr/bin/env python3
"""Meet-in-the-middle search for short odd trades in phase-lift clause gadgets."""
from __future__ import annotations
import argparse, random, sys
sys.path.insert(0,'experiments')
from phase_clause_gadget import VIEWS,FORBIDDEN,LEGAL,columns,target,random_alpha

def shortest_upto5(alpha,q):
    cs=columns(alpha,q); t=target(alpha[FORBIDDEN],q); n=len(cs)
    if t in cs:return 1
    pairs={}
    for i in range(n):
        for j in range(i+1,n): pairs.setdefault(cs[i]^cs[j],(i,j))
    for k,c in enumerate(cs):
        z=t^c
        if z in pairs:
            i,j=pairs[z]
            if k not in (i,j):return 3
    # Pair + triple. Distinctness is checked explicitly.
    for i in range(n):
        for j in range(i+1,n):
            ij=cs[i]^cs[j]
            for k in range(j+1,n):
                z=t^ij^cs[k]
                if z in pairs:
                    a,b=pairs[z]
                    if len({i,j,k,a,b})==5:return 5
    return None

def run(q=8,trials=100,seed=59):
    rng=random.Random(seed);hist={};best=None
    for _ in range(trials):
        a=random_alpha(q,rng);d=shortest_upto5(a,q);hist[d]=hist.get(d,0)+1
        if d is None:best=a
    result={'q':q,'trials':trials,'shortest_odd_trade_histogram':hist,'has_no_trade_upto5':best is not None,
            'example_no_trade_upto5':best}
    print(result);return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--q',type=int,default=8);ap.add_argument('--trials',type=int,default=100);ap.add_argument('--seed',type=int,default=59)
 a=ap.parse_args();run(a.q,a.trials,a.seed)
