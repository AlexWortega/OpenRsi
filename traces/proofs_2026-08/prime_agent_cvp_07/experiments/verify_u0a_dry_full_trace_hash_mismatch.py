#!/usr/bin/env python3
"""Regression for the repaired eager/dry scheduler trace hash mismatch.

The eager WAIT logger now records the physical stage dimension before appending
the stage.  Its framed unpadded trace is exactly the dry-run stream hash.  A
locally corrupted legacy label reproduces the retired mismatch hash.
"""
import hashlib
from verify_u0a_butterfly_formula_compiler import canonical,compile_formula,compile_formula_dry_run

def framed(events):
 h=hashlib.sha256()
 for e in events:
  b=canonical(e).encode('ascii');h.update(len(b).to_bytes(8,'big'));h.update(b)
 return h.hexdigest()
formula=(0,(0,0));eager=compile_formula(formula);dry=compile_formula_dry_run(formula)
unpadded=[e for e in eager['trace'] if e['kind'] not in ('PAD','CLEANUP')]
assert unpadded[1]=={'kind':'WAIT','dimension':0}
assert framed(unpadded)==dry['unpadded_trace_sha256']=='75c3037cf242a9d838b54a5d95c4d00b79e59242c8587af3929cda3b773a5d63'
legacy=[]
logw=eager['width'].bit_length()-1
for stage,e in enumerate(unpadded,1):
 e=dict(e)
 if e['kind']=='WAIT':
  # Retired eager logger called current_dim only after appending this stage.
  e['dimension']=(stage//2)%logw
 legacy.append(e)
assert framed(legacy)=='d19db47af2a7883dea21b7a92c8bc082848c55a68e41ebcc2914dc85b8c3b85f'
print('PASS: eager/dry trace hashes agree after WAIT-label repair')
print('formula',formula,'hash',dry['unpadded_trace_sha256'])
print('scope: finite metadata regression; no routing/soundness theorem')
