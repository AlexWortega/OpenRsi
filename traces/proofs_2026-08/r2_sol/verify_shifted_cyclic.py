#!/usr/bin/env python3
"""Verify layer-dependent cyclic colorings directly on every vertex triangle."""
import itertools,json
for p,r,k,path in [(31,2,5,'experiments/shifted_31x2_5.json'),(31,3,6,'experiments/shifted_31x3_6.json'),(127,2,6,'experiments/shifted_127x2_6.json'),(127,3,7,'experiments/shifted_127x3_7.json')]:
 D=json.load(open(path));assert (D['p'],D['r'],D['k'])==(p,r,k);mp={tuple(x):c for x,c in zip(D['keys'],D['colors'])}
 def color(u,v):
  a,x=u;b,y=v;d=(y-x)%p
  if a>b:a,b,d=b,a,(-d)%p
  if a==b:d=min(d,(-d)%p)
  return mp[(a,b,d)]
 V=[(a,x) for a in range(r) for x in range(p)];count=0
 for a,b,c in itertools.combinations(V,3):assert len({color(a,b),color(a,c),color(b,c)})>1;count+=1
 print('verified shifted cyclic K_%d with %d colors:'%(p*r,k),count,'triangles')
