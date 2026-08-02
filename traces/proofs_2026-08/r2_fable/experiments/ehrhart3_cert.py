# Question: for numerically found near-extremal n=3 bodies (barycenter 0, no nonzero
# interior lattice point), does some primitive direction ell give the prior-run certificate
# w * rho^2 <= 8/3  (=> vol <= w(2 rho)^2 <= 32/3)?  And which variants succeed where?
# Usage: python3 ehrhart3_cert.py <vertices.json>   (json: list of [x,y,z])
# Also runs on the sharp simplex and a few test bodies if no arg given.
import json, sys, itertools
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog

def support(pts, d):
    return pts @ d

def width_dir(pts, ell):
    v = pts @ ell
    return v.max() - v.min()

def section_2d(pts, ell, level=0.0, tol=1e-9):
    """Vertices of K cap {ell.x = level} as 2D polygon in an orthonormal basis of ell^perp.
    K given by hull of pts. Returns (poly2d (m,2), basis (2,3))."""
    h = ConvexHull(pts)
    A = h.equations[:, :3]; b = h.equations[:, 3]
    # basis of ell^perp
    ell = np.asarray(ell, float); ell = ell / np.linalg.norm(ell)
    # find two orthonormal vectors
    u = np.eye(3)[np.argmin(np.abs(ell))]
    e1 = u - (u @ ell) * ell; e1 /= np.linalg.norm(e1)
    e2 = np.cross(ell, e1)
    # section polytope in (s,t): A(level*ell + s e1 + t e2) + b <= 0
    A2 = np.stack([A @ e1, A @ e2], axis=1)
    b2 = -(b + A @ (level * ell))
    # enumerate vertices of {A2 z <= b2} by pairwise intersections
    verts = []
    m = len(b2)
    for i in range(m):
        for j in range(i+1, m):
            M = np.array([A2[i], A2[j]])
            if abs(np.linalg.det(M)) < 1e-12: continue
            z = np.linalg.solve(M, np.array([b2[i], b2[j]]))
            if np.all(A2 @ z <= b2 + 1e-7):
                verts.append(z)
    if not verts: return None, None
    verts = np.array(verts)
    if len(verts) >= 3:
        try:
            h2 = ConvexHull(verts)
            verts = verts[h2.vertices]
        except Exception:
            pass
    return verts, np.stack([e1, e2])

def rho_asym(poly2d, center=None, tol=1e-9):
    """min rho such that (P - c) subset -rho (P - c), c = origin (in section coords).
    P contains origin required. rho = max over vertices v of h_P(-v/|..|)... compute:
    rho = min{r: P subset -r P} = max_v min{r: -v/r ... } -- use support functions:
    P subset -rP  iff for all directions d: h_P(d) <= r h_P(-d).
    With P polygon, suffices to check facet normals of -P. We approximate by dense directions."""
    P = np.asarray(poly2d, float)
    if center is not None: P = P - center
    # need 0 in interior
    # support function via vertices
    best = 0.0
    for th in np.linspace(0, 2*np.pi, 720, endpoint=False):
        d = np.array([np.cos(th), np.sin(th)])
        hp = (P @ d).max(); hm = (P @ (-d)).max()
        if hm <= tol:
            return np.inf
        best = max(best, hp / hm)
    return best

def primitive_dirs(maxc=4):
    out = []
    for a in range(-maxc, maxc+1):
        for b in range(-maxc, maxc+1):
            for c in range(0, maxc+1):
                if (a,b,c) == (0,0,0): continue
                if c == 0 and (b < 0 or (b == 0 and a < 0)): continue
                from math import gcd
                g = gcd(gcd(abs(a),abs(b)),abs(c))
                if g != 1: continue
                out.append(np.array([a,b,c], float))
    return out

def check_body(pts, name=""):
    pts = np.asarray(pts, float)
    h = ConvexHull(pts)
    vol = h.volume
    results = []
    for ell in primitive_dirs(3):
        w = width_dir(pts[h.vertices], ell) / np.linalg.norm(ell)  # width in lattice units: use ell integer: lattice width = max ell.x - min ell.x
        lw = (pts @ ell).max() - (pts @ ell).min()   # lattice width for integer ell
        sec, _ = section_2d(pts, ell, 0.0)
        if sec is None: continue
        r = rho_asym(sec)
        crit = lw * r * r
        bound = lw * (2*r)**2 if np.isfinite(r) else np.inf
        results.append((crit, lw, r, tuple(int(x) for x in ell), bound))
    results.sort(key=lambda t: t[0])
    best = results[0] if results else None
    print(f"[{name}] vol={vol:.5f}  best cert: crit={best[0]:.4f} (need<=8/3={8/3:.4f}) "
          f"lw={best[1]:.4f} rho={best[2]:.4f} ell={best[3]} -> bound {best[4]:.4f}")
    return vol, results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pts = np.array(json.load(open(sys.argv[1])))
        check_body(pts, sys.argv[1])
    else:
        # sharp simplex
        S = 4*np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1.0]]) - 1.0
        check_body(S, "sharp simplex")
        # cube [-1,1]^3 scaled to open condition: (2-eps) cube... use [-1,1]^3 (boundary pts ok)
        C = np.array(list(itertools.product([-1,1],repeat=3)), float)
        check_body(C, "cube [-1,1]^3")
        # cross-polytope 2*conv(+-e_i)? interior lattice pts: +-e_i inside. use conv(+-1.5 e_i)? contains +-e_i interior. use conv(+-e_i)*2 - no. Use octahedron |x|+|y|+|z|<=2: contains e_i on... |e_i|_1=1<2 interior -> violates. skip.
