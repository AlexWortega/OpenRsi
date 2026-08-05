# ROADMAP.md

I did not consult the prohibited recent document or any account of its solutions. The attached scout likewise discarded an incidental result without opening it. Only the supplied materials and classical literature are used.

## Target

Give a deterministic polynomial-time many-one reduction from 3SAT of size \(S\) to Euclidean GapCVP in dimension \(n=\operatorname{poly}(S)\), with

\[
\operatorname{dist}_{\rm NO}>n^c\operatorname{dist}_{\rm YES}
\]

for an explicit absolute \(c>0\), without PCPs or unproved conjectures.

The affine quaternionic frontier is retired: further COPY searches exposing only the old seam marginals are forbidden unless they first defeat the toric exchange mechanism symbolically.

---

## Strategy 1 — Toric refinement, graded quaternion transfer, cycle-mean certification

Replace the killed affine checksum by pair-selector coordinates representing genuine products in the graded quaternion division ring.

### Lemma chain

**Q1. Toric-refined NAND/COPY tile lemma.**  
For the surviving \(N=8\) NAND module, construct constant-size fusion and COPY tiles over a maximal order \(\mathcal O\subset(-3,-17)\), with prime \(P\), satisfying:

1. all legal fibers are saturated and have common energy \(E\);
2. DROP and every false fiber either cost at least \(17E\) or have a nonzero transfer symbol;
3. if \(G\) is the projected-fiber Markov/Graver basis of the old seam grading, then every non-honest \(g\in G\), including the observed `false111-COPY11-false111` exchange, obeys
   \[
   \operatorname{in}_P T(g)\ne0;
   \]
4. \(T\) is emitted linearly on pair selectors but has tags \(a_jb_k\), so it refines the old grading and is not another affine checksum homogeneous under that grading.

**Q2. Symbolic valuation-transfer lemma.**  
Partition adverse states into finitely many residue classes and prove, for every lift and every transition,
\[
\operatorname{in}_P T_{\rm parent}
 =u\,\operatorname{in}_P T_{\rm child}\,v,
\qquad u,v\ne0
\]
after any prescribed gain factor \(\Pi^{\Delta}\). Since \(\operatorname{gr}_P(D)\) is a graded division ring, the right side never vanishes. The residue partition must be lift-independent; equivalently, all \(P\)-adic sections stabilize.

**Q3. Cycle-mean amplification lemma.**  
For the resulting finite adverse graph, assign edge weight
\[
w(e)=4\Delta v(e)-1.
\]
Every reachable directed cycle has positive mean weight. Karp duality then produces an integral potential \(h\) with
\[
w(u,v)+h(u)-h(v)\ge1.
\]
The existing Lean telescope yields
\[
v(T_{\rm root})\ge d/4-O(1)
\]
along every adverse path of length \(d\).

**Q4. Balanced compiler and energy lemma.**  
Compile a size-\(S\) 3CNF into a saturated NAND/COPY network of depth
\(d\ge\lfloor\log_2S\rfloor-O(1)\), with all coordinates explicitly emitted. Completeness has squared radius \(O(S\log S)\). Unsatisfiability supplies an adverse root-to-leaf path, and
\[
d_{\rm NO}^2\ge 17^{d/4-O(1)}.
\]

**Q5. Parameter lemma.**  
Arrange \(n\le S^{20}\). Since
\[
17^{d/4}/(S\log S)=S^{\log_2(17)/4-1-o(1)},
\]
the distance ratio is at least \(n^{1/2500}\) for large \(S\); hard-code smaller instances.

**Why sufficient.** Q1 creates the missing nonzero leading class; Q2 prevents cancellation under all lifts; Q3 gives uniform depth growth; Q4–Q5 convert it into the target GapCVP reduction.

**Crux.** Q1: separating the complete projected-fiber Markov basis, not merely the displayed exchange.

**First experiment.** Encode the current NAND/COPY seam in `4ti2` or Macaulay2, verify that the `111` splice is a `Quad`/projected-fiber generator, and enumerate product tags \(a_jb_k\bmod P^2\) from the smallest quaternion residue alphabet. Reject any tag set for which a non-honest primitive generator, DROP, or false NAND fiber has zero initial symbol.

---

## Strategy 2 — Möbius bags, primitive-move localization, expander detection

This is the commutative fallback, but it replaces named-attack testing by a universal Graver statement.

### Lemma chain

**M1. Depth-uniform primitive-localization lemma.**  
Construct polynomially many \(O(\log S)\)-variable splitter bags, each carrying all squarefree moments. For the complete bag-gluing matrix \(A_S\), every \(g\in\operatorname{Gr}(A_S)\) is either an honest global reassignment difference or has Möbius-defect support at most \(C\log S\). This includes negative coefficients, DROP, Lawrence moves \((u,-u)\), and diagonal splices.

**M2. Explicit expander detection lemma.**  
Attach an explicit \((C\log S,\varepsilon)\)-lossless-expander adjacency matrix \(H\). Every non-honest primitive defect satisfies \(H\Delta\ne0\) by a unique-neighbor row. Conformal Graver decomposition then extends detection to every signed integral deviation without cancellation.

**M3. Strict recursive cost lemma.**  
Give complete unrestricted min-plus tables for legal, detected, DROP, and malformed states and prove
\[
C_{\rm YES}(d)\le\mu^dC_0,\qquad
C_{\rm NO}(d)\ge\lambda^dC_0,\qquad
\lambda/\mu\ge65/64.
\]
No shell-restricted or named-attack state may be omitted.

**M4. Compiler and parameter lemma.**  
With \(d=\lfloor\log_2S\rfloor\) and \(n\le S^{20}\), obtain distance ratio
\[
(65/64)^{d/2}\ge n^{1/2500}.
\]

**Why sufficient.** M1 universalizes signed soundness, M2 detects every primitive defect, and M3–M4 provide multiplicative rather than finite-instance separation.

**Crux.** M1, especially whether the logarithmic-depth matrices admit uniform Graver localization rather than only fixed-stage stabilization.

**First experiment.** Compute the Graver bases of the smallest three-, four-, and five-bag overlap templates from G38. Record primitive support versus depth and test whether each matrix is an \(n\)-fold flattening with fixed blocks. Superlogarithmic primitive support or a surviving diagonal move kills the chain.

---

## Strategy 3 — Exact homogenization and rank-\(\le43\) E-type recursion

Use tensor amplification only after obtaining a genuine homogeneous minimum problem.

### Lemma chain

**T1. Exact layer-forcing homogenization lemma.**  
For each affine tile \((L,t)\), construct
\[
\widehat L=\{(x-kt,kH):x\in L,\ k\in\mathbb Z\}
\]
with rationally certified \(H\) such that every nonzero minimum has \(k=\pm1\); all \(k=0\) and \(|k|\ge2\) vectors are strictly longer. Legal and adverse minima must equal the intended CVP coset minima, including DROP and signed fibers.

**T2. Nonisometric rank-\(\le43\) tile lemma.**  
Construct NAND and COPY homogeneous tiles of rank at most \(43\), with legal minimum \(R\), adverse minimum at least \(\sqrt{17/16}R\), saturated gluing, and formula-dependent seeds not related by coefficient or ambient isometries. Their seam must pass the Q1 toric-exchange audit.

**T3. E-type tensor recursion lemma.**  
Tensor recursively with one fresh rank-\(\le43\) tile at each level. Kitaoka’s E-type theorem forces every minimum to be decomposable, hence
\[
d_{\rm YES}\le R^d,\qquad
d_{\rm NO}\ge(\sqrt{17/16}R)^d
\]
without entangled shortcuts.

**T4. Compiler and parameter lemma.**  
Compile at depth \(d=\Theta(\log S)\) with \(n\le S^{20}\), yielding \(d_{\rm NO}/d_{\rm YES}\ge n^{1/500}\).

**Why sufficient.** T1 turns CVP soundness into true homogeneous minima; T2 supplies separated nonisometric factors; T3 gives an all-depth theorem; T4 supplies the polynomial gap.

**Crux.** T1: simultaneously excluding zero and multiple layers without recreating DROP.

**First experiment.** For the rank-eight NAND survivor, compute exact functions
\(\min_{x\in L}\|x-kt\|^2+k^2H^2\) for \(k=0,\pm1,\pm2,\pm3\), solve the rational interval of admissible \(H^2\), and exhaust all vectors through \((17/16)R^2\). An empty interval kills this homogenization.

---

## Complete obstruction audit

- **G1 RS slack, G6 externally filtered quotient, G7 radix kernel:** Q/M/T emit all constraints as lattice coordinates and introduce no free residual slack or external filtering.
- **G2–3 local affine isolation, G5 private-row overlap, G9 degree-two parity, G11 unique-triple parity, G13 honest-affine-span collision, G15 laminar affine lift, G19 signed splicing, Goal G1 diagonal ordered-pair splice, and the fresh toric quadratic exchange:** Q audits the full projected-fiber Markov basis and escapes via noncommutative product tags; M audits all Graver primitives; T requires the same toric audit before tensoring.
- **G12 fingerprint DROP and Goal G8 augmented-Gram DROP:** DROP is explicit in Q1, M1/M3, and T1/T2.
- **G14 pair bags, G28 \(\lambda\le\mu\), G31 Walsh Gram, G32 additive parity, G37 universal parity cut, G38 splitter bags:** no finite pass is treated as amplification; Q3, M3, and T3 each state an all-depth strict-growth theorem.
- **G30 seed isometry:** T2 explicitly forbids it; Q and M are circuit-recursive rather than literal seed tensoring.
- **G33–34 exterior completeness failure, Goal G3 D4 midpoint, Goal G4 D4 Boolean interaction, Goal G5 D4 recombination, Goal G6–7 E6 affine-port:** none of the strategies uses those closed geometric families.
- **Goal G2 \(A_5\) bicyclic zero divisors:** Q uses a division algebra, M is commutative-linear without group rings, and T uses positive-definite lattices.
- **Goal G11 \(\mathbb F_{289}\) grade-zero attack, Goal G12 redundant NAND, and the killed affine COPY frontier:** Q requires a nonzero product initial symbol before valuation theory; M and T do not claim the redundant NAND seed composes unaudited.
- **Carry/lumpability obstruction:** Q2 requires symbolic section stabilization, not a \(P^2\)-only empirical table.

## Recommendation

Attempt **Strategy 1** first.

**FRONTIER lemma:** **Q1, the toric-refined NAND/COPY tile lemma.**

**First experiment:** compute the exact projected-fiber Markov basis of the current seam, identify the `111` exchange generator, and search the smallest quaternion product-tag alphabet modulo \(P^2\) that gives every non-honest primitive move, DROP, and false NAND fiber a nonzero initial symbol.
