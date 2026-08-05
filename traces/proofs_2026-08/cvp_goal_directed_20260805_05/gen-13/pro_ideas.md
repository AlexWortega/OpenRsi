No ranking is intended; the six routes use different proof or refutation mechanisms.

### 1. Coprime-cover/Bézout refuter

**Core trick.** Enumerate satisfiable finite covers of an unsatisfiable factor graph. If covers of coprime degrees \(r,s\) exist, an integral Bézout combination of their pushed-down assignment counts has normalization one and satisfies every emitted marginal equation; below the cover injectivity radius, walk features see only combined honest histories.

**Expected move.** Refute FRONTIER by producing bounded-energy zero-residual sections for \(d=\Theta(\log m)\).

**Falsification/experiment.** Enumerate connected \(2\)-, \(3\)-, and \(4\)-lifts of the nine-clause graph; SAT-solve each lift, push assignments down, and optimize Bézout combinations for \(d=1,2,3\). Kill if satisfiable cover degrees have nontrivial gcd or every combination already exceeds \((65/64)^dR^2\).

**Audit.** G1/G6/G7: exact emitted rows, no carries; G12: normalized drops searched; G2/G3: unrestricted integers. G14/G31/G38: an infinite cover family, not shell extrapolation. G5/G9/G11/G13/G15 and G19/GD1/ordered splice: not escaped—these are candidate witnesses. G28/G32/G37: no transfer/additivity; G30: no tensor; GD2/A5: no convolution; G33/G34: no exterior tags; D4 midpoint/nonantipodal/recombination, E6 bounded/unbounded, F289/N8: no shell ports or ramification.

**Likely death.** Cover degrees carry a common torsion divisor.

---

### 2. Saturated Ihara–Bass separation

**Core trick.** Amend bounded-incidence compilation by replacing each variable-occurrence star with a deterministic constant-degree expander of explicitly emitted COPY equalities. On \(K=\ker_{\mathbb Z}[A_F\mid-b_F]\), use an Ihara–Bass/Chebyshev polynomial in the nonbacktracking operator; SNF supplies integral separation from the Dirac sector, while spectral separation amplifies it.

**Expected move.** Prove FRONTIER by a generalized-eigenvalue bound on every saturated-kernel sector, including torsion lifts and cycle space.

**Falsification/experiment.** For parity contradictions of orders \(6,8,10\), compute an SNF basis of \(K\), restrict depth-\(d\) walk Grams to it, and certify the least generalized eigenvalue for \(d=1,2,3\). Kill on any eigenmode growing by at most one.

**Audit.** G1/G6/G7: COPY and residuals emitted; G12: DROP lies in the audited affine kernel; G2/G3: full saturated \(K\). G14/G31/G38: degree-uniform polynomial, not finite extrapolation. G5/G9/G11/G13/G15 and G19/GD1/ordered splice: not assumed away; they must appear as spectral sectors. G28/G32/G37: no finite transfer law; G30: no tensor; GD2/A5: no multiplication algebra; G33/G34: no exterior repair; all D4, E6, and F289/N8 obstructions concern absent shells/modules.

**Likely death.** Signed cycle space contains a unit-modulus nonbacktracking sector.

---

### 3. Twisted-sheaf holonomy

**Core trick.** Regard selector marginals as integral sections of a cellular sheaf on the incidence graph, with clause polarities defining orthogonal transport maps. Choose walk signs as matrix coefficients of parallel transport; a direct integral Hodge decomposition would show that low walk energy forces a global parallel Dirac section.

**Expected move.** Prove FRONTIER by showing every non-Dirac \(H^0\) class or torsion class has a coexact component whose holonomy energy expands exponentially with walk length.

**Falsification/experiment.** Build the sheaf for the nine-clause obstruction, compute integral \(H^0,H^1\) by SNF, and optimize all holonomy features through \(d=3\). Kill if G13 parity or the G19 splice is an actual parallel section.

**Audit.** G1/G6/G7: holonomies are emitted integer features, not filters; G12: drops are sheaf cochains; G2/G3: integral cohomology includes unbounded fibers. G14/G31/G38: proposed theorem is degree-uniform. G5/G9/G11/G13/G15: precisely the \(H^0\)/torsion audit; G19/GD1/ordered splice: included as diagonal sections. G28/G32/G37: Hodge filling, not transfer/additivity; G30: no tensor; GD2/A5: no group algebra; G33/G34: topology here uses no exterior tags; D4, E6, F289/N8 assumptions are absent.

**Likely death.** Affine pseudosections form genuine flat \(H^0\), invisible to all holonomy.

---

### 4. Nonbacktracking expander-code syndromes

**Core trick.** Label directed incidences by columns of an explicit asymptotically good Tanner code and let each walk feature be an integer syndrome accumulated along that path. A direct support-counting argument—not a rejection theorem—would force every nonzero discrepancy class to branch into many nonzero syndromes, while balanced simplex columns keep honest assignments equal-radius.

**Expected move.** Prove FRONTIER through code distance: adverse syndrome support multiplies by at least \(65/64\) per level.

**Falsification/experiment.** Put binary Hamming \([7,4,3]\) labels on the nine-clause graph, enumerate deterministic incidence-label permutations, and run exact zero-residual MIQP for \(d=1,2,3\). Kill if parity, DROP, or diagonal support remains constant.

**Audit.** G1/G6/G7: raw integer syndromes are emitted; no modular carries. G12: DROP is a codeword candidate; G2/G3: unrestricted coefficient module. G14/G31/G38: scalable code family, not finite Walsh inference. G5/G9/G11/G13/G15 and G19/GD1/ordered splice: not automatically escaped; quotient distance against each is the core claim. G28/G32/G37: no transfer table or superadditivity assumption; G30: no Kronecker tensor; GD2/A5: no convolution; G33/G34: no exterior metric; D4, E6, F289/N8 hypotheses are unused.

**Likely death.** The honest affine span lies inside the Tanner code’s zero-syndrome submodule.

---

### 5. \(p\)-adic divisibility propagation

**Core trick.** Homogenize to primitive vectors \((z,1)\in\ker_{\mathbb Z}[A_F\mid-b_F]\) and analyze raw integer walk syndromes through several \(p\)-adic valuations. If too few syndromes are nonzero, nonbacktracking propagation should force every coordinate to be divisible by \(p^d\), contradicting the final coordinate \(1\); modulo \(p\) is only a proof lens, never an external constraint.

**Expected move.** Prove FRONTIER by converting each failed divisibility propagation into a nonzero integer coordinate and hence Euclidean energy.

**Falsification/experiment.** For \(p=2,3,5\), compute depth-\(1,2,3\) syndrome kernels on the nine-clause and two-copy instances, including their SNF torsion, then find the minimum number of violated raw rows. Kill if one primitive adverse class survives every prime.

**Audit.** G1/G6/G7: no slack, quotient, or carries; G12: dropped sections remain primitive candidates; G2/G3: full integer kernel. G14/G31/G38: valuation induction scales with \(d\). G5/G9/G11/G13/G15 and G19/GD1/ordered splice: explicitly reduced at every prime, not presumed absent. G28/G32/G37: no transfer/additivity; G30: no tensor; GD2/A5: no units or convolution; G33/G34: no bivectors; D4, E6, F289/N8 assumptions are irrelevant.

**Likely death.** A local-global affine pseudosection survives over every \(\mathbb Z_p\).

---

### 6. Degree-uniform discrete-convexity certificate

**Core trick.** Let \(\Phi_k\) be full-Walsh energy over all rooted nonbacktracking neighborhoods of depth \(k\). Seek a symbolic identity
\[
\Phi_{k+1}-\frac{65}{64}\Phi_k
=\sum_j q_j(z)^2+\sum_i r_i(z)(A_Fz-b_F)_i,
\]
with equality classified as a common Dirac assignment; integrality supplies strictness without probabilistic testing.

**Expected move.** Prove FRONTIER directly by summing the same local square identity at every depth and controlling boundary multiplicities.

**Falsification/experiment.** Generate the depth-two bounded-degree tree identity by rational SDP, verify it exactly, then test its predicted inequality by certified MIQP at depths \(2,3,4\) on parity contradictions. Kill if any signed branching or diagonal path makes the left side negative.

**Audit.** G1/G6/G7: residual terms are emitted; G12: DROP must satisfy the same identity; G2/G3: polynomial identity holds for all integers. G14/G31/G38: one degree-uniform certificate, not finite-shell extrapolation. G5/G9/G11/G13/G15 and G19/GD1/ordered splice: equality classification must explicitly eliminate them. G28/G32/G37: symbolic convexity, not min-plus or additive composition; G30: no tensor; GD2/A5: no multiplication; G33/G34: no exterior tags; D4, E6, F289/N8 assumptions are absent.

**Likely death.** Signed cancellation violates the proposed branching convexity before depth three.

Classical ingredients invoked above are the Ihara–Bass determinant framework (Bass, 1992) and expander-code distance arguments (Sipser–Spielman, 1996); neither supplies the missing signed-integral theorem by itself.
