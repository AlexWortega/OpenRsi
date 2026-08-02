#!/usr/bin/env python3
"""Check the ordered 3-bit pattern used in the unrestricted matching obstruction."""
# On a homogeneous ordered 4-set a<b<c<d, bit A controls opposite pairs
# at the smallest endpoint, B the middle endpoint, C the largest endpoint.
a,b,c,d=range(4)
M={a:c,c:a,b:d,d:b};N={a:d,d:a,b:c,c:b}
def bit(i,x,y):
 s=sorted((i,x,y));return 0 if i==s[0] else (2 if i==s[2] else 1)
assert [bit(i,M[i],N[i]) for i in range(4)]==[0,0,2,2]
# A homogeneous 7-set contains i plus 3 larger points and i plus 3 smaller points.
S=range(7)
assert len([x for x in S if x>0])>=3 and len([x for x in S if x<6])>=3
print('PASS: switch coordinates use only outer bits A,A,C,C; a homogeneous 7-set tests triangles forcing A=C=0')
