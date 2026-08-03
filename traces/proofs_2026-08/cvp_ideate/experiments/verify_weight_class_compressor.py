#!/usr/bin/env python3
"""Exact nonlinear weight-class compressor and computability attack.

For an affine binary fiber F, map every x in F to generator (1,e_|x|), with
class coordinate w carrying Euclidean squared weight w^r. Any pointed mixed
sum uses an odd number of generators, hence has an odd occupied weight class;
its cost is at least min_{x in F}|x|^r, attained by one generator. Output has
only m+2 coordinates, independent of r.

This is an exact distance compressor but constructing its generator requires
the attainable weight set. For BMT, deciding whether class q occurs is exactly
perfect matching. We test exact tiny instances and the polynomial relaxation
that includes every parity/counting-allowed class; the latter inserts class q
in NO and destroys the gap. Explicit weighted CVP bases are checked.
"""
from __future__ import annotations
import itertools,math
import verify_feature_shell_3dm as f
import verify_weighted_symmetric_cvp as ws


def fiber(q,T):return f.fiber(q,T)
def attainable(q,T):return sorted({x.bit_count() for x in fiber(q,T)})
def class_code(W,m):
 # bit0 star, bit 1+w for class w.
 return ws.basis([1|(1<<(1+w)) for w in W])
def class_weights(m,r):return [1]+[max(1,w**r) for w in range(m+1)]
def pd(C,weights):
 return min(sum(weights[j] for j in range(len(weights)) if (x>>j)&1)
            for x in ws.words(C) if x&1)
def explicit(C,weights):
 # Anchor and star-zero code, then weighted Construction-A basis.
 anchor=next(x for x in ws.words(C) if x&1);C0=ws.basis([x for x in ws.words(C) if not x&1])
 B=ws.systematic_basis_from_code(C0,len(weights));E=ws.embedding(weights)
 EB=[ws.embed(tuple(v),E) for v in B];t=ws.embed(tuple((anchor>>i)&1 for i in range(len(weights))),E)
 d=min(sum(weights[j] for j in range(len(weights)) if ((anchor^c)>>j)&1) for c in ws.words(C0))
 assert len(B)==len(weights) and all(len(v)==len(t) for v in EB)
 return d,len(B),len(t)
def relaxed_classes(q,m):
 # BMT counting/parity alone: weights >=q and congruent q mod2.
 return list(range(q,m+1,2))
def main():
 q,m=3,8;Y,N=f.families(q,m,40);reports=[]
 for r in [1,2,4,8,16]:
  yd=[];nd=[];relax=[]
  for label,fam,out in [('Y',Y,yd),('N',N,nd)]:
   for T,M,F in fam:
    W=attainable(q,T);C=class_code(W,m);weights=class_weights(m,r)
    got=pd(C,weights);want=1+min(W)**r
    assert got==want
    if r<=4:
     d,rank,ambient=explicit(C,weights);assert d==got
    out.append(got)
    R=class_code(relaxed_classes(q,m),m);relax.append((label,pd(R,weights)))
  reports.append((r,max(yd),min(nd),min(nd)/max(yd),
                  max(v for lab,v in relax if lab=='Y'),min(v for lab,v in relax if lab=='N')))
 print({'reports':reports,'example_Y_weights':attainable(q,Y[0][0]),
        'example_NO_weights':attainable(q,N[0][0])})
 assert all(a[1]==1+3**a[0] and a[2]>=1+5**a[0] for a in reports)
 # Computable parity/counting relaxation always has the false class q.
 assert all(a[4]==a[5]==1+3**a[0] for a in reports)
 # Exact reduction barrier: q belongs to attainable set iff perfect matching.
 assert all((q in attainable(q,T))==bool(M) for T,M,F in Y+N)
 print('weight-class compressor and relaxation attack pass')
if __name__=='__main__':main()
