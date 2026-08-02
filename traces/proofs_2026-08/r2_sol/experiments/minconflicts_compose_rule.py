#!/usr/bin/env python3
# Question: can two copies of the verified 21-bit/13-color state rule be compressed below 26 colors?
import argparse,json,itertools,random,time
ap=argparse.ArgumentParser();ap.add_argument('-q',type=int,default=25);ap.add_argument('--steps',type=int,default=1000000);ap.add_argument('--restarts',type=int,default=20);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--baseline-init',action='store_true');ap.add_argument('--out',default='experiments/composed_rule.json');args=ap.parse_args();rng=random.Random(args.seed)
C=json.load(open('experiments/f2_7_5.json'));base={x:i+1 for i,S in enumerate(C) for x in S}
def st(x):return 0 if x==0 else base[x]
R={(st(x),st(y),st(x^y)) for x in range(128) for y in range(128)}
d=json.load(open('experiments/block_power_3_13.json'));mp={tuple(map(int,k.split(','))):v+1 for k,v in d['mapping'].items()}
# Derive exact ordered relation on output states 0..13.
R13=set()
for rels in itertools.product(R,repeat=3):
 ss=[tuple(rels[j][h] for j in range(3)) for h in range(3)]
 vals=tuple(0 if not any(s) else mp[s] for s in ss);R13.add(vals)
print('R13',len(R13),flush=True)
states=[s for s in itertools.product(range(14),repeat=2) if any(s)];idx={s:i for i,s in enumerate(states)};T=set()
for a,b in itertools.product(R13,repeat=2):
 ss=[(a[h],b[h]) for h in range(3)]
 if all(any(s) for s in ss) and len(set(ss))==3:T.add(tuple(sorted(idx[s] for s in ss)))
T=list(T);inc=[[] for _ in states]
for j,tr in enumerate(T):
 for x in tr:inc[x].append(j)
def bad(c,tr):a,b,d=tr;return c[a]==c[b]==c[d]
print('states',len(states),'triples',len(T),flush=True);best=10**9;t0=time.time()
for restart in range(args.restarts):
 if args.baseline_init:
  # Disjoint-palette/first-nonzero-block rule has 26 labels; randomly fold them to q.
  labels=list(range(26));rng.shuffle(labels);fold={labels[i]:i%args.q for i in range(26)}
  c=[fold[(a-1) if a else 13+(b-1)] for a,b in states]
 else:c=[rng.randrange(args.q) for _ in states]
 B={j for j,tr in enumerate(T) if bad(c,tr)}
 for step in range(args.steps):
  if not B:
   json.dump({'q':args.q,'mapping':{','.join(map(str,s)):c[i] for i,s in enumerate(states)}},open(args.out,'w'),indent=2);print(json.dumps({'found':True,'restart':restart,'step':step,'seconds':time.time()-t0}),flush=True);raise SystemExit
  if len(B)<best:best=len(B);print('best',best,flush=True)
  x=rng.choice(T[rng.choice(tuple(B))]);scores=[]
  for z in range(args.q):c[x]=z;scores.append(sum(bad(c,T[j]) for j in inc[x]))
  m=min(scores);c[x]=rng.randrange(args.q) if rng.random()<.02 else rng.choice([z for z,v in enumerate(scores) if v==m])
  for j in inc[x]:
   if bad(c,T[j]):B.add(j)
   else:B.discard(j)
print(json.dumps({'found':False,'best':best}),flush=True)
