#!/usr/bin/env python3
"""Generate bounded-degree Tseitin parity contradictions as exact 3CNF."""
from __future__ import annotations
import itertools,random
from connected_views import xor3_clauses

def random_3regular(n,seed):
 assert n%2==0 and n>=4
 rng=random.Random(seed)
 for _ in range(10000):
  stubs=[v for v in range(n) for _ in range(3)];rng.shuffle(stubs);E=[];ok=True
  for i in range(0,len(stubs),2):
   u,v=stubs[i],stubs[i+1]
   if u==v or tuple(sorted((u,v))) in E:ok=False;break
   E.append(tuple(sorted((u,v))))
  if ok:return E
 raise RuntimeError('no graph')
def formula(n,seed=313):
 E=random_3regular(n,seed);var={e:i+1 for i,e in enumerate(E)};C=[]
 for v in range(n):
  inc=tuple(var[e] for e in E if v in e);assert len(inc)==3
  C.extend(xor3_clauses(inc,1 if v==0 else 0))
 return C,E
