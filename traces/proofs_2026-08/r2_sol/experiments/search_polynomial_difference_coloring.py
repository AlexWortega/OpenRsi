#!/usr/bin/env python3
# Question: can polynomial hash formulas color integer differences with k colors on N superexponential in k?
import argparse,itertools,json,random
ap=argparse.ArgumentParser();ap.add_argument('-N',type=int,default=1000);ap.add_argument('-k',type=int,default=8);ap.add_argument('--trials',type=int,default=100000);ap.add_argument('--seed',type=int,default=1);args=ap.parse_args();rng=random.Random(args.seed);N,k=args.N,args.k
# Try c(d)=sum a_j digit_j(d) mod k in mixed bases.
for t in range(args.trials):
 base=rng.randrange(2,20);deg=rng.randrange(1,8);a=[rng.randrange(k) for _ in range(deg)]
 def c(d):
  z=0
  for q in a:z=(z+q*(d%base))%k;d//=base
  return z
 ok=True
 for x in range(1,N):
  for y in range(x+1,N):
   if c(x)==c(y)==c(y-x):ok=False;break
  if not ok:break
 if ok:print(json.dumps({'N':N,'k':k,'base':base,'coeff':a}));break
else:print(json.dumps({'found':False}))
