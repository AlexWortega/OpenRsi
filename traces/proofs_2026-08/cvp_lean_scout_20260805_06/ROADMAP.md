# ROADMAP.md

I did not consult the prohibited recent document, any mirror, summary, coverage, or discussion of its solutions. The literature scout reports that none of its inspected sources concerned that document.

## Target

Give a deterministic polynomial-time many-one reduction from size-\(S\) 3SAT to Euclidean GapCVP in dimension \(n=\operatorname{poly}(S)\), with

\[
\operatorname{dist}_{\mathrm{NO}}>n^c\operatorname{dist}_{\mathrm{YES}}
\]

for an explicit absolute \(c>0\), without PCPs or unproved conjectures.

## Retired frontier

The full-brick higher-Lawrence frontier is retired as the primary route. Two consecutive mutations failed before structural induction:

- the marked Beneš brick has an honest-affine primitive toric exchange and a separate cheap DROP;
- the quadratic-character repair has equal-radius support-three ghosts and a synchronized three-COPY-cycle primitive at legal energy.

No further fixed-brick, Beneš, character-orbit, product-channel, or Markov-only mutation is admissible without first passing the new tractability and full signed-kernel gates.

---

## Strategy 1 — Universal-circuit topology with growing separators and defect expansion

Replace the fixed higher-Lawrence family by a programmable universal topology whose nonlocal separator system deliberately falls outside known fixed-block convex integer-optimization classes.

### Lemma chain

**U0. Known-class tractability-exclusion lemma.**  
For the actual factor \(C_S\), form

\[
D_S=[I\; -C_S],\qquad
\min\{\|y-t_S\|_2^2:D_S(y,z)=0,\ (y,z)\in\mathbb Z^N\}.
\]

Prove that no marked row/column permutation, finite color refinement, or bounded-width auxiliary equality expansion puts \(D_S\) into fixed-block \(n\)-fold, generalized \(n\)-fold, tree-fold, or two-stage form. Give an explicit invariant—such as unbounded separator rank or unbounded marked neighborhood diversity—witnessed by the growing detector graph. This excludes direct application of Hemmecke–Onn–Weismantel convex minimization; it does not claim impossibility of every extended formulation.

**U1. Programmable universal-compiler lemma.**  
Compile a balanced NAND/COPY formula into a Valiant-style universal circuit of polynomial size. Program data changes only targets and marked finite-type supernodes. Unfold local computation into a balanced staged-tree core, while repeated-variable and reconvergence constraints are emitted through explicit growing separator/expander rows. Every honest encoding has common Euclidean energy, and zero/DROP is charged above the adverse threshold.

**U2. Low-energy defect-localization lemma.**  
Use assignment selectors on the staged-tree nodes and separator selectors on reconvergent interfaces. Prove that every unrestricted integral vector below threshold is either honest or induces a nonzero defect on a connected set of at most \(K\) interfaces. The proof must cover honest-affine combinations: increasing-arity separator selectors must force the G13/G11 pseudodistribution to pay energy rather than relying on a compatible linear syndrome.

**U3. Complete detector and recurrence lemma.**  
Apply an explicit lossless expander to all physical, separator, normalization and DROP coordinates. Enumerate every localized signed defect class and derive unrestricted min-plus recurrences

\[
C_{\rm NO}(d)\ge \lambda^d C_0,\qquad
C_{\rm YES}(d)\le \mu^d C_0,\qquad \lambda/\mu>1.
\]

Chordal/staged-tree quadratic Markov generation may organize the enumeration, but full Graver or equivalent signed classification is mandatory.

**U4. Parameter lemma.**  
Prove \(d\ge \log_2 S-O(1)\), \(n\le S^B\), and deterministic polynomial emission. Then

\[
\frac{d_{\rm NO}}{d_{\rm YES}}
\ge(\lambda/\mu)^{d/2-O(1)}
\ge n^c,\qquad
c=\frac{\log_2(\lambda/\mu)}{3B}>0.
\]

**Why sufficient.** U0 avoids the new algorithmic trap; U1 gives formula-oblivious compilation; U2–U3 establish unrestricted signed soundness and growth; U4 converts depth into a polynomial gap.

**Crux.** U2: reconvergence must remain polynomial-size while destroying honest-affine pseudodistributions and cycle primitives.

**First experiment.** Serialize universal-circuit cores of sizes \(8,16,32\), including fanout, reconvergence, physical selectors and DROP. Compute marked separator-rank/neighborhood invariants for U0. On the smallest reconvergent core, exhaust support-\(\le12\) signed vectors, beginning with the G13 affine collision, Beneš exchange, three quadratic ghosts and synchronized COPY-cycle witness.

---

## Strategy 2 — Variable-parameter transportation compiler with all-coordinate amplification

Use transportation universality rather than fixed local switching. Its dimensions grow with the formula, avoiding the unsupported fixed-brick premise.

### Lemma chain

**P1. Transportation realization lemma.**  
Transform bounded \(0/1\) 3SAT feasibility into a slim \(r\times c\times3\) integer transportation system in polynomial time, preserving integral feasible points by explicit projection. Add anchor and target coordinates so all honest Boolean tables have one energy \(E_S\).

**P2. Signed transportation separation lemma.**  
Augment the line-sum system with polynomially many joint-marginal coordinates of increasing arity. Prove that every unrestricted non-honest table either violates an emitted coordinate or has anchor energy at least \(\gamma E_S\), \(\gamma>1\). The proof must classify the relevant transportation Graver circuits directly; bounded Markov degree is not evidence for bounded Graver complexity.

**P3. Variable-parameter amplification lemma.**  
Recursively compose transportation instances using dimensions \(r_d,c_d\) that grow polynomially with depth. Establish a complete adverse-state recurrence with \(\lambda/\mu>1\), including carries, DROP, signed splices and affine mixtures. The growing transportation parameter is essential and must not collapse to a fixed \(n\)-fold block.

**P4. CVP and parameter lemma.**  
Emit an integer factor and target realizing the full quadratic objective exactly, prove rank and bit length polynomial, and derive \(n^c\) as in U4.

**Why sufficient.** P1 supplies a target-driven universal compiler; P2 gives unrestricted soundness; P3 amplifies it; P4 produces ordinary CVP.

**Crux.** P2: transportation systems naturally contain large signed cycle spaces, and the added marginals must defeat them without exponential size.

**First experiment.** Apply the explicit slim transportation construction to the eight-clause three-variable obstruction and the nine-clause G13 instance. Compute complete Graver bases where feasible, compare them with Markov bases, and search the exact shell through \(17E\) for affine parity, DROP and cycle attacks.

---

## Strategy 3 — Low-rank gate factors and affine-coset tensor soundness

Abandon linear transfer channels and amplify through recursively tensorized gate factors, but only after exact layer forcing and coset—not merely lattice—decomposability.

### Lemma chain

**T1. Exact homogenization lemma.**  
For every NAND/COPY factor \((L,t)\), compute \(d=\operatorname{dist}(t,L)\) and \(\lambda_1(L)\), and choose rational \(H^2\) satisfying simultaneously

\[
d^2/3<H^2<\lambda_1(L)^2-d^2.
\]

Then every relevant Kannan-embedding minimum lies in layer \(k=\pm1\); \(k=0\), \(|k|\ge2\), and DROP are strictly longer.

**T2. Rank-\(\le41\) nonisometric gate-factor lemma.**  
Construct legal and adverse homogeneous NAND/COPY factors of rank at most \(41\), common legal minimum \(R\), and adverse minimum at least \(\gamma R\), \(\gamma>1\). They must pass complete unrestricted audits for physical flips, affine collisions, diagonal splices, equal-radius ghosts and COPY cycles.

**T3. Affine-coset tensor theorem.**  
For the balanced gate recursion, prove every shortest vector in the distinguished tensor coset is decomposable. Use Kitaoka E-type decomposability only where applicable and a trace–determinant bound for remaining coset vectors. Conclude depth-\(d\) ratio at least \(\gamma^d\).

**T4. CVP recovery and tractability gate.**  
Compute the kernel of the final layer homomorphism and a coset representative, obtaining one ordinary CVP instance. Verify that its dense tensor factor does not admit the fixed-block formulation excluded in U0. Prove dimension \(\rho^d=S^{O(1)}\) and \(c=\log_\rho\gamma>0\).

**Why sufficient.** T1–T3 give rigorous tensor amplification without a rank-one assumption; T4 returns to many-one CVP with polynomial dimension.

**Crux.** T3: E-type minimal-vector results do not automatically control a prescribed affine coset.

**First experiment.** For the rank-eight redundant NAND survivor, compute exact \(d^2\) and \(\lambda_1^2\) for every legal, false, DROP and signed fiber and intersect all Kannan intervals. If nonempty, tensor two copies and enumerate the complete distinguished coset through \(\gamma^2R^2\).

---

## Complete obstruction audit

- **G1 RS slack, G6 filtered quotient, G7 radix kernel:** every strategy emits the complete objective; no residual-only amplification or external filtering.
- **G2–3 affine isolation, G5 private overlap, G9 parity, G11 unique-triple parity, G13 affine-span collision, G15 laminar lift, G19 signed flow:** U2, P2 and T2 require unrestricted signed and honest-affine audits.
- **G12 fingerprint DROP and Goal G8 augmented-Gram DROP:** zero/DROP is explicit in U1–U3, P2–P3 and T1–T2.
- **G14 pair bags, G28 \(\lambda\le\mu\), G31 finite Walsh pass, G32 additive parity, G37 parity cut, G38 splitter bags:** only all-depth strict recurrences count.
- **G30 seed isometry:** T2 requires nonisometry; U/P do not tensor a seed.
- **G33–34 exterior failure; Goal G3–5 D4 midpoint/grid/recombination; Goal G6–7 E6 ports:** none reuses these families.
- **Goal G1 diagonal splice, Goal G2 \(A_5\) zero divisors, G19 splice:** mandatory signed classes in U3, P3 and T2–T3.
- **Goal G11 grade-zero attack, Goal G12 redundant NAND, affine COPY frontier, toric quadratic exchange:** no local survivor is composed before full-factor classification.
- **Generation-4 seam, Generation-5 physical flip, Generation-6 Beneš exchange/marking, Generation-7 support-three ghosts/COPY cycle:** all named witnesses seed the first shell audits.
- **Carry/lumpability obstruction:** any finite-state recurrence must quantify over all lifts and carries.
- **Fixed-block tractability obstruction:** U0/T4 are mandatory; P3 must retain a growing parameter.
- **Markov-versus-Graver obstruction:** Dobra, staged-tree and Rauh–Sullivant results may organize Markov moves only; full signed primitives are computed independently.

## Recommendation

Attempt **Strategy 1** first.

**FRONTIER lemma:** **U0, the known-class tractability-exclusion lemma.**

**First experiment:** serialize size-\(8,16,32\) universal-circuit factors, form \(D_S=[I\; -C_S]\), test marked fixed-block/tree-fold/two-stage recognition, and measure whether the proposed growing separator graph supplies an explicit unbounded invariant.

## Frontier status — Generation 8 synthesis

Both reviews retain only the incidence-separator/treewidth route (Fable 2 / Pro 2) for one bounded U0 experiment. Its causal mechanism is that a growing marked support minor survives identity augmentation and faithful equality expansion, while each precisely defined fixed-template class should have template-bounded width. The expected move was finite evidence authorizing separate class-side closure theorems. Falsification was a bounded-width decomposition, failed faithful contraction, or failure of the predeclared separator growth gate.

The builder's frozen affine-detector surrogate passes its finite gates. For `S=8,16,32`, two independent exact MILP backends give top-level `2/3`-balanced separator optima `4,6,9`, strictly increasing and at least `S/4`. One-subdivision equality expansions contract back to each graph. Exact sparse signed search covers 654,384 defects modulo global sign and finds detector image energy at least support in the searched ranges. This is not the requested hereditary recursive separator profile, an actual U1 universal-circuit serializer, a fixed-class bound, U0, or an asymptotic theorem.

The breaker's synthetic control is the operative warning about overinterpreting support growth. For cumulative matrices at `n=8,16,32`, `D=[I|-C]` contains certified `K_{n/2,n/2}` support subgraphs while also admitting a support-two boundary kernel move, `n-1` support-three internal moves, and a unimodular row rebasing whose incidence graph is a tree. This does not refute the builder's different affine-detector family, and row rebasing is not automatically an allowed U0 transformation. It does prove that a large displayed support witness alone supplies neither signed soundness nor a row-basis-robust tractability exclusion.

`lean/Verify_support_minor_channel.lean` proves the universal plumbing that is actually established: the support graph of `C` is an induced subgraph and explicit minor of the support graph of `[I|-C]`; identity columns are leaves; and any equality expansion equipped with an onto collapse, internally connected fibers, and lifted old edges yields a branch-set minor model. It proves no separator growth, treewidth monotonicity theorem, fixed-class upper bound, or U0 statement.

U0 remains open. The next experiment must replace the surrogate by hash-frozen actual `C_8,C_16,C_32` universal-circuit serializers and formal U0 grammars. It must compute the hereditary recursive separator profile, emit faithful contraction certificates for every allowed equality gadget, search bounded row rebasings and reusable decompositions, and test each of the four class-side width claims separately. Three finite sizes remain only finite evidence until serializer growth and class closure are proved in Lean.
