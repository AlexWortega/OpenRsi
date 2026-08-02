#!/usr/bin/env python3
"""Heuristic codes for generalized shift graphs on increasing r-tuples."""
import argparse,itertools,json,random,time

def graph(n,r):
 V=list(itertools.combinations(range(n),r));idx={x:i for i,x in enumerate(V)};adj=[0]*len(V)
 for t in itertools.combinations(range(n),r+1):
  a=idx[t[:-1]];b=idx[t[1:]];adj[a]|=1<<b;adj[b]|=1<<a
 return V,adj
def cover(a,b,A):return any(x!=y and (A[x]>>y)&1 for x,y in zip(a,b))
def search(A,m,M,rng,sec):
 n=len(A);w=[tuple(rng.randrange(n) for _ in range(m)) for _ in range(M)]
 def cbad(x):return sum(not cover(w[x],w[y],A) for y in range(M) if y!=x)
 def allbad():return [(i,j) for i in range(M) for j in range(i) if not cover(w[i],w[j],A)]
 bad=allbad();best=len(bad);bw=w[:];end=time.time()+sec;it=0
 while bad and time.time()<end:
  i,j=rng.choice(bad);x=i if rng.random()<.5 else j;old=w[x];cand=[]
  # exploit neighbors of counterpart coordinates
  y=j if x==i else i
  for _ in range(100):
   z=list(old)
   if rng.random()<.7:
    h=rng.randrange(m); neigh=[u for u in range(n) if (A[u]>>w[y][h])&1];z[h]=rng.choice(neigh) if neigh else rng.randrange(n)
   else:z=[rng.randrange(n) for _ in range(m)]
   w[x]=tuple(z);cand.append((cbad(x),tuple(z)))
  w[x]=min(cand)[1];bad=allbad();it+=1
  if len(bad)<best:best=len(bad);bw=w[:]
  if it%500==0 and bad:
   for _ in range(max(1,M//10)):w[rng.randrange(M)]=tuple(rng.randrange(n) for _ in range(m))
   bad=allbad()
 return best,bw,it
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seconds',type=int,default=270);p.add_argument('--seed',type=int,default=5);p.add_argument('--out',default='experiments/generalized_shift_candidates.json');a=p.parse_args();rng=random.Random(a.seed);end=time.time()+a.seconds;out=[]
 cases=[(7,3,3,13),(9,3,3,13),(9,3,4,30),(9,4,4,30),(11,4,5,80)]
 t=0
 while time.time()<end:
  n,r,m,M=cases[t%len(cases)];V,A=graph(n,r);bad,w,it=search(A,m,M,rng,min(15,max(1,end-time.time())));rec={'n':n,'r':r,'alphabet':len(V),'m':m,'M':M,'base':M**(1/m),'bad':bad,'iterations':it,'vertices':V if bad==0 else None,'words':w if bad==0 else None};out.append(rec);print(json.dumps({k:v for k,v in rec.items() if k not in ('vertices','words')}),flush=True);json.dump(out,open(a.out,'w'));t+=1
