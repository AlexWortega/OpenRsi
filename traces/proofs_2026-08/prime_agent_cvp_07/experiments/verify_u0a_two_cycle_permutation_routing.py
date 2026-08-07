#!/usr/bin/env python3
"""Exact finite routing audit for the parameterized U0a butterfly.

At W=4 and W=8, two full cycles of dimension switches (4 log2 W actual
stages because each offset is repeated twice) realize every permutation.
The verifier exhausts the complete symmetric group using exact tuple states,
reconstructs settings for reversal, and checks those COPY_A/COPY_B settings
against the actual serialized C,D and a fixed output target.

This is finite routing evidence only; it is not an all-width Beneš theorem or
an arbitrary formula compiler.
"""
from itertools import permutations
from pathlib import Path
import importlib.util
src=Path(__file__).with_name('verify_u0a_universal_topology_serializer.py')
spec=importlib.util.spec_from_file_location('u0a',src);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def pairs(w,off):
 seen=set();out=[]
 for i in range(w):
  if i not in seen:
   j=i^off;out.append((i,j));seen|={i,j}
 return out

def build_layers(w):
 k=w.bit_length()-1;offs=[1<<b for _ in range(2) for b in range(k) for __ in range(2)]
 layers=[{tuple(range(w)):None}]
 for off in offs:
  nxt={};ps=pairs(w,off)
  for perm in layers[-1]:
   for mask in range(1<<len(ps)):
    q=list(perm)
    for a,(i,j) in enumerate(ps):
     if mask>>a&1:q[i],q[j]=q[j],q[i]
    nxt.setdefault(tuple(q),(perm,mask))
  layers.append(nxt)
 return offs,layers
records=[]
for w in (4,8):
 offs,layers=build_layers(w);allperms=set(permutations(range(w)))
 assert set(layers[-1])==allperms
 target=tuple(reversed(range(w)));settings=[];cur=target
 for stage in range(len(offs),0,-1):
  prev,mask=layers[stage][cur];settings.append(mask);cur=prev
 settings.reverse();assert cur==tuple(range(w))
 # Re-run actual permutation and create serialized COPY modes.
 token=list(range(w));modes={}
 for s,(off,mask) in enumerate(zip(offs,settings),1):
  ps=pairs(w,off);new=list(token)
  for a,(i,j) in enumerate(ps):
   swap=bool(mask>>a&1)
   modes[(s,i)]='COPY_B' if swap else 'COPY_A'
   modes[(s,j)]='COPY_B' if swap else 'COPY_A'
   if swap:new[i],new[j]=token[j],token[i]
  token=new
 assert tuple(token)==target
 payload,_,_=mod.make_factor(w,gate_stages=len(offs))
 # Check an actual binary pattern and fixed output target through C,D.
 bits=[(3*i+1)%2 for i in range(w)];sm=['FREE']*w;vals={(0,i):bits[i] for i in range(w)}
 for s,off in enumerate(offs,1):
  for i in range(w):
   a,b=vals[(s-1,i)],vals[(s-1,i^off)]
   vals[(s,i)]=mod.gate_value(modes[(s,i)],a,b)
 outs=[vals[(len(offs),i)] for i in range(w)]
 assert outs==[bits[j] for j in target]
 z=mod.honest_vector(payload,sm,modes,vals);t=mod.target_y(payload,sm,modes,outs)
 y=mod.matvec(payload['C']['shape'],payload['C']['entries'],z)
 assert sum((a-b)**2 for a,b in zip(y,t))==w*(len(offs)+1)
 assert mod.matvec(payload['D']['shape'],payload['D']['entries'],y+z)==[0]*payload['C']['shape'][0]
 records.append({'width':w,'actual_stages':len(offs),'reachable_permutations':len(layers[-1]),
  'expected_factorial':len(allperms),'reversal_settings_verified_in_C_D':True})
print('two-cycle butterfly permutation routing: PASS')
for r in records:print(r)
print('scope: exhaustive W=4,8 only; no all-width routing or formula-compilation theorem')
