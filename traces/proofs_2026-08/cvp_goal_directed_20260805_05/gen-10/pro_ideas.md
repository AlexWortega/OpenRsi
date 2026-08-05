1. **Excess-energy frontier instead of raw-\(\rho\) amplification.**  
**Mechanism/expected move.** Define \(\Delta(X)=\min E_X-R_X^2\). Amend FRONTIER to  
\[
R_{\mathcal LX}^2=\mu R_X^2,\qquad \Delta(\mathcal LX)\ge(257/256)\mu\Delta(X),
\]
hence \(\rho(\mathcal LX)-1\ge(257/256)(\rho(X)-1)\). This still yields a polynomial gap, while avoiding the satisfiable-padding contradiction for componentwise lifts.

**Audit.** G1/G6/G12/DROP: all emitted energy enters \(\Delta\). G2/G3/G14/G31/G38: requires an unrestricted theorem, not finite-shell extrapolation. G5: requires complete overlap. G7 and G9/G11/G13/G15: zero-residual attacks must gain anchor excess; not automatically escaped. G19/GD1: cycle excess must grow. G28/G32/G37: their additive witnesses directly falsify the recurrence. G30, G33/G34, all D4 variants, both E6 no-gos, GD2: outside assumptions—no tensor, exterior metric, shell, affine port, or convolution. Padding: explicitly repaired.

**Falsification/experiment.** Apply each roadmap graph on \(\le8\) vertices to G38 and to G38 padded by \(k=1,2,4\) satisfiable controls; search only up to the exact amended threshold.

**Likely death.** A G32-style affine witness has \(\Delta'=\mu\Delta\).

---

2. **Constant-weight code curvature on selector anchors.**  
**Mechanism/expected move.** Replace every local label by a short constant-weight codeword plus its complement, making all honest labels equidistant while giving signed distributions a nontrivial Gram curvature. Expander glue compares every code coordinate; seek a fixed code whose quadratic excess on every integral normalized non-Dirac distribution grows faster than honest energy.

**Audit.** G1/G6/G12/DROP: normalization, complements, and zero blocks are emitted. G2/G3: inequality quantifies over all integers. G14/G31: scalable repeated code, not fixed pair bags or one Walsh block, though G31 remains precedent. G5: complete coded overlaps. G7: exact residual kernels are intended to pay code-anchor curvature. G9/G11/G13/G15: not outside—these are the principal tests. G19/GD1: add complete cycle glue; curvature must still charge signed diagonals. G28/G32/G37: require strict excess recurrence, not additive composition. G38 is only seed. G30, G33/G34, D4 variants, E6 no-gos, GD2: no tensor, exterior tags, shells, ports, or convolution. Padding requires Sketch 1’s amendment.

**Falsification/experiment.** Enumerate binary constant-weight codes of length \(\le16\) for the sixteen full assignments; run exact depth-two DP on G38’s eleven full-variable bags.

**Likely death.** An integral affine mixture may have code energy exactly additive.

---

3. **Saturated integral Hodge completion.**  
**Mechanism/expected move.** For the disagreement cochain module, emit gradient \(d\), co-gradient \(d^\ast\), and an exact SNF-derived basis of the saturated harmonic lattice. A rational Hodge identity would then charge cuts, cycles, and harmonic integral classes simultaneously, rather than invoking the false inequality \(\|c\|\lesssim\|\partial c\|\) for cycles.

**Audit.** G1/G6/G12/DROP: stalk and normalization defects remain explicit coordinates. G2/G3: SNF saturation covers unrestricted fibers. G14/G31: no finite-shell inference. G5: uses complete overlaps. G7: exact kernels survive only if harmonic or stalkwise. G9/G11/G13/G15: not escaped; zero-disagreement affine pseudosections remain a fatal stalk kernel. G19/GD1: directly targeted by co-gradient and harmonic rows. G28/G32/G37: no min-plus/additive inference; test excess growth. G38 supplies the base complex. G30, G33/G34, D4 variants, E6 no-gos, GD2: outside—no tensor, tags, shells, ports, or group ring. Padding again requires excess normalization.

**Falsification/experiment.** For every connected degree-\(\le4\) bipartite graph on \(\le8\) vertices, construct exact \(d,d^\ast\), SNF harmonic rows, and enumerate G38 depth-two minima.

**Likely death.** G13/G15 lives in the simultaneous kernel before any Hodge operator sees it.

---

4. **Algebraic-geometry moment tower.**  
**Mechanism/expected move.** Place labels on a small projective curve over \(\mathbb F_q\), encode a Dirac label by evaluations of a balanced function space, and lift through a fixed-degree curve cover. Each level exposes new higher-order moments while a transitive automorphism orbit keeps honest energies equal; the desired move is that every non-Dirac integral signed measure eventually reveals a new moment.

**Audit.** G1/G6/G12/DROP: constants and homogenizing coordinates are emitted. G2/G3: needs an all-measure theorem, not bounded coefficients. G14/G31: changing AG function spaces, not fixed bags/Walsh; nevertheless their finite-only warning applies. G5: compare complete restricted evaluations. G7: old moment kernels should be exposed upstairs. G9/G11: degree growth targets parity. G13/G15: not outside—global honest-affine measures may preserve every evaluation. G19/GD1: signed measures included but cycles need glue. G28/G32/G37: recurrence must be proved, not inferred. G38 is the test sheaf. G30, G33/G34, D4 variants, E6 no-gos, GD2: no literal tensor, exterior metric, shell, affine port, or convolution. Padding needs Sketch 1.

**Falsification/experiment.** Use \(\mathbb P^1(\mathbb F_5)\), degree-\(\le2\) evaluations, and one quadratic cover on a four-bag G38 subinstance; enumerate all integral states through \(B+64\).

**Likely death.** The G13 affine span is functorial under every evaluation map.

---

5. **Two-generator integral holonomy with spectral gap.**  
**Mechanism/expected move.** Transport disagreements around the lift by two fixed matrices in \(SL_d(\mathbb Z)\) having no common nonzero fixed vector, and emit both transported edge checks and saturated harmonic coordinates. Unlike a single finite-group voltage, alternating generators could contract every nontrivial real representation while retaining integral control.

**Audit.** G1/G6/G12/DROP: all ports and zero selectors stay charged. G2/G3: requires an integral, not merely real, spectral inequality. G14/G31: uniform representation theorem replaces finite passes. G5: complete transported overlaps. G7: exact kernels must lie in the common invariant module. G9/G11/G13/G15: trivial-representation affine modes remain applicable. G19/GD1: principal target; diagonal and signed cycles meet multiple holonomies. G28/G32/G37: no additive/min-plus claim. G38 is seed only. G30: no tensor. G33/G34 and D4/E6 families: no tags or shells. GD2: no group-ring multiplication, although invariant integral submodules are analogous risks. Padding requires excess FRONTIER.

**Falsification/experiment.** Test all pairs of \(2\times2\) unimodular matrices with entries in \([-2,2]\) on every graph of the roadmap’s \(\le8\)-vertex family; compute common invariants, SNF kernels, and depth-two minima.

**Likely death.** The scalar/trivial component carries the affine pseudosection unchanged.

---

6. **Honest-affine-hull no-go certificate.**  
**Mechanism/expected move.** Refute broad classes of FRONTIER lifts before further search. Collect canonical honest vectors from satisfiable control sheaves realizing every local assignment; any label-natural linear lift preserving their equations also preserves their saturated affine hull. If a G13/G15 adverse vector lies there and the anchor map is isometric on that hull, strict amplification is impossible.

**Audit.** G1/G6/G12/DROP and G5/G7 become rows in the symbolic annihilator. G2/G3 are handled by saturation over \(\mathbb Z\). G14/G31/G38 are not extrapolated; they provide matrices. G9/G11/G13/G15 are direct certificates. G19/GD1 supply additional kernel generators. G28/G32/G37 give additive no-growth certificates. G30, G33/G34, D4 variants, E6 no-gos, GD2 are outside the theorem unless their constructions are label-natural and linear. Padding strengthens the no-go by adjoining honest components.

**Falsification/experiment.** Build sixteen satisfiable controls realizing all four-variable assignments, compute the saturated affine-hull lattice, insert the exact G13 coefficients, and solve symbolically for every radius-preserving lift Gram with rank multiplier \(\le16\).

**Likely death.** A genuinely sheaf-dependent nonlinear anchor may violate label naturality, so the certificate will not cover it.

---

7. **Exact discounted-potential certificate for a frozen lift.**  
**Mechanism/expected move.** Represent a lift step by separator marginals, affine-hull coordinates, and SNF cycle classes. Search an exact rational Bellman potential \(\Phi\) satisfying an excess inequality for every transition, together with \(|\Phi|\le\eta\Delta\); this comparison converts telescoping augmented energy back to actual energy and repairs the earlier uncancelled-potential defect.

**Audit.** G1/G6/G12/DROP: included in transition cost. G2/G3: coercivity gives a proved finite shell; SNF handles unbounded tails. G14/G31/G38: finite computation certifies a frozen uniform rule, not an asymptotic guess. G5: state records complete overlaps. G7 and G9/G11/G13/G15: exact kernel/affine coordinates are explicit states. G19/GD1: cycle classes are explicit. G28/G32/G37: their additive transitions make the LP infeasible, as desired. G30, G33/G34, D4 variants, E6 no-gos, GD2: absent unless the frozen lift uses them. Padding is compatible only with excess FRONTIER.

**Falsification/experiment.** Freeze the \(K_{3,3}\) replacement of the twelve G38 bags; enumerate the coercively bounded transition table and solve the rational LP for \(\gamma=257/256\), then verify by exact arithmetic.

**Likely death.** State count explodes, or a zero-cost affine/cycle loop forces \(\gamma\le1\).

Classical conceptual sources only: Goppa’s algebraic-geometric codes, Kazhdan’s property-\((T)\) framework, and Seymour’s regular-matroid methods; none supplies the missing lemma by itself.
