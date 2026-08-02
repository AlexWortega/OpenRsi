#!/usr/bin/env python3
"""Search triangle-free graphs on constant-weight subsets and correlated power codes.
Adjacency rules by intersection size; triangle-free is checked exactly.
"""
import itertools,random,argparse,json,time

def graph(n,r,T):
 V=list(itertools.combinations(range(n),r));S=list(map(set,V));A=[0]*len(V)
 for i in range(len(V)):
  for j in range(i):
   if len(S[i]&S[j]) in T:A[i]|=1<<j;A[j]|=1<<i
 tri=next(((i,j,h) for i in range(len(V)) for j in range(i) if (A[i]>>j)&1 for h in range(j) if (A[i]>>h)&1 and (A[j]>>h)&1),None)
 return V,A,tri
def greedy(A,m,sec,rng):
 n=len(A);W=list(itertools.product(range(n),repeat=m));rng.shuffle(W);C=[];end=time.time()+sec
 for w in W:
  if all(any(x!=y and (A[x]>>y)&1 for x,y in zip(w,z)) for z in C):C.append(w)
  if time.time()>end:break
 return C
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seconds',type=int,default=270);a=p.parse_args();rng=random.Random(1);end=time.time()+a.seconds;out=[]
 for n in range(5,11):
  for r in range(2,min(5,n)):
   for mask in range(1,1<<r):
    T={i for i in range(r) if mask>>i&1};V,A,tri=graph(n,r,T)
    if tri or not any(A):continue
    rec={'n':n,'r':r,'T':sorted(T),'v':len(V),'edges':sum(x.bit_count() for x in A)//2}
    for m in (2,3):
     if len(V)**m<=300000:
      C=greedy(A,m,min(3,max(0,end-time.time())),rng);rec[f'M{m}']=len(C);rec[f'base{m}']=len(C)**(1/m)
    out.append(rec);print(rec,flush=True)
    if time.time()>end:break
   if time.time()>end:break
  if time.time()>end:break
 json.dump(out,open('experiments/hamming_subset_codes.json','w'))
