#!/usr/bin/env python3
"""Verify cyclic induced subsets where every vertex misses at least three colors."""
import itertools,json
for p,k,N,path in [(509,7,15,'experiments/miss3_509_15.json'),(1021,8,25,'experiments/miss3_1021_25.json')]:
 D=json.load(open(path));V=D['vertices'];C=D['classes'];col={x:i for i,S in enumerate(C) for x in S};assert len(V)==N
 for a,b,c in itertools.combinations(V,3):assert len({col[(b-a)%p],col[(c-a)%p],col[(c-b)%p]})>1
 miss=[set(range(k))-{col[(b-a)%p] for b in V if b!=a} for a in V];assert min(map(len,miss))>=3
 print('verified three-missing cyclic K_%d: global %d, min missing %d'%(N,k,min(map(len,miss))))
