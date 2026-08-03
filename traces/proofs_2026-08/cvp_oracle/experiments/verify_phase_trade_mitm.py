#!/usr/bin/env python3
"""Verify deterministic larger-q phase trade searches through support five."""
import sys
sys.path.insert(0,'experiments')
from phase_trade_mitm import run
r4=run(4,500,59);r8=run(8,500,59);r16=run(16,300,59)
assert r4['shortest_odd_trade_histogram']=={None:354,3:91,5:55}
assert r8['shortest_odd_trade_histogram']=={None:481,3:11,5:8}
assert r16['shortest_odd_trade_histogram']=={None:300}
print('phase MITM finite claims verified')
