#!/usr/bin/env python3
"""Implement the characteristic-3 exact-one syndrome candidate and attack it exactly."""
from __future__ import annotations
import argparse, itertools
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix, hstack

# Literals are signed variable IDs, 1-based. Exact-one literals use the same form.

def preprocess(clauses, n):
    constraints = []
    next_var = n + 1
    for clause in clauses:
        assert len(clause) == 3
        selectors = tuple(range(next_var, next_var + 3)); next_var += 3
        aux = tuple(range(next_var, next_var + 3)); next_var += 3
        constraints.append(selectors)
        for j, lit in enumerate(clause):
            constraints.append((selectors[j], -lit, aux[j]))
    return next_var - 1, constraints


def matrix(clauses, n):
    N, constraints = preprocess(clauses, n)
    rows=[]; cols=[]; data=[]; target=[]
    def add(r,c,v=1): rows.append(r); cols.append(c); data.append(v % 3)
    # coordinate 2*(u-1)+b represents variable u taking Boolean value b.
    for u in range(1, N+1):
        r=len(target); target.append(1); add(r,2*(u-1)); add(r,2*(u-1)+1)
    for cons in constraints:
        r=len(target); target.append(1)
        for lit in cons:
            u=abs(lit); b=1 if lit>0 else 0
            add(r,2*(u-1)+b)
    return coo_matrix((data,(rows,cols)),shape=(len(target),2*N),dtype=np.int8), np.array(target,dtype=np.int8), N, constraints


def min_weight_mod3(H,t,time_limit=120):
    """MILP: Hx-3z=t, x in {0,1,2}, minimize nonzero coordinates."""
    H=H.tocsr().astype(float); r,p=H.shape
    # x_j <= 2 y_j and x_j >= y_j, y binary. z integer, bounded safely.
    Aeq=hstack([H, coo_matrix((r,p)), -3*coo_matrix(np.eye(r))],format='csr')
    maxrow=np.asarray(H.sum(axis=1)).ravel()
    c=np.r_[np.zeros(p),np.ones(p),np.zeros(r)]
    lb=np.zeros(2*p+r); ub=np.r_[2*np.ones(p),np.ones(p),np.ceil(2*maxrow/3)+1]
    # inequalities x-2y<=0 and -x+y<=0
    I=coo_matrix(np.eye(p)); Z=coo_matrix((p,r))
    A1=hstack([I,-2*I,Z],format='csr'); A2=hstack([-I,I,Z],format='csr')
    constraints=[LinearConstraint(Aeq,t,t),LinearConstraint(A1,-np.inf,0),LinearConstraint(A2,-np.inf,0)]
    res=milp(c,integrality=np.ones(2*p+r),bounds=Bounds(lb,ub),constraints=constraints,
             options={'time_limit':time_limit})
    x=None if res.x is None else np.rint(res.x[:p]).astype(int)%3
    return res,x


def all8():
    return [tuple((i+1) if bit==0 else -(i+1) for i,bit in enumerate(u))
            for u in itertools.product((0,1),repeat=3)]


def construction_a_basis(H):
    """Integer basis for {z: Hz=0 mod 3}, after modular RREF and column permutation."""
    A=(H.toarray().astype(int)%3); rows,cols=A.shape
    pivot_cols=[]; rr=0
    for c in range(cols):
        piv=next((i for i in range(rr,rows) if A[i,c]%3),None)
        if piv is None: continue
        A[[rr,piv]]=A[[piv,rr]]
        A[rr]=(A[rr]*pow(int(A[rr,c]),-1,3))%3
        for i in range(rows):
            if i!=rr and A[i,c]: A[i]=(A[i]-A[i,c]*A[rr])%3
        pivot_cols.append(c); rr+=1
        if rr==rows: break
    free=[c for c in range(cols) if c not in pivot_cols]; perm=pivot_cols+free; s=len(pivot_cols)
    R=A[:s][:,perm]; assert np.array_equal(R[:,:s],np.eye(s,dtype=int))
    # Columns in permuted ambient coordinates: [3I, -A; 0,I].
    Bp=np.block([[3*np.eye(s,dtype=int), -R[:,s:]],
                 [np.zeros((cols-s,s),dtype=int),np.eye(cols-s,dtype=int)]])
    B=np.zeros_like(Bp)
    B[perm,:]=Bp
    assert np.all((H.toarray().dot(B)%3)==0)
    return B


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--time',type=float,default=120); a=ap.parse_args()
    H,t,N,_=matrix(all8(),3); res,x=min_weight_mod3(H,t,a.time)
    assert x is not None and np.array_equal(H.dot(x)%3,t)
    B=construction_a_basis(H)
    print({'N':N,'H_shape':H.shape,'status':res.status,'optimum':round(res.fun),
           'expected':N+1,'lattice_rank':B.shape[1],'basis_max_abs':int(abs(B).max())})

if __name__=='__main__': main()
