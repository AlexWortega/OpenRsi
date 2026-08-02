#!/usr/bin/env python3
"""Test the oracle's explicit anchored-palette greedy process.

Color graphs are maintained triangle-free using integer bitset neighborhoods.
Failure edges are left uncolored. A greedy independent set in the failure graph
then gives an induced fully-colored valid seed, which is independently checked.
"""
import argparse, itertools, json, random, time

def run(r,g,variant,seed=1):
    random.seed(seed); U=range(3,g+1)
    verts=[(a,B) for a in (1,2) for B in itertools.combinations(U,r-1)]
    pals=[frozenset((0,a,*B)) for a,B in verts]; n=len(verts)
    edges=[(i,j,len(pals[i]&pals[j])) for i in range(n) for j in range(i+1,n)]
    if variant in ('list','load'): edges.sort(key=lambda x:(x[2],x[0],x[1]))
    elif variant=='random': random.shuffle(edges)
    # neigh[c][v] bitset of neighbors at color c
    neigh=[[0]*n for _ in range(g+1)]; loads=[0]*(g+1); failures=[]; first=None
    for idx,(u,v,ls) in enumerate(edges):
        colors=sorted(pals[u]&pals[v])
        legal=[c for c in colors if not (neigh[c][u]&neigh[c][v])]
        if not legal:
            witnesses={c:(neigh[c][u]&neigh[c][v]).bit_length()-1 for c in colors}
            failures.append((u,v,ls));
            if first is None:first={'u':u,'v':v,'list':colors,'witnesses':witnesses,'at_edge':idx}
            continue
        if variant in ('load','random'): c=min(legal,key=lambda x:(loads[x],random.random() if variant=='random' else x))
        else:c=legal[0]
        neigh[c][u]|=1<<v;neigh[c][v]|=1<<u;loads[c]+=1
    # Greedy low-failure-degree independent set, several orderings.
    fadj=[0]*n
    for u,v,_ in failures:fadj[u]|=1<<v;fadj[v]|=1<<u
    best=[]
    orders=[sorted(range(n),key=lambda v:(fadj[v].bit_count(),v))]
    for _ in range(20): orders.append(sorted(range(n),key=lambda v:(fadj[v].bit_count(),random.random())))
    for order in orders:
        chosen=0; arr=[]
        for v in order:
            if not (fadj[v]&chosen):chosen|=1<<v;arr.append(v)
        if len(arr)>len(best):best=arr
    # Independent verification on retained vertices: every edge colored, no mono triangle.
    keep=set(best); assert all(not(u in keep and v in keep) for u,v,_ in failures)
    for c in range(g+1):
        for u in best:
            common=neigh[c][u]
            # no adjacent pair among color-c neighbors of u
            x=common
            while x:
                lb=x&-x;v=lb.bit_length()-1;x-=lb
                assert not (neigh[c][v]&common)
    return {'r':r,'g':g,'variant':variant,'seed':seed,'N':n,'edges':len(edges),
            'failures':len(failures),'first_failure':first,'retained_greedy':len(best),
            'loads':loads,'vertices':[(a,list(B)) for a,B in verts], 'retained':best}

def main():
    p=argparse.ArgumentParser();p.add_argument('r',type=int);p.add_argument('g',type=int)
    p.add_argument('--variant',choices=['lex','list','load','random'],default='load');p.add_argument('--seed',type=int,default=1)
    a=p.parse_args();t=time.time();out=run(a.r,a.g,a.variant,a.seed);out['seconds']=time.time()-t
    path=f"experiments/results/anchored_r{a.r}_g{a.g}_{a.variant}_{a.seed}.json"
    with open(path,'w') as f:json.dump(out,f,indent=2)
    slim={k:v for k,v in out.items() if k not in ('vertices','retained','loads')};print(json.dumps(slim,indent=2));print(path)
if __name__=='__main__':main()
