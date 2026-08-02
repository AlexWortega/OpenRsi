#!/usr/bin/env python3
# Question: for random centered 3-polytopes scaled to first lattice contact, how does volume correlate with the best primitive-direction width*zero-section-asymmetry^2 certificate?
import argparse, itertools, json, math
import numpy as np
from scipy.spatial import ConvexHull

ap=argparse.ArgumentParser(); ap.add_argument('--samples',type=int,default=3000); ap.add_argument('--vertices',type=int,default=7); ap.add_argument('--seed',type=int,default=1); ap.add_argument('--lattice-box',type=int,default=7); ap.add_argument('--direction-box',type=int,default=2); ap.add_argument('--out',default='experiments/directional_stress.json'); args=ap.parse_args()
rng=np.random.default_rng(args.seed)
Z=np.array([z for z in itertools.product(range(-args.lattice_box,args.lattice_box+1),repeat=3) if z!=(0,0,0)],float)
dirs=[]
for u in itertools.product(range(-args.direction_box,args.direction_box+1),repeat=3):
 if u==(0,0,0):continue
 g=math.gcd(math.gcd(abs(u[0]),abs(u[1])),abs(u[2]))
 if g!=1:continue
 # identify u and -u
 if next(x for x in u if x)!=abs(next(x for x in u if x)):continue
 dirs.append(np.array(u,float))

def centroid_volume(p,h):
 q=p.mean(0); V=0.; M=np.zeros(3)
 for tri in h.simplices:
  a,b,c=p[tri]; v=abs(np.linalg.det(np.stack([a-q,b-q,c-q],1)))/6
  V+=v; M+=v*(q+a+b+c)/4
 return M/V,V

def section_vertices(p,h,u):
 vals=p@u; out=[]; edges=set()
 for tri in h.simplices:
  for i,j in itertools.combinations(tri,2):edges.add(tuple(sorted((int(i),int(j)))))
 for i,j in edges:
  a,b=vals[i],vals[j]
  if abs(a)<1e-10:out.append(p[i])
  if a*b< -1e-12:out.append(p[i]+(-a/(b-a))*(p[j]-p[i]))
 if len(out)<3:return None
 out=np.unique(np.round(out,12),axis=0)
 if len(out)<3:return None
 e1=np.cross(u,[1.,0.,0.] if abs(u[0])<.8*np.linalg.norm(u) else [0.,1.,0.]);e1/=np.linalg.norm(e1);e2=np.cross(u,e1);e2/=np.linalg.norm(e2)
 q=np.stack([out@e1,out@e2],1)
 try:hh=ConvexHull(q)
 except Exception:return None
 q=q[hh.vertices]; hh=ConvexHull(q); b=hh.equations[:,2]
 if np.max(b)>=-1e-8:return None
 rho=max(max((hh.equations[:,:2]@(-v))/(-b)) for v in q)
 return max(rho,1.0)

def evaluate(raw):
 try:h=ConvexHull(raw); cen,V=centroid_volume(raw,h);p=raw-cen;h=ConvexHull(p)
 except Exception:return None
 off=-h.equations[:,3]
 if off.min()<=1e-9:return None
 gauge=(Z@h.equations[:,:3].T/off).max(1); pos=gauge[gauge>1e-10]
 if not len(pos):return None
 scale=pos.min();p*=scale;h=ConvexHull(p);vol=V*scale**3
 best=1e99; bestu=None;bestrho=None
 for u in dirs:
  rho=section_vertices(p,h,u)
  if rho is None:continue
  width=(p@u).max()-(p@u).min(); score=width*rho*rho
  if score<best:best,bestu,bestrho=score,u.tolist(),rho
 return {'volume':float(vol),'best_score':float(best),'direction':bestu,'rho':float(bestrho)}

records=[]
# Include the sharp simplex as a calibration.
sharp=np.array([[-1,-1,-1],[3,-1,-1],[-1,3,-1],[-1,-1,3]],float); records.append({'kind':'sharp',**evaluate(sharp)})
for _ in range(args.samples):
 d=rng.normal(size=(args.vertices,3));d/=np.linalg.norm(d,axis=1)[:,None];raw=d*np.exp(rng.normal(0,1,size=args.vertices))[:,None]
 r=evaluate(raw)
 if r:records.append({'kind':'random',**r})
records.sort(key=lambda r:r['volume'],reverse=True)
out={'target_score':8/3,'target_volume':32/3,'samples':args.samples,'top':records[:100]}
json.dump(out,open(args.out,'w'),indent=2);print(json.dumps({'evaluated':len(records),'best':records[0],'sharp':next(r for r in records if r['kind']=='sharp'),'out':args.out}),flush=True)
