#!/usr/bin/env python3
"""Historical regression for the repaired deep-formula recursion bug.

A local copy of the former recursive traversal fails on the 1,101-leaf witness
at recursion limit 1000, while the current iterative `leaves_and_gates`
returns all nodes.  Full dense factor emission is outside this regression.
"""
import json,sys
from verify_u0a_butterfly_formula_compiler import leaves_and_gates

def legacy_nodes(f):
 if isinstance(f,int):return 1
 assert isinstance(f,tuple) and len(f)==2
 return legacy_nodes(f[0])+legacy_nodes(f[1])+1
old=sys.getrecursionlimit();sys.setrecursionlimit(1000)
try:
 formula=0
 for _ in range(1100):formula=(0,formula)
 failed=False
 try:legacy_nodes(formula)
 except RecursionError:failed=True
 assert failed
 leaves,gates,root=leaves_and_gates(formula)
 assert len(leaves)==1101 and len(gates)==1100 and root=='gate:1099'
finally:sys.setrecursionlimit(old)
print(json.dumps({'historical_counterexample':True,'legacy_failure':'RecursionError',
 'leaf_occurrences':len(leaves),'nand_gates':len(gates),
 'current_iterative_traversal':'PASS','scope':'parser regression only; no full dense emission'},indent=2,sort_keys=True))
print('PASS: historical recursion counterexample reproduced and iterative traversal repair checked')
