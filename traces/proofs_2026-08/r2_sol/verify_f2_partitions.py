#!/usr/bin/env python3
"""Verify explicit sum-free partitions and their induced translation colorings."""
import json
from itertools import combinations
for d,k,path in [(7,5,'experiments/f2_7_5.json'),(8,6,'experiments/f2_8_6.json')]:
 with open(path) as f:classes=[set(x) for x in json.load(f)]
 assert len(classes)==k
 assert set().union(*classes)==set(range(1,1<<d))
 assert sum(map(len,classes))==(1<<d)-1
 assert all((a^b) not in C for C in classes for a,b in combinations(C,2))
 color={x:i for i,C in enumerate(classes) for x in C}
 count=0
 for x,y,z in combinations(range(1<<d),3):
  assert not (color[x^y]==color[x^z]==color[y^z]);count+=1
 print(f'F2^{d}: {k} classes, checked {count} vertex triangles, sizes {list(map(len,classes))}')
