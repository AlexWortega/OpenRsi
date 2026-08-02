#!/usr/bin/env python3
"""Discriminating q=2 test for the oracle's GQ-Tanner rigidity proposal.

Builds GQ(2,2) as edges/perfect matchings of K6, finds a polarity, and checks
whether a doily collineation outside the polarity centralizer moves every point
to a nonneighbor in the polarity graph. Such a map would falsify rigidity for
every equitable Tanner configuration, without solving the Tanner CSP.
"""
from itertools import combinations, permutations
import networkx as nx

V=range(6)
points=list(combinations(V,2)); pidx={p:i for i,p in enumerate(points)}
def matchings(xs):
    xs=tuple(xs)
    if not xs: yield (); return
    a=xs[0]
    for j in range(1,len(xs)):
        b=xs[j]
        for rest in matchings(xs[1:j]+xs[j+1:]):
            yield tuple(sorted(((min(a,b),max(a,b)),)+rest))
lines=sorted(set(matchings(tuple(V)))); lidx={L:i for i,L in enumerate(lines)}
assert len(points)==len(lines)==15
# incidence graph and a side-swapping automorphism = polarity candidate
B=nx.Graph()
B.add_nodes_from([('p',i) for i in range(15)],bipartite=0)
B.add_nodes_from([('l',j) for j in range(15)],bipartite=1)
for i,p in enumerate(points):
    for j,L in enumerate(lines):
        if p in L:B.add_edge(('p',i),('l',j))
GM=nx.algorithms.isomorphism.GraphMatcher(B,B,node_match=lambda a,b:a['bipartite']!=b['bipartite'])
# node_match does not work this way for self matcher; explicitly map to side-swapped copy
C=nx.Graph()
for typ,i,d in [(u[0],u[1],d) for u,d in B.nodes(data=True)]: C.add_node((typ,i),bipartite=1-d['bipartite'])
C.add_edges_from(B.edges())
iso=next(nx.algorithms.isomorphism.GraphMatcher(B,C,node_match=lambda a,b:a['bipartite']==b['bipartite']).isomorphisms_iter())
# iso maps B node to C node labels; because labels retained but colors swapped, p images must be l
pi=[None]*15; inv=[None]*15
for i in range(15):
    image=iso[('p',i)]
    assert image[0]=='l'
    pi[i]=image[1]
for j in range(15):
    image=iso[('l',j)]
    assert image[0]=='p'
    inv[j]=image[1]
# Need involutory polarity, not arbitrary duality. Search all dualities until inverse maps agree.
if any(inv[pi[i]]!=i for i in range(15)):
    found=False
    for iso in nx.algorithms.isomorphism.GraphMatcher(B,C,node_match=lambda a,b:a['bipartite']==b['bipartite']).isomorphisms_iter():
        pp=[iso[('p',i)][1] for i in range(15)]
        ii=[iso[('l',j)][1] for j in range(15)]
        if all(ii[pp[i]]==i for i in range(15)):
            pi,inv,found=pp,ii,True;break
    assert found
# polarity graph
adj=[[False]*15 for _ in range(15)]
for i,p in enumerate(points):
    for j in range(15):
        if i!=j and p in lines[pi[j]]: adj[i][j]=True
assert all(adj[i][j]==adj[j][i] for i in range(15) for j in range(15))
assert not any(adj[i][j] and adj[j][k] and adj[k][i] for i in range(15) for j in range(i+1,15) for k in range(j+1,15))

def point_perm(s):
    return [pidx[tuple(sorted((s[a],s[b])))] for a,b in points]
def line_image(j,s):
    return lidx[tuple(sorted(tuple(sorted((s[a],s[b]))) for a,b in lines[j]))]

central=[]; killers=[]
for s in permutations(V):
    pp=point_perm(s); ll=[line_image(j,s) for j in range(15)]
    preserves=all(ll[pi[i]]==pi[pp[i]] for i in range(15))
    if preserves: central.append(s)
    if all(not adj[i][pp[i]] for i in range(15)) and not preserves:
        killers.append(s)
print('polarity_edges',sum(map(sum,adj))//2,'centralizer',len(central),'outside_nonadjacent_maps',len(killers))
assert len(killers)==30
print('COUNTEREXAMPLE_PERM',killers[0])
print('PASS: exactly 30 non-polarity doily collineations move every point to a polarity nonneighbor')
