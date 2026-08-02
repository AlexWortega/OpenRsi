#!/usr/bin/env python3
"""Product-free inverse-orbit partitions of iterated wreath groups W_{m+1}=W_m wr C2."""
import argparse,json,random,time
# elements recursively encoded integers: W_{m+1}: (a,b,s), size 2*N^2, encode ((a*N+b)<<1)|s
def ops(level):
 if level==1:return 2,(lambda x,y:x^y),(lambda x:x)
 N,mul0,inv0=ops(level-1)
 def dec(x):return x//(2*N), (x//2)%N, x&1
 def enc(a,b,s):return ((a*N+b)<<1)|s
 def mul(x,y):
  a,b,s=dec(x);c,d,t=dec(y)
  if s:return enc(mul0(a,d),mul0(b,c),s^t)
  return enc(mul0(a,c),mul0(b,d),s^t)
 def inv(x):
  a,b,s=dec(x)
  if s:return enc(inv0(b),inv0(a),1)
  return enc(inv0(a),inv0(b),0)
 return 2*N*N,mul,inv
def build(level):
 N,mul,inv=ops(level);oid={};O=[]
 for x in range(1,N):
  if x not in oid:
   o=sorted(set((x,inv(x))));i=len(O);O.append(o)
   for z in o:oid[z]=i
 C=set();one=[]
 for x in range(1,N):
  for y in range(1,N):
   z=mul(x,y)
   if z:
    h=tuple(sorted(set((oid[x],oid[y],oid[z]))));C.add(h)
    if len(h)==1:one.append((x,y,z))
 return N,O,sorted(C),one
def solve(n,C,k,sec,seed):
 R=random.Random(seed);c=[R.randrange(k) for _ in range(n)];inc=[[]for _ in range(n)]
 for j,h in enumerate(C):
  for x in h:inc[x].append(j)
 def v(h):return len({c[x]for x in h})==1
 bad={j for j,h in enumerate(C)if v(h)};best=len(bad);bc=c[:];end=time.time()+sec;it=0
 while bad and time.time()<end:
  h=C[R.choice(tuple(bad))];x=R.choice(h);sc=[]
  for a in range(k):c[x]=a;sc.append(sum(v(C[j])for j in inc[x]))
  z=min(sc);c[x]=R.choice([a for a,s in enumerate(sc)if s==z])
  for j in inc[x]:
   if v(C[j]):bad.add(j)
   else:bad.discard(j)
  if len(bad)<best:best=len(bad);bc=c[:];print('best',best,'iter',it,flush=True)
  if it%20000==19999:
   for _ in range(max(1,n//20)):c[R.randrange(n)]=R.randrange(k)
   bad={j for j,h in enumerate(C)if v(h)}
  it+=1
 return best,bc,it
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--level',type=int,default=3);p.add_argument('--k',type=int,default=5);p.add_argument('--seconds',type=int,default=270);p.add_argument('--out');a=p.parse_args();N,O,C,one=build(a.level);print({'level':a.level,'order':N,'orbits':len(O),'constraints':len(C),'one':len(one)},flush=True)
 if one:print('ONE',one[0]);raise SystemExit
 best,col,it=solve(len(O),C,a.k,a.seconds,1);r={'level':a.level,'k':a.k,'order':N,'orbits':O,'colors':col,'best':best};print({'best':best},flush=True);json.dump(r,open(a.out or f'experiments/wreath{a.level}_k{a.k}.json','w'))
