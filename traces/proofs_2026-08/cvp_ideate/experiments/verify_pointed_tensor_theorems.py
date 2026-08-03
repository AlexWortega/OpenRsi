#!/usr/bin/env python3
"""Finite checks accompanying the pointed-sublattice/tensor theorems.

Checks on deterministic tiny 3DM incidence lattices:
  * odd mod-2 fiber distance q+3 (including homogenizing coordinate);
  * homogeneous mod-2 distance >=4;
  * every enumerated primitive-functional rank-2 sublattice obeys
        Gram determinant >=4(q+2), support >=q+5;
  * general odd-Pluecker lower count for enumerated rank-3 bases;
  * the explicit Z^2 primitive-functional all-partner counterexample.
The quantified theorems are proved in proof_cvp.md; this script certifies the
finite examples and exact arithmetic quoted there.
"""
from __future__ import annotations
import itertools,math
import verify_feature_shell_3dm as f
import verify_highrank_integer_tensor as ht
import verify_tensor_subdeterminants as sd


def mod2_words(B):
 seen=set()
 for c in itertools.product((0,1),repeat=len(B)):
  seen.add(tuple(sum(c[i]*B[i][j] for i in range(len(B)))&1 for j in range(len(B[0]))))
 return seen
def gramdet(vs):
 if len(vs)==2:return sd.det2(vs[0],vs[1])
 if len(vs)==3:
  a,b,c=vs
  aa,bb,cc=sd.dot(a,a),sd.dot(b,b),sd.dot(c,c)
  ab,ac,bc=sd.dot(a,b),sd.dot(a,c),sd.dot(b,c)
  return aa*bb*cc+2*ab*ac*bc-aa*bc*bc-bb*ac*ac-cc*ab*ab
 raise ValueError
def odd_maximal_minors(vs):
 r=len(vs);n=len(vs[0]);count=0
 for J in itertools.combinations(range(n),r):
  if r==2:
   d=vs[0][J[0]]*vs[1][J[1]]-vs[0][J[1]]*vs[1][J[0]]
  else:
   a=[[vs[i][j] for j in J] for i in range(3)]
   d=(a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
     -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
     +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))
  count+=abs(d)%2
 return count
def main():
 q=3;Q=q+2;records=[]
 for yes in [True,False]:
  fam=ht.sample(q,9,3,yes,10);assert len(fam)==10
  for T,B in fam:
   W=mod2_words(B)
   pointed=[sum(x) for x in W if x[-1]==1]
   kernel=[sum(x) for x in W if x[-1]==0 and any(x)]
   assert min(kernel)>=4
   assert min(pointed)==(q+1 if yes else q+3)
   C=sd.coeff_vectors(3);V={c:sd.vec(B,c) for c in C}
   checked2=0
   for i,c in enumerate(C):
    for d in C[i+1:]:
     if not sd.rank2(c,d):continue
     u,v=V[c],V[d]
     if math.gcd(abs(u[-1]),abs(v[-1]))!=1:continue
     checked2+=1
     if not yes:
      assert gramdet([u,v])>=4*Q
      assert sd.support([u,v])>=q+5
   # The whole saturated rank-3 lattice has primitive star functional.  Check
   # Cauchy--Binet and the theorem-4 odd-minor count.
   odd=odd_maximal_minors(B);det=gramdet(B)
   lower=math.ceil((q+3)*4**2/math.factorial(3))
   assert det>=odd>=lower
   records.append(('Y' if yes else 'N',min(pointed),min(kernel),checked2,odd,det))
 print({'records':records,'rank2_NO_bound':4*Q,'rank2_NO_support':q+5,
        'rank3_odd_minor_bound':math.ceil((q+3)*16/6)})
 # Universal pointed all-partner inequality counterexample.
 # s=tau=(2,5), X=[[-1,-1],[-1,1]].
 X=((-1,-1),(-1,1));a=(2,5)
 functional=sum(a[i]*X[i][j]*a[j] for i in range(2) for j in range(2))
 norm2=sum(x*x for row in X for x in row)
 base=min(x*x+y*y for x in range(-20,21) for y in range(-20,21) if 2*x+5*y==1)
 assert (functional,norm2,base)==(1,4,5)
 assert norm2<base*base
 print({'all_partner_counterexample':{'functional':functional,'tensor_norm2':norm2,
                                      'base_pointed_norm2':base,'claimed_product':base*base}})
 print('pointed tensor theorem finite checks pass')
if __name__=='__main__':main()
