#!/usr/bin/env python3
"""Exact finite attack on Fable proposal 2: A4 convolution buckets.

Represent PSL_2(F_3) by A4 acting on four points.  Order its twelve permutation
tuples lexicographically, assign the first eight to the canonically sorted
triple coordinates, and choose the lexicographically first element of each of
the four conjugacy classes as probes.  For every ordered pair (i,j), block s
places W_ij in bucket lambda_i a_s lambda_j^{-1}.  The fold has 48 nominal
moving bits.

Every mixed image word is enumerated on ten YES, 200 NO, twenty affine-closure,
all-eight, and an eight-coordinate holonomy dictionary.  Explicit syndrome
fibers and exact-transfer ranks are reconstructed.  Finite evidence only.
"""
from __future__ import annotations
import itertools,json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"prior"/"experiments"))
import verify_asymmetric_hash_fold as base  # type: ignore


def compose(p,q):return tuple(p[q[i]] for i in range(4))
def inverse(p):
 out=[0]*4
 for i,v in enumerate(p):out[v]=i
 return tuple(out)
def parity(p):return sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))&1
A4=tuple(sorted(p for p in itertools.permutations(range(4)) if parity(p)==0))
IDENTITY=(0,1,2,3);assert len(A4)==12 and A4[0]==IDENTITY
INDEX={g:i for i,g in enumerate(A4)}

def conjugacy_class(g):return frozenset(compose(compose(h,g),inverse(h)) for h in A4)
CLASSES=sorted({conjugacy_class(g) for g in A4},key=lambda C:min(C))
PROBES=tuple(min(C) for C in CLASSES)
assert len(CLASSES)==4 and sorted(map(len,CLASSES))==[1,3,4,4]
LABELS=A4[:8]
NOMINAL=48


def incidence_fiber(q,T):
 T=sorted(T);cols=[base.syn(q,t) for t in T];target=(1<<(3*q))-1;F=[]
 for x in range(1<<len(T)):
  s=0
  for j,c in enumerate(cols):
   if x>>j&1:s^=c
  if s==target:F.append(x)
 return F

def pointed_code(q,T):
 T=sorted(T);cols=[base.syn(q,t) for t in T];target=(1<<(3*q))-1;K=[];F=[]
 for x in range(1<<len(T)):
  s=0
  for j,c in enumerate(cols):
   if x>>j&1:s^=c
  if s==0:K.append(x)
  if s==target:F.append(x)
 if not F:return None
 p=min(F,key=lambda x:(x.bit_count(),x))
 return base.basis([x<<1 for x in K]+[1|(p<<1)]),F

def rref(rows,n):
 rows=[x&((1<<n)-1) for x in rows if x];piv=[];rank=0
 for col in range(n):
  p=next((i for i in range(rank,len(rows)) if rows[i]>>col&1),None)
  if p is None:continue
  rows[rank],rows[p]=rows[p],rows[rank]
  for i in range(len(rows)):
   if i!=rank and rows[i]>>col&1:rows[i]^=rows[rank]
  piv.append(col);rank+=1
  if rank==len(rows):break
 return rows[:rank],piv

def nullspace(rows,n):
 E,piv=rref(rows,n);out=[]
 for f in (j for j in range(n) if j not in piv):
  x=1<<f
  for row,p in zip(E,piv):
   if (row&x).bit_count()&1:x|=1<<p
  out.append(x)
 assert all(not((h&r).bit_count()&1) for h in out for r in rows)
 return out

def explicit_fiber(image,n):
 p=next(r for r in image if r&1);K=[]
 for r in image:
  z=r^(p if r&1 else 0)
  if z:K.append(z>>1)
 K=base.basis(K);H=nullspace(K,n);t=sum((((h&(p>>1)).bit_count()&1)<<i) for i,h in enumerate(H))
 assert len(K)+len(H)==n
 for r in image:
  s=sum((((h&(r>>1)).bit_count()&1)<<i) for i,h in enumerate(H));assert s==(t if r&1 else 0)
 return H,t

def gray_min(rows):
 rows=base.basis(rows);x=0;best=None;bestword=None;total=1<<len(rows)
 for step in range(total):
  if x&1:
   w=(x>>1).bit_count()
   if best is None or w<best:best,bestword=w,x
  if step+1<total:x^=rows[((step+1)&-(step+1)).bit_length()-1]
 assert best is not None
 return best,bestword,total

def pair_buckets():
 out=[]
 for a in PROBES:
  block=[]
  for li in LABELS:
   row=[]
   for lj in LABELS:
    g=compose(compose(li,a),inverse(lj));row.append(INDEX[g])
   block.append(tuple(row))
  out.append(tuple(block))
 return tuple(out)
BUCKETS=pair_buckets()
assert len(BUCKETS)==4

def fold_matrix(row_masks):
 word=0
 for s in range(4):
  for i,row in enumerate(row_masks):
   while row:
    bit=row&-row;j=bit.bit_length()-1;word^=1<<(12*s+BUCKETS[s][i][j]);row^=bit
 return word

def prune(rows):
 rows=base.basis(rows);active=[j for j in range(NOMINAL) if any(r>>(1+j)&1 for r in rows)];out=[]
 for r in rows:
  y=r&1
  for k,j in enumerate(active):y|=((r>>(1+j))&1)<<(1+k)
  out.append(y)
 return base.basis(out),active

def report(q,T):
 T=sorted(T);assert len(T)==8;D=pointed_code(q,T);assert D is not None;rows,F=D;m=8;gens=[]
 for l in rows:
  rb=sum(((l>>(1+i))&1)<<i for i in range(m))
  for r in rows:
   cb=sum(((r>>(1+j))&1)<<j for j in range(m));matrix=[cb if rb>>i&1 else 0 for i in range(m)]
   gens.append(((l&1)&(r&1))|(fold_matrix(matrix)<<1))
 image,active=prune(gens);best,bestword,total=gray_min(image);H,target=explicit_fiber(image,len(active));amask=sum(1<<j for j in active)
 legal=[];illegal=[]
 for x in F:
  matrix=[x if x>>i&1 else 0 for i in range(8)];cost=(fold_matrix(matrix)&amask).bit_count();(legal if x.bit_count()==q else illegal).append(cost)
 d=min(x.bit_count() for x in F)
 return {"base_distance":d,"unfurled_square_distance":d*d,"source_square_dimension":len(base.reduced(rows,8)),"fiber_size":len(F),"image_dimension":len(image),"nominal_pointed_length":49,"active_pointed_length":1+len(active),"exact_transfer_rank":len(active),"parity_check_rank":len(H),"target":target,"folded_distance":best,"minimum_output_word":bestword,"pointed_kernel":best==0,"legal_pure_square_range":None if not legal else [min(legal),max(legal)],"cheapest_semantic_illegal_pure_square":min(illegal,default=None),"mixed_words_enumerated":total}

def families(n=200):
 Y=[base.planted(3,8,s) for s in range(10)];N=[]
 for s in range(10000,100000):
  T=base.randomT(3,8,s);F=incidence_fiber(3,T)
  if F and min(x.bit_count() for x in F)>3:
   assert min(x.bit_count() for x in F)==5;N.append(T)
   if len(N)==n:break
 return Y,N

def contains(rows,x):
 for r in sorted(base.basis(rows),key=int.bit_length,reverse=True):
  if x.bit_length()==r.bit_length():x^=r
 return x==0

def closure(n=20):
 out=[]
 for s in range(100000):
  T=base.randomT(3,8,s);F=incidence_fiber(3,T);M=[x for x in F if x.bit_count()==3]
  if not M:continue
  ref=M[0];R=[x^ref for x in M[1:]];bad=[x for x in F if x.bit_count()!=3 and contains(R,x^ref)]
  if bad:
   out.append((s,T,bad))
   if len(out)==n:break
 assert len(out)==n;return out

def all8():return 2,list(itertools.product(range(2),repeat=3))
def hol8():
 q=3;M=[[(0,0,0),(1,1,1),(2,2,2)],[(0,0,0),(1,1,2),(2,2,1)],[(0,0,1),(1,2,0),(2,1,2)]];T=sorted(set().union(*map(set,M)));assert len(T)==8
 bad=set(M[0])^set(M[1])^set(M[2]);mask=sum(1<<T.index(t) for t in bad);assert mask in incidence_fiber(q,T) and mask.bit_count()==7
 return q,T

def relabel_check(T,exhaustive):
 canonical=sorted(T);perms=itertools.permutations(range(8)) if exhaustive else [tuple(reversed(range(8)))];n=0
 for p in perms:assert sorted(T[i] for i in p)==canonical;n+=1
 return n

def compact(r):return {k:r[k] for k in ("base_distance","unfurled_square_distance","source_square_dimension","fiber_size","image_dimension","nominal_pointed_length","active_pointed_length","exact_transfer_rank","parity_check_rank","folded_distance","pointed_kernel","legal_pure_square_range","cheapest_semantic_illegal_pure_square","mixed_words_enumerated")}

def all_eight_label_permutation_attack(T):
 """Test the corner-kernel condition for every assignment of the eight labels."""
 rows,_=pointed_code(2,T);generator_specs=[]
 for l in rows:
  for r in rows:
   pairs=[(i,j) for i in range(8) if l>>(1+i)&1 for j in range(8) if r>>(1+j)&1]
   generator_specs.append(((l&1)&(r&1),pairs))
 kernels=0;tested=0
 for permutation in itertools.permutations(range(8)):
  pair_words=[[0]*8 for _ in range(8)]
  for i in range(8):
   for j in range(8):
    word=0
    for s in range(4):word^=1<<(12*s+BUCKETS[s][permutation[i]][permutation[j]])
    pair_words[i][j]=word
  generators=[]
  for corner,pairs in generator_specs:
   moving=0
   for i,j in pairs:moving^=pair_words[i][j]
   generators.append(corner|(moving<<1))
  image=base.basis(generators);p=next(r for r in image if r&1);K=[]
  for r in image:
   z=r^(p if r&1 else 0)
   if z:K.append(z>>1)
  if contains(K,p>>1):kernels+=1
  tested+=1
 assert tested==math.factorial(8)
 return tested,kernels

def main():
 Y,N=families();C=closure();q8,E=all8();qh,H=hol8();YR=[report(3,t) for t in Y];NR=[report(3,t) for t in N];CR=[(s,report(3,t),bad) for s,t,bad in C];ER=report(q8,E);HR=report(qh,H)
 worst=max(r["folded_distance"] for r in YR);best=min(r["folded_distance"] for r in NR);rank=max(r["exact_transfer_rank"] for r in YR+NR);ratio=best/worst if worst else 0;exponent=math.log(ratio)/math.log(rank) if ratio>1 and rank>1 else 0;baseline=math.log(25/9)/math.log(65)
 hostile=[r["cheapest_semantic_illegal_pure_square"] for _,r,_ in CR]+[ER["cheapest_semantic_illegal_pure_square"],HR["cheapest_semantic_illegal_pure_square"]];bases=[r["legal_pure_square_range"][1] for _,r,_ in CR]+[ER["legal_pure_square_range"][1],HR["legal_pure_square_range"][1]]
 label_permutations,label_kernels=all_eight_label_permutation_attack(E)
 checks=0
 for T in Y+N[:10]+[x[1] for x in C]+[E,H]:checks+=relabel_check(T,True)
 for T in N[10:]:checks+=relabel_check(T,False)
 assert checks==42*math.factorial(8)+190
 R=YR+NR+[ER,HR]+[r for _,r,_ in CR];success=not any(r["pointed_kernel"] for r in R) and best>worst and exponent>baseline and all(c>b for c,b in zip(hostile,bases))
 summary={"mechanism":"A4 convolution buckets lambda_i a_s lambda_j^-1 with one probe per conjugacy class","expected_move":"quasirandom product mixing spreads NO mixed matrices while structured YES squares remain concentrated","falsification":"pointed kernel, NO not above worst YES, hostile illegal cost not above legal baseline, or exponent not above baseline","group":{"model":"A4 isomorphic to PSL2(F3)","ordered_elements":[list(g) for g in A4],"conjugacy_class_sizes":[len(c) for c in CLASSES],"probes":[list(g) for g in PROBES],"labels":[list(g) for g in LABELS]},"instances":{"YES_q3_m8":10,"NO_q3_m8":200,"affine_closure_q3_m8":20,"all_eight_q2_m8":1,"holonomy_q3_m8":1},"unfurled":{"worst_YES":9,"best_NO":25,"exact_transfer_rank":64,"rank_exponent":baseline},"folded":{"worst_YES":worst,"best_NO":best,"uniform_ratio":ratio,"max_exact_transfer_rank":rank,"rank_exponent":exponent,"YES_distance_range":[min(r["folded_distance"] for r in YR),worst],"NO_distance_range":[best,max(r["folded_distance"] for r in NR)],"YES_pointed_kernels":sum(r["pointed_kernel"] for r in YR),"NO_pointed_kernels":sum(r["pointed_kernel"] for r in NR)},"all_eight":compact(ER),"holonomy":compact(HR),"affine_closure":{"seeds":[s for s,_,_ in CR],"distance_range":[min(r["folded_distance"] for _,r,_ in CR),max(r["folded_distance"] for _,r,_ in CR)],"semantic_illegal_cost_range":[min(r["cheapest_semantic_illegal_pure_square"] for _,r,_ in CR),max(r["cheapest_semantic_illegal_pure_square"] for _,r,_ in CR)],"legal_baseline_range":[min(r["legal_pure_square_range"][1] for _,r,_ in CR),max(r["legal_pure_square_range"][1] for _,r,_ in CR)],"pointed_kernels":sum(r["pointed_kernel"] for _,r,_ in CR)},"mixed_words_enumerated":sum(r["mixed_words_enumerated"] for r in R),"coordinate_relabelings_checked":checks,"all_eight_label_permutations_tested":label_permutations,"all_eight_label_permutation_kernels":label_kernels,"primary_success":success}
 print(json.dumps(summary,indent=2,sort_keys=True))
 assert (worst,best,rank)==(20,10,48)
 assert [min(r["folded_distance"] for r in YR),worst]==[12,20]
 assert [best,max(r["folded_distance"] for r in NR)]==[10,22]
 assert not any(r["pointed_kernel"] for r in YR+NR)
 assert ER["folded_distance"]==0 and ER["pointed_kernel"]
 assert HR["cheapest_semantic_illegal_pure_square"]==22<HR["legal_pure_square_range"][1]
 assert label_kernels>0
 assert not success
 print("A4_CONVOLUTION_FOLD_PASS")
if __name__=="__main__":main()
