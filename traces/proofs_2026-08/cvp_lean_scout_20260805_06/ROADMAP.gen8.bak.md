# ROADMAP.md

I did not consult the prohibited recent document, any mirror, or any discussion of its solutions. The supplied scout discarded a potentially derivative result unread. Only supplied results and independent literature are used.

## Target

Give a deterministic polynomial-time many-one reduction from size-\(S\) 3SAT to Euclidean GapCVP in dimension \(n=\operatorname{poly}(S)\), with

\[
\operatorname{dist}_{\mathrm{NO}}>n^c\operatorname{dist}_{\mathrm{YES}}
\]

for an explicit absolute \(c>0\), without PCPs or unproved conjectures.

## Retired frontier

The pair-supported quaternion-product strategy is retired. Generations 4–5 exposed both enlarged seam kernels and physical-selector flips invisible to every tested channel prefix. No further product-channel, \(P^3\), or carry search is admissible unless a complete full-selector matrix first passes the compatibility and structural-recognition gates below.

---

## Strategy 1 — Full-brick higher-Lawrence recursion and all-coordinate detection

Replace ad hoc transfer channels by a recursion whose complete signed kernel has a depth-independent structural theorem.

### Lemma chain

**L1. Full-brick Lawrence realization lemma.**  
Construct a fixed finite brick configuration \(A_\star\), containing physical NAND/COPY selectors, pair selectors, normalization, glue, DROP and transfer auxiliaries, such that every depth-\(r\) compiler matrix is integrally row/column equivalent to a colored higher Lawrence lifting of \(A_\star\). Formula dependence may occur only through finitely many brick colors, column permutations and targets. All honest encodings have common energy.

**L2. Uniform primitive classification lemma.**  
Using Santos–Sturmfels, compute a constant \(K=g(A_\star)\) such that every Graver element uses at most \(K\) bricks. For every primitive \(g\), prove exactly one of:

1. \(g\) is an honest reassignment difference;
2. its image in a sparse local quotient \(Q\) is nonzero and supported on at most \(K\) brick-coordinate pairs;
3. its anchor energy already exceeds the adverse threshold.

In particular, no low-energy malformed primitive lies in the honest affine-difference lattice. This is the mandatory Generation-13 compatibility gate.

**L3. Full-selector unique-neighbor detector lemma.**  
Instantiate an explicit GUV lossless expander for sparsity \(K\), with left vertices covering every coordinate of \(Q\), including physical selectors. Tensor each unique-neighbor row with a fixed local quotient basis. Then every low-energy malformed primitive has nonzero integral syndrome, while every honest difference has zero syndrome. Conformal Graver decomposition plus the L2 energy alternative yields a cancellation-free adverse witness.

**L4. Lift-independent adverse-transducer lemma.**  
Lift every detector component to its own quaternionic prime channel and construct a finite residue-state transition system. Prove symbolically, for all lifts and carries, section stabilization and a bounded integral potential giving one net \(17\)-adic gain per four binary levels. The resulting unrestricted min-plus recurrence satisfies

\[
\frac{d_{\rm NO}}{d_{\rm YES}}
 \ge (17/16)^{d/8-O(1)}.
\]

DROP, malformed physical states and vector-syndrome cancellation are explicit states.

**L5. Compiler and parameter lemma.**  
Balance the circuit to depth \(d\ge\log_2S-O(1)\), emit all coordinates deterministically, and prove \(n\le S^B\) for an explicit \(B\). Then

\[
d_{\rm NO}/d_{\rm YES}\ge n^c,
\qquad
c=\frac{\log_2(17/16)}{8B}>0,
\]

after hard-coding finitely many small inputs.

**Why sufficient.** L1–L3 replace empirical seam testing by a theorem covering the complete signed kernel and physical flips. L4 supplies all-depth multiplicative growth; L5 converts it to the target reduction.

**Crux.** L1: arbitrary formula wiring must genuinely be a fixed-brick higher Lawrence family, not merely resemble one locally.

**First experiment.** Serialize depth \(1,2,3\) full matrices for one proposed brick, including physical and pair rows. Compute their integer kernels and test the exact identity

\[
\ker A^{(r)}
=\{(u_1,\ldots,u_r):A_\star u_i=0,\ \sum_i u_i=0\}.
\]

Simultaneously compute the honest affine lattice and test every Graver primitive against L2, beginning with the G13 parity, the Generation-4 seam witness, and all Hamming-one/two physical flips.

---

## Strategy 2 — Toric-fibre compiler with complete signed lifting calculus

This fallback permits several fixed tile types, but replaces incomplete old-generator audits by a full higher-codimension lifting theorem.

### Lemma chain

**F1. Finite-type toric compiler lemma.**  
Express the balanced NAND/COPY network as an iterated toric fibre product of finitely many saturated tile types over an explicit common multigrading containing every physical, pair and glue coordinate. Honest fibers have common energy.

**F2. Signed bounded-lifting lemma.**  
Verify the Rauh–Sullivant compatible-projection property and normality for every gluing type. Strengthen the Draisma–Oosterhof bounded Markov-degree conclusion to this compiler’s signed kernel: every Graver element is a conformal composition of at most \(K\) kernel moves, compatible factor lifts and glued moves, for a constant \(K\).

**F3. Complete primitive separation lemma.**  
Enumerate those finitely many move types. Each malformed type must either leave the honest affine lattice, where a full-selector expander detector sees it, or have anchor cost at least \(\gamma E\) for explicit \(\gamma>1\). DROP, Lawrence moves, diagonal splices and physical flips are included.

**F4. Strict recursive cost lemma.**  
Construct unrestricted min-plus tables for all legal and adverse classes and prove

\[
C_{\rm NO}(d)\ge\lambda^d C_0,\qquad
C_{\rm YES}(d)\le\mu^d C_0,\qquad
\lambda/\mu>1.
\]

No shell-restricted or named-attack-only table suffices.

**F5. Parameter lemma.**  
With \(d=\Theta(\log S)\) and \(n\le S^B\), obtain
\(d_{\rm NO}/d_{\rm YES}\ge n^{\log_2(\lambda/\mu)/(2B)}\).

**Why sufficient.** F1–F3 give complete signed soundness under gluing; F4–F5 amplify it polynomially.

**Crux.** F2: bounded Markov degree does not by itself bound unrestricted Graver moves.

**First experiment.** On the smallest three-, four- and five-bag G38 templates, compute normality, compatible projections, complete Markov bases and complete Graver bases. Record Graver type and support by depth. A growing signed move, failed projection property, or surviving honest-affine malformed primitive kills this chain.

---

## Strategy 3 — Exact homogenization, rank-\(\le41\) factors and coset tensor soundness

Retain tensor amplification only with the corrected Kitaoka rank bound and an explicit return to CVP.

### Lemma chain

**T1. Exact layer-forcing lemma.**  
For every affine tile \((L,t)\), compute \(d=\operatorname{dist}(t,L)\) and \(\lambda=\lambda_1(L)\). Choose one rational \(H^2\) satisfying, for every legal and adverse target class,

\[
d^2/3<H^2<\lambda^2-d^2.
\]

Then all relevant nonzero minima of Kannan’s embedding occur in layers \(k=\pm1\); \(k=0\) and \(|k|\ge2\) are strictly longer.

**T2. Formula-sensitive rank-\(\le41\) tile lemma.**  
Construct nonisometric legal/adverse homogeneous factors of rank at most \(41\), common legal minimum \(R\), and adverse factor at least \(\gamma R\), \(\gamma>1\). They must pass the complete signed-kernel, DROP and physical-flip audits.

**T3. Coset tensor soundness lemma.**  
Prove that recursive tensor products preserve the distinguished product layer and that every shortest vector in its affine coset is decomposable. Use Kitaoka E-type decomposability where applicable and a Haviv–Regev-style trace–determinant dichotomy for the remaining coset vectors.

**T4. Affine-slice recovery lemma.**  
Compute a basis for the kernel of the final layer-coordinate homomorphism and a representative of the distinguished layer. Their distance is exactly the amplified coset minimum, yielding one ordinary CVP instance.

**T5. Parameter lemma.**  
For depth \(\Theta(\log S)\), prove polynomial dimension and ratio \(\gamma^{\Theta(\log S)}=n^c\).

**Why sufficient.** T1–T3 produce tensor soundness without assuming all tensors are rank one; T4 returns to many-one CVP; T5 gives the gap.

**Crux.** T3: ordinary E-type minimal-vector decomposability does not automatically control a prescribed affine coset.

**First experiment.** For the rank-eight redundant NAND survivor, compute exact \(d_i^2\) and \(\lambda_1(L)^2\) for all legal, false, DROP and signed fibers, and intersect the rational Kannan intervals. An empty intersection kills this realization before tensor work.

---

## Complete obstruction audit

- **G1 RS slack, G6 filtered quotient, G7 radix kernel:** every strategy emits all constraints; no external filtering or residual-only amplification.
- **G2–3 affine isolation, G5 private overlap, G9 parity, G11 unique-triple parity, G13 affine-span collision, G15 laminar lift, G19 signed flow:** L2, F2–F3 and T2 require complete signed-kernel classification plus an explicit affine-compatibility-or-cost certificate.
- **G12 fingerprint DROP and Goal G8 augmented-Gram DROP:** DROP is explicit in L1/L4, F3/F4 and T1/T2.
- **G14 pair bags, G28 \(\lambda\le\mu\), G31 finite Walsh pass, G32 additive parity, G37 parity cut, G38 splitter bags:** no finite shell is treated as amplification; L4, F4 and T3 are all-depth statements.
- **G30 seed isometry:** T2 forbids coefficient or ambient isometries; L/F are not literal seed tensoring.
- **G33–34 exterior failure; Goal G3–5 D4 midpoint/grid/recombination; Goal G6–7 E6 affine ports:** none reuses those closed geometric families.
- **Goal G1 diagonal ordered-pair splice, Goal G2 \(A_5\) zero divisors, G19 splice:** all are included in signed primitive audits.
- **Goal G11 grade-zero attack, Goal G12 redundant NAND, killed affine COPY frontier, toric quadratic exchange:** no local NAND survivor is composed before complete full-matrix classification.
- **Generation-4 seam witness and Generation-5 physical flip:** detector support explicitly includes pair and physical coordinates.
- **Carry/lumpability obstruction:** L4 requires symbolic lift-independent section stabilization; finite \(P^2/P^3\) tables alone are insufficient.

## Recommendation

Attempt **Strategy 1** first.

**FRONTIER lemma:** **L1, the full-brick Lawrence realization lemma.**

**First experiment:** serialize the complete depth-\(1,2,3\) matrices, verify the exact higher-Lawrence kernel identity over \(\mathbb Z\), and run the honest-affine compatibility audit on all Graver primitives, starting with G13, the seam witness, and physical Hamming-one/two flips.

## Frontier status — Generation 6 synthesis

Both reviews select only marked oblivious Beneš routing (Fable 1 / Pro 1). Its causal mechanism is to keep one fixed routing matrix while formula wiring changes only switch targets; physical and anchor columns may move only by color-preserving signed permutations. The expected move was a marked local normal form suitable for an L1 induction. Falsification was any setting-dependent matrix, unequal legal energy, extra low-weight marked kernel class, honest-affine malformed primitive, or DROP below threshold.

The breaker supplies the operative cheat for the frozen pair-linearized switch brick. Its hash-locked matrix has shape `54x76`. Exact search of 6,560 local signed candidates finds the support-eight primitive `(1,-1,-1,1,1,-1,-1,1)`, with no proper conformal kernel summand. It preserves every emitted row and equals the honest affine difference `h000-h011-h100+h111`. Hence any detector required to vanish on honest differences also misses it. The same movement gives zero-residual malformed energy 92 or 108 versus legal energy 76 in all 384 permutation/input fibers. This finitely kills that switch brick, not every possible full Beneš brick.

The builder's larger target-only local serialization independently exposes another finite failure. Its fixed `136x142` matrix has common legal energy 142 across 384 encodings and blocks physical-only Hamming-one/two kernel changes, but residual scale 5 gives all-zero DROP energy `692<2414=17*142`. Its six local weight-eight switch primitives are quotient-detectable only after using setting-specific forbidden coordinates, so this does not override the breaker's honest-affine collision in the other frozen brick.

`lean/Verify_integral_euclidean_isometry.lean` proves the needed universal marking restriction: a square integer matrix with Gram identity is exactly a signed permutation matrix. Thus arbitrary unimodular column operations cannot preserve Euclidean energy and selector support unless they reduce to signed permutations; residual metrics must be transported explicitly. The theorem proves no Beneš compiler, L1 identity, primitive classification, or hardness result.

L1 remains open. The next experiment must freeze the missing full marked brick, including COPY tree, fanout diamond, three-COPY cycle, NAND, physical/pair/DROP/transfer/anchor rows, and depths 1–3. Before any induction, rerun the exact honest-affine exchange and DROP tests. Any added detector must be shown nonzero on the exchange without violating the required honest-equivalence semantics; otherwise this Beneš mutation fails L2 compatibility even if L1 kernel recognition succeeds.

## Frontier status — Generation 7 synthesis

Only Pro Proposal 2 survives opponent review: replace the killed common-fibre mark by the equal-radius quadratic-character orbit `q(a,b)=(1,(-1)^a,(-1)^b,(-1)^(ab))`. Its local mechanism is genuine: the old mixed rectangle has nonzero quadratic derivative, all four honest words have one radius, and wire swap is a marked coordinate permutation. The expected move was a complete brick with no equal-radius signed ghost. Falsification was any normalized malformed selector or glued cycle primitive at energy at most the legal energy, even after DROP clears threshold.

The breaker finds the earliest cheat. Exhaustive search of `{-1,0,1}^4` finds three support-three normalized ghosts. For example `(-1,1,1,0)` maps to `(1,-1,-1,1)`, a non-honest word of the same squared mark norm 4 as every honest word. Its anchor energy is 12 versus 4. For each of the 65 tested mark scales `m=0,...,64`, normalization is raised to the least integer value making local DROP cost at least `17E`; the ghost remains below `17E`. This finitely kills the frozen local objective, not every augmented brick.

The builder's fuller `74x44` three-COPY-cycle serialization confirms that gluing does not automatically cure the issue. Complete search of all `3^12=531441` COPY movements finds exactly the two signs of a conformally primitive synchronized three-rectangle move. It preserves all physical, character-transport, NAND, transfer, normalization, glue, and DROP rows. In each honest fiber one sign has malformed energy exactly `885`, equal to legal energy, while DROP is `120000>15045=17E`. Thus this hash-locked realization is killed at ratio one despite clearing DROP and physical Hamming-one/two checks.

`lean/Verify_quadratic_character_switch.lean` proves the local positive facts: common squared radius 4, mixed derivative `-2` in the quadratic coordinate, integer linear independence of the four character columns, and marked wire-swap transport. These facts do not exclude signed selectors mapping to a different equal-norm point or synchronized cycle movements, and they prove no L1 identity.

L1 remains open, but this quadratic-character realization is dead. Any changed brick must embed all three support-three ghosts before depth serialization and add rows that charge them while preserving one honest radius. It must then retest synchronized rectangles on the smallest fanout diamond and three-COPY cycle, with DROP above threshold, before any depth-1/2/3 Lawrence audit.
