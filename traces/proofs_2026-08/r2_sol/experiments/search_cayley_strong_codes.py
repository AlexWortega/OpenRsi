#!/usr/bin/env python3
# Question: do triangle-free Cayley complements from symmetric sum-free sets admit large correlated strong-cube codes beyond fixed Mycielski examples?
import argparse,json,random,time
ap=argparse.ArgumentParser();ap.add_argument('-p',type=int,default=31);ap.add_argument('--sets',type=int,default=500);ap.add_argument('--restarts',type=int,default=500);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/cayley_codes.json');args=ap.parse_args();rng=random.Random(args.seed);p=args.p
def valid(S,x):
 T=S|{x,(-x)%p};return all((a+b)%p not in T for a in T for b in T)
def code(S):
 words=[(i//(p*p),(i//p)%p,i%p) for i in range(p**3)];best=[]
 def comp(a,b):return any((a[j]-b[j])%p in S for j in range(3))
 for _ in range(args.restarts):
  cand=list(range(len(words)));C=[]
  while cand:
   sample=rng.sample(cand,min(12,len(cand)));probe=rng.sample(cand,min(128,len(cand)))
   x=max(sample,key=lambda z:sum(comp(words[z],words[y]) for y in probe));C.append(x);cand=[y for y in cand if comp(words[x],words[y])]
  if len(C)>len(best):best=C
 return [words[i] for i in best]
bestrec=None;t=time.time()
for z in range(args.sets):
 S=set();cand=list(range(1,(p+1)//2));rng.shuffle(cand)
 while cand:
  x=cand.pop()
  if valid(S,x):S|={x,(-x)%p}
 C=code(S);r={'p':p,'S':sorted(S),'code':C,'size':len(C),'base':len(C)**(1/3)}
 if bestrec is None or r['size']>bestrec['size']:bestrec=r;print(json.dumps({k:v for k,v in r.items() if k!='code'}),flush=True)
json.dump(bestrec,open(args.out,'w'),indent=2);print(json.dumps({'seconds':time.time()-t,'out':args.out}),flush=True)
