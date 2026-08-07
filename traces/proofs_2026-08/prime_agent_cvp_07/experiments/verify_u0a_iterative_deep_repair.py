#!/usr/bin/env python3
"""Exact repair audit for the Generation-12 deep-formula recursion witness.

The same 1,101-leaf right-deep formula is traversed, evaluated and scheduled by
iterative routines under recursion limit 1000.  The dry run streams a hash of
unpadded events and represents padding by a count, so it does not allocate the
roughly two-billion-entry dense modes grid.  Full factor/target emission is
intentionally not claimed by this verifier.
"""
import json,sys
from verify_u0a_butterfly_formula_compiler import (
    leaves_and_gates,eval_formula,compile_formula_dry_run,stage_budget)
old=sys.getrecursionlimit();sys.setrecursionlimit(1000)
try:
 formula=0
 for _ in range(1100):formula=(0,formula)
 leaves,gates,root=leaves_and_gates(formula)
 assert len(leaves)==1101 and len(gates)==1100 and root=='gate:1099'
 # NAND(x,x)=not x at the deepest gate, followed by NAND(x,previous)
 # values are checked by the iterative evaluator, not a closed-form claim.
 vals=[eval_formula(formula,{0:b}) for b in (0,1)]
 summary=compile_formula_dry_run(formula,assert_bit=1)
 assert summary['leaf_occurrences']==1101 and summary['nand_gates']==1100
 assert summary['width']==2048 and summary['gate_stages']==stage_budget(2048)==991254
 assert summary['raw_stage_count_before_padding']<summary['gate_stages']
 assert summary['pad_stages']==summary['gate_stages']-summary['raw_stage_count_before_padding']-1
 assert summary['materialized'] is False
 # Dense mode materialization would contain this many formula-program cells.
 dense_cells=summary['width']*summary['gate_stages']
 assert dense_cells==2_030_088_192
finally:
 sys.setrecursionlimit(old)
out={k:summary[k] for k in ['schema','materialized','width','gate_stages','leaf_occurrences','nand_gates','raw_stage_count_before_padding','pad_stages','event_counts','unpadded_trace_sha256']}
out['evaluations_at_x0_x1']=vals;out['omitted_dense_mode_cells']=dense_cells
out['scope']='repairs recursive traversal/evaluation/scheduling only; full C,D,target emission is still omitted'
print(json.dumps(out,indent=2,sort_keys=True))
print('PASS: iterative deep-formula traversal and streaming dry-run repair')
