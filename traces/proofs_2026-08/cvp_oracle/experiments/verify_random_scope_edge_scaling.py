#!/usr/bin/env python3
"""Verify random-scope coverage/output arithmetic table."""
import sys
sys.path.insert(0,'experiments')
from random_scope_edge_scaling import run
r=run()
assert len(r)==12
assert r[0]['required_scopes_union_bound']==5586
assert r[3]['required_scopes_union_bound']==120658
assert r[6]['required_scopes_union_bound']==2420353
assert r[9]['required_scopes_union_bound']==46504956
assert all(x['column_upper']==x['required_scopes_union_bound']*x['views_upper_per_scope'] for x in r)
print('random-scope coverage/output arithmetic verified')
