# Idea population

Status vocabulary: **untested / wounded / killed / promising**. An idea is abandoned only after a mutation aimed at its specific failure has also been tested.

## Inherited autopsies

### I01 — GF(2) one-hot legal clause views — killed
**Mechanism.** Select one global value per variable and one legal local view per clause; use affine incidence/coverage rows.

**AUTOPSY.** At forbidden `u`, three legal views `u+p,u+q,u+p+q` sum to `u`. This is an exact support-three zero-residual repair, not a residual-distance issue.

**Fine print.** Needs an affine signature of at least a 2-face of local Boolean views. It does not cover genuinely joint nonlinear/global interfaces.

**MUTATION TESTED.** Degree-`d` local signatures, including quadratic signatures and full local truth tables projected to unary interfaces. Finite-difference cubes or `a+b-c` after projection still cheat. Mutation killed.

### I02 — Connected/random/full-intersection local-view hierarchies — killed
**Mechanism.** Enumerate satisfying views on scopes and enforce exact restriction marginals; grow scope depth or use nonlocal pairs.

**AUTOPSY.** Twisted odd-color cycles give support-three pseudoassignments on every proper forest scope. Integer 2/3-orbit differences give mass one. All-pairs scopes have an exact Petersen charged-flow pseudoassignment; each fixed level has a charged-incidence counterexample at suitable arity.

**Fine print.** The strongest theorem for arbitrary fixed level allows arity to grow with level. It does not universally exclude growing scopes for fixed arity, but connected proper scopes already fail at logarithmic depth and explicit full-scope tables spend exponential columns.

**MUTATION TESTED.** Random disconnected scopes with full intersections, then all pairs. Both initially passed small tests; sparse scopes failed on long cycles, and all pairs were killed by Petersen flow. Mutation killed.

### I03 — Change characteristic / integer row scaling / exact slacks — killed
**Mechanism.** Work over GF(3) or integers; make unsatisfied residuals huge while honest coefficients remain short.

**AUTOPSY.** GF(3) exact-one has an additive one-coordinate repair. Integer affine count slacks satisfy `w0=2w1-w2`; bounded polynomial count slacks obey finite differences. Therefore NO points remain in the exact fiber at constant additive norm, independent of scaling.

**Fine print.** Requires clause validity to factor through bounded-degree count/slack witnesses. It does not cover a genuinely global nonlinear norm condition.

**MUTATION TESTED.** Couple every Boolean bit through one CRT integer, while retaining clause slack rows. The false clause still repairs exactly at additive squared cost 8 and the CRT coordinate inflates the YES baseline. Mutation killed.

### I04 — Compact global predicate via circuit tableau — killed
**Mechanism.** Evaluate determinant/resultant/high-degree assignment predicates with polynomial-size bounded-fan-in circuits; linearize legal gate tables.

**AUTOPSY.** OR has the exact legal-column relation `(0,0,1)=(0,1,1)+(1,0,1)-(1,1,1)` including coverage. One gate flips false to true at additive cost two, and the fault propagates through an accepting transcript.

**Fine print.** Requires bounded-fan-in local tables communicating by affine wire interfaces. Direct genuinely global rows are not covered.

**MUTATION TESTED.** Full-degree clause truth tables over integers. Unary global interfaces restore the affine parallelogram and yield a norm-13 all-eight witness. Mutation killed.

### I05 — Local phase lifts / global branch selector — killed
**Mechanism.** Add cyclic phase labels to increase local trade girth; preserve some phase lift for each satisfying assignment.

**AUTOPSY.** Random phases often increase local girth but reject YES assignments exponentially in incidence cycle rank. Under copy-stable universal completeness, phases are coboundaries and gauge away. A shared global branch controlling permutation constraints still admits a weight-9 rectangle splice.

**Fine print.** Coboundary classification assumes copy-stability, cycle realization, and single-valued interfaces. Formula-dependent global selectors are not formally excluded.

**MUTATION TESTED.** Finite seed menus and a globally shared controlled-permutation branch. Zero-holonomy seeds are locally cheatable; marginal rectangle superpositions splice global branches. Mutation killed within tested selector model.

### I06 — Global complete-assignment fingerprints — killed
**Mechanism.** Give each complete assignment dense Walsh, moment, or arbitrary feature values and enforce equality across forbidden groups.

**AUTOPSY.** Over fixed fields, fewer than `2^n-1` augmented fingerprints are dependent. For polynomial-bit integer fingerprints, subset-sum collisions yield signed kernel vectors. Walsh and univariate moments exhibit explicit virtual measures unless interpolation-complete, which costs exponential rows.

**Fine print.** Assumes complete-assignment columns/groups, already exponential. It does not cover a different polynomial-size sparse dictionary.

**MUTATION TESTED.** Walsh characters, arbitrary field features, bounded integer features, and univariate high-degree moments. All incomplete families have exact low-cost witnesses; complete families are exponential. Mutation killed.

### I07 — Reduced pointed tensor + fresh-symmetry orbit fold — promising
**Mechanism.** Homogenize an affine coset to a pointed code. Tensoring exactly raises pointed distance to a power.

**AUTOPSY.** Full tensor length is exponential in tensor order, so an additive base gap gives vanishing approximation exponent relative to output size. Pure-power symmetric orbit representatives still have length `binom(L+q-1,q)` and force bounded `q`; orbit XOR collapses tiny examples.

**Fine print.** The sampling no-go applies only to one fixed code-oblivious coordinate sample. It does not exclude code-dependent dense structured folding or a reduction-specific tensor family.

**MUTATION TESTED.** Pure-power subcode, symmetric representative puncturing, code-dependent coordinate puncturing, permutation-orbit XOR, and random dense tiny folds. None gives useful parameters; a few dense tiny folds preserve distance, so the broad dense-fold route remains open rather than killed.

**MUTATION TESTED AND PARTLY PROVED THIS RUN.** Replicate a pointed code over an odd cyclic phase action and XOR tensor coordinates by diagonal orbits. `experiments/verify_cyclic_tensor_fold.py` exactly enumerates all mixed folded words. On 20 replicated hostile/random codes and 100 natural small invariant cyclic codes (`ell=3`), the fold obeys the proved bound

`delta_fold >= 1 + ceil((delta^2-1)/ell)`.

Proof: symmetrize any pointed mixed tensor word over the odd group. The distinguished bit remains one; on each free orbit the symmetrized value is the fold parity, so symmetrized weight is `1+ell(weight_fold-1)`. Full tensor pointed distance is `delta^2`. If a pointed minimum word is invariant, its square attains equality. This is now in `proof_cvp.md`. The earlier shorthand `ceil(delta^2/ell)` was weaker and hid the distinguished fixed orbit.

**Unresolved parameter wall.** Naive phase replication changes length to `1+ell(L-1)` and YES weight to `1+ell(d-1)` before folding, so the resulting length remains `Omega(ell L^2)`—worse than the unreplicated tensor. For reduced moving weights with base `q` versus `q+1` (or the parity-sharper `q+2`), the exponent after `k` squarings is `2^k`; useful iteration requires intrinsic large free symmetry and a sparse YES word without paying group order in padding.

**RESIDUAL-LINEAGE AUTOPSY.** `proof_cvp.md` now proves a parameter no-go for the natural residual action after diagonal quotient. If fixed/moving cross-sector orbits remain fixed at the next level, supported fixed weight obeys `s_1>=3`, `s_{i+1}>=s_i^2`, so final length `N_k>=3^{2^{k-1}}`. The certified ratio from the fold lemma is at most `N_k^{3/(Q ln 3)}` for base YES weight `Q` and NO `Q+1`, hence exponent `o(1)` as `Q` grows. `verify_residual_fold_parameters.py` checks 14,773 exact recurrence transitions.

**Fine print.** The theorem permits arbitrary odd group orders and actions free off their fixed sets, but assumes inherited fixed/cross sectors are not remobilized by an unrelated new symmetry. It does not cover a genuinely new action that mixes those sectors while preserving the folded code and sparse YES word.

**NEXT MUTATION TESTED AT COORDINATE LEVEL.** Classical biset composition spends a left group while retaining a fresh commuting right group, outside residual lineage. `experiments/verify_pointed_biset_cross.py` exactly checks 54 regular cyclic `(G,H)` products. The fresh `H` action is free on every quotient coordinate except the unavoidable classes `[u,*]`; if the first pointed factor has `R_U` moving regular orbits, there are exactly `1+R_U` fresh-action fixed coordinates. Thus fresh symmetry genuinely remobilizes old moving-moving sectors but a pointed cross sector still accumulates.

**CURRENT MUTATION PARTLY PROVED.** Plainly delete both star-cross sectors but retain the distinguished corner and moving-moving block. Contrary to the initial concern, this *reduced pointed tensor* has exact distance `1+(delta_*(D)-1)^2` for all mixed words, by a two-stage contraction/slicing proof. Under an odd group free on moving coordinates, orbit folding gives `1+ceil((delta-1)^2/ell)`. `experiments/verify_reduced_orbit_fold.py` checks 100 deterministic randomly generated reduced codes and 100 invariant folds exactly; proof is in `proof_cvp.md`.

This removes the fixed cross sectors that drove the residual-lineage theorem. The remaining construction need is a chain of bimodule codes whose fresh action lives on the reduced moving sector, with an invariant sparse YES word and explicit generator recurrence. Coordinate bisets alone are insufficient, but the earlier residual no-go no longer applies verbatim to this reduced product.

**END-TO-END ASSEMBLY TESTED.** `experiments/verify_reduced_fold_3dm.py` starts from exact 3DM YES distance 3 and NO odd-cover distance 5, installs one `Z3` symmetry, and iterates reduced residual folds twice. Exact mixed-word enumeration gives moving distances YES `9,27,243`, NO `15,75,1875`; ratios are exactly `(5/3)^(1,2,4)`. Lengths are `25,193,12289`. This validates functorial residual symmetry and ratio squaring, but also illustrates conserved exponent/output blowup.

**NON-INVARIANT SUPER-BUDGET MUTATION TESTED.** To avoid paying group order in YES weight, give each cyclic sheet an independent pointed 3DM witness (minimum lies on one sheet). For `ell=3,5,7,11`, exact folds on YES distance 3 and NO distance 5 retained full squares `9` and `25`, despite orbit lower bounds as small as 1 and 3. `verify_superbudget_3dm.py` checks this end to end. Broader cyclic searches (`verify_noninvariant_superbudget.py`, `verify_noninvariant_random_codes.py`) found no nontrivial `ell>d>1` case attaining the orbit floor: observed cases had `d=1`, or folded distance stayed much larger. Finite evidence only.

**CURRENT STATUS AFTER CONSTRUCTION ROUND 3.** Harvest found no unfinished background jobs. At the user's checkpoint, oracle was `$13.81/$23.94`; only `$10.13` was non-oracle, so dollar attribution could not safely certify that construction alone exceeded 40%. I therefore treated quarantine as binding and made every subsequent research action a construction or exact attack on a proposed construction—eight new verifier scripts plus an explicit CVP basis transfer—without another oracle call.

**Structured autocorrelation mutation tested.** `verify_cyclic_ideal_superbudget.py` exhausts 116 binary cyclic ideals of odd length at most 31 with parity star form. Among 94 nontrivial `ell>d>1` cases, all 94 compress below `d^2`; best examples have `(ell,d,d')=(31,11,11)` rather than `121`. None reaches the generic orbit floor. This is a genuine positive construction signal absent from direct-sum sheets.

**Formula-derived cyclic closure autopsy.** The immediate attempt to install that symmetry directly on 3DM—embed triple coordinates in `Z_11` and close the pointed instance code under all shifts—destroys the gap completely. `verify_cyclic_closure_3dm.py` exactly checks 400 assemblies (20 YES and 20 NO instances, ten embeddings each): every transformed code has moving distance 1 and folded distance 1. **AUTOPSY:** shifted affine generators span singleton-like pointed combinations, erasing global incidence soundness. **MUTATION TESTED:** keep the instance code intact and tensor it with a separate cyclic-ideal catalyst instead of closing it under shifts.

**Cyclic catalyst mutation.** For the length-15 dimension-3 cyclic ideal generated by `(x^4+x+1)(x^4+x^3+1)(x^4+x^3+x^2+x+1)`, odd distance and correlation-image odd distance are both 5. Coupling this catalyst to 3DM and folding only phase gives exact moving distances YES `15 -> 45` and NO `25 -> 125`, hence ratio square `(5/3)^2`; `verify_cyclic_ideal_3dm.py` enumerates every mixed word. `verify_cyclic_catalyst.py` checks 100 arbitrary small pointed outer codes and obtains exact distance `5d^2`. This is rigorous by ordinary pointed tensor multiplicativity plus the computed fixed catalyst distance.

**CATALYST AUTOPSY / PARAMETER THEOREM.** Any pure tensor catalyst with output length `L` and common YES/NO distance multiplier `a` maps `n→Ln²`, `d→ad²`, `b→ab²`. Therefore standard rank exponent becomes `2log(b/d)/(2log n+log L)`, never larger than the base exponent, regardless of whether the catalyst family grows. `verify_catalyst_exponent_bound.py` checks 17,151,060 finite tuples; the displayed logarithmic identity is the proof. The earlier fixed-catalyst recurrence check remains useful implementation evidence.

**MUTATION TESTED.** `verify_asymmetric_hash_fold.py` applies 1- and 2-sparse deterministic hash maps to reduced 3DM squares, using the same map for ten planted YES and ten exact NO instances. It exactly checks 866 valid map/sample combinations. Best uniform finite ratio is `7/5` at 32 outputs, with standard rank exponent `0.0962`, below unfurled `25/9` at length 65 (exponent `0.2447`). **AUTOPSY:** cancellation shrinks NO at least as aggressively as uniform YES completeness; most maps collapse the gap to one. This kills the tested formula-oblivious sparse-hash mutation, not code-dependent or algebraically asymmetric folds.

**NEXT MUTATION.** A code-dependent fold may inspect the instance parity-check/kernel but must be computable without knowing SAT. Search exact tiny maps optimized against the entire affine fiber using only linear-algebraic invariants (not YES witnesses), then test transfer across isomorphic relabelings and adversarial NO instances.

### I08 — Sparse global algebraic dictionary — untested
**Mechanism.** Avoid complete-assignment columns. Use polynomially many sparse algebraic generators whose Boolean combinations encode assignments/clauses globally, while a nullspace/girth/integrality theorem makes every spurious representation polynomially heavier.

**Position against map.** Must not factor through bounded-degree local signatures, proper marginals, or bounded-fan-in transcript rows. Must use genuinely global rows but not enumerate `2^n` assignments.

**First test requirement.** Specify an explicit matrix for arbitrary 3CNF; brute-force the all-eight core and twisted holonomy instance; compare exact YES and NO coset weights.

### I09 — Concatenated pointed-code gap multiplication — wounded
**Mechanism.** Replace huge tensor coordinates by inner encodings/concatenated products whose length grows only multiplicatively by a fixed polynomial while pointed distance compounds. Tailor inner code to the current outer pointed code.

**AUTOPSY (literature-level).** Equidistant inner codes exactly preserve symbol-weight ratios; expander/AEL amplification is saturating and can flatten nearby ratios; sparse expander images give only approximately linear support growth. No classical composition found compounds the ratio at polynomial length.

**Fine print.** This is not an impossibility theorem for tailored nonlinear block grouping or a reduction-specific alphabet. It rules out treating standard concatenation/distance amplification as a black-box multiplier.

**MUTATION TO TEST.** Couple exact-cover coefficients through one shared dense-coset/inner-code coefficient vector rather than encode output symbols independently; test whether the transform remains affine in base distance (likely) or separates illegal quotient classes.

### I10 — Exact-cover incidence + relative quotient distance — wounded
**Mechanism.** Start from the BMT binary incidence reduction for exact 3-dimensional matching. Let the syndrome fiber be `x0+C`. Define a subspace `B⊆C` generated by differences of legal perfect matchings (or by explicit local exchange boundaries). Seek an explicit polynomial-size embedding into a larger pair `B'⊆C'` with large `d(C'/B')`, while preserving a sparse representative for every perfect matching. Illegal parity covers must map to `C'\B'`.

**Position against map.** Columns are allowed triples, not local assignment truth tables or complete assignments. Soundness begins with global incidence counting. The quotient explicitly permits short differences among multiple legal witnesses, avoiding the ordinary-girth obstruction.

**Unproved core lemma.** An efficiently generated boundary space must contain all legal matching differences but no illegal parity-cover difference. If `B` is simply the span of all legal differences, computing it may require finding perfect matchings and may collapse illegal vectors into the same span. If generated by local exchanges, disconnected/global matching components may escape or illegal parity cycles may be boundaries.

**EXACT TEST OUTCOME.** `experiments/verify_exchange_quotient.py` exhaustively checked 120 small 3DM dictionaries, including 20 NO instances with parity covers. In 66 YES instances, an illegal odd cover shared a perfect matching's class modulo the span of all 2↔2/3↔3 packing exchanges. More strongly, in 32 instances an illegal odd cover lay in the affine span of the perfect matchings themselves—the *minimal* affine class any quotient must identify if all perfect matchings are assigned one cheap class. Lightest examples had weight 5 versus matching weight 3.

**AUTOPSY OF CURRENT FORM.** Quotienting all legal differences necessarily quotients every odd XOR of legal witnesses. When three perfect matchings have an odd XOR that is not itself a perfect matching, an illegal cover is information-theoretically in the legal affine class; no relative-distance shell can charge it. Local exchange spans often make the collapse even worse.

**MUTATION.** Do not identify all legal witnesses. Either transform to a matching family whose odd affine closure contains only matchings (unique/canonical or affine-closed completeness), or give each legal class a separate sparse protected sector while charging their superpositions. Deterministic uniqueness is itself dangerous and unproved. This mutation must be tested before killing the broad relative-distance route.

### I11 — Homological exact-cover encoding — wounded
**Mechanism.** Interpret legal exchanges as boundaries in a sparse chain complex and parity-superposed nonmatchings as nontrivial homology. Use an explicit high-systole complex to force nontrivial classes to have linear support.

**Position against map.** Directly targets odd holonomy rather than enforcing bounded local marginals. Relative homology allows many short legal representatives.

**Risk.** The map from arbitrary SAT/3DM to homology may itself be a local tableau/marginal construction, restoring virtual measures. Attaching a fixed high-systole complex does not ensure illegal parity covers land in nontrivial classes.

**First test outcome.** The quotient computation in `verify_exchange_quotient.py` already gives the base chain-complex answer: any boundary space containing all legal differences also contains illegal odd XORs on 32 tested instances. Thus a fixed high-systole shell applied after this classification cannot rescue those classes.

**AUTOPSY.** F2 homology is linear, so declaring every legal witness homologous also declares their odd affine combinations legal. The inherited local holonomy issue is replaced by an affine-closure issue.

**MUTATION.** Use filling *area* with separate legal fillings rather than one homology class, so odd superpositions could require many 2-cells even when homologically trivial. Must explicitly prevent the XOR of three cheap legal fillings from being another cheap filling; ordinary linear chain weight makes that difficult.

### I12 — Global Lagrange/RS error-budget shell — wounded
**Mechanism.** Interpolate triple-incidence columns as global low-degree evaluation words; use identity error columns. A parity-coverage defect is a nonzero polynomial and has large evaluation weight.

**AUTOPSY.** Every odd cover has exactly the same interpolation polynomial as a perfect matching: the constant one. Thus the shell charges only vectors already outside the BMT syndrome fiber, while the hard `q+1` odd covers cost zero errors.

**MUTATION.** Interpolate labels of quotient defect classes rather than raw element coverage. This is conditional on a surviving non-affine classifier and currently collapses back to I10.

### I13 — Bose–Chowla/Sidon shielding of defect columns — wounded
**Mechanism.** Give unavoidable defect absorbers additive signatures with no short integer relation, forcing high coefficient norm.

**AUTOPSY.** Clean odd covers avoid defect columns entirely. Binary expansion introduces carry/slack interfaces that risk the proved affine exact-fiber repairs.

**MUTATION.** Shield representatives of a classifier that every NO fiber must use. Again conditional on solving I10's classifier problem; no such classifier exists here.

### I14 — Pfaffian parity canonicalization + BCH shell — untested
**Mechanism.** In a tractable matching family, compute the XOR of all perfect-matching indicators by Pfaffian methods and use it as a canonical center for a high-girth shell.

**Risk.** The aggregate can be dense, vanishes for even witness count, and completeness still requires annihilating all legal differences, triggering I10's affine-span collapse. General 3SAT matching families are not Pfaffian-tractable.

**MUTATION.** Use a deterministic family of forced-edge derived instances so one aggregate is useful, then encode a disjunction of centers. This risks exponential branching and has not been tested.

### I15 — Expander bundling of a relative pair — untested
**Mechanism.** Make local legal exchanges cheap within bundles while global defect classes touch many expander neighborhoods.

**Risk.** Matching witnesses and many odd covers are both globally spread, so bundle weight saturates for both and flattens the ratio. If an illegal cover is already in the legal affine class, no linear bundling separates it.

**MUTATION.** Bundle only coordinates participating in certified defect patterns, leaving one matching-supporting dictionary unbundled. Requires a matching-independent defect certification.
