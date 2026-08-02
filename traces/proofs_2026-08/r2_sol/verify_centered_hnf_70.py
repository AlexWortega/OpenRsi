#!/usr/bin/env python3
"""Independently verify centered integer tetrahedron HNFs through determinant 70."""
import json, math
from fractions import Fraction

def residues(a,b,c,d,e,f):
    out=[]
    for i in range(a):
      for j in range(d):
       for k in range(f):
        x=Fraction(i,a); y=Fraction(j-b*x,d); z=Fraction(k-c*x-e*y,f)
        out.append(tuple(q-math.floor(q) for q in (x,y,z)))
    assert len(set(out))==a*d*f
    return out

def centered(a,b,c,d,e,f): return a%4==0 and (b+d)%4==0 and (c+e+f)%4==0
stats={'tested':0,'centered':0,'feasible':0};best=0;wins=[];bydet={}
for D in range(1,71):
 for a in range(1,D+1):
  if D%a:continue
  for d in range(1,D//a+1):
   if (D//a)%d:continue
   f=D//a//d
   for b in range(a):
    for c in range(a):
     for e in range(d):
      stats['tested']+=1
      if not centered(a,b,c,d,e,f):continue
      stats['centered']+=1
      inside=[r for r in residues(a,b,c,d,e,f) if all(q>0 for q in r) and sum(r)<1]
      if inside != [(Fraction(1,4),)*3]:continue
      stats['feasible']+=1;bydet[D]=bydet.get(D,0)+1;H=((a,0,0),(b,d,0),(c,e,f))
      if D>best:best=D;wins=[H]
      elif D==best:wins.append(H)
expected=json.load(open('experiments/centered_hnf_70.json'))
assert stats=={'tested':229510,'centered':3268,'feasible':62}
assert best==64 and wins==[((4,0,0),(0,4,0),(0,0,4))]
assert bydet=={4:1,8:3,12:6,16:10,20:6,24:12,28:8,32:15,64:1}
assert expected['tested_hnfs']==stats['tested'] and expected['centered_hnfs']==stats['centered'] and expected['feasible_hnfs']==stats['feasible'] and expected['best_det']==best
print('verified centered HNFs through determinant 70:',stats,'unique maximum det 64')
