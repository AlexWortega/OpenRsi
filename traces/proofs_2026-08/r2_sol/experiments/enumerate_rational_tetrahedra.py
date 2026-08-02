#!/usr/bin/env python3
# Question: among centroid-zero denominator-D tetrahedra in a box, can volume exceed 32/3 while lattice-free?
import argparse,itertools,json,time
ap=argparse.ArgumentParser();ap.add_argument('-D',type=int,default=2);ap.add_argument('--lo',type=int,default=-1);ap.add_argument('--hi',type=int,default=2);ap.add_argument('--out',default='experiments/rational_tetra.json');args=ap.parse_args()
# Work with integer numerators; lattice query p is represented by D*p.
loN=args.lo*args.D;hiN=args.hi*args.D;pts=list(itertools.product(range(loN,hiN+1),repeat=3));S=set(pts)
def sub(a,b):return tuple(a[i]-b[i] for i in range(3))
def det(a,b,c):return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
def inside(v,p):
 a,b,c,d=v;A=sub(a,d);B=sub(b,d);C=sub(c,d);q=sub(p,d);V=det(A,B,C)
 ns=[det(q,B,C),det(A,q,C),det(A,B,q)];ns+=[V-sum(ns)]
 return all(x>0 for x in ns) if V>0 else all(x<0 for x in ns)
best=feasible=tested=0;W=[];t=time.time()
for a,b,c in itertools.combinations(pts,3):
 d=tuple(-a[i]-b[i]-c[i] for i in range(3))
 if d not in S or not c<d:continue
 tested+=1;v=(a,b,c,d);V=det(sub(a,d),sub(b,d),sub(c,d))
 if not V:continue
 mn=[min(x[i] for x in v)//args.D-1 for i in range(3)];mx=[max(x[i] for x in v)//args.D+2 for i in range(3)]
 if any(p!=(0,0,0) and inside(v,tuple(args.D*x for x in p)) for p in itertools.product(*(range(mn[i],mx[i]+1) for i in range(3)))):continue
 feasible+=1
 if abs(V)>best:best=abs(V);W=[v]
 elif abs(V)==best:W.append(v)
out={'D':args.D,'box':[args.lo,args.hi],'tested':tested,'feasible':feasible,'max_scaled_det':best,'max_volume':best/(6*args.D**3),'winner_count':len(W),'winners':W,'seconds':time.time()-t}
json.dump(out,open(args.out,'w'),indent=2);print(json.dumps({k:v for k,v in out.items() if k!='winners'}),flush=True)
