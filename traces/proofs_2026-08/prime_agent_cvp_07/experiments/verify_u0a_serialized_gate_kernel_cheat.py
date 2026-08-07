#!/usr/bin/env python3
"""Exact signed affine attack on the frozen U0a width-8 factor.

The physical selector identity rows prevent the local rectangle from being a
literal C-kernel vector, repairing an earlier draft.  Nevertheless the same
rectangle annihilates every nonphysical row.  Adding it to the identity-free
honest program preserves all normalization, program, edge, separator and
output coordinates, and raises exact squared energy only from 72 to 74.
This is a low-overhead localized affine ghost that U2/U3 must explicitly
classify.  By itself it is not a soundness counterexample: it is semantically
invisible and a later detector could charge its physical defect.
"""
from pathlib import Path
import importlib.util
src=Path(__file__).with_name('verify_u0a_universal_topology_serializer.py')
spec=importlib.util.spec_from_file_location('u0a_serializer',src)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
payload,_,_=mod.make_factor(8)
m,k=payload['C']['shape']; cols=payload['column_marks']; rows=payload['row_marks']
lookup={c['id']:c['index'] for c in cols}

def matvec(shape,entries,x):
 y=[0]*shape[0]
 for i,j,v in entries:y[i]+=v*x[j]
 return y

def nz(x):return [(i,a) for i,a in enumerate(x) if a]

ids=['gate:1:0:COPY_A:000','gate:1:0:COPY_A:010','gate:1:0:COPY_A:101','gate:1:0:COPY_A:111']
js=[lookup[x] for x in ids]
q=[0]*k
for j,a in zip(js,(1,-1,-1,1)):q[j]=a
Cq=matvec(payload['C']['shape'],payload['C']['entries'],q)
assert len(nz(q))==4 and sum(a*a for a in q)==4
# The only detected coordinates are the explicit physical selector rows.
assert all((value==0) if rows[i]['kind']!='PHYSICAL_SELECTOR'
           else value==q[rows[i]['selector_column']]
           for i,value in enumerate(Cq))
assert [(rows[i]['selector_column'],v) for i,v in nz(Cq)]==nz(q)
# As always for D=[I|-C], the paired movement (Cq,q) is in ker D.
assert mod.matvec(payload['D']['shape'],payload['D']['entries'],Cq+q)==[0]*m

sm,gm,vals,outs=mod.make_program(payload,'identity_free')
base=mod.honest_vector(payload,sm,gm,vals)
assert base[js[1]]==1 and sum(base[j] for j in js)==1
cheat=[a+b for a,b in zip(base,q)]
assert [cheat[j] for j in js]==[1,0,-1,1]
t=mod.target_y(payload,sm,gm,outs)
Cb=mod.matvec(payload['C']['shape'],payload['C']['entries'],base)
Cc=mod.matvec(payload['C']['shape'],payload['C']['entries'],cheat)
assert all((Cb[i]==Cc[i]) for i,r in enumerate(rows) if r['kind']!='PHYSICAL_SELECTOR')
Ebase=sum((a-b)**2 for a,b in zip(Cb,t)); Echeat=sum((a-b)**2 for a,b in zip(Cc,t))
assert (Ebase,Echeat)==(72,74)
assert mod.matvec(payload['D']['shape'],payload['D']['entries'],Cc+cheat)==[0]*m

# All affine/constant local modes have the same nonphysical rectangle.
count=0
for s in range(1,payload['gate_stages']+1):
 for lane in range(payload['width']):
  for mode in ('COPY_A','COPY_B','ZERO','ONE'):
   modecols=[c for c in cols if c['stage']==s and c['lane']==lane and c['kind']=='GATE_SELECTOR' and c['state']['mode']==mode]
   byab={(c['state']['a'],c['state']['b']):c['index'] for c in modecols}; qq=[0]*k
   for ab,a in [((0,0),1),((0,1),-1),((1,0),-1),((1,1),1)]:qq[byab[ab]]=a
   image=mod.matvec(payload['C']['shape'],payload['C']['entries'],qq)
   assert all(v==0 for i,v in enumerate(image) if rows[i]['kind']!='PHYSICAL_SELECTOR')
   assert sum(v*v for i,v in enumerate(image) if rows[i]['kind']=='PHYSICAL_SELECTOR')==4
   count+=1
assert count==payload['gate_stages']*payload['width']*4==256
# Repeat the same exact local witness at every frozen width.  This is finite
# evidence only, not an asymptotic statement.
energy_table=[]
for ww in mod.WIDTHS:
 pp,_,_=mod.make_factor(ww); cc=pp['column_marks']; rr=pp['row_marks']; lk={c['id']:c['index'] for c in cc}
 jj=[lk[x] for x in ids]; qq=[0]*len(cc)
 for j,a in zip(jj,(1,-1,-1,1)):qq[j]=a
 ssm,ggm,vvals,oouts=mod.make_program(pp,'identity_free')
 bb=mod.honest_vector(pp,ssm,ggm,vvals); assert bb[jj[1]]==1
 bad=[a+b for a,b in zip(bb,qq)]; tt=mod.target_y(pp,ssm,ggm,oouts)
 by=mod.matvec(pp['C']['shape'],pp['C']['entries'],bb)
 cy=mod.matvec(pp['C']['shape'],pp['C']['entries'],bad)
 assert all(by[i]==cy[i] for i,r in enumerate(rr) if r['kind']!='PHYSICAL_SELECTOR')
 eb=sum((a-b)**2 for a,b in zip(by,tt)); ec=sum((a-b)**2 for a,b in zip(cy,tt))
 assert ec==eb+2
 energy_table.append((ww,eb,ec))
assert energy_table==[(8,72,74),(16,176,178),(32,416,418)]
print('verified frozen U0a serialized-gate affine attack')
print('base_energy',Ebase,'malformed_energy',Echeat,'excess',Echeat-Ebase)
print('witness_ids',ids,'coefficients',(1,-1,-1,1))
print('all affine/constant gate rectangles',count)
print('frozen_width_energy_table',energy_table)
print('scope: low-overhead localized affine ghost; does not alone kill soundness because later detectors may charge it')
