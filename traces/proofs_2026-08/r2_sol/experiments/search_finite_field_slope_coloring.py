#!/usr/bin/env python3
# Question: can points in F_q^2 be edge-colored by compressed slopes without monochromatic triangles, giving q^2 vertices with O(q^a) colors?
import argparse,itertools,json,random
ap=argparse.ArgumentParser();ap.add_argument('-q',type=int,default=7);ap.add_argument('-k',type=int,required=True);ap.add_argument('--steps',type=int,default=3000000);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/slope.json');args=ap.parse_args();q,k=args.q,args.k;rng=random.Random(args.seed)
# Difference directions modulo sign: canonical nonzero vectors. Color depends only on direction and optional norm class suppressed.
D=[];di={}
for x,y in itertools.product(range(q),repeat=2):
 if (x,y)==(0,0):continue
 inv=pow(x if x else y,-1,q);s=(1,y*inv%q) if x else (0,1)
 if s not in di:di[s]=len(D);D.append(s)
def dr(a,b):x=(b[0]-a[0])%q;y=(b[1]-a[1])%q;return di[(1,y*pow(x,-1,q)%q) if x else (0,1)]
V=list(itertools.product(range(q),repeat=2));T=set()
for a,b,c in itertools.combinations(V,3):
 u=tuple(sorted({dr(a,b),dr(a,c),dr(b,c)}))
 if len(u)==1:print({'one_state':u});raise SystemExit(2)
 T.add(u)
T=list(T);inc=[[] for _ in D]
for j,u in enumerate(T):
 for x in u:inc[x].append(j)
def bad(c,u):return len({c[x] for x in u})==1
c=[rng.randrange(k) for _ in D];B={j for j,u in enumerate(T) if bad(c,u)};best=len(B)
for step in range(args.steps):
 if not B:json.dump({'q':q,'k':k,'colors':c},open(args.out,'w'));print({'found':True,'N':q*q});break
 x=rng.choice(T[rng.choice(tuple(B))]);scores=[]
 for z in range(k):c[x]=z;scores.append(sum(bad(c,T[j]) for j in inc[x]))
 m=min(scores);c[x]=rng.choice([z for z,v in enumerate(scores) if v==m])
 for j in inc[x]:
  if bad(c,T[j]):B.add(j)
  else:B.discard(j)
 if len(B)<best:best=len(B);print('best',best,flush=True)
else:print({'found':False,'best':best})
