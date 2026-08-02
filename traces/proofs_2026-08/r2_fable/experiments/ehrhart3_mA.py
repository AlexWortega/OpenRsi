# Question: over feasible 3D bodies (barycenter 0, int cap Z^3 = {0}), is
#   min over primitive ell of  m_ell * A_ell  <=  9/2 ,
# where m_ell = min(max ell.x, -min ell.x) (near-side reach) and A_ell = lattice area of
# the zero section K cap ell^perp?  Combined with Lemma A' (vol <= (64/27) m A) this gives
# vol <= 32/3. Equality at the sharp simplex (m=1, A=9/2, ell=e_3).
# Adversarial: maximize min_ell (m_ell A_ell)/4.5 over feasible bodies.
import numpy as np, sys
from math import gcd
from scipy.spatial import ConvexHull
from scipy.optimize import minimize

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 0)
V = int(sys.argv[2]) if len(sys.argv)>2 else 6

def hull(pts):
    try: return ConvexHull(pts)
    except Exception: return None

def barycenter_vol(pts):
    h = hull(pts)
    if h is None: return None, None
    c = pts[h.vertices].mean(axis=0); tot=0.0; cen=np.zeros(3)
    for s in h.simplices:
        tri = pts[s]; vol = abs(np.linalg.det(tri-c))/6.0
        cen += vol*(c+tri.sum(0))/4.0; tot += vol
    if tot <= 1e-9: return None, None
    return cen/tot, tot

def interior_pen(pts):
    h = hull(pts); A=h.equations[:,:3]; b=h.equations[:,3]
    lo=np.floor(pts.min(0)).astype(int); hi=np.ceil(pts.max(0)).astype(int)
    pen=0.0
    for x in range(lo[0],hi[0]+1):
        for y in range(lo[1],hi[1]+1):
            for z in range(lo[2],hi[2]+1):
                if (x,y,z)==(0,0,0): continue
                d=(A@np.array([x,y,z],float)+b).max()
                if d < 0: pen += -d
    return pen

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

def perp_basis(ell):
    a,b,c = ell
    found=[]
    for x in range(-6,7):
        for y in range(-6,7):
            for z in range(-6,7):
                if (x,y,z)==(0,0,0): continue
                if a*x+b*y+c*z==0: found.append((x,y,z))
    found.sort(key=lambda v: v[0]**2+v[1]**2+v[2]**2)
    B=[np.array(found[0],float)]
    for v in found[1:]:
        w=np.array(v,float)
        if np.linalg.norm(np.cross(B[0],w))>1e-9: B.append(w); break
    if abs(np.linalg.norm(np.cross(B[0],B[1]))-np.linalg.norm(np.array(ell,float)))>1e-6:
        return None
    return np.array(B)

PERP = {ell: perp_basis(ell) for ell in DIRS}
PERP = {k:v for k,v in PERP.items() if v is not None}

def section_area(pts, ell):
    B = PERP.get(ell)
    if B is None: return None
    h = hull(pts); A=h.equations[:,:3]; bb=h.equations[:,3]
    A2 = np.stack([A@B[0], A@B[1]],axis=1); b2=-bb
    verts=[]; m=len(b2)
    for i in range(m):
        for j in range(i+1,m):
            M=np.array([A2[i],A2[j]])
            if abs(np.linalg.det(M))<1e-12: continue
            z=np.linalg.solve(M,np.array([b2[i],b2[j]]))
            if np.all(A2@z<=b2+1e-7): verts.append(z)
    if len(verts)<3: return 0.0
    verts=np.array(verts)
    try: return ConvexHull(verts).volume
    except Exception: return 0.0

def mA_value(pts0):
    best = np.inf; bell=None
    for ell in PERP:
        e = np.array(ell, float)
        v = pts0 @ e
        m = min(v.max(), -v.min())   # near-side reach in lattice-height units (ell primitive: heights ell.x)
        if m <= 1e-9: continue
        a = section_area(pts0, ell)
        if a is None or a <= 1e-9: continue
        val = m * a
        if val < best: best = val; bell = ell
    return best, bell

def objective(flat):
    pts = flat.reshape(-1,3)
    bc, vol = barycenter_vol(pts)
    if bc is None: return 1e6
    pts0 = pts - bc
    pen = interior_pen(pts0)
    val, _ = mA_value(pts0)
    if not np.isfinite(val): return 1e6
    return -val + 300.0*pen

best_global = (0.0, None)
for trial in range(10**9):
    x0 = rng.normal(scale=1.6, size=(V,3)).flatten()
    res = minimize(objective, x0, method="Nelder-Mead",
                   options={"maxiter":6000,"xatol":1e-6,"fatol":1e-9})
    pts = res.x.reshape(-1,3)
    bc, vol = barycenter_vol(pts)
    if bc is None: continue
    pts0 = pts - bc
    if interior_pen(pts0) > 1e-7: continue
    val, ell = mA_value(pts0)
    if val > best_global[0]:
        best_global = (val, pts0.copy())
        print(f"trial {trial}: mA={val:.5f} (target 4.5) vol={vol:.4f} ell={ell}", flush=True)
        if val > 4.5 + 1e-4:
            np.set_printoptions(precision=5, suppress=True)
            print("EXCEEDS 4.5, vertices:"); print(pts0[hull(pts0).vertices], flush=True)
