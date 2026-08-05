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

### I16 — Code-dependent generator-column type puncture — wounded
**Mechanism.** Inspect a reduced tensor code by Gaussian elimination, group
moving coordinates having the same generator-column type, and retain
`ceil(m_a/B)` representatives from each multiplicity class.  This is
basis-invariant and does not inspect a nearest word.  Every codeword's weight
`w` and punctured weight `w'` obey `w/B <= w' <= w/B + a`, where `a` is its
number of active types.

**EXACT TEST OUTCOME.** `verify_code_dependent_type_fold.py` applies the rule
to every mixed word in ten tiny YES and ten NO 3DM reduced squares, checks the
rounding inequality and coordinate-relabeling invariance exactly.  At `B=2`,
the uniform gap drops from `25/9` at length 65 to at most `13/9` with maximum
length 51; larger budgets collapse the sampled gap to one or below.  No tested
budget improves the standard rank exponent.

**AUTOPSY.** Generator type multiplicity is not aligned with coset distance:
the adversarial YES codes can have 49 active types while another code has
nine.  Rounding loss is controlled by active-type count rather than the
YES/NO minimum and harms NO at least as much as worst-case YES.

**MUTATION TESTED.** Switch from generator types, whose deletion changes the
Hamming objective, to *parity-check* parallel classes, for which exact coset
distance is preserved.  See I17.

### I17 — Exact parity-check parallel simplification after tensoring — killed for BMT reduced tensors
**Mechanism.** For binary syndrome decoding merge all identical nonzero
columns of `H` and delete zero columns.  Taking the parity of selections in
each class proves exact preservation of every target's minimum Hamming weight.
This operation is deterministic, code-dependent, and basis-invariant.
Repeated reduced tensoring followed by exact simplification would solve the
length wall if only polynomially many column types survived.

**EXACT TEST OUTCOME.** `verify_parity_type_tensor.py` alternates reduced
pointed tensoring, conversion to an explicit affine parity-check fiber,
parallel simplification, and re-homogenization.  On tiny 3DM YES/NO fibers the
formal/type counts are `8 -> 64 -> 4096`: every column is distinct through two
squarings.  Mixed moving distances remain exactly `3^(2^i)` and `5^(2^i)`.

**AUTOPSY (rigorous).** For `K=ker H`, equal parity-check columns imply
`e_i+e_j in K`, and a zero column implies `e_i in K`.  Thus `d(K)>=3` makes
`H` simple.  In BMT 3DM, the moving linear span `C` contains the incidence
kernel and a target representative; every nonzero word in `C` has weight at
least three (kernel weights one/two are impossible for distinct nonzero triple
columns; target-fiber words have weight at least `q>=3`).  The reduced tensor's
star-zero code is a subcode of `C tensor C`, so its distance is at least nine.
Inductively every parity-check matrix remains simple.  Exact simplification
therefore never compresses this ladder.

**MUTATION TESTED.** Generator-type approximate puncturing (I16) was tested
first and loses the gap.  Both natural sides of column-type compression are
therefore buried for this BMT reduced-tensor family; a different base with
many parity-check parallels would already have kernel distance at most two
and requires a separate soundness invariant.

### I18 — Direct integer exact-cover CVP + variable pair projections — wounded additive-gap construction
**Mechanism.** For 3DM incidence `A`, use the explicit full-column-rank
integer basis `B=[I; M A]` and target `[0; M 1]`.  In the exact fiber
`Az=1`, summing one vertex part gives `sum z_j=q`; for integral `z`,
`sum z_j^2>=sum z_j=q`, with equality iff every coefficient is Boolean.
Thus YES has squared distance `q`, while NO exact-fiber points have at least
`q+2` (the difference `sum(z_j^2-z_j)` is a positive even integer).  Taking
`M^2` above the NO threshold excludes residual points.  This is a clean direct
integer-CVP version of exact-cover hardness, but only additive gap.

**EXACT TEST OUTCOME.** `verify_integer_3dm_cvp.py` performs meet-in-the-middle
signed search over `[-2,2]^8` on 40 YES and 40 NO tiny instances and checks the
actual lattice residual.  YES squared norms are all 3; NO norms are 5 (35), 7
(1), 9 (2), 13 (2).  The lightest NO witness uses coefficients
`(1,0,-1,1,0,1,0,1)`, confirming that soundness must include signed points.

**MUTATION TESTED.** Append all three 2D pair-projection rows and fix their
target to the three permutation matrices of a matching.  On four YES/four NO
instances, exhaustive `{-1,0,1}` search over all 36 consistent target triples
gives YES norm 3 and *no* NO exact-fiber point.  A reduction does not know
which of the `(q!)^2` targets a satisfying matching realizes.

**SECOND MUTATION TESTED.** Make the three projection tables themselves
integer lattice coefficients `p=Pi(z)` and impose their row/column sums, so a
single fixed target existentially permits every permutation.  This is
polynomial size and `verify_variable_pair_projection_cvp.py` checks all signed
vectors in `[-2,2]^8` on 40 YES/40 NO instances.  With equal weights the exact
gap is squared norm `12` versus `14`; weighting original triples by
`1,2,4,8` gives finite ratios `7/6, 19/15, 29/21, 49/33`, all still additive.

**AUTOPSY OF GAP AMPLIFICATION.** Every integer table with row sums one has
squared norm at least `q`, equality iff it is a permutation.  Thus the
variable-target trick replaces an exponential disjunction by an additive
integrality baseline: YES pays `q` for `z` and for each of three projections.
A nonintegral table adds only an even constant.  Weight replication magnifies
both the YES baseline and defect, asymptotically retaining a `1+O(1/q)` ratio.
The polynomial classifier is valid but does not supply a polynomial gap.

**NEXT MUTATION.** Seek a zero-baseline linear representation of the union of
permutation matrices, or a multiplicative composition of this integrality
classifier with submultiplicative output.  Ordinary table coefficients cannot
do this because charging their Euclidean norm creates the `q` baseline.

### I21 — Homogenized integer exact-cover tensor — promising mixed-word finite signal, rank wall
**Mechanism.** Homogenize integer exact cover as
`L(T)={(z,s):Az=s*1}` and distinguish `s=1`.  YES pointed squared norm is
`q+1`; NO is at least `q+3`.  Tensoring may multiply this norm gap, but unlike
binary product codes arbitrary mixed lattice tensors can be shorter; the
needed invariant is Haviv--Regev's every-partner/all-sublattices property.

**EXACT TEST OUTCOME.** `verify_homogeneous_integer_tensor.py` constructs exact
short integer bases for four YES/four NO tiny 3DM lattices, searches pointed
coefficients in `[-2,2]`, then exhausts all mixed tensor coefficients in
`[-1,1]`.  Base squared norms are YES 4 and NO 6 or 8; tensor minima are
exactly 16 and 36 or 64.  Every tested mixed minimum is multiplicative, not
just a pure square.

**MUTATION TESTED: HIGHER RANK.** `verify_highrank_integer_tensor.py` uses
Smith decomposition to obtain saturated exact Z-bases for six YES/six NO
rank-three lattices, certifies bounded saturation, and exhausts all `3^9`
mixed tensor coefficient matrices.  Base squared norms 4 versus 6 become
exactly 16 versus 36 in every case.  The harvested coefficient-`[-2,2]`
search is now reproduced by `verify_highrank_tensor_C2.py`: three YES/three NO
instances exhaust `5^9` mixed matrices and remain exactly 16 versus 36.

**AUTOPSY OF NAIVE ALL-SUBLATTICES LEMMA.**
`verify_tensor_subdeterminants.py` enumerates 13 primitive coefficient vectors
and 78 rank-two pairs for each of twelve YES/twelve NO rank-three lattices.
Unrestricted NO lattices have the same minimum rank-one norm 4, rank-two Gram
determinant 12, and support 6 as YES, due to short homogeneous `s=0`
directions.  Thus a theorem lower-bounding *every* NO sublattice more strongly
than YES is false in this form, despite pointed tensor multiplicativity in the
bounded searches.

**MUTATION TESTED: POINTED SUBLATTICES.**
`verify_pointed_sublattice_diagnostics.py` restricts to rank-one directions
with nonzero `s` and rank-two sublattices on which `s` is primitive.  Across
20 YES/20 NO rank-three lattices, minima separate: rank-one norm/support
`4/4` versus `6/6`, and rank-two Gram determinant/support `12/6` versus
`20/8`.  This reverses the unrestricted autopsy and is a genuinely promising
finite invariant; no quantified theorem is claimed.

**WIDER MIXED SEARCH HARVESTED.** A background `[-2,2]^9` mixed tensor search
finished on three YES/three NO instances (1,953,125 coefficient matrices per
instance), again exactly multiplicative `16` versus `36`.  The result is
reproducible in `verify_highrank_tensor_C2.py`.

**COEFFICIENT-BOX MUTATION TESTED.**
`verify_pointed_rank3_coeff_bound.py` expands from `{-1,0,1}` to all 145
primitive directions in `[-3,3]^3` and at least 7,480 primitive-functional
rank-two pairs on each of ten YES/ten NO lattices.  The same gaps persist:
rank-one 4 versus 6; rank-two determinant 12 versus 20 and support 6 versus 8.
This reduces the risk that the signal is a tiny coefficient-box artifact.

**RANK-FOUR MUTATION TESTED.** `verify_pointed_rank4_diagnostics.py` checks
20 YES/20 NO rank-four (`m=10`) lattices: all 40 primitive box-one directions,
702 primitive-functional rank-two pairs, and at least 451 pointed mixed tensor
combinations of support at most three per instance.  The same minima persist:
rank-one 4/6, rank-two determinant 12/20 and support 6/8, sparse tensor 16/36.

**CONVERGE RESULT / THEOREM.** The rank-two signal is proved universally:
for every NO rank-two `K<=L_A` with `s(K)=Z`,
`det_Gr(K)>=4(q+2)` and support at least `q+5`, by mod-2 Pluecker counting.
More generally, rank `r` has at least `ceil((q+3)4^(r-1)/r!)` odd maximal
minors.  `verify_pointed_tensor_theorems.py` checks the exact finite claims.

**AUTOPSY OF ARBITRARY-PARTNER HOPE.** Primitive-functional multiplicativity
is false: `Z^2` with `s=(2,5)` has pointed squared minimum 5, but its self
tensor has a mixed norm-4 matrix with functional one.  The sufficient pointed
determinant profile requires rank-two determinant `Omega(q^2)`, whereas the
proved incidence bound is only `4(q+2)`.

**SURVIVING CERTIFICATE.** Coordinate reduction mod 2 gives pointed binary
distance `q+1` versus `q+3`, exactly multiplicative against all mixed tensors;
integer squared norm dominates parity weight.  Thus tensor soundness is
rigorous, but ordinary tensor rank growth leaves the approximation exponent
vanishing.  The current need is solely submultiplicative rank compression that
preserves this parity certificate; previous orbit/hash/type folds failed.

### I22 — Weighted set-support compression of pure-power tensors — killed for general BMT amplification
**Mechanism.** For binary vectors, a tensor coordinate
`x_{i1}...x_{ir}` depends only on the underlying set `S={i1,...,ir}`.  In the
pure-power subcode `P_r(D)=span{x^tensor r:x in D}`, every mixed word therefore
has one bit per nonempty `S` of size at most `r`, with integer multiplicity
`w_S=|S|! S(r,|S|)`.  Weighted Hamming distance is *exactly* full tensor
Hamming distance.  Represent each integer weight as a deterministic
`O(log w_S)` sum of squares from its binary expansion; scaling explicit
integer rows realizes the weighted metric as ordinary Euclidean squared norm.
Construction-A on the compressed binary code then gives an explicit integer
CVP basis.

**EXACT TEST OUTCOME.** `verify_weighted_symmetric_cvp.py` checks 72 random
codes, every mixed pure-power word, exact multiset-orbit weighting, and explicit
integer bases.  `verify_set_support_weighted_cvp.py` strengthens multiset
orbits to set supports on 100 random cases and tiny 3DM.  For the 3DM code of
moving length 8, compressed lengths saturate at 255 while distances remain
exactly `3^r` versus `5^r` through `r=12`.

**MUTATION TESTED: FUNCTION TYPES.** Equal set-support Boolean functions on
the message space are merged and their weights summed.
`verify_function_type_weighted_cvp.py` checks 405 random cases and 20 3DM
parameter cases.  For 3DM dictionaries of sizes 8,9,10,11,12 (code dimensions
2,...,6), type counts at large `r` are 6,20,59,251,1158, much smaller than
`2^n` but growing rapidly with code dimension.

**DIMENSION AUTOPSY (RIGOROUS).** If `dim D=k`, its coordinate linear forms
span the dual message space.  Products of `r` such forms span every nonconstant
squarefree monomial of degree at most `r` (expand products of linear
combinations and pad lower degrees by repetitions, using `x^2=x`).  Therefore

`dim P_r(D)=sum_{j=1}^{min(k,r)} binom(k,j)`, saturating at `2^k-1` for `r>=k`.

Any exact linear/CVP realization has rank at least this dimension, regardless
of coordinate merging or weights.  `verify_pure_power_dimension.py` checks 448
random cases and increasing 3DM dimensions.  Thus output polynomiality forces
this binomial sum to be polynomial; for growing `r` and nonlogarithmic `k` it
fails.  A BMT fiber with `k=O(log input)` could itself be exhaustively decoded
in polynomial time, so it cannot provide NP-hardness unless P=NP.

**MUTATION TESTED.** Function-type merging is the maximal exact coordinate
quotient by evaluations and was tested above; the dimension theorem shows it
cannot evade rank.  Weighted pure-power compression is therefore killed as a
route from general BMT instances, despite being an exact and useful finite
construction.  A surviving tensor compressor must discard part of
`P_r(D)` while retaining pointed distance, as the earlier pure-power idea
already did relative to the full tensor, or use nonlinear/nonlinear-rank
representation outside an explicit lattice basis.

### I23 — Weight-class nonlinear compressor — killed by NP-hard construction step
**Mechanism.** For affine fiber `F`, create a pointed generator `(1,e_w)` for
each attainable weight `w=|x|`, and give class `w` Euclidean weight `w^r`.
Every pointed mixed sum uses an odd number of generators, hence leaves an odd
occupied class; distance is exactly `1+(min_{x in F}|x|)^r`.  Output has only
`m+2` weighted coordinates, independent of tensor order and code dimension.

**EXACT TEST OUTCOME.** `verify_weight_class_compressor.py` checks 40 YES/40
NO BMT instances and explicit weighted CVP bases.  For `r=16`, the finite
ratio is `(1+5^16)/(1+3^16)>3500`, with only ten class coordinates.

**AUTOPSY.** Constructing the class dictionary requires knowing whether weight
`q` is attainable.  In BMT this is exactly existence of a perfect matching,
the NP-hard source decision.  The compressor is nonlinear in the input code,
not a polynomial-time reduction.

**MUTATION TESTED.** Include every class permitted by polynomially known BMT
counting/parity (`w>=q`, `w=q mod 2`) rather than exact attainability.  This
always inserts class `q` into NO instances and makes YES/NO compressed distance
identical.  Thus the compact class mechanism buries the hardness in generator
construction.

### I24 — Deterministic sampled pure-power functions — killed after generalization mutation
**Mechanism.** Sample polynomially many ordered tensor coordinates from a
canonical hash of the row-reduced input code.  Merge duplicate product
functions and retain their sample multiplicities as Euclidean weights.  This
discards most of `P_r(D)`, evading its dimension lower bound; exact message
enumeration attacks every mixed image word on tiny codes.

**INITIAL EXACT SIGNAL.** `verify_sampled_pure_power_fold.py` checks 1,400
parameter/family combinations on ten YES/ten NO `m=8` instances.  One public
setting `(r,M,salt)=(8,256,19)` has worst YES distance 1 and best NO 7, a
finite ratio 7, substantially above the base 5/3.

**GENERALIZATION MUTATION TESTED.** Freeze that setting before expanding the
test family.  `verify_sampled_fold_generalization.py` checks 50 YES/50 NO at
each `m=8,...,12` plus independently permuted presentations.  The ratio falls
to 4/3 already at `m=8`, then 1/3, 1, 1, 1; permutations do not rescue it.

**AUTOPSY.** The sampler overfit a ten-instance finite family.  As code
dimension grows, polynomially many sampled products miss most constraints and
both YES/NO images acquire pointed weight one.  The map is also presentation
sensitive through its canonical bit-string seed, though the explicit
permutation attack was no worse than base.  No asymptotic soundness lemma
survives.  Mutation tested; route killed in this deterministic sampling form.

### I25 — Low-dimensional exact-power base — positive finite toy, asymptotically incompatible with hardness
**Mechanism.** Combine exact weighted pure-power compression with BMT codes of
small dimension `k`; output rank is about `2^k r log m` while the Euclidean gap
is `((q+3)/(q+1))^(r/2)`.

**EXACT TEST OUTCOME.** `verify_exact_power_polynomial_base.py` searches five
YES/five NO q=3 families at m=8,...,12.  Finite exponents are large; the best
toy has k=6, r=12, rank proxy 3024, and ratio 11.390625.

**AUTOPSY.** This is fixed-q/small-k finite behavior.  For an asymptotic
NP-hard base, `2^k` cannot be polynomial with enumerable messages: if
`k=O(log input)`, exhaustive decoding of the affine fiber is polynomial.  If
`k=omega(log input)`, exact compression rank `2^k` is superpolynomial once
`r>=k`; for `r<k`, the binomial dimension wall still applies.  No separate
mutation remains beyond function merging and sampling, both already tested.

### I20 — Determinant/exterior global permutation dictionary — wounded, explicit-size wall
**Mechanism.** Use the Cauchy--Binet determinant polynomial whose monomials
are exactly permutations.  Charge a coefficient table over permutation
monomials and optionally its aggregate exterior-power/compound states.  This
is genuinely global and avoids bounded-fan-in tableau interfaces.

**EXACT TEST OUTCOME.** `verify_determinant_permutation_dictionary.py`
exhausts all signed affine coefficient vectors in `[-2,2]^6` for `q=3` and
all 12,144 support-three trades for `q=4`.  Charging only monomial coefficients
gives legal/virtual squared costs 1/3.  Adding the table gives 4/8 at `q=3`
but only 5/7 at `q=4`.  Top determinant/sign state gives 2/4 in both cases.
All compound states give 8/22 and 16/34, respectively: finite constant
separation, not an asymptotic construction.

**AUTOPSY.** The global determinant selects permutations as monomials, but an
explicit linear dictionary has `q!` coefficient columns.  Compressing it by a
polynomial determinant circuit restores the already-proved local tableau
faults; retaining only top determinant or low exterior states admits
support-three affine virtual permutations.  Exterior-state baselines also
grow with their dimension.

**MUTATION TESTED.** Add every compound/exterior state, including middle
powers, rather than only the top determinant.  Exact support-three search still
finds constant-factor virtual states, while explicit state/dictionary size is
exponential.  This kills the tested explicit determinant dictionary, not a
hypothetical succinct global nonlinear lattice constraint.

### I19 — Linear feature-cost shell on 3DM — killed for tested global/sparse features
**Mechanism.** Add explicit variables `z=Fx` to binary BMT syndrome decoding
and charge `R` copies of `z`, so exact cost is `|x|+R|Fx|`.  Test global
AB/AC/BC pair projections, deterministic sparse hashes, and their hybrid.

**EXACT TEST OUTCOME.** `verify_feature_shell_3dm.py` checks every odd cover
on 40 YES and 40 NO instances across 45 feature/replication choices and also
constructs an explicit augmented syndrome matrix for a cheating witness.  The
best uniform ratio is only `14/12=7/6` (one pair-feature copy), below the base
`5/3`; hashes and hybrids frequently make a NO point cheaper than worst-case
YES.

**AUTOPSY.** Over GF(2), feature cost depends on parities of a cover's global
projections.  Perfect matchings have varying feature vectors, forcing a large
worst-case completeness baseline, while signed/odd NO covers can cancel the
same rows.  Replication magnifies baseline and cheat together.

**MUTATION TESTED.** Hybridize genuinely global pair projections with sparse
hash/expander-style rows and replicate up to 16 times.  All tested hybrids are
worse; mutation killed.  The integer fixed-pair-target mutation avoids feature
cost and instead imposes exact projection values, recorded separately as I18.

### I26 — Canonical modular-Kronecker tensor fold — killed for the tested frozen family
**Mechanism.** Canonicalize the base pointed code under row-basis changes and coordinate relabeling. Assign powers of two to canonical generator-column types, give the two ordered tensor positions disjoint exponent ranges, and XOR reduced-square coordinates by their exponents modulo fixed `M_j<=32`.

**Expected move.** Modular sparse-PIT buckets might retain every low-weight NO mixed word while using fewer than the 64 unfurled moving coordinates.

**Falsification and exact outcome.** `experiments/verify_sparse_pit_tensor_fold.py` freezes 35 rules (singletons `2..32` and four prime-prefix tuples), then enumerates every mixed image word on ten YES/ten NO `q=3,m=8` codes. All 35 are strictly compressed, but none has uniform ratio above one; 23 have ratio exactly one and the rest invert the gap. The precommitted tuple `(5,7,11,13,17)` has worst YES 17 and best NO 5 at ambient rank 53. The verifier also checks all `806400` moving-coordinate relabelings. This kills only this finite exponent/modulus family, not every dense code-dependent fold.

**AUTOPSY.** Modular parity collisions create cheap mixed words in the NO image at least as quickly as in the YES image. Post-hoc modulus selection is disallowed and would not help this family anyway.

### I27 — Collision-seeded nonbacktracking Schur walks — promising finite signal, asymptotics open
**Mechanism.** Keep the original 3DM triple coordinates and add one Boolean product coordinate for each ordered nonbacktracking walk in the triple-incompatibility graph. A matching activates no walk coordinate; a NO odd cover contains collisions that may activate many indexed walks. The linear code is the span of all nonlinear lifts of the affine fiber, so soundness is attacked against every mixed word.

**PRECOMMITTED OUTCOME.** `experiments/verify_nonbacktracking_schur_walks.py` tests exact walk lengths 2, 3, and primary length 4. On ten planted YES and 200 deterministic exact NO `q=3,m=8` dictionaries, length 4 has worst YES 3, best NO 33, ratio 11, and maximum nominal pointed length 1277. Its finite rank exponent is `0.3352636`, above the original `log(5/3)/log(9)=0.2324868`. All 103,136 tested mixed words were enumerated; the inherited first ten NO instances are included.

**HOSTILE DIAGNOSTICS.** The complete `q=2` all-eight dictionary has a cheapest illegal mixed word of cost 6 with no walk charge, and the union of three twisted `q=3` permutation matchings has an illegal all-nine mixed word of cost 9 with no walk charge. Thus affine XORs of legal lifts can cancel the entire shell even though the tested NO families retain a gap. Relabeling covariance was checked on all `21*8!` permutations plus the nine-coordinate reverse test.

**BLOCKERS.** This is finite evidence, not a lemma. For `r=Theta(log q)`, the walk count `m Delta^(r-1)` is polynomial only under a missing bounded-incompatibility-degree reduction. Indexed walks can repeatedly traverse a constant collision cycle, so the finite amplification may be duplicate-coordinate replication rather than global soundness. No asymptotic NO lower bound, polynomial output proof, NCP reduction, or CVP hardness follows.

### I28 — Nonsemisimple truncated-algebra multiplication fold — killed for the frozen rule
**Mechanism.** Freeze `A=F_2[u]/(u^16)`. For triple coordinate `j`, put `h_j=1+(c_j mod 7)` using its canonical incidence-column integer and `a_j=1+u^{h_j}+u^{2h_j+1}`. Map ordered reduced-square coordinate `(i,j)` to the 16 coefficient bits of `a_i a_j`, retaining the pointed corner.

**EXACT OUTCOME.** `experiments/verify_nonsemisimple_multiplication_fold.py` enumerates every mixed image word on ten YES and 200 exact NO `q=3,m=8` dictionaries. The fold compresses nominal length 65 to at most 17 active coordinates, but worst YES is 4 and best NO is 2, so the uniform ratio is `1/2` and the rank exponent is zero. The complete all-eight dictionary has the pointed corner-only image word of moving weight zero. Twisted holonomy has folded distance 3. All 846,911 tested coordinate relabelings/reverse spectra agree.

**AUTOPSY.** Truncated multiplication is commutative, so it identifies `(i,j)` with `(j,i)` and has a large structured mixed-tensor kernel. The unit constant terms and nilpotent layers do not align valuation with exact-cover soundness; cancellations shrink NO at least as strongly as YES. This kills only the specified `M=16` label rule, not all nonsemisimple algebras.

### I29 — Frozen rank-one `M_3(F_4)` ordered-pair fold — killed
**Mechanism.** Enumerate the 1,323 distinct nonzero rank-one `3x3` matrices over `F_4=F_2[a]/(a^2+a+1)`, sort their row-major entries lexicographically, assign the kth label to the kth sorted triple, and map ordered reduced-square coordinate `(i,j)` to the 18 binary coefficients of `L_iL_j`. This is genuinely noncommutative and has an explicit binary syndrome image.

**EXACT OUTCOME.** `experiments/verify_f4_ordered_pair_fold.py` enumerates every mixed image word on ten YES, 200 NO, twenty affine-closure, all-eight, and holonomy dictionaries. Worst YES is 3, best NO is 0, and maximum exact-transfer rank is only 4. Five YES and 112 NO dictionaries have pointed kernels; 18/20 affine-closure instances do too. Holonomy has distance zero. All-eight has distance one and a semantic illegal pure-square cost one. The rule fails every acceptance criterion.

**AUTOPSY.** Noncommutativity removes the automatic transpose symmetry but not low-rank bilinear identities. Lexicographically first rank-one labels occupy highly aligned rows/columns, so many products vanish or span only a few binary coordinates; orientation survives without support. This kills the frozen canonical rule, not every growing noncommutative family.

### I30 — Five-block `F_8` two-sided Vandermonde condenser — killed
**Mechanism.** Canonically sort the triple coordinates, identify the eight positions with `F_8=F_2[u]/(u^3+u+1)`, and apply five frozen `2xm`/`mx2` generalized-Vandermonde maps. Each `A_s W B_s` contributes four field symbols, hence 60 nominal binary moving coordinates. Every image is converted to an explicit syndrome fiber.

**EXACT OUTCOME.** `experiments/verify_f8_two_sided_condenser.py` enumerates 83,648 mixed words over ten YES, 200 NO, twenty affine-closure, all-eight, and holonomy dictionaries. There are no pointed kernels, but worst YES is 31 while best NO is 6; the uniform ratio is `6/31` and exponent zero at maximum exact-transfer rank 48. All-eight has distance 2 and a semantic illegal cost 2, below legal pure-square costs 6--10. Holonomy has distance/illegal cost 6 versus legal costs 15--28.

**AUTOPSY.** The blocks retain nonzeroness but not useful Hamming support. Vandermonde measurements densify different YES squares to 13--31 bits, while mixed NO matrices cancel to 6 bits. Stacking five blocks raises the completeness baseline without a proportional soundness floor. This kills the frozen family, not all code-dependent dense condensers.

### I31 — Canonical 64-coordinate polar shortening — killed
**Mechanism.** Sort the eight triple coordinates, order reduced-square pairs lexicographically, apply row-vector multiplication by `[[1,0],[1,1]]^tensor6`, and delete exactly transformed coordinates that vanish on the full star-zero subcode. This is an invertible dense transform before code-dependent shortening, not raw puncturing.

**EXACT OUTCOME.** `experiments/verify_polar_shortening.py` enumerates 33,636,544 mixed words over ten YES, 200 NO, twenty affine-closure, all-eight, and an eight-coordinate holonomy dictionary. Worst YES is 13 and best NO is zero; 3 YES, 38 NO, and 5 affine-closure images have pointed kernels. Retained ranks range from 9 to 63. All-eight retains 40 coordinates but has a corner-only image and a semantic illegal pure square of cost zero.

**AUTOPSY.** The polar transform is invertible, but deleting coordinates invisible to the star-zero subcode can delete the only separation between its affine pointed coset and the kernel. Canonicalization gives relabeling invariance, not metric polarization. This kills the frozen orientation/shortening rule, not every dense transform.

### I32 — Four-probe `A_4` convolution fold — killed
**Mechanism.** Model `PSL_2(F_3)` as the twelve even permutations `A_4`, assign the first eight lexicographic elements to sorted triple coordinates, and use the first representative of each of four conjugacy classes as probes. Ordered pair `(i,j)` contributes to bucket `lambda_i a_s lambda_j^{-1}`, giving 48 moving bits.

**EXACT OUTCOME.** `experiments/verify_a4_convolution_fold.py` enumerates 605,072 mixed words on ten YES, 200 NO, twenty affine-closure, all-eight, and eight-coordinate holonomy dictionaries. Main images have no pointed kernels, but worst YES is 20 and best NO is 10, so the ratio is `1/2` at exact-transfer rank 48. Canonical all-eight has a pointed kernel; 28,800 of all 40,320 assignments of the eight group labels also have one. Holonomy's semantic illegal cost 22 is below legal baseline 24.

**AUTOPSY.** Group product mixing preserves orientation but does not turn Fourier/quasirandom spread into Hamming support. Convolution buckets densify YES words to 12--20 while NO mixed words reach 10, and the group-algebra map has large hostile kernels. This kills the frozen `A_4` map, not growing quasirandom groups in general.

### I33 — Adversarial all-functional matroid-fold ILP — killed as scalable route
**Mechanism.** For a reduced tensor code of dimension `d`, enumerate all `2^d-1` nonzero row functionals and choose integer multiplicities of total length at most 64. The canonical ILP maximizes non-rank-one minimum minus rank-one maximum, then the non-rank-one minimum, minimizes length, and uses a fixed weighted row order. Constraints use only the generator and exact rank-one classification, not YES/NO labels.

**EXACT OUTCOME.** `experiments/verify_adversarial_matroid_fold.py` exactly solves every `d=4` pattern: nine YES and 195 NO instances. Every selected image has output rank 64 and pointed distance exactly 16, so the uniform ratio is one despite no kernels. The remaining one YES/five NO have `d=9`. All twenty affine-closure cases have `d=9` or 16, holonomy has `d=9`, and all-eight has `d=25`, requiring 33,554,431 row variables and 16,777,216 pointed constraints before tie-breaking.

**AUTOPSY.** The unrestricted tiny-code optimum is a simplex-like metric that equalizes every nonzero pointed message rather than preserving the 9-versus-25 source gap. More importantly, exact row selection grows exponentially in code dimension and is itself a decoding-scale separation problem. This kills the proposed exact ILP construction; it is not a theorem about efficiently generated dense rows.

### I15 — Expander bundling of a relative pair — untested
**Mechanism.** Make local legal exchanges cheap within bundles while global defect classes touch many expander neighborhoods.

**Risk.** Matching witnesses and many odd covers are both globally spread, so bundle weight saturates for both and flattens the ratio. If an illegal cover is already in the legal affine class, no linear bundling separates it.

**MUTATION.** Bundle only coordinates participating in certified defect patterns, leaving one matching-supporting dictionary unbundled. Requires a matching-independent defect certification.
