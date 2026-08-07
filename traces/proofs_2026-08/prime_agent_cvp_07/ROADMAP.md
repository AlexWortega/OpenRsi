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

**U0a. Serializer-and-grammar lemma (new frontier).**  
Before any class exclusion, emit one hash-frozen family of actual factors
\(C_{S,F}\) for the U1 universal compiler, with formula dependence \(F\)
restricted exactly to declared targets/marks.  Define the row and column marks,
the uniform fixed-template quantifiers for each candidate class, the support
or column-matroid convention, and every allowed auxiliary equality gadget.
The grammar must say whether semantically free unimodular row rebasing is
allowed; a claim of algorithmic exclusion must handle it rather than silently
freeze an equation basis.

**U0b. Basis-robust known-class exclusion lemma (after U0a/U1).**  
For the emitted factor form

\[
D_{S,F}=[I\; -C_{S,F}],\qquad
\min\{\|y-t_{S,F}\|_2^2:D_{S,F}(y,z)=0,\ (y,z)\in\mathbb Z^N\}.
\]

Prove, separately for fixed-block \(n\)-fold, generalized \(n\)-fold,
tree-fold, and two-stage matrices, that no transformation in the precise U0a
grammar produces a uniform fixed-template presentation.  The invariant must
be unchanged both by invertible integral left equation operations and by
right-unimodular lattice-basis changes `C -> C Q`.  Exact counterexamples now
exclude the column matroid/circuit/branch-width of one systematic `D` as such
an invariant.  U0b therefore needs a genuinely lattice-intrinsic decomposition
width of the embedded image `C Z^n`, plus objective-preserving certificates for
auxiliary gadgets.  This excludes only the named direct algorithms.

The former U0 is retired as a sufficient tractability-exclusion lemma.  It
referred to an undefined “actual” \(C_S\), left all four grammars and their
uniform quantifiers unspecified, and omitted kernel-preserving row rebasing.
Exact counterexamples in the current frontier status below kill both suggested
raw invariants as general class-side/basis-robust criteria.

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

**Why sufficient.** U0a makes the compiler and transformation grammar well-defined; U1 emits the formula-oblivious factor; U0b then excludes the named algorithmic trap in a row-basis-robust way. U2–U3 establish unrestricted signed soundness and growth; U4 converts depth into a polynomial gap.

**Crux.** U0a is now first: without an actual serialized factor and precise grammars, neither U0b nor the original U2 soundness statement has a quantified object. The later mathematical crux remains U2: reconvergence must remain polynomial-size while destroying honest-affine pseudodistributions and cycle primitives.

**First experiment.** Extend the hash-frozen width-`8,16,32` factors to a total deterministic `Serialize(S,F)` with canonical formula encoding, padding, polynomial dimension/bit bounds, and a verified compiler from balanced NAND/COPY formulas to target bits.  Use the exact grammars in `U0_GRAMMARS.md`.  Search both left row and right lattice-basis rebasings.  Any future U0b invariant must belong to the embedded lattice image, not the column matroid of one chosen basis.  On the smallest reconvergent core, classify the certified additive-2 affine ghost together with G13, Beneš and COPY-cycle witnesses.

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
Compute the kernel of the final layer homomorphism and a coset representative, obtaining one ordinary CVP instance. Verify that its dense tensor factor does not admit the fixed-block formulation excluded in U0b. Prove dimension \(\rho^d=S^{O(1)}\) and \(c=\log_\rho\gamma>0\).

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
- **Fixed-block tractability obstruction:** U0a/U0b/T4 are mandatory; P3 must retain a growing parameter.
- **Markov-versus-Graver obstruction:** Dobra, staged-tree and Rauh–Sullivant results may organize Markov moves only; full signed primitives are computed independently.

## Recommendation

Attempt **Strategy 1** first, but in dependency order.

**FRONTIER lemma:** **U0a, the serializer-and-grammar lemma.**

**First experiment:** formalize the generic butterfly formula compiler in
Lean: formula evaluation, unique-variable sources, COPY fanout, swap routing,
NAND consumption, cleanup, fixed targets, and polynomial emission.  Then add a
width-16 randomized/exhaustive finite stress suite.  Test both left row
rebasing and right-unimodular lattice-basis changes.  Do not use raw support or
chosen-basis column-matroid invariants for U0b.

## Frontier status — Generation 9 reroute

The former U0 edge is retired as a sufficient known-class
tractability-exclusion lemma.  This is not a proof that the eventual actual
factor belongs to any tractable class: no actual factor has yet been emitted.
The edge is killed because its two proposed raw invariants do not support its
claimed general inference, and because the object and transformation grammars
were undefined.

The class-side counterexample is exact.  For the fixed one-by-one n-fold
template \(A_1=A_2=[1]\), the standard \(n\)-fold matrix and its systematic
identity augmentation \(D=[I|-C]\) are trees of treewidth one with a
size-one balanced separator, yet their standard color-aware neighborhood
counts at \(n=8,16,32\) are respectively `17,33,65` for \(C\) and
`26,50,98` for \(D\).  Thus unbounded ordinary marked neighborhood diversity
is not a fixed-block n-fold exclusion.  This is certified by
`experiments/verify_gen8_neighborhood_diversity_nfold_counterexample.py`.
`lean/Verify_two_stage_neighborhood_counterexample.lean` gives the universal
companion: even the fixed two-stage template \(A=B=[1]\) has \(n\) pairwise
distinct scenario-row open neighborhoods.

Displayed support width is also not equation-basis robust.  For every size,
`lean/Verify_row_rebasing_support_failure.lean` proves that the cumulative
systematic matrix \([I|-C_n]\) contains an explicit \(K_{m,m}\) when
\(n=2m\), while invertible integral first differences send it exactly to a
lower-bidiagonal block plus \(-I\), with row support at most three; prefix
sums are the inverse.  `lean/Verify_row_rebasing_kernel.lean` separately
proves that invertible integral left rebasing preserves the integer kernel.
Hence such preprocessing changes neither feasible coefficient vectors nor
their Euclidean objective.

A finite fixed-class stress test gives the same warning from the other side.
`experiments/verify_u0_fixed_nfold_support_counterexample.py` starts with the
literal fixed n-fold template \(A_1=A_2=[1]\).  At `n=8,16,32`, a cumulative
unimodular row presentation has complete-bipartite displayed supports
`K_{9,8}`, `K_{17,16}`, `K_{33,32}` and exact `2/3`-balanced separators
`6,11,22`; the explicit difference inverse returns the fixed n-fold matrix.
This verifier also confirms ordinary colored neighborhood counts
`17,33,65` and primal cliques of orders `8,16,32`.

These certificates do **not** prove that the Generation-8 affine detector is
row-equivalent to a fixed-template class, and row rebasing was not listed in
the former restricted grammar.  They instead kill the assertion that the
former test, by itself, excludes direct tractability preprocessing.  The
surviving minor plumbing in `lean/Verify_support_minor_channel.lean` remains
valid only for a frozen row basis and explicitly faithful connected-fiber
expansions.

The reroute is therefore mandatory: U0a must first emit the actual compiler
factor and precise uniform grammars.  Only afterward may U0b seek a lattice-image-intrinsic decomposition invariant
and prove four separate class bounds; Generation 10 below kills the initially
suggested chosen-basis column-matroid repair.  The next finite run must serialize actual
cores, not another surrogate.


## Frontier status — Generation 10 finite U0a serializer and basis correction

U0a now has its first actual numerical artifacts.  The verifier
`experiments/verify_u0a_universal_topology_serializer.py` emits complete sparse
integer factors `C` and systematic matrices `D=[I|-C]` at widths `8,16,32`.
The fixed butterfly-style topology contains programmable source modes,
COPY/NAND/constant gates, fanout, explicit two-step reconvergence diamonds,
normalization/DROP guards, redundant dyadic edge sums, output rows, and one
physical identity row per selector.  Program dependence is confined to `0/1`
target coordinates.  Three honest programs per width are checked against the
actual `C,D`, with squared energies `72,176,416`.  The canonical JSON artifacts
are frozen under SHA256
`9d8e9251...20b`, `82eb6225...5d01`, and `b0cd6e7c...5652`.
This is finite serialization and completeness only, not an all-size compiler.

`U0_GRAMMARS.md` now separates growing IDs from a fixed finite structural-color
alphabet and gives explicit campaign grammars for fixed-template n-fold,
finite-type generalized n-fold, fixed-depth tree-fold, and finite-type
two-stage matrices.  Its semantic closure includes left equality rebasing,
right-unimodular lattice-basis changes, and only objective-preserving auxiliary
bijections.  Thus the former undefined grammar blocker is narrowed, but U0a
still lacks total `Serialize(S,F)`, formula compilation, uniform polynomial
bounds, and an all-size rank/completeness theorem.

The frozen factor contains a mandatory localized adverse state.
`experiments/verify_u0a_serialized_gate_kernel_cheat.py` proves that the affine
rectangle `(+1,-1,-1,+1)` cancels every nonphysical row at all three frozen
widths.  Physical identity rows contain zero-cost kernel cheating, but adding
the rectangle to an honest vector changes energy only
`72->74`, `176->178`, and `416->418`.  This is finite additive-two evidence,
not an asymptotic theorem or soundness kill; U2/U3 must explicitly charge it.
The generic unanchored switch collision is independently checked by
`experiments/verify_u0a_switch_span_cheat.py`.

The frozen topology is not yet universal even at its declared sizes.
`experiments/verify_u0a_frozen_depth_obstruction.py` proves that its dependency
DAG has only `8,10,12` gate stages, so strict NAND chains of lengths `9,11,13`
have zero order-preserving stage embeddings.  The all-size repair must add a
polynomial number of repeated computation stages and prove a compiler; hashes
alone cannot discharge U0a.

The first proposed U0b repair—column-matroid connectivity of systematic
`D`—is itself killed as a lattice-intrinsic invariant.  The sorry-free theorem
`lean/Verify_right_unimodular_lattice_image.lean` proves that `C` and `C Q`
have exactly the same integer lattice image and the same attainable values for
every output-only objective whenever `Q` is integrally invertible.  Yet
`experiments/verify_right_unimodular_column_matroid_failure.py` exhaustively
computes different, nonisomorphic column matroids for `[I|-I_2]` and
`[I|-Q]`.  The larger controls in
`experiments/verify_u0b_right_basis_circuit_failure.py` show fundamental
circuit support changing from `2` to `9,17,33` for the same lattice at
`n=8,16,32`.  `lean/Verify_column_matroid_grammar.lean` remains useful only for
left row rebasing and column permutations; it cannot cross a general right
basis change.

**Generation-10 frontier:** extend the shallow finite factors to parameterized
depth and a formula compiler.  Generation 11 below supplies the executable
construction and finite audits; the remaining U0a frontier is its universal
Lean correctness theorem and canonical all-instance interface.


## Frontier status — Generation 11 parameterized depth and finite formula compiler

The depth obstruction has an explicit polynomial-size repair.  The serializer
now accepts any power-of-two width `w` and positive depth `d` while preserving
the three frozen default artifacts.  `experiments/verify_u0a_parameterized_depth_chain.py`
checks actual factors at `(w,d)=(4,5),(8,9),(16,17),(32,33)` and compiles
repeated NAND chains to fixed all-one outputs.  Exact dimensions agree with

`k = 4w + 20wd`, `m = 30wd + 9w - 2d`.

The sorry-free file `lean/Verify_u0a_serializer_dimensions.lean` proves these
formulas universally, proves explicit quadratic bounds `k<=24(w+d+1)^2`,
`m<=39(w+d+1)^2`, `m+k<=63(w+d+1)^2`, and proves a strict chain fits exactly
when its depth is at most `d`.  This removes the shallow-chain blocker without
claiming universality or soundness.

Finite routing evidence now covers the relevant mechanism.  Exhaustive
`experiments/verify_u0a_two_cycle_permutation_routing.py` shows that two
butterfly cycles realize all `4!` and `8!` coordinate permutations and checks a
reversal program in the actual `C,D`.  Conversely,
`experiments/verify_u0a_repeated_butterfly_routing_obstruction.py` proves the
default width-8 depth realizes only `18,688/40,320` permutations and misses
`(0,1,2,4,3,5,6,7)`; the ninth actual stage reaches all `40,320`.  Thus the
default hashes are not routing-universal, but polynomial extra depth repairs
this finite obstruction.  The same audit catches that the old example helper
made every output target witness-dependent; a valid SAT compiler must fix only
the asserted root and force unused outputs to constants.

`experiments/verify_u0a_butterfly_formula_compiler.py` implements that repair.
It uses one FREE source per variable, COPY fanout for repeated occurrences,
hypercube swaps, adjacent NAND, formula-oblivious polynomial padding, and a
final ZERO cleanup so the target is assignment-independent.  On the actual
factors it exhausts 100 ordered two-variable NAND trees with 2--4 leaves over
all 400 assignments, including `((x0 NAND x1) NAND (x0 NAND x1))`, and an
8-leaf width-8 example over all eight assignments.  `D(Cz,z)=0`, exact energy,
and target-row restrictions are checked.  A false asserted output costs only
one extra unit; this is completeness/evaluation evidence, not soundness.

**Generation-11 frontier:** formalize the generic compiler and freeze a
canonical `Serialize(S,F)` interface.  Generation 12 below proves the universal
semantic/postorder kernel and supplies the finite canonical manifest, while
leaving butterfly placement/routing and a recursion-safe total emitter open.


## Frontier status — Generation 12 semantic compiler theorem and totality blocker

A universal part of U0a is now machine proved.  The sorry-free file
`lean/Verify_nand_formula_compiler.lean` defines NAND formulas over an arbitrary
variable type, one global assignment, a canonical postorder stack program, and
a total executor.  `compile_correct` proves for every formula, assignment and
initial stack that execution returns exactly recursive NAND evaluation.
Repeated occurrences share the same assignment value.  A fixed root assertion
is assignment-independent and is hit iff the formula evaluates to the desired
bit.  `compile_length` proves exactly one instruction per syntax node.  This is
the semantic compiler kernel, not yet the butterfly placement theorem.

The byte-level interface is also concrete.
`experiments/verify_u0a_canonical_serialize_manifest.py` defines canonical
ordered NAND JSON, rejects malformed/noncanonical inputs, and emits a versioned
manifest for `Serialize(S,F)`.  For fixed `S`, width, depth, row/column marks and
actual `C,D` are formula- and assignment-independent; only declared program
and target rows change.  The finite `S=4` audit covers all 100 formulas and 400
assignments, reconstructs every `D=[I|-C]` entry, freezes factor hash
`355b469b...4b241`, and checks executable polynomial count bounds through
`S=4096`.  These finite arithmetic checks are not the universal complexity
theorem.

The compiler received a much larger finite breaker audit.
`experiments/verify_u0a_butterfly_formula_compiler_exhaustive8.py` exhausts all
1,901,166 pairs of ordered binary shape and repeated-variable equality pattern
through eight leaves.  Worst raw stage counts `0,2,11,19,41,53,65,77` remain
below budgets 68 or 294.  Per-size worst witnesses are also executed by the
actual compiler over all assignments.  This is strong finite evidence, not a
proof of the token-placement invariant.

The exact Python recursion blocker is repaired, but only at the front-end and
dry-scheduler layers.  `experiments/verify_u0a_butterfly_deep_formula_iterative_repair.py`
runs with recursion limit 50, fully materializes and simulates a 61-leaf deep
formula, and iteratively canonical-encodes/decodes and schedules the former
1,101-leaf witness at width 2,048.  Its compressed manifest omits the roughly
two-billion padded mode cells and actual `C,D,target_y`; this is finite
implementation evidence, not a total serializer theorem.

**Active frontier:** formalize the bridge from the proved postorder semantics
to butterfly token placement, COPY fanout, routing, cleanup rows, and actual
streamed `C,D` completeness/emission.  U0b and signed soundness remain separate
open obligations.


## Frontier status — Generation 13 iterative repair, SSA bridge, and streaming blocker

The certified recursion bug is repaired at the parser/scheduler layer.
`leaves_and_gates`, evaluation, canonical v1 encoding/decoding, and the new
`compile_formula_dry_run` use explicit stacks.  The dry run stores
`O(width + syntax)` live state, streams an unpadded trace hash, and compresses
padding to a count.  `experiments/verify_u0a_butterfly_deep_formula_iterative_repair.py`
fully materializes and simulates a 61-leaf width-64 program at recursion limit
50, then canonically encodes/decodes and dry-schedules the former 1,101-leaf
witness at width 2,048.  Its 991,254 stages are summarized without allocating
2,030,088,192 padded mode cells.  The historical counterexample verifier now
reproduces the retired recursive failure locally and confirms current
iterative traversal succeeds.

A second universal bridge is compiled in Lean.
`lean/Verify_nand_register_compiler.lean` defines an abstract LOAD/COPY/NAND
register machine and a postorder SSA compiler.  For every formula it proves
one operation per syntax node, consecutive fresh destinations, preservation of
all registers outside the allocation interval, older operands, and exact root
evaluation.  Separate fresh COPY/NAND theorems preserve their source
registers.  This is stronger than stack semantics but still does not assign
registers to butterfly lanes or numerical factor rows.

The next literal implementation blocker is exact and resource-scoped.
`experiments/verify_u0a_eager_materialization_resource_counterexample.py`
passes complete eager serialization at `S=4` and the deep iterative dry run,
but under a fresh 256 MiB address-space cap the valid complete `serialize`
call at `S=16` raises `MemoryError`.  Exact shapes are
`m=493440,k=330304`; at `S=1101`, the count model gives
`m=60,900,681,684`, `k=40,601,772,032`, and systematic `D` has at least `m`
identity triples.  These counts are polynomial, so this is not a mathematical
impossibility; it proves only that the current eager Python-object interface is
not a streaming polynomial-space emitter.

**Active frontier:** implement canonical streaming emission of padded program,
sparse `C`, systematic `D`, and target without eager Python containers, then
prove the correspondence from the abstract SSA trace through token fanout and
butterfly lane placement to those emitted rows.  Signed soundness and U0b
remain open.


## Frontier status — Generation 14 canonical factor streaming

The eager sparse-factor resource failure is repaired for the next audited
size.  `experiments/verify_u0a_canonical_streaming_emitter.py` generates row
and column marks, complete sparse `C`, systematic `D=[I|-C]`, and target in
canonical eager order while retaining no matrix triple list.  At `S=4` it
compares every streamed item against eager `make_factor`, including component,
program and target hashes.  In a fresh 256 MiB subprocess it completes `S=16`
with `C` shape `493440x330304`, `4,457,168` nonzeros, and `D` shape
`493440x823744`, `4,950,608` nonzeros; measured child RSS is about 22 MiB.
Independent grids `w=2,4,8`, `d=1,2,3,5` also match eager rows, columns,
matrices and mixed targets exactly.

`lean/Verify_sparse_coo_stream.lean` supplies a universal semantic kernel for
this repair.  For arbitrary integer COO records—including duplicates, zeros
and negatives—it proves online fold matvec equals dense materialization and
`Matrix.mulVec`; append/chunk and permutation laws are also proved.  It does
not formalize the serializer's row enumeration or resource bounds.

A trace-metadata race found by the breaker is fixed.  The eager compiler used
to label WAIT after incrementing the stage, so its framed hash differed from
the dry stream.  `experiments/verify_u0a_dry_full_trace_hash_mismatch.py` now
proves eager and dry hashes agree at `75c303...a5d63` and locally reproduces
the retired `d19db4...3b85f` hash.

The remaining implementation bottleneck moved to program emission.
`experiments/verify_u0a_streaming_program_resource_counterexample.py` proves
that the factor streamer still calls dense `compile_formula`: at `S=128` it
retains 3,213,056 mode-dictionary cells and raises `MemoryError` under a fresh
256 MiB cap before matrix streaming.  Counts remain polynomial and the factor
streamer itself is not implicated.

**Active frontier:** stream the padded program from sparse event overrides
(COPY_A default, counted padding, explicit cleanup), stream the corresponding
target program rows without a dense mode map, and prove that this program
stream is the butterfly realization of the abstract SSA trace.  Then lift the
finite row-enumeration equality to an all-parameter Lean theorem.  Soundness
and U0b remain open.


## Frontier status — Generation 15 sparse program streaming

The dense padded-program cap failure is repaired.  The version-1 sparse program
uses COPY_A as the raw/padding default, stores only sorted nondefault
`(stage,lane,mode)` overrides, represents padding by a count, and represents
cleanup by default ZERO with one root-lane COPY_A override.  Source and output
vectors use analogous fixed defaults and ordered overrides.
`experiments/verify_u0a_sparse_program_stream.py` proves exact dense-program
hash, logical mode grid, and target equality on multiple small formulas.  Under
256 MiB it hashes all 3,213,056 logical cells at `S=128` with zero dense mode
cells retained and opens canonical C/D/target streams.

The independent breaker
`experiments/verify_u0a_sparse_program_breaker.py` makes 204 exact comparisons:
all 100 ordered two-variable trees through four leaves with both assertion
bits, plus width-8/16 cases.  It verifies ordering, uniqueness, defaults,
padding boundary, cleanup, random lookup, dense mode equivalence, program hash,
and every target coordinate.  A 256 MiB child at width 256 hashes all
16,781,312 logical cells at depth 65,552.  No mismatch is found; the huge
factor/target is not fully traversed there.

`lean/Verify_sparse_program_overrides.lean` proves the universal representation
kernel: sparse lookup equals dense materialization; strictly sorted overrides
have unique keys and return recorded values; program-row targets are one-hot,
sum to one per cell and to the cell count globally; sparse and dense targets
agree; absent cells select the default.  It proves no butterfly compiler or
resource bound.

Together Generations 14--15 eliminate eager matrix and program storage on the
audited path.  The remaining implementation cost is output/time volume: the
complete stream itself is polynomial but enormous, and only prefixes are
consumed at S=128/256.  `lean/Verify_butterfly_lane_semantics.lean` now proves
the universal local physical bridge: XOR neighbors are involutions; the exact
mode patterns realize SWAP, DUPLICATE, NAND+ZERO, WAIT/padding identity and
cleanup; and any locally valid scheduled trace equals its abstract lane trace.
It assumes rather than derives validity of the sparse compiler's event trace.
The remaining proof gap is therefore correspondence among sparse event
generation, the abstract SSA/token map, local validity hypotheses, and every
emitted target/factor row.

**Active frontier:** formalize that sparse event generation maintains the token
map and emits locally valid scheduled events, then prove all-parameter row
enumeration and target correspondence. Add a chunked on-disk integration test
at the largest practical complete size without conflating output volume with a
mathematical obstruction. Signed soundness and U0b remain open.


## Frontier status — Generation 16 lane semantics and numerical row bridge

The physical lane semantics of every sparse event is now universal.
`lean/Verify_butterfly_lane_semantics.lean` defines the exact five gate modes,
XOR butterfly neighbors, physical stage evaluation, and abstract WAIT/SWAP/
DUPLICATE/NAND+ZERO/cleanup events.  It proves XOR-neighbor involution,
COPY_A identity, local semantics for every event, and by induction that any
trace whose adjacency/distinctness obligations hold has physical lane state
identical to its logical event state.  This is an honest-Boolean theorem, not
an integer-selector or energy theorem.

The finite numerical bridge is much stronger than output-only testing.
`experiments/verify_u0a_sparse_matrix_trace.py` selects one actual source/gate
column per node from a sparse program, streams every C and D row, and checks
normalization, one-hot program, edge, dyadic separator, output and physical
moments.  It checks each D row is exactly systematic `[I|-C]` and every
`D(Cz,z)` moment is zero.  Twenty-one assignments cover widths 4/8 plus a full
width-16 C/D pass under 256 MiB; 1,150,512 rows are checked.

The independent breaker
`experiments/verify_u0a_sparse_numerical_bridge_breaker.py` audits every emitted
C coefficient at width/depth `4/68` and `8/294`, exhausts all ordered
shape/equality-pattern formulas through five leaves (728 at size five), performs
6,878 packed assignment evaluations and 1,044 full streamed-C honest-vector
checks, and kills deliberate offset, neighbor, COPY_B and fanout mutants.  It
finds no counterexample.  NAND child exchange is correctly harmless because
NAND is symmetric, while physical A/B port orientation is still audited.

The remaining universal gap is sharply localized.  The Python sparse compiler
checks event adjacency and token placement, but Lean currently assumes each
`ScheduledEvent.Valid`; the numerical row bridge is finite.  No theorem yet
shows the generated event list satisfies validity, preserves the compiler's
token map, and selects the exact emitted column/row moments for all formulas.

**Active frontier:** formalize the sparse event generator and prove its event
validity/token-map invariant, then connect the universal lane trace to one-hot
selector columns and streamed C row equations.  Only after this completes U0a
honest completeness may the campaign return to signed U2/U3 soundness and the
separate U0b lattice-class exclusion.


## Frontier status — Generation 17 valid-by-construction events and certificates

The abstract trace-validity premise is removed for the actual edge grammar.
`lean/Verify_butterfly_lane_semantics.lean` now defines smart `XorEvent`s that
store only a physical dimension and free endpoint; scheduling synthesizes the
other endpoint by XOR with `2^d`.  Lean proves this neighbor has no fixed point,
every smart event satisfies involution/adjacency/distinctness, every generated
trace is valid, and physical execution equals logical execution unconditionally
for all smart XOR traces.  The remaining gap is proving the Python sparse
compiler corresponds to this datatype and stays inside its finite width.

The executable compiler now emits a JSON-safe per-stage event/token
certificate.  `experiments/verify_u0a_event_token_certificate.py` round-trips
this artifact before checking it, independently validates formula tables,
source allocation, duplicate/NAND demand order, every stage/dimension/mode
pattern and before/after token map, then derives actual selected columns and
projects every streamed C row.  It exhausts all 102 ordered two-variable trees
through four leaves and 408 assignments; a capped width-16 child is included.
In total 1,347 events and 3,781,920 C-row projections are checked, including
129,136 exact selected physical rows.

A separate bounded breaker
`experiments/verify_u0a_sparse_event_validity_breaker.py` symbolically replays
486 comb/balanced/fuzz cases through 129 leaves, covering occupied/empty path
swaps and duplicate calls after their base token moved.  No semantic or
adjacency failure appears.  The earlier numerical mutation breaker continues
to reject offset, neighbor, COPY_B and fanout errors.

The full-snapshot certificate introduces the next finite resource boundary.
`experiments/verify_u0a_event_certificate_resource_counterexample.py` passes a
129-leaf certificate but under 256 MiB a valid 1,025-leaf distinct-variable
comb raises `MemoryError`.  Before/after live-token snapshots at every event are
polynomial but unnecessarily quadratic-ish in stored state; the executable
program itself remains sparse.

**Active frontier:** replace full token-map snapshots by a canonical delta
certificate (event operands/endpoints plus optional checkpoints), stream and
verify it, and formalize that the Python event generator elaborates to the
Lean smart-XOR trace.  Then prove selected-column/row completeness universally.
Signed soundness and U0b remain open.


## Frontier status — Generation 18 snapshot-free delta certificates

The full-snapshot certificate failure is repaired by schema v2.  The sparse
compiler accepts `certificate_version="v2"`; it retains canonical formula
tables, one initial and final token map, and ordered event records containing
only stage/dimension, role-ordered endpoints, nondefault modes and semantic
tokens.  No per-event before/after maps are stored.  Optional checkpoints are
domain-separated, length-framed hashes of verifier-owned replay states.

`experiments/verify_u0a_delta_event_certificate_breaker.py` independently
replays JSON-round-tripped v2 certificates.  It exhausts 102 small formulas,
checks a width-16 trace, and rejects seven mutations: missing token, duplicate
lane, event reordering, omitted program/event override, checkpoint state
substitution, and missing semantic token.  Under 256 MiB a 4,097-leaf skew comb
passes with width 8,192, 84,863 events, 20,420 overrides and about 122 MiB RSS.
This strictly repairs the former 1,025-leaf full-snapshot failure.

`lean/Verify_event_delta_replay.lean` supplies the universal bookkeeping
kernel.  Token maps are verifier-owned functions to optional lanes; ordered
sparse deltas replay by updates.  `allTransitionsMatch` checks each delta
against its advertised logical event at the state reached by preceding deltas.
Lean proves local agreement composes, eventwise agreement suffices, and a
snapshot-free certificate's logical final map and every token lookup equal its
claimed final map.  The theorem is generic and does not prove concrete Python
deltas match XorEvent logical transitions.

**Active frontier:** formalize the concrete v2 event/delta encoding and prove
each SWAP/DUPLICATE/NAND delta equals the corresponding Lean smart-XOR logical
step; then compose this with selected-column streamed-row semantics.  Optional
checkpoint hashing remains an implementation integrity layer, not part of the
Lean theorem.  Signed soundness and U0b remain open.


## Frontier status — Generation 19 explicit concrete token deltas

Certificate v3 closes the representational mismatch between Python events and
Lean `Change` lists.  Every WAIT has an empty delta; SWAP records the occupied
endpoint token moves; DUPLICATE creates its fresh token; NAND canonically
deletes left and right then creates the output.  The certificate remains
snapshot-free and v1/v2 compatibility is preserved.

`experiments/verify_u0a_explicit_token_delta_breaker.py` JSON-round-trips v3,
independently derives the exact delta required by each event from verifier-owned
state, compares sequence equality, and applies simultaneous delete/write
semantics with lane-collision checks.  It rejects nine mutants, including a
missing two-sided SWAP token, empty-empty routed SWAP, wrong deletion/order,
duplicate write, invented empty-endpoint token and lane collisions.  The
4,097-leaf capped run passes with 84,863 events, 22,091 delta records and about
135 MiB RSS.

`lean/Verify_concrete_event_deltas.lean` formalizes the same concrete event
family.  Exact endpoint occupancy, freeness and token/lane distinctness form
the state-dependent validity predicate.  Lean proves the canonical short delta
list implements WAIT, all four SWAP occupancy cases, DUPLICATE and NAND; these
local results compose into a snapshot-free final-map theorem.  This is the
first formal bridge whose data shape matches the v3 producer directly, modulo
JSON parsing and naming.

**Active frontier:** prove the compiler-generated v3 trace satisfies the Lean
concrete event validity predicate and finite-width bounds by structural
induction on formula/token scheduling, then connect final token placement to
the universal streamed-row equations.  Finite certificates strongly support
this bridge but do not replace it.  Signed soundness and U0b remain open.


## Frontier status — Generation 20 finite-width and occupancy invariants

The finite-lane omission in the unbounded XOR model is closed universally.
`lean/Verify_butterfly_finite_width.lean` proves that for lane `<2^k` and
`d<k`, XOR by `2^d` remains `<2^k`; it packages the neighbor as
`Fin (2^k)->Fin (2^k)`, proves involution and fixed-point freeness, and defines
finite-width smart events whose scheduled endpoints are valid by construction.
Thus out-of-range XOR routing cannot occur once the compiler supplies
`d : Fin k` and lanes of the finite type.

`lean/Verify_concrete_event_deltas.lean` now also proves the live-token
invariants needed by the concrete scheduler.  `OccupancyInjective` is preserved
by valid WAIT/SWAP/DUPLICATE/NAND logical steps and whole valid traces; erasing
a token and writing into a checked free lane preserve exclusive ownership.
Exact active-token counts are preserved by WAIT/SWAP, increase by one for
DUPLICATE, and decrease by one for NAND.  These are universal conditional
invariants over the concrete event validity predicate.

The large finite breaker
`experiments/verify_u0a_v3_power_boundary_breaker.py` checks JSON-round-tripped
v3 traces at 8,191, 8,192 and 8,193 leaves, crossing width 8,192 to 16,384.
Every endpoint, explicit delta destination, override and output lane stays in
range; 12 out-of-range/adjacency/collision/stage/snapshot mutations are rejected.
The three capped children replay 278k--344k events with no full snapshots.
This is finite implementation evidence, not the compiler induction.

**Active frontier:** formalize the formula scheduler itself so its state carries
finite lane types, occupancy injectivity, free-lane existence and postorder
demand invariants, and prove its emitted v3 trace instantiates the already
proved smart-event/delta theorems.  The remaining honest row bridge can then be
an induction over emitted stages.  Signed soundness and U0b remain open.
