#!/usr/bin/env python3
# Question: can subsets of [m] support a triangle-free coloring by a witness coordinate in each symmetric difference, yielding m colors on superexponentially many vertices?
import argparse,itertools,json,random,time
ap=argparse.ArgumentParser();ap.add_argument('-m',type=int,default=6);ap.add_argument('--layers',default='3');ap.add_argument('--steps',type=int,default=3000000);ap.add_argument('--restarts',type=int,default=10);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/subset_witness.json');args=ap.parse_args();rng=random.Random(args.seed);m=args.m;L=set(map(int,args.layers.split(',')));V=[x for x in range(1<<m) if x.bit_count() in L]
edges=list(itertools.combinations(range(len(V)),2));allowed=[]
for i,j in edges:allowed.append([b for b in range(m) if ((V[i]^V[j])>>b)&1])
ei={e:i for i,e in enumerate(edges)};T=list(itertools.combinations(range(len(V)),3));inc=[[] for _ in edges]
for z,(a,b,c) in enumerate(T):
 for e in ((a,b),(a,c),(b,c)):inc[ei[e]].append(z)
def bad(col,t):a,b,c=t;return col[ei[(a,b)]]==col[ei[(a,c)]]==col[ei[(b,c)]]
best=10**9;t0=time.time()
for r in range(args.restarts):
 col=[rng.choice(A) for A in allowed];B={z for z,t in enumerate(T) if bad(col,t)}
 for step in range(args.steps):
  if not B:
   json.dump({'m':m,'layers':sorted(L),'vertices':V,'colors':{f'{V[i]},{V[j]}':col[z] for z,(i,j) in enumerate(edges)}},open(args.out,'w'),indent=2);print(json.dumps({'found':True,'N':len(V),'step':step}),flush=True);raise SystemExit
  if len(B)<best:best=len(B);print('best',best,flush=True)
  tri=T[rng.choice(tuple(B))];e=tuple(sorted(rng.choice(list(itertools.combinations(tri,2)))));x=ei[e];scores=[]
  for c in allowed[x]:col[x]=c;scores.append(sum(bad(col,T[z]) for z in inc[x]))
  q=min(scores);col[x]=rng.choice(allowed[x]) if rng.random()<.02 else rng.choice([c for c,v in zip(allowed[x],scores) if v==q])
  for z in inc[x]:
   if bad(col,T[z]):B.add(z)
   else:B.discard(z)
print(json.dumps({'found':False,'N':len(V),'best':best}),flush=True)
