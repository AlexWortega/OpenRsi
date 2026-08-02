#!/usr/bin/env python3
"""Verify the 12-color state rule on a 21-bit seed-rule block plus one F2^7 block."""
import json,itertools
C=json.load(open('experiments/f2_7_5.json'));base={x:i+1 for i,S in enumerate(C) for x in S}
def st(x):return 0 if x==0 else base[x]
R5={(st(x),st(y),st(x^y)) for x in range(128) for y in range(128)}
d=json.load(open('experiments/block_power_3_13.json'));mp13={tuple(map(int,k.split(','))):v+1 for k,v in d['mapping'].items()}
R13=set()
for rels in itertools.product(R5,repeat=3):
 ss=[tuple(rels[j][h] for j in range(3)) for h in range(3)];R13.add(tuple(0 if not any(s) else mp13[s] for s in ss))
e=json.load(open('experiments/extend_rule_q12.json'));assert e['q']==12
mp={tuple(map(int,k.split(','))):v for k,v in e['mapping'].items()};states={(a,b) for a in range(14) for b in range(6) if (a,b)!=(0,0)}
assert set(mp)==states and set(mp.values())<=set(range(12));count=0
for a,b in itertools.product(R13,R5):
 ss=[(a[h],b[h]) for h in range(3)]
 if all(any(s) for s in ss) and len(set(ss))==3:
  assert not (mp[ss[0]]==mp[ss[1]]==mp[ss[2]]);count+=1
print('verified 12-color state-rule partition of F2^28; checked',count,'ordered relation pairs; R13 size',len(R13))
