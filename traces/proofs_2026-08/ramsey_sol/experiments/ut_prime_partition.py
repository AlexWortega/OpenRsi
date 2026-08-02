#!/usr/bin/env python3
"""Symmetric product-free partitions of UT(n,p), small odd prime p."""
import argparse,itertools,json,random,time
p0=argparse.ArgumentParser();p0.add_argument('-n',type=int,default=3);p0.add_argument('-p',type=int,default=5);p0.add_argument('-k',type=int,default=6);p0.add_argument('--seconds',type=int,default=270);p0.add_argument('--out');a=p0.parse_args();pos=[(i,j)for i in range(a.n)for j in range(i+1,a.n)];ix={z:t for t,z in enumerate(pos)};G=list(itertools.product(range(a.p),repeat=len(pos)));e=(0,)*len(pos)
def mul(x,y):
 z=[(x[t]+y[t])%a.p for t in range(len(pos))]
 for i in range(a.n):
  for j in range(i+1,a.n):
   for h in range(i+1,j):z[ix[i,j]]=(z[ix[i,j]]+x[ix[i,h]]*y[ix[h,j]])%a.p
 return tuple(z)
def inv(x):return next(y for y in G if mul(x,y)==mul(y,x)==e)
oid={};O=[]
for x in G:
 if x==e or x in oid:continue
 o=sorted(set((x,inv(x))));i=len(O);O.append(o)
 for z in o:oid[z]=i
C=set();one=[]
for x in G:
 if x==e:continue
 for y in G:
  if y==e:continue
  z=mul(x,y)
  if z!=e:
   h=tuple(sorted(set((oid[x],oid[y],oid[z]))));C.add(h)
   if len(h)==1:one.append((x,y,z))
print({'n':a.n,'p':a.p,'order':len(G),'orbits':len(O),'constraints':len(C),'one':len(one)},flush=True)
if one:print('ONE',one[0]);raise SystemExit
C=sorted(C);R=random.Random(1);col=[R.randrange(a.k)for _ in O];inc=[[]for _ in O]
for j,h in enumerate(C):
 for x in h:inc[x].append(j)
def bad(h):return len({col[x]for x in h})==1
B={j for j,h in enumerate(C)if bad(h)};best=len(B);bc=col[:];end=time.time()+a.seconds
while B and time.time()<end:
 h=C[R.choice(tuple(B))];x=R.choice(h);sc=[]
 for c in range(a.k):col[x]=c;sc.append(sum(bad(C[j])for j in inc[x]))
 z=min(sc);col[x]=R.choice([c for c,s in enumerate(sc)if s==z])
 for j in inc[x]:
  if bad(C[j]):B.add(j)
  else:B.discard(j)
 if len(B)<best:best=len(B);bc=col[:];print('best',best,flush=True)
print({'best':best});json.dump({'n':a.n,'p':a.p,'k':a.k,'order':len(G),'orbits':[[list(x)for x in o]for o in O],'colors':bc,'best':best},open(a.out or'experiments/utp.json','w'))
