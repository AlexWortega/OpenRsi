# Status

**Outcome:** PARTIAL NEGATIVE RESULTS ONLY / no progress on goal ladder (a)--(c).

## Proved

* The one-hot GF(2) syndrome gadget has an additive-cost-2 exact superposition cheat at each violated clause.
* Universally, two lattice branch points within radius `R` create the affine extrapolation `2p0-p1` within radius `3R`; any integer affine combination is bounded by its coefficient l1 norm. Thus local Boolean branches cannot be separated polynomially from all affine extrapolations without global coupling.
* More generally, every degree-`d` polynomial local signature has an alternating `(d+1)`-cube cheat: a forbidden view is an exact +/-1 combination of at most `2^(d+1)-1` other vertices. For constant local degree this costs only a constant in support/squared coefficient norm and survives all subsequent linear mixing, modular reduction, tensoring, and dense linear folding. The affine parallelogram is `d=1`; all seven legal 3-bit views defeat quadratic clause signatures.
* Copy-stable local phase lifts satisfying cycle realization and universal assignment completeness are necessarily coboundaries: every realizable alternating type cycle has zero holonomy, so spanning-forest potentials gauge phases away. The original support-three trade then returns. This theorem does not cover global cycle-dependent selectors.
* Bounded-order GF(2) marginals are intrinsically nonintegral: unary systems have 2x2 rectangle kernels, and for a `k`-bit table the sum of all cube vertices vanishes under every marginal of arity `< k`. Full-arity information is required to kill this universal parity kernel, explaining factor/branching splices and higher-order analogues.
* The logarithmic connected-view hierarchy is refuted by an explicit bounded-occurrence exact-3CNF family. For every integer depth `1 <= d < n`, it has an exact pseudoassignment of weight at most `3K` (`proof_cvp.md`). The odd-orbit obstruction also survives arbitrary disconnected proper scopes if consistency is only unary: each forest scope's three translated colorings have the same all-three-colors marginal at every variable.
* Pointed distance is exactly multiplicative both for full tensor codes and for the subcode spanned only by pure powers. Symmetric-orbit representative puncturing of the latter gives length `binom(L+q-1,q)` and retains distance at least `delta^q/q!`, but polynomial output still forces bounded `q`, so it cannot amplify the additive base gap.
* For every **fixed, code-oblivious** tensor-coordinate sample required to separate all one-dimensional pure-support codes uniformly, a quantitative adjacent-layer lower bound holds. A strict factor `> R` requires at least `(N/(K+1))^floor(K+2-(K+1)/R)` sampled coordinates; for factor `>= R`, use exponent `ceil(K+2-(K+1)/R)-1`. This does not cover code-dependent samples.

## Computational evidence (not proof certificates)

* A characteristic-3 exact-one implementation kills the specific GF(2) cheats but has additive threshold N versus N+1. HiGHS reports N=51, optimum 52 on the all-eight-clauses core.
* A direct integer CVP encoding with equation scale `M=10^6` has an explicit exact-fiber false-clause repair of additive squared cost 2, independent of `M`. Padding drives the distance ratio to 1 (below 1.0005 at verified `D=1000`). Generally, every clause-slack system affine in true-literal count extrapolates short witnesses by `w_false=2w_count1-w_count2`, so scaling/moduli cannot fix it.
* HiGHS reports minimum support 243 for the fixed depth-2 connected-view instance. These floating-point MILP runs have no independently checked exact branch-and-bound certificates.
* Finite sanity checks run via the `experiments/verify_*.py` scripts; they do not prove quantified asymptotic statements.
* Exact code-dependent puncture search on `D=span{110,101}` found that preserving its tensor-square pointed distance 4 requires all 9 tensor coordinates. Among 40 deterministic random length-4 dimension-2 codes, some could be punctured strongly and others required 8, 9, or all 16 coordinates. No asymptotic theorem follows.
* The all-pairs full-intersection hierarchy is **dead despite extensive positive tests**. A charged GF(3) incidence CSP on the Petersen graph is UNSAT yet has an exact zero-residual pseudoassignment. Disjoint unions give an infinite cubic arity-3 family whose pseudoassignment weight is only a constant factor (tending to 81) above the group baseline. More generally, every fixed scope level `k` fails on charged incidence constraints over `K_(2k+1)` of arity `2k`.
* On holonomy cycles, all-intersection random scopes show a density threshold: all 30 deterministic n=5..10 trials using `2n` random 3-edge scopes were infeasible; sparser/2-edge systems often remained feasible.
* A global controlled-permutation-cycle candidate also cheats: an explicit q=3 exact syndrome witness has weight 9 although both fixed Boolean branches have fixed-point-free holonomy. Random q=3,4,5 length-3 instances all receive reported optimum 9; a three-column factor superposition splices inconsistent trajectories. The explicit witness is exact, but general optimality remains MILP evidence.
* Phase-lifted local clause columns were attacked by exact GF(2) subset DP. Across recorded random q=2,3,4 signatures, every feasible forbidden boundary had a three-column trade; larger-q MITM searches often found no trade through support 5. But nontrivial random phases reject satisfying instances: a fixed assignment lifts with exact probability `q^{-(E-V+c)}`, exponential in incidence-cycle rank; the unique-SAT core has exponent 12, and 0/1000 sampled tables at each q=2,3,5 lifted it. Completeness-preserving coboundary phases are gauge-equivalent to the unlifted gadget and restore its cheat. This route currently has no completeness/soundness balance.
* Exact enumeration on the smallest 2-dimensional pointed code shows permutation-orbit XOR folding drops tensor-square pointed distance from 4 to 2. Of 200 deterministic random dense 9-to-6 folds, only 2 retained distance 4; 52 dropped to 1. This is evidence against naive dense folding, not a theorem about structured code-dependent folds.

## Claims not established

No polynomial-gap NCP reduction and no GapCVP reduction have been obtained. These are obstruction/counterexample results, not item (a). Construction-A distance identities are available but have no polynomial-gap input.

## Structural wall

Linear encodings admit cheap affine extrapolation, and degree-below-arity local signatures admit finite-difference cube relations. The cubic 3-clause violation indicator does separate the forbidden view, but its nonzero third mixed difference means it cannot be assembled from unary variable interfaces. Full local truth tables inside logarithmic scopes admit odd-holonomy pseudoassignments. Scaling constraint coordinates cannot help exact alternative representations. Therefore a surviving construction needs genuinely joint/global signatures plus a norm-versus-integrality theorem tying them to separately encoded variables inside a nonempty exact fiber—the original difficult step.

## Tensor-compression classes not covered here

Code-dependent coordinate samples and arbitrary **dense** structured linear foldings are not covered by the fixed-sample lower bound. Naive symmetric-orbit XOR and random dense maps fail on tiny exact tests. More structured dense functionals can separate adjacent layers on pure tensors, but an explicit polynomial image generator and soundness against all tensor combinations are missing.

## Honest ladder assessment

Zero advancement on (a)--(c): no polynomial-gap NCP instance and hence no polynomial-gap CVP reduction. The proved results are negative diagnostics only.

## Current milestone

Consultations 6, 7, and 8 have been fully acted on in code and proof. All 40 `experiments/verify_*.py` scripts pass together; combined output is saved in `verify_all.log` (regenerated after the latest milestone). No further oracle call is warranted until a genuinely global candidate matrix—not a bounded-local signature, unary random-scope system, fixed local phase system, or routine tensor folding—is specified and survives exact low-weight search.
