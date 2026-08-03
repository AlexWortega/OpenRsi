#!/usr/bin/env python3
"""Exhaustively verify pointed-distance tensor multiplicativity on random tiny codes."""
import itertools, random, numpy as np

def span_words(G):
    k,L=G.shape
    return [np.bitwise_xor.reduce(G[[i for i,b in enumerate(bits) if b]],axis=0)
            if any(bits) else np.zeros(L,dtype=np.uint8)
            for bits in itertools.product((0,1),repeat=k)]

def pointed(G,star):
    ws=span_words(G)
    return min(int(w.sum()) for w in ws if w[star])

def independent_rows(rows):
    basis={}
    for arr in rows:
        mask=sum(int(b)<<i for i,b in enumerate(arr))
        x=mask
        while x:
            p=x.bit_length()-1
            if p not in basis: basis[p]=x; break
            x^=basis[p]
    return len(basis)==len(rows)

def main():
    rng=random.Random(7); checked=0
    for _ in range(100):
        L=rng.choice((3,4)); k=rng.choice((1,2))
        while True:
            G=np.array([[rng.randrange(2) for _ in range(L)] for _ in range(k)],dtype=np.uint8)
            if independent_rows(G): break
        star=rng.randrange(L)
        if not any(w[star] for w in span_words(G)): continue
        H=G
        ds=[]
        for q in range(1,4):
            if q>1: H=np.array([np.kron(a,b)%2 for a in H for b in G],dtype=np.uint8)
            d=pointed(H, sum(star*(L**j) for j in range(q)))
            ds.append(d)
            assert d==pointed(G,star)**q
        checked+=1
    print({'random_codes_checked':checked,'powers_through':3})
if __name__=='__main__': main()
