#!/usr/bin/env python3
"""Measure phase-lift completeness on explicit unique-SAT formulas exactly."""
from __future__ import annotations
import argparse,random,sys
sys.path.insert(0,'experiments')
from connected_views import all_eight_clauses
from phase_lift_ncp import random_alpha,sat_assignments,assignment_lifts

def unique_core():
    # Remove one clause from all8; its unique falsifying assignment satisfies the other seven.
    return all_eight_clauses()[1:]

def run(q=2,trials=1000,seed=101):
    C=unique_core();sats=sat_assignments(C,3);assert len(sats)==1
    rng=random.Random(seed);good=0
    for _ in range(trials):
        a=random_alpha(C,q,rng);good += assignment_lifts(sats[0],C,q,a) is not None
    result={'q':q,'trials':trials,'satisfying_assignments':sats,'lifts':good,
            'empirical_probability':good/trials}
    print(result);return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--q',type=int,default=2);ap.add_argument('--trials',type=int,default=1000);ap.add_argument('--seed',type=int,default=101)
 a=ap.parse_args();run(a.q,a.trials,a.seed)
