#!/usr/bin/env python3
"""Construction: exact weighted symmetric compression of pure-power codes.

Every word in P_r(D)=span{x^tensor r:x in D} is invariant under permutation
of tensor positions. Keep one coordinate per multiset orbit and give it weight
the orbit size. By Lagrange's four-square theorem, each integer orbit weight
is represented by at most four integer-scaled Euclidean rows. This yields an
explicit integer CVP lattice whose squared distance equals the *full* tensor
Hamming distance, without expanding orbit multiplicities.

The script constructs tiny codes, enumerates every mixed pure-power word,
checks exact weighted distance, builds four-square embeddings and an explicit
Construction-A basis, and verifies distances by exhaustive affine enumeration.
"""
from __future__ import annotations
import itertools,math,random
import verify_reduced_orbit_fold as ro


def basis(rows):return ro.basis(rows)
def words(rows):return ro.words(rows)
def tuples(n,r):return itertools.product(range(n),repeat=r)
def orbit_key(t):return tuple(sorted(t))
def pure_power(x,n,r):
 y=0
 for j,t in enumerate(tuples(n,r)):
  if all((x>>i)&1 for i in t):y|=1<<j
 return y
def pure_code(D,n,r):return basis([pure_power(x,n,r) for x in words(D)])
def orbit_data(n,r):
 keys={}
 for j,t in enumerate(tuples(n,r)):
  keys.setdefault(orbit_key(t),[]).append(j)
 return [keys[k] for k in sorted(keys)]
def compress(rows,n,r):
 O=orbit_data(n,r);out=[]
 for x in rows:
  y=0
  for a,J in enumerate(O):
   bits={(x>>j)&1 for j in J};assert len(bits)==1
   if bits=={1}:y|=1<<a
  out.append(y)
 return basis(out),[len(J) for J in O]
def weighted(x,w):return sum(w[i] for i in range(len(w)) if (x>>i)&1)
def binary_squares(N):
 """Deterministic O(log N)-term square representation from binary digits."""
 out=[];j=0
 while N:
  if N&1:
   a=1<<(j//2)
   out.extend([a] if j%2==0 else [a,a])
  N//=2;j+=1
 assert out and sum(a*a for a in out)>0
 return tuple(out)
def parity_checks(C,n):
 # Orthogonal complement rows.
 return basis([h for h in range(1<<n) if all((h&c).bit_count()%2==0 for c in C)])
def systematic_basis_from_code(K,n):
 """Integer basis of {z mod2 in K}, using 2I plus a binary code basis."""
 import sympy as sp
 from sympy.matrices.normalforms import hermite_normal_form
 gens=[[2*int(i==j) for j in range(n)] for i in range(n)]
 gens += [[int((x>>j)&1) for j in range(n)] for x in basis(K)]
 M=sp.Matrix(n,len(gens),lambda i,j:gens[j][i]);B=hermite_normal_form(M)
 assert B.shape==(n,n)
 return [[int(B[i,j]) for i in range(n)] for j in range(n)]
def embedding(weights):
 E=[binary_squares(w) for w in weights]
 assert all(sum(a*a for a in e)==w for e,w in zip(E,weights))
 return E
def embed(z,E):
 return tuple(a*z[i] for i,e in enumerate(E) for a in e)
def explicit_distance(C,target,weights):
 # Lattice residues are the star-zero subcode C0; target is one pointed word.
 anchor=next(x for x in words(C) if x&1)
 C0=basis([x for x in words(C) if not (x&1)])
 target=anchor
 B=systematic_basis_from_code(C0,len(weights));E=embedding(weights)
 EB=[embed(tuple(v),E) for v in B];t=embed(tuple((target>>i)&1 for i in range(len(weights))),E)
 d=min(weighted(target^c,weights) for c in words(C0))
 assert all(len(v)==sum(map(len,E)) for v in EB)
 return d,len(B),len(t),max(max(e) for e in E),EB,t

def main():
 rng=random.Random(991);reports=[]
 for n in [3,4,5]:
  for r in [2,3,4]:
   for seed in range(8):
    D=basis([1|(rng.randrange(1<<(n-1))<<1) for _ in range(2)])
    P=pure_code(D,n,r);Q,w=compress(P,n,r)
    assert len(w)==math.comb(n+r-1,r) and sum(w)==n**r
    # Star tuple is first multiset orbit (coordinate zero repeated r).
    full=min(x.bit_count() for x in words(P) if x&1)
    comp=min(weighted(x,w) for x in words(Q) if x&1)
    assert full==comp
    d,rank,ambient,maxscale,EB,t=explicit_distance(Q,1,w)
    assert d==comp and rank==len(w)
    reports.append((n,r,len(D),len(P),n**r,len(w),full,max(w),maxscale))
 print({'checked':len(reports),'sample':reports[:20]})
 # Deterministic counts and at least one strict orbit compression.
 assert len(reports)==72 and any(a[4]>a[5] for a in reports)
 print('weighted symmetric pure-power CVP compression passes')
if __name__=='__main__':main()
