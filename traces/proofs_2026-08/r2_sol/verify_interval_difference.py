#!/usr/bin/env python3
"""Verify explicit interval translation-difference colorings."""
import itertools,json
for N,k,path in [(128,5,'experiments/interval_128_5.json'),(256,6,'experiments/interval_256_6.json'),(512,7,'experiments/interval_512_7.json'),(1024,8,'experiments/interval_1024_8.json'),(2048,9,'experiments/interval_2048_9.json')]:
 D=json.load(open(path));c=D['colors'];assert (D['N'],D['k'],len(c))==(N,k,N) and set(c[1:])<=set(range(k))
 for a in range(1,N):
  for b in range(a+1,N):assert not(c[a]==c[b]==c[b-a])
 count=N*(N-1)*(N-2)//6
 print('verified interval K_%d with %d colors:'%(N,k),count,'triangles')
