#!/usr/bin/env python3
"""Heuristic search for the oracle stationary-automaton trace identity.

Templates: C5 and the Groetzsch graph (Mycielski(C5)). Transitions are arbitrary
Boolean matrices. This produces no impossibility claim; every zero-excess
candidate is saved for independent verification.
"""
import argparse, json, math, os, random
import numpy as np
import networkx as nx

def template(name):
    if name == "c5": return nx.cycle_graph(5)
    if name == "grotzsch": return nx.mycielskian(nx.cycle_graph(5))
    raise ValueError(name)

def score(A, H, q):
    n=len(A); P=[(u,v) for u in range(n) for v in range(n) if H[u,v]==0]
    B=np.zeros((len(P),len(P)),dtype=np.int64)
    for i,(u,v) in enumerate(P):
        # Vectorized target condition is already encoded by P.
        B[i,:]=A[u,[x for x,y in P]]*A[v,[y for x,y in P]]
    W=int(np.trace(np.linalg.matrix_power(A,q)))
    WB=int(np.trace(np.linalg.matrix_power(B,q)))
    assert WB>=W
    return WB-W,W

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--graph",default="grotzsch")
    ap.add_argument("--q",type=int,default=3); ap.add_argument("--steps",type=int,default=20000)
    ap.add_argument("--restarts",type=int,default=10); ap.add_argument("--seed",type=int,default=1)
    a=ap.parse_args(); random.seed(a.seed)
    g=template(a.graph); n=len(g); H=nx.to_numpy_array(g,dtype=np.int64)
    best=(10**30,-1,None)
    for restart in range(a.restarts):
        # Start from arbitrary subsets of one H-edge, a guaranteed binary code.
        u,v=random.choice(list(g.edges())); A=np.zeros((n,n),dtype=np.int64)
        A[u,u]=A[u,v]=A[v,u]=A[v,v]=1
        cur=score(A,H,a.q)
        T=2.0
        for step in range(a.steps):
            i=random.randrange(n);j=random.randrange(n); A[i,j]^=1
            new=score(A,H,a.q)
            # Violations dominate; among feasible points maximize W.
            oldobj=cur[0]*100000-cur[1]; newobj=new[0]*100000-new[1]
            temp=max(.01,T*(1-step/a.steps))
            if newobj<=oldobj or random.random()<math.exp(min(0,(oldobj-newobj)/temp)):
                cur=new
            else:A[i,j]^=1
            if cur[0]<best[0] or (cur[0]==best[0] and cur[1]>best[1]):
                best=(cur[0],cur[1],A.copy()); print("best",best[:2],"restart",restart,"step",step,flush=True)
                if best[0]==0:
                    os.makedirs("experiments/results",exist_ok=True)
                    with open(f"experiments/results/stationary_{a.graph}_q{a.q}.json","w") as f:
                        json.dump({"graph":a.graph,"q":a.q,"excess":0,"W":best[1],"A":best[2].tolist()},f,indent=2)
        print("restart done",restart,cur,flush=True)
    print("FINAL",best[:2]); print(best[2])
if __name__=="__main__":main()
