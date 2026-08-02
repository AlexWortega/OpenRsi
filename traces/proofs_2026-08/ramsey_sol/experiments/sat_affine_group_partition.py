#!/usr/bin/env python3
"""Min-conflicts symmetric product-free partitions of AGL(1,q)."""
import argparse,json,random,time
from test_affine_group_rules import mul,inv
p=argparse.ArgumentParser();p.add_argument('--q',type=int,default=11);p.add_argument('--k',type=int,default=5);p.add_argument('--seconds',type=int,default=270);p.add_argument('--out');a=p.parse_args();G=[(x,b)for x in range(1,a.q)for b in range(a.q)];e=(1,0);oid={};O=[]
for x in G:
 if x==e or x in oid:continue
 o=sorted(set((x,inv(x,a.q))));i=len(O);O.append(o)
 for z in o:oid[z]=i
C=set();one=[]
for x in G:
 if x==e:continue
 for y in G:
  if y==e:continue
  z=mul(x,y,a.q)
  if z!=e:
   h=tuple(sorted(set((oid[x],oid[y],oid[z]))));C.add(h)
   if len(h)==1:one.append((x,y,z))
print({'q':a.q,'order':len(G),'orbits':len(O),'constraints':len(C),'one':len(one)},flush=True)
if one:print('ONE',one[0]);raise SystemExit
C=sorted(C);R=random.Random(1);col=[R.randrange(a.k)for _ in O];inc=[[]for _ in O]
for j,h in enumerate(C):
 for x in h:inc[x].append(j)
def bad(h):return len({col[x]for x in h})==1
B={j for j,h in enumerate(C)if bad(h)};best=len(B);bc=col[:];end=time.time()+a.seconds;it=0
while B and time.time()<end:
 h=C[R.choice(tuple(B))];x=R.choice(h);sc=[]
 for c in range(a.k):col[x]=c;sc.append(sum(bad(C[j])for j in inc[x]))
 z=min(sc);col[x]=R.choice([c for c,s in enumerate(sc)if s==z])
 for j in inc[x]:
  if bad(C[j]):B.add(j)
  else:B.discard(j)
 if len(B)<best:best=len(B);bc=col[:];print('best',best,flush=True)
 it+=1
print({'best':best},flush=True);json.dump({'q':a.q,'k':a.k,'order':len(G),'orbits':O,'colors':bc,'best':best},open(a.out or f'experiments/agl1_{a.q}_k{a.k}.json','w'))
