# Independent oracle brief: surviving design space after prior campaign

## Target and restrictions

Independently construct a deterministic polynomial-time many-one reduction from 3SAT to binary syndrome decoding with an `N^c` Hamming gap for an explicit constant `c>0`, and then use the exact mod-2 lattice lift to obtain an `N^{c/2}` Euclidean CVP gap. No PCP theorem, no Projection Games or other conjecture. The recent prohibited document named in `AGENTS.md`, and every copy, summary, discussion, or recollection of its proof, is off-limits. Use only classical literature predating that document and independent reasoning.

## Proved obstruction map inherited from `prior/`

These are theorems/certified witnesses, not intuitions.

1. **Bounded local signatures.** Every degree-`d` polynomial signature on a Boolean view has an alternating `(d+1)`-cube relation. A forbidden view is an exact signed combination of at most `2^(d+1)-1` allowed views. Affine signatures give the three-column parallelogram. The relation survives arbitrary linear rows, modular reduction, tensoring, and dense linear postprocessing. Assumptions: the independently flippable cube exists and signature degree is `<` cube dimension. It does not cover genuinely global/high-degree sparse columns.
2. **Marginal/tableau encodings.** Unary GF(2) marginals have rectangle kernels; every proper marginal of a `k`-bit table kills the full parity cube. OR-gate tableaus have a support-three output-flip. Full local truth tables with integer unary interfaces have the signed `a+b-c` cheat. Assumption: communication factors through proper affine marginals or bounded-fan-in wire interfaces. Genuinely global rows are outside it.
3. **Local-view hierarchies.** A bounded-occurrence exact-3CNF encoding of a twisted 3-color cycle has a support-three exact pseudoassignment on every proper connected scope; a signed 2-orbit/3-orbit version works over integers. All-pairs/full-intersection scopes fail on a charged Petersen-flow CSP; every fixed scope level fails at some growing arity. Assumptions: scopes miss the global dependency, or fixed level is allowed hostile arity. Growing logarithmic scopes for fixed arity are not covered in full generality, but explicit truth tables risk output explosion and odd holonomy defeats connected proper scopes.
4. **Phase lifts.** Copy-stable, single-valued local phases with universal completeness and cycle realization are coboundaries, hence gauge-trivial and retain the three-column trade. Random nontrivial phases reject YES instances with probability governed by incidence cycle rank. Assumptions exclude genuinely graph-dependent global selectors.
5. **Integer exact fibers.** Huge row scaling, affine/polynomial count slacks, CRT assignment coupling, and bounded-fan-in circuit evaluation all retain constant-cost exact-fiber repairs. Assumption: local validity remains affine/bounded-degree after global uniqueness is imposed.
6. **Complete-assignment fingerprints.** Over fixed prime fields fewer than `2^n-1` arbitrary feature rows are linearly dependent. Polynomial-count, polynomial-bit integer features have subset-sum collisions. Incomplete Walsh or univariate moment families have exact virtual assignments; complete families are exponential. Assumption: one explicitly groups columns by complete assignments; this does not cover a polynomial-size sparse dictionary.
7. **Tensor amplification.** Pointed distance of the full tensor code and pure-power subcode is exactly multiplicative. But explicit tensor length makes the exponent from an additive base gap tend to zero. Symmetric representative puncturing still forces bounded tensor order. A lower bound excludes fixed code-oblivious coordinate samples, but **not code-dependent dense structured folds**. Tiny dense folds usually collapse distance; no asymptotic no-go is known.
8. **Exact transfer (positive).** For binary `H,t`, `Lambda_H={z in Z^N: Hz=0 mod 2}` satisfies `dist_2(v,Lambda_H)^2=min{|e|:He=t}` for any binary `v` with `Hv=t`; an explicit integer basis follows from row reduction. Thus an NCP factor `gamma` gives Euclidean factor `sqrt(gamma)` at rank `N`.

## Structural opening

A surviving construction must use a polynomial-size sparse column model with genuinely global coupling and a norm-versus-integrality theorem. The two visible openings are:

* a **code-dependent dense structured folding** of a pointed tensor power whose generator is computable without expanding the tensor and whose soundness covers every mixed tensor combination; or
* a **sparse global algebraic dictionary** where legal Boolean assignments have very sparse representations but all nonintegral/superposed representations of the target are polynomially heavier.

Any proposal must explicitly survive: (i) the all-eight 3-clause core and its local cube trades, (ii) odd permutation holonomy, (iii) arbitrary mixed tensor words, and (iv) YES-baseline/output-rank accounting.

## Current post-construction position

The two original openings have now been narrowed substantially.

* Exact-cover relative quotients fail when illegal odd covers lie in the affine
  span of legal matchings (`verify_exchange_quotient.py`).
* Reduced pointed tensoring and odd orbit folding have rigorous all-mixed-word
  distance lemmas, but invariant ladders conserve a vanishing exponent;
  non-invariant sheets do not compress in tested cases; direct cyclic closure
  destroys distance; pure tensor catalysts cannot improve standard rank
  exponent; sparse hashes lose soundness.
* A deterministic code-dependent generator-column-type puncture was tested on
  every mixed word and loses the finite gap.
* Exact parity-check parallel simplification preserves every syndrome coset
  distance, but is rigorously vacuous on BMT reduced tensors: their moving
  span has distance at least three, tensor products have larger distance, and
  a parity-check kernel of distance at least three has no zero/repeated
  columns (`verify_parity_type_tensor.py`).

A new direct integer construction sharpens the remaining need.  Integer 3DM
incidence CVP has rigorous squared gap `q` versus `q+2`, including signed
coefficients.  Fixing all three pair-projection permutation matrices eliminates
the tested NO fibers.  Making those tables lattice variables gives a
polynomial-size signed-sound encoding of the disjunction, but each row-sum-one
table has norm at least `q`; exact tests give only 12 versus 14.  Global binary
feature-cost shells likewise reduce the gap.

A focused proof pass now resolves integer tensor soundness.  For coordinate
incidence lattices, reduction mod two has pointed distance `q+1` versus at
least `q+3`, and this distance multiplies exactly for every mixed tensor;
integer squared norm dominates parity support.  A rank-two pointed sublattice
theorem `det_Gr>=4(q+2)` is proved, but arbitrary-Euclidean all-partner
multiplicativity is false and its required determinant profile is too large.
A new exact Euclidean mechanism compresses pure-power tensor tuples to their
underlying set supports, retaining integer orbit multiplicities as sums of
scaled square rows.  It preserves every mixed pure-power word and makes output
independent of tensor order, but uses up to `2^n-1` subset coordinates in base
length `n`.  Merging identical product functions helps finite low-dimensional
3DM codes but has no polynomial asymptotic bound.

Thus the remaining core need is either (i) prove polynomially many reachable
product-function types for a suitable additive-gap base family, (ii) obtain a
base reduction with logarithmic coordinate length relative to represented
instance size, or (iii) an **asymmetric, code-dependent linear operation**
that can be computed from the instance without finding a SAT witness, gives a
short sparse representative to every satisfiable affine fiber, and provably
charges all unsatisfiable fiber words by a larger-than-common multiplier.  It
must not be pure tensor-product multiplication, ordinary puncturing/type
merging, or a quotient identifying all legal witnesses.  No such operation or
classifier is known in this run.  Any future proposal must specify an explicit
matrix and first survive the tiny 3DM YES/NO families plus the all-eight-clause
and odd-holonomy attacks.
