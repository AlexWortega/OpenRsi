#!/usr/bin/env python3
"""Search vertex-dependent palette recursion on rooted trees, beyond color-only reuse."""
# Vertices leaves [q]^d; edge state=(LCP prefix, two symbols). Optimize colors by min-conflicts.
import argparse,itertools,random,time,json
p=argparse.ArgumentParser();p.add_argument('--q',type=int,default=4);p.add_argument('--d',type=int,default=3);p.add_argument('-k',type=int,default=5);p.add_argument('--seconds',type=int,default=270);p.add_argument('--out');a=p.parse_args();V=list(itertools.product(range(a.q),repeat=a.d));states=[]
for h in range(a.d):
 for pre in itertools.product(range(a.q),repeat=h):
  for x in range(a.q):
   for y in range(x):states.append((pre,y,x))
ix={s:i for i,s in enumerate(states)}
def es(x,y):
 h=next(i for i in range(a.d)if x[i]!=y[i]);return ix[(x[:h],min(x[h],y[h]),max(x[h],y[h]))]
C=set()
for i,x in enumerate(V):
 for j,y in enumerate(V[:i]):
  for z in V[:j]:C.add(tuple(sorted(set((es(x,y),es(x,z),es(y,z))))))
C=sorted(C);R=random.Random(1);col=[R.randrange(a.k)for _ in states];inc=[[]for _ in states]
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
print({'q':a.q,'d':a.d,'N':len(V),'k':a.k,'states':len(states),'constraints':len(C),'best':best,'base':len(V)**(1/a.k)},flush=True);json.dump({'q':a.q,'d':a.d,'k':a.k,'states':states,'colors':bc,'best':best},open(a.out or'experiments/treepalette.json','w'))
