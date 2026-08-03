#!/usr/bin/env python3
"""Output-size accounting for global field fingerprints.

If q=2^n complete assignments need at least q-1 independent feature rows for
exactness, then explicitly materializing those rows or q assignment columns is
exponential in n. This script checks representative exact integer inequalities.
"""
records=[]
for n in (8,16,32,64,128):
 q=1<<n
 # Any full-assignment group has q-1 legal columns; exact arbitrary field
 # fingerprints require m>=q-1 rows by the rank theorem.
 records.append({'n':n,'assignments_q':q,'minimum_feature_rows':q-1,
                 'columns_per_forbidden_group':q-1,'groups':q,
                 'full_table_columns':q*(q-1),
                 'both_exceed_n^10':(q-1>n**10 if n>=64 else None)})
assert all(r['both_exceed_n^10'] for r in records if r['both_exceed_n^10'] is not None)
print(records)
print('field-fingerprint exponential output accounting verified exactly')
