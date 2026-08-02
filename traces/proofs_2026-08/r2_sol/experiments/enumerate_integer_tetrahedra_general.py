#!/usr/bin/env python3
# Question: which centroid-zero lattice-free integer tetrahedra maximize volume in a chosen coordinate box?
import argparse,json,itertools,time
ap=argparse.ArgumentParser();ap.add_argument('--lo',type=int,default=-2);ap.add_argument('--hi',type=int,default=4);ap.add_argument('--out',default='experiments/integer_tetrahedra_general.json');args=ap.parse_args()
pts=list(itertools.product(range(args.lo,args.hi+1),repeat=3));S=set(pts)
def sub(a,b):return tuple(a[i]-b[i] for i in range(3))
def det(a,b,c):return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
def inside(v,p):
 a,b,c,d=v;A=sub(a,d);B=sub(b,d);C=sub(c,d);q=sub(p,d);D=det(A,B,C)
 ns=[det(q,B,C),det(A,q,C),det(A,B,q)];ns.append(D-sum(ns))
 return all(x>0 for x in ns) if D>0 else all(x<0 for x in ns)
best=0;winners=[];feasible=0;tested=0;t=time.time()
for a,b,c in itertools.combinations(pts,3):
 d=tuple(-a[i]-b[i]-c[i] for i in range(3))
 if d not in S or not c<d:continue
 tested+=1;v=(a,b,c,d);D=det(sub(a,d),sub(b,d),sub(c,d))
 if not D:continue
 lo=[min(x[i] for x in v) for i in range(3)];hi=[max(x[i] for x in v) for i in range(3)]
 if any(p!=(0,0,0) and inside(v,p) for p in itertools.product(*(range(lo[i]+1,hi[i]) for i in range(3)))):continue
 feasible+=1
 if abs(D)>best:best=abs(D);winners=[v]
 elif abs(D)==best:winners.append(v)
out={'box':[args.lo,args.hi],'tested_nondeferred':tested,'feasible':feasible,'max_det':best,'max_volume':best/6,'winner_count':len(winners),'winners':winners,'seconds':time.time()-t}
json.dump(out,open(args.out,'w'),indent=2);print(json.dumps({k:v for k,v in out.items() if k!='winners'}),flush=True)
