#!/usr/bin/env python3
"""Independent verifier for a Heisenberg-group difference partition candidate."""
import json,sys
path=sys.argv[1] if len(sys.argv)>1 else 'experiments/heisenberg_q4_k5.json'
r=json.load(open(path));q=r['q']; k=r['k']; orbits=[[tuple(x) for x in O] for O in r['orbits']]; colors=r['colors']
def mul(x,y):
 a,b,c=x;d,e,f=y
 return ((a+d)%q,(b+e)%q,(c+f+a*e)%q)
def inv(x):
 a,b,c=x
 return ((-a)%q,(-b)%q,(-c+a*b)%q)
e=(0,0,0); G={(a,b,c) for a in range(q) for b in range(q) for c in range(q)}; flat=[x for O in orbits for x in O]
assert len(colors)==len(orbits) and all(isinstance(c,int) and 0<=c<k for c in colors)
assert len(flat)==len(set(flat))==q**3-1 and set(flat)==G-{e}
owner={x:i for i,O in enumerate(orbits) for x in O}
for i,O in enumerate(orbits):
 assert set(O)=={O[0],inv(O[0])}
# Every color class is inverse-closed and product-free away from identity.
classes=[{x for i,O in enumerate(orbits) if colors[i]==c for x in O} for c in range(k)]
for c,S in enumerate(classes):
 assert all(inv(x) in S for x in S)
 for x in S:
  for y in S:
   z=mul(x,y)
   assert z==e or z not in S, (c,x,y,z)
# Directly verify all vertex triangles under c(x^{-1}y).
def edge_color(x,y): return colors[owner[mul(inv(x),y)]]
tri=0; L=sorted(G)
for a in range(len(L)):
 for b in range(a):
  cab=edge_color(L[a],L[b])
  for d in range(b):
   tri+=1
   assert not (cab==edge_color(L[a],L[d])==edge_color(L[b],L[d]))
print(f'verified H(Z/{q}Z), order {q**3}, {k} colors, {tri} triangles, class sizes {[len(S) for S in classes]}')
