#!/usr/bin/env python3
"""Finite audit of the parameterized-depth U0a serializer.

The serializer now accepts any positive gate depth at a power-of-two width.
For (W,T)=(4,5),(8,9),(16,17),(32,33), this verifier emits the actual C,D,
checks closed dimension formulas and the explicit physical identity submatrix,
and programs T parallel levels of NAND(x,x).  With a uniform FREE input of the
correct parity the fixed all-one output target is attained at the common
physical energy; the opposite input misses every output row.

This repairs the previously certified shallow-depth obstruction for this one
chain family.  It is finite evidence, not a compiler for arbitrary formulas or
an all-parameter theorem.
"""
from pathlib import Path
import importlib.util
src=Path(__file__).with_name('verify_u0a_universal_topology_serializer.py')
spec=importlib.util.spec_from_file_location('u0a',src)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
CASES=((4,5),(8,9),(16,17),(32,33))

def chain_program(payload,input_bit):
 w=payload['width'];T=payload['gate_stages']
 sm=['FREE']*w;gm={(s,i):'NAND' for s in range(1,T+1) for i in range(w)}
 vals={(0,i):input_bit for i in range(w)}
 logw=w.bit_length()-1
 for s in range(1,T+1):
  off=1<<(((s-1)//2)%logw)
  for i in range(w):
   a,b=vals[(s-1,i)],vals[(s-1,i^off)]
   assert a==b
   vals[(s,i)]=mod.gate_value('NAND',a,b)
 return sm,gm,vals,[vals[(T,i)] for i in range(w)]

def energy(payload,z,t):
 y=mod.matvec(payload['C']['shape'],payload['C']['entries'],z)
 return sum((a-b)**2 for a,b in zip(y,t)),y

records=[]
for w,T in CASES:
 payload,_,_=mod.make_factor(w,gate_stages=T);m,k=payload['C']['shape']
 assert k==4*w+20*w*T
 assert m==30*w*T+9*w-2*T
 assert payload['D']['shape']==[m,m+k]
 # Physical rows form an explicit selector identity block, proving finite full
 # column rank without a numerical rank routine.
 physical=[r for r in payload['row_marks'] if r['kind']=='PHYSICAL_SELECTOR']
 assert len(physical)==k
 byrow={r['index']:[] for r in physical}
 for i,j,v in payload['C']['entries']:
  if i in byrow:byrow[i].append((j,v))
 assert all(byrow[r['index']]==[(r['selector_column'],1)] for r in physical)
 # Choose parity so T repeated negations end at one.
 good_input=1 if T%2==0 else 0
 sm,gm,vals,outs=chain_program(payload,good_input);assert outs==[1]*w
 z=mod.honest_vector(payload,sm,gm,vals);t=mod.target_y(payload,sm,gm,[1]*w)
 eg,yg=energy(payload,z,t);nodes=w*(T+1);assert eg==nodes
 assert mod.matvec(payload['D']['shape'],payload['D']['entries'],yg+z)==[0]*m
 # The opposite uniform free input uses the same program target but outputs 0.
 sm2,gm2,vals2,outs2=chain_program(payload,1-good_input);assert outs2==[0]*w
 z2=mod.honest_vector(payload,sm2,gm2,vals2);eb,yb=energy(payload,z2,t)
 assert eb==nodes+w
 assert len(payload['C']['entries']) <= 100*w*T*(w.bit_length())
 records.append({'width':w,'gate_depth':T,'chain_levels_computed':T,
  'C_shape':[m,k],'C_nnz':len(payload['C']['entries']),
  'accepted_input':good_input,'accepted_energy':eg,
  'rejected_input':1-good_input,'rejected_energy':eb})
print('parameterized-depth NAND-chain serializer: PASS')
for r in records:print(r)
print('scope: finite chain-family completeness and polynomial-size formulas only; arbitrary formula compilation remains open')
