#!/usr/bin/env python3
"""Independent reproducibility driver for every current-run finite claim.

Re-enumerates the symmetric C5 class, compiles/runs the directed exhaustive
search, validates its complete output, and checks the anchored K6 obstruction.
"""
import json, os, subprocess, tempfile
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, timeout=180):
    return subprocess.run(cmd,cwd=ROOT,check=True,text=True,capture_output=True,timeout=timeout).stdout

# This re-enumerates all 2^15 symmetric matrices and rewrites the certificate.
run(['python3','experiments/search_stationary_c5.py'])
with open(os.path.join(ROOT,'experiments/results/stationary_c5_symmetric.json')) as f:d=json.load(f)
assert [d['best'][str(q)]['W'] for q in range(2,7)] == [4,8,16,32,64]
assert all(d['feasible_counts'][str(q)]>0 for q in range(2,7))

with tempfile.TemporaryDirectory() as td:
    exe=os.path.join(td,'search')
    run(['g++','-O3','-std=c++17','experiments/search_stationary_c5_directed.cpp','-o',exe],30)
    out=run([exe],180)
assert 'enumerated 1048576 automata' in out
for q in range(2,9):
    line=next(x for x in out.splitlines() if x.startswith(f'q={q} '))
    assert f'bestW={2**q} ' in line, line

out=run(['python3','experiments/verify_anchored_obstruction.py'],30)
assert out.startswith('verified:')
print('PASS: symmetric C5 2^15 enumeration; directed row-degree<=2 C5 20^5 enumeration; anchored K6 obstruction')
