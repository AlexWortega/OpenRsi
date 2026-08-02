#!/usr/bin/env python3
# Question: can nonabelian finite groups be partitioned into few inverse-closed product-free classes, yielding translation colorings with better order/color ratio?
import argparse,itertools,json,random,time
ap=argparse.ArgumentParser();ap.add_argument('--group',choices=['dihedral','symmetric'],default='dihedral');ap.add_argument('-n',type=int,default=16);ap.add_argument('-k',type=int,required=True);ap.add_argument('--steps',type=int,default=3000000);ap.add_argument('--restarts',type=int,default=10);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/group_partition.json');args=ap.parse_args();rng=random.Random(args.seed)
if args.group=='dihedral':
 G=[(a,b) for a in range(args.n) for b in range(2)];identity=(0,0)
 def mul(x,y):a,b=x;c,d=y;return ((a+(-1 if b else 1)*c)%args.n,(b+d)%2)
 def inv(x):a,b=x;return (((-1 if b==0 else 1)*a)%args.n,b)
else:
 G=list(itertools.permutations(range(args.n)));identity=tuple(range(args.n))
 def mul(x,y):return tuple(x[y[i]] for i in range(args.n))
 def inv(x):return tuple(x.index(i) for i in range(args.n))
U=[x for x in G if x!=identity];reps=[];ri={}
for x in U:
 r=min(x,inv(x))
 if r not in ri:ri[r]=len(reps);reps.append(r)
for x in U:ri[x]=ri[min(x,inv(x))]
T=set()
for x in U:
 for y in U:
  z=mul(x,y)
  if z!=identity:
   u=tuple(sorted({ri[x],ri[y],ri[z]}))
   if len(u)==1:print(json.dumps({'one_state_obstruction':[x,y,z]}),flush=True);raise SystemExit(2)
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
   classes=[[list(x) for x in U if c[ri[x]]==z] for z in range(args.k)];json.dump({'group':args.group,'n':args.n,'classes':classes},open(args.out,'w'),indent=2);print(json.dumps({'found':True,'order':len(G),'k':args.k,'step':step,'seconds':time.time()-t0}),flush=True);raise SystemExit
  if len(B)<best:best=len(B);print('best',best,flush=True)
  x=rng.choice(T[rng.choice(tuple(B))]);scores=[]
  for z in range(args.k):c[x]=z;scores.append(sum(bad(c,T[j]) for j in inc[x]))
  m=min(scores);c[x]=rng.randrange(args.k) if rng.random()<.02 else rng.choice([z for z,v in enumerate(scores) if v==m])
  for j in inc[x]:
   if bad(c,T[j]):B.add(j)
   else:B.discard(j)
print(json.dumps({'found':False,'best':best}),flush=True)
