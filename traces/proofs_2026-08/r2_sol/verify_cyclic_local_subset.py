#!/usr/bin/env python3
"""Verify induced cyclic seeds are triangle-free and omit a color at every vertex."""
import itertools,json
for expected,path in [(40,'experiments/cyclic127_local40.json'),(60,'experiments/cyclic251_local60.json'),(100,'experiments/cyclic509_local100.json'),(160,'experiments/cyclic1021_local160.json')]:
 D=json.load(open(path));p,k,V,C=D['p'],D['k'],D['vertices'],D['classes'];col={x:i for i,S in enumerate(C) for x in S};V=set(V)
 assert len(V)==expected
 for a,b,c in itertools.combinations(V,3):assert len({col[(b-a)%p],col[(c-a)%p],col[(c-b)%p]})>1
 used=[]
 for a in V:used.append({col[(b-a)%p] for b in V if b!=a})
 assert max(map(len,used))<=k-1
 print('verified cyclic induced K_%d: %d global colors, local sizes'% (len(V),k),list(map(len,used)))
