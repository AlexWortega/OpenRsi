#!/usr/bin/env python3
"""Heuristic code search for complements of finite shift graphs.
A shift-graph vertex is an ordered pair (a,b), a<b.  Two are adjacent when
b=c or d=a.  The graph is triangle-free. Output is heuristic only.
"""
import argparse,json,random,time

def graph(n):
 v=[(a,b) for a in range(n) for b in range(a+1,n)]
 adj=[0]*len(v)
 for i,(a,b) in enumerate(v):
  for j,(c,d) in enumerate(v[:i]):
   if b==c or d==a: adj[i]|=1<<j; adj[j]|=1<<i
 return v,adj

def cover(x,y,adj): return any(a!=b and (adj[a]>>b)&1 for a,b in zip(x,y))
def search(adj,m,M,rng,sec):
 n=len(adj); w=[tuple(rng.randrange(n) for _ in range(m)) for _ in range(M)]
 def conflicts(): return [(i,j) for i in range(M) for j in range(i) if not cover(w[i],w[j],adj)]
 bad=conflicts(); best=len(bad); bw=list(w); end=time.time()+sec; it=0
 while bad and time.time()<end:
  i,j=rng.choice(bad); x=i if rng.random()<.5 else j; old=w[x]
  candidates=[old]
  for _ in range(80):
   z=list(old)
   if rng.random()<.8: z[rng.randrange(m)]=rng.randrange(n)
   else: z=[rng.randrange(n) for _ in range(m)]
   candidates.append(tuple(z))
  score=None; chosen=old
  for z in candidates:
   s=sum(not cover(z,w[y],adj) for y in range(M) if y!=x)
   if score is None or s<score: score=s; chosen=z
  w[x]=chosen; bad=conflicts(); it+=1
  if len(bad)<best: best=len(bad); bw=list(w)
  if it%200==0 and bad and rng.random()<.2:
   for _ in range(max(1,M//10)): w[rng.randrange(M)]=tuple(rng.randrange(n) for _ in range(m))
   bad=conflicts()
 return best,bw,it

def main():
 p=argparse.ArgumentParser(); p.add_argument('--seconds',type=int,default=270);p.add_argument('--seed',type=int,default=2);p.add_argument('--out',default='experiments/shift_power_candidates.json');a=p.parse_args()
 rng=random.Random(a.seed); end=time.time()+a.seconds; out=[]
 # Targets deliberately test whether bases move past the constant 3 ceiling.
 cases=[(6,3,13),(8,4,45),(10,5,150),(12,5,200)]
 t=0
 while time.time()<end:
  n,m,M=cases[t%len(cases)]; vertices,adj=graph(n); sec=min(15,max(1,end-time.time())); bad,w,it=search(adj,m,M,rng,sec)
  rec={'n':n,'alphabet':len(adj),'m':m,'M':M,'base':M**(1/m),'bad':bad,'iterations':it,'vertices':vertices if bad==0 else None,'adj':adj if bad==0 else None,'words':w if bad==0 else None}
  out.append(rec); print(json.dumps({k:v for k,v in rec.items() if k not in ('vertices','adj','words')}),flush=True)
  with open(a.out,'w') as f: json.dump(out,f)
  t+=1
if __name__=='__main__': main()
