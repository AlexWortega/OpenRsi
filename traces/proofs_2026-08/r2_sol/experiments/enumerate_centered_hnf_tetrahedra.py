#!/usr/bin/env python3
# Question: among centered integer tetrahedra represented by small-determinant Hermite normal forms, can normalized volume exceed 64 without a second interior lattice point?
import argparse, json, math, time
from fractions import Fraction

ap=argparse.ArgumentParser();ap.add_argument('--max-det',type=int,default=100);ap.add_argument('--out',default='experiments/centered_hnf_tetrahedra.json');args=ap.parse_args()
# Lower-triangular column-HNF convention used here: [[a,0,0],[b,d,0],[c,e,f]],
# with 0<=b,c<a and 0<=e<d.  We independently test uniqueness of quotient reps.
def inv_apply(a,b,c,d,e,f,z):
 # Solve A r=z exactly for lower triangular A.
 r0=Fraction(z[0],a);r1=Fraction(z[1]-b*r0,d);r2=Fraction(z[2]-c*r0-e*r1,f)
 return tuple(x-math.floor(x) for x in (r0,r1,r2))
def centered(a,b,c,d,e,f):
 # v4=-(column1+column2+column3)/4 must be integral.
 return a%4==0 and (b+d)%4==0 and (c+e+f)%4==0
def interior_reps(a,b,c,d,e,f):
 # z=(i,j,k), 0<=i<a,0<=j<d,0<=k<f is a complete quotient set
 # for this triangular convention; verify distinctness adversarially.
 reps=[]
 for i in range(a):
  for j in range(d):
   for k in range(f):reps.append(inv_apply(a,b,c,d,e,f,(i,j,k)))
 assert len(set(reps))==a*d*f
 return [r for r in reps if all(x>0 for x in r) and sum(r)<1]
start=time.time();tested=cent=feasible=0;best=0;winners=[];bydet={}
for D in range(1,args.max_det+1):
 for a in range(1,D+1):
  if D%a:continue
  for d in range(1,D//a+1):
   if (D//a)%d:continue
   f=D//a//d
   for b in range(a):
    for c in range(a):
     for e in range(d):
      tested+=1
      if not centered(a,b,c,d,e,f):continue
      cent+=1;ints=interior_reps(a,b,c,d,e,f)
      # The centered origin is r=(1/4,1/4,1/4); require it and no other.
      if ints != [(Fraction(1,4),)*3]:continue
      feasible+=1;bydet[D]=bydet.get(D,0)+1
      H=((a,0,0),(b,d,0),(c,e,f))
      if D>best:best=D;winners=[H]
      elif D==best:winners.append(H)
out={'max_det_searched':args.max_det,'tested_hnfs':tested,'centered_hnfs':cent,'feasible_hnfs':feasible,'best_det':best,'best_volume':best/6,'winner_count':len(winners),'winners':winners,'feasible_by_det':bydet,'seconds':time.time()-start}
json.dump(out,open(args.out,'w'),indent=2);print(json.dumps({k:v for k,v in out.items() if k not in ('winners','feasible_by_det')}),flush=True)
