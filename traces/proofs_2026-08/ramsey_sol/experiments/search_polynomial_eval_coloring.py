#!/usr/bin/env python3
"""Test polynomial-evaluation edge-coloring templates over prime fields.
Vertices are polynomials degree < d. Color pair by a compressed function of
first evaluation point where values differ. Exhaustively finds triangle witness.
"""
import argparse,itertools

def val(poly,x,q):return sum(a*pow(x,i,q) for i,a in enumerate(poly))%q
def test(q,d,mode):
 V=list(itertools.product(range(q),repeat=d)); pts=list(range(q));ev={p:tuple(val(p,x,q) for x in pts) for p in V}
 def color(a,b):
  ea,eb=ev[a],ev[b];x=next(x for x in pts if ea[x]!=eb[x]);u,v=ea[x],eb[x]
  if mode=='raw':return (x,min(u,v),max(u,v))
  if mode=='diff':return (x,min((u-v)%q,(v-u)%q))
  if mode=='sum':return (x,(u+v)%q)
  if mode=='prod':return (x,(u*v)%q)
  if mode=='ratio':return (x,min((u*pow(v,-1,q))%q if v else q,(v*pow(u,-1,q))%q if u else q))
 C={}
 for i,a in enumerate(V):
  for b in V[:i]:C[a,b]=color(a,b)
 for i,a in enumerate(V):
  for j,b in enumerate(V[:i]):
   ab=C[a,b]
   for c in V[:j]:
    if ab==C[a,c]==C[b,c]:return False,(a,b,c,ab)
 return True,len(set(C.values()))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--max-q',type=int,default=7);p.add_argument('--max-d',type=int,default=3);a=p.parse_args()
 for q in [3,5,7][:a.max_q]:
  for d in range(1,a.max_d+1):
   if q**d>500:continue
   for m in ['raw','diff','sum','prod','ratio']:
    try:r=test(q,d,m)
    except Exception as e:r=('ERROR',str(e))
    print(q,d,m,r,flush=True)
