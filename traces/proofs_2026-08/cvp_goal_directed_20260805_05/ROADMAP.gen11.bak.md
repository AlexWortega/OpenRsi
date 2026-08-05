# ROADMAP.md

## Target

Prove, without PCP machinery or unproved conjectures, a deterministic polynomial-time many-one reduction from 3SAT of size \(m\) to Euclidean GapCVP of rank \(n=\operatorname{poly}(m)\) with approximation factor \(n^c\) for an explicit absolute \(c>0\).

Every normalization, consistency, carry, boundary, and auxiliary condition must be emitted as a lattice coordinate. Soundness quantifies over all integer coefficients.

The entire Voronoi-coercive program is retired. The repeated \(D_4\), \(E_6\), and augmented-Gram failures indicate that searching fixed equal-radius NAND shells is no longer the frontier. Ordered-pair flows, group-ring convolution, literal tensoring, and fixed local min-plus tiles remain retired.

---

## Strategy 1 — Expander-sheaf norm amplification

Build on the finite G38 splitter-bag pass, but replace fixed bag shells by a scalable algebraic agreement lift. This uses explicit expanders only as emitted consistency systems, not as PCP tests or as a gap-SAT assumption.

### Lemmas

1. **Balanced legal-sheaf compilation lemma.**  
   Deterministically transform \(F\) into a bounded-degree incidence sheaf \(X_F\) of size at most \(m^4\). Each stalk has a constant-size integral selector basis; all clause legality, normalization, and complete overlap marginals are emitted. Honest \(0/1\) global sections correspond exactly to satisfying assignments. Every honest section has the same squared anchor radius \(R_0^2\).

2. **FRONTIER — robust integral agreement-lift lemma.**  
   Construct an explicit constant-degree lift \(\mathcal L\) such that, for every emitted legal-label sheaf \(X\):

   - \(\operatorname{rank}(\mathcal L X)\le4096\,\operatorname{rank}(X)\);
   - every honest section lifts canonically, with legal squared radius multiplied by a fixed \(\mu\);
   - every normalization and overlap equation of the lift is emitted and weighted;
   - defining
     \[
     \rho(X)=\frac{\min_{z\in\mathbb Z^{N_X}}E_X(z)}{R_X^2},
     \]
     for any \(X\) with no honest section,
     \[
     \rho(\mathcal L X)\ge\frac{257}{256}\rho(X);
     \]
   - the proof decomposes the complete integral disagreement module into expander cut space, cycle space, and saturated torsion-free components. It must cover zero-residual affine pseudosections, signed cycles, clause drops, and arbitrary coefficients—not merely a bounded attack list.

3. **Iterated agreement theorem.**  
   For \(t=\lfloor\log_2m\rfloor\), construct \(X_t=\mathcal L^tX_F\). If \(F\) is satisfiable, its canonical section has radius \(R_t\). If \(F\) is unsatisfiable, Lemma 2 gives
   \[
   \operatorname{dist}(y_t,L_t)^2\ge(257/256)^tR_t^2.
   \]

4. **Rational Euclidean compilation and accounting lemma.**  
   Convert the integral quadratic objective into a rational Euclidean factor using exact \(LDL^\top\) elimination and four-square rational realization. Then
   \[
   n\le m^4\,4096^t\le m^{16},
   \qquad
   \frac{\operatorname{dist}_{NO}}{\operatorname{dist}_{YES}}
   \ge n^{c_1},
   \]
   where
   \[
   c_1=\frac{\log(257/256)}{32\log2}>0.
   \]

**Why sufficient.** Lemma 1 gives exact SAT completeness. Lemma 2 supplies dimension-independent growth over unrestricted integer sections. Iteration yields polynomial separation while preserving polynomial rank, and Lemma 4 produces a standard rational GapCVP instance.

**Crux.** Proving expansion against the saturated integral cycle module. Ordinary real agreement expansion does not exclude the G13/G15 affine lift or G19 signed cycles.

**First experiment.** Apply every connected degree-\(\le4\) bipartite replacement graph on at most eight vertices to the twelve G38 bags. Compute exact depth-two minima by disagreement-state dynamic programming and SNF decomposition. Reject unless normalized adverse growth exceeds \(257/256\), the matched control radius is exact, and the complete shell includes DROP, G13, G15, G19, and all cycle-space representatives.

---

## Strategy 2 — Totally real ideal-norm gate recursion

Replace Euclidean shell coercivity by arithmetic growth in a commutative domain. False transfer states must acquire prime-ideal valuation, while Minkowski/trace norm converts valuation into Euclidean energy.

### Lemmas

1. **Balanced circuit lemma.**  
   Transform \(F\) into a bounded-fanout NAND/COPY circuit of size \(m^{O(1)}\) and depth
   \[
   \lfloor\log_2m\rfloor\le d\le4\lceil\log_2m\rceil,
   \]
   with unique legal evaluation for every input assignment.

2. **FRONTIER — associated-graded ideal gate lemma.**  
   Construct a fixed totally real field \(K\) of degree \(r\le4\), its ring of integers \(\mathcal O_K\), a prime ideal \(\mathfrak p\) with norm at least \(17\), and constant-size NAND/COPY modules satisfying:

   - legal gate configurations have identical trace-form energy and valuation zero;
   - all module, port, carry, and glue coordinates are emitted integrally;
   - on the complete adverse quotient, the transfer map induced on
     \[
     \operatorname{gr}_{\mathfrak p}M
       =\bigoplus_j\mathfrak p^jM/\mathfrak p^{j+1}M
     \]
     is injective;
   - a false root over depth \(h\) therefore yields either a nonzero defect in \(\mathfrak p^h\), or a charged coefficient vector of at least the same trace energy;
   - this dichotomy holds for every integral coefficient vector, including affine parity, diagonal embeddings, signed flows, and arbitrary carries.

3. **Ideal valuation-to-energy lemma.**  
   For nonzero \(\alpha\in\mathfrak p^h\), the arithmetic-geometric mean over the real embeddings gives
   \[
   \sum_{\sigma:K\hookrightarrow\mathbb R}\sigma(\alpha)^2
   \ge r\,17^{2h/r}.
   \]
   If legal squared energy grows by at most \(4^h\), each false circuit root gains squared ratio at least
   \[
   \left(\frac{\sqrt{17}}4\right)^h.
   \]

4. **Integral realization and gap lemma.**  
   Expand the trace forms in an integral basis of \(\mathcal O_K\), emit every glue equation, and realize the resulting rational positive-definite form in Euclidean space. With constant rank expansion and \(d=\Theta(\log m)\), obtain \(n\le m^{20}\) and
   \[
   \operatorname{dist}_{NO}/\operatorname{dist}_{YES}\ge n^{c_2},
   \qquad
   c_2=\frac{\log(\sqrt{17}/4)}{40\log2}>0.
   \]

**Why sufficient.** Unsatisfiability forces a false output. Injectivity on the associated graded prevents cancellation of its accumulated ideal defect; the field norm then yields exponential energy growth through logarithmic depth.

**Crux.** Honest difference modules are often primitive. The gate must create valuation growth without letting affine combinations become valuation-zero units or zero-defect signed splices.

**First experiment.** Enumerate real quadratic and cubic fields of discriminant at most \(500\), prime ideals of norm \(17\)–\(31\), and NAND selector modules with at most twelve columns. Use Hermite/SNF calculations over an integral basis to test associated-graded injectivity through depth two. Then exactly enumerate the remaining trace-energy shell, seeded with G13, G15, G19, DROP, diagonal, and bicyclic-style signed combinations.

---

## Complete obstruction audit

| Recorded obstruction | Strategy 1 escape | Strategy 2 escape |
|---|---|---|
| **G1 RS slack; G6 external quotient; G12 clause drop; augmented-Gram DROP** | All slack, normalization, and drop coordinates are emitted and charged. | All carries and zero selectors enter the trace form and adverse quotient. |
| **G2 affine/Graver isolation; G3 unbounded fibers; G14 finite pair-bag pass; G31 finite Walsh pass** | Saturated module theorem replaces bounded-shell extrapolation. | Associated-graded injectivity is an all-coefficient algebraic statement. |
| **G5 private-row overlap** | Complete overlaps are lifted globally through the expander. | Complete gate ports, not private marginal fragments, are glued. |
| **G7 radix kernel** | Exact kernels remain subject to integral agreement growth. | Exact residual kernels must carry ideal defect or charged module norm. |
| **G9 degree-two parity; G11 cubic parity; G13 affine collision; G15 laminar lift** | Explicitly included in the saturated cycle/affine module. | Explicitly included in the adverse quotient; primitive affine units are the main gate test. |
| **G19 signed flow; GD1 diagonal closure** | Cycle space is charged; no flow or diagonal-tensor inference is used. | Graded injectivity must block signed and diagonal cancellation. |
| **G28 min-plus failure; G32 additive parity; G37 parity cut; G38 finite splitter pass** | Uses G38 only as a seed; advancement requires a uniform lift theorem, not finite min-plus or additive composition. | Uses arithmetic valuation, not additive metric composition. |
| **G30 tensor-seed isometry** | No tensor product. | No literal tensoring; field multiplication is controlled by ideals. |
| **G33 bivector incompleteness; G34 metric-repair infeasibility** | No exterior tags or Gram repair. | Fixed trace forms replace synthesized exterior metrics. |
| **D4 triality midpoint, non-antipodal D4 Boolean shell, independent-D4 recombination** | No Delaunay or product-coordinate shell. | No Voronoi shell or separable \(D_4\) geometry. |
| **E6 bounded-map and unbounded affine-port no-go** | Ports are complete selector marginals, not affine shell projections. | Ports are module classes, not affine maps from a Delaunay cell. |
| **GD2 bicyclic group-ring units** | No convolution algebra. | \(\mathcal O_K\) is a commutative domain; the lemma still audits all signed combinations. |

---

## Recommendation

Attempt **Strategy 1** first. G38 supplies a verified finite seed, while the next step is a scalable structural theorem rather than another fixed-shell search.

**FRONTIER lemma:** robust integral agreement-lift lemma.

**First experiment:** exact depth-two expander lifts of the twelve G38 splitter bags, with SNF cycle decomposition and complete unrestricted shell search testing normalized growth \(>257/256\).
