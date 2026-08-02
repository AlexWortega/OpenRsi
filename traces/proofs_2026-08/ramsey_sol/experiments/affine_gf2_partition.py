#!/usr/bin/env python3
"""Min-conflicts symmetric product-free partitions of AGL(1,2^m)."""
import argparse,json,random,time
# irreducible polynomials binary including leading bit
POLY={2:0b111,3:0b1011,4:0b10011,5:0b100101,6:0b1000011,7:0b10000011,8:0b100011101}
p=argparse.ArgumentParser();p.add_argument('-m',type=int,default=3);p.add_argument('-k',type=int,default=5);p.add_argument('--seconds',type=int,default=270);p.add_argument('--out');a=p.parse_args();q=1<<a.m;mod=POLY[a.m]
def add(x,y):return x^y
def fm(x,y):
 z=0
 while y:
  if y&1:z^=x
  y>>=1;x<<=1
  if x&q:x^=mod
 return z
def pw(x,n):
 z=1
 while n:
  if n&1:z=fm(z,x)
  x=fm(x,x);n>>=1
 return z
def gi(x):return pw(x,q-2)
def mul(x,y):
 A,b=x;c,d=y
 return(fm(A,c),add(fm(A,d),b))
def inv(x):A,b=x;ai=gi(A);return(ai,fm(ai,b))
G=[(x,b)for x in range(1,q)for b in range(q)];e=(1,0);oid={};O=[]
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
print({'m':a.m,'q':q,'order':len(G),'orbits':len(O),'constraints':len(C),'one':len(one)},flush=True)
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
 if it%40000==39999:
  for _ in range(max(1,len(O)//30)):col[R.randrange(len(O))]=R.randrange(a.k)
  B={j for j,h in enumerate(C)if bad(h)}
 it+=1
print({'best':best},flush=True);json.dump({'m':a.m,'k':a.k,'q':q,'order':len(G),'orbits':O,'colors':bc,'best':best},open(a.out or f'experiments/agl2_{a.m}_k{a.k}.json','w'))
