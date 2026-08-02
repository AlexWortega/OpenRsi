#!/usr/bin/env python3
"""Search linear correlated codes for triangle-free Cayley graphs over F_2^r."""
import argparse,random,json,time

def sumfree(S):
 T=set(S)
 return all((x^y)not in T for x in S for y in S if x!=y)
def greedy_S(r,R):
 U=list(range(1,1<<r));R.shuffle(U);S=[];T=set()
 for x in U:
  if all((x^y)not in T for y in S) and all((y^z)!=x for i,y in enumerate(S)for z in S[:i]):S.append(x);T.add(x)
 return S
def eval_bad(rows,S,m,r):
 D=len(rows);bad=[];mask=(1<<r)-1
 for u in range(1,1<<D):
  w=0
  for i,row in enumerate(rows):
   if u>>i&1:w^=row
  if all(((w>>(j*r))&mask)not in S for j in range(m)):bad.append(u)
 return bad
def search(r,m,D,sec,R):
 S=greedy_S(r,R);rows=[R.randrange(1,1<<(m*r))for _ in range(D)];bad=eval_bad(rows,set(S),m,r);best=len(bad);br=rows[:];end=time.time()+sec;it=0
 while bad and time.time()<end:
  i=R.randrange(D);old=rows[i];rows[i]=R.randrange(1,1<<(m*r));b=eval_bad(rows,set(S),m,r)
  if len(b)<=len(bad)or R.random()<.002:bad=b
  else:rows[i]=old
  if len(bad)<best:best=len(bad);br=rows[:];print('best',best,'r,m,D',r,m,D,flush=True)
  if it%20000==19999:S=greedy_S(r,R);bad=eval_bad(rows,set(S),m,r)
  it+=1
 return S,br,best
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seconds',type=int,default=270);p.add_argument('--out',default='experiments/linear_cayley_codes.json');a=p.parse_args();R=random.Random(4);end=time.time()+a.seconds;out=[]
 cases=[(4,3,6),(5,3,7),(6,3,8),(6,4,10),(7,4,11),(8,5,14)]
 for r,m,D in cases:
  S,rows,b=search(r,m,D,min(40,max(1,end-time.time())),R);rec={'r':r,'m':m,'D':D,'base':2**(D/m),'S':S,'rows':rows,'bad':b};out.append(rec);print({k:v for k,v in rec.items()if k not in('S','rows')},flush=True);json.dump(out,open(a.out,'w'))
  if time.time()>end:break
