# Question: for feasible 3D bodies (barycenter 0, int cap Z^3 = {0}), does there always
# exist a primitive direction ell with  vol(K) <= (4/3)^3 * area(K cap ell^perp)
# AND area_lattice(K cap ell^perp) <= 9/2  (area measured w.r.t. the induced lattice Z^3 cap ell^perp)?
# This is the recursive scheme that is TIGHT at the sharp simplex (ell = e_1).
# Method: random feasible polytopes (rejection + shrink) + the sharp simplex + perturbations.
import numpy as np, itertools, sys
from math import gcd
from scipy.spatial import ConvexHull

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)

def hull(pts):
    try: return ConvexHull(pts)
    except Exception: return None

def barycenter_vol(pts):
    h = hull(pts)
    c = pts[h.vertices].mean(axis=0); tot = 0.0; cen = np.zeros(3)
    for s in h.simplices:
        tri = pts[s]; vol = abs(np.linalg.det(tri - c))/6.0
        cen += vol*(c + tri.sum(axis=0))/4.0; tot += vol
    return cen/tot, tot

def feasible(pts, tol=1e-9):
    # int(K) cap Z^3 subset {0}
    h = hull(pts); A = h.equations[:,:3]; b = h.equations[:,3]
    lo = np.floor(pts.min(0)).astype(int); hi = np.ceil(pts.max(0)).astype(int)
    for x in range(lo[0],hi[0]+1):
        for y in range(lo[1],hi[1]+1):
            for z in range(lo[2],hi[2]+1):
                if (x,y,z)==(0,0,0): continue
                if (A@np.array([x,y,z],float)+b).max() < -1e-7: return False
    return True

def primitive_dirs(maxc=3):
    out=[]
    for a in range(-maxc,maxc+1):
        for b in range(-maxc,maxc+1):
            for c in range(0,maxc+1):
                if (a,b,c)==(0,0,0): continue
                if c==0 and (b<0 or (b==0 and a<0)): continue
                if gcd(gcd(abs(a),abs(b)),abs(c))!=1: continue
                out.append((a,b,c))
    return out

DIRS = primitive_dirs(3)

def lattice_basis_perp(ell):
    """basis of Z^3 cap ell^perp (rank 2) via HNF-ish: solve ell.x=0 over Z."""
    a,b,c = ell
    # brute force two short independent integer vectors orthogonal to ell
    found=[]
    for x in range(-6,7):
        for y in range(-6,7):
            for z in range(-6,7):
                if (x,y,z)==(0,0,0): continue
                if a*x+b*y+c*z==0:
                    found.append((x,y,z))
    found.sort(key=lambda v: v[0]**2+v[1]**2+v[2]**2)
    B=[np.array(found[0],float)]
    for v in found[1:]:
        w=np.array(v,float)
        if np.linalg.norm(np.cross(B[0],w))>1e-9:
            B.append(w); break
    # make it a *basis* of the perp lattice: check index via |cross| = |ell| iff basis
    if abs(np.linalg.norm(np.cross(B[0],B[1])) - np.linalg.norm(np.array(ell,float))) > 1e-6:
        return None  # not unimodular basis; skip (rare with short vectors)
    return np.array(B)

PERP = {}
for ell in DIRS:
    Bp = lattice_basis_perp(ell)
    if Bp is not None: PERP[ell]=Bp

def section_area_lattice(pts, ell):
    """area of K cap ell^perp in lattice-normalized coords of Z^3 cap ell^perp."""
    if ell not in PERP: return None
    B = PERP[ell]  # rows: lattice basis of perp
    h = hull(pts); A = h.equations[:,:3]; bb = h.equations[:,3]
    # section in coords (s,t) -> point s*B0 + t*B1 ; constraints A(sB0+tB1) <= -bb
    A2 = np.stack([A@B[0], A@B[1]],axis=1); b2 = -bb
    verts=[]
    m=len(b2)
    for i in range(m):
        for j in range(i+1,m):
            M=np.array([A2[i],A2[j]])
            if abs(np.linalg.det(M))<1e-12: continue
            z=np.linalg.solve(M,np.array([b2[i],b2[j]]))
            if np.all(A2@z <= b2+1e-7): verts.append(z)
    if len(verts)<3: return 0.0
    verts=np.array(verts)
    try:
        h2=ConvexHull(verts); return h2.volume  # 2D volume = area, in lattice coords
    except Exception: return 0.0

def check(pts, name):
    bc, vol = barycenter_vol(pts); pts0 = pts - bc
    if not feasible(pts0):
        return None
    best = None
    for ell in DIRS:
        a = section_area_lattice(pts0, ell)
        if a is None or a <= 0: continue
        ratio = vol / a
        ok = (ratio <= (4/3)**3 + 1e-9) and (a <= 4.5 + 1e-9)
        cand = (0 if ok else 1, ratio, a, ell)
        if best is None or cand < best: best = cand
    status = "OK " if best and best[0]==0 else "FAIL"
    print(f"[{name}] vol={vol:.4f} {status} best: ratio={best[1]:.4f} (<= {(4/3)**3:.4f}?) "
          f"area={best[2]:.4f} (<=4.5?) ell={best[3]}", flush=True)
    return status=="OK "

if __name__ == "__main__":
    fails = 0; total = 0
    # sharp simplex + random unimodular images of it
    S = 4*np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1.]]) - 1.0
    check(S, "sharp simplex")
    # random feasible bodies: sample vertices, shrink until feasible
    for t in range(2000):
        V = rng.integers(4, 9)
        pts = rng.normal(scale=1.6, size=(V,3))
        bc,_ = barycenter_vol(pts) if hull(pts) is not None else (None,None)
        if bc is None: continue
        pts = pts - bc
        # grow until infeasible, then back off: scale search
        lo_s, hi_s = 0.1, 6.0
        for _ in range(40):
            mid = 0.5*(lo_s+hi_s)
            P = pts*mid; bc2,_ = barycenter_vol(P); P = P - bc2
            if feasible(P): lo_s = mid
            else: hi_s = mid
        P = pts*lo_s; bc2,_ = barycenter_vol(P); P = P - bc2
        if not feasible(P): continue
        _, vol = barycenter_vol(P)
        if vol < 4.0: continue  # only interesting when reasonably big
        total += 1
        ok = check(P, f"rand{t}")
        if ok is False: fails += 1
        if total >= 200: break
    print(f"DONE total={total} fails={fails}")
