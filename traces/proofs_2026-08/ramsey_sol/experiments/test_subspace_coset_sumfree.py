#!/usr/bin/env python3
"""Test recursive coset pairing colorings of F_2^d for compression."""
import argparse,itertools,math

def color_rule(x,d,block,mode):
 # split at highest nonzero block; attempt hash within that block
 chunks=[(x>>(i*block))&((1<<block)-1) for i in range((d+block-1)//block)]
 h=max(i for i,a in enumerate(chunks) if a)
 a=chunks[h]
 if mode=='raw':return (h,a)
 if mode=='weight':return (h,a.bit_count())
 if mode=='orbit':return (h,min(a, ((a<<1)|(a>>(block-1)))&((1<<block)-1)))
 if mode=='trace':return (h,(a^(a>>1)).bit_count()%2)
def test(d,b,m):
 C=[None]+[color_rule(x,d,b,m) for x in range(1,1<<d)]
 for x in range(1,1<<d):
  for y in range(x+1,1<<d):
   z=x^y
   if C[x]==C[y]==C[z]:return False,(x,y,z,C[x])
 return True,len(set(C[1:]))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--max-d',type=int,default=12);a=p.parse_args()
 for d in range(4,a.max_d+1):
  for b in range(2,min(6,d)+1):
   for m in ['raw','weight','orbit','trace']:
    r=test(d,b,m);print(d,b,m,r,flush=True)
