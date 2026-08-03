#!/usr/bin/env python3
"""Verify exact completeness failures and the coboundary gauge identity for phase lifts."""
import itertools,random,sys
sys.path.insert(0,'experiments')
from phase_lift_ncp import sat_pair,sat_assignments,random_alpha,assignment_lifts
from connected_views import satisfies

def completeness_count(q,trials=30,seed=71):
 rng=random.Random(seed);C=sat_pair();sats=sat_assignments(C,3);good=0
 for _ in range(trials):
  a=random_alpha(C,q,rng)
  good+=any(assignment_lifts(b,C,q,a) is not None for b in sats)
 return len(sats),good
assert completeness_count(2)==(6,23)
assert completeness_count(3)==(6,14)

# Coboundary phases alpha[j,a,r]=beta[i,b]-gamma[j,a] are removed by
# y'=y-beta[i,b], z'=z-gamma[j,a]: y=z+alpha iff y'=z'.
rng=random.Random(83)
checks=0
for q in (2,3,5,7):
 C=sat_pair(); beta={(i,b):rng.randrange(q) for i in range(1,4) for b in (0,1)}
 for j,c in enumerate(C):
  views=[]
  scope=tuple(abs(x) for x in c)
  for a in itertools.product((0,1),repeat=3):
   if satisfies(c,dict(zip(scope,a))):views.append(a)
  for a in views:
   gamma=rng.randrange(q)
   alpha=tuple((beta[(abs(c[r]),a[r])]-gamma)%q for r in range(3))
   for z in range(q):
    y=tuple((z+alpha[r])%q for r in range(3))
    yp=tuple((y[r]-beta[(abs(c[r]),a[r])])%q for r in range(3))
    zp=(z-gamma)%q
    assert yp==(zp,zp,zp);checks+=1
print({'random_completeness':{2:'23/30',3:'14/30'},'coboundary_gauge_checks':checks})
