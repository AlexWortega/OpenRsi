#!/usr/bin/env python3
"""Verify closed-form scaling of integer Petersen all-pairs witnesses."""
import sys
sys.path.insert(0,'experiments')
from integer_petersen_family import run
r=run()
assert r[0]['pseudo_support']==3565 and r[0]['squared_norm']==53365
# Ratios approach nonadjacent-pair constants 97 and 481.
assert r[-1]['support_over_K']<98 and r[-1]['support_over_K']>96
assert r[-1]['squared_norm_over_K']<482 and r[-1]['squared_norm_over_K']>480
print('integer Petersen family scaling verified exactly')
