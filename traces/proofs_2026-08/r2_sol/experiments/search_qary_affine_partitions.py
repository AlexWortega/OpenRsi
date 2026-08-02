#!/usr/bin/env python3
# Question: can affine vector spaces over odd fields be partitioned into few symmetric sum-free difference classes with a growing order/color ratio?
import argparse,itertools,json,random,time
ap=argparse.ArgumentParser();ap.add_argument('-q',type=int,default=3);ap.add_argument('-d',type=int,default=4);ap.add_argument('-k',type=int,required=True);ap.add_argument('--steps',type=int,default=3000000);ap.add_argument('--restarts',type=int,default=20);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/qary_partition.json');args=ap.parse_args();rng=random.Random(args.seed);q,d=args.q,args.d
vec=[x for x in itertools.product(range(q),repeat=d) if any(x)];idx={x:i for i,x in enumerate(vec)}
def neg(x):return tuple((-z)%q for z in x)
def add(x,y):return tuple((a+b)%q for a,b in zip(x,y))
# Collapse antipodal pairs because undirected differences need equal colors.
reps=[];ri={}
for x in vec:
 r=min(x,neg(x))
 if r not in ri:ri[r]=len(reps);reps.append(r)
for x in vec:ri[x]=ri[min(x,neg(x))]
T=set()
for x in vec:
 for y in vec:
  z=add(x,y)
  if any(z):
   u=tuple(sorted({ri[x],ri[y],ri[z]}))
   # A one-state constraint means the antipodal quotient itself forces a
   # monochromatic triangle (notably every nonzero x in exponent three).
   if len(u)==1:
    print(json.dumps({'impossible_by_one_state':True,'witness':[x,y,z]}),flush=True);raise SystemExit(2)
   T.add(u)
T=list(T);inc=[[] for _ in reps]
for j,u in enumerate(T):
 for x in u:inc[x].append(j)
def bad(c,u):return len({c[x] for x in u})==1
best=10**9;t0=time.time()
for restart in range(args.restarts):
 c=[rng.randrange(args.k) for _ in reps];B={j for j,u in enumerate(T) if bad(c,u)}
 for step in range(args.steps):
  if not B:
   classes=[[list(x) for x in vec if c[ri[x]]==z] for z in range(args.k)];json.dump({'q':q,'d':d,'classes':classes},open(args.out,'w'),indent=2);print(json.dumps({'found':True,'q':q,'d':d,'k':args.k,'step':step,'seconds':time.time()-t0}),flush=True);raise SystemExit
  if len(B)<best:best=len(B);print('best',best,flush=True)
  x=rng.choice(T[rng.choice(tuple(B))]);scores=[]
  for z in range(args.k):c[x]=z;scores.append(sum(bad(c,T[j]) for j in inc[x]))
  m=min(scores);c[x]=rng.randrange(args.k) if rng.random()<.02 else rng.choice([z for z,v in enumerate(scores) if v==m])
  for j in inc[x]:
   if bad(c,T[j]):B.add(j)
   else:B.discard(j)
print(json.dumps({'found':False,'best':best,'seconds':time.time()-t0}),flush=True)
