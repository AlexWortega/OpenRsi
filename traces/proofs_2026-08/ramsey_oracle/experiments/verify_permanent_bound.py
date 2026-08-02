#!/usr/bin/env python3
"""Finite adversarial checks for the universal permanent lower-bound proof.

1. Exact symbolic/numeric constant checks.
2. Exhaust all labeled triangle-free H through n=6; exact permanent and bound.
3. Exhaust the numeric core of the bipartite factor lemma for m<=12 by all
   (x,y,a) cardinalities, checking the proof's rectangle lower bound.
"""
import itertools,math
C=2.5*(5/3)**1.5
assert abs(C-25*math.sqrt(15)/18)<1e-12 and 5<C<5.38
# proof-core inequality: rectangle edge lower bound >= (m-2a)(x-y)
for m in range(1,13):
 for a in range(0,m+1):
  if 9*a>4*m:continue
  for x in range(m+1):
   for y in range(x):
    lower=x*(m-y)-min(a*x,a*(m-y))
    assert lower >= (m-2*a)*(x-y), (m,a,x,y)

def permanent(M):
 n=len(M);dp=[0]*(1<<n);dp[0]=1
 for s in range(1<<n):
  i=s.bit_count()
  if i==n:continue
  for j in range(n):
   if not(s>>j&1) and M[i][j]:dp[s|1<<j]+=dp[s]
 return dp[-1]
counts=[]
for n in range(1,7):
 E=list(itertools.combinations(range(n),2));ok=0
 for mask in range(1<<len(E)):
  H=[[0]*n for _ in range(n)]
  for k,(u,v) in enumerate(E):
   if mask>>k&1:H[u][v]=H[v][u]=1
  if any(H[a][b] and H[a][c] and H[b][c] for a,b,c in itertools.combinations(range(n),3)):continue
  M=[[int(i==j or not H[i][j]) for j in range(n)] for i in range(n)]
  D=permanent(M)
  assert D+1e-12 >= math.factorial(n)/C**n
  ok+=1
 counts.append(ok)
assert counts==[1,2,7,41,388,5789],counts
print('PASS: C=',C,' rectangle inequalities m<=12; triangle-free labeled counts/permanent bound n<=6:',counts)
