#!/usr/bin/env python3
"""Exact depth obstruction for the frozen U0a butterfly artifacts.

Every numerical dependency edge goes from stage s-1 to stage s.  Therefore a
strict NAND dependency chain can use at most `gate_stages` programmed gate
nodes after a source.  The verifier constructs a chain with one more gate at
each frozen width and certifies that no order-preserving stage injection exists.
This kills universality of the frozen topology for those explicit chains; it
does not rule out adding polynomially many repeated computation stages.
"""
import json
from pathlib import Path
WIDTHS=(8,16,32)
records=[]
for w in WIDTHS:
 p=Path(__file__).with_name('artifacts')/f'u0a_universal_topology_w{w}.json'
 d=json.loads(p.read_text()); L=d['gate_stages']
 edges=[r for r in d['row_marks'] if r['kind']=='EDGE_CONSISTENCY']
 assert edges and all(r['parent_stage']==r['stage']-1 for r in edges)
 assert {r['stage'] for r in edges}==set(range(1,L+1))
 # Dynamic longest gate path by stage.  All parents lie exactly one stage back.
 longest={0:0}
 for s in range(1,L+1):longest[s]=1+longest[s-1]
 assert longest[L]==L
 chain_gates=L+1
 # An embedding of a strict dependency chain requires strictly increasing
 # integer stages in {1,...,L}; pigeonhole/order bound makes this impossible.
 possible_stage_sequences=[]
 # Avoid exponential enumeration: recurrence count C(L,k), with zero once k>L.
 counts=[0]*(chain_gates+1);counts[0]=1
 for _stage in range(1,L+1):
  for k in range(chain_gates,0,-1):counts[k]+=counts[k-1]
 assert counts[chain_gates]==0 and counts[L]==1
 records.append({'width':w,'available_gate_stages':L,
                 'obstructing_nand_chain_gates':chain_gates,
                 'stage_injections':counts[chain_gates]})
print('frozen U0a depth obstruction: PASS')
for r in records:print(r)
print('scope: finite artifacts only; repair is to add enough repeated computation stages and prove polynomial compilation')
