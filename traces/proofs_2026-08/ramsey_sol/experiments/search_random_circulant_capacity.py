#!/usr/bin/env python3
"""Search triangle-free circulant graphs with growing fractional chromatic diagnostic and cube codes."""
import argparse,random,itertools,json,time

def graph(n,D):
 A=[0]*n
 for i in range(n):
  for d in D:
   j=(i+d)%n
   if i!=j:A[i]|=1<<j
 tri=any((A[i]&A[j]) for i in range(n) for j in range(i) if A[i]>>j&1)
 return A,tri
def greedy(A,m,rng):
 n=len(A);W=list(itertools.product(range(n),repeat=m));rng.shuffle(W);C=[]
 for w in W:
  if all(any(x!=y and(A[x]>>y)&1 for x,y in zip(w,z)) for z in C):C.append(w)
 return C
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seconds',type=int,default=270);a=p.parse_args();rng=random.Random(3);end=time.time()+a.seconds;out=[]
 for n in range(11,80,2):
  for t in range(200):
   base={d for d in range(1,(n+1)//2) if rng.random()<.25};D=base|{n-d for d in base};A,tri=graph(n,D)
   if tri or not D:continue
   C=greedy(A,3,rng) if n<=35 else []
   # vertex-transitive chi_f=n/alpha; greedy alpha lower bound gives only diagnostic upper
   I=[]
   for x in rng.sample(range(n),n):
    if all(not(A[x]>>y&1) for y in I):I.append(x)
   r={'n':n,'D':sorted(D),'degree':len(D),'ind_lb':len(I),'chi_f_ub':n/len(I),'cube':len(C),'base':len(C)**(1/3) if C else 0};out.append(r);print(r,flush=True)
   if time.time()>end:break
  if time.time()>end:break
 json.dump(out,open('experiments/random_circulant_capacity.json','w'))
