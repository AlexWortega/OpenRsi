#!/usr/bin/env python3
# Question: among centroid-zero integer tetrahedra with vertices in [-1,3]^3, which lattice-free ones maximize volume?
import json,itertools,time
import numpy as np
pts=[p for p in itertools.product(range(-1,4),repeat=3)];PSET=set(pts)
# Determinant-based strict containment, exact Python integers.
def det3(a,b,c):
 return (a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0]))
def sub(a,b):return tuple(a[i]-b[i] for i in range(3))
def interior(v,p):
 # Cramer's barycentric numerators relative to v3; all must have strict sign of D.
 a,b,c,d=v; A=sub(a,d);B=sub(b,d);C=sub(c,d);q=sub(p,d);D=det3(A,B,C)
 ns=[det3(q,B,C),det3(A,q,C),det3(A,B,q)]
 ns.append(D-sum(ns))
 return all(n>0 for n in ns) if D>0 else all(n<0 for n in ns)
best=-1; winners=[]; feasible=0;t=time.time()
for a,b,c in itertools.combinations(pts,3):
 d=tuple(-a[i]-b[i]-c[i] for i in range(3))
 if d not in PSET or not (c<d):continue # unique sorted quadruple a<b<c<d
 D=det3(sub(a,d),sub(b,d),sub(c,d))
 if not D:continue
 lo=[min(x[i] for x in (a,b,c,d)) for i in range(3)]; hi=[max(x[i] for x in (a,b,c,d)) for i in range(3)]
 bad=False
 for p in itertools.product(*(range(lo[i]+1,hi[i]) for i in range(3))):
  if p!=(0,0,0) and interior((a,b,c,d),p):bad=True;break
 if bad:continue
 feasible+=1;ad=abs(D)
 if ad>best:best=ad;winners=[(a,b,c,d)]
 elif ad==best:winners.append((a,b,c,d))
out={'box':[-1,3],'feasible':feasible,'max_det':best,'max_volume':best/6,'winner_count':len(winners),'winners':winners,'seconds':time.time()-t}
with open('experiments/integer_tetrahedra_box.json','w') as f:json.dump(out,f,indent=2)
print(json.dumps({k:v for k,v in out.items() if k!='winners'}))
