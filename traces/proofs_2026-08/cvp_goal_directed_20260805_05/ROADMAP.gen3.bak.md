Below, \(m\) is the 3SAT size and \(n\) the rank of the emitted lattice. All searches must optimize over unrestricted integer coefficients; no consistency condition may remain external.

## Strategy 1 — Tensor-coherent lift of a width-5 branching program

Use Barrington’s width-5 construction directly, not as a PCP: a balanced Boolean formula of size \(\operatorname{poly}(m)\) becomes a width-5 permutation branching program of length \(L=\operatorname{poly}(m)\) [Barrington, JCSS 38 (1989)].

### Lemmas

1. **Deterministic evaluator lemma.**  
   In polynomial time, transform \(F\) into a width-5 program \(P_F\) with \(L=\operatorname{poly}(m)\) labeled layers such that a consistent assignment induces exactly one path, and that path reaches ACCEPT iff it satisfies \(F\).

2. **Integral \(k\)-coherent lift lemma.**  
   For every \(k\), construct a Euclidean CVP instance with \(O(L\,10^k)\) columns whose variables describe ordered \(k\)-tuples of transitions. Emit all transition, marginal, repeated-query, source, and ACCEPT equations. Honest paths have a common squared distance \(R_k^2\). No condition is enforced outside the lattice.

3. **FRONTIER — signed-flow amplification lemma.**  
   For \(k\ge1\), if \(P_F\) has no accepting consistent path, then every unrestricted integral accepting \(k\)-flow \(z\) satisfies
   \[
   \|C_kz-y_k\|_2^2\ge (4/3)^kR_k^2.
   \]
   Equivalently, any accepting signed splice either contains an honest accepting path in its integral decomposition or its tensor-coherence energy grows by at least \(4/3\) per level.

4. **Polynomial-gap realization lemma.**  
   Take \(k=\lfloor\log_2L\rfloor\). Then
   \[
   n=O(L10^k)\le L^{1+\log_2 10+o(1)}
   \]
   while the distance gap is at least \((4/3)^{k/2}\). Thus one may take
   \[
   c=\frac{\log_2(4/3)}{2(1+\log_2 10)}-o(1)>0.047.
   \]
   Padding handles small instances and makes, for example, \(c=1/50\) explicit.

**Why sufficient.** Lemmas 1–2 give deterministic completeness; Lemma 3 gives soundness against every integer vector; Lemma 4 converts exponential-in-\(k\) coherence into polynomial-in-\(n\) GapCVP hardness.

**Crux.** Proving Lemma 3 without silently assuming rank-one or nonnegative flows.

**First experiment.** Construct the \(k=2\) lift of the smallest Barrington program exhibiting the Generation-19 two-negative accepting splice. Exact MILP/DP should compute the unrestricted accepting-fiber minimum and test whether it is at least \(4R_2^2/3\). Reconstruct any violating vector.

---

## Strategy 2 — A coercive finite-state gate tile and min-plus recursion

Replace path flows by a balanced circuit assembled from a single, exhaustively certified integer tile.

### Lemmas

1. **Balanced bounded-degree circuit lemma.**  
   Deterministically convert \(F\) to an equivalent fan-in-two circuit of depth \(d=O(\log m)\), size \(m^{O(1)}\), with explicit COPY gates for repeated inputs.

2. **FRONTIER — coercive tile lemma.**  
   Construct one integer Euclidean tile with at most \(D=4096\) selector columns and a finite complete port classification—LEGAL, FALSE, DROP, AFFINE, SPLICE, and MALFORMED—and a rational potential \(\Phi\) such that:
   - every legal gate configuration has cost at most \(\mu\);
   - every composition whose output falsely claims legality satisfies
     \[
     E_{\rm parent}+\Phi_{\rm out}
       \ge \frac{33}{32}\mu^{-1}
          \sum_{\rm children}(E_i+\Phi_i);
     \]
   - the inequality covers every integral port vector, not merely a bounded named family;
   - honest configurations all have equal radius.

3. **Recursive soundness lemma.**  
   Complete min-plus composition of certified tile tables preserves the coercive inequality. If the root claims TRUE for an unsatisfiable circuit, some adverse leaf-to-root chain yields squared-distance ratio at least \((33/32)^d\).

4. **CVP compilation lemma.**  
   Glue copies only through emitted equality rows and clear denominators. With \(n\le m^3D^d\), the distance gap is \(n^c\), where
   \[
   c=\frac{\log_2(33/32)}{2(3+\log_2D)}>1/700.
   \]

**Why sufficient.** The circuit represents arbitrary 3SAT; the all-integral transfer inequality supplies induction through logarithmic depth; the last lemma gives an ordinary many-one Euclidean CVP instance.

**Crux.** Finding a tile with strict adverse growth after accounting for every malformed interface state.

**First experiment.** Enumerate complete unrestricted transfer tables for one NAND/COPY tile and its depth-two composition. Search small integral factors \(C=[aI;bA]\), \(a,b\le12\), and bounded auxiliary-port designs. Reject unless exact tables certify \(\lambda/\mu\ge33/32\), including DROP, affine-parity, and two-negative splice states.

---

## Strategy 3 — Splitter bags with norm-expanding extension

Scale Generation 38 by using logarithmic clause bags and an extension theorem, rather than extrapolating its finite shell.

### Lemmas

1. **Deterministic splitter hierarchy lemma.**  
   Construct in polynomial time levels \(\mathcal B_0,\ldots,\mathcal B_t\), \(t=\lfloor\log_2m\rfloor\), of clause bags, each containing \(O(t)\) clauses and each having at most \(2^{O(t)}=\operatorname{poly}(m)\) assignments. Every support of at most \(2^i\) defective bags is isolated by some level-\(i\) parent. Classical deterministic splitter families may be used [Naor–Schulman–Srinivasan, FOCS 1995].

2. **Exact bag-lattice lemma.**  
   Give each bag selectors only for assignments satisfying all its clauses; emit normalization and complete parent-child marginal rows. Honest global assignments have equal squared radius, and the total rank is polynomial.

3. **FRONTIER — signed-extension growth lemma.**  
   For every normalized integral family of bag distributions satisfying all emitted marginals, either it is induced by a global satisfying assignment or, at some level,
   \[
   \sum_{B\in\mathcal B_{i+1}}\|z_B\|_2^2
      \ge \frac{17}{16}
         \sum_{B\in\mathcal B_i}\|z_B\|_2^2.
   \]
   The same conclusion, with larger cost, holds if any emitted residual is nonzero.

4. **Iteration and gap lemma.**  
   Iterating Lemma 3 for \(t=\Theta(\log m)\) gives squared-distance ratio \((17/16)^t\). If each level expands rank by at most \(64\) and preprocessing costs \(m^3\), then
   \[
   c=\frac{\log_2(17/16)}{2(3+\log_2 64)}>1/210.
   \]

**Why sufficient.** Unsatisfiability rules out the first branch of Lemma 3; logarithmic norm growth gives a polynomial approximation gap while all bags remain polynomial-sized.

**Crux.** Signed local distributions may extend through every overlap despite having no global probability interpretation.

**First experiment.** Compose two copies of the Generation-38 12-bag system using every splitter-prescribed parent bag. Compute exact min-plus tables through the claimed \(17/16\) threshold, explicitly seeding the Generation-13 affine vector, clause drops, and the cheapest zero-residual signed lift.

---

## Obstruction audit for every chain

| Named obstruction | Required escape in all three strategies |
|---|---|
| **G1 RS slack cheat** | No free integer slack; soundness charges selector/flow norm even at zero residual. |
| **G2 affine/Graver isolation; G3 unbounded fiber audit** | No inference from bounded local isolation; each frontier lemma quantifies over all integers. |
| **G5 private-row overlap failure** | Full tuple ports, complete tile ports, or complete bag marginals are included in the composition theorem. |
| **G6 invalid filtered quotient** | Normalization and consistency are emitted lattice rows; experiments search unrestricted vectors. |
| **G7 radix zero kernel** | No residual-only radix amplification; exact residual kernels remain subject to norm growth. |
| **G9 degree-two parity; G11 cubic parity** | Parity states are explicit adverse states in each frontier lemma and first experiment. |
| **G12 clause drop** | DROP is included in normalization and transfer/growth inequalities. |
| **G13 affine collision** | Enlarged tuple/bag encodings are nonlinear lifts; the theorem must charge their exact affine lifts. |
| **G14 pair-bag finite pass** | S3 proves logarithmic extension growth; S1–S2 use different global mechanisms. |
| **G15 laminar zero-residual lift** | Zero-residual signed pseudodistributions are explicitly covered. |
| **G19 signed flow** | S1 directly lifts the splice; S2–S3 classify it as adverse. |
| **G28 min-plus growth failure** | S2 advances only after exact \(\lambda>\mu\); S1/S3 do not reuse that tile. |
| **G30 tensor seed isometry** | S1 is not literal seed tensoring and must first distinguish ACCEPT from rejection; no rank-one assumption. |
| **G31 finite Walsh pass** | No finite ratio is extrapolated without a growth lemma. |
| **G32 additive parity; G37 universal parity cut** | Compatible parity copies must satisfy the strict frontier inequality; orthogonal additive coupling is not used. |
| **G33 bivector incompleteness; G34 metric-repair infeasibility** | Completeness uses orthogonal one-hot anchors, not exterior tags or a synthesized Gram metric. |
| **G38 finite splitter pass** | S3’s new content is precisely the missing scaling law; S1–S2 make no extrapolation from G38. |

## Recommendation

Attempt **Strategy 1** first: it targets the strongest concrete obstruction, Generation 19, and has the smallest state space and best prospective exponent.

**FRONTIER lemma:** the signed-flow amplification lemma.

**First experiment:** exact unrestricted optimization of the \(k=2\) tensor-coherent lift of the smallest two-negative accepting splice, testing the \(4/3\) squared-gap threshold.

## Frontier status — goal-directed Generation 1

**Finite counterexample for the frozen linear pair lift; FRONTIER remains unproved.** Fable proposal 1 was the best cross-review survivor. Its causal mechanism was closure of the G19 signed splice under layerwise moments; the expected move was a zero-residual `k=2` point below the displayed `16R_2^2/9` bound (also compared with the weaker `4R_2^2/3` test), and that point was the falsification condition.

`experiments/verify_k2_barrington_tensor_splice.py` emits the full ordered-pair and unary flow/marginal/query system plus strong off-diagonal-zero and diagonal-idempotence rows. The pure tensor is blocked by 14 diagonal rows, but `diag(s)` for the exact G19 two-negative flow satisfies all 348,451 rows. Its cost is 224,330 against exact control `R_2^2=224282`, far below both thresholds. This finite result kills this explicit linear realization; it neither computes the `k=2` optimum nor rules out a genuinely different enlarged construction.

### Goal-directed Generation 2

**Finite counterexample for the frozen `A5` fusion tile; both FRONTIER lemmas remain unproved.** Only Fable proposal 3 survived as an authorized experiment. Its causal mechanism was strict energy growth under complete nonabelian multiplication; its expected move was a `33/32` depth-two certificate for some `C=[aI;bA]`, and an unrestricted legal-boundary virtual product below that ratio was the falsifier.

`experiments/verify_a5_bicyclic_fusion_attack.py` emits three complete 3,600-selector multiplication tiles. A bicyclic `x in Z[A5]` satisfies `x^2=0`; the virtual units `1+x` and `(1-x)ACCEPT` produce a zero-residual false ACCEPT composition from four identity leaves. Its cost is `10936a^2` against exact matched-control radius `10800a^2`, and `32*10936 < 33*10800`, so all 144 tested `(a,b)` pairs fail. This finite result kills the explicit tile, not arbitrary nonabelian constructions. The next proposal must specify a uniform coercifier that blocks both the G19 diagonal map and integral group-ring units before another growth claim is tested.
