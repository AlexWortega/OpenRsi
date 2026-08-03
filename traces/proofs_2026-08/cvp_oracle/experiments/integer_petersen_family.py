#!/usr/bin/env python3
"""Closed-form scaling of the integer mixed-characteristic Petersen cheat."""
from __future__ import annotations

def record(copies:int):
    N=10*copies;adj=15*copies;nonadj=N*(N-1)//2-adj
    # singleton: 4 coeff -20 and 9 coeff 9
    # adjacent pair: 8 coeff -10 and 27 coeff 3
    # nonadjacent pair: 16 coeff -5 and 81 coeff 1
    weight=N*(4+9)+adj*(8+27)+nonadj*(16+81)
    sq=N*(4*20**2+9*9**2)+adj*(8*10**2+27*3**2)+nonadj*(16*5**2+81)
    K=N+N*(N-1)//2
    return {'copies':copies,'vertices':N,'groups_K':K,'pseudo_support':weight,'squared_norm':sq,
            'support_over_K':weight/K,'squared_norm_over_K':sq/K}
def run():
    out=[record(s) for s in (1,2,3,10,100,10000)]
    print(out);return out
if __name__=='__main__':run()
