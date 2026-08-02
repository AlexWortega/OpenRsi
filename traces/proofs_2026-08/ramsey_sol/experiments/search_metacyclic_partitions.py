#!/usr/bin/env python3
"""Search inverse-closed product-free partitions of semidirect C_p wr/action C_q, 3-torsion-free."""
import argparse,json,random,time
# G={(a,b)}, multiply (a,b)(c,d)=(a+t^b c,b+d), t order q mod p
P=argparse.ArgumentParser();P.add_argument('--p',type=int,default=11);P.add_argument('--q',type=int,default=5);P.add_argument('-k',type=int,default=6);P.add_argument('--seconds',type=int,default=60);P.add_argument('--out');a=P.parse_args()
t=next(x for x in range(2,a.p)if pow(x,a.q,a.p)==1 and all(pow(x,d,a.p)!=1 for d in range(1,a.q)))
def mul(x,y):A,b=x;c,d=y;return((A+pow(t,b,a.p)*c)%a.p,(b+d)%a.q)
def inv(x):A,b=x;return((-pow(t,-b,a.p)*A)%a.p,(-b)%a.q)
G=[(x,y)for x in range(a.p)for y in range(a.q)];e=(0,0);oid={};O=[]
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
print({'p':a.p,'q':a.q,'t':t,'order':len(G),'orbits':len(O),'constraints':len(C),'one':len(one)},flush=True)
if one:print('ONE',one[0]);raise SystemExit
C=sorted(C);R=random.Random(2);col=[R.randrange(a.k)for _ in O];inc=[[]for _ in O]
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
print({'best':best},flush=True);json.dump({'p':a.p,'q':a.q,'t':t,'k':a.k,'order':len(G),'orbits':O,'colors':bc,'best':best},open(a.out or'experiments/metacyclic.json','w'))
