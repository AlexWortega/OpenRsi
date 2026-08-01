# Status

Updated: budget-terminal verification completed; all checks pass and both problems remain PARTIAL.

## Problem 1 — Ehrhart volume conjecture

**Status: PARTIAL. The general conjecture is not proved, and the unrestricted `4^n` bound is not improved.**

Rigorous results in `proof_ehrhart.md`:

- Symmetric bodies satisfy `vol(K)<=2^n`; more generally `K subset -rho K` gives `vol(K)<=(2rho)^n`.
- A general section theorem uses Brunn--Minkowski and a log-concave entropy inequality. Under a compatible primitive section, it gives `vol_n(K)<=2A_(n-1)<A_n`. It is unconditional for the resulting three-dimensional class and permits changing, asymmetric sections.
- If the zero section has origin-asymmetry `rho` and projection width `w`, then `vol(K)<=w(2rho)^(n-1)`. In dimension three, `w rho^2<=8/3` suffices.
- Higher-codimension projection--fiber lifting gives `vol(K)<=A_mA_r<=A_n` for centered known terminal factors, and `vol(K)<=(2rho_P)^r(2rho_0)^m` for origin-asymmetric factors. Integral-linear interior selectors can create the required zero section by a unimodular shear.
- Compatible partial flags, recursive block factorizations, coupled homothetic fibers, products, and lattice-aligned centered pyramids are treated. Equality in the analytic section estimate forces an affine-sheared cylinder.

**Precise gap:** an arbitrary highly asymmetric body need not have a primitive direction with a narrow, origin-nearly-symmetric zero section, nor a compatible projection--fiber splitting. None of the proved structured criteria controls that case or contains the sharp simplex geometry.

## Problem 2 — multicolor triangle Ramsey lower bound

**Status: PARTIAL. No superexponential lower bound is proved. The asymptotic consequences remain weaker than the best classical exponential construction quoted in the prompt.**

Rigorous results in `proof_ramsey.md`:

- Explicit checked colorings of `K_16` with three colors and `K_32` with four colors; the latter has no numerical advantage. A fixed-layer extension of the displayed `F_2^5` partition to `F_2^6` is computer-verified impossible, but unrestricted `F_2^6` remains unresolved.
- Exact lexicographic, first-difference, and missing-color blow-up lemmas. Fixed seeds remain fixed-base exponential.
- For locally `s`-colored complete graphs, `L_s<=1+sL_(s-1)<3s!`, with `L_1=2,L_2=5,L_3=16`. Palette-type, multiplicity, equality-regularity, and global-palette constraints are proved. The attempted `L_4=65` aggregate obstruction is feasible and therefore banked.
- Exact capacity identity:
  `max_(alpha(G)<=r) alpha(G^boxtimes k)=R_k(r+1)-1`.
  For `alpha(G)<=2`, the strong-square values are exactly `1,4,5`; value `5` occurs iff the triangle-free complement contains `C_5`.
- `Theta(G)<=chi_f(overline G)<=chi(overline G)`. Nonempty bipartite complements have capacity exactly `2`.
- Independent-coordinate random product codes cannot beat base `2` using direct first moment, elementary edge expurgation, or the basic dependency-graph LLL, even with coordinate-dependent marginals.
- Effective interpolation/capacity criteria identify the needed quantitative witness-power control.

**Precise gap:** construct a coherent family of correlated strong-power codes, or equivalent colorings, whose per-color base grows. Fixed seeds, simple products, iid pair-event methods, tested permutation constructions, and tested algebraic extensions do not do this.

## Reproducibility and integrity

- `python3 verify_ramsey.py` checks the `K_16` and `K_32` seeds, 560 and 4,960 triangles, fixed-layer nonextension node counts `[57,56,64,64]`, and the ternary aggregate witness.
- `python3 verify_ehrhart.py` checks the exact constants and factor inequalities used in the Ehrhart write-up.
- No forbidden document, mirror, summary, or coverage was accessed or searched.
