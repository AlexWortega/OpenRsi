## Generation 27 — divergent mechanisms

*G20/G21/G22 occur only in the gate; I interpret them respectively as failure of relative-gap growth, polynomial-size scaling, and unlisted entangled vectors.*

### 1. Rényi-energy logarithmic bags

**Mechanism.** Replace half-integral anchors by zero-centered \(k\)-variable bag selectors: normalization makes an honest one-hot bag cost \(1\), whereas a signed pseudomarginal costs \(\|z_B\|_2^2\). Use deterministic \(k=\Theta(\log n)\) overlapping bags, seeking a lemma that every inconsistent integral family is either a drop or has average collision energy \(n^\epsilon\).

**Expected move.** Weight normalization heavily; then bag-energy growth gives an \(n^{\epsilon/2}\) distance gap with polynomially many \(2^k\)-sized tables.

**Obstruction audit.** G1: no slack. G2/3: local isolation unused. G5: global bags replace private rows. G6: all conditions are lattice coordinates. G7: zero residual still pays bag energy. G9/G11: parity must spread, not merely become nonzero. G12: drops pay normalization weight. G13: affine mixtures remain legal but are priced by projected \(\ell_2\)-energy. G14: this is its logarithmic, zero-centered extension. G15: zero residual no longer implies cheap anchors. G19: induced flow marginals must be audited. G20/G21: the required energy lemma is presently missing. G22: unrestricted enumeration remains mandatory.

**Falsification.** A zero-residual inconsistent family with \(O(1)\) energy per bag.

**Experiment.** On the nine-clause instance, use all four three-variable bags, objective \(\sum_B\|z_B\|^2+W^2\|Az-b\|^2\), and exact DP for \(W=3,5,9\).

**Likely death.** The G13 affine mixture may retain constant collision energy everywhere.

---

### 2. Discrete-convex Booleanity lock

**Mechanism.** Search for a formula gadget whose centered Gram matrix satisfies explicit coordinate-clipping inequalities: replacing any integral coefficient by its nearest value in \(\{0,1\}\) never increases distance. A sign-switched Stieltjes/M-matrix geometry is the candidate sufficient structure; if preserved by clause auxiliaries, unrestricted CVP collapses to Boolean optimization.

**Expected move.** Once clipping is certified, clause penalties can be scaled polynomially without opening signed shortcuts.

**Obstruction audit.** G1: no slack variables. G2/3 and G5: clipping is global, not local-fiber composition. G6: clipping concerns the emitted lattice itself. G7, G9, G11, G13, G15, G19: every negative or \(>1\) coefficient is dominated by a Boolean vector, so these signed attacks are outside the certified region—if certification succeeds. G12: clause drops are Boolean and therefore still require expensive normalization rows. G14: no bag hierarchy is assumed. G20/G21: polynomial scaling follows only after a size-independent clipping theorem. G22: clipping would include entangled vectors; bounded testing alone would not prove it.

**Falsification.** Any integer vector improved by moving a coordinate away from \(\{0,1\}\), or incompatibility between OR and the required Gram signs.

**Experiment.** For the unsatisfiable eight-clause, three-variable core, MILP-search integral Gram entries in \([-3,3]\), then exhaust \(z\in[-2,3]^d\) and certify the tails by diagonal dominance.

**Likely death.** Exact OR penalties probably cannot be quadratized within this discrete-convex class.

---

### 3. Segre tensor amplification with normalization paid once

**Mechanism.** Tensor a constant-size selector tile \(t\) times, using tuple selectors and marginal glue, but impose only one outer normalization. Honest decomposable tensors retain norm \(1\), while a base signed state of squared norm \(q>1\) would cost \(q^t\); constant alphabet and \(t=\Theta(\log n)\) keep dimension polynomial.

**Expected move.** Obtain polynomial amplification from tensor norm rather than repeated residual weights or repeated completeness baseline.

**Obstruction audit.** G1: no slack. G2/3/G5: tensor glue replaces private overlap. G6: every marginal is emitted. G7: its signed vector tensors expensively, unless an alternative lift exists. G9/G11: parity likewise amplifies only when decomposable. G12: outer normalization prices drops. G13: raw affine relations are not preserved by nonlinear tensoring, but affine combinations of tensor codewords may replace them. G14/G15: this is neither fixed pair bags nor additive hierarchy. G19: signed paths may generate entangled tensors. G20/G21: \(q^t\) is the proposed explicit recurrence. G22: entangled low-norm tensors are the central unresolved obstruction, not outside the assumptions.

**Falsification.** A nondecomposable tensor satisfying all marginals below the base signed-vector cost.

**Experiment.** Tensor-square the seven-selector falsified-OR tile: 49 tuple variables, diagonal honest controls, full one-factor marginals. Exactly enumerate the unrestricted shell through baseline \(+24\).

**Likely death.** Marginals admit cheap entangled couplings whose norm does not multiply.

---

### 4. Nonabelian holonomy / twisted-sheaf barrier

**Mechanism.** Put a small integral representation space on each occurrence and permutation-valued transports on overlaps. Honest assignments are flat sections; inconsistency should create nontrivial holonomy, and a magnetic-Laplacian block charges every vector outside the common invariant subspace rather than merely detecting scalar marginal disagreement.

**Expected move.** Tensor or symmetric-power representations of depth \(O(\log n)\) could turn a constant holonomy angle into polynomial energy while retaining polynomial dimension.

**Obstruction audit.** G1: no slack. G2/3/G5: overlap is coupled through noncommuting transports, not private scalar rows. G6: flatness and legality are emitted coordinates. G7: scalar zero kernels need not be twisted-flat. G9/G11: parity is tested in representation channels. G12: zero sections violate normalization. G13/G15: affine combinations of flat sections remain flat, so success requires proving the unsatisfiable legality slice has no invariant vector; not automatic. G14: no complete pair mesh. G19: signed-flow splicing may survive as an invariant subrepresentation. G20/G21: representation-power growth needs proof. G22: all invariant and entangled sections must be enumerated.

**Falsification.** A nonzero integral legal flat section, especially one induced by G13 or G19.

**Experiment.** On the nine-clause graph, enumerate \(S_3\) transports in its two-dimensional standard representation; reject completeness failures, then use SNF plus exact shell DP to find legal twisted sections.

**Likely death.** Semantic completeness may force a common invariant direction that also carries the affine attack.

---

### 5. Iterated Lawrence lifting of harmful fibers

**Mechanism.** Replace ordinary clause gluing by iterated Lawrence liftings of the local constraint matrix, chosen so projected kernel moves must appear in coupled positive/negative layers. Seek a family where every harmful zero-residual Graver move has norm multiplying with depth, while honest selectors use one diagonal layer.

**Expected move.** If minimum harmful Graver norm grows as \(\gamma^t\) for \(t=\Theta(\log n)\), zero-centered anchors yield a polynomial gap in polynomial dimension.

**Obstruction audit.** G1: no slack. G2/3: starts from the certified local matrix but changes composition. G5: Lawrence coupling is intended specifically to prevent clause-supported circuits. G6: full lifted equations are emitted. G7: its kernel move must lift through every layer. G9/G11: parity becomes a candidate Graver element. G12: layer normalization prices drops. G13/G15: affine lifts remain possible and are the primary test. G14: no fixed bag-shell claim. G19: network matrices often retain tiny circuits, so signed flow is not escaped automatically. G20/G21: multiplicative Graver growth is the missing theorem. G22: primitive mixed-layer moves require complete enumeration.

**Falsification.** A bounded-support Graver element persisting at every lift level.

**Experiment.** Apply one, two, and three Lawrence lifts to a Generation-3 survivor joined across two clauses; compute shortest kernel vectors and harmful affine fibers by exact branch-and-bound or `4ti2`.

**Likely death.** Lawrence lifting may merely replicate the G5/G13 circuit with constant complexity.

---

### 6. Recursively closed Voronoi transfer tiles

**Mechanism.** Treat short vectors of a full-rank CVP tile as finite port states and compute exact min-plus gluing, including legal, malformed, drop, affine, and entangled states. Search for a tile whose transfer operator contracts legal cost by \(\mu\) but forces every illegal state to grow by \(\lambda>\mu\), giving a certified depth recurrence.

**Expected move.** Depth \(O(\log n)\) would produce ratio \((\lambda/\mu)^{\Theta(\log n)}=n^c\) with constant branching.

**Obstruction audit.** G1: no slack. G2/3/G5: overlap behavior is represented as states, not assumed compositional. G6: the basis and target are fixed. G7, G9, G11, G13, G15, G19: include their exact port signatures as named states. G12: DROP is explicit. G14: uses its finite-pass philosophy but demands recursive closure. G20: \(\lambda>\mu\) is the required relative-growth certificate. G21: constant branching supplies polynomial size. G22: every depth-two minimizer must map to a listed state; otherwise kill.

**Falsification.** State nonclosure, completeness mismatch, or \(\lambda\le\mu\).

**Experiment.** Base tile: two seven-selector clauses sharing one variable, objective \(\|z\|^2+9\|Az-b\|^2\), port equal to both normalizations and shared marginals. Enumerate all vectors through \(B+16\), glue two tiles with weight \(3\), and recompute the complete depth-two state table.

**Likely death.** A previously expensive entangled representative may re-enter cheaply after contraction.

Classical vocabulary used here: K. Murota, *Discrete Convex Analysis* (2003); B. Sturmfels, *Gröbner Bases and Convex Polytopes* (1996), especially Lawrence configurations and Graver bases.
