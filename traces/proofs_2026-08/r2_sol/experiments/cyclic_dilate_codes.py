#!/usr/bin/env python3
# Question: can symmetric sum-free Cayley sets in Z_p have unusually efficient multiplicative-dilate covers, yielding correlated strong-power codes?
import argparse,json,math,random,time
ap=argparse.ArgumentParser();ap.add_argument('--primes',default='17,31,61,127,251,509,1021');ap.add_argument('--restarts',type=int,default=2000);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/cyclic_dilate_codes.json');args=ap.parse_args();rng=random.Random(args.seed)
def isprime(n):return n>1 and all(n%d for d in range(2,int(n**.5)+1))
def valid_add(S,x,p):
 T=S|{x,(-x)%p}
 return all((a+b)%p not in T for a in T for b in T)
def greedy_cover(S,p):
 U=set(range(1,p));A=[];dil={a:{a*x%p for x in S} for a in range(1,p)}
 while U:
  a=max(dil,key=lambda z:len(dil[z]&U));gain=dil[a]&U
  if not gain:return None
  A.append(a);U-=gain
 return A
results=[];t0=time.time()
for p in map(int,args.primes.split(',')):
 assert isprime(p);best=None
 for r in range(args.restarts):
  S=set();cand=list(range(1,(p+1)//2));rng.shuffle(cand)
  # randomized maximal symmetric sum-free set
  while cand:
   sample=cand[:min(12,len(cand))];x=max(sample,key=lambda z:rng.random())
   cand.remove(x)
   if valid_add(S,x,p):S|={x,(-x)%p}
  A=greedy_cover(S,p)
  if A is not None and (best is None or len(A)<len(best['multipliers'])):
   best={'p':p,'S':sorted(S),'multipliers':A,'m':len(A),'base':p**(1/len(A)),'density':len(S)/(p-1)};print(json.dumps(best),flush=True)
 results.append(best)
json.dump(results,open(args.out,'w'),indent=2);print(json.dumps({'seconds':time.time()-t0,'out':args.out}),flush=True)
