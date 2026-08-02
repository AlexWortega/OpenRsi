# Question: is the sharp simplex S = 4*conv{0,e1,e2,e3} - (1,1,1) a strict local max of volume
# among barycenter-0, interior-lattice-free convex bodies in R^3? Perturb its 4 vertices,
# re-center, project back to feasibility, and see if volume can exceed 32/3.
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import minimize

S0 = np.array([[-1,-1,-1],[3,-1,-1],[-1,3,-1],[-1,-1,3]], float)

def analyze(pts):
    h = ConvexHull(pts)
    c = pts.mean(axis=0)  # for simplex, centroid of vertices = barycenter
    return h, c

def centroid_poly(pts):
    h = ConvexHull(pts)
    c0 = pts[h.vertices].mean(axis=0)
    tot=0.; cen=np.zeros(3)
    for s in h.simplices:
        tri = pts[s]; M = tri - c0
        v = abs(np.linalg.det(M))/6.0
        tot += v; cen += v*(c0+tri.sum(axis=0))/4.0
    return cen/tot, tot

def pen(pts):
    h = ConvexHull(pts)
    A = h.equations[:,:3]; b = h.equations[:,3]
    lo = np.floor(pts.min(0)).astype(int); hi = np.ceil(pts.max(0)).astype(int)
    p = 0.0
    for x in range(lo[0],hi[0]+1):
        for y in range(lo[1],hi[1]+1):
            for z in range(lo[2],hi[2]+1):
                if (x,y,z)==(0,0,0): continue
                d = (A@np.array([x,y,z],float)+b).max()
                if d < -1e-12: p += -d
    return p

def obj(flat):
    pts = flat.reshape(-1,3)
    try:
        bc, vol = centroid_poly(pts)
    except Exception:
        return 1e6
    pts0 = pts - bc
    return -vol + 500.0*pen(pts0)

rng = np.random.default_rng(7)
best = 32/3
print(f"start vol {32/3:.6f}, feasible pen {pen(S0):.2e}")
for eps in [0.3, 0.1, 0.03]:
    for t in range(60):
        x0 = (S0 + rng.normal(scale=eps, size=S0.shape)).flatten()
        r = minimize(obj, x0, method="Nelder-Mead", options={"maxiter":6000,"fatol":1e-10,"xatol":1e-8})
        pts = r.x.reshape(-1,3)
        try:
            bc, vol = centroid_poly(pts)
        except Exception:
            continue
        p = pen(pts-bc)
        if p < 1e-9 and vol > best + 1e-6:
            best = vol
            print(f"eps={eps} t={t}: IMPROVED vol={vol:.6f}", flush=True)
print(f"final best {best:.6f} vs 32/3={32/3:.6f} -> {'simplex beaten!' if best>32/3+1e-6 else 'simplex locally maximal (numerically)'}")
