#!/usr/bin/env python3
"""Finite checks for sampled-tensor arbitrary-combination and layer obstructions."""
import itertools, numpy as np

def span(G):
    out=[]
    for bits in itertools.product((0,1),repeat=len(G)):
        w=np.zeros(G.shape[1],dtype=np.uint8)
        for b,g in zip(bits,G):
            if b:w^=g
        out.append(w)
    return out

def sampled_tensor_generator(G,S):
    q=len(S[0]); B=np.ones((1,len(S)),dtype=np.uint8)
    for h in range(q):
        rows=[]
        for b in B:
            for g in G: rows.append(b*np.array([g[a[h]] for a in S],dtype=np.uint8))
        # retain independent rows
        basis={}; keep=[]
        for row in rows:
            mask=sum(int(x)<<i for i,x in enumerate(row)); z=mask
            while z:
                p=z.bit_length()-1
                if p not in basis: basis[p]=z; keep.append(row); break
                z^=basis[p]
        B=np.array(keep,dtype=np.uint8) if keep else np.zeros((0,len(S)),dtype=np.uint8)
    return B

def main():
    G=np.array([[1,1,0],[1,0,1]],dtype=np.uint8)
    S=[(0,0),(0,1),(0,2),(1,1),(1,2),(2,2)]
    B=sampled_tensor_generator(G,S)
    pointed=[int(w.sum()) for w in span(B) if w[0]]
    assert min(pointed)==2

    # Sanity-check the sampling lemma on 20 deterministic lists with
    # m=4,N=8,d=3,s=2, for which 4*(3/8)^2 < 1.
    N,d,s,m=8,3,2,4
    subsets=[frozenset(i for i in range(N) if mask>>i&1) for mask in range(1<<N)]
    # Sample deterministic diverse lists rather than all C(256,4).
    lists=[]
    for shift in range(20):
        lists.append([subsets[(37*j+shift*11)%(1<<N)] for j in range(m)])
    for Ts in lists:
        def f(Z): return sum(T<=Z for T in Ts)
        C=max(f(frozenset(X)) for X in itertools.combinations(range(N),d-1))
        Bmin=min(f(frozenset(Y)) for Y in itertools.combinations(range(N),d))
        assert Bmin*(d-s+1) <= d*C
    print({'mixed_tensor_min':min(pointed),'sample_lists_checked':len(lists)})
if __name__=='__main__':main()
