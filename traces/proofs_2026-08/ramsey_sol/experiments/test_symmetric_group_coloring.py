#!/usr/bin/env python3
"""Test O(n)-color product-free rules on S_n; falsification first."""
import itertools,argparse

def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def label(p,rule):
 n=len(p);i=next(i for i in range(n) if p[i]!=i);j=p[i] # j>i for least moved point
 if rule=='pair':return (i,j)
 if rule=='sum':return (i+j)%(n if n%2 else n-1) # candidate round-robin-ish
 if rule=='diff':return j-i
 if rule=='xor':return i^j
 if rule=='edge':
  # proper edge color K_n for odd n: (i+j)/2 midpoint mod n
  if n%2:return ((i+j)*pow(2,-1,n))%n
  return (i+j)%(n-1) if j<n-1 else 2*i%(n-1)
def main(n,rule):
 P=list(itertools.permutations(range(n)));e=tuple(range(n)); classes={}
 for p in P:
  if p!=e:classes.setdefault(label(p,rule),[]).append(p)
 for c,S in classes.items():
  T=set(S)
  for x in S:
   for y in S:
    z=comp(x,y)
    if z in T:return False,c,x,y,z
 return True,len(classes),[len(x) for x in classes.values()]
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--max-n',type=int,default=7);a.add_argument('--rule',default='edge');x=a.parse_args()
 for n in range(2,x.max_n+1):
  r=main(n,x.rule);print(n,r if r[0] else ('FAIL',)+r[1:],flush=True)
