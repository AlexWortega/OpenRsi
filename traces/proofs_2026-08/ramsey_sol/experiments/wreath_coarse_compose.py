#!/usr/bin/env python3
"""Exact coarse-state composition constraints for W_{m+1} from a verified W_m partition."""
import argparse,json,itertools,random,time
from wreath2_partition import ops

def main(inp,k,sec,out):
 r=json.load(open(inp));lev=r['level'];N,mul,inv=ops(lev);own={0:-1}
 for i,o in enumerate(r['orbits']):
  for x in o:own[x]=r['colors'][i]
 states=sorted({(own[a],own[b],s)for a in range(N)for b in range(N)for s in range(2)if(a,b,s)!=(0,0,0)});ix={x:i for i,x in enumerate(states)};C=set();one=[]
 def wm(x,y,s,t):return (mul(x,y)if not s else mul(x,y[1]) if False else 0)
 # stream all pairs of W_{lev+1}; at lev3 this is 1B impossible. Instead enumerate coarse realizations
 # with representative-level multiplication tables: gather output coarse states for each input coarse pair.
 elems=[(a,b,s)for a in range(N)for b in range(N)for s in range(2)if(a,b,s)!=(0,0,0)]
 buckets={z:[]for z in states}
 for e in elems:buckets[own[e[0]],own[e[1]],e[2]].append(e)
 # sample/exhaust exact only if product bucket sizes manageable; random discrimination
 rng=random.Random(1); keys=states
 for _ in range(3000000):
  A=rng.choice(keys);B=rng.choice(keys);a,b,s=rng.choice(buckets[A]);c,d,t=rng.choice(buckets[B])
  if s:z=(mul(a,d),mul(b,c),s^t)
  else:z=(mul(a,c),mul(b,d),s^t)
  if z!=(0,0,0):
   Z=(own[z[0]],own[z[1]],z[2]);h=tuple(sorted(set((ix[A],ix[B],ix[Z]))));C.add(h)
   if len(h)==1:one.append((A,B,Z))
 print({'states':len(states),'sampled_constraints':len(C),'one':len(one)},flush=True)
 if one:print('ONE',one[0]);return
 C=sorted(C)
 col=[rng.randrange(k)for _ in states];inc=[[]for _ in states]
 for j,h in enumerate(C):
  for x in h:inc[x].append(j)
 def bad(h):return len({col[x]for x in h})==1
 B={j for j,h in enumerate(C)if bad(h)};best=len(B);bc=col[:];end=time.time()+sec;it=0
 while B and time.time()<end:
  h=C[rng.choice(tuple(B))];x=rng.choice(h);scores=[]
  for c in range(k):col[x]=c;scores.append(sum(bad(C[j])for j in inc[x]))
  z=min(scores);col[x]=rng.choice([c for c,s in enumerate(scores)if s==z])
  for j in inc[x]:
   if bad(C[j]):B.add(j)
   else:B.discard(j)
  if len(B)<best:best=len(B);bc=col[:];print('best',best,flush=True)
  it+=1
 print({'best':best},flush=True);json.dump({'input':inp,'k':k,'states':states,'colors':bc,'best':best,'sampled':True},open(out,'w'))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',default='experiments/wreath3_k6.json');p.add_argument('--k',type=int,default=12);p.add_argument('--seconds',type=int,default=240);p.add_argument('--out',default='experiments/wreath4_coarse.json');a=p.parse_args();main(a.input,a.k,a.seconds,a.out)
