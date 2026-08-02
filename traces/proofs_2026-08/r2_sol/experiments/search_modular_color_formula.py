#!/usr/bin/env python3
# Question: do the verified cyclic colorings reveal a simple residue/valuation formula that generalizes to growing-base families?
import json,collections,math
for p,k in [(127,5),(251,6),(509,7),(1021,8),(2039,9)]:
 C=json.load(open(f'experiments/cyclic_{p}_{k}.json'));col={x:i for i,S in enumerate(C) for x in S}
 print('\n',p,k)
 # Test correlation with multiplicative doubling orbits and low moduli.
 orbits=[];seen=set()
 for x in range(1,p):
  if x in seen:continue
  O=[];y=x
  while y not in O:O.append(y);seen.add(y);y=2*y%p
  orbits.append(O)
 print('doubling orbit lengths',collections.Counter(map(len,orbits)),'mean color changes',sum(sum(col[O[i]]!=col[O[(i+1)%len(O)]] for i in range(len(O))) for O in orbits)/sum(map(len,orbits)))
 for m in range(2,13):
  # majority prediction of color from x mod m
  pred={r:collections.Counter(col[x] for x in range(1,p) if x%m==r).most_common(1)[0][0] for r in range(m)}
  acc=sum(col[x]==pred[x%m] for x in range(1,p))/(p-1)
  if acc>.35:print('mod',m,'accuracy',acc)
