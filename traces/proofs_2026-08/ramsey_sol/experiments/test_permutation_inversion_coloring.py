#!/usr/bin/env python3
"""Test compressed first-inversion colorings on permutations."""
import itertools,argparse

def invdiff(p,q):
 n=len(p);ip=[0]*n;iq=[0]*n
 for i,x in enumerate(p):ip[x]=i
 for i,x in enumerate(q):iq[x]=i
 return [(a,b) for a in range(n) for b in range(a+1,n) if (ip[a]<ip[b])!=(iq[a]<iq[b])]
def test(n,order,compress):
 V=list(itertools.permutations(range(n))); cache={}
 keys=list(itertools.combinations(range(n),2))
 if order=='gap':keys.sort(key=lambda x:(x[1]-x[0],x))
 if order=='sum':keys.sort(key=lambda x:(sum(x),x))
 rank={x:i for i,x in enumerate(keys)}
 def c(p,q):
  D=invdiff(p,q);a,b=min(D,key=lambda x:rank[x])
  if compress=='a':return a
  if compress=='b':return b
  if compress=='sum':return (a+b)%n
  if compress=='gap':return b-a
  if compress=='parity':return (a&1,b&1)
  if compress=='pair':return(a,b)
 for i,p in enumerate(V):
  for j,q in enumerate(V[:i]):
   x=c(p,q)
   for r in V[:j]:
    if x==c(p,r)==c(q,r):return False,(p,q,r,x)
 return True,None
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--max-n',type=int,default=7);z=a.parse_args()
 for n in range(3,z.max_n+1):
  for o in ['lex','gap','sum']:
   for c in ['a','b','sum','gap','parity','pair']:
    ok,w=test(n,o,c);print(n,o,c,ok,w if not ok else'',flush=True)
