#!/usr/bin/env python3
"""Compile and verify exact permanent diagnostics for C5/Mycielski levels 0..2."""
import os,subprocess,tempfile,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with tempfile.TemporaryDirectory() as d:
 exe=d+'/p';subprocess.run(['g++','-O3','-std=c++17','experiments/permutation_orbit_capacity.cpp','-o',exe],cwd=ROOT,check=True)
 got=[]
 for l in range(3):
  s=subprocess.check_output([exe,str(l)],text=True,timeout=120);print(s.strip())
  m=re.search(r'n=(\d+) D=([^ ]+).*base=([^ ]+)',s);assert m;got.append((int(m[1]),float(m[2]),float(m[3])))
assert [x[0] for x in got]==[5,11,23]
assert abs(got[0][1]-13)<.1 and abs(got[1][1]-583659)<.1
assert all(got[i][2]>got[i+1][2] for i in range(2))
print('PASS: exact subset-DP permanent diagnostics')
