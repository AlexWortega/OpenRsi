#!/usr/bin/env python3
"""Finite resource counterexample for full token-map snapshots per event.

Sparse mode emission is repaired, but the optional event certificate currently
stores complete before/after live-token maps at every raw stage.  Under a fresh
256 MiB cap a valid 1,025-leaf distinct-variable comb raises MemoryError.  A
129-leaf control succeeds.  This concerns the Python certificate object, not
compiler mathematics; delta or checkpoint certificates may repair it.
"""
import resource,subprocess,sys,json
from pathlib import Path
from verify_u0a_sparse_program_stream import compile_formula_sparse
CAP=256

def comb(n):
 f=0
 for i in range(1,n):f=(i,f)
 return f

def child(n):
 cap=CAP*1024*1024;resource.setrlimit(resource.RLIMIT_AS,(cap,cap))
 try:
  p=compile_formula_sparse(comb(n),assert_bit=1)
 except MemoryError:
  print('MEMORY_ERROR');return 0
 print(json.dumps({'result':'PASS','leaves':n,'width':p['width'],'events':len(p['event_certificate']['events']),
  'overrides':len(p['raw_gate_overrides'])},sort_keys=True));return 0

def run(n):
 q=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--child',str(n)],capture_output=True,text=True,timeout=90)
 assert q.returncode==0,(q.returncode,q.stdout,q.stderr);return q.stdout.strip()

def main():
 if len(sys.argv)==3 and sys.argv[1]=='--child':raise SystemExit(child(int(sys.argv[2])))
 small=run(129);large=run(1025)
 assert '"result": "PASS"' in small
 assert large=='MEMORY_ERROR',large
 print('PASS: full token-map event certificate resource counterexample')
 print('cap_MiB',CAP,'small',small,'large_1025',large)
 print('scope: finite Python certificate resource failure; delta/checkpoint streaming may repair it')
if __name__=='__main__':main()
