#!/usr/bin/env python3
"""Exhaustively verify the centroid-zero integer-tetrahedron claim in [-1,3]^3."""
import itertools
pts=list(itertools.product(range(-1,4),repeat=3));S=set(pts)
def sub(a,b):return tuple(a[i]-b[i] for i in range(3))
def det(a,b,c):return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
def inside(v,p):
 a,b,c,d=v;A=sub(a,d);B=sub(b,d);C=sub(c,d);q=sub(p,d);D=det(A,B,C)
 ns=[det(q,B,C),det(A,q,C),det(A,B,q)];ns+=[D-sum(ns)]
 return all(n>0 for n in ns) if D>0 else all(n<0 for n in ns)
best=0; winners=[];feasible=0
for a,b,c in itertools.combinations(pts,3):
 d=tuple(-a[i]-b[i]-c[i] for i in range(3))
 if d not in S or not c<d:continue
 v=(a,b,c,d);D=det(sub(a,d),sub(b,d),sub(c,d))
 if D==0:continue
 lo=[min(x[i] for x in v) for i in range(3)];hi=[max(x[i] for x in v) for i in range(3)]
 if any(p!=(0,0,0) and inside(v,p) for p in itertools.product(*(range(lo[i]+1,hi[i]) for i in range(3)))):continue
 feasible+=1
 if abs(D)>best:best=abs(D);winners=[v]
 elif abs(D)==best:winners.append(v)
assert feasible==1078
assert best==64
assert winners==[((-1,-1,-1),(-1,-1,3),(-1,3,-1),(3,-1,-1))]
print('verified exhaustive box claim: 1078 feasible, unique maximizer, volume 64/6=32/3')
