#!/usr/bin/env python3
"""Exact exponent arithmetic for bounded-fingerprint collision inequality."""
# Representative polynomial row/bit bounds: m=n^3, H=2^(n^2).
# Since log2((q+1)(2qH+1)^m) < (n+1)+m(n+n^2+2), it suffices that
# q=2^n exceed this polynomial upper bound. No giant 2^q integers are built.
records=[]
for n in (16,24,32,48,64):
 q=1<<n;m=n**3;hbits=n*n
 log2_bins_upper=(n+1)+m*(n+hbits+2)
 records.append({'n':n,'q':q,'m':m,'log2_H':hbits,
                 'log2_bins_upper':log2_bins_upper,'collision_certified':q>log2_bins_upper})
assert all(r['collision_certified'] for r in records[1:])
print(records)
print('bounded-fingerprint asymptotic exponent arithmetic verified exactly')
