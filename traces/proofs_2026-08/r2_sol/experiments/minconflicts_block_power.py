#!/usr/bin/env python3
# Question: can t blocks of the F2^7 five-color seed be recolored with fewer than 5t colors using only block color states?
import argparse,json,itertools,random,time
ap=argparse.ArgumentParser();ap.add_argument('-t',type=int,default=3);ap.add_argument('-q',type=int,default=14);ap.add_argument('--steps',type=int,default=2000000);ap.add_argument('--restarts',type=int,default=20);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/block_power.json');args=ap.parse_args()
rng=random.Random(args.seed); C=json.load(open('experiments/f2_7_5.json'));k=len(C);col={x:i+1 for i,S in enumerate(C) for x in S}
def st(x):return 0 if x==0 else col[x]
# Ordered state relations from x,y,x+y. Keeping orientation preserves cross-coordinate pairing.
R={(st(x),st(y),st(x^y)) for x in range(128) for y in range(128)}
states=[s for s in itertools.product(range(k+1),repeat=args.t) if any(s)];idx={s:i for i,s in enumerate(states)}
T=set()
for rels in itertools.product(R,repeat=args.t):
 ss=tuple(tuple(rels[j][h] for j in range(args.t)) for h in range(3))
 if all(any(s) for s in ss):
  # x,y,x+y are distinct nonzero vectors, but their coarse state vectors may
  # repeat.  A repeated-state line imposes a 2-state inequality constraint.
  tri=tuple(sorted({idx[s] for s in ss}))
  if len(tri)>=2:T.add(tri)
T=list(T);inc=[[] for _ in states]
for j,tr in enumerate(T):
 for x in tr:inc[x].append(j)
def badline(colors,tr):return len({colors[x] for x in tr})==1
best=10**9;t0=time.time()
for restart in range(args.restarts):
 colors=[rng.randrange(args.q) for _ in states];bad={j for j,tr in enumerate(T) if badline(colors,tr)}
 for step in range(args.steps):
  if not bad:
   out={'t':args.t,'q':args.q,'seed':'experiments/f2_7_5.json','mapping':{','.join(map(str,s)):colors[i] for i,s in enumerate(states)}}
   json.dump(out,open(args.out,'w'),indent=2);print(json.dumps({'found':True,'states':len(states),'triples':len(T),'restart':restart,'step':step,'seconds':time.time()-t0}),flush=True);raise SystemExit
  if len(bad)<best:best=len(bad);print('best',best,'restart',restart,'step',step,flush=True)
  x=rng.choice(T[rng.choice(tuple(bad))]);scores=[]
  old=colors[x]
  for c in range(args.q):
   colors[x]=c;scores.append(sum(badline(colors,T[j]) for j in inc[x]))
  m=min(scores);colors[x]=rng.randrange(args.q) if rng.random()<.02 else rng.choice([c for c,v in enumerate(scores) if v==m])
  for j in inc[x]:
   if badline(colors,T[j]):bad.add(j)
   else:bad.discard(j)
print(json.dumps({'found':False,'best':best,'states':len(states),'triples':len(T),'seconds':time.time()-t0}),flush=True)
