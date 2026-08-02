#!/usr/bin/env python3
"""Verify induced cyclic subsets where every vertex misses at least two colors."""
import itertools,json
for p,k,N,path in [(127,5,10,'experiments/multimiss_127_10.json'),(251,6,15,'experiments/multimiss_251_15.json'),(509,7,25,'experiments/multimiss_509_25.json'),(509,7,50,'experiments/multimiss_509_50.json'),(1021,8,80,'experiments/multimiss_1021_80.json'),(2039,9,130,'experiments/multimiss_2039_130.json')]:
 D=json.load(open(path));V=D['vertices'];C=D['classes'];col={x:i for i,S in enumerate(C) for x in S};assert len(V)==N
 for a,b,c in itertools.combinations(V,3):assert len({col[(b-a)%p],col[(c-a)%p],col[(c-b)%p]})>1
 miss=[]
 for a in V:miss.append(set(range(k))-{col[(b-a)%p] for b in V if b!=a})
 assert min(map(len,miss))>=2
 print('verified multi-missing cyclic K_%d: global %d, min missing %d'%(N,k,min(map(len,miss))))
