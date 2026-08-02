#!/usr/bin/env python3
# Question: can the independently verified corrected 3-block state hypergraph be colored with q colors, starting from its repeated-state graph structure?
import argparse, json, random, time
import networkx as nx

ap=argparse.ArgumentParser();ap.add_argument('-q',type=int,default=14);ap.add_argument('--steps',type=int,default=2000000);ap.add_argument('--restarts',type=int,default=20);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/block_power_correct.json');args=ap.parse_args();rng=random.Random(args.seed)
data=json.load(open('experiments/block_power_constraints_t3.json'));states=[tuple(s) for s in data['states']];constraints=[tuple(u) for u in data['constraints']]
pairs=[u for u in constraints if len(u)==2]; triples=[u for u in constraints if len(u)==3];G=nx.Graph();G.add_nodes_from(range(len(states)));G.add_edges_from(pairs)
inc=[[] for _ in states]
for j,u in enumerate(constraints):
 for x in u:inc[x].append(j)
def bad(c,u):return len({c[x] for x in u})==1
def dsatur():
 d=nx.coloring.greedy_color(G,strategy='saturation_largest_first'); return [d[i] for i in range(len(states))]
base=dsatur();baseq=1+max(base);print(json.dumps({'states':len(states),'pairs':len(pairs),'triples':len(triples),'dsatur_colors':baseq,'dsatur_bad_triples':sum(bad(base,u) for u in triples)}),flush=True)
best=10**9;t0=time.time()
for restart in range(args.restarts):
 if restart==0 and baseq<=args.q:c=base[:]
 else:
  # Perturb the proper pair-graph coloring rather than discard its structure.
  c=base[:] if baseq<=args.q else [rng.randrange(args.q) for _ in states]
  for _ in range(5*restart):c[rng.randrange(len(c))]=rng.randrange(args.q)
 B={j for j,u in enumerate(constraints) if bad(c,u)}
 for step in range(args.steps):
  if not B:
   json.dump({'t':3,'q':args.q,'mapping':{','.join(map(str,s)):c[i] for i,s in enumerate(states)}},open(args.out,'w'),indent=2);print(json.dumps({'found':True,'restart':restart,'step':step,'seconds':time.time()-t0}),flush=True);raise SystemExit
  if len(B)<best:best=len(B);print('best',best,'restart',restart,'step',step,flush=True)
  x=rng.choice(constraints[rng.choice(tuple(B))]);scores=[]
  for z in range(args.q):c[x]=z;scores.append(sum(bad(c,constraints[j]) for j in inc[x]))
  m=min(scores);c[x]=rng.randrange(args.q) if rng.random()<.01 else rng.choice([z for z,v in enumerate(scores) if v==m])
  for j in inc[x]:
   if bad(c,constraints[j]):B.add(j)
   else:B.discard(j)
print(json.dumps({'found':False,'best':best,'seconds':time.time()-t0}),flush=True)
