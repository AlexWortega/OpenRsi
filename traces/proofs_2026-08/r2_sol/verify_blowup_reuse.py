#!/usr/bin/env python3
"""Verify two missing-color K2 blow-ups directly."""
import itertools,json
cases=[]
C16=[{1,2,4,8,15},{3,5,7,10,11},{6,9,12,13,14}];cases.append(('experiments/blowup_K16x2_4.json',16,4,lambda a,b:next(i for i,S in enumerate(C16) if (a^b) in S)))
C=json.load(open('experiments/cyclic_127_5.json'));cc={x:i for i,S in enumerate(C) for x in S};cases.append(('experiments/blowup_cyclic127x2_6.json',127,6,lambda a,b:cc[(b-a)%127]))
for path,n,k,out in cases:
 D=json.load(open(path));inside=D['internal_colors'];V=list(itertools.product(range(n),range(2)))
 def color(u,v):
  return inside[u[0]] if u[0]==v[0] else out(*sorted((u[0],v[0])))
 for a,b,c in itertools.combinations(V,3):assert len({color(a,b),color(a,c),color(b,c)})>1
 print('verified missing-color blow-up K_%d with %d colors'%(2*n,k))
