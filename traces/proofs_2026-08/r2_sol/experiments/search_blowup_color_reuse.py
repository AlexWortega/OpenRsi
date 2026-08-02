#!/usr/bin/env python3
# Question: can a triangle-free seed be blown up while reusing some outer colors inside clusters, reducing palette cost below additive composition?
import argparse,itertools,json,random,time
ap=argparse.ArgumentParser();ap.add_argument('--seed',choices=['K16','cyclic127'],default='K16');ap.add_argument('-q',type=int,default=2);ap.add_argument('-k',type=int,required=True);ap.add_argument('--steps',type=int,default=3000000);ap.add_argument('--restarts',type=int,default=10);ap.add_argument('--rng',type=int,default=1);ap.add_argument('--out',default='experiments/blowup_reuse.json');args=ap.parse_args();rng=random.Random(args.rng)
if args.seed=='K16':
 C=[{1,2,4,8,15},{3,5,7,10,11},{6,9,12,13,14}];n=16;outer={(a,b):next(i for i,S in enumerate(C) if (a^b) in S) for a,b in itertools.combinations(range(n),2)}
else:
 C=json.load(open('experiments/cyclic_127_5.json'));n=127;col={x:i for i,S in enumerate(C) for x in S};outer={(a,b):col[(b-a)%n] for a,b in itertools.combinations(range(n),2)}
# Cross-cluster colors fixed by outer seed. Optimize internal K_q color at each cluster using same k-palette.
# A mixed triangle forces internal color at cluster a to avoid every outer color incident at a; this is exact.
incident=[{outer[tuple(sorted((a,b)))] for b in range(n) if b!=a} for a in range(n)]
allowed=[set(range(args.k))-P for P in incident]
print(json.dumps({'n':n,'q':args.q,'k':args.k,'outer_colors':len(C),'allowed_sizes':list(map(len,allowed))}),flush=True)
if any(not A for A in allowed):raise SystemExit(2)
# For q=2 one internal edge per cluster and no internal triangle; choices are independent.
if args.q==2:
 choices=[min(A) for A in allowed];json.dump({'seed':args.seed,'q':2,'k':args.k,'internal_colors':choices},open(args.out,'w'),indent=2);print(json.dumps({'found':True,'N':2*n}),flush=True)
else:print(json.dumps({'implemented':False}),flush=True)
