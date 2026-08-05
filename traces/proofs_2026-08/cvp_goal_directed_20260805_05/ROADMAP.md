# ROADMAP.md

## Target

Prove, without PCP machinery or unproved conjectures, a deterministic polynomial-time many-one reduction from a 3SAT instance of size \(m\) to Euclidean GapCVP of rank \(n=\operatorname{poly}(m)\), with approximation factor \(n^c\) for an explicit absolute \(c>0\).

Every normalization, legality, consistency, carry, boundary, and auxiliary condition must be emitted as a lattice coordinate. Soundness quantifies over all integer coefficient vectors.

The ramified quaternion gate-library route is retired. The canonical module has a grade-zero affine attack, while the redundant \(N=8\) NAND survivor is only a depth-one metric fact and supplies neither COPY nor recursive filtration. No further strategy may infer asymptotic amplification from that survivor.

---

## Strategy 1 — One-shot logarithmic expander bags

This retains logarithmic bags but replaces extrapolation from G38 by an explicit formula-dependent integral filling theorem.

### Lemmas

1. **Bounded-incidence compilation.**  
   Transform \(F\) deterministically into an equisatisfiable 3CNF \(F^\flat\) of size \(m^{O(1)}\), maximum incidence degree \(12\), with all COPY, auxiliary, and boundary constraints explicit and a bijection on satisfying assignments after forgetting auxiliaries.

2. **Expander-cover bag construction.**  
   Construct \(M=\operatorname{poly}(m)\) bags of width at most \(10\lceil\log_2m\rceil\), indexed by neighborhoods in an explicit lossless bipartite expander. Emit legal-assignment selectors, normalization, and complete marginal equations on every intersection. The selector count \(N\) is polynomial, and every satisfying assignment has squared anchor energy exactly \(N\).

3. **FRONTIER — saturated integral filling inequality.**  
   Choose the cover so that for every unsatisfiable \(F^\flat\) and every \(z\in\mathbb Z^N\),
   \[
   A_Fz=b_F\quad\Longrightarrow\quad
   \|2z-\mathbf1\|_2^2\ge N^{1+1/32}.
   \]
   The proof must classify the entire saturated kernel, including affine pseudosections, clause drops, torsion, signed cycles, diagonal embeddings, and sections supported on proper subcovers. It must be a direct integer expansion/filling argument, not a local-rejection theorem.

4. **GapCVP realization.**  
   Use
   \[
   E(z)=\|2z-\mathbf1\|_2^2+
   W\|A_Fz-b_F\|_2^2,\qquad
   W=\lceil N^{1+1/32}\rceil .
   \]
   Completeness is \(N\); in a NO instance either the residual costs \(W\), or Lemma 3 applies. Rational factorization yields rank \(n=N\) and distance gap at least \(n^{1/64}\).

**Why sufficient.** Lemma 3 controls exactly the zero-residual signed branch; weighting handles every other integer vector.

**Crux.** Prove superlinear integral filling without enumerating global assignments or silently invoking agreement testing.

**First experiment.** Convert parity contradictions on explicit 3-regular expanders of orders \(6,8,10\) to 3CNF. Build the prescribed logarithmic bags and compute the exact zero-residual minimum by SNF plus certified MIQP. Reject the route if normalized anchor excess fails to increase between two consecutive sizes or if any G13/G19/diagonal witness remains bounded.

---

## Strategy 2 — Occurrence-tagged free-word computation histories

Replace quotient algebras and finite transfer tables by the free associative algebra, where distinct computation histories cannot fuse algebraically.

### Lemmas

1. **Balanced circuit compilation.**  
   Compile \(F\) into a bounded-fanout NAND/COPY circuit of size \(m^{O(1)}\) and depth
   \[
   \lceil\log_2m\rceil\le h\le6\lceil\log_2m\rceil ,
   \]
   with accepting output and all fanout equalities explicit.

2. **Prefix-free history encoding.**  
   Assign each gate occurrence its own alphabet symbols. Construct selector coordinates indexed by legal labelled prefixes of length at most \(h\), emitting normalization, gate, prefix-marginal, COPY, and boundary equations. No words are identified by commutation, group multiplication, or truncation. Rank is at most \(m^{60}\).

3. **FRONTIER — free-word adverse-mass theorem.**  
   For every false-root integral section of the complete emitted system,
   \[
   E_{\mathrm{false}}(h)\ge
   \left(\frac{33}{32}\right)^hE_{\mathrm{legal}}(h).
   \]
   This must hold for arbitrary signed coefficients and non-rank-one couplings. The proof must use unique-word coefficients and a global prefix cancellation invariant, not a finite min-plus state table. It must explicitly rule out diagonal path embeddings and affine combinations of complete histories.

4. **Euclidean accounting.**  
   Add a residual weight above the adverse bound and factor the resulting integral Gram matrix. Since \(n\le m^{60}\), the distance gap is
   \[
   n^{c_2},\qquad
   c_2=\frac{\log_2(33/32)}{120}>0 .
   \]

**Why sufficient.** A false output forces excess mass at every prefix depth; logarithmic depth turns constant multiplicative excess into a polynomial gap.

**Crux.** COPY identifications may allow a signed section to recombine occurrence-tagged histories without ever identifying their words.

**First experiment.** Emit the smallest depth-two NAND/COPY tree using occurrence-tagged words and the best known eight-coordinate redundant signatures only as a search seed. Compute exact unrestricted minima for depths one, two, and three. Include DROP, G13, G19, diagonal-splice, and bicyclic-shaped coefficient patterns. Reject unless the squared adverse/legal ratio grows by at least \(33/32\) at both compositions.

---

## Strategy 3 — Logarithmic nonbacktracking-walk Gram

Generalize the finite equal-radius Walsh success using formula-dependent long walks rather than copywise moments or incidence-orbit weights.

### Lemmas

1. **Bounded-incidence compilation.**  
   Use Lemma 1 of Strategy 1.

2. **Equal-radius walk features.**  
   For \(d=\lceil\log_2m\rceil\), enumerate all nonbacktracking incidence walks of length at most \(d\). For each walk emit signed character features of the local labels encountered along it. There are \(m^{O(1)}\) features, and every honest global assignment has the same feature norm.

3. **FRONTIER — signed-walk spectral coercion.**  
   There is a deterministic choice of walk signs and weights such that every unsatisfiable instance and unrestricted integral selector vector satisfies either a nonzero emitted residual or
   \[
   E_{\mathrm{walk}}(z)\ge
   \left(\frac{65}{64}\right)^dR_{\mathrm{YES}}^2.
   \]
   The proof must act on the full signed selector module. In particular, proper-moment parity, affine-span collisions, copywise additive witnesses, and diagonal sections must have a nonzero expanding nonbacktracking component.

4. **Factorization and gap.**  
   Emit the walk matrix directly and weight ordinary residuals above the claimed bound. If rank is at most \(m^{50}\), rational factorization gives
   \[
   c_3=\frac{\log_2(65/64)}{100}>0.
   \]

**Why sufficient.** Equal-radius features preserve completeness, while logarithmic walk length converts spectral excess into polynomial Euclidean separation.

**Crux.** Establish coercion on integral signed distributions, not merely on real functions orthogonal to honest assignments.

**First experiment.** On the nine-clause obstruction and its two-copy additive-parity instance, emit all nonbacktracking features for \(d=1,2,3\). Use exact DP to optimize the unrestricted zero-residual energy. Reject if the G11/G13 parity remains additive, if a clause drop wins, or if the adverse/legal squared ratio fails to increase with \(d\).

---

## Complete obstruction audit

| Obstruction | Required escape in Strategies 1 / 2 / 3 |
|---|---|
| **G1 RS slack, G6 external quotient, G7 radix kernel** | No external filters or free carries. All equations are emitted; the frontier lemmas cover zero residual and explicit weights cover nonzero residual. |
| **G12 spherical-fingerprint clause DROP; augmented-Gram zero DROP** | DROP is named in all frontier statements and first experiments; no bounded-entry extended Gram is used. |
| **G2 affine/Graver isolation, G3 unbounded fibers** | Every frontier quantifies over the complete unbounded integer lattice and saturated kernel. |
| **G14 finite pair bags, G31 finite Walsh pass, G38 finite splitter pass** | S1 proves a scalable expander filling inequality; S3 uses logarithmic walks. Neither extrapolates from a finite shell. |
| **G5 private overlap, G9/G11 parity, G13 affine collision, G15 laminar lift** | S1 uses complete expander intersections; S2 uses unique occurrence words; S3 explicitly requires spectral detection of affine and parity classes. |
| **G19 signed flow, GD1 diagonal closure, ordered-pair diagonal splice** | Diagonal and signed-history sections are explicit cases of every frontier lemma. |
| **G28 min-plus failure, G32 additive parity, G37 parity cut** | No fixed transfer table. S2 requires a global free-word invariant; S3 uses nonbacktracking cross-incidence features and must defeat additive parity. |
| **G30 tensor isometry** | No literal Kronecker tensoring occurs. |
| **GD2/A5 bicyclic units** | S2 uses the free monoid without quotient multiplication; S1/S3 use no convolution algebra. |
| **G33 bivector incompleteness, G34 metric-repair infeasibility** | No exterior tags or repaired exterior Gram. |
| **D4 midpoint, non-antipodal D4 Boolean obstruction, independent-D4 recombination** | No fixed Voronoi/Delaunay shell or coordinate-separable port geometry. |
| **E6 bounded-map and unbounded affine-port no-go** | No affine projection of a fixed shell. |
| **F289 grade-zero attack; redundant-\(N=8\) finite survivor** | Residue/quaternion filtration is retired. The survivor may seed experiments but is not a lemma or recursive mechanism. |

---

## Recommendation

Attempt **Strategy 3** first: it has the smallest global experiment and directly confronts the known additive parity obstruction.

**FRONTIER lemma:** signed-walk spectral coercion.

**First experiment:** exact \(d=1,2,3\) nonbacktracking-walk Gram optimization on the nine-clause obstruction and its two-copy parity witness, with unrestricted integer coefficients and all DROP, G13, G19, and diagonal attacks included.
