#!/usr/bin/env python3
"""Verify the 13-color state-rule partition on three F2^7 seed blocks."""
import json,itertools
C=[set(x) for x in json.load(open('experiments/f2_7_5.json'))];col={x:i+1 for i,S in enumerate(C) for x in S}
def st(x):return 0 if x==0 else col[x]
data=json.load(open('experiments/invalid/block_power_3_13.json'));assert data['t']==3 and data['q']==13
mp={tuple(map(int,k.split(','))):v for k,v in data['mapping'].items()}
states={s for s in itertools.product(range(6),repeat=3) if any(s)};assert set(mp)==states and set(mp.values())<=set(range(13))
# Generate all ordered state triples realizable by x,y,x+y in one seed block.
R={(st(x),st(y),st(x^y)) for x in range(128) for y in range(128)};count=0
for rels in itertools.product(R,repeat=3):
 ss=tuple(tuple(rels[j][h] for j in range(3)) for h in range(3))
 if all(any(s) for s in ss):
  # Coarse state vectors can coincide even though the underlying nonzero
  # vectors x,y,x+y are distinct.  Such lines must also be checked.
  assert not (mp[ss[0]]==mp[ss[1]]==mp[ss[2]]), (rels,ss)
  count+=1
print('verified 13-color state-rule partition of F2^21; checked',count,'ordered relation triples')
