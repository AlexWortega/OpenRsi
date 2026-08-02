#!/usr/bin/env python3
import json,sys
p=sys.argv[1]if len(sys.argv)>1 else'experiments/meta_43_7_k9.json';r=json.load(open(p));P,Q,t=r['p'],r['q'],r['t'];G=[(a,b)for a in range(P)for b in range(Q)];e=(0,0)
def mul(x,y):a,b=x;c,d=y;return((a+pow(t,b,P)*c)%P,(b+d)%Q)
def inv(x):a,b=x;return((-pow(t,-b,P)*a)%P,(-b)%Q)
O=[[tuple(x)for x in o]for o in r['orbits']];flat=[x for o in O for x in o];assert set(flat)==set(G)-{e}and len(flat)==len(set(flat));C=[{x for i,o in enumerate(O)if r['colors'][i]==c for x in o}for c in range(r['k'])]
for c,S in enumerate(C):
 assert all(inv(x)in S for x in S)
 for x in S:
  for y in S:
   z=mul(x,y);assert z==e or z not in S,(c,x,y,z)
print(f'verified metacyclic order {len(G)}, {r["k"]} colors, sizes {[len(s)for s in C]}, base {len(G)**(1/r["k"]):.6f}')
