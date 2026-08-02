#!/usr/bin/env python3
# Question: can six global colors support a large triangle-free complete-graph coloring with at most four incident colors per vertex?
import argparse,itertools,json,random,time
ap=argparse.ArgumentParser();ap.add_argument('-N',type=int,default=40);ap.add_argument('-g',type=int,default=6);ap.add_argument('-s',type=int,default=4);ap.add_argument('--steps',type=int,default=3000000);ap.add_argument('--restarts',type=int,default=20);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/local_palette.json');args=ap.parse_args();rng=random.Random(args.seed)
# For s>g/2 all s-subsets pairwise intersect. Balance palette types cyclically.
types=list(itertools.combinations(range(args.g),args.s));pal=[set(types[i%len(types)]) for i in range(args.N)];rng.shuffle(pal)
edges=list(itertools.combinations(range(args.N),2));ei={e:i for i,e in enumerate(edges)};allowed=[sorted(pal[a]&pal[b]) for a,b in edges]
assert all(allowed);tris=list(itertools.combinations(range(args.N),3));inc=[[] for _ in edges]
for j,(a,b,c) in enumerate(tris):
 for e in ((a,b),(a,c),(b,c)):inc[ei[e]].append(j)
def bad(col,t):a,b,c=t;return col[ei[(a,b)]]==col[ei[(a,c)]]==col[ei[(b,c)]]
best=10**9;t0=time.time()
for restart in range(args.restarts):
 col=[rng.choice(A) for A in allowed];B={j for j,t in enumerate(tris) if bad(col,t)}
 for step in range(args.steps):
  if not B:
   out={'N':args.N,'g':args.g,'s':args.s,'palettes':[sorted(x) for x in pal],'edge_colors':{f'{a},{b}':col[i] for i,(a,b) in enumerate(edges)}};json.dump(out,open(args.out,'w'),indent=2);print(json.dumps({'found':True,'restart':restart,'step':step,'seconds':time.time()-t0}),flush=True);raise SystemExit
  if len(B)<best:best=len(B);print('best',best,flush=True)
  tri=tris[rng.choice(tuple(B))];e=tuple(sorted(rng.choice(list(itertools.combinations(tri,2)))));x=ei[e];scores=[]
  for z in allowed[x]:col[x]=z;scores.append(sum(bad(col,tris[j]) for j in inc[x]))
  m=min(scores);col[x]=rng.choice(allowed[x]) if rng.random()<.02 else rng.choice([z for z,v in zip(allowed[x],scores) if v==m])
  for j in inc[x]:
   if bad(col,tris[j]):B.add(j)
   else:B.discard(j)
print(json.dumps({'found':False,'best':best,'seconds':time.time()-t0}),flush=True)
