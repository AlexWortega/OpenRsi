#!/usr/bin/env python3
"""Exhaustively verify centroid-zero integer tetrahedra in [-2,4]^3."""
import itertools
pts=list(itertools.product(range(-2,5),repeat=3));S=set(pts)
def sub(a,b):return tuple(a[i]-b[i] for i in range(3))
def det(a,b,c):return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
def inside(v,p):
 a,b,c,d=v;A=sub(a,d);B=sub(b,d);C=sub(c,d);q=sub(p,d);D=det(A,B,C)
 ns=[det(q,B,C),det(A,q,C),det(A,B,q)];ns+=[D-sum(ns)]
 return all(x>0 for x in ns) if D>0 else all(x<0 for x in ns)
best=feasible=tested=0;W=[]
for a,b,c in itertools.combinations(pts,3):
 d=tuple(-a[i]-b[i]-c[i] for i in range(3))
 if d not in S or not c<d:continue
 tested+=1;v=(a,b,c,d);D=det(sub(a,d),sub(b,d),sub(c,d))
 if not D:continue
 lo=[min(x[i] for x in v) for i in range(3)];hi=[max(x[i] for x in v) for i in range(3)]
 if any(p!=(0,0,0) and inside(v,p) for p in itertools.product(*(range(lo[i]+1,hi[i]) for i in range(3)))):continue
 feasible+=1
 if abs(D)>best:best=abs(D);W=[v]
 elif abs(D)==best:W.append(v)
assert (tested,feasible,best,len(W))==(135534,26928,64,19)
# Every maximizer has edge-lattice Smith invariants (4,4,4): gcd entries=4 and determinant=64.
for v in W:
 M=[[v[j][i]-v[0][i] for j in range(1,4)] for i in range(3)]
 assert all(x%4==0 for row in M for x in row) and abs(det(*zip(*M)))==64
print('verified [-2,4]^3: 26928 feasible; 19 maximizers, volume 32/3, edge lattice 4Z^3 up to unimodular basis')
