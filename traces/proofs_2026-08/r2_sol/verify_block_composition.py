#!/usr/bin/env python3
"""Verify the explicit 10-color block composition of the F2^7 seed."""
import json,itertools
seed=[set(C) for C in json.load(open('experiments/f2_7_5.json'))];k=len(seed);d=7
col={x:i+1 for i,C in enumerate(seed) for x in C}
def st(x):return 0 if x==0 else col[x]
data=json.load(open('experiments/block_q10.json'));q=data['q'];mp={tuple(map(int,s.split(','))):c for s,c in data['mapping'].items()}
assert q==10 and set(mp)=={(a,b) for a in range(k+1) for b in range(k+1) if (a,b)!=(0,0)}
# Verify the induced coloring directly on all projective lines of F2^14 by state reduction.
def color(x):
 a=x&127;b=x>>7;return mp[(st(a),st(b))]
count=0
for x in range(1,1<<14):
 for y in range(x+1,1<<14):
  z=x^y
  if y<z:
   assert not (color(x)==color(y)==color(z));count+=1
print('verified 10-color sum-free partition of F2^14:',count,'projective lines')
