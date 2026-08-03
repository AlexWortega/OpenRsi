#!/usr/bin/env python3
"""Run exact output-size accounting for global field fingerprints."""
import runpy
ns=runpy.run_path('experiments/field_fingerprint_output_accounting.py')
records=ns['records']
assert records[0]['assignments_q']==256
assert records[-1]['minimum_feature_rows']==2**128-1
print('global field-fingerprint output accounting verifier passed')
