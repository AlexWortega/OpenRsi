#!/usr/bin/env python3
# Question: can a scale-recursive coloring of integer differences reuse colors across dyadic levels without monochromatic triangles?
import argparse,itertools,json,random
ap=argparse.ArgumentParser();ap.add_argument('-N',type=int,default=256);ap.add_argument('-k',type=int,default=6);ap.add_argument('--steps',type=int,default=3000000);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/recursive_diff.json');args=ap.parse_args();rng=random.Random(args.seed);N,k=args.N,args.k
# Translation coloring on interval vertices depends on positive difference d. Constraint colors(a),colors(b),colors(b-a).
T=list(itertools.combinations(range(1,N),2));inc=[[] for _ in range(N)]
for j,(a,b) in enumerate(T):
 for d in (a,b,b-a):inc[d].append(j)
def bad(c,t):a,b=t;return c[a]==c[b]==c[b-a]
best=10**9
for restart in range(10):
 c=[0]+[rng.randrange(k) for _ in range(1,N)];B={j for j,t in enumerate(T) if bad(c,t)}
 for step in range(args.steps):
  if not B:json.dump({'N':N,'k':k,'colors':c},open(args.out,'w'));print({'found':True,'step':step});raise SystemExit
  if len(B)<best:best=len(B);print('best',best,flush=True)
  a,b=T[rng.choice(tuple(B))];x=rng.choice((a,b,b-a));scores=[]
  for z in range(k):c[x]=z;scores.append(sum(bad(c,T[j]) for j in inc[x]))
  m=min(scores);c[x]=rng.choice([z for z,v in enumerate(scores) if v==m])
  for j in inc[x]:
   if bad(c,T[j]):B.add(j)
   else:B.discard(j)
print({'found':False,'best':best})
