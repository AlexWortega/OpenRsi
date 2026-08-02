#!/usr/bin/env python3
# Question: how large a cyclic group Z_p admits a translation-invariant k-coloring with symmetric sum-free difference classes?
import argparse,itertools,json,random,time
ap=argparse.ArgumentParser();ap.add_argument('-p',type=int,required=True);ap.add_argument('-k',type=int,required=True);ap.add_argument('--steps',type=int,default=3000000);ap.add_argument('--restarts',type=int,default=20);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/cyclic_coloring.json');args=ap.parse_args();rng=random.Random(args.seed);p=args.p
assert p%2==1
# Variables are antipodal pairs {d,-d}; every vertex triple reduces to a constraint on three pair indices.
def idx(d):d%=p;return min(d,p-d)-1
T=set()
for a in range(1,p):
 for b in range(a+1,p):
  c=(b-a)%p;u=tuple(sorted({idx(a),idx(b),idx(c)}))
  if len(u)>=2:T.add(u)
T=list(T);n=(p-1)//2;inc=[[] for _ in range(n)]
for j,u in enumerate(T):
 for x in u:inc[x].append(j)
def bad(c,u):return len({c[x] for x in u})==1
best=10**9;t0=time.time()
for restart in range(args.restarts):
 c=[rng.randrange(args.k) for _ in range(n)];B={j for j,u in enumerate(T) if bad(c,u)}
 for step in range(args.steps):
  if not B:
   classes=[[d for d in range(1,p) if c[idx(d)]==z] for z in range(args.k)];json.dump(classes,open(args.out,'w'),indent=2);print(json.dumps({'found':True,'p':p,'k':args.k,'restart':restart,'step':step,'seconds':time.time()-t0}),flush=True);raise SystemExit
  if len(B)<best:best=len(B);print('best',best,flush=True)
  x=rng.choice(T[rng.choice(tuple(B))]);scores=[]
  for z in range(args.k):c[x]=z;scores.append(sum(bad(c,T[j]) for j in inc[x]))
  m=min(scores);c[x]=rng.randrange(args.k) if rng.random()<.02 else rng.choice([z for z,v in enumerate(scores) if v==m])
  for j in inc[x]:
   if bad(c,T[j]):B.add(j)
   else:B.discard(j)
print(json.dumps({'found':False,'p':p,'k':args.k,'best':best,'seconds':time.time()-t0}),flush=True)
