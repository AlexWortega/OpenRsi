#!/usr/bin/env python3
"""Min-conflicts inverse-orbit product-free partitions of H(Z/qZ).
Heuristic only. A zero-conflict output must be independently verified.
"""
import argparse,json,random,time

def mul(x,y,q):
 a,b,c=x; d,e,f=y
 return ((a+d)%q,(b+e)%q,(c+f+a*e)%q)
def inv(x,q):
 a,b,c=x
 return ((-a)%q,(-b)%q,(-c+a*b)%q)
def build(q):
 e=(0,0,0); elems=[(a,b,c) for a in range(q) for b in range(q) for c in range(q) if (a,b,c)!=e]
 oid={}; orbits=[]
 for x in elems:
  if x in oid: continue
  y=inv(x,q); i=len(orbits); orb=sorted(set((x,y))); orbits.append(orb)
  for z in orb: oid[z]=i
 constraints=set()
 one=[]
 for x in elems:
  for y in elems:
   z=mul(x,y,q)
   if z==e: continue
   h=tuple(sorted(set((oid[x],oid[y],oid[z]))))
   if len(h)==1: one.append((x,y,z,h[0]))
   constraints.add(h)
 return orbits,sorted(constraints),one

def solve(n,cons,k,seconds,seed):
 rng=random.Random(seed); col=[rng.randrange(k) for _ in range(n)]; inc=[[] for _ in range(n)]
 for j,h in enumerate(cons):
  for x in h: inc[x].append(j)
 def violated(h): return len(h)>1 and len({col[x] for x in h})==1
 bad={j for j,h in enumerate(cons) if violated(h)}; best=len(bad); bc=col[:]; end=time.time()+seconds; it=0
 while bad and time.time()<end:
  j=rng.choice(tuple(bad)); h=cons[j]; x=rng.choice(h); old=col[x]
  scores=[]
  for c in range(k):
   col[x]=c; scores.append(sum(violated(cons[t]) for t in inc[x]))
  m=min(scores); opts=[c for c,s in enumerate(scores) if s==m]; col[x]=rng.choice(opts)
  for t in inc[x]:
   if violated(cons[t]): bad.add(t)
   else: bad.discard(t)
  if len(bad)<best: best=len(bad); bc=col[:]; print('best',best,'iter',it,flush=True)
  if it%10000==9999 and bad:
   for _ in range(max(1,n//20)): col[rng.randrange(n)]=rng.randrange(k)
   bad={j for j,h in enumerate(cons) if violated(h)}
  it+=1
 return best,bc,it

def main():
 p=argparse.ArgumentParser();p.add_argument('--q',type=int,default=4);p.add_argument('--k',type=int,default=5);p.add_argument('--seconds',type=int,default=240);p.add_argument('--seed',type=int,default=1);p.add_argument('--out');a=p.parse_args()
 orb,cons,one=build(a.q); print(json.dumps({'q':a.q,'order':a.q**3,'orbits':len(orb),'constraints':len(cons),'one_state':len(one)}),flush=True)
 if one: print('IMPOSSIBLE_MODEL_WITNESS',one[0]); return
 best,col,it=solve(len(orb),cons,a.k,a.seconds,a.seed); result={'q':a.q,'k':a.k,'order':a.q**3,'orbits':orb,'colors':col,'best':best,'iterations':it}
 print(json.dumps({x:result[x] for x in ('q','k','order','best','iterations')}),flush=True)
 with open(a.out or f'experiments/heisenberg_q{a.q}_k{a.k}.json','w') as f: json.dump(result,f)
if __name__=='__main__':main()
