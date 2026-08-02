#!/usr/bin/env python3
"""Run independent verifiers for every finite construction promoted in this run."""
import os, subprocess, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
commands=[
 [sys.executable,'experiments/verify_heisenberg_partition.py'],
 [sys.executable,'experiments/verify_unitriangular_partition.py','experiments/ut3_k3_sat.json'],
 [sys.executable,'experiments/verify_unitriangular_partition.py','experiments/ut4_k5_sat.json'],
 [sys.executable,'experiments/verify_unitriangular_partition.py','experiments/ut5_k9_sat.json'],
 [sys.executable,'experiments/verify_wreath_partition.py','experiments/wreath3_k6.json'],
 [sys.executable,'experiments/verify_ut_prime_partition.py','experiments/ut3p5_k6.json'],
 [sys.executable,'experiments/verify_metacyclic_partition.py','experiments/meta_11_5_k5.json'],
 [sys.executable,'experiments/verify_permutation_state_coloring.py','experiments/permstate_n4_k5.json'],
 [sys.executable,'experiments/verify_permutation_state_coloring.py','experiments/permstate_n5_k7.json'],
 [sys.executable,'experiments/verify_permutation_state_coloring.py','experiments/permstate_n6_k10.json'],
 [sys.executable,'experiments/verify_tree_relabel_coloring.py','experiments/tree_n4_k5.json'],
 [sys.executable,'experiments/verify_tree_relabel_coloring.py','experiments/tree_n5_k7.json'],
 [sys.executable,'experiments/verify_tree_relabel_coloring.py','experiments/tree_n6_k10.json'],
]
env=dict(os.environ);env['PYTHONPATH']=os.path.join(ROOT,'experiments')
for cmd in commands:
 print('+',' '.join(cmd),flush=True)
 subprocess.run(cmd,cwd=ROOT,env=env,check=True)
print('all promoted finite claims verified')
