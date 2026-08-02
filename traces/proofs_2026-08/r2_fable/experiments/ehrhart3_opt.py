# Question: in R^3, what does the maximizer of vol(K) look like subject to barycenter(K)=0
# and int(K) cap Z^3 = {0}? Conjecture: sharp simplex, vol = 32/3 ~ 10.667.
# Method: polytopes with V vertices, translate to barycenter 0, penalize interior lattice
# points (depth = distance inside boundary), maximize volume by random restarts + Nelder-Mead/CMA-ish.
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import minimize
import sys

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
V = int(sys.argv[2]) if len(sys.argv) > 2 else 4

def hull_data(pts):
    try:
        h = ConvexHull(pts)
    except Exception:
        return None
    return h

def barycenter(h, pts):
    # centroid of the polytope via simplex decomposition from mean point
    c = pts[h.vertices].mean(axis=0)
    tot = 0.0; cen = np.zeros(3)
    for s in h.simplices:
        tri = pts[s]
        # tetra c, tri
        M = tri - c
        vol = abs(np.linalg.det(M)) / 6.0
        cent = (c + tri.sum(axis=0)) / 4.0
        tot += vol; cen += vol * cent
    return cen / tot, tot

def interior_penalty(h, pts):
    # sum of depths of nonzero lattice points strictly inside
    A = h.equations[:, :3]; b = h.equations[:, 3]
    lo = np.floor(pts.min(axis=0)).astype(int); hi = np.ceil(pts.max(axis=0)).astype(int)
    pen = 0.0
    for x in range(lo[0], hi[0]+1):
        for y in range(lo[1], hi[1]+1):
            for z in range(lo[2], hi[2]+1):
                if x == 0 and y == 0 and z == 0: continue
                p = np.array([x,y,z], float)
                d = (A @ p + b).max()   # <=0 inside; depth = -max
                if d < -1e-9:
                    pen += -d
    return pen

def objective(flat):
    pts = flat.reshape(-1,3)
    h = hull_data(pts)
    if h is None or len(h.vertices) < 4: return 1e6
    bc, vol = barycenter(h, pts)
    pts0 = pts - bc
    h2 = hull_data(pts0)
    if h2 is None: return 1e6
    pen = interior_penalty(h2, pts0)
    return -vol + 200.0 * pen

best = (0, None)
for trial in range(400):
    x0 = rng.normal(scale=1.5, size=(V,3)).flatten()
    res = minimize(objective, x0, method="Nelder-Mead",
                   options={"maxiter": 4000, "xatol":1e-6, "fatol":1e-8})
    val = -res.fun
    pts = res.x.reshape(-1,3)
    h = hull_data(pts)
    if h is None: continue
    bc, vol = barycenter(h, pts)
    pts0 = pts - bc
    h2 = hull_data(pts0)
    pen = interior_penalty(h2, pts0)
    if pen < 1e-7 and vol > best[0]:
        best = (vol, pts0.copy())
        print(f"trial {trial}: vol={vol:.5f} pen={pen:.2e}", flush=True)

print(f"V={V} BEST vol = {best[0]:.6f}  (target 32/3 = {32/3:.6f})")
if best[1] is not None:
    np.set_printoptions(precision=4, suppress=True)
    h = ConvexHull(best[1])
    print("vertices:"); print(best[1][h.vertices])
