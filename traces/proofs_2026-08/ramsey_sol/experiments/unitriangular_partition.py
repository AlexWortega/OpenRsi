#!/usr/bin/env python3
"""Min-conflicts symmetric product-free partitions of UT(n,2). Heuristic."""
import argparse,json,random,time

def setup(n):
 pos=[(i,j) for i in range(n) for j in range(i+1,n)]; ix={p:t for t,p in enumerate(pos)}; N=1<<len(pos)
 def mul(x,y):
  z=x^y
  for i in range(n):
   for j in range(i+1,n):
    v=0
    for h in range(i+1,j): v^=((x>>ix[i,h])&1)&((y>>ix[h,j])&1)
    z^=v<<ix[i,j]
  return z
 def inv(x):
  # finite geometric series A+A^2+... via repeated multiplication in group:
  # brute find using recurrence B=A+A B, entries by increasing gap.
  b=0
  for gap in range(1,n):
   for i in range(n-gap):
    j=i+gap; v=(x>>ix[i,j])&1
    for h in range(i+1,j): v^=((x>>ix[i,h])&1)&((b>>ix[h,j])&1)
    b|=v<<ix[i,j]
  return b
 return N,mul,inv,pos

def build(n):
 N,mul,inv,pos=setup(n); oid={}; O=[]
 for x in range(1,N):
  if x not in oid:
   o=sorted(set((x,inv(x)))); i=len(O);O.append(o)
   for z in o:oid[z]=i
 C=set(); one=[]
 for x in range(1,N):
  for y in range(1,N):
   z=mul(x,y)
   if not z:continue
   h=tuple(sorted(set((oid[x],oid[y],oid[z]))));C.add(h)
   if len(h)==1:one.append((x,y,z,h[0]))
 return N,O,sorted(C),one,pos

def solve(N,C,k,sec,seed):
 r=random.Random(seed);c=[r.randrange(k) for _ in range(N)];inc=[[] for _ in range(N)]
 for j,h in enumerate(C):
  for x in h:inc[x].append(j)
 def badh(h):return len({c[x] for x in h})==1
 bad={j for j,h in enumerate(C) if badh(h)};best=len(bad);bc=c[:];end=time.time()+sec;it=0
 while bad and time.time()<end:
  h=C[r.choice(tuple(bad))];x=r.choice(h);scores=[]
  for a in range(k):c[x]=a;scores.append(sum(badh(C[t]) for t in inc[x]))
  z=min(scores);c[x]=r.choice([a for a,s in enumerate(scores) if s==z])
  for t in inc[x]:
   if badh(C[t]):bad.add(t)
   else:bad.discard(t)
  if len(bad)<best:best=len(bad);bc=c[:];print('best',best,'iter',it,flush=True)
  if it%20000==19999 and bad:
   for _ in range(max(1,N//30)):c[r.randrange(N)]=r.randrange(k)
   bad={j for j,h in enumerate(C) if badh(h)}
  it+=1
 return best,bc,it
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=5);p.add_argument('--k',type=int,default=5);p.add_argument('--seconds',type=int,default=270);p.add_argument('--seed',type=int,default=1);p.add_argument('--out');a=p.parse_args()
 N,O,C,one,pos=build(a.n);print(json.dumps({'n':a.n,'order':N,'orbits':len(O),'constraints':len(C),'one':len(one)}),flush=True)
 if one:print('ONE_STATE',one[0]);raise SystemExit
 best,col,it=solve(len(O),C,a.k,a.seconds,a.seed);r={'n':a.n,'k':a.k,'order':N,'orbits':O,'colors':col,'best':best,'iterations':it};print(json.dumps({x:r[x] for x in ('n','k','order','best','iterations')}),flush=True);json.dump(r,open(a.out or f'experiments/ut{a.n}_k{a.k}.json','w'))
