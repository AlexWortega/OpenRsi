#!/usr/bin/env python3
# Question: can jointly optimizing edge colors and incident palettes produce factorial-scale locally-s colorings missed by fixed palette designs?
import argparse,itertools,json,random,time
ap=argparse.ArgumentParser();ap.add_argument('-N',type=int,default=40);ap.add_argument('-g',type=int,default=8);ap.add_argument('-s',type=int,default=4);ap.add_argument('--steps',type=int,default=5000000);ap.add_argument('--restarts',type=int,default=10);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/joint_local.json');args=ap.parse_args();rng=random.Random(args.seed);N,g,s=args.N,args.g,args.s
edges=list(itertools.combinations(range(N),2));ei={e:i for i,e in enumerate(edges)};tris=list(itertools.combinations(range(N),3));incT=[[] for _ in edges]
for j,t in enumerate(tris):
 for e in itertools.combinations(t,2):incT[ei[e]].append(j)
def mono(c,t):a,b,d=t;return c[ei[(a,b)]]==c[ei[(a,d)]]==c[ei[(b,d)]]
def score(c):
 pal=[set() for _ in range(N)]
 for z,(a,b) in enumerate(edges):pal[a].add(c[z]);pal[b].add(c[z])
 return sum(mono(c,t) for t in tris)+sum(max(0,len(x)-s)*20 for x in pal),pal
best=10**9;t0=time.time()
for restart in range(args.restarts):
 # Initialize each vertex with a random s-palette, repairing empty intersections by a common anchor.
 P=[{0,*rng.sample(range(1,g),s-1)} for _ in range(N)];c=[rng.choice(list(P[a]&P[b])) for a,b in edges];cur,pal=score(c)
 for step in range(args.steps):
  if cur==0:
   json.dump({'N':N,'g':g,'s':s,'edge_colors':{f'{a},{b}':c[z] for z,(a,b) in enumerate(edges)}},open(args.out,'w'),indent=2);print(json.dumps({'found':True,'step':step,'seconds':time.time()-t0}),flush=True);raise SystemExit
  if cur<best:best=cur;print('best',best,flush=True)
  # Usually select an edge of a monochromatic triangle; otherwise random edge.
  bad=[t for t in tris if mono(c,t)]
  if bad:e=tuple(sorted(rng.choice(list(itertools.combinations(rng.choice(bad),2)))))
  else:e=rng.choice(edges)
  x=ei[e];old=c[x];bestz=[];bv=10**9
  for z in range(g):
   c[x]=z;v,_=score(c)
   if v<bv:bv=v;bestz=[z]
   elif v==bv:bestz.append(z)
  c[x]=rng.randrange(g) if rng.random()<.01 else rng.choice(bestz);cur,pal=score(c)
print(json.dumps({'found':False,'best':best}),flush=True)
