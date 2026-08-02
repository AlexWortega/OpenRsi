#!/usr/bin/env python3
# Question: can F_2^d\{0} be partitioned into k sum-free classes (translation coloring seed)?
import argparse,json,random,time
ap=argparse.ArgumentParser();ap.add_argument('-d',type=int,default=7);ap.add_argument('-k',type=int,default=5);ap.add_argument('--restarts',type=int,default=100);ap.add_argument('--steps',type=int,default=200000);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/f2_partition.json');args=ap.parse_args()
rng=random.Random(args.seed); N=1<<args.d
lines=[]; incident=[[] for _ in range(N)]
for x in range(1,N):
 for y in range(x+1,N):
  z=x^y
  if y<z:
   idx=len(lines);lines.append((x,y,z))
   for u in (x,y,z):incident[u].append(idx)

def badline(col,L):a,b,c=L;return col[a]==col[b]==col[c]
best=10**9;t0=time.time()
for restart in range(args.restarts):
 col=[-1]+[rng.randrange(args.k) for _ in range(1,N)]
 bad={i for i,L in enumerate(lines) if badline(col,L)}
 for step in range(args.steps):
  if not bad:
   classes=[[x for x in range(1,N) if col[x]==c] for c in range(args.k)]
   with open(args.out,'w') as f:json.dump(classes,f,indent=2)
   print(json.dumps({'found':True,'d':args.d,'k':args.k,'restart':restart,'step':step,'seconds':time.time()-t0,'sizes':list(map(len,classes))}),flush=True);raise SystemExit
  if len(bad)<best:best=len(bad);print('best',best,'restart',restart,'step',step,flush=True)
  li=rng.choice(tuple(bad)); x=rng.choice(lines[li]); old=col[x]
  scores=[]
  for c in range(args.k):
   col[x]=c;scores.append(sum(badline(col,lines[j]) for j in incident[x]))
  m=min(scores); choices=[c for c,s in enumerate(scores) if s==m]
  # Noise avoids the ubiquitous one-conflict local minima.
  col[x]=rng.randrange(args.k) if rng.random()<.03 else rng.choice(choices)
  for j in incident[x]:
   if badline(col,lines[j]):bad.add(j)
   else:bad.discard(j)
print(json.dumps({'found':False,'best':best,'seconds':time.time()-t0}),flush=True)
