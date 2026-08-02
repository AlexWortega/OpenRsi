#!/usr/bin/env python3
# Question: can a non-translation layer-dependent coloring on Z_p x [r] reuse a cyclic seed palette more efficiently than disjoint products?
import argparse,itertools,json,random,time
ap=argparse.ArgumentParser();ap.add_argument('-p',type=int,default=127);ap.add_argument('-r',type=int,default=2);ap.add_argument('-k',type=int,default=6);ap.add_argument('--steps',type=int,default=3000000);ap.add_argument('--restarts',type=int,default=10);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/shifted_cyclic.json');args=ap.parse_args();rng=random.Random(args.seed);p,r,k=args.p,args.r,args.k
# Variables: color depends on unordered layer pair and oriented difference; enforce c_ab(d)=c_ba(-d).
keys=[];idx={}
for a in range(r):
 for b in range(a,r):
  ds=range(1,(p+1)//2) if a==b else range(p)
  for d in ds:idx[(a,b,d)]=len(keys);keys.append((a,b,d))
def key(a,b,d):
 d%=p
 if a>b:a,b,d=b,a,(-d)%p
 if a==b:d=min(d,(-d)%p)
 return idx[(a,b,d)]
verts=[(a,x) for a in range(r) for x in range(p)];T=set()
for u,v,w in itertools.combinations(verts,3):
 e=tuple(sorted({key(u[0],v[0],v[1]-u[1]),key(u[0],w[0],w[1]-u[1]),key(v[0],w[0],w[1]-v[1])}))
 if len(e)>=2:T.add(e)
T=list(T);inc=[[] for _ in keys]
for j,e in enumerate(T):
 for x in e:inc[x].append(j)
def bad(c,e):return len({c[x] for x in e})==1
best=10**9;t0=time.time()
for restart in range(args.restarts):
 c=[rng.randrange(k) for _ in keys];B={j for j,e in enumerate(T) if bad(c,e)}
 for step in range(args.steps):
  if not B:
   json.dump({'p':p,'r':r,'k':k,'keys':[list(x) for x in keys],'colors':c},open(args.out,'w'),indent=2);print(json.dumps({'found':True,'step':step,'seconds':time.time()-t0}),flush=True);raise SystemExit
  if len(B)<best:best=len(B);print('best',best,flush=True)
  x=rng.choice(T[rng.choice(tuple(B))]);scores=[]
  for z in range(k):c[x]=z;scores.append(sum(bad(c,T[j]) for j in inc[x]))
  m=min(scores);c[x]=rng.randrange(k) if rng.random()<.02 else rng.choice([z for z,v in enumerate(scores) if v==m])
  for j in inc[x]:
   if bad(c,T[j]):B.add(j)
   else:B.discard(j)
print(json.dumps({'found':False,'best':best,'seconds':time.time()-t0}),flush=True)
