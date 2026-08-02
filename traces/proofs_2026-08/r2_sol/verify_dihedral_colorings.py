#!/usr/bin/env python3
"""Verify explicit inverse-symmetric product-free partitions of dihedral groups."""
import itertools,json
for n,k,path in [(16,4,'experiments/dihedral_16_4.json'),(32,5,'experiments/dihedral_32_5.json'),(64,6,'experiments/dihedral_64_6.json'),(128,7,'experiments/dihedral_128_7.json'),(256,8,'experiments/dihedral_256_8.json'),(512,9,'experiments/dihedral_512_9.json')]:
 D=json.load(open(path));C=[{tuple(x) for x in S} for S in D['classes']];G=[(a,b) for a in range(n) for b in range(2)];e=(0,0);U=set(G)-{e}
 def mul(x,y):a,b=x;c,d=y;return ((a+(-1 if b else 1)*c)%n,(b+d)%2)
 def inv(x):a,b=x;return (((-1 if b==0 else 1)*a)%n,b)
 assert len(C)==k and set().union(*C)==U and sum(map(len,C))==len(U)
 assert all(all(inv(x) in S for x in S) for S in C)
 assert all(all(mul(x,y) not in S for x in S for y in S) for S in C)
 col={x:i for i,S in enumerate(C) for x in S}
 def edge(x,y):return col[mul(inv(x),y)]
 count=0
 for x,y,z in itertools.combinations(G,3):assert len({edge(x,y),edge(x,z),edge(y,z)})>1;count+=1
 print('verified dihedral order',2*n,'with',k,'colors:',count,'triangles; sizes',list(map(len,C)))
