# Ehrhart attack log (current run)

Gap: n=3 bodies that are highly asymmetric with no narrow near-symmetric zero
section. Target: complete n=3.

## Three code-driven routes

1. **Numerical extremizer hunt in n=3.** Maximize vol(P) over polytopes with
   barycenter 0 and int(P)∩Z^3={0}; confirm the simplex (32/3) is max, and map
   the local-max landscape. Reverse-engineer the structure of near-extremal
   bodies (which lattice points are on the boundary, what widths occur).
   First experiment: experiments/ehrhart3_opt.py (projected gradient / local
   move on vertex polytopes, penalty for interior lattice points).

2. **Covering-radius / width dichotomy.** Every lattice-point-free-interior K
   with barycenter 0 has bounded lattice width in some primitive direction
   (flatness-type). Compute, for near-extremal numerical bodies, min over
   primitive ℓ of (width_ℓ, ρ of zero fiber): does some certificate variant
   (e.g. using the section through the *barycenter of the slab* rather than 0,
   or a two-direction certificate) always succeed except at the simplex?
   Experiment: experiments/ehrhart3_cert.py on optimizer output.

3. **Simplex-neighborhood rigidity.** Prove: if K is close to the sharp simplex
   it satisfies the bound (local analysis); combined with a global bound for
   bodies far from the simplex (e.g. quantitative certificate). Experiment
   first: perturb the sharp simplex, check vol always decreases under the
   constraints (numerically) to guide the local proof.

## Log
- Prior verifiers pass. Starting optimizer.
- ehrhart3_opt (V=4..8): best feasible volumes so far 9.18 (V=4), 8.84 (V=6);
  approaching 32/3=10.667 from below, no counterexample. Simplex-local perturbation
  run confirms 32/3 is a strict local max (start vol stays 10.6667, pen 0).
- ehrhart3_cert: prior-run certificate w·ρ²≤8/3 FAILS at the sharp simplex itself
  (best crit = 4.0 > 8/3). Confirmed: that route cannot contain the extremizer.
- NEW candidate two-part certificate (tight at the simplex): ∃ primitive ℓ with
  (a) vol(K) ≤ (4/3)³ · area_lat(K ∩ ℓ^⊥)  and  (b) area_lat(K ∩ ℓ^⊥) ≤ 9/2.
  ehrhart3_ratio: holds on 200 random feasible bodies; equality (both parts) at
  the sharp simplex with ℓ=e₃. ehrhart3_adv (running): adversarially maximize
  min_ℓ max(ratio/(4/3)³, area/4.5); max found so far 0.876 < 1.
- IMPORTANT NEGATIVE (planar_one_pt): a planar convex body with unique interior
  lattice point can have area > 9/2 (slivers; unbounded). So part (b) cannot
  follow from the section being 'unique-interior-point' alone — the 3D barycenter
  constraint must be used to rule out sliver sections. The proof of (b) must show:
  if every good-ℓ section is a sliver, the body itself is a slab-like body handled
  by the width route. Two-lemma structure to prove:
    Lemma A (1D): h≥0, h^{1/2}... actually f(t)=area of slice, f^{1/2} NOT concave
    in 3D — f^{1/3}? No: slices of 3D body: f^{1/2} concave (Brunn-Minkowski,
    codim 1 slices of 3D body have f^{1/(n-1)}=f^{1/2} concave). With barycenter
    condition ∫t f = 0 and lattice-width constraint, want ∫f ≤ (64/27) f(0).
    lemmaR_w.py: numerics suggest R(w) ≤ max(w, 64/27) roughly; cone profile on
    [-1,3] attains 64/27 at w=4. Need the exact statement.
    Lemma B (2D): section through 0 of a feasible body with the induced barycenter
    control has lattice-area ≤ 9/2. OPEN — this is where slivers must be excluded.
