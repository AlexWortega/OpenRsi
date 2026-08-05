I use this obstruction key below:

- **O1 — Slack annihilation (G1):** free integer auxiliaries erase amplified residuals.
- **O2 — Noncomposition (G2/3/5):** fixed-marginal local isolation collapses under overlap via short circuits.
- **O3 — Invalid quotient (G6):** external filters, changed references, or an unrestricted mod-2 bypass invalidate CVP evidence.
- **O4 — Exact signed kernel (G7):** radix weighting cannot detect a residual-zero signed selector.
- **O5 — Low-degree parity/padding (G9):** degree-two moments admit the seven-term cube-parity repair, whose constant cost is diluted by padding.

## 1. Degree-three polynomial-calculus closure

**Core trick.** Introduce squarefree monomial variables and integer residual rows for clause indicators and multiplication identities, initially through degree three. Formula-adaptively close under multiplying existing equations by selected variables; an integral derivation of `1=0` would force a residual independent of selector representation.

**Expected move.** Degree three directly charges the G9 cube-parity vector; modest higher closure might eliminate global pseudo-moments and permit arbitrarily large residual scaling.

**Obstruction check.** **O1:** no free clause slack; every monomial auxiliary is anchored and identity-checked. **O2:** monomials are global across occurrences, not private fixed marginals, though new overlap circuits may remain. **O3:** all identities must be emitted in one fixed-target lattice; audit mod 2 explicitly. **O4:** the seven-term vector has nonzero cubic moment, but a higher-degree zero fiber would still kill it. **O5:** outside the degree-two assumption; padding still wins unless closure yields a uniform contradiction.

**Experiment/falsification.** Add all degree-three rows to the nine-clause instance; compute exact SNF/HNF and search unrestricted vectors through anchor excess 32. Kill on any zero-residual constant-cost vector.

**Likely death.** Worst-case formulas require polynomial-calculus degree linear in `n`, making the monomial lift exponential.

---

## 2. Relative BCH syndrome on the honest-assignment quotient

**Core trick.** Let `U` be the saturated integer span of differences between honest global selector configurations. Construct a deterministic BCH-style parity check on the quotient module, vanishing on `U` but having large Lee distance on harmful classes; realize congruences as `Hz-qy=s` inside the lattice.

**Expected move.** A harmful selector would require coefficient norm at least `T=m^{1+2c}`, producing a polynomial distance gap while all honest assignments retain one target syndrome.

**Obstruction check.** **O1:** congruence carries `y` recreate the slack risk; this route is outside O1 only if their norm is included in the proved quotient distance. **O2:** coding is global modulo all honest differences, not clause-private. **O3:** unlike G6, normalization, consistency, carries, and reference must all be fixed lattice coordinates; mod-2 bypasses are part of the test. **O4:** if the signed kernel lies in `sat(U)`, every such code is powerless. **O5:** likewise, cube parity must be nonzero in the quotient; otherwise padding remains fatal.

**Experiment/falsification.** On the nine-clause instance, enumerate honest configurations, compute `sat(U)`, and test whether the three- and seven-term attacks vanish modulo primes `2,3,5`. If not, search the smallest parity-check matrix attaining quotient distance 5.

**Likely death.** Harmful affine relations probably already belong to the saturated honest-difference span, or cheap carry vectors erase the code distance.

---

## 3. Cosystolic-expander selector complex

**Core trick.** Replace the factor graph by an explicit 2-complex: selector deviations are integer cochains, consistency rows are coboundaries, and extra dual/filling coordinates charge both noncycles and homologically nontrivial cycles. Honest assignments form a designated gauge submodule; cosystolic expansion should force every other class to have polynomial support.

**Expected move.** A localized clause repair must either expose many violated cells or acquire large filling norm, giving anchor excess `Ω(N^α)`.

**Obstruction check.** **O1:** filling variables are dangerous slack and must be anchored in the filling-norm objective. **O2:** global 2-cells deliberately couple overlap circuits rather than fixing private marginals. **O3:** use explicit integral boundary matrices and one target; no filtered cochains. **O4:** a residual-zero signed selector becomes a cycle and is charged only if it is outside the honest gauge or has large filling. **O5:** the cube-parity cycle should cease being local; padding cannot dilute it if the complex has a uniform cosystole.

**Experiment/falsification.** Attach the smallest tetrahedral/triangular cell completion to the nine-clause incidence graph. Use exact ILP to find the minimum-norm harmful cochain modulo honest gauges.

**Likely death.** The attack may be a small boundary, invisible because `∂²=0`; forcing large fillings may conflict with cheap honest assignment changes.

---

## 4. Totally-real number-field fingerprints

**Core trick.** Tag selector columns by algebraic integers in a totally real field and measure discrepancies with the trace quadratic form over all embeddings. Any nonzero integral fingerprint `a` satisfies `|Norm(a)|≥1`, hence `Σσ(a)^2≥D` in field degree `D`; unauthorized cancellation can therefore cost `Ω(√D)`.

**Expected move.** Choose polynomial degree `D=m^α` and tags separating all short harmful selector relations, while honest labels are canceled by global tag columns.

**Obstruction check.** **O1:** tags act directly on selectors, not a slack-cancelable residual; any denominator/carry would reintroduce O1. **O2:** use one global fingerprint system across overlaps. **O3:** emit the integral trace Gram matrix and an exact rational Euclidean realization; no embedding-based external test. **O4:** radix-zero attacks are charged if their tagged algebraic sum is nonzero. **O5:** tags are not restricted to degree-two moments, so cube parity can be separated; however padding wins if the honest trace baseline also scales by `D`.

**Experiment/falsification.** Use a degree-8 totally real field, assign tags to the nine-clause columns, evaluate both known attacks exactly, then enumerate all signed relations of `ℓ₁≤9`.

**Likely death.** Exact relations forced by completeness may survive every tagging, or the trace form may amplify completeness and soundness equally, leaving only a constant ratio.

---

## 5. Uniform Chvátal–Gomory closure encoded as CVP

**Core trick.** Start from the rational local-assignment polytope and uniformly generate a bounded number of Chvátal–Gomory or split-cut rounds. Encode each rounded inequality, including quotient variables, as an integer lattice residual; these global cuts can separate signed affine combinations invisible to moment equalities.

**Expected move.** A polynomial-size, polynomial-rank closure might force every unsatisfiable instance to violate an integral cut by one, after which scaling yields the gap.

**Obstruction check.** **O1:** quotient variables are potential slack; their anchors and all rounding equations must be included, so this is not automatically outside O1. **O2:** cuts combine many clauses and therefore do not assume private-row composition. **O3:** cuts must be generated uniformly for every formula and embedded in one fixed-target CVP—no post hoc separator or filtered search. **O4:** include cuts explicitly separating the known signed kernels. **O5:** higher-rank cuts can detect cube parity, but only a uniform rank bound prevents padding dilution.

**Experiment/falsification.** Generate all rank-one cuts with coefficients in `[-2,2]` for the nine-clause polytope; test the known attacks, then encode surviving cuts and solve the exact CVP. Repeat at rank two only if rank one helps.

**Likely death.** Cutting-plane rank or proof size is exponential; selecting useful cuts may itself require solving the SAT instance.

---

## 6. Segre/exterior-power lift

**Core trick.** Introduce selectors for pairs or `k`-tuples of clause states. Honest assignments produce decomposable tensors, while signed mixtures generally have nonzero exterior minors; linearize the minors with tuple variables and enforce all flattening marginals in the lattice.

**Expected move.** Tensor soundness could make one local defect contaminate many tuples. A sparse perfect-hash family might approximate `k=Θ(log n)` tensorization without enumerating all tuples.

**Obstruction check.** **O1:** linearization auxiliaries are a new slack surface and must be anchored and exactly constrained. **O2:** tuple coordinates couple overlapping and nonoverlapping clauses globally. **O3:** every flattening and auxiliary belongs to the emitted fixed-target instance; no rank filtering after optimization. **O4:** the three- and seven-term mixtures should have nonzero wedge signature, unless an entangled integer tensor cancels it. **O5:** exterior coordinates exceed degree two and replicate defects across tuples, so simple satisfied-clause padding should not preserve constant cost.

**Experiment/falsification.** Build the full pair lift (`k=2`) of the nine-clause instance, explicitly evaluate both known attacks, and run exact low-anchor search. Kill if a rank-one or entangled signed pseudo-tensor attains zero residual.

**Likely death.** Integer tensor products admit cheap entangled vectors; `k=Θ(log n)` has superpolynomial dimension, while sparse compression may amount to rebuilding a PCP.

---

## 7. Higher Lawrence lifting of the global selector matrix

**Core trick.** Apply an `r`-layer Lawrence lifting to the entire selector/consistency matrix, coupling layer aggregates while allowing honest assignments only along a diagonal fiber. Graver-basis structure may force a harmful global kernel move to occupy many layers, converting constant selector excess into `Ω(r)` excess.

**Expected move.** With polynomial `r`, the shortest harmful affine move grows as `r^β` while completeness grows more slowly or can be normalized.

**Obstruction check.** **O1:** no residual slack is introduced; all layer variables receive the same anchor metric. **O2:** the whole overlapping matrix is lifted, rather than composing private clause gadgets. **O3:** the Lawrence matrix and target are explicit; unrestricted kernel search replaces filtered quotient reasoning. **O4:** exact signed kernels are not removed, only purportedly lengthened—so a two-layer realization kills the idea immediately. **O5:** cube parity must replicate across many layers for this to escape constant-cost padding; that is the central test, not an assumption.

**Experiment/falsification.** Construct `r=2,3,4` lifts of the nine-clause matrix and use exact ILP/Graver enumeration to measure the minimum harmful anchor excess. Reject unless it increases at every step.

**Likely death.** Standard Lawrence kernels often contain `(g,-g)` supported on two layers for every base circuit `g`, preserving constant cost regardless of `r`.

Classical touchstones only: polynomial calculus (Clegg–Edmonds–Impagliazzo, 1996), BCH codes (Hocquenghem, 1959; Bose–Ray-Chaudhuri, 1960), Chvátal–Gomory cuts (Gomory, 1958; Chvátal, 1973), and Lawrence/Graver constructions (Sturmfels, *Gröbner Bases and Convex Polytopes*, 1996).
