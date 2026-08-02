#!/usr/bin/env python3
"""Verify explicit locally-four-colored seeds using five global colors."""
import itertools,json
for N,g,s,path in [(20,5,4,'experiments/local_20_g5_s4.json'),(25,5,4,'experiments/local_25_g5_s4.json'),(26,5,4,'experiments/local_26_g5_s4.json'),(50,6,5,'experiments/local_50_g6_s5.json'),(55,6,5,'experiments/local_55_g6_s5.json'),(56,6,5,'experiments/local_56_g6_s5.json'),(57,6,5,'experiments/local_57_g6_s5.json')]:
 D=json.load(open(path));P=list(map(set,D['palettes']));E={tuple(map(int,k.split(','))):v for k,v in D['edge_colors'].items()}
 assert (D['N'],D['g'],D['s'])==(N,g,s) and len(P)==N and all(len(x)<=s and x<=set(range(g)) for x in P)
 assert set(E)==set(itertools.combinations(range(N),2))
 for (a,b),c in E.items():assert c in P[a]&P[b]
 for a,b,c in itertools.combinations(range(N),3):assert len({E[(a,b)],E[(a,c)],E[(b,c)]})>1
 used=[{E[tuple(sorted((v,w)))] for w in range(N) if w!=v} for v in range(N)]
 assert max(map(len,used))<=s
 print('verified locally-%d K%d with %d global colors; incident palette sizes'%(s,N,g),list(map(len,used)))
