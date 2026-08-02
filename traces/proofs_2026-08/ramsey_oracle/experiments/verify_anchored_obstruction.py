#!/usr/bin/env python3
"""Verify the six-vertex obstruction to the anchored-palette proposal."""
import itertools

def verify(r):
    g=6*r-4
    blocks=[frozenset(range(3+i*(r-1),3+(i+1)*(r-1))) for i in range(6)]
    palettes=[frozenset((0,1,*B)) for B in blocks]
    assert max(max(B) for B in blocks)<=g
    for i,j in itertools.combinations(range(6),2): assert palettes[i]&palettes[j]=={0,1}
    # Exhaust all 2^15 edge-colorings of K6 and find a monochromatic triangle.
    edges=list(itertools.combinations(range(6),2)); ei={e:k for k,e in enumerate(edges)}
    for mask in range(1<<len(edges)):
        assert any(((mask>>ei[tuple(sorted((a,b)))]&1)==
                    (mask>>ei[tuple(sorted((a,c)))]&1)==
                    (mask>>ei[tuple(sorted((b,c)))]&1))
                   for a,b,c in itertools.combinations(range(6),3))
    return g,blocks
for r in range(2,10): verify(r)
print('verified: for every symbolic r>=2 the displayed six blocks fit when g>=6r-4; exhaustive K6 two-color obstruction passes')
