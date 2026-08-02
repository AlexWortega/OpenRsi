#!/usr/bin/env python3
"""Exact maximum pairwise-separated partial H-assignments for small cases.

Objects are r-subsets of [m] labeled by V(H). Two objects are compatible when
some shared coordinate receives adjacent labels. The compatibility graph clique
is the proposed triangle-free coloring's vertex family.
"""
import argparse,itertools,json,networkx as nx,os,time

def solve(m,r,hname):
    H=nx.cycle_graph(5) if hname=='c5' else nx.path_graph(2)
    objects=[]
    for B in itertools.combinations(range(m),r):
        for vals in itertools.product(H.nodes(),repeat=r): objects.append(tuple(zip(B,vals)))
    maps=[dict(o) for o in objects]; G=nx.Graph();G.add_nodes_from(range(len(objects)))
    for i in range(len(objects)):
        a=maps[i]
        for j in range(i):
            b=maps[j]
            if any(H.has_edge(a[x],b[x]) for x in a.keys()&b.keys()):G.add_edge(i,j)
    clique=max(nx.find_cliques(G),key=len)
    # independent direct compatibility validation
    for i,j in itertools.combinations(clique,2):
        assert any(H.has_edge(maps[i][x],maps[j][x]) for x in maps[i].keys()&maps[j].keys())
    return {'m':m,'r':r,'H':hname,'objects':len(objects),'max':len(clique),
            'family':[objects[i] for i in clique]}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('m',type=int);p.add_argument('r',type=int);p.add_argument('--H',default='c5',choices=['c5','k2']);a=p.parse_args();t=time.time();d=solve(a.m,a.r,a.H);d['seconds']=time.time()-t
 os.makedirs('experiments/results',exist_ok=True);fn=f'experiments/results/partial_{a.H}_m{a.m}_r{a.r}.json';json.dump(d,open(fn,'w'),indent=2);print({k:v for k,v in d.items() if k!='family'});print(fn)
