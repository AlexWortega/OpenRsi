#!/usr/bin/env python3
# Question: can edge colors defined by several quadratic characters over F_q produce q vertices with substantially fewer than log q colors?
import argparse,itertools,json
ap=argparse.ArgumentParser();ap.add_argument('-p',type=int,default=101);ap.add_argument('--chars',type=int,default=3);ap.add_argument('--out',default='experiments/quadratic_coloring.json');args=ap.parse_args();p=args.p
# Color difference d by vector of Legendre symbols of d+a_j, symmetrized with -d.
def chi(x):x%=p;return 0 if x==0 else (1 if pow(x,(p-1)//2,p)==1 else -1)
best=None
for shifts in itertools.combinations(range(p),args.chars):
 sig={d:tuple(sorted((tuple(chi(d+a) for a in shifts),tuple(chi(-d+a) for a in shifts)))) for d in range(1,p)}
 col={s:i for i,s in enumerate(sorted(set(sig.values())))};bad=False
 for a in range(1,p):
  for b in range(a+1,p):
   if col[sig[a]]==col[sig[b]]==col[sig[(b-a)%p]]:bad=True;break
  if bad:break
 if not bad and (best is None or len(col)<best['k']):best={'p':p,'shifts':shifts,'k':len(col),'mapping':{str(d):col[sig[d]] for d in sig}};print(best['p'],best['shifts'],best['k'],flush=True)
json.dump(best,open(args.out,'w'),indent=2);print('done',best and best['k'])
