#!/usr/bin/env python3
# Question: do iterated Mycielski triangle-free graphs yield growing strong-cube code bases?
import argparse,json,numpy as np,networkx as nx
ap=argparse.ArgumentParser();ap.add_argument('--levels',type=int,default=2);ap.add_argument('--restarts',type=int,default=5000);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='experiments/mycielski_greedy.json');args=ap.parse_args()
H=nx.cycle_graph(5)
for _ in range(args.levels):H=nx.mycielskian(H)
n=len(H); A=np.zeros((n,n),dtype=bool)
for u,v in H.edges():A[u,v]=A[v,u]=1
words=np.indices((n,n,n),dtype=np.int16).reshape(3,-1).T
rng=np.random.default_rng(args.seed);best=[]
for r in range(args.restarts):
 cand=np.arange(len(words));code=[]
 while len(cand):
  # Prefer among a small random sample the word retaining most sampled candidates.
  sample=rng.choice(cand,size=min(16,len(cand)),replace=False); probe=rng.choice(cand,size=min(256,len(cand)),replace=False)
  scores=[]
  for x in sample:
   w=words[x];scores.append(np.count_nonzero(A[w[0],words[probe,0]]|A[w[1],words[probe,1]]|A[w[2],words[probe,2]]))
  x=sample[int(np.argmax(scores))];code.append(int(x));w=words[x]
  cand=cand[A[w[0],words[cand,0]]|A[w[1],words[cand,1]]|A[w[2],words[cand,2]]]
 if len(code)>len(best):best=code;print('best',len(best),'base',len(best)**(1/3),flush=True)
data={'vertices':n,'levels':args.levels,'size':len(best),'base':len(best)**(1/3),'code':[words[i].tolist() for i in best]}
with open(args.out,'w') as f:json.dump(data,f,indent=2)
print(json.dumps({k:v for k,v in data.items() if k!='code'}),flush=True)
