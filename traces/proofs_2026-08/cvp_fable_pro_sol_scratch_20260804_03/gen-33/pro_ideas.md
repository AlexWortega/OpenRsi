## 1. Nonabelian holonomy expander

**Mechanism.** Replace additive copy-equalities by edge-bag constraints twisted by explicit noncommuting signed permutations \(S_e\). Honest assignment \(a\) receives a gauge \(g_a\) satisfying every edge, while a signed parity must synchronize around cycles whose holonomy is designed to fix only honest rays.

**Expected move.** Expander-cycle frustration forces either \(n^\alpha\) anchor excess or a nonzero emitted edge residual, which can be polynomially scaled.

**Obstruction audit.** G1: no slack/evaluation residual. G2–3: no fixed local affine fiber. G5: cyclic shared edges, not private rows. G6: every constraint is emitted. G7: no radix; exact kernels remain the key test. G9/G11: not degree-\(\le3\) moments. G12: no single-clause tag. G13: enlarged edge-pair encoding with assignment-dependent gauges, not a raw common syndrome. G14: twists and cycle holonomy are absent from pair bags. G15: nonlaminar. G19: no flow. G28: no identity tile. G30: no Kronecker seed. G31: no block \(H_8\) Gram. G32: noncommuting edge energy, not additive moments.

**Falsification/test.** Enumerate signed-permutation triples on a three-copy triangle; exact-search coefficients in \([-2,2]\), including the two-parity witness. Require cost \(>3d_1^2\).

**Likely death.** A common invariant subspace lets parity synchronize exactly.

---

## 2. Splitter-covered high-order spectra

**Mechanism.** Use an explicit perfect-hash/splitter family to build polynomially many \(k\)-boundary bags, \(k=\Theta(\log n)\), each carrying its complete Walsh spectrum. Any signed pseudodistribution supported on at most \(k\) variables is isolated by some splitter; affine parity may still lift, but must become non-Boolean in many bags.

**Expected move.** Prove a support dichotomy: small attacks pay polynomially replicated anchor excess, while large attacks already have polynomial support.

**Obstruction audit.** G1: no slack. G2–3: not constant local isolation. G5: bags overlap globally, not through private syndromes. G6: all bag coordinates and checks are emitted. G7: no radix. G9/G11: degree grows with \(k\), rather than stopping at two/three. G12: a drop contaminates many scopes, not one tag. G13: not a raw 72-selector hash; its affine collision may remain zero-residual but is intentionally replicated. G14: scopes exceed fixed pairs. G15: splitter DAG, not one laminar tree. G19: no flow. G28: no frozen tile. G30: no tensor. G31: not nine local \(H_8\) blocks. G32: not two-copy moment equality.

**Falsification/test.** For the four-variable obstruction, emit every \(k=4\) scope, lift the G13 affine coefficients, and compare excess against baseline exactly.

**Likely death.** Replication enlarges honest baseline at the same rate, yielding only a constant ratio.

*Classical ingredient: Naor–Schulman–Srinivasan, “Splitters and Near-Optimal Derandomization,” FOCS 1995.*

---

## 3. Integral cohomology / cosystolic encoding

**Mechanism.** Build a clause-assignment cell complex whose integral sections are globally consistent assignments; the target is an explicit cocycle, and the lattice is the integral coboundary lattice. SAT makes the cocycle trivial through an honest section, while UNSAT should leave a nontrivial class with large cosystolic norm.

**Expected move.** An elementary expansion proof for the constructed complex would turn every signed section into many violated cells; scale those emitted coordinates polynomially.

**Obstruction audit.** G1: no slack. G2–3 and G5: no selector-isolation/private-row assumptions. G6: chain maps and target are actual lattice coordinates. G7: no radix, though an exact coboundary is fatal. G9/G11/G31/G32: no bounded moments or Walsh Gram. G12: no clausewise fingerprint. G13: works in a quotient/cohomology group rather than hashing raw selectors. G14/G15: neither pair mesh nor laminar hierarchy. G19: no accepting flow. G28: no min-plus tile. G30: no tensor seed.

**Falsification/test.** Construct the smallest mapping-cone complex for the eight-clause three-variable obstruction. Compute Smith normal form, then exact CVP in the integral coboundary lattice; explicitly test whether the signed three-term and seven-term attacks trivialize the class.

**Likely death.** Formula attachment creates thin cells: a one-clause defect becomes a small boundary, so no cosystolic expansion survives.

---

## 4. Toric border-basis amplifier

**Mechanism.** Lift assignments to squarefree monomials and emit the Boolean border relations \(x_i^2=x_i\), multiplication-table consistency, and clause polynomials. Evaluate every resulting border residual by a multiplicity code, so any nonzero polynomial defect spreads without introducing free slack.

**Expected move.** A direct effective-Nullstellensatz argument at degree \(D=O(\log n)\) would imply that every UNSAT integral pseudomoment has either large support or a multiplicity-code residual.

**Obstruction audit.** G1: no slack; amplification acts on multiplication defects themselves. G2–3/G5: not local affine isolation or private composition. G6: all monomials and border equations are emitted. G7: exact pseudomoments bypass evaluations and are fatal. G9/G11: degree is variable, not fixed at two/three. G12: no single tag. G13: formally outside raw-selector hashing, but its affine combination of full assignments may lift to every monomial and remains a serious obstruction. G14/G15: neither pair bags nor a fixed hierarchy. G19: no flow. G28/G30: no tile/tensor. G31/G32: no fixed Walsh or cross-copy moments.

**Falsification/test.** Emit the degree-four Macaulay/border matrix for the nine-clause instance; exact-search for an integral zero-residual pseudomoment through the G13 anchor budget.

**Likely death.** Known-looking high-degree pseudoassignments persist until \(D=\Theta(n)\), making the lift exponential.

---

## 5. Formula-equivariant PSD synthesis

**Mechanism.** Use cutting-plane SDP to synthesize a rational Gram matrix from a polynomial local template: honest encodings may have different images but equal radius, while every currently known signed shell vector receives larger energy. Seek an explicit association-scheme/Krawtchouk or quadratic-chirp formula for the resulting Gram, then prove its spectral bound directly.

**Expected move.** A distance-distribution inequality could charge every affine parity in proportion to its support and compose without additive block witnesses.

**Obstruction audit.** G1: no slack. G2–3/G5: not affine isolation/private rows. G6: rational factor and center must be emitted. G7: a Gram can charge raw-residual kernels. G9 and G11: unrestricted PSD interactions, not fixed degree-two/three moments. G12: not one top-Walsh tag. G13: unequal honest images avoid the common-syndrome assumption. G14/G15/G19/G28/G30: no pair mesh, hierarchy, flow, tile, or literal tensor. G31: general synthesized Gram, not \(Q=12I+100A^\top A\). G32: interaction need not be additive across copies.

**Falsification/test.** On the rank-72 instance, optimize \(Q\) against all 959 normalized/legal local states plus parity and drop cuts; rationalize \(Q\), factor it, and rerun exact shell DP.

**Likely death.** PSD convexity gives an affine-combination witness with only constant-factor energy, regardless of the chosen Gram.

*Classical ingredient: Delsarte, “An Algebraic Approach to the Association Schemes of Coding Theory,” 1973.*

---

## 6. Iterated Lawrence/Graver lifting

**Mechanism.** Apply \(r\) explicit Lawrence liftings to the Generation-31 residual matrix, adding replica-sum and replica-difference rows. Honest witnesses lift diagonally, but a harmful primitive circuit may be forced to split conformally across \(2^r\) replicas; with \(r=\Theta(\log n)\), its Graver norm could become polynomial.

**Expected move.** Prove that every harmful zero-residual circuit has norm \(n^\alpha\), while honest radius grows more slowly; scale nonzero residuals above that shell.

**Obstruction audit.** G1: no slack. G2–3: global lifting, not three-row local isolation. G5: coupling is through replica sums, not private clause rows. G6: every Lawrence row is emitted. G7: attacks may remain exact kernels, but their norm is the intended amplifier. G9/G11/G12: no fixed moments or tag. G13: the affine collision remains a kernel element; unlike raw hashing, the claim is only that lifting enlarges its support. G14/G15: no pair mesh or laminar tree. G19: no flow. G28: no identity min-plus tile. G30: direct sums with coupling, not Kronecker products. G31: changes the matrix rather than reusing its Gram. G32: replica coupling is nonadditive.

**Falsification/test.** Construct first and second Lawrence lifts of the exact G31 matrix; use MILP/DP to find the minimum lifted parity circuit and compare growth with the lifted control radius.

**Likely death.** A diagonal lift preserves a constant-size circuit, or both harmful and honest norms double identically.

*Classical ingredient: Sturmfels, **Gröbner Bases and Convex Polytopes**, 1996.*

---

## 7. Number-field norm trap without slack

**Mechanism.** Assign each local label an algebraic integer and emit all Minkowski embeddings of shared-label differences. A nonzero algebraic residual has integer norm of magnitude at least one; carefully unbalanced conjugate weights or an \(O(\log n)\)-degree field tower could convert this product bound into polynomial Euclidean distance.

**Expected move.** Obtain exact-fiber separation first, then use the norm inequality to amplify every surviving nonzero residual without PCP-style repetition.

**Obstruction audit.** G1: specifically outside its causal assumption—there is no free integer slack; the norm is applied directly to label differences. G2–3/G5: no local isolation or private rows. G6: every conjugate coordinate is emitted exactly. G7: an exact signed residual kernel still defeats every embedding, so this obstruction applies honestly. G9/G11: no moment truncation. G12: not a single Walsh tag. G13: if all honest images share one target, its affine collision still kills the scheme; assignment-dependent equal-norm images are therefore mandatory. G14/G15/G19/G28/G30: no bags, hierarchy, flow, tile, or tensor seed. G31: algebraic conjugate Gram, not \(H_8\). G32: no additive cross-copy moments.

**Falsification/test.** Search quadratic through degree-six fields for eight label integers; emit exact trace-form Grams and test G7, G11, drop, and two-copy parity witnesses.

**Likely death.** Required honest relations automatically generate the same short integral relation lattice as the signed attacks.
