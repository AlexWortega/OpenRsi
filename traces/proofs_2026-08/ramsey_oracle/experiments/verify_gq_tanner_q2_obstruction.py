#!/usr/bin/env python3
"""Independent exact q=2 GQ-Tanner obstruction via perfect matchings."""
from itertools import combinations
V=tuple(range(6)); DUADS=tuple(combinations(V,2))
def syn(rem=V):
 rem=tuple(rem)
 if not rem: yield ();return
 a=rem[0]
 for j in range(1,len(rem)):
  b=rem[j]
  for tail in syn(rem[1:j]+rem[j+1:]):yield tuple(sorted(((a,b),)+tail))
SYN=tuple(sorted(set(syn())));INC=[tuple(j for j,S in enumerate(SYN) if p in S) for p in DUADS]
PM=[];a=[-1]*15
def rec(rows,used):
 if not rows:PM.append(tuple(a));return
 p=min(rows,key=lambda r:sum(not (used>>s&1) for s in INC[r]));nr=rows-{p}
 for s in INC[p]:
  if not (used>>s&1):a[p]=s;rec(nr,used|1<<s)
rec(set(range(15)),0)
n=len(PM);adj=[0]*n
for i in range(n):
 for j in range(i+1,n):
  if sum(x==y for x,y in zip(PM[i],PM[j]))==3:adj[i]|=1<<j;adj[j]|=1<<i
best=[]
def expand(clique,cand):
 global best
 if len(clique)+cand.bit_count()<=len(best):return
 if not cand:
  if len(clique)>len(best):best=clique[:]
  return
 while cand:
  if len(clique)+cand.bit_count()<=len(best):return
  bit=cand&-cand;cand^=bit;v=bit.bit_length()-1
  expand(clique+[v],cand&adj[v])
expand([], (1<<n)-1)
print('perfect_matchings',n,'compatibility_edges',sum(x.bit_count() for x in adj)//2,'clique_number',len(best))
assert len(best)<6
print('PASS: no six perfect matchings have every pairwise intersection equal to 3')
