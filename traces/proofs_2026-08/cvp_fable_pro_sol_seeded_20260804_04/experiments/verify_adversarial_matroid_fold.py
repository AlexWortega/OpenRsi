#!/usr/bin/env python3
"""Bounded exact feasibility test for Fable proposal 5.

For each canonical reduced 8x8 tensor code of dimension d, the row universe is
all 2^d-1 distinct nonzero linear functionals on the code.  Integer variables
choose row multiplicities with total output length at most 64.  Constraints,
derived only from the generator, require every pointed word to be hit, cap all
pointed rank-one tensors by Y, and lower-bound every non-rank-one pointed mixed
word by B.  A deterministic hierarchical integer objective maximizes B-Y,
then B, minimizes length, and finally a fixed weighted row order.

The resulting binary image is enumerated exactly and converted to a syndrome
fiber.  The complete all-eight code is also diagnosed: its d=25 universe and
pointed constraint set are explicitly counted before solver construction.  A
positive tiny solve is not a polynomial-time reduction; runtime/size are part
of the falsification test.
"""
from __future__ import annotations
import itertools,json,math,sys,time
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csr_matrix, vstack
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"prior"/"experiments"))
import verify_asymmetric_hash_fold as base  # type: ignore

BUDGET=64
# Exact row universes have 2^d-1 variables and 2^(d-1) pointed constraints.
# The bounded experiment solves d<=4 and records larger instances as the
# proposal's explicit separation-oracle/size failure rather than approximating.
MAX_EXACT_DIMENSION=4


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
 p=min(F,key=lambda x:(x.bit_count(),x));return base.basis([x<<1 for x in K]+[1|(p<<1)]),F

def square_word(left,right):
 moving=0
 for i in range(8):
  if not(left>>(1+i)&1):continue
  for j in range(8):
   if right>>(1+j)&1:moving|=1<<(8*i+j)
 return ((left&1)&(right&1))|(moving<<1)

def message_dictionary(rows):
 out={}
 for mask in range(1<<len(rows)):
  word=0
  for i,r in enumerate(rows):
   if mask>>i&1:word^=r
  out[word]=mask
 assert len(out)==1<<len(rows);return out

def rankone_messages(base_rows,square_rows):
 lookup=message_dictionary(square_rows);pointed=[w for w in base.words(base_rows) if w&1];out=set()
 for x in pointed:
  for y in pointed:out.add(lookup[square_word(x,y)])
 return frozenset(out)

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
 E,piv=rref(rows,n);ans=[]
 for f in (j for j in range(n) if j not in piv):
  x=1<<f
  for row,p in zip(E,piv):
   if (row&x).bit_count()&1:x|=1<<p
  ans.append(x)
 return ans

def explicit_fiber(image,n):
 p=next(r for r in image if r&1);K=[]
 for r in image:
  z=r^(p if r&1 else 0)
  if z:K.append(z>>1)
 K=base.basis(K);H=nullspace(K,n);target=sum((((h&(p>>1)).bit_count()&1)<<i) for i,h in enumerate(H))
 assert len(K)+len(H)==n
 return H,target

def solve_pattern(d,star,rankone):
 pointed=[c for c in range(1<<d) if (c&star).bit_count()&1]
 nonrank=[c for c in pointed if c not in rankone]
 types=list(range(1,1<<d));T=len(types);nv=T+2;iy,ib=T,T+1
 rows=[];lower=[];upper=[]
 # Total output length at most 64.
 rows.append({i:1 for i in range(T)});lower.append(-np.inf);upper.append(BUDGET)
 def support(c):return [i for i,t in enumerate(types) if (t&c).bit_count()&1]
 for c in pointed:
  rows.append({i:1 for i in support(c)});lower.append(1);upper.append(np.inf)
 for c in rankone:
  row={i:1 for i in support(c)};row[iy]=-1;rows.append(row);lower.append(-np.inf);upper.append(0)
 for c in nonrank:
  row={i:-1 for i in support(c)};row[ib]=1;rows.append(row);lower.append(-np.inf);upper.append(0)
 rr=[];cc=[];dd=[]
 for r,row in enumerate(rows):
  for c,value in row.items():rr.append(r);cc.append(c);dd.append(value)
 A=csr_matrix((dd,(rr,cc)),shape=(len(rows),nv),dtype=float);lb=np.array(lower);ub=np.array(upper)
 bounds=Bounds(np.zeros(nv),np.full(nv,BUDGET));integrality=np.ones(nv)
 start=time.monotonic()
 def run(c,A0=A,lo=lb,hi=ub):
  result=milp(c=np.asarray(c,dtype=float),integrality=integrality,bounds=bounds,constraints=LinearConstraint(A0,lo,hi),options={"time_limit":60,"mip_rel_gap":0.0})
  assert result.success,result.message
  return np.rint(result.x).astype(int)
 # Exact integer hierarchy: maximize B-Y, then B, minimize length, then
 # minimize a fixed weighted row order.
 c=np.zeros(nv);c[iy]=1;c[ib]=-1;x=run(c);margin=int(x[ib]-x[iy])
 eq=np.zeros((1,nv));eq[0,ib]=1;eq[0,iy]=-1;A1=vstack([A,csr_matrix(eq)]);lo1=np.r_[lb,margin];hi1=np.r_[ub,margin]
 c=np.zeros(nv);c[ib]=-1;x=run(c,A1,lo1,hi1);bv=int(x[ib]);yv=int(x[iy])
 eq2=np.zeros((2,nv));eq2[0,ib]=1;eq2[1,iy]=1;A2=vstack([A1,csr_matrix(eq2)]);lo2=np.r_[lo1,bv,yv];hi2=np.r_[hi1,bv,yv]
 c=np.zeros(nv);c[:T]=1;x=run(c,A2,lo2,hi2);length=int(x[:T].sum())
 eq3=np.zeros((1,nv));eq3[0,:T]=1;A3=vstack([A2,csr_matrix(eq3)]);lo3=np.r_[lo2,length];hi3=np.r_[hi2,length]
 c=np.zeros(nv);c[:T]=np.arange(1,T+1);x=run(c,A3,lo3,hi3)
 elapsed=time.monotonic()-start;mult=tuple(map(int,x[:T]));assert sum(mult)==length
 costs={c0:sum(mult[i] for i in support(c0)) for c0 in pointed}
 assert min(costs.values())>=1 and max(costs[c0] for c0 in rankone)<=yv
 if nonrank:assert min(costs[c0] for c0 in nonrank)>=bv
 return {"multiplicities":mult,"Y":yv,"B":bv,"length":length,"solve_seconds":elapsed,"pointed_constraints":len(pointed),"rankone_constraints":len(rankone),"nonrank_constraints":len(nonrank),"row_universe":T,"actual_rankone_max":max(costs[c0] for c0 in rankone),"actual_nonrank_min":min((costs[c0] for c0 in nonrank),default=None)}

CACHE={}
def code_report(q,T,solve=True):
 T=sorted(T);D=pointed_code(q,T);assert D is not None;base_rows,F=D;square=base.reduced(base_rows,8);d=len(square);star=sum((r&1)<<i for i,r in enumerate(square));rankone=rankone_messages(base_rows,square)
 pointed_count=1<<(d-1);universe=(1<<d)-1
 if not solve or d>MAX_EXACT_DIMENSION:
  return {"solved":False,"code_dimension":d,"row_universe":universe,"pointed_constraints":pointed_count,"rankone_constraints":len(rankone),"reason":"exact ILP exceeds precommitted dimension cap","unfurled_square_distance":min(x.bit_count() for x in F)**2}
 key=(d,star,tuple(sorted(rankone)))
 if key not in CACHE:CACHE[key]=solve_pattern(d,star,rankone)
 sol=CACHE[key];types=list(range(1,1<<d));coordinates=[]
 for i,t in enumerate(types):coordinates.extend([t]*sol["multiplicities"][i])
 image=[]
 for i,r in enumerate(square):
  word=r&1
  for j,t in enumerate(coordinates):word|=((t>>i)&1)<<(1+j)
  image.append(word)
 image=base.basis(image);spectrum=sorted((w>>1).bit_count() for w in base.words(image) if w&1);assert spectrum
 H,target=explicit_fiber(image,len(coordinates))
 lookup=message_dictionary(square);illegal=[];legal=[]
 for x in F:
  c=lookup[square_word(1|(x<<1),1|(x<<1))];cost=sum(1 for t in coordinates if (t&c).bit_count()&1);(legal if x.bit_count()==q else illegal).append(cost)
 return {"solved":True,"code_dimension":d,"row_universe":universe,"pointed_constraints":pointed_count,"rankone_constraints":len(rankone),"selected_distinct_rows":sum(v>0 for v in sol["multiplicities"]),"output_length":len(coordinates),"exact_transfer_rank":len(coordinates),"parity_check_rank":len(H),"target":target,"folded_distance":spectrum[0],"folded_max":spectrum[-1],"pointed_kernel":spectrum[0]==0,"legal_pure_square_range":None if not legal else [min(legal),max(legal)],"cheapest_semantic_illegal_pure_square":min(illegal,default=None),"objective_margin":sol["B"]-sol["Y"],"B":sol["B"],"Y":sol["Y"],"actual_rankone_max":sol["actual_rankone_max"],"actual_nonrank_min":sol["actual_nonrank_min"],"solve_seconds":sol["solve_seconds"],"mixed_words_enumerated":1<<len(image),"unfurled_square_distance":min(x.bit_count() for x in F)**2}

def families(n=200):
 Y=[base.planted(3,8,s) for s in range(10)];N=[]
 for s in range(10000,100000):
  T=base.randomT(3,8,s);F=incidence_fiber(3,T)
  if F and min(x.bit_count() for x in F)>3:N.append(T)
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
  if bad:out.append((s,T,bad))
  if len(out)==n:break
 return out

def all8():return 2,list(itertools.product(range(2),repeat=3))
def hol8():
 M=[[(0,0,0),(1,1,1),(2,2,2)],[(0,0,0),(1,1,2),(2,2,1)],[(0,0,1),(1,2,0),(2,1,2)]];T=sorted(set().union(*map(set,M)));return 3,T

def compact(r):return r

def main():
 Y,N=families();C=closure();q8,E=all8();qh,J=hol8();YR=[code_report(3,t) for t in Y];NR=[code_report(3,t) for t in N];CR=[(s,code_report(3,t),bad) for s,t,bad in C];ER=code_report(q8,E,solve=False);HR=code_report(qh,J)
 solved_Y=[r for r in YR if r["solved"]];unsolved_Y=[r for r in YR if not r["solved"]];solved_N=[r for r in NR if r["solved"]];unsolved_N=[r for r in NR if not r["solved"]];solved_closure=[(s,r,b) for s,r,b in CR if r["solved"]];unsolved_closure=[(s,r,b) for s,r,b in CR if not r["solved"]];solved=solved_Y+solved_N+[r for _,r,_ in solved_closure]
 worst=max(r["folded_distance"] for r in solved_Y);best=min(r["folded_distance"] for r in solved_N);maxrank=max(r["exact_transfer_rank"] for r in solved_Y+solved_N);ratio=best/worst if worst else 0;exp=math.log(ratio)/math.log(maxrank) if ratio>1 and maxrank>1 else 0;baseexp=math.log(25/9)/math.log(65)
 success=not (unsolved_Y or unsolved_N or unsolved_closure) and ER["solved"] and HR["solved"] and not any(r["pointed_kernel"] for r in solved) and ratio>25/9 and maxrank<65 and exp>baseexp
 summary={"mechanism":"exact integer row-multiplicity ILP over every nonzero code functional","objective":"maximize nonrank minimum minus rank-one maximum, then nonrank minimum, minimize length, fixed weighted row order","budget":BUDGET,"exact_dimension_cap":MAX_EXACT_DIMENSION,"instances":{"YES":10,"NO":200,"affine_closure":20,"all_eight":1,"holonomy":1},"unfurled":{"worst_YES":9,"best_NO":25,"rank":64,"exponent":baseexp},"folded_solved_subset":{"solved_YES":len(solved_Y),"unsolved_YES":len(unsolved_Y),"solved_NO":len(solved_N),"unsolved_NO":len(unsolved_N),"unsolved_YES_dimensions":[r["code_dimension"] for r in unsolved_Y],"unsolved_NO_dimensions":[r["code_dimension"] for r in unsolved_N],"worst_YES":worst,"best_NO":best,"uniform_ratio":ratio,"max_rank":maxrank,"exponent":exp,"YES_range":[min(r["folded_distance"] for r in solved_Y),worst],"NO_range":[best,max(r["folded_distance"] for r in solved_N)],"output_length_range":[min(r["output_length"] for r in solved_Y+solved_N),max(r["output_length"] for r in solved_Y+solved_N)],"objective_margin_range":[min(r["objective_margin"] for r in solved_Y+solved_N),max(r["objective_margin"] for r in solved_Y+solved_N)],"pointed_kernels":sum(r["pointed_kernel"] for r in solved)},"all_eight":ER,"holonomy":HR,"affine_closure":{"seeds":[s for s,_,_ in CR],"solved":len(solved_closure),"unsolved":len(unsolved_closure),"unsolved_dimensions":[r["code_dimension"] for _,r,_ in unsolved_closure],"distance_range":None if not solved_closure else [min(r["folded_distance"] for _,r,_ in solved_closure),max(r["folded_distance"] for _,r,_ in solved_closure)],"pointed_kernels":sum(r["pointed_kernel"] for _,r,_ in solved_closure)},"unique_ILPs":len(CACHE),"total_solver_seconds":sum(x["solve_seconds"] for x in CACHE.values()),"mixed_words_enumerated":sum(r["mixed_words_enumerated"] for r in solved),"primary_success":success}
 print(json.dumps(summary,indent=2,sort_keys=True))
 assert (len(solved_Y),len(unsolved_Y),len(solved_N),len(unsolved_N))==(9,1,195,5)
 assert (worst,best,maxrank)==(16,16,64)
 assert all(r["folded_distance"]==16 and r["output_length"]==64 for r in solved_Y+solved_N)
 assert not any(r["pointed_kernel"] for r in solved)
 assert ER["code_dimension"]==25 and ER["row_universe"]==33554431 and ER["pointed_constraints"]==16777216
 assert not success
 print("ADVERSARIAL_MATROID_FOLD_PASS")
if __name__=="__main__":main()
