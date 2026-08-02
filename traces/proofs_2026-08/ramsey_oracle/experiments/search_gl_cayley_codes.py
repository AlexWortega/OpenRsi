#!/usr/bin/env python3
"""Search matrix-orbit codes over F_2^d against nonlinear sum-free Cayley sets."""
import random,sys,math
from itertools import combinations
import networkx as nx

def rank(rows,d):
 r=0
 for bit in reversed(range(d)):
  p=next((i for i in range(r,d) if rows[i]>>bit&1),None)
  if p is not None:
   rows[r],rows[p]=rows[p],rows[r]
   for i in range(d):
    if i!=r and rows[i]>>bit&1:rows[i]^=rows[r]
   r+=1
 return r

def gl(d):
 out=[]
 # matrix word stores d columns, each d bits
 for z in range(1<<(d*d)):
  cols=[(z>>(d*j))&((1<<d)-1) for j in range(d)]
  rows=[sum(((cols[j]>>i)&1)<<j for j in range(d)) for i in range(d)]
  if rank(rows[:],d)==d:out.append(tuple(cols))
 return out

def sumfree(S):
 S=set(S)
 return all((a^b) not in S for a,b in combinations(S,2))

def maximal_caps(d,tries=1000):
 vals=list(range(1,1<<d));seen=set();out=[]
 # include affine hyperplanes and random greedy caps
 for mask in range(1,1<<d):
  S=frozenset(x for x in vals if (x&mask).bit_count()%2)
  seen.add(S);out.append(S)
 for _ in range(tries):
  random.shuffle(vals);S=[]
  for x in vals:
   if all((x^y) not in S for y in S):S.append(x)
  S=frozenset(S)
  if S not in seen:seen.add(S);out.append(S)
 return out

def greedy_code(M,S,runs=100):
 n=len(M);best=[];order=list(range(n));S=set(S)
 def good(i,j):return any((a^b) in S for a,b in zip(M[i],M[j]))
 for _ in range(runs):
  random.shuffle(order);C=[]
  for i in order:
   if all(good(i,j) for j in C):C.append(i)
  if len(C)>len(best):best=C[:]
 return best

def exact_code(M,S):
 G=nx.Graph();G.add_nodes_from(range(len(M)));S=set(S)
 for i in range(len(M)):
  for j in range(i):
   if any((a^b) in S for a,b in zip(M[i],M[j])):G.add_edge(i,j)
 # Exact maximum clique by complement maximum independent set, with timeout handled outside.
 C=max(nx.find_cliques(G),key=len)
 return C

d=int(sys.argv[1]) if len(sys.argv)>1 else 3
random.seed(1);M=gl(d);caps=maximal_caps(d,2000 if d<=4 else 200)
print('d',d,'GL',len(M),'caps',len(caps),flush=True)
best=(0,None,None)
for z,S in enumerate(caps):
 C=greedy_code(M,S,200 if d==3 else 10)
 if len(C)>best[0]:
  best=(len(C),S,C);print('best',len(C),'cap',len(S),'base',len(C)**(1/d),sorted(S),flush=True)
print('FINAL',best[0],best[0]**(1/d))
