#!/usr/bin/env python3
"""Coverage statistics explaining long-cycle random-scope phase transition."""
from __future__ import annotations
import random,collections

def stats(n,d,mult,trials,seed):
 rng=random.Random(seed);rows=[]
 for _ in range(trials):
  scopes=[set(rng.sample(range(n),d)) for _ in range(mult*n)]
  edge=[sum(e in S for S in scopes) for e in range(n)]
  pair=[sum(e in S and (e+1)%n in S for S in scopes) for e in range(n)]
  rows.append((min(edge),sum(x==0 for x in pair),max(pair),sum(pair)))
 return rows
def run():
 out={n:stats(n,3,2,100,307+n) for n in (12,24,30,60,100)}
 summary={n:{'avg_min_edge_coverage':sum(x[0] for x in R)/len(R),
             'avg_uncovered_adjacent_pairs':sum(x[1] for x in R)/len(R),
             'prob_all_adjacent_pairs_covered':sum(x[1]==0 for x in R)/len(R),
             'avg_total_adjacent_pair_hits':sum(x[3] for x in R)/len(R)} for n,R in out.items()}
 print(summary);return summary
if __name__=='__main__':run()
