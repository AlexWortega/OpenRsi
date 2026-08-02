#!/usr/bin/env python3
"""Heuristic correlated-code search in OR powers of random maximal triangle-free graphs.
No output is a proof; candidates are written for independent verification.
"""
import argparse, json, math, random, time

def tf_graph(n, rng):
    adj=[0]*n
    pairs=[(i,j) for i in range(n) for j in range(i)]
    rng.shuffle(pairs)
    for i,j in pairs:
        if not (adj[i]&adj[j]):
            adj[i]|=1<<j; adj[j]|=1<<i
    return adj

def covers(a,b,adj): return any(x!=y and ((adj[x]>>y)&1) for x,y in zip(a,b))

def search(adj,m,M,rng,seconds):
    n=len(adj); words=[tuple(rng.randrange(n) for _ in range(m)) for _ in range(M)]
    bad=set()
    def reset(i):
        for j in range(M):
            if i!=j: bad.discard((min(i,j),max(i,j)))
        for j in range(M):
            if i!=j and not covers(words[i],words[j],adj): bad.add((min(i,j),max(i,j)))
    for i in range(M): reset(i)
    best=len(bad); bestw=list(words); end=time.time()+seconds; it=0
    while time.time()<end and bad:
        i,j=rng.choice(tuple(bad)); x=i if rng.random()<.5 else j
        old=words[x]; oldbad=len(bad); candidate=old
        # Sample mutations and retain the locally best one.
        score=oldbad
        for _ in range(40):
            w=list(old)
            if rng.random()<.7: w[rng.randrange(m)]=rng.randrange(n)
            else: w=[rng.randrange(n) for _ in range(m)]
            words[x]=tuple(w); reset(x); s=len(bad)
            if s<score: score=s; candidate=tuple(w)
        words[x]=candidate; reset(x)
        if len(bad)>oldbad and rng.random()>.02:
            words[x]=old; reset(x)
        if len(bad)<best: best=len(bad); bestw=list(words)
        it+=1
    return best,bestw,it

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--seconds',type=int,default=240); ap.add_argument('--seed',type=int,default=1); ap.add_argument('--out',default='experiments/tf_power_candidates.json')
    a=ap.parse_args(); rng=random.Random(a.seed); deadline=time.time()+a.seconds; records=[]
    # increasing orders; targets around and above prior fixed benchmarks
    cases=[(14,3,13),(18,3,14),(22,4,40),(28,4,60),(36,5,160)]
    while time.time()<deadline:
        n,m,M=cases[len(records)%len(cases)]; adj=tf_graph(n,rng)
        budget=min(12,max(1,deadline-time.time())); bad,w,it=search(adj,m,M,rng,budget)
        rec={'n':n,'m':m,'M':M,'bad':bad,'base':M**(1/m),'edges':sum(x.bit_count() for x in adj)//2,'adj':adj if bad==0 else None,'words':w if bad==0 else None,'iterations':it}
        records.append(rec); print(json.dumps({k:v for k,v in rec.items() if k not in ('adj','words')}),flush=True)
        with open(a.out,'w') as f: json.dump(records,f)
if __name__=='__main__': main()
