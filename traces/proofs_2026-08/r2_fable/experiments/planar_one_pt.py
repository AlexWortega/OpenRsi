# Question: does every planar convex body whose interior contains exactly one lattice point
# have area <= 9/2? (classical for lattice polygons: Scott; here general bodies).
# Adversarial: maximize area of polygon with 0 the only interior lattice point (0 interior).
import numpy as np, sys
from scipy.spatial import ConvexHull
from scipy.optimize import minimize

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 0)

def area_pen(flat, V):
    pts = flat.reshape(V,2)
    try: h = ConvexHull(pts)
    except Exception: return 1e6
    A = h.equations[:,:2]; b = h.equations[:,2]
    lo = np.floor(pts.min(0)).astype(int); hi = np.ceil(pts.max(0)).astype(int)
    pen = 0.0; has0 = False
    for x in range(lo[0],hi[0]+1):
        for y in range(lo[1],hi[1]+1):
            d = (A@np.array([x,y],float)+b).max()
            if (x,y)==(0,0):
                if d < -1e-9: has0 = True
                else: pen += d + 0.1
                continue
            if d < 0: pen += -d
    if not has0: pen += 1.0
    return -h.volume + 100*pen

best = 0.0
for trial in range(600):
    V = rng.integers(3, 8)
    x0 = rng.normal(scale=1.5, size=(V,2)).flatten()
    res = minimize(area_pen, x0, args=(V,), method="Nelder-Mead",
                   options={"maxiter":6000, "fatol":1e-10})
    pts = res.x.reshape(V,2)
    try: h = ConvexHull(pts)
    except Exception: continue
    A = h.equations[:,:2]; b = h.equations[:,2]
    lo = np.floor(pts.min(0)).astype(int); hi = np.ceil(pts.max(0)).astype(int)
    bad = False; has0 = False
    for x in range(lo[0],hi[0]+1):
        for y in range(lo[1],hi[1]+1):
            d = (A@np.array([x,y],float)+b).max()
            if (x,y)==(0,0): has0 = d < -1e-7
            elif d < -1e-7: bad = True
    if bad or not has0: continue
    if h.volume > best:
        best = h.volume
        print(f"trial {trial}: area={best:.6f} (target 4.5)", flush=True)
        if best > 4.5 + 1e-4:
            print("EXCEEDS 4.5:", pts[h.vertices], flush=True)
print(f"BEST {best:.6f} vs 4.5")
